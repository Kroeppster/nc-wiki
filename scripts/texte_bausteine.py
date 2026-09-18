#!/usr/bin/env python3
"""
================================================================================
GEMEINSAME TEILE FUER DIE TEXTLISTE
================================================================================
Wird von scripts/texte-ausgeben.py und scripts/texte-einlesen.py benutzt.

WARUM DIESE DATEI EINEN UNTERSTRICH IM NAMEN HAT und nicht wie die anderen
Skripte einen Bindestrich: Python kann eine Datei mit Bindestrich nicht
importieren. Die beiden Skripte drumherum behalten den Bindestrich, weil sie
von Hand aufgerufen werden.

DIE WICHTIGSTE REGEL HIER: Ausgeben und Einlesen muessen eine Seite GENAU
GLEICH in Bausteine zerlegen. Sonst landet ein geschriebener Text an der
falschen Stelle. Deshalb steht die Zerlegung genau einmal hier und nicht
zweimal in den beiden Skripten.

Ein Baustein merkt sich seine Zeichenposition in der Datei. Beim Einlesen wird
die Datei neu zerlegt und der neue Text an genau dieser Stelle eingesetzt -
so bleibt alles andere in der Datei unangetastet, auch Einrueckungen,
Shortcodes und Zeilenumbrueche, die niemand angefasst hat.
================================================================================
"""
import os
import re
import hashlib

SPRACHEN = ('de', 'fr', 'it')

# Bausteine, die bearbeitet werden duerfen. Tabellen, HTML und reine
# Shortcode-Zeilen stehen zwar in der Liste, sind aber gesperrt: Wer dort ein
# Zeichen verschiebt, macht die Seite kaputt, und dafuer ist eine
# Redaktionstabelle das falsche Werkzeug.
BEARBEITBAR = ('Titel', 'Beschreibung', 'Ueberschrift', 'Absatz', 'Liste', 'Zitat')


def pruefsumme(text):
    """Kurze Pruefsumme eines Bausteins - erkennt beim Einlesen, ob sich die
    Datei seit dem Ausgeben geaendert hat."""
    return hashlib.sha1(text.encode('utf-8')).hexdigest()[:8]


def frontmatter_trennen(roh):
    """Trennt den Kopf (zwischen den --- Zeilen) vom Text darunter.

    Gibt (kopf_text, koerper_text, koerper_start) zurueck. koerper_start ist
    die Zeichenposition, ab der der Text beginnt - sie wird gebraucht, damit
    die Positionen der Bausteine auf die ganze Datei passen.
    """
    if not roh.startswith('---'):
        return '', roh, 0
    ende = roh.find('\n---', 3)
    if ende < 0:
        return '', roh, 0
    zeilenende = roh.find('\n', ende + 1)
    if zeilenende < 0:
        return roh[3:ende], '', len(roh)
    return roh[3:ende], roh[zeilenende + 1:], zeilenende + 1


def kopf_feld(kopf, feld):
    """Liest ein einfaches Feld aus dem Kopf, z.B. title.

    Bewusst ohne YAML-Bibliothek: Gebraucht werden nur zwei einzeilige Felder,
    und der Wert soll ZEICHENGENAU zurueckgeschrieben werden koennen - eine
    YAML-Bibliothek formatiert beim Schreiben die ganze Datei neu.

    Gibt (anzeigewert, rohwert, von, bis) zurueck. ANZEIGEWERT und ROHWERT
    sind nicht dasselbe: In der Datei steht title: "EMS" mit
    Anfuehrungszeichen, in der Tabelle soll EMS stehen. Zum Pruefen und
    Ersetzen zaehlt der Rohwert samt Anfuehrungszeichen - sonst landet der
    neue Text zwei Zeichen daneben.
    """
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(feld), kopf, re.MULTILINE)
    if not m:
        return None, None, None, None
    roh = m.group(1).rstrip()
    wert = roh
    if len(wert) >= 2 and wert[0] == wert[-1] and wert[0] in '"\'':
        wert = wert[1:-1]
    anfang = 3 + m.start(1)            # der Kopf beginnt in der Datei bei 3
    return wert, roh, anfang, anfang + len(roh)


def bausteine(pfad):
    """Zerlegt eine Seite in Bausteine. Siehe bausteine_aus_text().

    Jeder Baustein ist ein dict mit:
      nr        laufende Nummer in der Datei
      typ       Titel, Beschreibung, Ueberschrift, Absatz, Liste, Zitat,
                Tabelle, HTML, Shortcode, Code
      text      der Text, wie er in der Datei steht
      abschnitt die naechste Ueberschrift darueber (zur Orientierung)
      von, bis  Zeichenposition in der Datei
      summe     Pruefsumme des Textes
    """
    with open(pfad, encoding='utf-8') as f:
        return bausteine_aus_text(f.read())


