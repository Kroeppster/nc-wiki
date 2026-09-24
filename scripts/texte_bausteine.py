#!/usr/bin/env python3
"""
================================================================================
GEMEINSAME TEILE FUER DIE TEXTLISTE
================================================================================
Wird von scripts/texte-ausgeben.py, scripts/texte-einlesen.py und
scripts/texte-mappe-pruefen.py benutzt.

WARUM DIESE DATEI EINEN UNTERSTRICH IM NAMEN HAT und nicht wie die anderen
Skripte einen Bindestrich: Python kann eine Datei mit Bindestrich nicht
importieren.

DIE WICHTIGSTE REGEL HIER: Ausgeben und Einlesen muessen eine Seite GENAU
GLEICH in Bausteine zerlegen. Deshalb steht die Zerlegung genau einmal hier.

Ein Baustein ist ein Stueck Seitentext zwischen zwei Leerzeilen: ein Absatz,
eine Liste, eine Ueberschrift, ein Code-Block. Dazu kommen die Felder aus dem
Seitenkopf, die sichtbarer Text sind (Titel, Beschreibung, Bildtext).
================================================================================
"""
import hashlib
import math
import os
import re

SPRACHEN = ('de', 'fr', 'it')

# Bausteine, die in der Tabelle gesperrt sind: Wer dort ein Zeichen
# verschiebt, macht die Seite kaputt, und dafuer ist eine Redaktionstabelle
# das falsche Werkzeug. Sie stehen grau in der Tabelle, damit man sieht, wo
# auf der Seite sie sitzen.
GESPERRT = ('tabelle', 'code', 'baustein', 'html')

# Felder im Seitenkopf, die sichtbarer Text sind.
KOPFFELDER = (('title', 'titel'), ('description', 'beschreibung'),
              ('featured_image_alt', 'bildtext'))


def pruefsumme(text):
    """Kurze Pruefsumme - erkennt beim Einlesen, ob sich eine Datei seit dem
    Ausgeben geaendert hat."""
    return hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Seitenkopf
# ---------------------------------------------------------------------------
def kopf_trennen(roh):
    """Trennt den Seitenkopf (zwischen den --- Zeilen) vom Text.

    Gibt (kopf_mit_strichen, koerper, versatz) zurueck. kopf_mit_strichen ist
    alles bis einschliesslich der schliessenden --- Zeile, versatz die
    Zeichenposition, an der der Text beginnt.
    """
    if not roh.startswith('---'):
        return '', roh, 0
    ende = roh.find('\n---', 3)
    if ende < 0:
        return '', roh, 0
    zeilenende = roh.find('\n', ende + 1)
    if zeilenende < 0:
        return roh + '\n', '', len(roh)
    return roh[:zeilenende + 1], roh[zeilenende + 1:], zeilenende + 1


def kopf_feld(kopf, feld):
    """Liest ein Textfeld aus dem Seitenkopf.

    Gibt (wert, zeile_von, zeile_bis) oder (None, None, None) zurueck;
    zeile_von/bis umfassen das ganze Feld samt Zeilenumbruch - auch die
    Folgezeilen, wenn der Wert ueber mehrere Zeilen geht. Das tut er, sobald
    der Web-Editor (Pages CMS) eine Seite gespeichert hat: Er bricht lange
    Texte um (eingerueckte Folgezeilen). Wuerde hier nur die erste Zeile
    gelesen, stuende die Beschreibung abgeschnitten in der Mappe, und beim
    Zurueckschreiben blieben die Folgezeilen als Muell im Seitenkopf stehen.

    Einzeilige Werte werden ohne YAML-Bibliothek gelesen: So bleibt der Wert
    zeichengenau, wie er dasteht (PyYAML machte z. B. aus "2024" eine Zahl).
    """
    m = re.search(r'^%s:[ \t]*(.*)$\n?' % re.escape(feld), kopf, re.MULTILINE)
    if not m:
        return None, None, None
    ende = m.end()
    folge = re.match(r'(?:[ \t]+\S.*(?:\n|$)|[ \t]*\n(?=[ \t]+\S))*', kopf[ende:])
    if folge and folge.group(0):
        # Mehrzeilig (umbrochen, oder > / | Blocktext): YAML entscheidet
        import yaml
        ende += len(folge.group(0))
        try:
            wert = yaml.safe_load(kopf[m.start():ende]).get(feld)
        except Exception:
            wert = None
        wert = '' if wert is None else str(wert)
        return wert, m.start(), ende
    wert = m.group(1).rstrip()
    if len(wert) >= 2 and wert[0] == wert[-1] and wert[0] in '"\'':
        innen = wert[1:-1]
        wert = innen.replace('\\"', '"').replace('\\\\', '\\') if wert[0] == '"' else innen.replace("''", "'")
    return wert, m.start(), m.end()


