# -*- coding: utf-8 -*-
"""Schneidet eine Sprachaufnahme in die Ansagen des Simulationsmodus.

WOZU: Die Ansagen (assets/audio/simulationsmodus/<sprache>/*.mp3) werden pro Sprache
in EINEM Durchgang aufgenommen, z. B. mit Google AI Studio: alle 30 Sätze untereinander.
Die Pausen zwischen den Sätzen sind dabei oft nicht länger als die innerhalb eines
Satzes - an den Pausen allein lässt sich also nicht schneiden. Dieses Skript kennt den
Text jedes Satzes (aus der Tabelle in assets/audio/simulationsmodus/README.md) und damit
seine ungefähre Länge. Es verteilt die Sprachstücke so auf die Sätze, dass die Längen
am besten passen, und prüft danach, dass jede Kurzansage («Muster zuordnen.») wie der
Anfang der passenden langen Ansage klingt.

AUFRUF (ffmpeg muss installiert sein; einmalig: pip install numpy scipy pyyaml):

    python3 scripts/ansagen-schneiden.py ansagen-de.wav de assets/audio/simulationsmodus/de
    python3 scripts/ansagen-schneiden.py konz-instruktion-de.wav de assets/audio/simulationsmodus/de --instruktion

Mit --instruktion wird die Aufnahme der Instruktion zum Konzentrationstest nicht
geschnitten, sondern nach dem Satz zum Beispiel («Schauen Sie sich das Beispiel kurz
an.») auf gut 10 Sekunden Stille verlängert - so wie die Aufsicht im Saal wartet.
Gefunden wird der Satz über dieselbe Längenrechnung, Satz für Satz (Text aus
i18n/<sprache>.yaml, pm_konz_instruktion_ansage).

Ausgabe: MP3, mono, 96 kbit/s, Lautheit -18 LUFS, vorne und hinten 0,5 s Stille.
Vor dem Hochladen die Dateien anhören - das Skript prüft Längen und Klang, nicht den
Inhalt.
"""
import math, os, re, subprocess, sys, tempfile, wave
import numpy as np
from scipy.fft import dct
from scipy.signal import stft

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(WURZEL, 'assets/audio/simulationsmodus/README.md')
ABSCHNITT = {'de': '## Deutsch', 'fr': '## Français', 'it': '## Italiano'}
ZAHLEN = {'de': {'1': 'eins', '4': 'vier', '5': 'fünf', '6': 'sechs', '8': 'acht', '10': 'zehn', '16': 'sechzehn', '18': 'achtzehn', '40': 'vierzig', '45': 'fünfundvierzig'},
          'fr': {'1': 'une', '4': 'quatre', '5': 'cinq', '6': 'six', '8': 'huit', '10': 'dix', '16': 'seize', '18': 'dix-huit', '40': 'quarante', '45': 'quarante-cinq'},
          'it': {'1': 'uno', '4': 'quattro', '5': 'cinque', '6': 'sei', '8': 'otto', '10': 'dieci', '16': 'sedici', '18': 'diciotto', '40': 'quaranta', '45': 'quarantacinque'}}
PAUSE_BEISPIEL = 10.0   # Sekunden Stille nach dem Satz zum Beispiel


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True)


def lade(pfad):
    with wave.open(pfad) as f:
        return f.getframerate(), np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16)


def speichere(pfad, rate, x):
    with wave.open(pfad, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate); f.writeframes(x.astype(np.int16).tobytes())


def als_mp3(wav, mp3):
    ffmpeg('-i', wav, '-af', 'adelay=500:all=1,apad=pad_dur=0.5', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '96k', mp3)


def silben(text, sprache):
    """Ungefähre Sprechlänge eines Satzes: Silben plus etwas für jedes Satzzeichen."""
    t = re.sub(r'\d+', lambda m: ' ' + ZAHLEN[sprache].get(m.group(0), m.group(0)) + ' ', text.lower())
    return len(re.findall(r'[aeiouyäöüàâéèêëîïôùûœ]+', t)) + 1.5 * len(re.findall(r'[.,;:!?–]', text))


