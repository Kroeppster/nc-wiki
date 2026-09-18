#!/usr/bin/env python3
"""
================================================================================
FIGUREN-GENERATOR GEGEN DIE ECHTEN SERIEN MESSEN
================================================================================
Vergleicht die erzeugten Figuren mit den 200 Figuren aus unseren eigenen
Uebungsserien (2022, 2024, 2025, 2026). Der Generator soll nicht "irgendwie
aehnlich" aussehen, sondern in denselben Zahlenbereichen liegen.

    ~/bin/hugo --minify && (Server auf public/, Port 8123)
    python3 scripts/figuren-vergleichen.py

Ohne Argument holt sich das Skript die erzeugten Figuren selbst (ueber
scripts/figuren-abbild.mjs). Ein bereits vorhandenes Blatt geht auch:

    python3 scripts/figuren-vergleichen.py blatt.png

Eine Zahl als Argument legt fest, wie viele Figuren erzeugt werden (54 sind
die Vorgabe; fuer eine belastbare Aussage eher 150 nehmen, ein Blatt mit 54
Figuren schwankt spuerbar):

    python3 scripts/figuren-vergleichen.py 150

Gebraucht werden pymupdf, numpy und scipy (pip install pymupdf numpy scipy).

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
                fuellgrad=flaeche / (h * b), seitenverh=b / h,
                schwarzanteil=schwarz[0]['anteil'] if schwarz else 0,
                anteile=sorted(f['anteil'] for f in felder),
                laenglich=max(f['laenglich'] for f in felder))


def blatt_messen(bild):
    return [m for f in einzelne_figuren(bild) if (m := messen(*f))]


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


def zeile(name, echt, neu, ziffern=2):
    def z(v):
        return f'{np.mean(v):.{ziffern}f} [{np.percentile(v,10):.{ziffern}f}-{np.percentile(v,90):.{ziffern}f}]'
    daneben = ''
    if abs(np.mean(echt) - np.mean(neu)) > 0.25 * (np.percentile(echt, 90) - np.percentile(echt, 10)):
        daneben = '  <-- weicht ab'
    print(f'  {name:<26} {z(echt):>22}   {z(neu):>22}{daneben}')


def main():
    blatt = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isdigit() else None
    anzahl = next((a for a in sys.argv[1:] if a.isdigit()), '54')
    weg = None
    if not blatt:
        weg = os.path.join(tempfile.mkdtemp(), 'figuren.png')
        print('Erzeuge ein Blatt mit Figuren ...')
        r = subprocess.run(['node', os.path.join(PROJEKT, 'scripts/figuren-abbild.mjs'), weg, anzahl])
        if r.returncode:
            sys.exit('Das Blatt konnte nicht erzeugt werden. Laeuft der Testserver auf Port 8123?')
        blatt = weg
    print('Messe die echten Serien ...')
    echt = echte_figuren()
    neu = blatt_messen(np.array(Image.open(blatt).convert('RGB')))
    if not echt or not neu:
        sys.exit('Zu wenig gemessen - stimmen die Pfade?')

    def anteil5(ms):
        return sum(1 for m in ms if m['felderzahl'] == 5) / len(ms)
    print(f'\n{"":<28} {"ECHT (n=" + str(len(echt)) + ")":>22}   {"ERZEUGT (n=" + str(len(neu)) + ")":>22}')
    print(f'  {"genau fuenf Felder":<26} {anteil5(echt)*100:21.0f}%   {anteil5(neu)*100:21.0f}%')
    e5 = [m for m in echt if m['felderzahl'] == 5]
    n5 = [m for m in neu if m['felderzahl'] == 5]
    if not e5 or not n5:
        sys.exit('Keine Figuren mit fuenf Feldern gefunden.')
    zeile('Nachbarschaften', [m['nachbarn'] for m in e5], [m['nachbarn'] for m in n5])
    zeile('Flaeche/Rahmen', [m['fuellgrad'] for m in e5], [m['fuellgrad'] for m in n5])
    zeile('Seitenverhaeltnis', [m['seitenverh'] for m in e5], [m['seitenverh'] for m in n5])
    zeile('schwarzes Feld', [m['schwarzanteil'] for m in e5], [m['schwarzanteil'] for m in n5])
    zeile('kleinstes Feld', [m['anteile'][0] for m in e5], [m['anteile'][0] for m in n5])
    zeile('groesstes Feld', [m['anteile'][-1] for m in e5], [m['anteile'][-1] for m in n5])
    zeile('laenglichstes Feld', [m['laenglich'] for m in e5], [m['laenglich'] for m in n5])
    print('\n  (Mittelwert, in Klammern der Bereich, in dem 80% der Figuren liegen.)')
    print('  Bei den echten Serien sind die "nicht fuenf Felder" fast immer')
    print('  Messfehler an eng beieinander liegenden Feldern, keine echten Fehler.')
    if weg:
        print(f'\n  Blatt: {weg}')


if __name__ == '__main__':
    main()
