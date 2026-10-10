#!/usr/bin/env python3
"""
================================================================================
KONZENTRATIONSTEST: RASTER UND LÖSUNG FÜR «KONZTEST AUSWERTEN» AUSLESEN
================================================================================
Liest aus dem Testheft und dem Lösungs-PDF einer Testsimulation den
Konzentrationstest (40 Zeilen zu 40 Zeichen) und schreibt nach
data/konztest.yaml:
  - welches Zeichen wo steht (das Raster; die Auswertung erkennt daran, wie
    der Bogen auf dem Foto liegt),
  - wo die Mitte jeder Zeile und Spalte liegt (pt),
  - welche Zeichen zu markieren sind (die Lösung).

    pip install pymupdf numpy
    python3 scripts/konztest-loesungen.py            # nur prüfen und zeigen
    python3 scripts/konztest-loesungen.py --schreiben

ZWEI QUELLEN, EINE PRÜFUNG: Die Zeichen stehen im Testheft als Text in einer
eigenen Schrift (ein Zeichen 0-F je Symbol), die Lösung im Lösungs-PDF als
schwarze Kästchen. Beides muss zur Regel der Anleitung passen («markieren,
wenn die Pfeilrichtung mit der Öffnungsrichtung des darauf folgenden
Zeichens übereinstimmt»; Pfeil = Zeichen mod 4, Öffnung = Zeichen div 4).
Stimmt auch nur ein Feld nicht, bricht das Skript ab.

Aktuell nur 2026: Ältere Jahre haben die Zeichen als Bilder im PDF und
keine Lösung, die sich so lesen lässt (siehe docs/WARTUNG-DETAILLIERT.md 11).
================================================================================
"""
import sys

try:
    import numpy as np
    import pymupdf
except ImportError:
    sys.exit('Fehlt: pymupdf und numpy. Installieren mit "pip install pymupdf numpy".')

ORDNER = 'assets/downloads/testsimulationen/'
ZIEL = 'data/konztest.yaml'
JAHRE = {
    2026: dict(heft='2026_testsimulationen_Testsimulation.pdf', seite=84, schrift='KonzTestsim2026',
               loesung='2026_testsimulationen_Loesung.pdf', loesung_seite=1),
}
N = 40


def lesen(j):
    heft = pymupdf.open(ORDNER + j['heft'])[j['seite']]
    loes = pymupdf.open(ORDNER + j['loesung'])[j['loesung_seite']]
    # Mitten der Kästchen im Lösungs-PDF (sie stehen genau auf den Zeichen)
    q = [z['rect'] for z in loes.get_drawings()
         if 7 < z['rect'].width < 9 and 7 < z['rect'].height < 9 and z['rect'].y0 > 180]
    # Kästchen doppelt gezeichnet (Rahmen, Füllung) und auf Hundertstel
    # verschieden: Mitten innerhalb von 1 pt zusammenfassen
    def gruppen(werte):
        g = []
        for v in sorted(werte):
            if g and v - g[-1][-1] < 1:
                g[-1].append(v)
            else:
                g.append([v])
        return [sum(x) / len(x) for x in g]
    xs = gruppen((r.x0 + r.x1) / 2 for r in q)
    ys = gruppen((r.y0 + r.y1) / 2 for r in q)
    if len(ys) != N or len(xs) != N:
        sys.exit('%s: %d x %d Kästchen statt 40 x 40' % (j['loesung'], len(xs), len(ys)))
    # Zeichen: jedes zur nächsten Mitte
    zeichen = [[None] * N for _ in range(N)]
    for b in heft.get_text('rawdict')['blocks']:
        for line in b.get('lines', []):
            for s in line['spans']:
                if j['schrift'] not in s['font']:
                    continue
                for c in s['chars']:
                    gx, gy = (c['bbox'][0] + c['bbox'][2]) / 2, (c['bbox'][1] + c['bbox'][3]) / 2
                    if not c['c'].strip() or gy < 180:
                        continue
                    r = int(np.argmin([abs(gy - y) for y in ys]))
                    k = int(np.argmin([abs(gx - x) for x in xs]))
                    if zeichen[r][k] is not None:
                        sys.exit('Zwei Zeichen auf Zeile %d, Platz %d' % (r + 1, k + 1))
                    zeichen[r][k] = c['c'].upper()
    if any(z is None for zeile in zeichen for z in zeile):
        sys.exit('Nicht alle 1600 Zeichen gefunden')
    # Lösung: schwarz gefüllte Kästchen (gerendert, in der Mitte gemessen)
    s = 200 / 72
    pix = loes.get_pixmap(dpi=200)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3].mean(axis=2)
    ziele = [''.join('1' if a[int(y * s) - 4:int(y * s) + 5, int(x * s) - 4:int(x * s) + 5].mean() < 100 else '0'
                     for x in xs) for y in ys]
    # Gegenprobe mit der Regel
    for r in range(N):
        for k in range(N):
            regel = k < N - 1 and int(zeichen[r][k], 16) % 4 == int(zeichen[r][k + 1], 16) // 4
            if regel != (ziele[r][k] == '1'):
                sys.exit('Lösung und Regel widersprechen sich: Zeile %d, Zeichen %d' % (r + 1, k + 1))
    return {'x': xs, 'y': ys, 'zeichen': [''.join(z) for z in zeichen], 'ziele': ziele}


def main():
    aus = '''# ============================================================================
# KONZENTRATIONSTEST: RASTER UND LÖSUNG - für «Konztest auswerten» (Alpha)
# ============================================================================
# AUTOMATISCH ERZEUGT von scripts/konztest-loesungen.py aus Testheft und
# Lösungs-PDF unter assets/downloads/testsimulationen/. Nicht von Hand ändern.
#   x, y      Mitte jeder Spalte bzw. Zeile auf der Seite (pt, von oben links)
#   zeichen   je Zeile 40 Zeichen 0-F: welches Symbol wo steht
#   ziele     je Zeile 40 Ziffern: 1 = zu markieren
# Geprüft: Lösung und Regel der Anleitung stimmen in allen 1600 Feldern.
# ============================================================================
testsimulationen:
'''
    for jahr, j in JAHRE.items():
        d = lesen(j)
        print(jahr, 'ok:', sum(z.count('1') for z in d['ziele']), 'Ziele,', [z.count('1') for z in d['ziele']][:5], '...')
        aus += '  - jahr: %d\n    quelle: "%s, S. %d / %s"\n' % (jahr, j['heft'], j['seite'] + 1, j['loesung'])
        aus += '    x: [%s]\n    y: [%s]\n' % (', '.join('%.2f' % v for v in d['x']), ', '.join('%.2f' % v for v in d['y']))
        aus += '    zeichen:\n' + ''.join('      - "%s"\n' % z for z in d['zeichen'])
        aus += '    ziele:\n' + ''.join('      - "%s"\n' % z for z in d['ziele'])
    if '--schreiben' in sys.argv:
        with open(ZIEL, 'w', encoding='utf-8') as f:
            f.write(aus)
        print('geschrieben:', ZIEL)


if __name__ == '__main__':
    main()
