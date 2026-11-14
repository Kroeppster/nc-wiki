#!/usr/bin/env python3
"""
================================================================================
STRUKTUR-PRUEFSTAND: DOPPELTE, VERWAISTE UND TOTE SEITEN
================================================================================
Liest den gebauten Ordner und beantwortet drei Fragen, die man einer Website
nicht ansieht:

  1. Gibt es Seiten mit IDENTISCHEM Inhalt unter verschiedenen Adressen?
  2. Welche Seiten sind von der Startseite aus NICHT erreichbar?
  3. Welche Links zeigen auf Seiten, die es nicht gibt?

    python3 scripts/struktur-pruefen.py

Geprueft wird der Ordner "public" neben dem Projekt, also das Ergebnis von
"hugo --minify". Ein anderer Ordner laesst sich als Argument uebergeben:

    python3 scripts/struktur-pruefen.py pfad/zum/ordner

(Frueher stand hier ein fest eingetragener Pfad in den Temp-Ordner einer
einzelnen Sitzung. Der zeigte spaeter auf einen alten Build, und das Skript
pruefte klaglos den Stand von vorgestern - deshalb jetzt der Projektordner.)

ZU ERWARTEN SIND GENAU ZWOELF UNERREICHBARE SEITEN, alle absichtlich nirgends
verlinkt: der Mitgliederbereich (/mitglieder/ und die beiden Unterseiten, mal
drei Sprachen = 9, siehe docs/WARTUNG-DETAILLIERT.md, Abschnitt "Mitgliederbereich") und
die Alpha-Seite (/alpha/, /fr/alpha/, /it/alpha/; Abschnitt 11, «Alpha-Seite»). Taucht sonst etwas auf, ist es ein
Fund.

Weiterleitungsseiten (Hugo legt sie z.B. fuer /de/ an) werden erkannt und
nicht als Inhalt gezaehlt.
================================================================================
"""
import os, re, sys, hashlib, json, collections
from urllib.parse import unquote
PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WURZEL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PROJEKT, 'public')
if not os.path.isdir(WURZEL):
    sys.exit(f'Ordner "{WURZEL}" gibt es nicht. Zuerst "hugo --minify" laufen lassen.')

seiten = {}
for dp, dn, fn in os.walk(WURZEL):
    if 'index.html' not in fn: continue
    pfad = '/' + os.path.relpath(os.path.join(dp,'index.html'), WURZEL).replace('index.html','').rstrip('/') + '/'
    pfad = pfad.replace('//','/')
    seiten[pfad] = os.path.join(dp,'index.html')

weiterleitung, inhalt, links = {}, {}, {}
for pfad, datei in seiten.items():
    h = open(datei, encoding='utf-8', errors='replace').read()
    if 'http-equiv=refresh' in h or 'http-equiv="refresh"' in h:
        m = re.search(r'url=([^"\'>\s]+)', h)
        weiterleitung[pfad] = m.group(1) if m else '?'
        continue
    m = re.search(r'<main.*?>(.*?)</main>', h, re.S)
    kern = m.group(1) if m else h
    text = re.sub(r'<[^>]+>', ' ', kern)
    text = re.sub(r'\s+', ' ', text).strip()
    inhalt[pfad] = (hashlib.sha1(text.encode()).hexdigest(), len(text), text[:80])
    links[pfad] = set()
    for href in re.findall(r'href=["\']?([^"\'>\s]+)', h):
        if href.startswith(('http://','https://','mailto:','tel:','#','javascript:')): continue
        href = unquote(href.split('#')[0].split('?')[0])
        if not href: continue
        if not href.startswith('/'):
            href = os.path.normpath(os.path.join(os.path.dirname(pfad.rstrip('/')), href))
        if not href.endswith('/'): 
            if '.' in os.path.basename(href): continue   # Datei, keine Seite
            href += '/'
        links[pfad].add(href)

print('Seiten gesamt:        %d' % len(seiten))
print('davon Weiterleitung:  %d' % len(weiterleitung))
print('echte Inhaltsseiten:  %d' % len(inhalt))

# --- 1) Doppelte Inhalte ---------------------------------------------------
nach_hash = collections.defaultdict(list)
for p,(h,n,t) in inhalt.items():
    if n > 40: nach_hash[h].append((p,n,t))
