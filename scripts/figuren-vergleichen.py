#!/usr/bin/env python3
"""
================================================================================
FIGUREN-GENERATOR GEGEN DIE ECHTEN SERIEN MESSEN
================================================================================
Vergleicht die erzeugten Figuren mit den echten aus unseren eigenen
Uebungsserien (2022, 2024, 2025, 2026). Der Generator soll nicht "irgendwie
aehnlich" aussehen, sondern in denselben Zahlenbereichen liegen.

    ~/bin/hugo --minify && (Server auf public/, Port 8123)
    python3 scripts/figuren-vergleichen.py [anzahl-serien]

Vorgabe sind 10 Serien zu je 18 Figuren; mehr wird genauer und dauert
laenger. Das Skript holt sich die Figuren selbst (ueber
scripts/figuren-abbild.mjs) und braucht dafuer den laufenden Testserver.

Mit --original <pfad.pdf> kommt zusaetzlich die Seite "Figuren lernen
(Einpraegephase)" aus den offiziellen Beispielaufgaben von swissuniversities
dazu. Das PDF liegt NICHT im Repo (es gehoert nicht uns), zu finden ist es
ueber swissuniversities.ch, Stichwort Beispielaufgaben EMS. Ohne den Schalter
zeigt die Ausgabe die einmal gemessenen Werte des Jahrgangs 2026 aus der
Tabelle weiter unten.

Zwei Dinge dabei im Kopf behalten:
  - Vom Original gibt es nur EINE Serie. Was dort innerhalb der Serie streut,
    ist ein Anhaltspunkt; wie stark sich zwei Serien unterscheiden duerfen,
    sagt diese eine Seite nicht.
  - Die Aufgaben wechseln von Jahr zu Jahr. 2026 sind es glatte Kiesel,
    unsere Serie 2025 ist deutlich kantiger. Beides ist richtig, der
    Generator soll beides koennen.

Gebraucht werden pymupdf, numpy und scipy (pip install pymupdf numpy scipy).

ES GIBT ZWEI TEILE, und der zweite ist der wichtigere:

  TEIL 1 vergleicht die Figuren EINZELN, zusammengeworfen ueber alle Serien.
  Er beantwortet: Sieht eine Figur aus wie eine echte?

  TEIL 2 vergleicht GANZE SERIEN miteinander. Er beantwortet: Sehen zwei
  Durchlaeufe verschieden aus? Dass sich die Figuren INNERHALB einer Serie
  aehneln, ist richtig so - man muss sie ja auseinanderhalten koennen, das
  ist die Aufgabe. Zwei verschiedene Serien sollen dagegen erkennbar anders
  wirken, so wie unsere Serien 2022, 2025 und 2026 es untereinander tun.
  Teil 1 kann perfekt aussehen, waehrend Teil 2 zeigt, dass alle Serien
  einander gleichen - genau dieser Fall lag vor, bevor der Generator seinen
  Stil je Serie wuerfelte: Ueber acht Serien lag der Fuellgrad zwischen 0.68
  und 0.70, bei elf echten Serien zwischen 0.63 und 0.79.

WAS GEMESSEN WIRD - und warum genau das:
  Felder je Figur    Muss 5 sein. Der erste Entwurf legte Trennlinien quer
                     ueber die Figur; in einer eingebuchteten Form zerfiel
                     ein Feld dann in zwei Flecken oder verschwand. Ergebnis:
                     Die Figur zeigte vier oder sechs Flecken, obwohl fuenf
                     Antworten zur Wahl stehen. Das ist kein Schoenheits-
                     fehler, sondern eine unloesbare Aufgabe.
  Nachbarschaften    Wie viele der zehn moeglichen Feldpaare aneinander
                     grenzen. Fuenf Streifen ergeben 4 - eine Kette. Die
                     echten Figuren liegen bei 7.9: ein Netz. Das ist der
                     Unterschied, den man auf den ersten Blick sieht.
  Flaeche/Rahmen     Wie sehr die Form ihren Rahmen ausfuellt. Klein heisst
                     zerklueftet, gross heisst rund und langweilig.
  Seitenverhaeltnis  Breit oder hochkant. Ohne Streuung sehen alle Figuren
                     gleich aus.
  Feldgroessen       Kleinstes und groesstes Feld. Sind alle gleich gross,
                     wirkt die Figur wie eine Wabe statt wie eine Aufteilung.
  laenglichstes Feld Bei den echten zieht sich meist ein Feld lang an der
                     Kontur entlang.

ZUR MESSUNG SELBST: Sie liest Bilder, keine Zeichenbefehle - die Figuren in
den PDFs sind Rasterbilder. Weisse und schwarze Flaechen innerhalb der Kontur
sind die Felder; alles unter 2% der Figurflaeche gilt als Rest. Die Werte fuer
das schwarze Feld liegen systematisch etwas hoeher als bei den weissen, weil
die Umrandung mitgezaehlt wird - das betrifft echte und erzeugte Figuren
gleichermassen und stoert den Vergleich deshalb nicht.
================================================================================
"""
import os, sys, glob, subprocess, tempfile, collections
try:
    import numpy as np, pymupdf
    from scipy import ndimage
    from PIL import Image
