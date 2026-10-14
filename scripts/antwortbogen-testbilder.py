#!/usr/bin/env python3
"""
================================================================================
TESTBILDER FÜR «ANTWORTBOGEN AUSWERTEN» (Alpha-Seite)
================================================================================
Erzeugt ausgefüllte Antwortbögen als Bilder, deren Markierungen bekannt sind:
der echte Bogen der Testsimulation 2026 (erste Seite des Hefts), darin wie
verlangt mit Bleistift je ein schräger Strich, einmal mit radierten - dann einmal als sauberer Scan und mehrmals als «Handyfoto»
(schräg, gedreht, auf dunklem Tisch, mit Schatten, unscharf, als JPG).
scripts/antwortbogen-pruefen.mjs liest sie im Browser und vergleicht.

    pip install pymupdf pillow numpy
    python3 scripts/antwortbogen-testbilder.py ORDNER

Schreibt ORDNER/*.jpg|png|pdf und ORDNER/erwartet.json:
  {"bild.jpg": {"antworten": "A.B*..", "fehler": false}, ...,
   "_schluessel": {"dateien": [...], "loesungen": "AB.C.."}}
  Je Aufgabe ein Zeichen: A-E ein Strich, "." leer, "*" mehrere; im
  Schlüssel "." = Aufgabe ohne Lösung.

Dazu ein eigener Lösungsschlüssel, wie ihn das Formatierungstool ausgibt
(vorlage/loesungsblatt.typ): ein PDF mit einer Tabellenseite und danach dem
Antwortbogen, die richtigen Kästchen schwarz - hier die Lösungen 2026, aber
Muster zuordnen 3-18 ohne Lösung (wie im Tool, wo diese Serie keine hat).
Und derselbe Schlüssel als Foto, und der Scan als PDF.

Die Striche sitzen dort, wo die Kästchen im PDF wirklich stehen (aus den
Zeichnungen des PDFs gelesen, nicht aus den Zahlen der Auswertung) - sonst
prüfte der Test die Auswertung gegen sich selbst.
================================================================================
"""
import json
import math
import os
import random
import sys

import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFilter

HEFT = 'assets/downloads/testsimulationen/2026_testsimulationen_Testsimulation.pdf'
DPI = 150
BST = 'ABCDE'


def kaestchen():
    """Die 720 Antwortkästchen des Bogens aus dem PDF: [(x0, y0, x1, y1)] in pt,
    sortiert nach Aufgabe und Buchstabe."""
    seite = pymupdf.open(HEFT)[0]
    felder = set()
    for z in seite.get_drawings():
        r = z['rect']
        if abs(r.width - 9.12) < 0.6 and abs(r.height - 6.24) < 0.6 and r.y0 > 200:
            felder.add((round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1)))
    felder = sorted(felder, key=lambda r: (r[1], r[0]))
    assert len(felder) == 720, len(felder)
    # Zeilen zu je 4 Blöcken x 5 Kästchen; Blöcke oben (y < 500) und unten
    zeilen = {}
    for r in felder:
        zeilen.setdefault(r[1], []).append(r)
    aus = {}
    for y, reihe in zeilen.items():
        reihe.sort()
        unten = y > 500
        zeile = round((y - (537.4 if unten else 241.4)) / 13.48)
        for k in range(4):
            block = k + (4 if unten else 0)
            nr = block * 18 + zeile
            aus[nr] = reihe[k * 5:(k + 1) * 5]
    return [aus[nr] for nr in range(144)]


