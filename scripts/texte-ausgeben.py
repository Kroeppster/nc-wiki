#!/usr/bin/env python3
"""
================================================================================
TEXTLISTE ERZEUGEN - alle Seiten in einer Tabelle zum Durchgehen
================================================================================
    python3 scripts/texte-ausgeben.py [datei.xlsx]

Schreibt jede Seite der Website Baustein fuer Baustein in eine Arbeitsmappe:
Titel, Beschreibung, Ueberschriften, Absaetze, Listen. Wer Texte schreibt,
braucht dafuer weder Git noch Markdown zu koennen - nur die Spalte
"Text neu" auszufuellen.

ZURUECK INS REPO geht es mit scripts/texte-einlesen.py. Das ist der Punkt:
Eine Liste, die nur ausgibt, verlagert die Arbeit bloss - hinterher muesste
jemand 1600 Zeilen von Hand abtippen.

DIE MAPPE GEHOERT NICHT INS REPO. Sie ist eine Arbeitsdatei, die sich staendig
aendert; als Binaerdatei in Git gaebe sie bei jeder Aenderung einen Konflikt,
den niemand aufloesen kann. Versioniert sind die beiden Skripte, nicht ihr
Ergebnis (siehe .gitignore).

Gebraucht wird openpyxl (pip install openpyxl).
================================================================================
"""
import os
import re
import sys

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    sys.exit('Fehlendes Paket: openpyxl. Bitte "pip install openpyxl".')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texte_bausteine as tb

PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHRIFT = 'Arial'
KOPF_FUELLUNG = PatternFill('solid', fgColor='1F3864')
EINGABE_FUELLUNG = PatternFill('solid', fgColor='FFF2CC')   # hier wird geschrieben
FEHLT_FUELLUNG = PatternFill('solid', fgColor='FCE4E4')
# Die Stile EINMAL bauen und wiederverwenden. Fuer jede der 27000 Zellen ein
# eigenes Font-Objekt anzulegen macht die Datei gross und traege - LibreOffice
# brauchte damit ueber sechs Minuten, um sie nur durchzurechnen.
NORMAL = Font(name=SCHRIFT, size=9)
GRAU = Font(name=SCHRIFT, size=9, color='909090', italic=True)
OBEN = Alignment(vertical='top')
UMBRUCH = Alignment(wrap_text=True, vertical='top')
# Was jemand selbst setzt, und was das Skript vorbelegt:
STATUS_WERTE = ['zu pruefen', 'in Arbeit', 'fertig', 'passt so']
STATUS_AUTOMATISCH = ['Platzhalter', 'fehlt', 'nicht bearbeiten']

# In diesem Repo sind Platzhalter so markiert (siehe content/de/_index.md).
PLATZHALTER = re.compile(r'platzhalter|lorem ipsum|\bTODO\b|\bTBD\b', re.IGNORECASE)


def kopfzeile(blatt, spalten, zeile=1):
    for i, (titel, breite) in enumerate(spalten, start=1):
        z = blatt.cell(row=zeile, column=i, value=titel)
        z.font = Font(name=SCHRIFT, bold=True, color='FFFFFF', size=10)
        z.fill = KOPF_FUELLUNG
        z.alignment = Alignment(vertical='center', wrap_text=True)
        blatt.column_dimensions[get_column_letter(i)].width = breite
    blatt.row_dimensions[zeile].height = 28
    blatt.freeze_panes = blatt.cell(row=zeile + 1, column=1)


