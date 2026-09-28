#!/usr/bin/env python3
"""
================================================================================
UNIGUIDE-BLATT: DIE GANZE UNI-TABELLE IN DER TEXTMAPPE
================================================================================
Wird ueber scripts/texte_ansicht.py von texte-ausgeben.py (Blatt erzeugen) und
texte-einlesen.py (Blatt einlesen) benutzt.

Die Angaben zu den Universitaeten stehen nicht im Seitentext, sondern in
data/unis.yaml. Dieses Blatt zeigt sie als Tabelle: je Universitaet eine
Zeile, je Angabe eine Spalte - dieselben Angaben wie in der Tabelle und auf
den Uni-Seiten der Website.

SPRACHE: Texte (Kanton, Zulassungsverfahren, Besonderheiten, Anmeldefrist,
Studienbeginn, Semestergebuehr) stehen in data/unis.yaml je Sprache
({de: …, fr: …, it: …}) und werden in der Mappe DIESER Sprache bearbeitet.
Alles andere (Name, Sprachen, Studiengaenge, EMS, Studienplaetze, Links,
Stand, Quelle) gilt fuer alle Sprachen und laesst sich in jeder Mappe aendern.

EINLESEN: Wie bei den anderen Ansichtsblaettern wird nur geschrieben, was sich
geaendert hat - und in data/unis.yaml nur genau dieses Feld dieser Uni. Die
Kommentare in der Datei bleiben stehen. Leere Zelle loescht nichts, !Löschen!
leert das Feld. Stand ein Feld inzwischen anderswo anders, wird es
uebersprungen und gemeldet.
================================================================================
"""
import datetime
import json
import os
import re

import texte_bausteine as tb

try:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
    from openpyxl.comments import Comment
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:      # das melden die aufrufenden Skripte
    pass

UNIS = 'data/unis.yaml'
LOESCHEN = re.compile(r'!\s*(l(ö|oe)schen|supprimer|eliminare)\s*!', re.IGNORECASE)
SCHRIFT = 'Arial'
PAPIER, NAVY, GRAU, LINIE, WEISS = 'F5F7FB', '101A33', '636D88', 'DDE2EC', 'FFFFFF'

# Spalten: (Feld, Breite in Zeichen). Reihenfolge wie auf der Uni-Seite.
SPALTEN = [('name', 24), ('kanton', 14), ('sprache', 16), ('studiengaenge', 15), ('ems_erforderlich', 11),
           ('auswahlverfahren', 46), ('besonderheiten', 46), ('studienplaetze', 11), ('anmeldefrist', 16),
           ('studienbeginn', 16), ('semestergebuehr', 18), ('website', 26), ('website_medizin', 26),
           ('stand', 12), ('quelle', 30)]
SPRACHFELDER = ('kanton', 'auswahlverfahren', 'besonderheiten', 'anmeldefrist', 'studienbeginn', 'semestergebuehr')
LISTEN = ('sprache', 'studiengaenge', 'besonderheiten')
EMS = ('ja', 'nein', 'teilweise')
# Namen der Unterrichtssprachen, wie man sie auch schreiben koennte -> Wert in data/unis.yaml
SPRACHNAMEN = {}
for schluessel, namen in {'Deutsch': ('deutsch', 'allemand', 'tedesco', 'german'),
                          'Français': ('français', 'francais', 'französisch', 'franzoesisch', 'francese', 'french'),
                          'Italiano': ('italiano', 'italienisch', 'italien', 'italian')}.items():
    for n in namen + (schluessel.lower(),):
        SPRACHNAMEN[n] = schluessel