def ausfuellen(bild, felder, antworten, stift, s, breite_pt=(0.9, 1.5), radiert=0.0):
    """Markiert wie am EMS verlangt («Bitte nur so markieren» oben auf dem
    Bogen): mit Bleistift EIN schräger Strich durchs Kästchen, mal / mal \\,
    leicht schief und über den Rand. Doppelt markierte Zeilen haben zwei
    solche Kästchen. radiert: Anteil der Zeilen mit einem wegradierten Strich
    (nur noch ein Hauch) in einem anderen Kästchen - gezählt wird der deutliche."""
    zeichnen = ImageDraw.Draw(bild)
    weg = []
    def strich(x0, y0, x1, y1, farbe):
        j = lambda: random.uniform(-0.8, 0.8) * s
        breite = max(1, int(round(random.uniform(*breite_pt) * s)))
        if random.random() < 0.5:
            zeichnen.line([(x0 + j(), y1 + j()), (x1 + j(), y0 + j())], fill=farbe, width=breite)
        else:
            zeichnen.line([(x0 + j(), y0 + j()), (x1 + j(), y1 + j())], fill=farbe, width=breite)
    for nr, a in enumerate(antworten):
        if a == '.':
            continue
        wahl = [BST.index(a)] if a in BST else random.sample(range(5), 2)
        for k in wahl:
            strich(*[v * s for v in felder[nr][k]], stift)
        if a in BST and random.random() < radiert:
            k = random.choice([i for i in range(5) if i != wahl[0]])
            hauch = tuple(min(255, int(c + 0.85 * (235 - c))) for c in stift)
            strich(*[v * s for v in felder[nr][k]], hauch)
            weg.append(nr)
    return weg


def perspektive(punkte_von, punkte_nach):
    """Koeffizienten für Image.transform(PERSPECTIVE): Ziel -> Quelle."""
    a, b = [], []
    for (x, y), (u, v) in zip(punkte_nach, punkte_von):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return np.linalg.solve(np.array(a, float), np.array(b, float)).tolist()


def foto(scan, drehung, schraeg, rand, schatten, unschaerfe, breite_ziel):
    """Ein Handyfoto des Bogens: auf einem dunkleren Tisch, perspektivisch
    verzerrt, gedreht, mit Helligkeitsverlauf, unscharf."""
    w, h = scan.size
    gross = Image.new('RGB', (int(w * (1 + 2 * rand)), int(h * (1 + 2 * rand))), (92, 84, 76))
    gw, gh = gross.size
    # Die Ecken des Blatts im Foto: verschoben und schräg
    cx, cy = gw / 2, gh / 2
    ecken = []
    for (ex, ey) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x = cx + ex * w / 2 + random.uniform(-schraeg, schraeg) * w
        y = cy + ey * h / 2 + random.uniform(-schraeg, schraeg) * h
        ecken.append((x, y))
    koeff = perspektive([(0, 0), (w, 0), (w, h), (0, h)], ecken)
    blatt = scan.transform((gw, gh), Image.PERSPECTIVE, koeff, Image.BICUBIC, fillcolor=(0, 0, 0))
    maske = Image.new('L', scan.size, 255).transform((gw, gh), Image.PERSPECTIVE, koeff, Image.BICUBIC, fillcolor=0)
    gross.paste(blatt, (0, 0), maske)
    # Licht von der Seite: eine Ecke deutlich dunkler
    g = np.array(gross).astype(float)
    yy, xx = np.mgrid[0:gh, 0:gw]
    winkel = random.uniform(0, 2 * math.pi)
    verlauf = (np.cos(winkel) * (xx / gw - .5) + np.sin(winkel) * (yy / gh - .5))
    g *= (1 - schatten * (verlauf + .5))[..., None]
    g += np.random.normal(0, 4, g.shape)
    gross = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
    gross = gross.rotate(drehung, expand=True, fillcolor=(92, 84, 76), resample=Image.BICUBIC)
    if unschaerfe:
        gross = gross.filter(ImageFilter.GaussianBlur(unschaerfe))
    z = breite_ziel / gross.size[0]
    return gross.resize((int(gross.size[0] * z), int(gross.size[1] * z)), Image.LANCZOS)


