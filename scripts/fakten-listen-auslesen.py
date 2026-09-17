#!/usr/bin/env python3
"""
================================================================================
WORTLISTEN FÜR DEN FAKTEN-GENERATOR AUS DEN EIGENEN PDFs AUSLESEN
================================================================================
Liest die Einprägephasen der eigenen Fakten-Übungsserien und sammelt daraus
Nachnamen, Berufe, Merkmale und Krankheiten. Das Ergebnis ist die Grundlage
von data/fakten-generator.yaml.

    pip install pymupdf
    python3 scripts/fakten-listen-auslesen.py

ACHTUNG, DIE DATEI WIRD NICHT ÜBERSCHRIEBEN. Das Skript gibt die gefundenen
Wörter nur aus. data/fakten-generator.yaml enthält von Hand vergebene
Kategorien (Zahn/Herz/Knochen, Berufsfelder) und Geschlechtsangaben, die ein
Skript nicht erraten kann - die wären sonst weg. Neue Wörter also von Hand in
die passende Kategorie übernehmen.

WARUM DIE DREI SERIEN UNTERSCHIEDLICH GELESEN WERDEN MÜSSEN: Jede ist anders
gesetzt. S02 schreibt "ca. 25", S03 "ca. 25 Jahre", S04 "ca. 20 Jahre," mit
Komma und Zeilenumbruch mitten im Eintrag. Deshalb wird der ganze Text zuerst
zu einer einzigen Zeile normalisiert und dann mit einem Muster gelesen, das
alle drei Schreibweisen abdeckt.
================================================================================
"""
import glob
import re
import sys

try:
    import pymupdf
except ImportError:
    sys.exit('Fehlt: pymupdf. Installieren mit "pip install pymupdf".')

ORDNER = 'assets/downloads/uebungsaufgaben/figuren-fakten-lernen'

MUSTER = re.compile(
    r'([A-ZÄÖÜ][A-Za-zäöüßA-ZÄÖÜ]{2,})\s*:\s*'        # Nachname
    r'ca\.\s*(\d{2})\s*(?:Jahre)?\s*,?\s*'             # Alter
    r'([A-ZÄÖÜ][a-zäöüß/-]+)\s*,\s*'                   # Beruf
    r'([A-Za-zäöüß]+)\s*-\s*'                          # Merkmal
    r'([A-ZÄÖÜ][A-Za-zäöüß0-9-]*(?:\s[a-zäöüß]+)?)'    # Krankheit
)


def main():
    personen = []
    dateien = sorted(glob.glob(f'{ORDNER}/*fakten*Einpraegephase*.pdf'))
    if not dateien:
        sys.exit(f'Keine Einprägephasen gefunden unter {ORDNER}')

    for pfad in dateien:
        dok = pymupdf.open(pfad)
        text = ' '.join(seite.get_text() for seite in dok)
        dok.close()
        text = re.sub(r'\s+', ' ', text).split('Zeit:', 1)[-1]
        treffer = [m.groups() for m in MUSTER.finditer(text)]
        personen += treffer
        print(f'  {pfad.split("/")[-1]}: {len(treffer)} Personen')

    print(f'\n{len(personen)} Personen insgesamt\n')
    for i, feld in enumerate(['NACHNAMEN', 'ALTER', 'BERUFE', 'MERKMALE', 'KRANKHEITEN']):
        woerter = sorted({p[i].strip() for p in personen})
        print(f'{feld} ({len(woerter)}):')
        print('  ' + ', '.join(woerter) + '\n')


if __name__ == '__main__':
    main()
