#!/usr/bin/env python3
"""
KAMERA-LABOR: SZENE ERZEUGEN
============================
Rendert einen ausgefüllten Antwortbogen oder Konzentrationstest (echte Vorlage
aus den PDFs, Markierungen wie von Hand) und filmt ihn mit einer simulierten
Handykamera: 3D-Lage der Kamera (Abstand, Neigung, Drehung), gewölbtes Papier,
Anflug und Handzittern, Bewegungsunschärfe, Fokus, Belichtungsautomatik,
Weissabgleich, Licht- und Handschatten, Glanzfleck, Finger am Rand, Rauschen,
Bildverarbeitung des Handys (Entrauschen, Nachschärfen), JPEG.

Ergebnis ist ein MJPEG-Video (30 Bilder/s) für Chromiums Fake-Kamera
(--use-file-for-fake-video-capture=video.mjpeg) und die Wahrheit dazu.

Aufruf (Python mit numpy, pymupdf, pillow, pyyaml - wie die Testbilder-Skripte):
    python3 scripts/kamera-labor/szene.py konfig.json AUSGABEORDNER
Ein Video von 8 s rechnet etwa 2 bis 3 Minuten (ein Prozessorkern).

Schreibt AUSGABEORDNER/video.mjpeg, wahrheit.json, standbild.jpg (ein Bild aus
der Haltephase, für den Vergleich mit dem Hochladen), vorschau.jpg (Montage).

KONFIGURATION (JSON, alles optional; Standardwerte siehe STANDARD unten):
  seed, art ("antwortbogen" | "konztest"), jahr (Antwortbogen: 2022-2026),
  konztest (ID aus data/konztest.yaml, z. B. "ts2026", "s2025-07"),
  antworten: {leer, doppelt, radiert}                  Antwortbogen
  konz: {bis: [von, bis], treffer, daneben}             Konztest (Lesereihenfolge)
  stift: {art: bleistift|fineliner|kugelschreiber, farbe, breite_mm, druck (0-1),
          stil: schraeg|kurz|kreuz|haken|kreis|ausmalen|punkt|waagrecht|unterstrich,
          anteil_stil (Anteil Markierungen im Stil, der Rest schräg), zittern (0-1),
          daneben_mm (wie weit ein Strich danebenliegen darf)}
  papier: {woelbung_mm, ton [r,g,b], verschmiert (0-1), knick (bool)}
  kamera: {aufloesung [w,h], hfov_grad, dauer_s, ablauf [[phase, sekunden], ...]
           (phasen: tisch, anflug, halten, wackeln, weg, zurueck),
           fuellung (Anteil des Bildes, den das Blatt füllt), neigung_grad [x, y],
           drehung_grad, versatz [x, y] (Anteile), zittern_mm, zittern_grad, drift_mm,
           belichtungszeit_s, fokus_jagen_s, unschaerfe_px, belichtung, ae_schwanken,
           weissabgleich [r,g,b], licht {verlauf, schatten {staerke, groesse, weich,
           bewegt}, glanz {staerke, groesse}}, rauschen, vignette, jpeg,
           isp_schaerfen, hintergrund (holz|grau|weiss|unruhig|dunkel),
           finger {ecke (ol|or|ul|ur|l|r|u|o), groesse_mm}}
"""
import io
import json
import math
import os
import random
import sys

import numpy as np
import pymupdf
import yaml
from PIL import Image, ImageDraw, ImageFilter