def sprachstuecke(rate, x):
    """Zusammenhängende Stellen mit Sprache, in Sekunden (Anfang, Ende)."""
    hop = int(rate * 0.01)
    x = x.astype(float)
    db = 20 * np.log10(np.sqrt(np.convolve(x**2, np.ones(hop*2) / (hop*2), mode='same')[::hop] + 1e-9) / 32768)
    still = db < max(-45, np.percentile(db, 95) - 38)
    stuecke, i = [], 0
    while i < len(still):
        if still[i]:
            i += 1; continue
        j = i
        while j < len(still) and not still[j]: j += 1
        if stuecke and i - stuecke[-1][1] < 15: stuecke[-1][1] = j   # Lücken unter 0,15 s füllen
        else: stuecke.append([i, j])
        i = j
    stuecke = [s for s in stuecke if s[1] - s[0] >= 4]
    return np.array([s[0] for s in stuecke]) * 0.01, np.array([s[1] for s in stuecke]) * 0.01


def zuordnen(anf, end, gewichte):
    """Teilt die Sprachstücke der Reihe nach auf die Sätze auf (dynamische
    Programmierung): Jede Satzlänge soll zur geschätzten Länge passen, lange Pausen
    sind als Grenze bevorzugt. Gibt je Satz (erstes Stück, Stück nach dem letzten)."""
    M, L = len(anf), len(gewichte)
    if M < L:
        sys.exit(f'Nur {M} Sprachstücke für {L} Sätze - fehlen Sätze in der Aufnahme?')
    luecke = np.append(anf[1:] - end[:-1], 9.0)

    def loesen(k):
        best = np.full((L + 1, M + 1), np.inf); zurueck = np.zeros((L + 1, M + 1), int); best[0, 0] = 0
        for i in range(1, L + 1):
            for b in range(i, M + 1):
                for a in range(i - 1, b):
                    if best[i-1, a] == np.inf: continue
                    c = best[i-1, a] + math.log((end[b-1] - anf[a]) / (k * gewichte[i-1]))**2 - 1.2 * min(luecke[b-1], 2.0)
                    if c < best[i, b]: best[i, b] = c; zurueck[i, b] = a
        grenzen, b = [], M
        for i in range(L, 0, -1):
            a = zurueck[i, b]; grenzen.append((a, b)); b = a
        return grenzen[::-1]

    k = (end[-1] - anf[0] - 0.7 * (L - 1)) / sum(gewichte)
    for _ in range(3):
        g = loesen(k)
        k = float(np.median([(end[b-1] - anf[a]) / gewichte[i] for i, (a, b) in enumerate(g)]))
    return g, k, luecke


def klang(rate, x):
    """MFCC-ähnliche Merkmale für den Klangvergleich."""
    f, _, Z = stft(x.astype(float), rate, nperseg=512, noverlap=352)
    mel = lambda hz: 2595 * np.log10(1 + hz / 700)
    kanten = 700 * (10**(np.linspace(mel(60), mel(8000), 42) / 2595) - 1)
    fb = np.array([np.clip(np.minimum((f - kanten[i]) / (kanten[i+1] - kanten[i]), (kanten[i+2] - f) / (kanten[i+2] - kanten[i+1])), 0, None) for i in range(40)])
    M = dct(np.log(fb @ np.abs(Z)**2 + 1e-6), axis=0, norm='ortho')[1:14]
    return ((M - M.mean(1, keepdims=True)) / (M.std(1, keepdims=True) + 1e-6)).T


def abstand(A, B):
    D = np.full((len(A) + 1, len(B) + 1), np.inf); D[0, 0] = 0
    C = np.linalg.norm(A[:, None] - B[None], axis=2)
    for i in range(1, len(A) + 1):
        for j in range(1, len(B) + 1):
            D[i, j] = C[i-1, j-1] + min(D[i-1, j], D[i, j-1], D[i-1, j-1])
    return D[-1, -1] / (len(A) + len(B))


def saetze_aus_readme(sprache):
    text = open(README, encoding='utf-8').read()
    teil = text[text.index(ABSCHNITT[sprache]):]
    teil = teil[:teil.index('\n---') if '\n---' in teil else len(teil)]
    return [(m.group(1), m.group(2).strip()) for m in re.finditer(r'^\| `([\w-]+)\.mp3` \| (.+?) \|$', teil, re.M)
            if m.group(1) != 'konz-instruktion']