def kopfzeile(feld, wert):
    """Eine Kopfzeile so schreiben, wie Hugo sie liest."""
    return '%s: "%s"\n' % (feld, wert.replace('\\', '\\\\').replace('"', '\\"'))


def kopf_setzen(kopf, feld, wert):
    """Ein Feld im Seitenkopf setzen, anlegen oder (wert=None) entfernen.

    Ein neues Feld kommt direkt unter den Titel - dort sucht man es.
    """
    alt, von, bis = kopf_feld(kopf, feld)
    if wert is None:
        return kopf if von is None else kopf[:von] + kopf[bis:]
    zeile = kopfzeile(feld, wert)
    if von is not None:
        return kopf[:von] + zeile + kopf[bis:]
    _, tv, tb = kopf_feld(kopf, 'title')
    stelle = tb if tv is not None else kopf.find('\n') + 1
    return kopf[:stelle] + zeile + kopf[stelle:]


# ---------------------------------------------------------------------------
# Text in Bausteine zerlegen
# ---------------------------------------------------------------------------
def einordnen(text):
    """Was fuer ein Baustein ist das? Gibt einen der Schluessel zurueck:
    ueberschrift, absatz, liste, zitat, tabelle, code, baustein, html."""
    erste = text.lstrip().split('\n')[0]
    if re.match(r'^#{1,6}\s', erste):
        return 'ueberschrift'
    if erste.startswith('```'):
        return 'baustein' if re.match(r'^```\s*baustein\b', erste) else 'code'
    if erste.startswith('>'):
        return 'zitat'
    if erste.startswith('|'):
        return 'tabelle'
    if erste.startswith('<'):
        return 'html'
    if re.match(r'^\{\{[<%]', erste):
        return 'html'          # alte Shortcode-Schreibweise: ebenfalls gesperrt
    if re.match(r'^([-*+]|\d+\.)\s', erste):
        return 'liste'
    return 'absatz'


def ebene(roh):
    """Ueberschriftenebene (Anzahl #), 0 wenn keine Ueberschrift."""
    m = re.match(r'^\s*(#{1,6})\s', roh)
    return len(m.group(1)) if m else 0


def anzeige(typ, roh):
    """Wie ein Baustein in der Tabelle erscheint.

    Ueberschriften ohne ihre Rauten - die Ebene steht in der Typ-Spalte.
    &amp; als & - der Web-Editor schreibt & als &amp;, und niemand soll in
    der Tabelle Entitaeten lesen muessen. Beides wird beim Vergleich wieder
    beruecksichtigt: Unveraenderte Bausteine werden nie neu geschrieben.
    """
    if typ == 'ueberschrift':
        roh = re.sub(r'^\s*#{1,6}\s+', '', roh)
    if typ not in GESPERRT:
        roh = roh.replace('&amp;', '&')
    return roh