T = {
    'de': dict(
        hinweis='Je Universität eine Zeile – dieselben Angaben wie in der Tabelle und auf den Uni-Seiten. '
        'Nur in die weissen Felder schreiben. Spalten mit grünem Kopf sind Texte und gelten nur für '
        'diese Sprache, alles andere für alle Sprachen. Nur eintragen, was auf einer offiziellen Seite steht, '
        'und dann „Stand“ und „Quelle“ mitändern. Leere Zelle löscht nichts, !Löschen! leert das Feld. '
        'Mehrere Besonderheiten: je eine pro Zeile (Alt+Enter).',
        felder=dict(name='Name', kanton='Kanton', sprache='Sprachen', studiengaenge='Studiengänge',
                    ems_erforderlich='EMS nötig', auswahlverfahren='Zulassungsverfahren',
                    besonderheiten='Besonderheiten', studienplaetze='Studienplätze', anmeldefrist='Anmeldefrist',
                    studienbeginn='Studienbeginn', semestergebuehr='Semestergebühr', website='Website',
                    website_medizin='Website Medizin', stand='Stand', quelle='Quelle'),
        hilfe=dict(sprache='Deutsch, Français, Italiano – mit Komma', studiengaenge='z. B. Bachelor, Master',
                   ems_erforderlich='ja / nein / teilweise', studienplaetze='nur die Zahl',
                   stand='Datum der Prüfung, z. B. 2027-01-15'),
        deutsch='Deutsch:'),
    'fr': dict(
        hinweis="Une ligne par université – les mêmes informations que dans le tableau et sur les pages des "
        "universités. N'écris que dans les cases blanches. Les colonnes à en-tête vert sont des textes "
        "et valent seulement pour cette langue, tout le reste pour toutes les langues. N'inscris que ce qui figure sur une page "
        "officielle, et modifie alors aussi « Stand » et « Quelle ». Une case vide ne supprime rien, !Supprimer! "
        "vide le champ. Plusieurs particularités : une par ligne (Alt+Entrée).",
        felder=dict(name='Nom', kanton='Canton', sprache='Langues', studiengaenge='Filières',
                    ems_erforderlich='EMS requis', auswahlverfahren='Procédure de sélection',
                    besonderheiten='Particularités', studienplaetze="Places d'étude", anmeldefrist="Délai d'inscription",
                    studienbeginn='Début des études', semestergebuehr='Taxe semestrielle', website='Site web',
                    website_medizin='Site médecine', stand='Stand (vérifié le)', quelle='Quelle (source)'),
        hilfe=dict(sprache='Deutsch, Français, Italiano – séparées par des virgules',
                   studiengaenge='p. ex. Bachelor, Master', ems_erforderlich='ja / nein / teilweise (oui/non/partiel)',
                   studienplaetze='seulement le nombre', stand='date de vérification, p. ex. 2027-01-15'),
        deutsch='Allemand :'),
    'it': dict(
        hinweis="Una riga per università – le stesse informazioni della tabella e delle pagine delle università. "
        "Scrivi solo nelle caselle bianche. Le colonne con intestazione verde sono testi "
        "e valgono solo per questa lingua, tutto il resto per tutte le lingue. Inserisci solo ciò che figura su una pagina "
        "ufficiale, e modifica allora anche «Stand» e «Quelle». Una casella vuota non elimina nulla, !Eliminare! "
        "svuota il campo. Più particolarità: una per riga (Alt+Invio).",
        felder=dict(name='Nome', kanton='Cantone', sprache='Lingue', studiengaenge='Corsi di laurea',
                    ems_erforderlich='EMS richiesto', auswahlverfahren='Procedura di selezione',
                    besonderheiten='Particolarità', studienplaetze='Posti di studio',
                    anmeldefrist="Termine d'iscrizione", studienbeginn='Inizio degli studi',
                    semestergebuehr='Tassa semestrale', website='Sito web', website_medizin='Sito medicina',
                    stand='Stand (verificato il)', quelle='Quelle (fonte)'),
        hilfe=dict(sprache='Deutsch, Français, Italiano – separate da virgole',
                   studiengaenge='p. es. Bachelor, Master', ems_erforderlich='ja / nein / teilweise (sì/no/in parte)',
                   studienplaetze='solo il numero', stand='data della verifica, p. es. 2027-01-15'),
        deutsch='Tedesco:'),
}


# ---------------------------------------------------------------------------
# Werte <-> Zellen
# ---------------------------------------------------------------------------
def _sprachwert(w, sprache):
    """Wert eines Sprachfelds fuer eine Sprache (ohne Rueckfall)."""
    if isinstance(w, dict):
        return w.get(sprache)
    return w if sprache == 'de' else None


def anzeige(uni, feld, sprache):
    """So steht ein Feld in der Zelle."""
    w = uni.get(feld)
    if feld in SPRACHFELDER:
        w = _sprachwert(w, sprache)
    if w is None:
        return ''
    if isinstance(w, list):
        return ('\n' if feld == 'besonderheiten' else ', ').join(str(x) for x in w)
    return str(w)


def zelle_lesen(v):
    """Zelleninhalt als Text - auch wenn Excel eine Zahl oder ein Datum daraus gemacht hat."""
    if v is None:
        return ''
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime('%Y-%m-%d')
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    s = str(v).replace('\r\n', '\n').strip()
    return re.sub(r'^(\d{4}-\d{2}-\d{2}) 00:00:00$', r'\1', s)


