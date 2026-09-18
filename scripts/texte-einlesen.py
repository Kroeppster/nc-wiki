#!/usr/bin/env python3
"""
================================================================================
TEXTLISTE ZURUECK IN DIE WEBSITE SCHREIBEN
================================================================================
    python3 scripts/texte-einlesen.py ncwiki-texte.xlsx --probe   # nur zeigen
    python3 scripts/texte-einlesen.py ncwiki-texte.xlsx           # schreiben

Liest die ausgefuellte Mappe aus scripts/texte-ausgeben.py und traegt jeden
Text, der in der Spalte "Text neu" steht, in die passende Markdown-Datei ein.
Zeilen ohne neuen Text bleiben unberuehrt.

WIE DIE STELLE WIEDERGEFUNDEN WIRD: Die Mappe merkt sich je Zeile die Datei,
die Nummer des Bausteins und eine Pruefsumme des alten Textes. Beim Einlesen
wird die Datei NEU zerlegt (mit derselben Funktion wie beim Ausgeben) und die
Pruefsumme verglichen. Stimmt sie nicht, hat jemand die Datei in der
Zwischenzeit geaendert - dann wird diese Zeile NICHT geschrieben, sondern
gemeldet. Lieber eine Meldung als ein Text an der falschen Stelle.

Geschrieben wird von hinten nach vorn, damit die Zeichenpositionen der noch
nicht bearbeiteten Stellen gueltig bleiben.

ZWEI HILFEN, weil sie sonst immer wieder passieren:
  - Eine Ueberschrift ohne ihre Rauten bekommt sie zurueck. Wer "## Angebot"
    zu "Unser Angebot" aendert, meint die Ueberschrift, nicht einen Absatz.
  - Ein Titel oder eine Beschreibung wird in Anfuehrungszeichen gesetzt, wie
    Hugo es im Seitenkopf braucht.

Gebraucht wird openpyxl (pip install openpyxl).
================================================================================
"""
import os
import re
import sys

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit('Fehlendes Paket: openpyxl. Bitte "pip install openpyxl".')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texte_bausteine as tb

PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Die Spalten werden ueber die KOPFZEILE gesucht, nicht ueber ihre Position.
# Sonst schreibt dieses Skript stillschweigend Unsinn, sobald jemand in der
# Mappe eine Spalte einfuegt oder verschiebt.
GEBRAUCHT = ('Typ', 'Text bisher', 'Text neu', 'Datei', 'Baustein', 'Pruefsumme')


def kopfwert(text):
    """Einen Wert fuer den Seitenkopf in Anfuehrungszeichen setzen."""
    return '"%s"' % text.replace('\\', '\\\\').replace('"', '\\"')


