#!/usr/bin/env python3
"""
================================================================================
LÖSUNGEN DER TESTSIMULATIONEN FÜR «ANTWORTBOGEN AUSWERTEN» AUSLESEN
================================================================================
Liest aus den veröffentlichten Lösungs-PDFs (assets/downloads/testsimulationen/)
die 144 Lösungsbuchstaben je Jahr und schreibt sie nach
data/antwortbogen.yaml. Die Seite «Antwortbogen auswerten» (Alpha) vergleicht
ein Foto des ausgefüllten Antwortbogens damit.

    pip install pymupdf
    python3 scripts/antwortbogen-loesungen.py            # nur prüfen und zeigen
    python3 scripts/antwortbogen-loesungen.py --schreiben

Für eine neue Testsimulation: das Lösungs-PDF wie gewohnt hochladen, unten in
DATEIEN eintragen und das Skript mit --schreiben laufen lassen. Es bricht ab,
wenn nicht genau eine Lösung für jede der 144 Aufgaben gefunden wird - lieber
gar keine Daten als eine verrutschte Lösung.

Gelesen wird «Nummer Buchstabe» (zum Beispiel «27 D»). In den PDFs stehen
dazwischen manchmal unsichtbare Zeichen (U+200B) oder ein Zeilenumbruch; beides
wird übergangen. Alle Lösungs-PDFs von 2022 bis 2026 sind gleich aufgebaut: acht
Untertests zu je 18 Aufgaben, in der Reihenfolge des Antwortbogens.
================================================================================
"""
import os
import re
import sys
from collections import defaultdict

try:
    import pymupdf
except ImportError:
    sys.exit('Fehlt: pymupdf. Installieren mit "pip install pymupdf".')

ORDNER = 'assets/downloads/testsimulationen'
ZIEL = 'data/antwortbogen.yaml'
# Jahr -> Lösungs-PDF. Neueste zuerst; so stehen sie auch in der Auswahl.
DATEIEN = {
    2026: '2026_testsimulationen_Loesung.pdf',
    2025: '2025_testsimulationen_Loesung-Auswertung-Konzentrationstest.pdf',
    2024: '2024_testsimulationen_Loesung.pdf',
    2023: '2023_testsimulationen_Loesung.pdf',
    2022: '2022_testsimulationen_Loesung.pdf',
}
AUFGABEN, BLOCK = 144, 18

KOPF = '''# ============================================================================
# LÖSUNGEN DER TESTSIMULATIONEN - für «Antwortbogen auswerten» (Alpha-Seite)
# ============================================================================
# AUTOMATISCH ERZEUGT von scripts/antwortbogen-loesungen.py aus den
# Lösungs-PDFs unter assets/downloads/testsimulationen/. Nicht von Hand
# ändern - eine falsche Lösung hier zählt bei allen, die ihren Bogen
# auswerten, falsch. Ist ein PDF fehlerhaft, das PDF korrigieren und das
# Skript neu laufen lassen.
#
# Je Testsimulation acht Zeilen zu 18 Buchstaben, eine je Untertest in der
# Reihenfolge des Antwortbogens (siehe "bloecke"). Der Antwortbogen selbst
# ist seit 2022 derselbe (Passermarken, Kästchen), deshalb gilt für alle
# Jahre dieselbe Lage der Kästchen (layouts/partials/bausteine/
# antwortbogen-auswertung.html).
# ============================================================================
bloecke:
  - de: "Muster zuordnen"
    fr: "Reconnaissance de fragments de figure"
    it: "Associare le figure"
  - de: "Med.-nat. Grundverständnis"
    fr: "Compréhension de questions fond. de la médecine et des sc. nat."
    it: "Comprensione di base di questioni medico-scientifiche"
  - de: "Objekte im Raum"
    fr: "Objets dans l'espace"
    it: "Oggetti nello spazio"
  - de: "Quantitative und formale Probleme"
    fr: "Problèmes quantitatifs et formels"
    it: "Problemi quantitativi e formali"
  - de: "Textverständnis"
    fr: "Compréhension de textes"
    it: "Comprensione di testi"
  - de: "Figuren lernen"
    fr: "Apprendre des figures"
    it: "Memorizzazione di figure"
  - de: "Fakten lernen"
    fr: "Apprendre des faits"
    it: "Memorizzazione di fatti"
  - de: "Diagramme und Tabellen"
    fr: "Diagrammes et tableaux"
    it: "Diagrammi e tabelle"
testsimulationen:
'''


def lesen(pfad):
    text = ''.join(seite.get_text() for seite in pymupdf.open(pfad)).replace('​', ' ')
    gefunden = defaultdict(list)
    for nr, buchstabe in re.findall(r'(?<![\d.])(\d{1,3})\s+([A-E])(?![A-Za-z])', text):
        if 1 <= int(nr) <= AUFGABEN:
            gefunden[int(nr)].append(buchstabe)
    falsch = [nr for nr in range(1, AUFGABEN + 1) if len(gefunden[nr]) != 1]
    if falsch:
        sys.exit('%s: keine oder mehrere Lösungen bei Aufgabe %s'
                 % (pfad, ', '.join(map(str, falsch[:10]))))
    return ''.join(gefunden[nr][0] for nr in range(1, AUFGABEN + 1))


def main():
    aus = KOPF
    for jahr, datei in DATEIEN.items():
        loesungen = lesen(os.path.join(ORDNER, datei))
        print(jahr, loesungen)
        aus += '  - jahr: %d\n    quelle: "%s"\n    loesungen:\n' % (jahr, datei)
        for b in range(0, AUFGABEN, BLOCK):
            aus += '      - "%s"\n' % loesungen[b:b + BLOCK]
    if '--schreiben' in sys.argv:
        with open(ZIEL, 'w', encoding='utf-8') as f:
            f.write(aus)
        print('geschrieben:', ZIEL)


if __name__ == '__main__':
    main()
