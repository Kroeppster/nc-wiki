#!/usr/bin/env python3
"""
================================================================================
PRUEFSTAND FUER DIE TEXTLISTE
================================================================================
    python3 scripts/texte-mappe-pruefen.py

Prueft die beiden Skripte texte-ausgeben.py und texte-einlesen.py in einem
Durchgang: Mappe erzeugen, Formeln nachrechnen, einen Text eintragen,
zurueckschreiben, nachsehen ob er an der richtigen Stelle steht - und die
Datei wieder herstellen.

WARUM DIE FORMELN IN PYTHON NACHGERECHNET WERDEN und nicht in einer echten
Tabellenkalkulation: LibreOffice laesst sich in der Entwicklungsumgebung
dieses Projekts nicht starten ("source file could not be loaded"). Geprueft
wird deshalb das, was wirklich schiefgehen kann - ob die BEREICHE der Formeln
zu den Daten passen. Dass Excel die Formeln versteht, sagt das nicht; benutzt
werden aber nur COUNTIF, COUNTIFS, SUM, LEN, IFERROR und COUNTA, also
Funktionen, die es seit Excel 2007 unveraendert gibt.

DER RUNDLAUF FASST EINE ECHTE DATEI AN und stellt sie danach wieder her. Der
urspruengliche Inhalt wird vorher im Speicher festgehalten und in einem
finally-Block zurueckgeschrieben - auch wenn die Pruefung mittendrin
abbricht.

Gebraucht wird openpyxl (pip install openpyxl).
================================================================================
"""
import os
import re
import subprocess
import sys
import tempfile

try:
    from openpyxl import load_workbook
    from openpyxl.utils import column_index_from_string
except ImportError:
    sys.exit('Fehlendes Paket: openpyxl. Bitte "pip install openpyxl".')

PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJEKT, 'scripts'))
import texte_bausteine as tb

ok = fehlt = 0


def pruef(name, bedingung, hinweis=''):
    global ok, fehlt
    if bedingung:
        ok += 1
        print('  OK    ' + name)
    else:
        fehlt += 1
        print('  FEHLT ' + name + ('  ' + str(hinweis) if hinweis else ''))


def spalte(blatt, buchstabe, von, bis):
    i = column_index_from_string(buchstabe)
    return [blatt.cell(row=r, column=i).value for r in range(von, bis + 1)]


def zerlegung_pruefen():
    """Die Zeichenpositionen muessen aufs Zeichen stimmen - sonst landet ein
    geschriebener Text an der falschen Stelle."""
    print('=== Zerlegung in Bausteine ===')
    falsch = neu = gesamt = 0
    for s in tb.seiten(PROJEKT):
        roh = open(s['pfad'], encoding='utf-8').read()
        for b in tb.bausteine(s['pfad']):
            gesamt += 1
            if b['von'] == b['bis']:
                neu += 1
                continue
            if roh[b['von']:b['bis']] != b['roh']:
                falsch += 1
    pruef(f'{gesamt} Bausteine, alle Positionen zeichengenau', falsch == 0, f'{falsch} falsch')
    pruef(f'{neu} Stellen zum Einfuegen erkannt (fehlende Beschreibungen)', neu > 0)