def bausteine_aus_text(roh):
    """Dasselbe fuer einen Text, der schon im Speicher liegt.

    Gebraucht vom Pruefstand, der den Zustand VOR einer Aenderung mit dem
    danach vergleicht - die alte Fassung steht dann nicht mehr auf der Platte.

    Jeder Baustein ist ein dict mit:
      nr        laufende Nummer in der Datei
      typ       Titel, Beschreibung, Ueberschrift, Absatz, Liste, Zitat,
                Tabelle, HTML, Shortcode, Code
      text      der Text zum Anzeigen und Bearbeiten
      roh       der Text, wie er wirklich in der Datei steht (beim Titel samt
                Anfuehrungszeichen) - danach richten sich Pruefsumme und
                Position
      abschnitt die naechste Ueberschrift darueber (zur Orientierung)
      von, bis  Zeichenposition in der Datei
      summe     Pruefsumme des Rohtextes
    """
    kopf, koerper, versatz = frontmatter_trennen(roh)
    raus = []

    def anhaengen(typ, text, abschnitt, von, bis, roh_text=None):
        if roh_text is None:
            roh_text = text
        raus.append(dict(nr=len(raus), typ=typ, text=text, roh=roh_text,
                         abschnitt=abschnitt, von=von, bis=bis,
                         summe=pruefsumme(roh_text)))

    # 1. Kopf: Titel und Beschreibung sind Text, den jemand schreibt.
    titel_wert, titel_roh, titel_von, titel_bis = kopf_feld(kopf, 'title')
    if titel_wert is not None:
        anhaengen('Titel', titel_wert, '(Seitenkopf)', titel_von, titel_bis, titel_roh)
    besch_wert, besch_roh, besch_von, besch_bis = kopf_feld(kopf, 'description')
    if besch_wert is not None:
        anhaengen('Beschreibung', besch_wert, '(Seitenkopf)', besch_von, besch_bis, besch_roh)
    elif titel_wert is not None:
        # NOCH KEINE BESCHREIBUNG: trotzdem eine Zeile anbieten. Von 241 Seiten
        # haben nur 6 eine - das ist die groesste Luecke fuer Suchmaschinen,
        # und in einer Textliste faellt sie auf, wenn die Zeile leer dasteht.
        # von == bis heisst: neu einfuegen statt ersetzen (siehe einsetzen()).
        zeilenende = roh.find('\n', titel_bis)
        stelle = zeilenende + 1 if zeilenende >= 0 else titel_bis
        anhaengen('Beschreibung', '', '(Seitenkopf)', stelle, stelle, '')

    # 2. Koerper: an Leerzeilen trennen. Ein Codeblock mit ``` bleibt am
    #    Stueck, sonst zerfaellt er in Bruchstuecke.
    abschnitt = ''
    pos = 0
    in_code = False
    stueck_start = None
    zeilen = koerper.split('\n')
    puffer = []
    for zeile in zeilen + ['']:
        if zeile.strip().startswith('```'):
            in_code = not in_code
        leer = (zeile.strip() == '') and not in_code
        if leer:
            if puffer:
                text = '\n'.join(puffer).rstrip()
                von = versatz + stueck_start
                typ = einordnen(text)
                if typ == 'Ueberschrift':
                    abschnitt = text.lstrip('#').strip()
                    anhaengen(typ, text, abschnitt, von, von + len(text))
                else:
                    anhaengen(typ, text, abschnitt, von, von + len(text))
                puffer = []
                stueck_start = None
        else:
            if not puffer:
                stueck_start = pos
            puffer.append(zeile)
        pos += len(zeile) + 1
    return raus


def einordnen(text):
    """Was fuer ein Baustein ist das?"""
    erste = text.lstrip().split('\n')[0]
    if erste.startswith('#'):
        return 'Ueberschrift'
    if erste.startswith('```'):
        return 'Code'
    if erste.startswith('>'):
        return 'Zitat'
    if erste.startswith('|'):
        return 'Tabelle'
    if erste.startswith('<'):
        return 'HTML'
    if re.match(r'^\{\{[<%]', erste) and text.strip().endswith(('>}}', '%}}')):
        return 'Shortcode'
    if re.match(r'^([-*+]|\d+\.)\s', erste):
        return 'Liste'
    return 'Absatz'


def seiten(projekt):
    """Alle Inhaltsseiten, nach Sprache und Pfad sortiert."""
    raus = []
    for sprache in SPRACHEN:
        wurzel = os.path.join(projekt, 'content', sprache)
        if not os.path.isdir(wurzel):
            continue
        for ordner, _, dateien in os.walk(wurzel):
            for name in sorted(dateien):
                if not name.endswith('.md'):
                    continue
                pfad = os.path.join(ordner, name)
                raus.append(dict(sprache=sprache, pfad=pfad,
                                 rel=os.path.relpath(pfad, projekt).replace(os.sep, '/'),
                                 adresse=adresse_von(projekt, pfad, sprache),
                                 bereich=bereich_von(projekt, pfad, sprache)))
    return sorted(raus, key=lambda s: (SPRACHEN.index(s['sprache']), s['rel']))


def adresse_von(projekt, pfad, sprache):
    rel = os.path.relpath(pfad, os.path.join(projekt, 'content', sprache)).replace(os.sep, '/')
    rel = rel[:-3]                      # .md weg
    if rel.endswith('_index'):
        rel = rel[:-6]
    rel = rel.strip('/')
    # Deutsch ist die Standardsprache und laeuft ohne Praefix (siehe hugo.toml)
    vor = '' if sprache == 'de' else '/' + sprache
    return (vor + '/' + rel + '/').replace('//', '/') if rel else (vor + '/' or '/')


def bereich_von(projekt, pfad, sprache):
    rel = os.path.relpath(pfad, os.path.join(projekt, 'content', sprache)).replace(os.sep, '/')
    teile = rel.split('/')
    if len(teile) == 1:
        return 'Startseite' if teile[0] == '_index.md' else 'Einzelseite'
    return teile[0]