def ansagen(wav, sprache, ziel, arbeit):
    saetze = saetze_aus_readme(sprache)
    rate, x = lade(wav)
    anf, end = sprachstuecke(rate, x)
    g, k, luecke = zuordnen(anf, end, [silben(t, sprache) for _, t in saetze])
    print(f'{len(anf)} Sprachstücke, {len(saetze)} Sätze, {k:.3f} s pro Silbe')
    stuecke = {}
    for (name, text), (a, b) in zip(saetze, g):
        dauer = end[b-1] - anf[a]; verh = dauer / (k * silben(text, sprache))
        warnung = '   <- Länge prüfen' if not 0.6 <= verh <= 1.5 else ''
        print(f'  {name:32s} {anf[a]:7.2f}-{end[b-1]:7.2f}  {dauer:5.2f} s  ({verh:4.2f}){warnung}')
        stuecke[name] = x[max(0, int((anf[a] - 0.08) * rate)):int((end[b-1] + 0.12) * rate)]
    # Gegenprobe: Kurzansage = Anfang der langen Ansage
    lang = [n[:-5] for n in stuecke if n.endswith('-kurz') and n[:-5] in stuecke]
    merkmale = {n: klang(rate, stuecke[n]) for n in stuecke}
    falsch = []
    for n in lang:
        kurz = merkmale[n + '-kurz']
        werte = {m: abstand(kurz, merkmale[m][:int(len(kurz) * 1.15)]) for m in lang}
        if min(werte, key=werte.get) != n: falsch.append(n)
    print(f'Gegenprobe: {len(lang) - len(falsch)}/{len(lang)} Kurzansagen passen zur langen Ansage')
    if falsch:
        sys.exit('Nicht eindeutig: ' + ', '.join(falsch) + ' - nichts geschrieben. Aufnahme anhören, ggf. neu erzeugen.')
    os.makedirs(ziel, exist_ok=True)
    for name, y in stuecke.items():
        tmp = os.path.join(arbeit, name + '.wav')
        speichere(tmp, rate, y)
        als_mp3(tmp, os.path.join(ziel, name + '.mp3'))
    print(f'{len(stuecke)} Dateien nach {ziel} geschrieben')


def instruktion(wav, sprache, ziel, arbeit):
    import yaml
    text = yaml.safe_load(open(os.path.join(WURZEL, f'i18n/{sprache}.yaml'), encoding='utf-8'))['pm_konz_instruktion_ansage']
    absaetze = [a.strip() for a in text.split('\n\n') if a.strip()]
    saetze, ende_beispiel = [], None
    for absatz in absaetze:
        for s in re.split(r'(?<=[.!?])\s+', absatz):
            saetze.append(s)
        if re.search(r'korrekt bearbeitet|traité correctement|elaborata correttamente', absatz):
            ende_beispiel = len(saetze) - 1   # letzter Satz des Absatzes mit dem Beispiel
    rate, x = lade(wav)
    anf, end = sprachstuecke(rate, x)
    g, k, luecke = zuordnen(anf, end, [silben(s, sprache) for s in saetze])
    a, b = g[ende_beispiel]
    print(f'Satz zum Beispiel: «{saetze[ende_beispiel]}» {anf[a]:.2f}-{end[b-1]:.2f} s, Pause danach {luecke[b-1]:.2f} s')
    schnitt = int((end[b-1] + min(0.5, luecke[b-1] / 2)) * rate)
    still = np.zeros(int(max(0.0, PAUSE_BEISPIEL - luecke[b-1]) * rate), dtype=np.int16)
    y = np.concatenate([x[max(0, int((anf[0] - 0.08) * rate)):schnitt], still, x[schnitt:int((end[-1] + 0.15) * rate)]])
    tmp = os.path.join(arbeit, 'instruktion.wav')
    speichere(tmp, rate, y)
    os.makedirs(ziel, exist_ok=True)
    als_mp3(tmp, os.path.join(ziel, 'konz-instruktion.mp3'))
    print(f'konz-instruktion.mp3 geschrieben ({len(y) / rate:.0f} s)')


if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[2] not in ABSCHNITT:
        sys.exit(__doc__)
    quelle, sprache, ziel = sys.argv[1:4]
    with tempfile.TemporaryDirectory() as arbeit:
        norm = os.path.join(arbeit, 'norm.wav')
        ffmpeg('-i', quelle, '-af', 'loudnorm=I=-18:TP=-1.5:LRA=7', '-ar', '24000', '-ac', '1', '-c:a', 'pcm_s16le', norm)
        (instruktion if '--instruktion' in sys.argv else ansagen)(norm, sprache, ziel, arbeit)
