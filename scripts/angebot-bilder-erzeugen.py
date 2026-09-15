#!/usr/bin/env python3
"""
================================================================================
BILDER FÜR "DAS MATERIAL SELBST" AUF DER STARTSEITE ERZEUGEN
================================================================================
Die Startseite zeigt unter "Alles kostenlos, alles von Studierenden gemacht"
keine Symbolbilder, sondern ECHTE SEITEN aus den PDFs, die hier zum Download
stehen (siehe layouts/partials/material-grid.html). Dieses Skript erzeugt sie.

Von Hand schneiden wäre ein Fehler: Ändert sich das Layout einer Übungsserie
oder kommt ein neuer Jahrgang dazu, müsste jemand daran denken. So läuft
stattdessen das Skript neu.

    pip install pymupdf
    python3 scripts/angebot-bilder-erzeugen.py

Die Bilder landen in assets/images/angebot/ und werden von Hugo beim Bauen auf
die Anzeigegrösse verkleinert - die Quelldateien dürfen also grosszügig sein.

NICHT ENTHALTEN sind drei Bilder der Collage "Orientierung und Austausch":
uniguide.png und berichte.png sind Bildschirmfotos der eigenen Website,
discord.png ist eine selbst gestaltete Karte. Die entstehen mit Playwright;
wie, steht in docs/WARTUNG-DETAILLIERT.md. Aus dem echten Discord-Server gibt
es bewusst KEIN Bild - dort stehen Namen und Nachrichten von Leuten.

DAS SEITENVERHÄLTNIS 1.538:1 ist nicht beliebig: Genau so breit und hoch sind
die acht Felder der Collage (zwei Spalten, vier Zeilen in einer Fläche im
Papierformat). Ein anderes Verhältnis führt dazu, dass die Ausschnitte
beschnitten werden und nur noch Streifen zu sehen sind.
================================================================================
"""
import os
import sys

try:
    import pymupdf
except ImportError:
    sys.exit('Fehlt: pymupdf. Installieren mit "pip install pymupdf".')

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(WURZEL, 'assets/images/angebot')
UEBUNGEN = os.path.join(WURZEL, 'assets/downloads/uebungsaufgaben')
VERHAELTNIS = 1.538

# Je Untertest: welche Datei, welche Seite (ab 0) und wie weit unten der
# Ausschnitt beginnt (Anteil der Seitenhöhe). Die Werte sind so gewählt, dass
# die Aufgaben zu sehen sind und nicht die Kopfzeile.
SERIEN = [
    ('ut1-muster',      'muster-zuordnen',           '2026_muster-zuordnen_S04.pdf',           0, 0.11),
    ('ut2-mednat',      'med-nat-grundverstaendnis', '2026_med-nat-grundverstaendnis_S02.pdf', 0, 0.13),
    ('ut3-objekte',     'objekte-im-raum',           '2026_objekte-im-raum_S06.pdf',           0, 0.13),
    ('ut4-quantitativ', 'quantitative-probleme',     '2026_quantitative-probleme_S03.pdf',     2, 0.12),
    ('ut5-figuren',     'figuren-fakten-lernen',     '2026_figuren-einpraegen_S04.pdf',        1, 0.14),
    ('ut6-text',        'textverstaendnis',          '2026_textverstaendnis_S03.pdf',          0, 0.16),
    ('ut7-diagramme',   'diagramme-tabellen',        '2026_diagramme-tabellen_S03.pdf',        3, 0.10),
    ('ut8-konztest',    'konzentriertes-arbeiten',   '2025_konzentriertes-arbeiten_S19.pdf',   0, 0.22),
]

# Ganze Seiten (kein Ausschnitt): Deckblatt des Testhefts, Titelseite des Skripts
SEITEN = [
    ('testheft',   'assets/downloads/testsimulationen/2026_testsimulationen_Testsimulation.pdf', 2),
    ('kursskript', 'assets/downloads/kursskripte/NCWiki_Kursskript_2026_deutsch.pdf',            0),
]


def ausschnitt(name, ordner, datei, seite_nr, oben):
    pfad = os.path.join(UEBUNGEN, ordner, datei)
    if not os.path.exists(pfad):
        print('  FEHLT, übersprungen: %s' % pfad)
        return
    dok = pymupdf.open(pfad)
    seite = dok[min(seite_nr, dok.page_count - 1)]
    r = seite.rect
    breite = r.width * 0.88
    clip = pymupdf.Rect(r.width * 0.06, r.height * oben,
                        r.width * 0.94, r.height * oben + breite / VERHAELTNIS)
    pix = seite.get_pixmap(dpi=105, clip=clip)
    pix.save(os.path.join(ZIEL, name + '.png'))
    print('  %-16s %-44s %4dx%4d' % (name, datei, pix.width, pix.height))
    dok.close()


def ganze_seite(name, pfad, seite_nr):
    voll = os.path.join(WURZEL, pfad)
    if not os.path.exists(voll):
        print('  FEHLT, übersprungen: %s' % pfad)
        return
    dok = pymupdf.open(voll)
    pix = dok[min(seite_nr, dok.page_count - 1)].get_pixmap(dpi=78)
    pix.save(os.path.join(ZIEL, name + '.png'))
    print('  %-16s %-44s %4dx%4d' % (name, os.path.basename(pfad), pix.width, pix.height))
    dok.close()


def main():
    os.makedirs(ZIEL, exist_ok=True)
    print('Ausschnitte der acht Untertests:')
    for eintrag in SERIEN:
        ausschnitt(*eintrag)
    print('Ganze Seiten:')
    for eintrag in SEITEN:
        ganze_seite(*eintrag)
    print('\nFertig. Die drei Bilder der Collage "Orientierung und Austausch"')
    print('(uniguide, berichte, discord) entstehen separat - siehe Kopf dieser Datei.')


if __name__ == '__main__':
    main()