REPO = os.environ.get('NCWIKI_REPO', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BST = 'ABCDE'
MM = 25.4 / 72  # mm pro pt

STANDARD = {
    'seed': 1, 'art': 'antwortbogen', 'jahr': 2026, 'konztest': 'ts2026', 'dpi': 300,
    'antworten': {'leer': 0.08, 'doppelt': 0.02, 'radiert': 0.0},
    'konz': {'bis': [900, 1300], 'treffer': 0.92, 'daneben': 0.02},
    'stift': {'art': None, 'farbe': None, 'breite_mm': None, 'druck': 0.8, 'stil': 'schraeg',
              'anteil_stil': 0.0, 'zittern': 0.3, 'daneben_mm': 0.4},
    'papier': {'woelbung_mm': 4, 'ton': [248, 246, 240], 'verschmiert': 0.0, 'knick': False},
    'kamera': {'aufloesung': [1080, 1920], 'hfov_grad': 46, 'dauer_s': 7,
               'ablauf': [['tisch', 0.5], ['anflug', 1.2], ['halten', 6.5]],
               'fuellung': 0.86, 'neigung_grad': [6, 3], 'drehung_grad': 2, 'versatz': [0.0, 0.0],
               'zittern_mm': 0.25, 'zittern_grad': 0.06, 'drift_mm': 3,
               'belichtungszeit_s': 1 / 60, 'fokus_jagen_s': 0.5, 'unschaerfe_px': 0.7,
               'belichtung': 1.0, 'ae_schwanken': 0.03, 'weissabgleich': [1.0, 0.97, 0.9],
               'licht': {'verlauf': 0.25, 'schatten': {'staerke': 0.35, 'groesse': 0.35, 'weich': 0.25, 'bewegt': True},
                         'glanz': None},
               'rauschen': 3.5, 'vignette': 0.2, 'jpeg': 85, 'isp_schaerfen': 0.5,
               'hintergrund': 'holz', 'finger': None},
}


def mischen(a, b):
    """b über a (verschachtelte dicts)."""
    aus = dict(a)
    for k, v in (b or {}).items():
        aus[k] = mischen(a[k], v) if isinstance(v, dict) and isinstance(a.get(k), dict) else v
    return aus


# --------------------------------------------------------------- Vorlagen
def antwortbogen_vorlage(jahr):
    """Seite und die 720 Kästchen (pt) des Antwortbogens der Testsimulation."""
    pfad = os.path.join(REPO, 'assets/downloads/testsimulationen/%d_testsimulationen_Testsimulation.pdf' % jahr)
    seite = pymupdf.open(pfad)[0]
    felder = set()
    for z in seite.get_drawings():
        r = z['rect']
        if abs(r.width - 9.12) < 0.6 and abs(r.height - 6.24) < 0.6 and r.y0 > 200:
            felder.add((round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1)))
    felder = sorted(felder, key=lambda r: (r[1], r[0]))
    # gleiche Kästchen mit Rundungsunterschied zusammenlegen
    eindeutig = []
    for r in felder:
        if not any(abs(r[0] - e[0]) < 1 and abs(r[1] - e[1]) < 1 for e in eindeutig[-30:]):
            eindeutig.append(r)
    felder = eindeutig
    if len(felder) != 720:
        raise SystemExit('Antwortbogen %d: %d statt 720 Kästchen' % (jahr, len(felder)))
    zeilen = {}
    for r in felder:
        zeilen.setdefault(round(r[1]), []).append(r)
    ys = sorted(zeilen)
    oben = [y for y in ys if y < 500]
    unten = [y for y in ys if y >= 500]
    if len(oben) != 18 or len(unten) != 18:
        raise SystemExit('Antwortbogen %d: Zeilen %d/%d' % (jahr, len(oben), len(unten)))
    aus = {}
    for teil, liste in ((0, oben), (1, unten)):
        for zeile, y in enumerate(liste):
            reihe = sorted(zeilen[y])
            if len(reihe) != 20:
                raise SystemExit('Antwortbogen %d: Zeile mit %d Kästchen' % (jahr, len(reihe)))
            for k in range(4):
                aus[(teil * 4 + k) * 18 + zeile] = reihe[k * 5:(k + 1) * 5]
    return pfad, 0, [aus[nr] for nr in range(144)]


def konztest_vorlage(kid):
    k = [t for t in yaml.safe_load(open(os.path.join(REPO, 'data/konztest.yaml'), encoding='utf-8'))['konztests'] if t['id'] == kid][0]
    datei, rest = k['quelle'].split(' / ')[0].split(', S. ')
    seite = int(rest) - 1
    unter = 'testsimulationen' if 'testsimulationen' in datei else 'uebungsaufgaben/konzentriertes-arbeiten'
    return os.path.join(REPO, 'assets/downloads', unter, datei), seite, k


# ------------------------------------------------------- Markierungen
class Stift:
    def __init__(self, cfg, art_bogen, s):
        art = cfg['art'] or ('bleistift' if art_bogen == 'antwortbogen' else 'fineliner')
        self.art = art
        druck = max(0.05, min(1.0, cfg['druck']))
        if art == 'bleistift':
            grau = 150 - 95 * druck          # HB fest: ~75, leicht: ~140
            self.farbe = cfg['farbe'] or [grau, grau, grau + 4]
            self.breite = (cfg['breite_mm'] or 0.55) * s / MM / 1.0
            self.deckung = 0.55 + 0.4 * druck
            self.koernung = 0.45
        elif art == 'fineliner':
            self.farbe = cfg['farbe'] or [22, 22, 28]
            self.breite = (cfg['breite_mm'] or 0.6) * s / MM
            self.deckung = 0.9 + 0.08 * druck
            self.koernung = 0.06
        else:  # kugelschreiber
            self.farbe = cfg['farbe'] or [30, 45, 150]
            self.breite = (cfg['breite_mm'] or 0.35) * s / MM
            self.deckung = 0.75 + 0.2 * druck
            self.koernung = 0.15
        self.zittern = cfg['zittern']


def linie(zeichnen, punkte, breite):
    zeichnen.line(punkte, fill=255, width=max(1, int(round(breite))), joint='curve')
    r = breite / 2
    for x, y in (punkte[0], punkte[-1]):
        zeichnen.ellipse([x - r, y - r, x + r, y + r], fill=255)


