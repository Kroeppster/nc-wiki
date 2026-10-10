#!/usr/bin/env python3
"""
================================================================================
KONZENTRATIONSTESTS: RASTER UND LÖSUNG FÜR «KONZTEST AUSWERTEN» AUSLESEN
================================================================================
Liest aus jeder Testseite (40 Zeilen zu 40 Zeichen) und ihrem Lösungsblatt
und schreibt nach data/konztest.yaml:
  - wo die Mitte jeder Zeile und Spalte liegt (pt),
  - welche Zeichen einander gleichen (Klassen 0-9, A-Z, a-z: die Auswertung
    erkennt daran, wie der Bogen auf dem Foto liegt),
  - welche Zeichen zu markieren sind (die Lösung).

    pip install pymupdf numpy
    python3 scripts/konztest-loesungen.py            # nur prüfen und zeigen
    python3 scripts/konztest-loesungen.py --schreiben

DASSELBE VERFAHREN WIE IM BROWSER: Ein eigener Konztest (z. B. aus dem
Formatierungstool) wird auf der Seite genau so gelesen, wenn jemand Aufgabe
und Lösung als PDF hochlädt (layouts/partials/bausteine/konztest-auswertung.html,
«leseKonztest»). Dieses Skript macht es für die Konztests der Webseite im
Voraus - die Testhefte sind zu gross, um sie im Browser zu laden.
  1. Testseite mit 4 Bildpunkten je pt zeichnen. Bedruckt ist Magenta
     (falls es viel davon gibt) oder sonst Dunkles.
  2. Flecken (Stücke, die sich auf 1 pt berühren) von 2 bis 16 pt Grösse;
     ihre Mitten zu Zeilen und Spalten gruppieren und die 40 gleichmässigsten
     nehmen (so fallen Kopfzeile, Zeilennummern, Rahmen heraus).
  3. Je Zeichen der Schwerpunkt des Bedruckten (so misst auch das Foto) und
     ein Bild von 12 x 12; gleiche Bilder = gleiche Klasse.
  4. Lösungsblatt: Zielzeichen sind dort ausgefüllte Kästchen oder Balken
     (auf das Raster der Aufgabe gelegt oder als eigenes Raster an derselben
     Stelle). «Ausgefüllt» heisst: auch 1 pt nach innen noch ganz bedruckt;
     Buchstaben und Umrisse sind dünner. Die Lage wird um bis zu einen
     halben Zeichenabstand verschoben gesucht.
PRÜFUNGEN (sonst Abbruch): 40 x 40 Zeichen gefunden, Lösung eindeutig (kaum
halb gefüllte Stellen), 40 bis 1200 Ziele; Regelprobe (alle Regeln hängen
nur vom Zeichen und einem Nachbarn ab: gleiches Paar, gleiche Lösung) mit
höchstens 5 Widersprüchen; wo die Anleitung «10 pro Zeile»
vorgibt, genau 10 je Zeile; für 2026 zusätzlich die Regel der Anleitung
(Pfeil = Zeichen mod 4, Öffnung = Zeichen div 4).

Nicht dabei, weil auf der Webseite kein lesbares Lösungsblatt liegt:
Testsimulation 2024 und 2025, Serien 2025 S18 und S19; 2021 S03 hat eines,
aber die Kästchen sitzen nicht eindeutig; 2022 S02 hat die Zeichen schwarz
gedruckt (ein Konztest hat sie immer in Farbe). Siehe docs/WARTUNG-DETAILLIERT.md 11.
================================================================================
"""
import sys

try:
    import numpy as np
    import pymupdf
except ImportError:
    sys.exit('Fehlt: pymupdf und numpy. Installieren mit "pip install pymupdf numpy".')