def auswerten(feld, text):
    """Zelle -> Wert fuer data/unis.yaml. ValueError mit Begruendung, wenn es nicht passt."""
    if feld == 'studienplaetze':
        t = text.replace("'", '').replace('’', '').replace(' ', '')
        if not t.isdigit():
            raise ValueError(f'„{text}“ ist keine Zahl')
        return int(t)
    if feld == 'ems_erforderlich':
        t = text.strip().lower()
        t = {'oui': 'ja', 'sì': 'ja', 'si': 'ja', 'non': 'nein', 'no': 'nein', 'partiel': 'teilweise',
             'partiellement': 'teilweise', 'in parte': 'teilweise'}.get(t, t)
        if t not in EMS:
            raise ValueError(f'„{text}“ – erlaubt sind ja, nein, teilweise')
        return t
    if feld == 'sprache':
        werte = []
        for teil in re.split(r'[,;/\n]', text):
            t = teil.strip()
            if not t:
                continue
            if t.lower() not in SPRACHNAMEN:
                raise ValueError(f'„{t}“ – erlaubt sind Deutsch, Français, Italiano')
            werte.append(SPRACHNAMEN[t.lower()])
        return list(dict.fromkeys(werte))
    if feld == 'studiengaenge':
        return [t.strip() for t in re.split(r'[,;\n]', text) if t.strip()]
    if feld == 'besonderheiten':
        return [' '.join(t.split()) for t in text.split('\n') if t.strip()]
    if feld in ('website', 'website_medizin', 'quelle') and not re.match(r'https?://', text.strip()):
        raise ValueError(f'„{text}“ ist kein Link (muss mit https:// beginnen)')
    return ' '.join(text.split())


# ---------------------------------------------------------------------------
# Blatt schreiben
# ---------------------------------------------------------------------------
def _fill(c):
    return PatternFill('solid', fgColor=c)


def _rand():
    s = Side(style='thin', color=LINIE)
    return Border(left=s, right=s, top=s, bottom=s)