def video(bild, aus, w, h, leer=15, voll=15, rauschen=0.0, wackeln=False):
    """y4m (YUV 4:2:0) für --use-file-for-fake-video-capture. rauschen:
    Bildrauschen (Standardabweichung) je Bild neu; wackeln: jedes Bild leicht
    verschoben und gedreht wie aus der Hand - für das Mitteln mehrerer
    Videobilder (bild-lesen.html, stapeln)."""
    def yuv(im):
        a = np.asarray(im.convert('RGB'), dtype=np.float32)
        y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
        u = (a[..., 2] - y) * 0.564 + 128
        v = (a[..., 0] - y) * 0.713 + 128
        halb = lambda c: c.reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))
        return b''.join(np.clip(c, 0, 255).astype(np.uint8).tobytes() for c in (y, halb(u), halb(v)))
    foto = Image.open(bild)
    foto.thumbnail((w, h))
    tisch = Image.new('RGB', (w, h), (92, 84, 76))
    mit = tisch.copy()
    mit.paste(foto, ((w - foto.size[0]) // 2, (h - foto.size[1]) // 2))
    a, b = yuv(tisch), yuv(mit)
    with open(aus, 'wb') as f:
        f.write(b'YUV4MPEG2 W%d H%d F10:1 Ip A1:1 C420jpeg\n' % (w, h))
        for i in range(leer + voll):
            f.write(b'FRAME\n')
            if i < leer:
                f.write(a)
            elif not rauschen and not wackeln:
                f.write(b)
            else:
                bildchen = mit
                if wackeln:
                    bildchen = mit.rotate(random.uniform(-0.3, 0.3), resample=Image.BICUBIC, fillcolor=(92, 84, 76),
                                          translate=(random.uniform(-4, 4), random.uniform(-4, 4)))
                arr = np.asarray(bildchen, dtype=np.float32)
                if rauschen:
                    arr = arr + np.random.normal(0, rauschen, arr.shape)
                f.write(yuv(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))))