ZIEL = 'data/konztest.yaml'
TS = 'assets/downloads/testsimulationen/'
UE = 'assets/downloads/uebungsaufgaben/konzentriertes-arbeiten/'
N = 40
S = 4                       # Bildpunkte je pt
KLASSEN = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# id, Art, Jahr, Serie, (Aufgabe, Seite), (Lösung, Seite), genau 10 je Zeile
KONZTESTS = [
    ('ts2026', 'testsimulation', 2026, '', (TS + '2026_testsimulationen_Testsimulation.pdf', 84), (TS + '2026_testsimulationen_Loesung.pdf', 1), True),
    ('ts2023', 'testsimulation', 2023, '', (TS + '2023_testsimulationen_Testsimulation.pdf', 77), (TS + '2023_testsimulationen_Loesung-Konzentrationstest.pdf', 0), False),
    ('ts2022', 'testsimulation', 2022, '', (TS + '2022_testsimulationen_Testsimulation.pdf', 72), (TS + '2022_testsimulationen_Loesung-Konzentrationstest.pdf', 0), False),
] + [
    ('s2025-%02d' % n, 'serie', 2025, 'S%02d' % n, (UE + '2025_konzentriertes-arbeiten_S%02d.pdf' % n, 1), (UE + '2025_konzentriertes-arbeiten_S%02d.pdf' % n, 2), True)
    for n in range(2, 18)
] + [
    ('s2024-%02d' % n, 'serie', 2024, 'S%02d' % n, (UE + '2024_konzentriertes-arbeiten_S%02d.pdf' % n, 0), (UE + '2024_konzentriertes-arbeiten_S%02d.pdf' % n, 1), False)
    for n in (2, 3)
] + [
    # 2022 S02 nicht: Zeichen schwarz gedruckt (ein Konztest hat sie immer in
    # Farbe, markiert wird schwarz oder blau)
    ('s2021-02', 'serie', 2021, 'S02', (UE + '2021_konzentriertes-arbeiten_S02.pdf', 0), (UE + '2021_konzentriertes-arbeiten_S02_Loesung.pdf', 0), False),
    # 2021 S03 nicht: die Kästchen im Lösungsblatt sitzen teils zwischen zwei
    # Ziffern (von Hand gesetzt), 25 Widersprüche in der Regelprobe
]


class Fehler(Exception):
    pass


def zeichnen(datei, seite):
    pix = pymupdf.open(datei)[seite].get_pixmap(matrix=pymupdf.Matrix(S, S), alpha=False)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3).astype(np.int32)


def helligkeit(a):
    return (299 * a[..., 0] + 587 * a[..., 1] + 114 * a[..., 2]) // 1000


def flecken(m, kasten=False):
    """Stücke auf einem Raster von 1 pt (eine Zelle zählt, wenn darin etwas
    bedruckt ist), 8er-Nachbarschaft. -> Liste (Mitte x, Mitte y, Grösse) in pt"""
    h, w = m.shape
    H, W = h // S, w // S
    g = m[:H * S, :W * S].reshape(H, S, W, S).any(axis=(1, 3))
    gesehen = np.zeros((H, W), bool)
    aus = []
    for y0, x0 in zip(*np.nonzero(g)):
        if gesehen[y0, x0]:
            continue
        gesehen[y0, x0] = True
        stapel, ys, xs = [(y0, x0)], [], []
        while stapel:
            y, x = stapel.pop()
            ys.append(y); xs.append(x)
            for yy in (y - 1, y, y + 1):
                for xx in (x - 1, x, x + 1):
                    if 0 <= yy < H and 0 <= xx < W and g[yy, xx] and not gesehen[yy, xx]:
                        gesehen[yy, xx] = True
                        stapel.append((yy, xx))
        x0_, x1_, y0_, y1_ = min(xs), max(xs) + 1, min(ys), max(ys) + 1
        aus.append((x0_, y0_, x1_, y1_) if kasten else ((x0_ + x1_) / 2, (y0_ + y1_) / 2, max(x1_ - x0_, y1_ - y0_)))
    return aus


def vierzig(werte):
    """Werte zu Gruppen (Lücke > 2.5 pt trennt), Gruppen mit >= 25 Flecken,
    davon die 40 aufeinanderfolgenden mit dem gleichmässigsten Abstand."""
    werte = np.sort(np.asarray(werte))
    grenzen = np.nonzero(np.diff(werte) > 2.5)[0] + 1
    gruppen = [g for g in np.split(werte, grenzen) if len(g) >= 25]
    if len(gruppen) < N:
        raise Fehler('nur %d Zeilen/Spalten mit Zeichen gefunden' % len(gruppen))
    mitten = np.array([np.median(g) for g in gruppen])
    beste = min(range(len(mitten) - N + 1), key=lambda i: np.diff(mitten[i:i + N]).std() / np.diff(mitten[i:i + N]).mean())
    m = mitten[beste:beste + N]
    if np.diff(m).std() / np.diff(m).mean() > 0.1:
        raise Fehler('Zeilen/Spalten nicht gleichmässig')
    return m