def anleitung(mappe, anzahl_texte, anzahl_seiten, ohne_beschreibung):
    b = mappe.active
    b.title = 'Anleitung'
    b.sheet_view.showGridLines = False
    b.column_dimensions['A'].width = 3
    b.column_dimensions['B'].width = 104

    zeilen = [
        ('titel', 'NCWiki - Texte durchgehen und schreiben'),
        ('leer', ''),
        ('text', f'In dieser Mappe steht der gesamte sichtbare Text der Website: '
                 f'{anzahl_texte} Textbausteine auf {anzahl_seiten} Seiten, in Deutsch, '
                 f'Franzoesisch und Italienisch.'),
        ('leer', ''),
        ('kopf', 'So wird damit gearbeitet'),
        ('text', '1. Im Blatt "Seiten" eine Seite aussuchen und in der Spalte "Zustaendig" '
                 'euren Namen eintragen. So arbeitet niemand doppelt.'),
        ('text', '2. Im Blatt "Texte" nach dieser Seite filtern (Filter in der Kopfzeile).'),
        ('text', '3. Den neuen Text in die GELBE Spalte "Text neu" schreiben. Die Spalte '
                 '"Text bisher" bleibt unveraendert stehen - sie ist der Vergleich.'),
        ('text', '4. "Status" auf "fertig" setzen. Wo der bisherige Text schon gut ist: '
                 '"passt so" und die gelbe Spalte leer lassen.'),
        ('leer', ''),
        ('kopf', 'Was der Status vorher schon sagt'),
        ('text', '"Platzhalter" = hier steht noch gar kein richtiger Text, das ist die '
                 'dringendste Arbeit.  ·  "fehlt" = die Seitenbeschreibung fehlt ganz '
                 '(rote Zeile).  ·  "zu pruefen" = es steht ein Text da, er ist nur noch '
                 'niemandem vorgelegt worden.  ·  "nicht bearbeiten" = Tabelle, HTML oder '
                 'Shortcode, graue Zeile - dort bitte nichts aendern.'),
        ('leer', ''),
        ('kopf', 'Nur die gelben Spalten werden ausgefuellt'),
        ('text', 'Gelb = "Text neu". Dazu Status, Zustaendig und Bemerkung. Alles andere '
                 'bitte stehen lassen: Rechts stehen (ausgeblendet) die Angaben, mit denen '
                 'das Einlesen den Text wiederfindet. Zeilen bitte weder loeschen noch '
                 'neu einfuegen - sortieren und filtern ist dagegen unbedenklich.'),
        ('leer', ''),
        ('kopf', 'Beispiel, wie eine ausgefuellte Zeile aussieht'),
        ('beispiel', ''),
        ('leer', ''),
        ('kopf', 'Was zurueck in die Website kommt'),
        ('text', 'Nur Zeilen, in denen "Text neu" ausgefuellt ist. Wer nichts eintraegt, '
                 'aendert nichts. Eingelesen wird mit:'),
        ('code', 'python3 scripts/texte-einlesen.py ncwiki-texte.xlsx'),
        ('text', 'Das Skript schreibt die Texte in die Markdown-Dateien und zeigt vorher an, '
                 'was es aendern wuerde (mit --probe aendert es nichts und zeigt nur).'),
        ('leer', ''),
        ('kopf', 'Markdown - das Wenige, das man wissen muss'),
        ('text', '**fett**  ·  *kursiv*  ·  [Linktext](Adresse)  ·  Aufzaehlung mit "- " am '
                 'Zeilenanfang. Ueberschriften beginnen mit # ## ### - diese Zeichen bitte '
                 'stehen lassen und nur den Text dahinter aendern.'),
        ('text', 'Steht im Text etwas wie {{< ref "/ems/uniguide" >}}, ist das ein interner '
                 'Link. Unveraendert uebernehmen, sonst bricht der Link.'),
        ('leer', ''),
        ('kopf', 'Zwei Dinge, die auffallen werden'),
        ('text', f'Seitenbeschreibung: {ohne_beschreibung} Seiten haben noch keine. Das ist '
                 'der Text, den Google unter dem Seitentitel anzeigt - ein bis zwei Saetze, '
                 'hoechstens 160 Zeichen. Diese Zeilen sind rot hinterlegt und haben den '
                 'Status "fehlt".'),
        ('text', 'Platzhalter: Wo "Platzhaltertext" steht, wartet die Seite auf einen '
                 'richtigen Text. Diese Zeilen stehen im Status "offen".'),
    ]
    r = 2
    for art, text in zeilen:
        z = b.cell(row=r, column=2, value=text)
        if art == 'titel':
            z.font = Font(name=SCHRIFT, bold=True, size=16, color='1F3864')
            b.row_dimensions[r].height = 26
        elif art == 'kopf':
            z.font = Font(name=SCHRIFT, bold=True, size=11, color='1F3864')
            b.row_dimensions[r].height = 22
        elif art == 'code':
            z.font = Font(name='Courier New', size=10)
            z.fill = PatternFill('solid', fgColor='F2F2F2')
        elif art == 'beispiel':
            r = beispielzeile(b, r)
            continue
        else:
            z.font = Font(name=SCHRIFT, size=10)
            z.alignment = Alignment(wrap_text=True, vertical='top')
            b.row_dimensions[r].height = 13 * (1 + len(text) // 95)
        r += 1
    return b


def beispielzeile(blatt, r):
    """Eine gefuellte Musterzeile - nicht in den Daten, sondern hier, damit sie
    beim Einlesen nicht versehentlich in die Website wandert."""
    spalten = ['Text bisher', 'Text neu', 'Status', 'Zustaendig', 'Bemerkung']
    werte = ['Platzhaltertext: Hier kommt noch etwas.',
             'Wir bereiten dich kostenlos auf den EMS vor - mit Uebungsserien, '
             'Testsimulationen und Kursen von Studierenden.',
             'fertig', 'Anna', 'Zahlen noch vom Vorstand bestaetigen lassen']
    for i, (kopf, wert) in enumerate(zip(spalten, werte)):
        k = blatt.cell(row=r, column=2 + i, value=kopf)
        k.font = Font(name=SCHRIFT, bold=True, size=9, color='FFFFFF')
        k.fill = KOPF_FUELLUNG
        w = blatt.cell(row=r + 1, column=2 + i, value=wert)
        w.font = Font(name=SCHRIFT, size=9)
        w.alignment = Alignment(wrap_text=True, vertical='top')
        if kopf in ('Text neu', 'Status', 'Zustaendig', 'Bemerkung'):
            w.fill = EINGABE_FUELLUNG
        if i:
            blatt.column_dimensions[get_column_letter(2 + i)].width = 26
    blatt.row_dimensions[r + 1].height = 46
    return r + 2


def sammeln():
    """Alle Seiten und ihre Bausteine einlesen."""
    seiten, texte = [], []
    for s in tb.seiten(PROJEKT):
        bs = tb.bausteine(s['pfad'])
        titel = next((b['text'] for b in bs if b['typ'] == 'Titel'), '')
        if not titel:
            kopf, _, _ = tb.frontmatter_trennen(open(s['pfad'], encoding='utf-8').read())
            name, _, _, _ = tb.kopf_feld(kopf, 'name')
            jahr, _, _, _ = tb.kopf_feld(kopf, 'jahr')
            titel = f'{name} – {jahr}' if name else os.path.basename(s['pfad'])[:-3]
        s['titel'] = titel
        s['bausteine'] = bs
        seiten.append(s)
        for b in bs:
            texte.append((s, b))
    return seiten, texte


def blatt_texte(mappe, texte):
    b = mappe.create_sheet('Texte')
    spalten = [('Nr', 6), ('Sprache', 8), ('Bereich', 14), ('Seite', 22), ('Adresse', 26),
               ('Abschnitt', 22), ('Typ', 13), ('Zeichen', 8),
               ('Text bisher', 60), ('Text neu', 60), ('Status', 11),
               ('Zustaendig', 12), ('Bemerkung', 26),
               ('Datei', 40), ('Baustein', 9), ('Pruefsumme', 11)]
    kopfzeile(b, spalten)
    r = 2
    for nr, (s, bs) in enumerate(texte, start=1):
        bearbeitbar = bs['typ'] in tb.BEARBEITBAR
        fehlt = bs['typ'] == 'Beschreibung' and not bs['text']
        # Der Status sagt, WAS ZU TUN IST - nicht bei jeder Zeile dasselbe.
        # "zu pruefen" ueberall waere Rauschen; wer nach "Platzhalter" filtert,
        # sieht sofort, wo noch gar kein Text steht.
        if fehlt:
            status = 'fehlt'
        elif not bearbeitbar:
            status = 'nicht bearbeiten'
        elif PLATZHALTER.search(bs['text']):
            status = 'Platzhalter'
        else:
            status = 'zu pruefen'
        werte = [nr, s['sprache'], s['bereich'], s['titel'], s['adresse'],
                 bs['abschnitt'], bs['typ'], f'=LEN(I{r})',
                 bs['text'], None, status, None, None,
                 s['rel'], bs['nr'], bs['summe']]
        schrift = NORMAL if bearbeitbar else GRAU
        for i, wert in enumerate(werte, start=1):
            z = b.cell(row=r, column=i, value=wert)
            z.font = schrift
            z.alignment = UMBRUCH if i in (9, 10, 13) else OBEN
        if bearbeitbar:
            b.cell(row=r, column=10).fill = FEHLT_FUELLUNG if fehlt else EINGABE_FUELLUNG
        r += 1
    b.auto_filter.ref = f'A1:P{r - 1}'
    pruefung = DataValidation(type='list', formula1='"%s"' % ','.join(STATUS_WERTE + STATUS_AUTOMATISCH),
                              allow_blank=True, showDropDown=False)
    b.add_data_validation(pruefung)
    pruefung.add(f'K2:K{r - 1}')
    # Die drei Maschinenspalten ausblenden: Sie gehoeren zum Wiederfinden der
    # Textstelle, nicht zur Redaktionsarbeit.
    for sp in ('N', 'O', 'P'):
        b.column_dimensions[sp].hidden = True
    return b, r - 1


def blatt_seiten(mappe, seiten, letzte_textzeile):
    b = mappe.create_sheet('Seiten')
    spalten = [('Sprache', 8), ('Bereich', 16), ('Seite', 30), ('Adresse', 34),
               ('Textbausteine', 12), ('davon fertig', 12), ('Zeichen', 10),
               ('Beschreibung', 12), ('Zustaendig', 14), ('Bemerkung', 34), ('Datei', 44)]
    kopfzeile(b, spalten)
    r = 2
    for s in seiten:
        zahl = sum(1 for x in s['bausteine'] if x['typ'] in tb.BEARBEITBAR)
        zeichen = sum(len(x['text']) for x in s['bausteine'])
        hat_beschreibung = any(x['typ'] == 'Beschreibung' and x['text'] for x in s['bausteine'])
        werte = [s['sprache'], s['bereich'], s['titel'], s['adresse'], zahl,
                 f'=COUNTIFS(Texte!$N$2:$N${letzte_textzeile},$K{r},Texte!$K$2:$K${letzte_textzeile},"fertig")',
                 zeichen, 'ja' if hat_beschreibung else 'fehlt', None, None, s['rel']]
        for i, wert in enumerate(werte, start=1):
            z = b.cell(row=r, column=i, value=wert)
            z.font = NORMAL
            z.alignment = UMBRUCH if i in (3, 10) else OBEN
        if not hat_beschreibung:
            b.cell(row=r, column=8).fill = FEHLT_FUELLUNG
        for sp in (9, 10):
            b.cell(row=r, column=sp).fill = EINGABE_FUELLUNG
        r += 1
    b.auto_filter.ref = f'A1:K{r - 1}'
    b.column_dimensions['K'].hidden = True
    return r - 1


def blatt_uebersicht(mappe, letzte_textzeile, letzte_seitenzeile):
    b = mappe.create_sheet('Uebersicht')
    b.sheet_view.showGridLines = False
    b.column_dimensions['A'].width = 3
    b.column_dimensions['B'].width = 34
    for sp in 'CDEF':
        b.column_dimensions[sp].width = 14

    def schreiben(zeile, spalte, wert, fett=False, format=None):
        z = b.cell(row=zeile, column=spalte, value=wert)
        z.font = Font(name=SCHRIFT, size=10, bold=fett,
                      color='1F3864' if fett else '000000')
        if format:
            z.number_format = format
        return z

    schreiben(2, 2, 'Wie weit sind wir?', fett=True).font = Font(name=SCHRIFT, bold=True, size=14, color='1F3864')
    T = f'Texte!$B$2:$B${letzte_textzeile}'
    S = f'Texte!$K$2:$K${letzte_textzeile}'
    kopf = ['', 'Bausteine', 'fertig', 'passt so', 'noch offen']
    for i, k in enumerate(kopf):
        if k:
            schreiben(4, 2 + i, k, fett=True)
    r = 5
    for sprache, name in (('de', 'Deutsch'), ('fr', 'Franzoesisch'), ('it', 'Italienisch')):
        schreiben(r, 2, name)
        schreiben(r, 3, f'=COUNTIF({T},"{sprache}")')
        schreiben(r, 4, f'=COUNTIFS({T},"{sprache}",{S},"fertig")')
        schreiben(r, 5, f'=COUNTIFS({T},"{sprache}",{S},"passt so")')
        schreiben(r, 6, f'=C{r}-D{r}-E{r}')
        r += 1
    schreiben(r, 2, 'zusammen', fett=True)
    for sp in range(3, 7):
        schreiben(r, sp, f'=SUM({get_column_letter(sp)}5:{get_column_letter(sp)}{r-1})', fett=True)
    anteil = r + 1
    schreiben(anteil, 2, 'Anteil erledigt', fett=True)
    schreiben(anteil, 3, f'=IFERROR((D{r}+E{r})/C{r},0)', fett=True, format='0.0%')

    schreiben(anteil + 2, 2, 'Zeilen mit Platzhaltertext', fett=True)
    schreiben(anteil + 2, 3, f'=COUNTIF({S},"Platzhalter")')
    schreiben(anteil + 3, 2, 'Seiten ohne Beschreibung', fett=True)
    schreiben(anteil + 3, 3, f'=COUNTIF(Seiten!$H$2:$H${letzte_seitenzeile},"fehlt")')
    schreiben(anteil + 4, 2, 'Seiten insgesamt')
    schreiben(anteil + 4, 3, f'=COUNTA(Seiten!$C$2:$C${letzte_seitenzeile})')
    schreiben(anteil + 6, 2,
              'Die Zahlen rechnen sich aus dem Blatt "Texte" - sie stimmen also '
              'immer, ohne dass jemand sie nachfuehrt.').font = Font(name=SCHRIFT, size=9, italic=True, color='606060')


def blatt_luecken(mappe, seiten):
    """Welche deutsche Seite hat noch keine franzoesische oder italienische
    Entsprechung? Auf einer dreisprachigen Website ist das der Fehler, den man
    beim Textschreiben am ehesten findet."""
    b = mappe.create_sheet('Fehlende Uebersetzungen')
    kopfzeile(b, [('Adresse (Deutsch)', 34), ('Seite', 34), ('Bereich', 16),
                  ('Franzoesisch', 14), ('Italienisch', 14), ('Datei', 44)])
    pfade = {s['sprache']: {s2['rel'].split('/', 2)[2] for s2 in seiten if s2['sprache'] == s['sprache']}
             for s in seiten}
    r = 2
    for s in seiten:
        if s['sprache'] != 'de':
            continue
        rest = s['rel'].split('/', 2)[2]
        fr = rest in pfade.get('fr', set())
        it = rest in pfade.get('it', set())
        if fr and it:
            continue
        for i, wert in enumerate([s['adresse'], s['titel'], s['bereich'],
                                  'ja' if fr else 'fehlt', 'ja' if it else 'fehlt',
                                  s['rel']], start=1):
            z = b.cell(row=r, column=i, value=wert)
            z.font = NORMAL
            if wert == 'fehlt':
                z.fill = FEHLT_FUELLUNG
        r += 1
    b.auto_filter.ref = f'A1:F{max(r - 1, 2)}'
    return r - 2


def main():
    ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PROJEKT, 'ncwiki-texte.xlsx')
    seiten, texte = sammeln()
    ohne_beschreibung = sum(1 for s, b in texte if b['typ'] == 'Beschreibung' and not b['text'])
    mappe = Workbook()
    anleitung(mappe, len(texte), len(seiten), ohne_beschreibung)
    _, letzte_text = blatt_texte(mappe, texte)
    letzte_seite = blatt_seiten(mappe, seiten, letzte_text)
    blatt_uebersicht(mappe, letzte_text, letzte_seite)
    luecken = blatt_luecken(mappe, seiten)
    mappe.save(ziel)
    print(f'{ziel}')
    print(f'  {len(seiten)} Seiten, {len(texte)} Textbausteine')
    print(f'  {ohne_beschreibung} Seiten ohne Beschreibung, {luecken} ohne vollstaendige Uebersetzung')


if __name__ == '__main__':
    main()