def main():
    ordner = sys.argv[1]
    os.makedirs(ordner, exist_ok=True)
    random.seed(2026)
    np.random.seed(2026)
    felder = kaestchen()
    s = DPI / 72
    pix = pymupdf.open(HEFT)[0].get_pixmap(dpi=DPI)
    leer = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    erwartet = {}

    def bogen(muster):
        """Zufällige Antworten: meist ein Strich, ein paar leer, ein paar doppelt."""
        aus = []
        for _ in range(144):
            r = random.random()
            aus.append('.' if r < muster[0] else '*' if r < muster[0] + muster[1] else random.choice(BST))
        return ''.join(aus)

    faelle = [
        # name, stift, foto-Einstellungen (None = Scan), Strichbreite (pt), radiert
        # Bleistift in verschiedenen Härten; einmal Kugelschreiber zum Vergleich
        ('scan.png', (70, 70, 70), None, (0.9, 1.5), 0),
        ('foto-gerade.jpg', (95, 95, 95), dict(drehung=0, schraeg=0.01, rand=0.06, schatten=0.25, unschaerfe=0.6, breite_ziel=2400), (0.9, 1.5), 0),
        ('foto-schraeg.jpg', (20, 40, 140), dict(drehung=4, schraeg=0.04, rand=0.08, schatten=0.45, unschaerfe=1.0, breite_ziel=3000), (0.9, 1.5), 0),
        ('foto-kopfueber.jpg', (110, 110, 110), dict(drehung=178, schraeg=0.02, rand=0.05, schatten=0.3, unschaerfe=0.8, breite_ziel=2200), (0.9, 1.5), 0),
        ('foto-quer.jpg', (100, 100, 100), dict(drehung=91, schraeg=0.02, rand=0.1, schatten=0.35, unschaerfe=0.8, breite_ziel=3200), (0.9, 1.5), 0),
        ('foto-bleistift.jpg', (130, 130, 130), dict(drehung=-2, schraeg=0.02, rand=0.07, schatten=0.3, unschaerfe=0.9, breite_ziel=2400), (0.7, 1.1), 0),
        ('foto-radiert.jpg', (110, 110, 110), dict(drehung=1, schraeg=0.02, rand=0.06, schatten=0.3, unschaerfe=0.8, breite_ziel=2400), (0.9, 1.3), 0.05),
    ]
    for name, stift, einst, breite_pt, radiert in faelle:
        antworten = bogen((0.08, 0.03))
        scan = leer.copy()
        weg = ausfuellen(scan, felder, antworten, stift, s, breite_pt, radiert)
        bild = scan if einst is None else foto(scan, **einst)
        pfad = os.path.join(ordner, name)
        if name.endswith('.jpg'):
            bild.save(pfad, quality=82)
        else:
            bild.save(pfad)
        erwartet[name] = {'antworten': antworten, 'fehler': False, 'radiert': weg}
    # Zu klein: der ganze Bogen nur 420 Bildpunkte breit
    klein = leer.copy()
    klein.thumbnail((420, 600))
    k = Image.new('RGB', (1200, 1600), (90, 80, 70))
    k.paste(klein, (390, 500))
    k.save(os.path.join(ordner, 'zu-klein.jpg'), quality=85)
    erwartet['zu-klein.jpg'] = {'antworten': None, 'fehler': True}
    # Kein Antwortbogen: eine Textseite aus dem Heft
    pix = pymupdf.open(HEFT)[10].get_pixmap(dpi=DPI)
    Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(os.path.join(ordner, 'kein-bogen.png'))
    erwartet['kein-bogen.png'] = {'antworten': None, 'fehler': True}
    # Der Scan noch einmal als PDF (eine Seite, Bild darin)
    pdf = pymupdf.open()
    seite = pdf.new_page(width=595.2, height=842.16)
    seite.insert_image(seite.rect, filename=os.path.join(ordner, 'scan.png'))
    pdf.save(os.path.join(ordner, 'scan.pdf'))
    erwartet['scan.pdf'] = dict(erwartet['scan.png'])
    # Der eigene Lösungsschlüssel
    import yaml
    daten = yaml.safe_load(open('data/antwortbogen.yaml', encoding='utf-8'))
    loes = ''.join([t for t in daten['testsimulationen'] if t['jahr'] == 2026][0]['loesungen'])
    loes = loes[:2] + '.' * 16 + loes[18:]
    heft = pymupdf.open(HEFT)
    pdf = pymupdf.open()
    tabelle = pdf.new_page(width=595.28, height=841.89)
    tabelle.insert_text((42.5, 98.7), 'Lösungen   Testsimulation (Probe)', fontsize=12)
    for i, l in enumerate(loes):
        if l != '.':
            tabelle.insert_text((42.5 + (i % 10) * 36, 140 + (i // 10) * 20), '%d %s' % (i + 1, l), fontsize=8)
    pdf.insert_pdf(heft, from_page=0, to_page=0)
    bogen = pdf[1]
    for nr, l in enumerate(loes):
        if l != '.':
            bogen.draw_rect(pymupdf.Rect(felder[nr][BST.index(l)]), color=(0, 0, 0), fill=(0, 0, 0), width=1.07)
    pdf.save(os.path.join(ordner, 'schluessel.pdf'))
    pix = pdf[1].get_pixmap(dpi=DPI)
    schl = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    random.seed(7)
    foto(schl, drehung=-3, schraeg=0.02, rand=0.07, schatten=0.3, unschaerfe=0.8, breite_ziel=2600).save(
        os.path.join(ordner, 'schluessel-foto.jpg'), quality=82)
    erwartet['_schluessel'] = {'dateien': ['schluessel.pdf', 'schluessel-foto.jpg'], 'loesungen': loes}
    # Für die Live-Kamera: ein y4m-Video (Chromiums Fake-Kamera spielt es ab),
    # erst eineinhalb Sekunden leerer Tisch, dann das schräge Foto
    video(os.path.join(ordner, 'foto-schraeg.jpg'), os.path.join(ordner, 'kamera.y4m'), 1080, 1440)
    erwartet['_kamera'] = {'datei': 'kamera.y4m', 'antworten': erwartet['foto-schraeg.jpg']['antworten']}
    # Dasselbe verrauscht und wackelnd, für das Mitteln mehrerer Videobilder:
    # der Bogen in hellem Bleistift, wo ein einzelnes verrauschtes Bild nicht reicht
    video(os.path.join(ordner, 'foto-bleistift.jpg'), os.path.join(ordner, 'kamera-wackelt.y4m'), 1080, 1440,
          voll=45, rauschen=30, wackeln=True)
    erwartet['_kamera_wackelt'] = {'datei': 'kamera-wackelt.y4m', 'antworten': erwartet['foto-bleistift.jpg']['antworten']}
    with open(os.path.join(ordner, 'erwartet.json'), 'w') as f:
        json.dump(erwartet, f, indent=1)
    print('geschrieben:', ', '.join(erwartet))


if __name__ == '__main__':
    main()