def bausteine_aus_text(roh):
    """Zerlegt eine Seite in Bausteine.

    Jeder Baustein ist ein dict mit:
      nr     laufende Nummer (Kopffelder zuerst, dann der Text)
      typ    titel, beschreibung, bildtext, ueberschrift, absatz, liste,
             zitat, tabelle, code, baustein, html
      roh    so, wie er in der Datei steht
      text   so, wie er in der Tabelle erscheint (siehe anzeige())
      ebene  bei Ueberschriften die Anzahl #

    Ueberschriften bekommen IMMER einen eigenen Baustein, auch wenn der Absatz
    darunter ohne Leerzeile anschliesst. Die erste Fassung hat das nicht
    getan, und "### Figuren" samt dem ganzen Absatz darunter stand in einer
    einzigen Zelle.
    """
    kopf, koerper, versatz = kopf_trennen(roh)
    raus = []

    def dazu(typ, roh_text, von, bis, text=None):
        raus.append(dict(nr=len(raus), typ=typ, roh=roh_text,
                         text=anzeige(typ, roh_text) if text is None else text,
                         ebene=ebene(roh_text) if typ == 'ueberschrift' else 0,
                         von=von, bis=bis))

    for feld, typ in KOPFFELDER:
        wert, von, bis = kopf_feld(kopf, feld)
        if wert is not None:
            dazu(typ, wert, von, bis, wert)

    # von/bis: wo der Baustein in der Datei steht. Beim Einlesen werden
    # unveraenderte Bausteine samt den Leerzeilen dazwischen zeichengenau aus
    # der Datei uebernommen - so aendert sich an einer Seite nur, was in der
    # Tabelle geaendert wurde.
    puffer, in_code, pos = [], False, versatz
    for zeile in koerper.split('\n') + ['']:
        if zeile.strip().startswith('```'):
            in_code = not in_code
        if zeile.strip() == '' and not in_code:
            if puffer:
                stueck = '\n'.join(z for z, _, _ in puffer).rstrip()
                typ = einordnen(stueck)
                if typ == 'ueberschrift' and len(puffer) > 1:
                    dazu('ueberschrift', puffer[0][0], puffer[0][1], puffer[0][2])
                    rest = '\n'.join(z for z, _, _ in puffer[1:]).rstrip().strip('\n')
                    if rest.strip():
                        dazu(einordnen(rest), rest, puffer[1][1], puffer[-1][2])
                else:
                    dazu(typ, stueck, puffer[0][1], puffer[-1][2])
                puffer = []
        else:
            puffer.append((zeile.rstrip() if not in_code else zeile, pos, pos + len(zeile)))
        pos += len(zeile) + 1
    return raus


def bausteine(pfad):
    with open(pfad, encoding='utf-8') as f:
        return bausteine_aus_text(f.read())


# ---------------------------------------------------------------------------
# Seiten finden und ordnen
# ---------------------------------------------------------------------------
def _kopfwerte(pfad):
    """Die paar Kopffelder, die fuer die Reihenfolge gebraucht werden."""
    try:
        import yaml
        with open(pfad, encoding='utf-8') as f:
            kopf, _, _ = kopf_trennen(f.read())
        daten = yaml.safe_load(kopf.strip().strip('-')) or {}
        return daten if isinstance(daten, dict) else {}
    except Exception:
        return {}