def strich_punkte(x0, y0, x1, y1, zittern, rnd, n=6):
    """Leicht gebogener, nicht ganz gerader Strich von (x0,y0) nach (x1,y1)."""
    dx, dy = x1 - x0, y1 - y0
    l = math.hypot(dx, dy) or 1
    nx, ny = -dy / l, dx / l
    bogen = rnd.uniform(-0.06, 0.06) * l * zittern * 2
    pts = []
    for i in range(n + 1):
        t = i / n
        b = bogen * 4 * t * (1 - t) + rnd.uniform(-0.01, 0.01) * l * zittern
        pts.append((x0 + dx * t + nx * b, y0 + dy * t + ny * b))
    return pts


def zeichne_markierung(zeichnen, stil, box, stift, s, rnd, daneben):
    """box: (x0, y0, x1, y1) in Pixeln - das Kästchen bzw. das Zeichen."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    j = lambda f=1.0: rnd.uniform(-1, 1) * daneben * s / MM * f
    b = stift.breite * rnd.uniform(0.85, 1.15)
    if stil in ('schraeg', 'kurz'):
        ueber = rnd.uniform(-0.05, 0.25)       # wie weit über das Kästchen hinaus
        if stil == 'kurz':
            ueber = rnd.uniform(-0.45, -0.2)
        ax, ay = w * (0.5 + ueber), h * (0.5 + ueber)
        if rnd.random() < 0.65:   # Rechtshänder: meist /
            p = strich_punkte(cx - ax + j(), cy + ay + j(), cx + ax + j(), cy - ay + j(), stift.zittern, rnd)
        else:
            p = strich_punkte(cx - ax + j(), cy - ay + j(), cx + ax + j(), cy + ay + j(), stift.zittern, rnd)
        linie(zeichnen, p, b)
    elif stil == 'kreuz':
        for (a, c) in (((-1, 1), (1, -1)), ((-1, -1), (1, 1))):
            p = strich_punkte(cx + a[0] * w * .55 + j(), cy + a[1] * h * .55 + j(), cx + c[0] * w * .55 + j(), cy + c[1] * h * .55 + j(), stift.zittern, rnd)
            linie(zeichnen, p, b)
    elif stil == 'haken':
        p = [(cx - w * .45 + j(), cy + j()), (cx - w * .1 + j(), cy + h * .45 + j()), (cx + w * .55 + j(), cy - h * .6 + j())]
        linie(zeichnen, p, b)
    elif stil == 'waagrecht':
        linie(zeichnen, strich_punkte(cx - w * .6 + j(), cy + j(.3), cx + w * .6 + j(), cy + j(.3), stift.zittern, rnd), b)
    elif stil == 'unterstrich':
        linie(zeichnen, strich_punkte(cx - w * .55 + j(), y1 + h * .15 + j(.3), cx + w * .55 + j(), y1 + h * .15 + j(.3), stift.zittern, rnd), b)
    elif stil == 'kreis':
        rx, ry = w * .75, h * .8
        zeichnen.ellipse([cx - rx + j(), cy - ry + j(), cx + rx + j(), cy + ry + j()], outline=255, width=max(1, int(b * .8)))
    elif stil == 'ausmalen':
        for i in range(int(max(3, h / (b * .7)))):
            yy = y0 + (i + .5) * h / max(3, h / (b * .7))
            linie(zeichnen, [(x0 + j(.3), yy + j(.2)), (x1 + j(.3), yy + j(.2))], b)
    elif stil == 'punkt':
        r = b * .9
        zeichnen.ellipse([cx - r + j(), cy - r + j(), cx + r + j(), cy + r + j()], fill=255)


def koernung(maske, staerke, rnd_np):
    """Graphit liegt nur auf den Erhebungen des Papiers: Löcher im Strich."""
    m = np.asarray(maske, dtype=np.float32) / 255
    if staerke <= 0:
        return m
    korn = rnd_np.random(m.shape).astype(np.float32)
    korn = np.asarray(Image.fromarray((korn * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), dtype=np.float32) / 255
    return m * np.clip(1 - staerke * (1.4 * (korn - 0.5) + 0.5), 0, 1)


def bearbeiten_antwortbogen(cfg, rnd):
    a = cfg['antworten']
    aus, radiert = [], []
    for nr in range(144):
        r = rnd.random()
        if r < a['leer']:
            aus.append('.')
        elif r < a['leer'] + a['doppelt']:
            aus.append('*')
        else:
            aus.append(rnd.choice(BST))
    for nr in range(144):
        if aus[nr] in BST and rnd.random() < a['radiert']:
            radiert.append(nr)
    return ''.join(aus), radiert


def bearbeiten_konztest(cfg, ziele, rnd):
    k = cfg['konz']
    bis = rnd.randint(*k['bis'])
    aus = []
    for n in range(1600):
        z = ziele[n // 40][n % 40] == '1'
        aus.append('0' if n > bis else ('1' if rnd.random() < (k['treffer'] if z else k['daneben']) else '0'))
    aus[bis] = '1'
    return ''.join(aus), bis


def blatt_rendern(cfg, rnd, rnd_np):
    """Das ausgefüllte Blatt als RGB-Bild (dpi) und die Wahrheit."""
    dpi = cfg['dpi']
    s = dpi / 72
    art = cfg['art']
    if art == 'antwortbogen':
        pfad, seite, felder = antwortbogen_vorlage(cfg['jahr'])
    else:
        pfad, seite, k = konztest_vorlage(cfg['konztest'])
    pix = pymupdf.open(pfad)[seite].get_pixmap(dpi=dpi)
    leer = np.asarray(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), dtype=np.float32)
    # Papierton und -struktur
    ton = np.array(cfg['papier']['ton'], np.float32) / 255
    blatt = leer * ton
    faser = rnd_np.normal(0, 1, leer.shape[:2]).astype(np.float32)
    faser = np.asarray(Image.fromarray(np.clip(128 + 40 * faser, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32)
    blatt *= (1 + (faser[..., None] - 128) / 128 * 0.025)
    stift = Stift(cfg['stift'], art, s)
    st = cfg['stift']
    maske = Image.new('L', (pix.width, pix.height), 0)
    zeichnen = ImageDraw.Draw(maske)
    hauch = Image.new('L', (pix.width, pix.height), 0)
    hauch_zeichnen = ImageDraw.Draw(hauch)
    stile = {}
    wahrheit = {'art': art}
    if art == 'antwortbogen':
        antworten, radiert = bearbeiten_antwortbogen(cfg, rnd)
        for nr, a in enumerate(antworten):
            if a == '.':
                continue
            wahl = [BST.index(a)] if a in BST else rnd.sample(range(5), 2)
            stil = st['stil'] if rnd.random() < st['anteil_stil'] else 'schraeg'
            if stil != 'schraeg':
                stile[nr] = stil
            for kk in wahl:
                box = [v * s for v in felder[nr][kk]]
                zeichne_markierung(zeichnen, stil, box, stift, s, rnd, st['daneben_mm'])
            if nr in radiert:
                kk = rnd.choice([i for i in range(5) if i not in wahl])
                zeichne_markierung(hauch_zeichnen, 'schraeg', [v * s for v in felder[nr][kk]], stift, s, rnd, st['daneben_mm'])
        wahrheit.update(jahr=cfg['jahr'], antworten=antworten, radiert=radiert)
    else:
        markiert, bis = bearbeiten_konztest(cfg, k['ziele'], rnd)
        zx, zy = k['x'], k['y']
        for n, m in enumerate(markiert):
            if m != '1':
                continue
            x, y = zx[n % 40] * s, zy[n // 40] * s
            box = (x - 4.5 * s, y - 5.5 * s, x + 4.5 * s, y + 5.5 * s)
            stil = st['stil'] if rnd.random() < st['anteil_stil'] else 'schraeg'
            if stil != 'schraeg':
                stile[n] = stil
            zeichne_markierung(zeichnen, stil, box, stift, s, rnd, st['daneben_mm'])
        wahrheit.update(konztest=cfg['konztest'], markiert=markiert, bis=bis, ziele=''.join(k['ziele']))
    wahrheit['stile'] = {str(k): v for k, v in stile.items()}
    wahrheit['stift'] = stift.art
    # Strich auftragen: Graphit/Tinte deckt, mit Körnung
    a = koernung(maske, stift.koernung, rnd_np) * stift.deckung
    if stift.art == 'fineliner':
        a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    farbe = np.array(stift.farbe, np.float32)
    blatt = blatt * (1 - a[..., None]) + farbe * a[..., None]
    h = koernung(hauch, 0.5, rnd_np) * 0.13
    h = np.asarray(Image.fromarray((h * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.0)), np.float32) / 255
    blatt = blatt * (1 - h[..., None]) + farbe * h[..., None]
    # Verschmiert (Handballen über Graphit)
    v = cfg['papier']['verschmiert']
    if v > 0:
        fleck = Image.new('L', (pix.width, pix.height), 0)
        fz = ImageDraw.Draw(fleck)
        for _ in range(int(3 + 6 * v)):
            cx, cy = rnd.uniform(0.1, 0.9) * pix.width, rnd.uniform(0.25, 0.95) * pix.height
            rx, ry = rnd.uniform(0.05, 0.15) * pix.width, rnd.uniform(0.01, 0.04) * pix.height
            fz.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=int(40 * v + 10))
        f = np.asarray(fleck.filter(ImageFilter.GaussianBlur(25)), np.float32) / 255
        blatt = blatt * (1 - f[..., None]) + farbe * f[..., None]
    # Knick: eine Falzlinie quer über das Blatt (leichter Schatten)
    if cfg['papier']['knick']:
        yy = np.arange(pix.height, dtype=np.float32)[:, None]
        mitte = pix.height * rnd.uniform(0.3, 0.7)
        blatt *= (1 - 0.08 * np.exp(-((yy - mitte) / (0.004 * pix.height)) ** 2))[..., None]
    return np.clip(blatt, 0, 255).astype(np.uint8), wahrheit


def finger_malen(blatt, cfg, s, rnd):
    f = cfg['kamera']['finger']
    if not f:
        return blatt
    im = Image.fromarray(blatt).convert('RGBA')
    H, W = blatt.shape[:2]
    g = f.get('groesse_mm', 20) * s / MM
    pos = {'ol': (0.02, 0.0), 'or': (0.98, 0.0), 'ul': (0.02, 1.0), 'ur': (0.98, 1.0),
           'l': (0.0, 0.5), 'r': (1.0, 0.55), 'u': (0.5, 1.0), 'o': (0.5, 0.0)}[f.get('ecke', 'ul')]
    cx, cy = pos[0] * W, pos[1] * H
    schicht = Image.new('RGBA', im.size, (0, 0, 0, 0))
    z = ImageDraw.Draw(schicht)
    haut = (int(205 + rnd.uniform(-25, 15)), int(150 + rnd.uniform(-25, 15)), int(125 + rnd.uniform(-25, 15)))
    for i in range(10):
        k = 1 - i / 12
        farbe = tuple(int(c * (0.82 + 0.18 * (1 - k))) for c in haut) + (255,)
        z.ellipse([cx - g * .55 * k, cy - g * k, cx + g * .55 * k, cy + g * k], fill=farbe)
    schicht = schicht.filter(ImageFilter.GaussianBlur(2))
    im.alpha_composite(schicht)
    return np.asarray(im.convert('RGB'))


# ------------------------------------------------------------- Kamera
def blick(ziel, abstand, neigung, drehung):
    """Kameramittelpunkt C und Rotation R (Welt -> Kamera). Welt: x rechts,
    y nach unten (Blatt), z in den Tisch; die Kamera schaut in +z."""
    vor = np.array([math.tan(math.radians(neigung[1])), math.tan(math.radians(neigung[0])), 1.0])
    vor /= np.linalg.norm(vor)
    C = np.array(ziel, float) - vor * abstand
    unten_hint = np.array([0.0, 1.0, 0.0])
    rechts = np.cross(unten_hint, vor); rechts /= np.linalg.norm(rechts)
    unten = np.cross(vor, rechts)
    a = math.radians(drehung)
    r2 = math.cos(a) * rechts + math.sin(a) * unten
    u2 = -math.sin(a) * rechts + math.cos(a) * unten
    return C, np.stack([r2, u2, vor])


def woelbung_z(X, Y, w_mm, art):
    """Höhe des Blatts (mm, zur Kamera hin) - leicht gewölbt wie ein Blatt,
    das gefaltet in der Mappe lag."""
    if w_mm <= 0:
        return np.zeros_like(X)
    u = (X / 210.0) * 2 - 1
    v = (Y / 297.0) * 2 - 1
    if art == 0:
        return w_mm * u ** 2                      # Ränder links/rechts heben sich
    if art == 1:
        return w_mm * (1 - u ** 2) * 0.6 + w_mm * 0.4 * v ** 2   # Buckel in der Mitte
    return w_mm * np.clip(v, 0, None) ** 2        # unterer Rand rollt sich


def auf_ebene(u, v, C, R, f, W, H, zfun, iter_=4):
    """Bildpunkte -> Punkte auf dem (gewölbten) Blatt in mm."""
    d = np.stack([(u - W / 2) / f, (v - H / 2) / f, np.ones_like(u)], -1) @ R  # Welt-Richtung
    ok = d[..., 2] > 1e-6
    Zs = np.zeros(u.shape)
    for _ in range(iter_):
        t = (Zs - C[2]) / np.where(ok, d[..., 2], 1)
        X = C[0] + t * d[..., 0]
        Y = C[1] + t * d[..., 1]
        Zs = -zfun(X, Y)
    return X, Y, ok & (t > 0)


def netz_transform(quelle, groesse, C, R, f, zfun, px_mm, versatz=(0, 0), raster=40):
    """quelle (PIL, mm * px_mm Pixel, Ursprung bei versatz mm) auf das Kamerabild."""
    W, H = groesse
    nx, ny = raster, int(raster * H / W)
    us = np.linspace(0, W, nx + 1)
    vs = np.linspace(0, H, ny + 1)
    U, V = np.meshgrid(us, vs)
    X, Y, ok = auf_ebene(U, V, C, R, f, W, H, zfun)
    SX = (X - versatz[0]) * px_mm
    SY = (Y - versatz[1]) * px_mm
    netz = []
    for j in range(ny):
        for i in range(nx):
            if not (ok[j, i] and ok[j + 1, i] and ok[j + 1, i + 1] and ok[j, i + 1]):
                continue
            box = (int(round(us[i])), int(round(vs[j])), int(round(us[i + 1])), int(round(vs[j + 1])))
            quad = (SX[j, i], SY[j, i], SX[j + 1, i], SY[j + 1, i], SX[j + 1, i + 1], SY[j + 1, i + 1], SX[j, i + 1], SY[j, i + 1])
            netz.append((box, quad))
    return quelle.transform((W, H), Image.MESH, netz, Image.BILINEAR, fillcolor=(0, 0, 0, 0))


def hintergrund_textur(art, rnd, rnd_np):
    """Tisch im Bereich -700..1000 x -700..1100 mm, 1.5 px/mm."""
    w, h = 2550, 2700
    if art == 'holz':
        x = np.linspace(0, 1, w)[None, :]
        y = np.linspace(0, 1, h)[:, None]
        maser = np.sin((x * 60 + 3 * np.sin(y * 7) + rnd_np.normal(0, 0.15, (h, w))) * 2) * 0.5 + 0.5
        basis = np.stack([150 + 30 * maser, 105 + 22 * maser, 70 + 15 * maser], -1)
    elif art == 'weiss':
        basis = np.ones((h, w, 3)) * [232, 230, 226] + rnd_np.normal(0, 2, (h, w, 1))
    elif art == 'dunkel':
        basis = np.ones((h, w, 3)) * [45, 44, 48] + rnd_np.normal(0, 3, (h, w, 1))
    elif art == 'unruhig':
        basis = np.ones((h, w, 3)) * [120, 110, 100] + rnd_np.normal(0, 3, (h, w, 1))
        im = Image.fromarray(np.clip(basis, 0, 255).astype(np.uint8))
        z = ImageDraw.Draw(im)
        for _ in range(14):   # andere Blätter, Hefte, Stifte
            x0, y0 = rnd.uniform(0, w), rnd.uniform(0, h)
            bw, bh = rnd.uniform(120, 500), rnd.uniform(80, 600)
            c = rnd.choice([(240, 240, 235), (230, 225, 210), (60, 70, 140), (200, 60, 50), (30, 30, 30)])
            z.rectangle([x0, y0, x0 + bw, y0 + bh], fill=c)
            if c[0] > 200:
                for yy in range(int(y0) + 15, int(y0 + bh) - 5, 14):
                    z.line([(x0 + 10, yy), (x0 + bw - rnd.uniform(10, 80), yy)], fill=(70, 70, 70), width=2)
        basis = np.asarray(im, np.float32)
    else:
        basis = np.ones((h, w, 3)) * [128, 124, 118] + rnd_np.normal(0, 3, (h, w, 1))
    return Image.fromarray(np.clip(basis, 0, 255).astype(np.uint8)).convert('RGBA')


def glatt(t):
    return t * t * (3 - 2 * t)


class Bewegung:
    """Kamerapose über die Zeit: Phasen + Handzittern + Drift."""
    def __init__(self, k, rnd):
        self.k = k
        self.rnd = rnd
        self.phasen = []
        t = 0
        for name, dauer in k['ablauf']:
            self.phasen.append((name, t, t + dauer))
            t += dauer
        self.dauer = t
        # Zittern: Summe von Sinus (3-11 Hz) mit zufälliger Phase, Drift langsam
        self.z = [(rnd.uniform(3, 11), rnd.uniform(0, 6.3), rnd.uniform(0.4, 1.0)) for _ in range(6)]
        self.d = [(rnd.uniform(0.15, 0.6), rnd.uniform(0, 6.3)) for _ in range(3)]

    def zittern(self, t, i):
        s = sum(a * math.sin(2 * math.pi * fr * t + ph + i * 1.7) for fr, ph, a in self.z) / 2.2
        return s

    def drift(self, t, i):
        return sum(math.sin(2 * math.pi * fr * t + ph + i * 2.3) for fr, ph in self.d) / 3

    def pose(self, t, ziel_basis, abstand_basis):
        k = self.k
        phase, t0, t1 = next(((n, a, b) for n, a, b in self.phasen if a <= t < b), self.phasen[-1])
        p = (t - t0) / max(1e-6, t1 - t0)
        neig = list(k['neigung_grad'])
        dreh = k['drehung_grad']
        ziel = np.array(ziel_basis, float)
        ab = abstand_basis
        sichtbar = True
        if phase in ('tisch', 'weg'):
            ziel = ziel + np.array([380.0, 120.0, 0])   # Kamera zeigt neben das Blatt
            ab *= 1.3
        elif phase in ('anflug', 'zurueck'):
            q = glatt(p)
            ziel = ziel + np.array([380.0, 120.0, 0]) * (1 - q)
            ab *= 1.3 - 0.3 * q
            neig = [neig[0] + 18 * (1 - q), neig[1] - 10 * (1 - q)]
            dreh = dreh + 12 * (1 - q)
        elif phase == 'wackeln':
            ziel = ziel + np.array([25 * math.sin(7 * t), 18 * math.sin(5.3 * t + 1), 0])
            dreh = dreh + 4 * math.sin(4.1 * t)
        zm, zg, dm = k['zittern_mm'], k['zittern_grad'], k['drift_mm']
        ziel = ziel + np.array([zm * self.zittern(t, 0) + dm * self.drift(t, 0), zm * self.zittern(t, 1) + dm * self.drift(t, 1), 0])
        ab = ab + zm * self.zittern(t, 2) + dm * self.drift(t, 2)
        neig = [neig[0] + zg * self.zittern(t, 3), neig[1] + zg * self.zittern(t, 4)]
        dreh = dreh + zg * self.zittern(t, 5)
        return ziel, ab, neig, dreh, phase


def kamera_bild(blatt_rgba, tisch, cfg, t, bew, rnd_np, zustand, f, W, H, ziel0, ab0, woelbung):
    k = cfg['kamera']
    px_mm_blatt = blatt_rgba.size[0] / 210.0
    zfun_blatt = lambda X, Y: woelbung(X, Y)
    # Bewegungsunschärfe: mehrere Unterbilder während der Belichtung
    teile = []
    belicht = k['belichtungszeit_s']
    ziel, ab, neig, dreh, phase = bew.pose(t, ziel0, ab0)
    ziel2, ab2, neig2, dreh2, _ = bew.pose(t + belicht, ziel0, ab0)
    C1, R1 = blick(ziel, ab, neig, dreh)
    C2, R2 = blick(ziel2, ab2, neig2, dreh2)
    # Bewegung in Pixeln abschätzen (Mitte des Blatts)
    def proj(C, R, P):
        q = R @ (np.array(P) - C)
        return np.array([f * q[0] / q[2] + W / 2, f * q[1] / q[2] + H / 2])
    weg_px = np.linalg.norm(proj(C1, R1, [105, 148, 0]) - proj(C2, R2, [105, 148, 0]))
    n = int(min(6, max(1, math.ceil(weg_px / 1.5))))
    acc = None
    for i in range(n):
        tt = t + belicht * (i / max(1, n - 1) if n > 1 else 0)
        zi, abi, ni, di, _ = bew.pose(tt, ziel0, ab0)
        C, R = blick(zi, abi, ni, di)
        bild = netz_transform(tisch, (W, H), C, R, f, lambda X, Y: np.zeros_like(X), 1.5, versatz=(-700, -700), raster=12)
        bl = netz_transform(blatt_rgba, (W, H), C, R, f, zfun_blatt, px_mm_blatt, raster=28)
        bild.alpha_composite(bl)
        a = np.asarray(bild.convert('RGB'), np.float32)
        acc = a.copy() if acc is None else acc + a
    img = acc / n if n > 1 else acc
    if 'gitter' not in zustand:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        zustand['gitter'] = (xx / W - 0.5, yy / H - 0.5)
        zustand['vign'] = None
    xn, yn = zustand['gitter']
    licht = np.ones((H, W), np.float32)
    L = k['licht']
    if L.get('verlauf'):
        w = zustand['licht_winkel']
        licht *= 1 - L['verlauf'] * (math.cos(w) * xn + math.sin(w) * yn + 0.5)
    sch = L.get('schatten')
    if sch:
        sx, sy = zustand['schatten_pos']
        if sch.get('bewegt'):
            sx += 0.05 * math.sin(1.3 * t); sy += 0.04 * math.sin(0.9 * t + 1)
        r = sch['groesse']
        dist = np.sqrt(((xn - sx) / r) ** 2 + ((yn - sy) / (r * 0.7)) ** 2)
        weich = max(0.02, sch['weich'])
        licht *= 1 - sch['staerke'] * np.clip((1 - dist) / weich, 0, 1)
    v = k['vignette']
    if zustand['vign'] is None:
        zustand['vign'] = (1 - v * (xn ** 2 + yn ** 2) * 2).astype(np.float32)
    licht *= zustand['vign']
    img *= licht[..., None]
    gl = L.get('glanz')
    if gl:
        gx, gy = zustand['glanz_pos']
        g = (gl['staerke'] * np.exp(-(((xn - gx) ** 2 + (yn - gy) ** 2) / (2 * gl['groesse'] ** 2)))).astype(np.float32)
        img += (255 - img) * g[..., None]
    # Belichtungsautomatik (träge) und Weissabgleich
    ziel_hell = 128 / max(20, float(img[::8, ::8].mean()))
    zustand['gain'] += (ziel_hell * k['belichtung'] - zustand['gain']) * 0.25
    gain = zustand['gain'] * (1 + k['ae_schwanken'] * math.sin(2.1 * t))
    img *= (gain * np.array(k['weissabgleich'], np.float32))
    # Optik zuerst (Fokus, Objektiv), dann der Sensor (Rauschen), dann die
    # Bildverarbeitung des Handys: Farbrauschen stark glätten, Helligkeit
    # leicht entrauschen und schärfen (nur Y - Handys schärfen nicht je
    # Farbkanal), zuletzt JPEG/Video mit halber Farbauflösung (4:2:0).
    unsch = k['unschaerfe_px']
    if phase in ('anflug', 'zurueck'):
        unsch += 1.5
    elif phase == 'halten':
        zustand.setdefault('halten_ab', t)
        if t - zustand['halten_ab'] < k['fokus_jagen_s']:
            unsch += 2.5 * (1 - (t - zustand['halten_ab']) / max(1e-6, k['fokus_jagen_s']))
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if unsch > 0.05:
        im = im.filter(ImageFilter.GaussianBlur(unsch))
    rs = k['rauschen']
    if rs > 0:
        img = np.asarray(im, np.float32)
        sigma = np.sqrt(img * (rs / 40) + rs ** 2 * 0.5)
        img = img + rnd_np.standard_normal(img.shape, dtype=np.float32) * sigma
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    y, cb, cr = im.convert('YCbCr').split()
    if rs > 0:
        y = y.filter(ImageFilter.GaussianBlur(0.5))
        cb = cb.filter(ImageFilter.GaussianBlur(1.6))
        cr = cr.filter(ImageFilter.GaussianBlur(1.6))
    if k['isp_schaerfen'] > 0:
        y = y.filter(ImageFilter.UnsharpMask(radius=2, percent=int(80 * k['isp_schaerfen']), threshold=2))
    im = Image.merge('YCbCr', (y, cb, cr)).convert('RGB')
    return im, phase


def main():
    cfg = mischen(STANDARD, json.load(open(sys.argv[1])))
    aus = sys.argv[2]
    os.makedirs(aus, exist_ok=True)
    rnd = random.Random(cfg['seed'])
    rnd_np = np.random.default_rng(cfg['seed'])
    blatt, wahrheit = blatt_rendern(cfg, rnd, rnd_np)
    s = cfg['dpi'] / 72
    blatt = finger_malen(blatt, cfg, s, rnd)
    blatt_rgba = Image.fromarray(blatt).convert('RGBA')
    # Blatt auf 210 x 297 mm genau skalieren (PDF-Seite ist A4)
    blatt_rgba = blatt_rgba.resize((int(210 * 6), int(297 * 6)), Image.LANCZOS)   # 6 px/mm (~152 dpi)
    k = cfg['kamera']
    W, H = k['aufloesung']
    f = (W / 2) / math.tan(math.radians(k['hfov_grad'] / 2))
    # Abstand so, dass das Blatt die gewünschte Fläche füllt
    fuell = k['fuellung']
    ab0 = max(210 * f / (fuell * W), 297 * f / (fuell * H))
    ziel0 = [105 - k['versatz'][0] * 210, 148.5 - k['versatz'][1] * 297, 0]
    tisch = hintergrund_textur(k['hintergrund'], rnd, rnd_np)
    wart = rnd.choice([0, 1, 2])
    woelbung = lambda X, Y: woelbung_z(X, Y, cfg['papier']['woelbung_mm'], wart)
    bew = Bewegung(k, rnd)
    zustand = {'gain': 1.0, 'licht_winkel': rnd.uniform(0, 2 * math.pi),
               'schatten_pos': (rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35)),
               'glanz_pos': (rnd.uniform(-0.25, 0.25), rnd.uniform(-0.3, 0.3))}
    fps = 30
    n = int(bew.dauer * fps)
    standbild_t = None
    halte = [(a, b) for name, a, b in bew.phasen if name == 'halten']
    if halte:
        standbild_t = halte[0][0] + min(1.5, (halte[0][1] - halte[0][0]) / 2)
    vorschau = []
    with open(os.path.join(aus, 'video.mjpeg'), 'wb') as fv:
        for i in range(n):
            t = i / fps
            im, phase = kamera_bild(blatt_rgba, tisch, cfg, t, bew, rnd_np, zustand, f, W, H, ziel0, ab0, woelbung)
            b = io.BytesIO()
            im.save(b, 'JPEG', quality=k['jpeg'])
            fv.write(b.getvalue())
            if standbild_t is not None and abs(t - standbild_t) < 0.5 / fps:
                im.save(os.path.join(aus, 'standbild.jpg'), quality=92)
            if i % max(1, n // 6) == 0:
                vorschau.append(im.resize((W // 4, H // 4)))
    mont = Image.new('RGB', (sum(v.size[0] for v in vorschau), vorschau[0].size[1]), (0, 0, 0))
    x = 0
    for v in vorschau:
        mont.paste(v, (x, 0)); x += v.size[0]
    mont.save(os.path.join(aus, 'vorschau.jpg'), quality=80)
    wahrheit['konfig'] = cfg
    wahrheit['dauer_s'] = bew.dauer
    json.dump(wahrheit, open(os.path.join(aus, 'wahrheit.json'), 'w'), indent=1)
    print('fertig', aus, n, 'Bilder', '%.0f MB' % (os.path.getsize(os.path.join(aus, 'video.mjpeg')) / 1e6))


if __name__ == '__main__':
    main()
