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

ZU ERWARTEN SIND GENAU ZEHN UNERREICHBARE SEITEN, alle absichtlich nirgends
verlinkt: der Mitgliederbereich (/mitglieder/ und die beiden Unterseiten, mal
drei Sprachen = 9, siehe docs/WARTUNG.md, Abschnitt "Mitgliederbereich") und
die Alpha-Seite /alpha/ (Abschnitt 11b-3). Taucht sonst etwas auf, ist es ein
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