def formeln_pruefen(pfad):
    print('\n=== Formeln ===')
    m = load_workbook(pfad)
    T, S, U = m['Texte'], m['Seiten'], m['Uebersicht']
    letzte_t, letzte_s = T.max_row, S.max_row
    sprachen = spalte(T, 'B', 2, letzte_t)
    status = spalte(T, 'K', 2, letzte_t)
    dateien = spalte(T, 'N', 2, letzte_t)

    fehler = []
    for r in (2, letzte_t // 2, letzte_t):
        f = T.cell(row=r, column=8).value or ''
        m2 = re.search(r'LEN\(I(\d+)\)', f)
        if not m2 or int(m2.group(1)) != r:
            fehler.append(f'Zeichen-Formel Zeile {r}')
    pruef('Zeichenzahl zeigt je Zeile auf die eigene Zeile', not fehler, fehler)

    fehler = []
    for r in (2, letzte_s // 2, letzte_s):
        f = S.cell(row=r, column=6).value or ''
        if re.search(r'Texte!\$N\$2:\$N\$(\d+)', f).group(1) != str(letzte_t):
            fehler.append(f'Dateibereich Zeile {r}')
        if re.search(r'Texte!\$K\$2:\$K\$(\d+)', f).group(1) != str(letzte_t):
            fehler.append(f'Statusbereich Zeile {r}')
        if re.search(r',\$K(\d+),', f).group(1) != str(r):
            fehler.append(f'Kriterium Zeile {r}')
    pruef('"davon fertig" zaehlt ueber alle Textzeilen der eigenen Datei', not fehler, fehler)

    fehler = []
    for r, sp in ((5, 'de'), (6, 'fr'), (7, 'it')):
        f = U.cell(row=r, column=3).value or ''
        gesucht = re.search(r'"(\w+)"\)', f)
        if not gesucht or gesucht.group(1) != sp:
            fehler.append(f'Sprache {sp}')
        if re.search(r'\$B\$2:\$B\$(\d+)', f).group(1) != str(letzte_t):
            fehler.append(f'Bereich {sp}')
    pruef('Uebersicht zaehlt je Sprache ueber alle Textzeilen', not fehler, fehler)
    pruef('Summe der drei Sprachen ergibt alle Bausteine',
          len(sprachen) == sum(sprachen.count(x) for x in ('de', 'fr', 'it')))
    platz = next((U.cell(row=r, column=3).value for r in range(9, 18)
                  if 'Platzhalter' in str(U.cell(row=r, column=3).value)), None)
    pruef('Platzhalter werden gezaehlt', platz is not None)
    pruef('Kein leerer Dateiname in der versteckten Spalte', all(dateien))
    pruef('Keine leere Pruefsumme', all(x is not None for x in spalte(T, 'P', 2, letzte_t)))
    return m, letzte_t


def rundlauf_pruefen(mappe_pfad):
    """Text eintragen, zurueckschreiben, nachsehen - und wieder herstellen."""
    print('\n=== Rundlauf (Datei wird angefasst und wieder hergestellt) ===')
    m = load_workbook(mappe_pfad)
    T = m['Texte']
    kopf = [z.value for z in T[1]]
    sp = {n: kopf.index(n) + 1 for n in ('Typ', 'Text neu', 'Datei', 'Baustein')}
    ziel = zeile_nr = baustein_nr = None
    for r in range(2, T.max_row + 1):
        if T.cell(row=r, column=sp['Typ']).value == 'Absatz':
            ziel = T.cell(row=r, column=sp['Datei']).value
            baustein_nr = int(T.cell(row=r, column=sp['Baustein']).value)
            zeile_nr = r
            break
    probetext = 'PRUEFTEXT aus scripts/texte-mappe-pruefen.py'
    T.cell(row=zeile_nr, column=sp['Text neu'], value=probetext)
    gefuellt = mappe_pfad.replace('.xlsx', '-gefuellt.xlsx')
    m.save(gefuellt)

    pfad = os.path.join(PROJEKT, ziel)
    vorher = open(pfad, 'rb').read()
    try:
        r = subprocess.run([sys.executable, os.path.join(PROJEKT, 'scripts/texte-einlesen.py'),
                            gefuellt], capture_output=True, text=True)
        pruef('Einlesen laeuft durch', r.returncode == 0, r.stderr[-200:])
        nachher = open(pfad, encoding='utf-8').read()
        pruef(f'Text steht jetzt in {ziel}', probetext in nachher)
        # ALLE ANDEREN BAUSTEINE MUESSEN UNVERAENDERT SEIN. Eine Pruefung, die
        # nur nachsieht, ob der neue Text irgendwo auftaucht, wuerde nicht
        # merken, dass daneben etwas zerschossen wurde.
        alt_b = [b['roh'] for b in tb.bausteine_aus_text(vorher.decode('utf-8'))]
        neu_b = [b['roh'] for b in tb.bausteine(pfad)]
        abweichend = [i for i, (a, n) in enumerate(zip(alt_b, neu_b)) if a != n]
        pruef('Genau ein Baustein veraendert, alle anderen unberuehrt',
              abweichend == [baustein_nr] and len(alt_b) == len(neu_b),
              f'veraendert: {abweichend}, erwartet: [{baustein_nr}]')
        # Zweiter Lauf mit derselben Mappe: Die Pruefsumme passt nun nicht mehr,
        # die Zeile MUSS uebersprungen werden - sonst wuerde ein Text doppelt
        # oder an der falschen Stelle landen.
        r2 = subprocess.run([sys.executable, os.path.join(PROJEKT, 'scripts/texte-einlesen.py'),
                             gefuellt], capture_output=True, text=True)
        pruef('Zweiter Lauf erkennt die geaenderte Datei und ueberspringt',
              'uebersprungen' in r2.stdout, r2.stdout[-160:])
    finally:
        with open(pfad, 'wb') as f:
            f.write(vorher)
        os.remove(gefuellt)
    pruef('Datei wieder im Ausgangszustand', open(pfad, 'rb').read() == vorher)


def main():
    ordner = tempfile.mkdtemp()
    mappe = os.path.join(ordner, 'probe.xlsx')
    r = subprocess.run([sys.executable, os.path.join(PROJEKT, 'scripts/texte-ausgeben.py'), mappe],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit('Die Mappe liess sich nicht erzeugen:\n' + r.stderr)
    print(r.stdout.strip() + '\n')
    zerlegung_pruefen()
    formeln_pruefen(mappe)
    rundlauf_pruefen(mappe)
    print(f'\n==== {ok} bestanden, {fehlt} nicht ====')
    sys.exit(1 if fehlt else 0)


if __name__ == '__main__':
    main()
