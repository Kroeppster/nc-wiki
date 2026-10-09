#!/usr/bin/env python3
"""
================================================================================
TESTBILDER FÜR «ANTWORTBOGEN AUSWERTEN» (Alpha-Seite)
================================================================================
Erzeugt ausgefüllte Antwortbögen als Bilder, deren Kreuze bekannt sind: der
echte Bogen der Testsimulation 2026 (erste Seite des Hefts), darin Kreuze
wie von Hand - dann einmal als sauberer Scan und mehrmals als «Handyfoto»
(schräg, gedreht, auf dunklem Tisch, mit Schatten, unscharf, als JPG).
scripts/antwortbogen-pruefen.mjs liest sie im Browser und vergleicht.

    pip install pymupdf pillow numpy
    python3 scripts/antwortbogen-testbilder.py ORDNER

Schreibt ORDNER/*.jpg|png|pdf und ORDNER/erwartet.json:
  {"bild.jpg": {"antworten": "A.B*..", "fehler": false}, ...,
   "_schluessel": {"dateien": [...], "loesungen": "AB.C.."}}
  Je Aufgabe ein Zeichen: A-E ein Kreuz, "." leer, "*" mehrere; im
  Schlüssel "." = Aufgabe ohne Lösung.

Dazu ein eigener Lösungsschlüssel, wie ihn das Formatierungstool ausgibt
(vorlage/loesungsblatt.typ): ein PDF mit einer Tabellenseite und danach dem
Antwortbogen, die richtigen Kästchen schwarz - hier die Lösungen 2026, aber
Muster zuordnen 3-18 ohne Lösung (wie im Tool, wo diese Serie keine hat).
Und derselbe Schlüssel als Foto, und der Scan als PDF.

Die Kreuze sitzen dort, wo die Kästchen im PDF wirklich stehen (aus den
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


def ausfuellen(bild, felder, antworten, stift, s):
    """Kreuze wie von Hand: zwei Striche, leicht schief und über den Rand."""
    zeichnen = ImageDraw.Draw(bild)
    for nr, a in enumerate(antworten):
        if a == '.':
            continue
        wahl = [BST.index(a)] if a in BST else random.sample(range(5), 2)
        for k in wahl:
            x0, y0, x1, y1 = [v * s for v in felder[nr][k]]
            j = lambda: random.uniform(-0.8, 0.8) * s
            breite = max(2, int(random.uniform(0.9, 1.5) * s))
            zeichnen.line([(x0 + j(), y0 + j()), (x1 + j(), y1 + j())], fill=stift, width=breite)
            zeichnen.line([(x0 + j(), y1 + j()), (x1 + j(), y0 + j())], fill=stift, width=breite)


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


def video(bild, aus, w, h, leer=15, voll=15):
    """y4m (YUV 4:2:0) für --use-file-for-fake-video-capture."""
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
            f.write(a if i < leer else b)


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
        """Zufällige Antworten: meist ein Kreuz, ein paar leer, ein paar doppelt."""
        aus = []
        for _ in range(144):
            r = random.random()
            aus.append('.' if r < muster[0] else '*' if r < muster[0] + muster[1] else random.choice(BST))
        return ''.join(aus)

    faelle = [
        # name, stift, foto-Einstellungen (None = Scan)
        ('scan.png', (25, 25, 120), None),
        ('foto-gerade.jpg', (30, 30, 30), dict(drehung=0, schraeg=0.01, rand=0.06, schatten=0.25, unschaerfe=0.6, breite_ziel=2400)),
        ('foto-schraeg.jpg', (20, 40, 140), dict(drehung=4, schraeg=0.04, rand=0.08, schatten=0.45, unschaerfe=1.0, breite_ziel=3000)),
        ('foto-kopfueber.jpg', (60, 60, 60), dict(drehung=178, schraeg=0.02, rand=0.05, schatten=0.3, unschaerfe=0.8, breite_ziel=2200)),
        ('foto-quer.jpg', (35, 35, 35), dict(drehung=91, schraeg=0.02, rand=0.1, schatten=0.35, unschaerfe=0.8, breite_ziel=3200)),
        ('foto-bleistift.jpg', (110, 110, 110), dict(drehung=-2, schraeg=0.02, rand=0.07, schatten=0.3, unschaerfe=0.7, breite_ziel=2600)),
    ]
    for name, stift, einst in faelle:
        antworten = bogen((0.08, 0.03))
        scan = leer.copy()
        ausfuellen(scan, felder, antworten, stift, s)
        bild = scan if einst is None else foto(scan, **einst)
        pfad = os.path.join(ordner, name)
        if name.endswith('.jpg'):
            bild.save(pfad, quality=82)
        else:
            bild.save(pfad)
        erwartet[name] = {'antworten': antworten, 'fehler': False}
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
    with open(os.path.join(ordner, 'erwartet.json'), 'w') as f:
        json.dump(erwartet, f, indent=1)
    print('geschrieben:', ', '.join(erwartet))


if __name__ == '__main__':
    main()
