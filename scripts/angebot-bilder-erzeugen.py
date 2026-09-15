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
# Je Untertest: Datei, Seite (ab 0), wo der Ausschnitt beginnt (Anteil der
# Seitenhoehe), wie hoch er ist (Anteil der Seitenhoehe) und wie breit
# (Anteil der Seitenbreite; None = aus der Hoehe gerechnet, also nah heran).
#
# NAH ODER WEIT - das ist die eigentliche Entscheidung hier: Bei den
# grafischen Untertests wird HERANGEZOOMT, damit im fingernagelgrossen Feld
# der Collage noch ein Muster, ein Koerper oder eine Figur zu erkennen ist.
# Bei den textlastigen (Med-nat, Textverstaendnis) wird dagegen die volle
# Spaltenbreite genommen: Zoomt man dort heran, stehen angeschnittene Woerter
# im Bild, und das sieht nach Fehler aus statt nach Aufgabe.
SERIEN = [
    ('ut1-muster',      'muster-zuordnen',           '2026_muster-zuordnen_S04.pdf',           0, 0.115, 0.145, None),
    ('ut2-mednat',      'med-nat-grundverstaendnis', '2026_med-nat-grundverstaendnis_S02.pdf', 0, 0.115, None,  0.92),
    ('ut3-objekte',     'objekte-im-raum',           '2026_objekte-im-raum_S06.pdf',           0, 0.140, 0.185, None),
    ('ut4-quantitativ', 'quantitative-probleme',     '2026_quantitative-probleme_S03.pdf',     2, 0.125, None,  0.80),
    ('ut5-figuren',     'figuren-fakten-lernen',     '2026_figuren-einpraegen_S04.pdf',        1, 0.145, 0.165, None),
    ('ut6-text',        'textverstaendnis',          '2026_textverstaendnis_S03.pdf',          0, 0.165, None,  0.92),
    ('ut7-diagramme',   'diagramme-tabellen',        '2026_diagramme-tabellen_S03.pdf',        3, 0.105, 0.210, None),
    ('ut8-konztest',    'konzentriertes-arbeiten',   '2025_konzentriertes-arbeiten_S19.pdf',   0, 0.235, 0.135, None),
]

# Ganze Seiten (kein Ausschnitt). Das Kursskript steht hier NICHT mehr: Fuer
# die Kurs-Kachel wird das Foto aus assets/images/vorbereitungskurse/
# verwendet - die gedruckten Skripte auf den Hoersaalpulten zeigen mehr vom
# Kurs als die Titelseite der PDF-Datei.
SEITEN = [
    ('testheft', 'assets/downloads/testsimulationen/2026_testsimulationen_Testsimulation.pdf', 2),
]


def ausschnitt(name, ordner, datei, seite_nr, oben, hoehe, breite_anteil):
    pfad = os.path.join(UEBUNGEN, ordner, datei)
    if not os.path.exists(pfad):
        print('  FEHLT, übersprungen: %s' % pfad)
        return
    dok = pymupdf.open(pfad)
    seite = dok[min(seite_nr, dok.page_count - 1)]
    r = seite.rect
    if breite_anteil:                      # weit: volle Spaltenbreite
        breite = r.width * breite_anteil
        hoehe_pt = breite / VERHAELTNIS
    else:                                  # nah: aus der gewünschten Höhe
        hoehe_pt = r.height * hoehe
        breite = hoehe_pt * VERHAELTNIS
    x0 = max(0.0, (r.width - breite) / 2)
    clip = pymupdf.Rect(x0, r.height * oben,
                        min(r.width, x0 + breite), r.height * oben + hoehe_pt)
    # Nahe Ausschnitte brauchen mehr Auflösung, sonst sind sie unscharf: Die
    # Vorlage zeigt sie 420px breit (siehe material-grid.html), darunter darf
    # die Quelldatei nicht liegen.
    pix = seite.get_pixmap(dpi=230 if not breite_anteil else 150, clip=clip)
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