except ImportError as fehlt:
    sys.exit(f'Fehlendes Paket: {fehlt.name}. Bitte "pip install pymupdf numpy scipy pillow".')

PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIEN = os.path.join(PROJEKT, 'assets/downloads/uebungsaufgaben/figuren-fakten-lernen')

# Einmal gemessen an der Seite "Figuren lernen (Einpraegephase)" der
# offiziellen Beispielaufgaben 2026 von swissuniversities (18 Figuren).
# Format: Mittelwert, 10er-, 90er-Perzentil. Das PDF selbst liegt nicht im
# Repo; mit --original <pfad.pdf> laesst sich das hier nachrechnen.
ORIGINAL_2026 = {
    'genau fuenf Felder': (1.00, 1.00, 1.00),
    'Nachbarschaften': (7.89, 7.00, 9.00),
    'Flaeche/Rahmen': (0.74, 0.62, 0.86),
    'Seitenverhaeltnis': (1.02, 0.92, 1.14),
    'schwarzes Feld': (0.26, 0.21, 0.31),
    'kleinstes Feld': (0.12, 0.08, 0.16),
    'groesstes Feld': (0.31, 0.24, 0.38),
    'laenglichstes Feld': (1.89, 1.34, 2.37),
    # Groessenstreuung innerhalb der einen Originalserie: praktisch keine.
    'Groesse CV': (0.027, 0.95, 1.05),
}


def einzelne_figuren(bild):
    """Schneidet ein Blatt in einzelne Figuren."""
    grau = bild[:, :, :3].mean(axis=2) if bild.ndim == 3 else bild.astype(float)
    tinte = grau < 200
    lab, n = ndimage.label(ndimage.binary_dilation(tinte, np.ones((9, 9))))
    raus = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 4000:                      # Text, Logo, Seitenzahl
            continue
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        if (y1 - y0) < 60 or (x1 - x0) < 60:
            continue
        raus.append((grau[y0:y1 + 1, x0:x1 + 1], tinte[y0:y1 + 1, x0:x1 + 1]))
    return raus