dubletten = {h:v for h,v in nach_hash.items() if len(v)>1}
print('\n=== DOPPELTE INHALTE: %d Gruppen ===' % len(dubletten))
for h,v in sorted(dubletten.items(), key=lambda x:-len(x[1]))[:25]:
    print('  [%d Seiten, %d Zeichen] %s' % (len(v), v[0][1], v[0][2][:60]))
    for p,_,_ in sorted(v): print('      ', p)

# --- 2) Erreichbarkeit ------------------------------------------------------
start = ['/']
gesehen, rand = set(), list(start)
while rand:
    p = rand.pop()
    if p in gesehen: continue
    gesehen.add(p)
    ziel = weiterleitung.get(p)
    for l in links.get(p, ()):
        if l in seiten and l not in gesehen: rand.append(l)
        elif l in weiterleitung and l not in gesehen: rand.append(l)
erreichbar = gesehen & set(seiten)
verwaist = sorted(set(inhalt) - erreichbar)
print('\n=== NICHT VON DER STARTSEITE AUS ERREICHBAR: %d ===' % len(verwaist))
for p in verwaist[:60]: print('   ', p)
if len(verwaist)>60: print('    ... und %d weitere' % (len(verwaist)-60))

# --- 3) Links ins Leere -----------------------------------------------------
tot = collections.defaultdict(set)
for p, ls in links.items():
    for l in ls:
        if l not in seiten and l not in weiterleitung:
            tot[l].add(p)
print('\n=== LINKS AUF NICHT VORHANDENE SEITEN: %d ===' % len(tot))
for l, von in sorted(tot.items())[:30]:
    print('   %s   <- %s' % (l, sorted(von)[0] + (' (+%d)' % (len(von)-1) if len(von)>1 else '')))

# --- 4) Sprachfassungen mit verschiedenem Dateinamen -------------------------
# Hugo verknuepft die Sprachfassungen einer Seite ueber den Dateinamen
# (content/de/news/x.md <-> content/fr/news/x.md). Der Web-Editor bildet den
# Dateinamen aus dem Titel - legt jemand dieselbe News dort in zwei Sprachen an,
# heissen die Dateien verschieden: Die Sprachwahl findet die andere Fassung
# nicht, und Suchmaschinen erfahren nicht, dass die Seiten zusammengehoeren.
# Gemeldet wird eine Seite, die es nur in einer Sprache gibt, wenn im selben
# Ordner einer anderen Sprache eine Seite mit demselben Datum liegt, die dort
# ebenfalls allein steht. Abhilfe: eine der Dateien umbenennen (docs/WARTUNG.md,
# Abschnitt 8) oder in beiden denselben "translationKey:" in den Seitenkopf.
import glob
def _kopf(pfad, feld):
    t = open(pfad, encoding='utf-8', errors='replace').read()
    m = re.search(r'^%s:\s*["\']?([^"\'\n]+)' % feld, t, re.M)
    return m.group(1).strip() if m else None
INHALT = os.path.join(PROJEKT, 'content')
je = {l: {os.path.relpath(f, os.path.join(INHALT, l)) for f in glob.glob(os.path.join(INHALT, l, '**', '*.md'), recursive=True)}
      for l in ('de', 'fr', 'it') if os.path.isdir(os.path.join(INHALT, l))}
paare = []
for a in je:
    for b in je:
        if a >= b: continue
        nur_a = [x for x in je[a] - je[b] if not _kopf(os.path.join(INHALT, a, x), 'translationKey')]
        nur_b = [x for x in je[b] - je[a] if not _kopf(os.path.join(INHALT, b, x), 'translationKey')]
        for x in nur_a:
            dx = (_kopf(os.path.join(INHALT, a, x), 'date') or '')[:10]
            if not dx: continue
            for y in nur_b:
                if os.path.dirname(x) == os.path.dirname(y) and (_kopf(os.path.join(INHALT, b, y), 'date') or '')[:10] == dx:
                    paare.append('%s/%s  <->  %s/%s  (%s)' % (a, x, b, y, dx))
print('\n=== VERMUTLICH DIESELBE SEITE UNTER VERSCHIEDENEM DATEINAMEN: %d ===' % len(paare))
for z in sorted(paare)[:30]: print('   ', z)