def seiten(projekt, sprache):
    """Alle Seiten einer Sprache, in der Reihenfolge der Navigationsleiste.

    Die Reihenfolge folgt dem Menue (menu.main.weight) und darunter dem Feld
    weight. Seiten, die nicht im Menue stehen (Impressum, Newsletter ...),
    kommen ans Ende. Je Seite: rel (Pfad ab Projekt), pfad, adresse, bereich
    (oberster Menuepunkt), titel, tiefe, eltern (Titel der Elternseite).
    """
    wurzel = os.path.join(projekt, 'content', sprache)
    if not os.path.isdir(wurzel):
        return []
    eintraege = []
    for ordner, _, dateien in os.walk(wurzel):
        for name in dateien:
            if name.endswith('.md'):
                eintraege.append(os.path.join(ordner, name))

    kopf = {p: _kopfwerte(p) for p in eintraege}

    def gewicht(p):
        k = kopf.get(p, {})
        menue = (k.get('menu') or {}).get('main') if isinstance(k.get('menu'), dict) else None
        if isinstance(menue, dict) and 'weight' in menue:
            return float(menue['weight'])
        if 'weight' in k:
            try:
                return 100 + float(k['weight'])
            except (TypeError, ValueError):
                pass
        return 900.0

    def ordner_index(ordner):
        p = os.path.join(ordner, '_index.md')
        return p if os.path.exists(p) else None

    def schluessel(p):
        rel = os.path.relpath(p, wurzel)
        teile = rel.replace(os.sep, '/').split('/')
        k = []
        ordner = wurzel
        for teil in teile[:-1]:
            ordner = os.path.join(ordner, teil)
            idx = ordner_index(ordner)
            k.append((gewicht(idx) if idx else 900.0, teil))
        name = teile[-1]
        if name == '_index.md':
            k.append((-1.0, ''))
        else:
            k.append((gewicht(p), (kopf[p].get('title') or name).lower()))
        # Einzelseiten ohne Menue (Impressum usw.) ans Ende, Startseite nach vorn
        if len(teile) == 1:
            if name == '_index.md':
                return [(-10.0, '')]
            return [(gewicht(p) if gewicht(p) < 900 else 950.0, name)]
        return k

    raus = []
    for p in sorted(eintraege, key=schluessel):
        rel = os.path.relpath(p, projekt).replace(os.sep, '/')
        innen = os.path.relpath(p, wurzel).replace(os.sep, '/')
        teile = innen.split('/')
        k = kopf.get(p, {})
        titel = k.get('title')
        if not titel and k.get('name'):
            titel = '%s – %s' % (k.get('name'), k.get('jahr', ''))
        titel = str(titel or teile[-1][:-3])
        oberster = teile[0] if len(teile) > 1 else ('' if teile[0] == '_index.md' else teile[0][:-3])
        eltern_ordner = os.path.dirname(p) if teile[-1] != '_index.md' else os.path.dirname(os.path.dirname(p))
        eltern = None
        if len(teile) > 1 and eltern_ordner.startswith(wurzel):
            ep = ordner_index(eltern_ordner)
            if ep and ep != p:
                eltern = str(kopf.get(ep, {}).get('title') or '')
        raus.append(dict(sprache=sprache, pfad=p, rel=rel, innen=innen,
                         adresse=adresse_von(innen, sprache), bereich=oberster,
                         titel=titel, tiefe=len(teile) - (1 if teile[-1] == '_index.md' else 0),
                         eltern=eltern, kopf=k))
    return raus


def adresse_von(innen, sprache):
    rel = innen[:-3]
    if rel.endswith('_index'):
        rel = rel[:-6]
    rel = rel.strip('/')
    vor = '' if sprache == 'de' else '/' + sprache
    return (vor + '/' + rel + '/').replace('//', '/') if rel else (vor + '/')


# ---------------------------------------------------------------------------
# Deutsche Vorlage neben eine Uebersetzung stellen
# ---------------------------------------------------------------------------
def _anker(text):
    """Was in jeder Sprache gleich bleibt: Zahlen, Linkziele, Abkuerzungen."""
    a = set(re.findall(r'\d+(?:[.,]\d+)?', text))
    a |= set(re.findall(r'\]\(([^)\s]+)', text))
    a |= set(re.findall(r'\b[A-Z][A-Z0-9&]{1,}\b', text))
    a |= {'**'} if '**' in text else set()
    return a