def messen(grau, tinte):
    frei = ~tinte
    rand = np.zeros_like(frei)
    rand[0, :], rand[-1, :] = frei[0, :], frei[-1, :]
    rand[:, 0], rand[:, -1] = frei[:, 0], frei[:, -1]
    innen = ~ndimage.binary_propagation(rand, mask=frei)
    flaeche = innen.sum()
    if flaeche < 2000:
        return None
    marke = np.zeros(innen.shape, dtype=int)
    felder, k = [], 0
    for maske, ist_schwarz in [(innen & (grau > 200), False), (innen & (grau < 80), True)]:
        lab, n = ndimage.label(maske)
        for i in range(1, n + 1):
            m = lab == i
            g = m.sum()
            if g < flaeche * 0.02:
                continue
            k += 1
            marke[m] = k
            ys, xs = np.where(m)
            h, b = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
            felder.append(dict(anteil=g / flaeche, schwarz=ist_schwarz, laenglich=max(h, b) / min(h, b)))
    if not felder:
        return None
    nachbarn = 0
    if k > 1:
        breit = {i: ndimage.binary_dilation(marke == i, np.ones((9, 9))) for i in range(1, k + 1)}
        for i in range(1, k + 1):
            for j in range(i + 1, k + 1):
                if (breit[i] & breit[j]).sum() > 25:
                    nachbarn += 1
    ys, xs = np.where(innen)
    h, b = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    schwarz = [f for f in felder if f['schwarz']]
    return dict(felderzahl=len(felder), nachbarn=nachbarn,
                # Fuer die Groesse die RAHMENDIAGONALE, nicht die Flaeche:
                # Die Flaeche mischt Groesse und Form - eine tief eingekerbte
                # Figur hat bei gleicher Spannweite weniger davon.
                groesse=float(np.hypot(h, b)),
                fuellgrad=flaeche / (h * b), seitenverh=b / h,
                schwarzanteil=schwarz[0]['anteil'] if schwarz else 0,
                anteile=sorted(f['anteil'] for f in felder),
                laenglich=max(f['laenglich'] for f in felder))


def ist_figur(m):
    """Figur oder Beiwerk?

    Auf den echten Blaettern stehen ausser den 18 Figuren noch das Logo (oben
    rechts) und das Lizenz-Abzeichen (unten). Beide sind gross genug, um als
    Flaeche erkannt zu werden - und weil sie ganz andere Groessen haben als
    die Figuren, haben sie die gemessene Groessenstreuung von 6% auf 20%
    aufgeblaeht. Der Generator wurde daraufhin auf eine Streuung eingestellt,
    die es in den echten Serien gar nicht gibt.
    Eine Figur hat vier bis sechs Felder, hoechstens die Haelfte davon
    schwarz, und fuellt ihren Rahmen weder fast ganz noch fast gar nicht.
    """
    return (m is not None and 4 <= m['felderzahl'] <= 6
            and m['schwarzanteil'] < 0.5 and 0.35 < m['fuellgrad'] < 0.95)


def blatt_messen(bild):
    return [m for f in einzelne_figuren(bild)
            if (m := messen(*f)) and ist_figur(m)]


def echte_figuren():
    alle = []
    for datei in sorted(glob.glob(os.path.join(SERIEN, '*figuren-einpraegen*.pdf'))):
        if 'Loesung' in os.path.basename(datei):
            continue
        d = pymupdf.open(datei)
        pix = d[0].get_pixmap(dpi=200)
        bild = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        alle += blatt_messen(bild)
    return alle


def zeile(name, echt, neu, orig=None, ziffern=2):
    def z(v):
        return f'{np.mean(v):.{ziffern}f} [{np.percentile(v,10):.{ziffern}f}-{np.percentile(v,90):.{ziffern}f}]'
    if orig is None:
        orig = ORIGINAL_2026.get(name)
    if isinstance(orig, tuple):
        ospalte = f'{orig[0]:.{ziffern}f} [{orig[1]:.{ziffern}f}-{orig[2]:.{ziffern}f}]'
    else:
        ospalte = z(orig)
    daneben = ''
    if abs(np.mean(echt) - np.mean(neu)) > 0.25 * (np.percentile(echt, 90) - np.percentile(echt, 10)):
        daneben = '  <-- weicht ab'
    print(f'  {name:<22} {ospalte:>20} {z(echt):>20} {z(neu):>20}{daneben}')


