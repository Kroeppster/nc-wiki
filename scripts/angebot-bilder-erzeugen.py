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
uniguide.png (vier Zeilen der Vergleichstabelle) und berichte.png (EINE
Erfahrungsbericht-Karte) sind Bildschirmfotos der eigenen Website,
discord.png ist eine gesetzte Einladungskarte in der Schrift der Website.
Die drei entstehen mit Playwright; wie, steht in docs/WARTUNG-DETAILLIERT.md.
Aus dem echten Discord-Server gibt es bewusst KEIN Bild - dort stehen Namen
und Nachrichten von Leuten.

DAS SEITENVERHÄLTNIS 1:1.30 (hochkant) ist nicht beliebig: Genau so sind die
neun Felder der Collage geschnitten (drei Spalten, drei Zeilen in einer Fläche
mit demselben Verhältnis). Ein anderes Verhältnis führt dazu, dass die
Ausschnitte beschnitten werden und Teile davon fehlen.
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
VERHAELTNIS = 1.30      # Hochformat: Hoehe = Breite * 1.30

# Je Untertest: welche Datei, welche Seite (ab 0) und wie weit unten der
# Ausschnitt beginnt (Anteil der Seitenhöhe). Die Werte sind so gewählt, dass
# die Aufgaben zu sehen sind und nicht die Kopfzeile.
# NEUN AUSSCHNITTE IM HOCHFORMAT, drei je Reihe in der Collage: zuerst der
# ANTWORTBOGEN - das Erste, was am Testtag auf dem Pult liegt und für alle,
# die den EMS kennen, sofort wiedererkennbar -, danach die acht Untertests in
# der Reihenfolge des echten Testtags (dieselbe wie in data/testablauf.yaml).
#
# Je Eintrag: Name, Pfad ab dem Projektordner, Seite (ab 0), linker Rand des
# Ausschnitts und sein oberer Rand als Anteil der Seite, und die Höhe des
# Ausschnitts als Anteil der Seitenhöhe. Die Breite wird daraus gerechnet -
# siehe VERHAELTNIS.
TEILE = [
    ('k1-antwortblatt', 'assets/downloads/testsimulationen/2026_testsimulationen_Testsimulation.pdf', 0, 0.05, 0.30, 0.55),
    ('k2-muster',       'assets/downloads/uebungsaufgaben/muster-zuordnen/2026_muster-zuordnen_S04.pdf', 0, 0.06, 0.10, 0.55),
    ('k3-mednat',       'assets/downloads/uebungsaufgaben/med-nat-grundverstaendnis/2026_med-nat-grundverstaendnis_S02.pdf', 0, 0.06, 0.12, 0.55),
    ('k4-objekte',      'assets/downloads/uebungsaufgaben/objekte-im-raum/2026_objekte-im-raum_S06.pdf', 0, 0.06, 0.12, 0.55),
    ('k5-quantitativ',  'assets/downloads/uebungsaufgaben/quantitative-probleme/2026_quantitative-probleme_S03.pdf', 2, 0.10, 0.12, 0.55),
    ('k6-figuren',      'assets/downloads/uebungsaufgaben/figuren-fakten-lernen/2026_figuren-einpraegen_S04.pdf', 1, 0.10, 0.13, 0.55),
    ('k7-text',         'assets/downloads/uebungsaufgaben/textverstaendnis/2026_textverstaendnis_S03.pdf', 0, 0.06, 0.16, 0.55),
    ('k8-diagramme',    'assets/downloads/uebungsaufgaben/diagramme-tabellen/2026_diagramme-tabellen_S03.pdf', 3, 0.10, 0.10, 0.55),
    ('k9-konztest',     'assets/downloads/uebungsaufgaben/konzentriertes-arbeiten/2025_konzentriertes-arbeiten_S19.pdf', 0, 0.06, 0.22, 0.55),
]

# Ganze Seiten (kein Ausschnitt). Das Kursskript steht hier NICHT: Für die
# Kurs-Kachel wird das Foto aus assets/images/vorbereitungskurse/ verwendet -
# die gedruckten Skripte auf den Hörsaalpulten zeigen mehr vom Kurs als die
# Titelseite der PDF-Datei.
SEITEN = [
    ('testheft', 'assets/downloads/testsimulationen/2026_testsimulationen_Testsimulation.pdf', 2),
]


def ausschnitt(name, pfad, seite_nr, links, oben, hoehe):
    voll = os.path.join(WURZEL, pfad)
    if not os.path.exists(voll):
        print('  FEHLT, übersprungen: %s' % pfad)
        return
    dok = pymupdf.open(voll)
    seite = dok[min(seite_nr, dok.page_count - 1)]
    r = seite.rect
    hoehe_pt = r.height * hoehe
    breite = hoehe_pt / VERHAELTNIS
    x0 = min(r.width * links, max(0.0, r.width - breite))
    clip = pymupdf.Rect(x0, r.height * oben, x0 + breite, r.height * oben + hoehe_pt)
    pix = seite.get_pixmap(dpi=150, clip=clip)
    pix.save(os.path.join(ZIEL, name + '.png'))
    print('  %-16s %-46s %4dx%4d' % (name, os.path.basename(pfad), pix.width, pix.height))
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
    print('Neun Ausschnitte (Antwortbogen + acht Untertests):')
    for eintrag in TEILE:
        ausschnitt(*eintrag)
    print('Ganze Seiten:')
    for eintrag in SEITEN:
        ganze_seite(*eintrag)
    print('\nFertig. Die drei Bilder der Collage "Orientierung und Austausch"')
    print('(uniguide, berichte, discord) entstehen separat - siehe Kopf dieser Datei.')


if __name__ == '__main__':
    main()
