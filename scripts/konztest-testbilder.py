#!/usr/bin/env python3
"""
================================================================================
TESTBILDER FÜR «KONZTEST AUSWERTEN» (Alpha-Seite)
================================================================================
Bearbeitete Konztest-Bögen mit bekannten Markierungen: der echte Bogen der
Testsimulation 2026, darin Striche wie von Hand - wie jemand, der bis Zeile
25 kommt, fast alle Zielzeichen findet und ein paar falsche markiert. Dann
als sauberer Scan und als «Handyfotos» (schräg, kopfüber, quer, Bleistift,
Schatten, JPG), dazu ein Bild ohne Konztest. scripts/konztest-pruefen.mjs
liest sie im Browser und vergleicht.

    pip install pymupdf pillow numpy pyyaml
    python3 scripts/konztest-testbilder.py ORDNER

Schreibt ORDNER/*.jpg|png und ORDNER/erwartet.json:
  {"bild.jpg": {"markiert": "0100...", "fehler": false}, ...}
  1600 Ziffern, Zeile für Zeile: 1 = markiert.
Die Lage der Striche kommt aus data/konztest.yaml (aus dem PDF gelesen).
Die Fotos macht dieselbe Funktion wie bei den Antwortbogen-Testbildern.
================================================================================
"""
import importlib.util
import json
import os
import random
import sys

import numpy as np
import pymupdf
import yaml
from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ab', os.path.join(HIER, 'antwortbogen-testbilder.py'))
ab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ab)

HEFT = 'assets/downloads/testsimulationen/2026_testsimulationen_Testsimulation.pdf'
SEITE = 84
DPI = 150


def bearbeiten(ziele, bis, treffer=0.92, daneben=0.02):
    """Markierungen wie von einem Kandidaten: in Lesereihenfolge bis zum
    Feld «bis», Zielzeichen meist gefunden, andere selten markiert."""
    aus = []
    for n in range(1600):
        z = ziele[n // 40][n % 40] == '1'
        if n > bis:
            aus.append('0')
        else:
            aus.append('1' if random.random() < (treffer if z else daneben) else '0')
    # das letzte bearbeitete Feld ist markiert (so ist «bis» eindeutig)
    aus[bis] = '1'
    return ''.join(aus)


def zeichnen(bild, k, markiert, stift, s, breite=1.3):
    d = ImageDraw.Draw(bild)
    for n, m in enumerate(markiert):
        if m != '1':
            continue
        x, y = k['x'][n % 40] * s, k['y'][n // 40] * s
        j = lambda: random.uniform(-0.8, 0.8) * s
        # ein Strich schräg durch das Zeichen, wie im Beispiel des Bogens
        d.line([(x - 4.5 * s + j(), y + 5.5 * s + j()), (x + 4.5 * s + j(), y - 5.5 * s + j())],
               fill=stift, width=max(2, int(breite * s)))


def main():
    ordner = sys.argv[1]
    os.makedirs(ordner, exist_ok=True)
    random.seed(40)
    np.random.seed(40)
    k = [t for t in yaml.safe_load(open('data/konztest.yaml', encoding='utf-8'))['konztests'] if t['id'] == 'ts2026'][0]
    s = DPI / 72
    pix = pymupdf.open(HEFT)[SEITE].get_pixmap(dpi=DPI)
    leer = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    erwartet = {}
    faelle = [
        ('scan.png', (25, 25, 120), None),
        ('foto-gerade.jpg', (30, 30, 30), dict(drehung=1, schraeg=0.01, rand=0.06, schatten=0.25, unschaerfe=0.6, breite_ziel=2400)),
        ('foto-schraeg.jpg', (20, 40, 140), dict(drehung=4, schraeg=0.035, rand=0.08, schatten=0.4, unschaerfe=0.9, breite_ziel=3000)),
        ('foto-kopfueber.jpg', (40, 40, 40), dict(drehung=179, schraeg=0.02, rand=0.05, schatten=0.3, unschaerfe=0.7, breite_ziel=2600)),
        ('foto-quer.jpg', (35, 35, 35), dict(drehung=-90, schraeg=0.02, rand=0.08, schatten=0.3, unschaerfe=0.7, breite_ziel=3400)),
        ('foto-bleistift.jpg', (105, 105, 105), dict(drehung=-2, schraeg=0.02, rand=0.07, schatten=0.3, unschaerfe=0.7, breite_ziel=2800)),
    ]
    for name, stift, einst in faelle:
        markiert = bearbeiten(k['ziele'], random.randint(900, 1300))
        bogen = leer.copy()
        zeichnen(bogen, k, markiert, stift, s)
        bild = bogen if einst is None else ab.foto(bogen, **einst)
        pfad = os.path.join(ordner, name)
        bild.save(pfad, quality=82) if name.endswith('.jpg') else bild.save(pfad)
        erwartet[name] = {'markiert': markiert, 'fehler': False}
    # Kein Konztest: der Antwortbogen
    pix = pymupdf.open(HEFT)[0].get_pixmap(dpi=DPI)
    Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(os.path.join(ordner, 'kein-konztest.png'))
    erwartet['kein-konztest.png'] = {'markiert': None, 'fehler': True}
    # Für die Live-Kamera
    ab.video(os.path.join(ordner, 'foto-gerade.jpg'), os.path.join(ordner, 'kamera.y4m'), 1080, 1440)
    erwartet['_kamera'] = {'datei': 'kamera.y4m', 'markiert': erwartet['foto-gerade.jpg']['markiert']}
    with open(os.path.join(ordner, 'erwartet.json'), 'w') as f:
        json.dump(erwartet, f, indent=1)
    print('geschrieben:', ', '.join(erwartet))


if __name__ == '__main__':
    main()