def serienwerte(ms):
    """Kennwerte EINER Serie."""
    f5 = [m for m in ms if m['felderzahl'] == 5]
    if len(f5) < 6:
        return None
    return dict(
        nachbarn=np.mean([m['nachbarn'] for m in f5]),
        fuellgrad=np.mean([m['fuellgrad'] for m in f5]),
        laenglich=np.mean([m['laenglich'] for m in f5]),
        kleinstes=np.mean([m['anteile'][0] for m in f5]),
        groesstes=np.mean([m['anteile'][-1] for m in f5]),
        # Wie stark die Figuren einer Serie in der GROESSE schwanken.
        groessenspiel=float(np.std([m['groesse'] for m in f5]) / np.mean([m['groesse'] for m in f5])))


def original_lesen(pfad):
    """Die Einpraegephase-Seite aus den offiziellen Beispielaufgaben messen."""
    d = pymupdf.open(pfad)
    for nr in range(d.page_count):
        t = d[nr].get_text()
        if 'Figuren lernen' in t and 'Einpr' in t and nr + 1 < d.page_count:
            pix = d[nr + 1].get_pixmap(dpi=250)   # die Figuren stehen auf der Folgeseite
            bild = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            ms = blatt_messen(bild)
            if len(ms) >= 12:
                return ms, f'{os.path.basename(pfad)[:18]} S.{nr+2}'
    return None, None