def _hoehe(text, breite):
    zeilen = sum(max(1, -(-len(z) // max(breite - 2, 8))) for z in str(text or '').split('\n'))
    return max(18, 13.5 * zeilen + 5)


def unis_laden(projekt):
    import yaml
    with open(os.path.join(projekt, UNIS), encoding='utf-8') as f:
        return yaml.safe_load(f) or []


def blatt(ws, sprache, projekt, merker):
    L = T[sprache]
    unis = unis_laden(projekt)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 12
    for i, (feld, breite) in enumerate(SPALTEN):
        ws.column_dimensions[chr(ord('B') + i)].width = breite
    letzte = len(SPALTEN) + 1
    for r in range(1, 5):
        for c in range(1, letzte + 1):
            ws.cell(row=r, column=c).fill = _fill(PAPIER)
    c = ws.cell(row=1, column=2, value=ws.title)
    c.font = Font(name=SCHRIFT, size=16, bold=True, color=NAVY)
    ws.row_dimensions[1].height = 26
    c = ws.cell(row=2, column=2, value=L['hinweis'])
    c.font = Font(name=SCHRIFT, size=9, italic=True, color=GRAU)
    c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=2, start_column=2, end_row=2, end_column=9)
    ws.row_dimensions[2].height = 58
    # Kopfzeile: Feldname, darunter klein die Eingabehilfe
    for i, (feld, breite) in enumerate(SPALTEN):
        text = L['felder'][feld] + (f'\n{L["hilfe"][feld]}' if feld in L['hilfe'] else '')
        c = ws.cell(row=4, column=2 + i, value=text)
        c.font = Font(name=SCHRIFT, size=9, bold=True, color=WEISS)
        c.fill = _fill('1C6B3F' if feld in SPRACHFELDER else NAVY)
        c.alignment = Alignment(wrap_text=True, vertical='top')
        c.border = _rand()
    c = ws.cell(row=4, column=1, value='slug')
    c.font = Font(name=SCHRIFT, size=8, color=GRAU)
    ws.row_dimensions[4].height = 40
    ems = DataValidation(type='list', formula1='"ja,nein,teilweise"', allow_blank=True)
    ws.add_data_validation(ems)
    r = 5
    for uni in unis:
        slug = uni.get('slug')
        c = ws.cell(row=r, column=1, value=slug)
        c.font = Font(name=SCHRIFT, size=8, color=GRAU)
        c.alignment = Alignment(vertical='top')
        hoehe = 18
        for i, (feld, breite) in enumerate(SPALTEN):
            wert = anzeige(uni, feld, sprache)
            c = ws.cell(row=r, column=2 + i, value=wert)
            c.font = Font(name=SCHRIFT, size=10, bold=feld == 'name', color=NAVY if feld == 'name' else '3A4460')
            c.fill = _fill(WEISS)
            c.border = _rand()
            c.alignment = Alignment(wrap_text=True, vertical='top')
            c.protection = Protection(locked=False)
            c.number_format = '@'
            if feld == 'ems_erforderlich':
                ems.add(c.coordinate)
            if feld in SPRACHFELDER and sprache != 'de':
                de = anzeige(uni, feld, 'de')
                if de and de != wert:
                    c.comment = Comment(f'{L["deutsch"]} {de}', 'NCWiki')
            pfad = [slug, feld, sprache if feld in SPRACHFELDER else None]
            merker.append(['uni', ws.title, c.coordinate, UNIS, json.dumps(pfad, ensure_ascii=False), wert])
            hoehe = max(hoehe, _hoehe(wert, breite))
        ws.row_dimensions[r].height = min(hoehe, 300)
        r += 1
    ws.freeze_panes = 'C5'
    ws.protection.sheet = True
    ws.protection.formatColumns = False
    ws.protection.formatRows = False


# ---------------------------------------------------------------------------
# data/unis.yaml gezielt aendern (Kommentare bleiben)
# ---------------------------------------------------------------------------
def _yaml_wert(w):
    if w is None:
        return 'null'
    if isinstance(w, bool):
        return 'true' if w else 'false'
    if isinstance(w, int):
        return str(w)
    return json.dumps(w, ensure_ascii=False)     # JSON-Text und -Listen sind gueltiges YAML


def _feld_text(feld, w):
    if isinstance(w, dict):
        return f'  {feld}:\n' + ''.join(f'    {k}: {_yaml_wert(w[k])}\n' for k in w)
    return f'  {feld}: {_yaml_wert(w)}\n'


def feld_ersetzen(text, slug, feld, wert):
    """Ersetzt in data/unis.yaml genau das Feld einer Uni (samt eingerueckten
    Folgezeilen). Fehlt es, kommt es ans Ende des Eintrags."""
    anfang = re.search(r'^- slug: ["\']?%s["\']?[ \t]*$' % re.escape(slug), text, re.M)
    if not anfang:
        raise KeyError(slug)
    ende = re.compile(r'^- ', re.M).search(text, anfang.end())
    ende = ende.start() if ende else len(text)
    block = text[anfang.start():ende]
    m = re.search(r'^  %s:[^\n]*\n(?:    [^\n]*\n)*' % re.escape(feld), block, re.M)
    neu = _feld_text(feld, wert)
    if m:
        block = block[:m.start()] + neu + block[m.end():]
    else:
        rest = block.rstrip('\n')
        block = rest + '\n' + neu + block[len(rest) + 1:]
    return text[:anfang.start()] + block + text[ende:]


def anwenden(projekt, eintraege, melde, probe=False):
    """Aenderungen aus dem Uniguide-Blatt in data/unis.yaml. Gibt die Zahl der
    geaenderten Felder zurueck."""
    import yaml
    pfad = os.path.join(projekt, UNIS)
    with open(pfad, encoding='utf-8') as f:
        roh = f.read()
    unis = {u.get('slug'): u for u in (yaml.safe_load(roh) or [])}
    text, zaehler = roh, 0
    for art, p, original, wert, wo in eintraege:
        if art != 'uni':
            continue
        slug, feld, sprache = p
        wert, original = zelle_lesen(wert), zelle_lesen(original)
        if wert == original or not wert:            # unveraendert, oder geleert (loescht nichts)
            continue
        uni = unis.get(slug)
        if uni is None:
            melde(f'{wo}: die Universität „{slug}“ gibt es nicht mehr - nicht übernommen.')
            continue
        ist = anzeige(uni, feld, sprache or 'de')
        if ist == wert:
            continue
        if ist != original:
            melde(f'{wo}: wurde inzwischen anderswo geändert („{ist[:40]}“) - übersprungen.')
            continue
        loeschen = bool(LOESCHEN.search(wert))
        try:
            neu = None if loeschen else auswerten(feld, wert)
        except ValueError as e:
            melde(f'{wo}: {e} - nicht übernommen.')
            continue
        if loeschen and feld in LISTEN and feld not in SPRACHFELDER:
            neu = []
        if feld in SPRACHFELDER:
            alt = uni.get(feld)
            d = dict(alt) if isinstance(alt, dict) else ({} if alt in (None, '', []) else {'de': alt})
            if neu in (None, []):
                d.pop(sprache, None)
            else:
                d[sprache] = neu
            neu = {k: d[k] for k in tb.SPRACHEN if d.get(k) not in (None, '', [])}
            if not neu:
                neu = [] if feld == 'besonderheiten' else None
        uni[feld] = neu
        text = feld_ersetzen(text, slug, feld, neu)
        zaehler += 1
    if zaehler:
        # Sicherheitsnetz: Die geaenderte Datei muss genau das ergeben, was gemeint war
        neu_geladen = {u.get('slug'): u for u in (yaml.safe_load(text) or [])}
        if neu_geladen != unis:
            melde(f'{UNIS}: Änderungen ergäben eine andere Datei als beabsichtigt - nichts geschrieben. '
                  'Bitte melden.')
            return 0
        if not probe:
            with open(pfad, 'w', encoding='utf-8') as f:
                f.write(text)
    return zaehler