def zeilen_lesen(mappe_pfad):
    mappe = load_workbook(mappe_pfad, data_only=True)
    if 'Texte' not in mappe.sheetnames:
        sys.exit(f'{mappe_pfad}: Das Blatt "Texte" fehlt. Ist das die richtige Mappe?')
    blatt = mappe['Texte']
    kopf = [z.value for z in blatt[1]]
    spalte = {}
    for name in GEBRAUCHT:
        if name not in kopf:
            sys.exit(f'{mappe_pfad}: In der Kopfzeile fehlt die Spalte "{name}". '
                     f'Wurde die Mappe mit scripts/texte-ausgeben.py erzeugt?')
        spalte[name] = kopf.index(name)
    raus = []
    for nr, zeile in enumerate(blatt.iter_rows(min_row=2, values_only=True), start=2):
        if len(zeile) <= max(spalte.values()):
            continue
        neu = zeile[spalte['Text neu']]
        if neu is None or not str(neu).strip():
            continue
        raus.append(dict(
            zeile=nr,
            typ=zeile[spalte['Typ']],
            alt=zeile[spalte['Text bisher']] or '',
            neu=str(neu).rstrip(),
            datei=zeile[spalte['Datei']],
            baustein=zeile[spalte['Baustein']],
            summe=zeile[spalte['Pruefsumme']] or '',
        ))
    return raus


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip().split('\n\n')[1])
    mappe_pfad = sys.argv[1]
    probe = '--probe' in sys.argv
    if not os.path.exists(mappe_pfad):
        sys.exit(f'{mappe_pfad} gibt es nicht.')

    zeilen = zeilen_lesen(mappe_pfad)
    if not zeilen:
        print('In der Spalte "Text neu" steht nichts - es gibt nichts einzutragen.')
        return

    nach_datei = {}
    for z in zeilen:
        nach_datei.setdefault(z['datei'], []).append(z)

    geschrieben, uebersprungen, dateien = 0, [], 0
    for rel, liste in sorted(nach_datei.items()):
        pfad = os.path.join(PROJEKT, rel)
        if not os.path.exists(pfad):
            uebersprungen += [(z, 'Datei gibt es nicht mehr') for z in liste]
            continue
        bs = tb.bausteine(pfad)
        aenderungen = []
        for z in liste:
            nr = int(z['baustein'])
            if nr >= len(bs):
                uebersprungen.append((z, 'Baustein gibt es nicht mehr'))
                continue
            b = bs[nr]
            if b['summe'] != z['summe']:
                uebersprungen.append((z, 'Datei wurde inzwischen geaendert'))
                continue
            text = z['neu']
            if b['typ'] == 'Ueberschrift' and not text.lstrip().startswith('#'):
                rauten = re.match(r'^(#+)', b['text'].lstrip()).group(1)
                text = f'{rauten} {text.lstrip()}'
            if b['typ'] in ('Titel', 'Beschreibung'):
                if b['von'] == b['bis']:          # es gibt noch keine Zeile
                    text = f'description: {kopfwert(text)}\n'
                else:
                    text = kopfwert(text)
            aenderungen.append((b['von'], b['bis'], text, z, b))
        if not aenderungen:
            continue
        with open(pfad, encoding='utf-8') as f:
            roh = f.read()
        # VON HINTEN NACH VORN, sonst verschieben die ersten Ersetzungen die
        # Positionen aller folgenden.
        for von, bis, text, z, b in sorted(aenderungen, key=lambda a: -a[0]):
            roh = roh[:von] + text + roh[bis:]
            geschrieben += 1
            kurz = (b['text'] or '(leer)').replace('\n', ' ')[:48]
            neu_kurz = text.replace('\n', ' ')[:48]
            print(f'  {rel}  Baustein {b["nr"]} ({b["typ"]})')
            print(f'      alt: {kurz}')
            print(f'      neu: {neu_kurz}')
        if not probe:
            with open(pfad, 'w', encoding='utf-8') as f:
                f.write(roh)
        dateien += 1

    print()
    if probe:
        print(f'PROBE - nichts geschrieben. {geschrieben} Aenderung(en) in {dateien} Datei(en) waeren faellig.')
    else:
        print(f'{geschrieben} Aenderung(en) in {dateien} Datei(en) geschrieben.')
    if uebersprungen:
        print(f'\n{len(uebersprungen)} Zeile(n) uebersprungen:')
        for z, grund in uebersprungen[:20]:
            print(f'  Zeile {z["zeile"]}: {z["datei"]} Baustein {z["baustein"]} - {grund}')
        if len(uebersprungen) > 20:
            print(f'  ... und {len(uebersprungen) - 20} weitere')
        print('\n  "Datei wurde inzwischen geaendert" heisst: Seit dem Erzeugen der Mappe')
        print('  hat jemand diese Stelle im Repo bearbeitet. Mappe neu erzeugen und die')
        print('  betroffenen Texte dort noch einmal eintragen.')
    if not probe and geschrieben:
        print('\nJetzt pruefen: hugo --minify  (und die Seiten im Browser ansehen)')


if __name__ == '__main__':
    main()