def main():
    serien = int(next((a for a in sys.argv[1:] if a.isdigit()), '10'))
    orig, original_quelle = None, '2026'
    if '--original' in sys.argv:
        pfad = sys.argv[sys.argv.index('--original') + 1]
        orig, quelle = original_lesen(pfad)
        if not orig:
            sys.exit(f'In {pfad} keine Figurenseite gefunden.')
        original_quelle = quelle
        print(f'Original gemessen: {len(orig)} Figuren aus {quelle}')
    o5liste = [m for m in orig if m['felderzahl'] == 5] if orig else None
    ordner = tempfile.mkdtemp()
    print(f'Erzeuge {serien} Serien ...')
    r = subprocess.run(['node', os.path.join(PROJEKT, 'scripts/figuren-abbild.mjs'),
                        os.path.join(ordner, 'serie.png'), str(serien), '--je-serie'])
    if r.returncode:
        sys.exit('Die Serien konnten nicht erzeugt werden. Laeuft der Testserver auf Port 8123?')
    print('Messe die echten Serien ...')
    echt_serien, echt = [], []
    for datei in sorted(glob.glob(os.path.join(SERIEN, '*figuren-einpraegen*.pdf'))):
        if 'Loesung' in os.path.basename(datei):
            continue
        d = pymupdf.open(datei)
        pix = d[0].get_pixmap(dpi=200)
        bild = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        ms = blatt_messen(bild)
        echt += ms
        w = serienwerte(ms)
        if w:
            echt_serien.append(w)
    neu_serien, neu = [], []
    for datei in sorted(glob.glob(os.path.join(ordner, 'serie-*.png'))):
        ms = blatt_messen(np.array(Image.open(datei).convert('RGB')))
        neu += ms
        w = serienwerte(ms)
        if w:
            neu_serien.append(w)
    if not echt or not neu:
        sys.exit('Zu wenig gemessen - stimmen die Pfade?')

    def anteil5(ms):
        return sum(1 for m in ms if m['felderzahl'] == 5) / len(ms)
    print('\nTEIL 1 - DIE EINZELNE FIGUR')
    print(f'  {"":<22} {"ORIGINAL " + str(original_quelle):>20} {"unsere Serien":>20} {"ERZEUGT":>20}')
    print(f'  {"":<22} {"(18 Figuren)":>20} {"(n=" + str(len(echt)) + ")":>20} {"(n=" + str(len(neu)) + ")":>20}')
    o5 = (f'{anteil5(orig)*100:.0f}%' if orig else f'{ORIGINAL_2026["genau fuenf Felder"][0]*100:.0f}%')
    print(f'  {"genau fuenf Felder":<22} {o5:>20} {anteil5(echt)*100:19.0f}% {anteil5(neu)*100:19.0f}%')
    e5 = [m for m in echt if m['felderzahl'] == 5]
    n5 = [m for m in neu if m['felderzahl'] == 5]
    if not e5 or not n5:
        sys.exit('Keine Figuren mit fuenf Feldern gefunden.')
    zeile('Nachbarschaften', [m['nachbarn'] for m in e5], [m['nachbarn'] for m in n5],
          [m['nachbarn'] for m in o5liste] if o5liste else None)
    zeile('Flaeche/Rahmen', [m['fuellgrad'] for m in e5], [m['fuellgrad'] for m in n5],
          [m['fuellgrad'] for m in o5liste] if o5liste else None)
    zeile('Seitenverhaeltnis', [m['seitenverh'] for m in e5], [m['seitenverh'] for m in n5],
          [m['seitenverh'] for m in o5liste] if o5liste else None)
    zeile('schwarzes Feld', [m['schwarzanteil'] for m in e5], [m['schwarzanteil'] for m in n5],
          [m['schwarzanteil'] for m in o5liste] if o5liste else None)
    zeile('kleinstes Feld', [m['anteile'][0] for m in e5], [m['anteile'][0] for m in n5],
          [m['anteile'][0] for m in o5liste] if o5liste else None)
    zeile('groesstes Feld', [m['anteile'][-1] for m in e5], [m['anteile'][-1] for m in n5],
          [m['anteile'][-1] for m in o5liste] if o5liste else None)
    zeile('laenglichstes Feld', [m['laenglich'] for m in e5], [m['laenglich'] for m in n5],
          [m['laenglich'] for m in o5liste] if o5liste else None)
    print('  (Mittelwert, in Klammern der Bereich, in dem 80% der Figuren liegen.)')
    print('  Bei den echten Serien sind die "nicht fuenf Felder" fast immer')
    print('  Messfehler an eng beieinander liegenden Feldern, keine echten Fehler.')

    print(f'\nTEIL 2 - UNTERSCHIEDE ZWISCHEN GANZEN SERIEN')
    print(f'{"":<28} {"ECHT (" + str(len(echt_serien)) + " Serien)":>22}   {"ERZEUGT (" + str(len(neu_serien)) + " Serien)":>22}')
    for feld, name in [('nachbarn', 'Nachbarschaften'), ('fuellgrad', 'Flaeche/Rahmen'),
                       ('laenglich', 'laenglichstes Feld'), ('kleinstes', 'kleinstes Feld'),
                       ('groesstes', 'groesstes Feld'), ('groessenspiel', 'Groessenstreuung in Serie')]:
        e = np.array([w[feld] for w in echt_serien])
        n = np.array([w[feld] for w in neu_serien])
        warnung = '  <-- zu wenig Unterschied' if n.std() < e.std() * 0.55 else ''
        print(f'  {name:<26} {e.min():7.2f}..{e.max():<6.2f} +-{e.std():.3f}   '
              f'{n.min():7.2f}..{n.max():<6.2f} +-{n.std():.3f}{warnung}')
    o = ORIGINAL_2026['Groesse CV']
    print(f'  (Zum Vergleich: die eine Originalserie 2026 streut in der Groesse um '
          f'{o[0]:.3f} -')
    print(f'   ihre kleinste Figur misst {o[1]:.2f}, ihre groesste {o[2]:.2f} des Schnitts.)')
    print('  (Kleinster und groesster SERIENWERT, dahinter die Streuung zwischen')
    print('  den Serien. Je groesser die Streuung, desto verschiedener wirken')
    print('  zwei Durchlaeufe. Zu kleine Streuung heisst: alle Serien gleichen')
    print('  einander, auch wenn Teil 1 stimmt.)')
    print(f'\n  Blaetter: {ordner}')


if __name__ == '__main__':
    main()
