#!/usr/bin/env python3
"""
==============================================================================
PRÜFUNG DER FERTIG GEBAUTEN WEBSITE (läuft in GitHub Actions vor dem Hochladen)
==============================================================================
Prüft den fertigen Ordner public/ - so, wie er veröffentlicht wird - auf drei
Fehlerarten, die man lokal leicht übersieht, weil dort die Website unter "/"
statt unter "/nc-wiki/" liegt und der Mitgliederbereich nicht verschlüsselt ist:

  1. Pfade ohne Projektpfad: Ein Bild, eine Tondatei oder ein Skript mit einer
     Adresse wie "/images/x.png" funktioniert lokal, live unter
     kroeppster.github.io/nc-wiki/ aber nicht. Die Linkprüfung (lychee) sieht
     nur Links im HTML, nicht Adressen in Skripten und Stylesheets.
  2. Grundangaben jeder Seite: Titel, Beschreibung, genau eine Hauptüberschrift
     (h1) und die richtige Sprache im <html lang>.
  3. Mitgliederbereich und Alpha-Seite (geschuetzt: true): Jede dieser Seiten
     muss verschlüsselt sein, und kein Satz daraus darf sonst irgendwo stehen
     (in anderen Seiten, im Suchindex, in Sitemap oder RSS).

Bei einem Fund bricht der Lauf ab, und nichts wird veröffentlicht.

    python3 scripts/ausgabe-pruefen.py public                       # lokal
    python3 scripts/ausgabe-pruefen.py public --basis /nc-wiki --verschluesselt

--basis: der Projektpfad der Website (leer = Website liegt direkt unter "/").
--verschluesselt: nach dem Schritt "Protect members-only pages" (nur bei einem
  Push auf main - bei einem Pull Request wird nicht verschlüsselt, siehe
  .github/workflows/hugo.yml). Ohne den Schalter wird Teil 3 übersprungen.

Entstanden aus dem Testlauf vom Oktober 2026 (A1, A2, A8); dort ohne Fund.
==============================================================================
"""
import glob, gzip, html, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
if not args:
    sys.exit(__doc__)
PUB = os.path.abspath(args[0])
BASIS = ''
if '--basis' in sys.argv:
    BASIS = '/' + sys.argv[sys.argv.index('--basis') + 1].strip('/')
    BASIS = '' if BASIS == '/' else BASIS
VERSCHLUESSELT = '--verschluesselt' in sys.argv
if not os.path.isdir(PUB):
    sys.exit(f'Ordner "{PUB}" gibt es nicht. Zuerst die Website bauen.')

funde = []
def fund(art, text):
    funde.append(f'{art}: {text}')

def lies(pfad):
    with open(pfad, 'rb') as f:
        b = f.read()
    if pfad.endswith(('.pf_fragment', '.pf_index', '.pf_meta', '.pf_filter')):
        try:
            b = gzip.decompress(b)
        except OSError:
            pass
    return b.decode('utf-8', 'ignore')

dateien = {}
for root, _, files in os.walk(PUB):
    for f in files:
        if f.endswith(('.html', '.css', '.js', '.json', '.xml', '.pf_fragment', '.pf_index', '.pf_meta')):
            p = os.path.join(root, f)
            dateien[p] = lies(p)
rel = lambda p: p[len(PUB):]

# ---------------------------------------------------------------- 1. Pfade
if BASIS:
    attr = re.compile(r'''(?:href|src|action|srcset|poster|data-[a-z-]+)\s*=\s*["']?(/(?!/)[^"'\s>]*)''')
    skript = re.compile(r'''["'`](/(?:images|audio|downloads|pagefind|css|js|fonts|fr|it|ems|news|alpha|mitglieder)/[^"'`\s]*)["'`]''')
    for p, t in dateien.items():
        if '/pagefind/' in p or not p.endswith(('.html', '.css', '.js')):
            continue
        for m in list(attr.finditer(t)) + list(skript.finditer(t)):
            u = m.group(1)
            if not (u == BASIS or u.startswith(BASIS + '/')):
                fund('Pfad ohne ' + BASIS, f'{u[:70]} in {rel(p)}')

# ------------------------------------------------------- 2. Grundangaben
def gruppe(rx, t):
    m = re.search(rx, t, re.S)
    return html.unescape(m.group(1)).strip() if m else ''

for p, t in dateien.items():
    if not (p.endswith('/index.html') or p.endswith('/404.html')) or '/pagefind/' in p:
        continue
    if re.search(r'http-equiv="?refresh', t) and len(t) < 1500:
        continue   # Weiterleitung (alte Adresse)
    if 'ncwiki-geschuetzt' in t or 'staticrypt' in t:
        continue   # geschützt: siehe Teil 3
    url = rel(p)[len(BASIS):] if BASIS and rel(p).startswith(BASIS) else rel(p)
    if not gruppe(r'<title>(.*?)</title>', t):
        fund('ohne Titel', url)
    if not re.search(r'<meta name="?description"? content="?[^">\s]', t):
        fund('ohne Beschreibung', url)
    n = len(re.findall(r'<h1[\s>]', t))
    if n != 1:
        fund(f'{n} statt einer h1', url)
    lang = gruppe(r'<html[^>]*\slang="?([a-zA-Z-]+)', t)[:2]
    soll = 'fr' if url.startswith('/fr/') else 'it' if url.startswith('/it/') else 'de'
    if lang != soll:
        fund('falsche Sprache', f'{url} hat lang="{lang}", erwartet {soll}')

# --------------------------------------------- 3. geschützte Seiten
if VERSCHLUESSELT:
    saetze = set()
    for md in glob.glob(os.path.join(WURZEL, 'content', '**', '*.md'), recursive=True):
        s = open(md, encoding='utf-8').read()
        if not re.search(r'^geschuetzt:\s*true', s, re.M):
            continue
        body = s.split('---', 2)[2] if s.startswith('---') else s
        for z in body.splitlines():
            z = re.sub(r'[*_`#>\[\]()]', '', z).strip()
            if len(z) > 45 and 'baustein' not in z:
                saetze.add(z[:40])
    verschluesselt = set()
    for p, t in dateien.items():
        if not p.endswith('.html'):
            continue
        if 'staticrypt-password' in t:
            verschluesselt.add(p)
        elif 'ncwiki-geschuetzt' in t:
            fund('nicht verschlüsselt', rel(p))
    for p, t in dateien.items():
        if p in verschluesselt:
            continue
        for satz in saetze:
            if satz in t:
                fund('Klartext aus geschützter Seite', f'«{satz}» in {rel(p)}')
    print(f'Geschützt: {len(verschluesselt)} verschlüsselte Seiten, {len(saetze)} Prüfsätze.')
else:
    print('Geschützte Seiten: übersprungen (ohne --verschluesselt).')

print(f'Geprüft: {len(dateien)} Dateien' + (f', Projektpfad {BASIS}' if BASIS else '') + '.')
if funde:
    print(f'\n{len(funde)} Fund(e):')
    for f in funde[:60]:
        print('  ' + f)
    sys.exit(1)
print('Keine Funde.')