def zuordnen(uebersetzung, vorlage):
    """Ordnet Bausteine einer Uebersetzung denen der deutschen Vorlage zu.

    Gibt eine Liste von Paaren (u, v) zurueck; u oder v kann None sein - dann
    fehlt der Baustein auf der einen Seite. Der Typ allein reicht nicht: Fehlt
    auf Deutsch Absatz 3 von 5, stuende sonst Absatz 4 neben dem
    franzoesischen Absatz 3. Deshalb zaehlen zusaetzlich Anker, die in jeder
    Sprache gleich bleiben (Zahlen, Linkziele, Abkuerzungen), und die Laenge.
    Kopffelder werden nach Typ gepaart und stehen immer oben.
    """
    kopf_u = {b['typ']: b for b in uebersetzung if b['typ'] in dict(KOPFFELDER).values()}
    kopf_v = {b['typ']: b for b in vorlage if b['typ'] in dict(KOPFFELDER).values()}
    paare = []
    for _, typ in KOPFFELDER:
        if typ in kopf_u or typ in kopf_v:
            paare.append((kopf_u.get(typ), kopf_v.get(typ)))
    u = [b for b in uebersetzung if b['typ'] not in dict(KOPFFELDER).values()]
    v = [b for b in vorlage if b['typ'] not in dict(KOPFFELDER).values()]

    def punkte(a, b):
        if a['typ'] != b['typ']:
            return -4.0
        s = 3.0
        if a['typ'] == 'ueberschrift' and a['ebene'] != b['ebene']:
            s -= 1.5
        aa, ab = _anker(a['roh']), _anker(b['roh'])
        if aa or ab:
            s += 3.0 * len(aa & ab) / len(aa | ab) - 1.0
        la, lb = max(len(a['roh']), 1), max(len(b['roh']), 1)
        s -= abs(math.log(la / lb))
        if a['typ'] in GESPERRT and a['roh'] == b['roh']:
            s += 4.0
        return s

    luecke = -1.0
    n, m = len(u), len(v)
    tab = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        tab[i][0] = i * luecke
    for j in range(1, m + 1):
        tab[0][j] = j * luecke
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            tab[i][j] = max(tab[i - 1][j - 1] + punkte(u[i - 1], v[j - 1]),
                            tab[i - 1][j] + luecke, tab[i][j - 1] + luecke)
    i, j, rueck = n, m, []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and tab[i][j] == tab[i - 1][j - 1] + punkte(u[i - 1], v[j - 1]):
            rueck.append((u[i - 1], v[j - 1])); i -= 1; j -= 1
        elif i > 0 and tab[i][j] == tab[i - 1][j] + luecke:
            rueck.append((u[i - 1], None)); i -= 1
        else:
            rueck.append((None, v[j - 1])); j -= 1
    return paare + list(reversed(rueck))


# ---------------------------------------------------------------------------
# Aus einer Tabellenzelle wieder Markdown machen
# ---------------------------------------------------------------------------
def zelle_zu_markdown(typ, text, ebene_alt=0):
    """Den Text aus einer Zelle so aufbereiten, wie er in die Datei gehoert.

    - Zeilenenden vereinheitlichen, Leerzeichen am Zeilenende weg.
    - Ueberschrift: Rauten davor, falls jemand sie weggelassen hat (in der
      Tabelle stehen Ueberschriften ohne Rauten). Die Ebene bleibt die alte;
      neue Ueberschriften bekommen ## bzw. ### bei Unterueberschrift.
    - Liste/Zitat in NEUEN Zeilen: jede Zeile bekommt "- " bzw. "> ", wenn
      sie es nicht schon hat.
    """
    t = text.replace('\r\n', '\n').replace('\r', '\n')
    t = '\n'.join(z.rstrip() for z in t.split('\n')).strip('\n')
    if typ in ('ueberschrift', 'unterueberschrift'):
        if not re.match(r'^#{1,6}\s', t):
            stufe = ebene_alt or (3 if typ == 'unterueberschrift' else 2)
            t = '#' * stufe + ' ' + t.lstrip()
        return t.split('\n')[0] + ('\n\n' + '\n'.join(t.split('\n')[1:]).strip() if '\n' in t else '')
    if typ == 'liste':
        return '\n'.join(z if (not z.strip() or re.match(r'^\s*([-*+]|\d+\.)\s', z)) else '- ' + z.lstrip()
                         for z in t.split('\n'))
    if typ == 'zitat':
        return '\n'.join(z if z.startswith('>') else '> ' + z for z in t.split('\n'))
    return t