def kastensumme(m, r):
    """Je Bildpunkt die Summe von m im Quadrat mit Halbseite r (Bildpunkte)."""
    k = np.pad(m.astype(np.int32), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    h, w = m.shape
    y0 = np.clip(np.arange(h) - r, 0, h); y1 = np.clip(np.arange(h) + r + 1, 0, h)
    x0 = np.clip(np.arange(w) - r, 0, w); x1 = np.clip(np.arange(w) + r + 1, 0, w)
    return k[y1][:, x1] - k[y0][:, x1] - k[y1][:, x0] + k[y0][:, x0], (y1 - y0)[:, None] * (x1 - x0)[None, :]


def aufgabe(datei, seite):
    a = zeichnen(datei, seite)
    farbig = np.minimum(a[..., 0], a[..., 2]) - a[..., 1] > 40
    if farbig.sum() <= 20000:
        raise Fehler('Zeichen nicht farbig gedruckt - ein Konztest hat sie immer in Magenta')
    farbe, m = True, farbig
    f = [z for z in flecken(m) if 2 <= z[2] <= 16]
    ys0, xs0 = vierzig([z[1] for z in f]), vierzig([z[0] for z in f])
    px, py = (xs0[-1] - xs0[0]) / (N - 1), (ys0[-1] - ys0[0]) / (N - 1)
    # Schwerpunkt je Zeichen, im Fenster von einem halben Abstand um die Mitte
    sx = np.zeros((N, N)); sy = np.zeros((N, N)); bilder = []
    for R in range(N):
        for C in range(N):
            y0, y1 = int((ys0[R] - py / 2) * S), int((ys0[R] + py / 2) * S)
            x0, x1 = int((xs0[C] - px / 2) * S), int((xs0[C] + px / 2) * S)
            w = m[y0:y1, x0:x1]
            yy, xx = np.nonzero(w)
            if len(yy) < 4:
                raise Fehler('Zeile %d, Zeichen %d: kein Zeichen' % (R + 1, C + 1))
            sx[R, C] = (x0 + xx.mean() + 0.5) / S; sy[R, C] = (y0 + yy.mean() + 0.5) / S
    xs, ys = np.median(sx, axis=0), np.median(sy, axis=1)
    # Bild je Zeichen: 16 x 16 Felder mit der mittleren Druckstärke, um den
    # Schwerpunkt der Druckstärke (so liegen gleiche Zeichen deckungsgleich)
    g = np.clip((np.minimum(a[..., 0], a[..., 2]) - a[..., 1]) / 150, 0, 1) if farbe else np.clip((255 - helligkeit(a)) / 200, 0, 1)
    hx, hy = int(0.45 * px * S), int(0.45 * py * S)
    gy, gx = np.mgrid[0:2 * hy, 0:2 * hx]
    b16x, b16y = (2 * hx) // 16, (2 * hy) // 16
    for R in range(N):
        for C in range(N):
            cx, cy = int(round(xs[C] * S)), int(round(ys[R] * S))
            w = g[cy - hy:cy + hy, cx - hx:cx + hx]
            # Ursprung auf den Schwerpunkt, auf Bruchteile eines Bildpunkts:
            # dazwischen linear (wie im Browser)
            ox = cx - hx + ((w * gx).sum() / w.sum() - hx if w.sum() > 0 else 0)
            oy = cy - hy + ((w * gy).sum() / w.sum() - hy if w.sum() > 0 else 0)
            fx, fy = ox + gx[:16 * b16y, :16 * b16x], oy + gy[:16 * b16y, :16 * b16x]
            x0, y0 = np.floor(fx).astype(int), np.floor(fy).astype(int)
            ax, ay = fx - x0, fy - y0
            v = ((1 - ay) * ((1 - ax) * g[y0, x0] + ax * g[y0, x0 + 1]) + ay * ((1 - ax) * g[y0 + 1, x0] + ax * g[y0 + 1, x0 + 1]))
            bilder.append(v.reshape(16, b16y, 16, b16x).mean(axis=(1, 3)).ravel())
    return dict(farbe=farbe, x=xs, y=ys, klassen=klassen(np.array(bilder)), a=a)


def klassen(bilder):
    """Gleiche Bilder bekommen dieselbe Klasse. Aus einer Schrift gezeichnet
    sind gleiche Zeichen praktisch gleich (Abweichung unter 0.003), verschiedene
    weichen ab 0.006 ab. Von Hand gezeichnete Grafiken (2025 S07, S08)
    schwanken von Stelle zu Stelle - dann die Grenze anheben, bis es höchstens
    40 Klassen sind. Ein Zeichen in zwei Klassen schadet nicht (die Auswertung
    vergleicht nur innerhalb einer Klasse), zwei Zeichen in einer schon."""
    grenze = 0.003
    while True:
        vertreter, aus = [], []
        for b in bilder:
            d = [np.abs(b - v).mean() for v in vertreter]
            if d and min(d) < grenze:
                aus.append(int(np.argmin(d)))
            else:
                vertreter.append(b); aus.append(len(vertreter) - 1)
        if len(vertreter) <= 40:
            return [''.join(KLASSEN[aus[R * N + C]] for C in range(N)) for R in range(N)]
        grenze *= 1.5


def loesung(datei, seite, xs, ys):
    a = zeichnen(datei, seite)
    tinte = (helligkeit(a) < 160) | (np.minimum(a[..., 0], a[..., 2]) - a[..., 1] > 100)
    # «Ausgefüllt»: auch 0.75 pt nach innen noch ganz bedruckt. Buchstaben,
    # Umrisse und Zeichen sind dünner und fallen heraus.
    summe, flaeche = kastensumme(tinte, 3)
    voll = summe == flaeche
    px, py = (xs[-1] - xs[0]) / (N - 1), (ys[-1] - ys[0]) / (N - 1)
    # Ausgefüllte Flächen; aneinanderstossende Kästchen einer Zeile sind eine
    # Fläche und werden nach ihrer Breite geteilt
    mitten = []
    for x0, y0, x1, y1 in flecken(voll, kasten=True):
        b, h = x1 - x0 + 1.5, y1 - y0 + 1.5
        if b < 2 or h < 2 or b > 4.5 * px or h > 1.6 * py:
            continue
        n = max(1, int(round(b / px)))
        mitten += [(x0 - 0.75 + (i + 0.5) * b / n, (y0 + y1) / 2) for i in range(n)]
    if len(mitten) < 40:
        raise Fehler('Lösung: nur %d ausgefüllte Kästchen' % len(mitten))
    P = np.array(mitten)

    def anpassen(werte, raster, schritt):
        # Verschiebung (gesucht) und Massstab (ausgeglichen): Lösungsblatt -> Raster
        def treffer(v):
            return np.abs(v[:, None] - raster[None, :]).min(axis=1) < 0.2 * schritt
        versch = max(np.arange(-0.5 * schritt, 0.5 * schritt, 0.25), key=lambda d: treffer(werte - d).sum())
        f, d = 1.0, versch
        for _ in range(3):
            v = (werte - d) / f
            i = np.abs(v[:, None] - raster[None, :]).argmin(axis=1)
            ok = np.abs(v - raster[i]) < 0.3 * schritt
            f, d = np.polyfit(raster[i][ok], werte[ok], 1)
        return (werte - d) / f
    X, Y = anpassen(P[:, 0], xs, px), anpassen(P[:, 1], ys, py)
    ziele = np.zeros((N, N), bool)
    for x, y in zip(X, Y):
        C, R = int(np.abs(xs - x).argmin()), int(np.abs(ys - y).argmin())
        if abs(xs[C] - x) > 0.3 * px or abs(ys[R] - y) > 0.3 * py:
            continue                  # ausserhalb des Rasters (Kopf, Logo)
        if ziele[R, C]:
            raise Fehler('Lösung: zwei Kästchen auf Zeile %d, Zeichen %d' % (R + 1, C + 1))
        ziele[R, C] = True
    if not 40 <= ziele.sum() <= 1200:
        raise Fehler('Lösung: %d Ziele' % ziele.sum())
    return [''.join('1' if ziele[R, C] else '0' for C in range(N)) for R in range(N)], (0, 0)


def regelprobe(klassen, ziele):
    """Alle Regeln der Konztests hängen nur vom Zeichen und seinem Nachbarn
    ab. Widersprüche (gleiches Paar, mal Ziel, mal nicht) zeigen Lesefehler
    - oder zwei Zeichen in einer Klasse. -> kleinste Zahl Widersprüche"""
    beste = None
    for nachbar in (1, -1, 0):
        je = {}
        for R in range(N):
            for C in range(N):
                n = klassen[R][C + nachbar] if 0 <= C + nachbar < N else None
                je.setdefault((klassen[R][C], n), []).append(ziele[R][C])
        w = sum(min(v.count('0'), v.count('1')) for v in je.values())
        beste = w if beste is None else min(beste, w)
    return beste


def gegenprobe_2026(t, ziele):
    """2026: Zeichen als Schrift 0-F; Regel der Anleitung muss passen."""
    seite = pymupdf.open(TS + '2026_testsimulationen_Testsimulation.pdf')[84]
    code = [[None] * N for _ in range(N)]
    for b in seite.get_text('rawdict')['blocks']:
        for line in b.get('lines', []):
            for s in line['spans']:
                if 'KonzTestsim2026' not in s['font']:
                    continue
                for c in s['chars']:
                    gx, gy = (c['bbox'][0] + c['bbox'][2]) / 2, (c['bbox'][1] + c['bbox'][3]) / 2
                    if c['c'].strip() and gy > 180:
                        code[int(np.argmin(abs(t['y'] - gy)))][int(np.argmin(abs(t['x'] - gx)))] = int(c['c'], 16)
    paare = set()
    for R in range(N):
        for C in range(N):
            paare.add((t['klassen'][R][C], code[R][C]))
            regel = C < N - 1 and code[R][C] % 4 == code[R][C + 1] // 4
            if regel != (ziele[R][C] == '1'):
                raise Fehler('2026: Lösung und Regel widersprechen sich (Zeile %d, Zeichen %d)' % (R + 1, C + 1))
    if len(paare) != len({p[0] for p in paare}):
        raise Fehler('2026: eine Klasse umfasst verschiedene Zeichen der Schrift')


def main():
    aus = '''# ============================================================================
# KONZENTRATIONSTESTS: RASTER UND LÖSUNG - für «Konztest auswerten» (Alpha)
# ============================================================================
# AUTOMATISCH ERZEUGT von scripts/konztest-loesungen.py aus den Testseiten
# und Lösungsblättern unter assets/downloads/. Nicht von Hand ändern.
#   id        Kennung; art testsimulation oder serie (Übungsserie)
#   farbe     immer true: die Zeichen stehen in Blindfarbe (Magenta)
#   x, y      Mitte jeder Spalte bzw. Zeile auf der Seite (pt, von oben links)
#   zeichen   je Zeile 40 Kennungen: gleiche Kennung = gleiches Zeichen
#   ziele     je Zeile 40 Ziffern: 1 = zu markieren
# ============================================================================
konztests:
'''
    fehler = 0
    for kid, art, jahr, serie, (af, ase), (lf, lse), zehn in KONZTESTS:
        try:
            t = aufgabe(af, ase)
            ziele, (dx, dy) = loesung(lf, lse, t['x'], t['y'])
            je = [z.count('1') for z in ziele]
            if zehn and any(n != 10 for n in je):
                raise Fehler('nicht 10 Ziele je Zeile: %s' % je)
            if kid == 'ts2026':
                gegenprobe_2026(t, ziele)
            if regelprobe(t['klassen'], ziele) > 5:
                raise Fehler('Regelprobe: %d Widersprüche - Lösung oder Zeichen falsch gelesen' % regelprobe(t['klassen'], ziele))
        except Fehler as e:
            print('%-9s FEHLER: %s' % (kid, e)); fehler += 1
            continue
        print('%-9s ok: %s, %d Zeichenarten, %d Ziele (je Zeile %d-%d), Regelprobe: %d Widersprüche' % (
            kid, 'Magenta' if t['farbe'] else 'schwarz', len(set(''.join(t['klassen']))), sum(je), min(je), max(je),
            regelprobe(t['klassen'], ziele)))
        aus += '  - id: %s\n    art: %s\n    jahr: %d\n    serie: "%s"\n    farbe: %s\n' % (kid, art, jahr, serie, 'true' if t['farbe'] else 'false')
        aus += '    quelle: "%s, S. %d / %s, S. %d"\n' % (af.split('/')[-1], ase + 1, lf.split('/')[-1], lse + 1)
        aus += '    x: [%s]\n    y: [%s]\n' % (', '.join('%.2f' % v for v in t['x']), ', '.join('%.2f' % v for v in t['y']))
        aus += '    zeichen:\n' + ''.join('      - "%s"\n' % z for z in t['klassen'])
        aus += '    ziele:\n' + ''.join('      - "%s"\n' % z for z in ziele)
    if fehler:
        sys.exit('%d Konztests mit Fehlern - nichts geschrieben' % fehler)
    if '--schreiben' in sys.argv:
        with open(ZIEL, 'w', encoding='utf-8') as f:
            f.write(aus)
        print('geschrieben:', ZIEL)


if __name__ == '__main__':
    main()
