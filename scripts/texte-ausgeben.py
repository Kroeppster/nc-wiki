#!/usr/bin/env python3
"""
================================================================================
TEXTLISTE ERZEUGEN - eine Arbeitsmappe je Sprache
================================================================================
    python3 scripts/texte-ausgeben.py                     # alle drei Sprachen
    python3 scripts/texte-ausgeben.py --sprachen fr       # nur Franzoesisch
    python3 scripts/texte-ausgeben.py --ziel ordner/
    python3 scripts/texte-ausgeben.py --uebernehmen alte.xlsx [weitere.xlsx]

Schreibt ncwiki-texte-de.xlsx, -fr.xlsx und -it.xlsx. Jede Mappe hat vorne
eine Anleitung und ein Inhaltsverzeichnis, dann ein Blatt pro Seite in der
Reihenfolge der Navigationsleiste. Die Erfahrungsberichte stehen gesammelt
auf einem Blatt - 68 eigene Reiter wuerden die anderen Seiten verschuetten.

SO WIRD GEARBEITET (steht auch in der Mappe, in der Sprache der Mappe):
  - Text direkt in der Zelle aendern.            -> Zelle wird gelb
  - Neuer Absatz: Zeile einfuegen, hineinschreiben. -> Zeile wird gruen
  - Absatz weg: !Löschen! in die Zelle.          -> Zelle wird rot
  - Ganze Seite weg: !Löschen! in die graue Seiten-Zeile oben.
Franzoesisch und Italienisch zeigen den deutschen Text als Vorlage daneben.
Fehlende Absaetze und fehlende Seiten erscheinen als leere Zeilen; wer sie
ausfuellt, ergaenzt bzw. legt die Seite in dieser Sprache neu an.

--uebernehmen liest den Stand ("fertig", "passt so" ...), Bemerkungen und
Zustaendigkeiten aus einer frueheren Mappe und traegt sie wieder ein - auch
aus dem alten Format mit nur einer Mappe fuer alles.

ZURUECK INS REPO: scripts/texte-einlesen.py. Die Mappen selbst gehoeren
nicht ins Repo (.gitignore); frische gibt es nach jeder Veroeffentlichung
unter <website>/redaktion/ (siehe .github/workflows/hugo.yml).

Gebraucht werden openpyxl und pyyaml (pip install openpyxl pyyaml).
================================================================================
"""
import argparse
import os
import re
import sys

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit('Fehlendes Paket: openpyxl. Bitte "pip install openpyxl pyyaml".')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texte_bausteine as tb

SCHRIFT = 'Arial'
ERSTE_ZEILE = 6            # hier beginnen die Daten auf jedem Seitenblatt
# Versteckte Spalten, fuer das Einlesen:
#   original  der Text beim Ausgeben (daran erkennt man eine Aenderung)
#   nr        Nummer des Bausteins in der Datei; leer = neue Zeile
#   datei     nur in der grauen Seiten-Zeile: die Datei der Seite
#   summe     nur dort: Pruefsumme der Datei beim Ausgeben (NEU = anzulegen)
#   quelle    nur dort, bei neuen Seiten: die deutsche Vorlage
#   art       Art des Bausteins (absatz, titel, tabelle ...)
#   vnr       Nummer des deutschen Vorlage-Bausteins
#   seite     in JEDER Zeile die Datei - so faellt beim Einlesen auf, wenn
#             die graue Seiten-Zeile geloescht oder eine Zeile aus einer
#             anderen Seite hineinkopiert wurde
SPALTEN = ['typ', 'text', 'vorlage', 'aenderung', 'stand', 'bemerkung',
           'original', 'nr', 'datei', 'summe', 'quelle', 'art', 'vnr', 'seite']
SP = {k: get_column_letter(i + 1) for i, k in enumerate(SPALTEN)}
VERSTECKT = ('original', 'nr', 'datei', 'summe', 'quelle', 'art', 'vnr', 'seite')
VERZEICHNIS = '_seiten'     # sehr verstecktes Blatt: welche Seiten in der Mappe stehen

# Die Loeschmarke wird in jeder Sprache erkannt - wer im franzoesischen Blatt
# aus Gewohnheit !Löschen! schreibt, soll trotzdem loeschen koennen.
LOESCHMARKEN = ('!löschen!', '!loeschen!', '!supprimer!', '!eliminare!')

FARBE = {
    '': '1F3864', 'news': '2E75B6', 'ems': '548235', 'unterstuetzer-innen': 'BF8F00',
    'ueber-uns': '7030A0', 'kontakt': 'C55A11', 'berichte': '70AD47',
}
WEITERE = '7F7F7F'

GELB = PatternFill('solid', fgColor='FFF2CC')
GRUEN = PatternFill('solid', fgColor='E2EFDA')
ROT = PatternFill('solid', fgColor='FCE4E4')
HELLGRAU = PatternFill('solid', fgColor='F2F2F2')
SEITENBAND = PatternFill('solid', fgColor='D9E1F2')
KOPF = PatternFill('solid', fgColor='1F3864')

# ---------------------------------------------------------------------------
# Alles, was in der Mappe zu lesen ist, in drei Sprachen
# ---------------------------------------------------------------------------
T = {
    'de': dict(
        typen=dict(seite='Seite', titel='Titel', beschreibung='Beschreibung', bildtext='Bildtext',
                   ueberschrift1='Hauptüberschrift', ueberschrift='Überschrift',
                   unterueberschrift='Unterüberschrift', absatz='Absatz', liste='Liste',
                   zitat='Zitat', tabelle='Tabelle', code='Code', baustein='Baustein', html='HTML'),
        einfuegbar=['Absatz', 'Überschrift', 'Unterüberschrift', 'Liste', 'Zitat'],
        kopf=['Typ', 'Text', 'Deutsche Vorlage', 'Änderung', 'Stand', 'Bemerkung'],
        stand=['offen', 'in Arbeit', 'fertig', 'passt so'],
        geaendert='✎ geändert', neu='+ neu', weg='✕ löschen', seite_weg='✕ ganze Seite löschen',
        leer='⚠ leer – bleibt', gesperrt='⚠ gesperrt – bleibt', fehlt='· fehlt noch',
        loeschmarke='!Löschen!',
        inhalt='Inhalt', anleitung='Anleitung', berichte='Erfahrungsberichte', berichte_zusatz='(+ {n} Berichte)',
        inhalt_kopf=['Bereich', 'Seite', 'Adresse', 'Änderungen', 'Beschreibung', 'Übersetzung',
                     'Zuständig', 'Stand', 'Bemerkung'],
        ja='ja', fehlt_wort='fehlt', neu_anlegen='neu anlegen', vorhanden='vorhanden',
        absaetze_fehlen='{n} Absätze fehlen', absatz_fehlt='1 Absatz fehlt',
        zurueck='← zum Inhalt', live='auf der Website ansehen ↗',
        seite_hinweis='Ganze Seite löschen: !Löschen! in die graue Zeile „Seite" schreiben.',
        neu_hinweis='Diese Seite gibt es auf dieser Sprache noch nicht. Titel und Texte ausfüllen – beim Einlesen wird sie angelegt.',
        bereiche={'': 'Startseite', 'news': 'News', 'ems': 'EMS', 'unterstuetzer-innen': 'Unterstützer:innen',
                  'ueber-uns': 'Über uns', 'kontakt': 'Kontakt'},
        weitere='Weitere Seiten',
        zusammen='Zusammen', seiten_wort='Seiten', aenderungen_wort='Änderungen bisher',
        titel='NCWiki – Texte (Deutsch)',
    ),
    'fr': dict(
        typen=dict(seite='Page', titel='Titre', beschreibung='Description', bildtext='Texte d\'image',
                   ueberschrift1='Titre principal', ueberschrift='Titre de section',
                   unterueberschrift='Sous-titre', absatz='Paragraphe', liste='Liste',
                   zitat='Citation', tabelle='Tableau', code='Code', baustein='Module', html='HTML'),
        einfuegbar=['Paragraphe', 'Titre de section', 'Sous-titre', 'Liste', 'Citation'],
        kopf=['Type', 'Texte', 'Modèle allemand', 'Modification', 'État', 'Remarque'],
        stand=['ouvert', 'en cours', 'terminé', 'ok tel quel'],
        geaendert='✎ modifié', neu='+ nouveau', weg='✕ supprimer', seite_weg='✕ supprimer la page',
        leer='⚠ vide – reste', gesperrt='⚠ verrouillé – reste', fehlt='· à traduire',
        loeschmarke='!Supprimer!',
        inhalt='Sommaire', anleitung='Mode d\'emploi', berichte='Témoignages', berichte_zusatz='(+ {n} témoignages)',
        inhalt_kopf=['Rubrique', 'Page', 'Adresse', 'Modifications', 'Description', 'Traduction',
                     'Responsable', 'État', 'Remarque'],
        ja='oui', fehlt_wort='manque', neu_anlegen='à créer', vorhanden='existe',
        absaetze_fehlen='{n} paragraphes à traduire', absatz_fehlt='1 paragraphe à traduire',
        zurueck='← sommaire', live='voir sur le site ↗',
        seite_hinweis='Supprimer toute la page : écrire !Supprimer! dans la ligne grise « Page ».',
        neu_hinweis='Cette page n\'existe pas encore en français. Remplir le titre et les textes – elle sera créée à l\'import.',
        bereiche={'': 'Accueil', 'news': 'Actualités', 'ems': 'EMS', 'unterstuetzer-innen': 'Soutiens',
                  'ueber-uns': 'À propos', 'kontakt': 'Contact'},
        weitere='Autres pages',
        zusammen='Total', seiten_wort='pages', aenderungen_wort='modifications jusqu\'ici',
        titel='NCWiki – Textes (français)',
    ),
    'it': dict(
        typen=dict(seite='Pagina', titel='Titolo', beschreibung='Descrizione', bildtext='Testo immagine',
                   ueberschrift1='Titolo principale', ueberschrift='Titolo di sezione',
                   unterueberschrift='Sottotitolo', absatz='Paragrafo', liste='Elenco',
                   zitat='Citazione', tabelle='Tabella', code='Codice', baustein='Modulo', html='HTML'),
        einfuegbar=['Paragrafo', 'Titolo di sezione', 'Sottotitolo', 'Elenco', 'Citazione'],
        kopf=['Tipo', 'Testo', 'Modello tedesco', 'Modifica', 'Stato', 'Nota'],
        stand=['aperto', 'in corso', 'finito', 'va bene così'],
        geaendert='✎ modificato', neu='+ nuovo', weg='✕ eliminare', seite_weg='✕ eliminare la pagina',
        leer='⚠ vuoto – resta', gesperrt='⚠ bloccato – resta', fehlt='· da tradurre',
        loeschmarke='!Eliminare!',
        inhalt='Indice', anleitung='Istruzioni', berichte='Testimonianze', berichte_zusatz='(+ {n} testimonianze)',
        inhalt_kopf=['Sezione', 'Pagina', 'Indirizzo', 'Modifiche', 'Descrizione', 'Traduzione',
                     'Responsabile', 'Stato', 'Nota'],
        ja='sì', fehlt_wort='manca', neu_anlegen='da creare', vorhanden='esiste',
        absaetze_fehlen='{n} paragrafi da tradurre', absatz_fehlt='1 paragrafo da tradurre',
        zurueck='← indice', live='vedi sul sito ↗',
        seite_hinweis='Eliminare tutta la pagina: scrivere !Eliminare! nella riga grigia «Pagina».',
        neu_hinweis='Questa pagina non esiste ancora in italiano. Compilare titolo e testi – verrà creata all\'importazione.',
        bereiche={'': 'Home', 'news': 'Notizie', 'ems': 'EMS', 'unterstuetzer-innen': 'Sostenitori',
                  'ueber-uns': 'Chi siamo', 'kontakt': 'Contatto'},
        weitere='Altre pagine',
        zusammen='Totale', seiten_wort='pagine', aenderungen_wort='modifiche finora',
        titel='NCWiki – Testi (italiano)',
    ),
}

ANLEITUNG = {
    'de': [
        ('titel', 'NCWiki – Texte bearbeiten'),
        ('text', 'In dieser Mappe steht jeder sichtbare Text der deutschen Website. Jede Seite hat ein '
                 'eigenes Blatt, in der Reihenfolge der Navigationsleiste. Im Blatt „Inhalt" gibt es zu '
                 'jeder Seite einen Link.'),
        ('kopf', 'So wird gearbeitet'),
        ('text', 'Text ändern: direkt in der Zelle in der Spalte „Text" überschreiben, wie in Word. '
                 'Die Zelle wird gelb.'),
        ('text', 'Neuer Absatz, am einfachsten: den Text in dieselbe Zelle schreiben, mit einer leeren '
                 'Zeile dazwischen (zweimal Alt+Enter, Mac: Ctrl+Option+Enter). Jede Leerzeile in einer '
                 'Zelle wird auf der Website ein neuer Absatz; auch Listen („- ") gehen so.'),
        ('text', 'Neue Überschrift oder neue Zeile: links auf die Zeilennummer klicken, sodass die GANZE '
                 'Zeile markiert ist, dann Rechtsklick → Zeilen einfügen, und den Text hineinschreiben. In '
                 'der Spalte „Typ" wählen, ob es ein Absatz, eine Überschrift oder eine Liste ist – ohne '
                 'Angabe wird es ein Absatz. Die Zeile wird grün. Wurden aus Versehen nur Zellen statt der '
                 'ganzen Zeile eingefügt oder verschoben, ist das nicht schlimm: Das Einlesen merkt es und '
                 'übernimmt die Seite so, wie sie im Blatt zu sehen ist.'),
        ('text', 'Absatz löschen: !Löschen! in die Zelle schreiben. Die Zelle wird rot.'),
        ('text', 'Ganze Seite löschen: !Löschen! in die graue Zeile „Seite" oben im Blatt schreiben.'),
        ('text', 'Reihenfolge ändern: Zeile ausschneiden und an der neuen Stelle einfügen.'),
        ('text', '„Stand" und „Bemerkung" sind für euch: Wer eine Seite durchgesehen hat, setzt '
                 '„fertig" oder „passt so". Das wird nicht auf die Website übertragen, bleibt aber in der '
                 'nächsten Mappe erhalten.'),
        ('kopf', 'Bitte nicht'),
        ('text', 'Nicht sortieren und nicht filtern-und-löschen: Die Reihenfolge der Zeilen ist die '
                 'Reihenfolge auf der Seite. Graue, kursive Zeilen (Tabellen, Bausteine) nicht ändern – '
                 'das Einlesen lässt sie ohnehin stehen. Eine leere Zelle löscht nichts; zum Löschen '
                 'immer !Löschen! schreiben.'),
        ('kopf', 'Ein paar Zeichen, die man kennen sollte'),
        ('text', '**fett**   ·   *kursiv*   ·   [Linktext](https://…)   ·   Link auf eine eigene Seite: '
                 '[Uniguide](/ems/uniguide) – nur der Pfad, ohne Sprache.'),
        ('text', 'In einer Liste beginnt jede Zeile mit „- ". Neue Zeile in derselben Zelle: Alt+Enter '
                 '(Mac: Ctrl+Option+Enter).'),
        ('kopf', 'Und dann?'),
        ('text', 'Die Datei auf GitHub in den Ordner „redaktion" hochladen: {ordner} → Add file → Upload '
                 'files → „Commit directly to the main branch". Nach ein, zwei Minuten erscheint ein '
                 'Vorschlag (Pull Request) mit einem Bericht, was übernommen wurde. Live ist es, sobald '
                 'jemand den Vorschlag übernimmt. Genaueres: docs/WARTUNG.md, Abschnitt 2b.'),
        ('text', 'Achtung: Das Repository ist öffentlich. Alles in der Mappe – auch Bemerkungen und '
                 'Zuständigkeiten – ist nach dem Hochladen für alle sichtbar.'),
        ('text', 'Immer mit einer frischen Mappe anfangen: {mappe} (nach jeder Veröffentlichung neu). '
                 'Wurde eine Seite inzwischen anderswo geändert, wird sie beim Einlesen übersprungen und '
                 'gemeldet, statt etwas zu überschreiben.'),
    ],
    'fr': [
        ('titel', 'NCWiki – modifier les textes'),
        ('text', 'Ce classeur contient tous les textes visibles du site en français. Chaque page a sa '
                 'propre feuille, dans l\'ordre du menu. La feuille « Sommaire » contient un lien vers '
                 'chaque page.'),
        ('text', 'La colonne « Modèle allemand » montre le texte allemand correspondant. Les lignes vides '
                 'avec un modèle sont des paragraphes – ou des pages entières – qui manquent encore en '
                 'français : il suffit de les remplir.'),
        ('kopf', 'Comment travailler'),
        ('text', 'Modifier un texte : écrire directement dans la cellule de la colonne « Texte ». La '
                 'cellule devient jaune.'),
        ('text', 'Nouveau paragraphe, le plus simple : écrire le texte dans la même cellule, avec une '
                 'ligne vide entre les deux (deux fois Alt+Entrée, Mac : Ctrl+Option+Entrée). Chaque ligne '
                 'vide dans une cellule devient un nouveau paragraphe sur le site ; les listes (« - ») '
                 'fonctionnent aussi.'),
        ('text', 'Nouveau titre ou nouvelle ligne : cliquer à gauche sur le numéro de ligne pour sélectionner '
                 'la ligne ENTIÈRE, puis clic droit → Insérer, et y écrire le texte. La colonne « Type » '
                 'permet de choisir paragraphe, titre ou liste – par défaut, paragraphe. La ligne devient '
                 'verte. Si seules des cellules ont été insérées ou déplacées par erreur, ce n\'est pas '
                 'grave : l\'import le remarque et reprend la page telle qu\'elle apparaît dans la feuille.'),
        ('text', 'Supprimer un paragraphe : écrire !Supprimer! dans la cellule. Elle devient rouge.'),
        ('text', 'Supprimer toute la page : écrire !Supprimer! dans la ligne grise « Page » en haut.'),
        ('text', '« État » et « Remarque » sont pour vous : ils ne vont pas sur le site, mais sont '
                 'repris dans le prochain classeur.'),
        ('kopf', 'À éviter'),
        ('text', 'Ne pas trier : l\'ordre des lignes est l\'ordre sur la page. Ne pas modifier les lignes '
                 'grises en italique (tableaux, modules). Une cellule vide ne supprime rien.'),
        ('kopf', 'Quelques signes utiles'),
        ('text', '**gras**   ·   *italique*   ·   [texte du lien](https://…)   ·   lien vers une page du '
                 'site : [Uniguide](/ems/uniguide) – seulement le chemin, sans /fr/.'),
        ('text', 'Nouvelle ligne dans la même cellule : Alt+Entrée (Mac : Ctrl+Option+Entrée).'),
        ('kopf', 'Et ensuite ?'),
        ('text', 'Déposer le fichier sur GitHub dans le dossier « redaktion » : {ordner} → Add file → '
                 'Upload files → « Commit directly to the main branch ». Une ou deux minutes plus tard, '
                 'une proposition (pull request) apparaît avec un rapport de ce qui a été repris. C\'est '
                 'en ligne dès que quelqu\'un accepte la proposition.'),
        ('text', 'Attention : le dépôt est public. Tout ce qui est dans le classeur – remarques et '
                 'responsables compris – est visible par tous une fois déposé.'),
        ('text', 'Toujours partir d\'un classeur récent : {mappe} (renouvelé à chaque publication). Une '
                 'page modifiée entre-temps ailleurs est sautée et signalée, rien n\'est écrasé.'),
    ],
    'it': [
        ('titel', 'NCWiki – modificare i testi'),
        ('text', 'Questa cartella contiene tutti i testi visibili del sito in italiano. Ogni pagina ha il '
                 'suo foglio, nell\'ordine del menu. Il foglio «Indice» contiene un link a ogni pagina.'),
        ('text', 'La colonna «Modello tedesco» mostra il testo tedesco corrispondente. Le righe vuote con '
                 'un modello sono paragrafi – o pagine intere – che mancano ancora in italiano: basta '
                 'compilarle.'),
        ('kopf', 'Come lavorare'),
        ('text', 'Modificare un testo: scrivere direttamente nella cella della colonna «Testo». La cella '
                 'diventa gialla.'),
        ('text', 'Nuovo paragrafo, il modo più semplice: scrivere il testo nella stessa cella, con una riga '
                 'vuota in mezzo (due volte Alt+Invio, Mac: Ctrl+Option+Invio). Ogni riga vuota in una cella '
                 'diventa un nuovo paragrafo sul sito; funzionano anche gli elenchi («- »).'),
        ('text', 'Nuovo titolo o nuova riga: cliccare a sinistra sul numero di riga, in modo da selezionare '
                 'l\'INTERA riga, poi clic destro → Inserisci, e scriverci il testo. La colonna «Tipo» permette '
                 'di scegliere paragrafo, titolo o elenco – di default paragrafo. La riga diventa verde. Se '
                 'per errore sono state inserite o spostate solo delle celle, non è grave: l\'importazione '
                 'se ne accorge e riprende la pagina così come appare nel foglio.'),
        ('text', 'Eliminare un paragrafo: scrivere !Eliminare! nella cella. Diventa rossa.'),
        ('text', 'Eliminare tutta la pagina: scrivere !Eliminare! nella riga grigia «Pagina» in alto.'),
        ('text', '«Stato» e «Nota» sono per voi: non vanno sul sito, ma vengono ripresi nella prossima '
                 'cartella.'),
        ('kopf', 'Da evitare'),
        ('text', 'Non ordinare: l\'ordine delle righe è l\'ordine sulla pagina. Non modificare le righe '
                 'grigie in corsivo (tabelle, moduli). Una cella vuota non elimina niente.'),
        ('kopf', 'Qualche segno utile'),
        ('text', '**grassetto**   ·   *corsivo*   ·   [testo del link](https://…)   ·   link a una pagina '
                 'del sito: [Uniguide](/ems/uniguide) – solo il percorso, senza /it/.'),
        ('text', 'Nuova riga nella stessa cella: Alt+Invio (Mac: Ctrl+Option+Invio).'),
        ('kopf', 'E poi?'),
        ('text', 'Caricare il file su GitHub nella cartella «redaktion»: {ordner} → Add file → Upload '
                 'files → «Commit directly to the main branch». Dopo un paio di minuti appare una proposta '
                 '(pull request) con un rapporto su cosa è stato ripreso. È online appena qualcuno accetta '
                 'la proposta.'),
        ('text', 'Attenzione: il repository è pubblico. Tutto ciò che è nella cartella – note e '
                 'responsabili compresi – è visibile a tutti dopo il caricamento.'),
        ('text', 'Partire sempre da una cartella recente: {mappe} (rinnovata a ogni pubblicazione). Una '
                 'pagina modificata nel frattempo altrove viene saltata e segnalata, niente viene '
                 'sovrascritto.'),
    ],
}

# Stand in allen Sprachen auf einen Schluessel bringen (fuer --uebernehmen)
STAND_SCHLUESSEL = ['offen', 'arbeit', 'fertig', 'passt']
STAND_ALT = {'passt so': 'passt', 'fertig': 'fertig', 'in arbeit': 'arbeit'}


def stand_schluessel(wert):
    if not wert:
        return None
    w = str(wert).strip().lower()
    for sprache in T.values():
        for k, name in zip(STAND_SCHLUESSEL, sprache['stand']):
            if w == name.lower():
                return k
    return STAND_ALT.get(w)


def typ_label(sprache, typ, ebene=0):
    t = T[sprache]['typen']
    if typ == 'ueberschrift':
        return t['ueberschrift1'] if ebene == 1 else (t['ueberschrift'] if ebene <= 2 else t['unterueberschrift'])
    return t.get(typ, typ)


def schluessel_text(text):
    """Vergleichsschluessel fuer --uebernehmen: eine Pruefsumme des Textes
    ohne Rauten, &amp; und Leerraum. Eine Pruefsumme statt des Textes, damit
    redaktion/stand.json nicht noch einmal die ganze Website enthaelt."""
    t = str(text or '')
    t = re.sub(r'^\s*#{1,6}\s+', '', t).replace('&amp;', '&')
    return tb.pruefsumme(re.sub(r'\s+', ' ', t).strip())


# ---------------------------------------------------------------------------
# Blattnamen
# ---------------------------------------------------------------------------
def blattname(seite, vergeben):
    """Excel erlaubt 31 Zeichen und keine der Zeichen : \\ / ? * [ ]."""
    titel = seite['titel']
    if len(titel) > 24 and ' - ' in titel:
        titel = titel.rsplit(' - ', 1)[1]
    name = titel
    if seite.get('eltern') and seite['tiefe'] >= 3:
        eltern = seite['eltern']
        kurz = eltern if len(eltern) + 3 + len(titel) <= 31 else eltern[:5].rstrip() + '.'
        name = f'{kurz} › {titel}'
    name = re.sub(r'[:\\/?*\[\]]', '', name).strip("' ")
    if len(name) > 31:
        name = name[:30].rstrip() + '…'
    basis, n = name, 2
    while name.lower() in vergeben:
        endung = f' {n}'
        name = basis[:31 - len(endung)] + endung
        n += 1
    vergeben.add(name.lower())
    return name


def zitat_name(name):
    return "'" + name.replace("'", "''") + "'"


# ---------------------------------------------------------------------------
# Eine Seite als Zeilen
# ---------------------------------------------------------------------------
def zeilen_fuer_seite(sprache, seite, de_seite, projekt):
    """Liefert die Zeilen fuer eine Seite: Liste von dicts mit den SPALTEN.

    seite     die Seite in dieser Sprache, oder None (gibt es noch nicht)
    de_seite  die deutsche Seite (Vorlage), oder None
    """
    zeilen = []
    if seite:
        with open(seite['pfad'], encoding='utf-8') as f:
            roh = f.read()
        eigene = tb.bausteine_aus_text(roh)
        summe = tb.pruefsumme(roh)
    else:
        eigene, summe = [], 'NEU'
    vorlage = tb.bausteine(de_seite['pfad']) if (de_seite and sprache != 'de') else []
    ziel = seite or de_seite
    datei = seite['rel'] if seite else de_seite['rel'].replace('content/de/', f'content/{sprache}/', 1)

    zeilen.append(dict(typ=T[sprache]['typen']['seite'], text=ziel['titel'], original=ziel['titel'],
                       datei=datei, summe=summe,
                       quelle=de_seite['rel'] if (de_seite and not seite) else '', art='seite',
                       _seite=ziel))

    paare = tb.zuordnen(eigene, vorlage) if vorlage else [(b, None) for b in eigene]

    # Titel und Beschreibung immer anbieten - eine fehlende Beschreibung ist
    # die haeufigste Luecke, und eine leere Zeile faellt auf. Ausser bei
    # Erfahrungsberichten: Die haben keinen Titel (angezeigt werden Name und
    # Jahr), und 67 leere Zeilenpaare waeren nur Rauschen.
    kopf_da = {(u or v)['typ'] for u, v in paare if (u or v)['typ'] in ('titel', 'beschreibung', 'bildtext')}
    einschub = []
    bericht = ziel['innen'].startswith('ems/erfahrungsberichte/') and not ziel['innen'].endswith('_index.md')
    for typ in ('titel', 'beschreibung'):
        if typ not in kopf_da and not bericht:
            einschub.append((None, None, typ))
    hat_bild = bool((ziel.get('kopf') or {}).get('featured_image'))
    if hat_bild and 'bildtext' not in kopf_da:
        einschub.append((None, None, 'bildtext'))

    def zeile_aus(u, v, typ_leer=None):
        b = u or v
        typ = b['typ'] if b else typ_leer
        eb = b['ebene'] if b else 0
        z = dict(typ=typ_label(sprache, typ, eb), art=typ)
        if u:
            z.update(text=u['text'], original=u['text'], nr=u['nr'])
        else:
            z.update(text='', original='', nr='')
        if v:
            z.update(vorlage=v['text'], vnr=v['nr'])
        gesperrt = typ in tb.GESPERRT
        if gesperrt and not u and v and not seite:
            # Neue Seite: Tabellen und Bausteine werden aus der deutschen
            # Seite uebernommen. Das soll man sehen, nicht erst hinterher.
            # nr "v" heisst: aus der Vorlage vorbelegt - weder gruen noch
            # als Aenderung gezaehlt, solange niemand daran etwas aendert.
            z.update(text=v['roh'], original=v['roh'], nr='v')
        z['_gesperrt'] = gesperrt
        return z

    kopfpaare = [(u, v) for u, v in paare if (u or v)['typ'] in ('titel', 'beschreibung', 'bildtext')]
    rumpfpaare = [(u, v) for u, v in paare if (u or v)['typ'] not in ('titel', 'beschreibung', 'bildtext')]
    reihenfolge = {'titel': 0, 'beschreibung': 1, 'bildtext': 2}
    kopfzeilen = [zeile_aus(u, v) for u, v in kopfpaare] + [zeile_aus(None, None, t) for _, _, t in einschub]
    kopfzeilen.sort(key=lambda z: reihenfolge[z['art']])
    zeilen += kopfzeilen
    zeilen += [zeile_aus(u, v) for u, v in rumpfpaare]
    return zeilen


# ---------------------------------------------------------------------------
# Blatt schreiben
# ---------------------------------------------------------------------------
def schluessel_zeile(blatt):
    for i, k in enumerate(SPALTEN, start=1):
        blatt.cell(row=1, column=i, value=k)
    blatt.row_dimensions[1].hidden = True


def spaltenkopf(blatt, sprache, zeile):
    for i, name in enumerate(T[sprache]['kopf'], start=1):
        z = blatt.cell(row=zeile, column=i, value=name)
        z.font = Font(name=SCHRIFT, bold=True, color='FFFFFF', size=10)
        z.fill = KOPF
        z.alignment = Alignment(vertical='center')
    breiten = dict(typ=17, text=82 if sprache == 'de' else 62, vorlage=55, aenderung=17, stand=12,
                   bemerkung=28)
    for k, w in breiten.items():
        blatt.column_dimensions[SP[k]].width = w
    for k in VERSTECKT:
        blatt.column_dimensions[SP[k]].hidden = True
    if sprache == 'de':
        blatt.column_dimensions[SP['vorlage']].hidden = True


def loesch_bedingung(zelle):
    return 'OR(' + ','.join(f'ISNUMBER(SEARCH("{m}",{zelle}))' for m in LOESCHMARKEN) + ')'


def zeilen_schreiben(blatt, sprache, zeilen, start, stand_alt):
    L = T[sprache]
    normal = Font(name=SCHRIFT, size=10)
    grau = Font(name=SCHRIFT, size=10, italic=True, color='808080')
    fett = Font(name=SCHRIFT, size=10, bold=True, color='1F3864')
    vorl = Font(name=SCHRIFT, size=9, color='595959')
    umbruch = Alignment(wrap_text=True, vertical='top')
    oben = Alignment(vertical='top')
    r = start
    for z in zeilen:
        for k in SPALTEN:
            if k in z and not k.startswith('_'):
                blatt.cell(row=r, column=SPALTEN.index(k) + 1, value=z[k])
        B, G = f'${SP["text"]}{r}', f'${SP["original"]}{r}'
        wegf = loesch_bedingung(B)
        if z['art'] == 'seite':
            formel = f'=IF({wegf},"{L["seite_weg"]}","")'
        elif z.get('_gesperrt'):
            formel = f'=IF(EXACT({B},{G}),"","{L["gesperrt"]}")' if z.get('nr') != '' else ''
        elif z.get('nr') == '':
            formel = f'=IF({wegf},"",IF({B}="","{L["fehlt"]}" ,"{L["neu"]}"))'.replace('" ,', '",') \
                if z.get('vorlage') else f'=IF(OR({B}="",{wegf}),"","{L["neu"]}")'
        else:
            formel = f'=IF({wegf},"{L["weg"]}",IF({B}="","{L["leer"]}",IF(EXACT({B},{G}),"","{L["geaendert"]}")))'
        if formel:
            blatt.cell(row=r, column=SPALTEN.index('aenderung') + 1, value=formel)

        # Stand und Bemerkung aus einer frueheren Mappe
        alt = stand_alt.get((z['seite'], schluessel_text(z.get('original') or z.get('text'))))
        if alt:
            if alt[0]:
                blatt.cell(row=r, column=SPALTEN.index('stand') + 1,
                           value=L['stand'][STAND_SCHLUESSEL.index(alt[0])])
            if alt[1]:
                blatt.cell(row=r, column=SPALTEN.index('bemerkung') + 1, value=alt[1])

        for k in ('typ', 'text', 'vorlage', 'aenderung', 'stand', 'bemerkung'):
            c = blatt.cell(row=r, column=SPALTEN.index(k) + 1)
            c.alignment = umbruch if k in ('text', 'vorlage', 'bemerkung') else oben
            c.font = vorl if k == 'vorlage' else normal
            if k == 'text':
                c.number_format = '@'
        if z['art'] == 'seite':
            for k in ('typ', 'text', 'vorlage', 'aenderung', 'stand', 'bemerkung'):
                c = blatt.cell(row=r, column=SPALTEN.index(k) + 1)
                c.fill = SEITENBAND
                c.font = fett
        elif z.get('_gesperrt'):
            for k in ('typ', 'text'):
                c = blatt.cell(row=r, column=SPALTEN.index(k) + 1)
                c.font = grau
                c.fill = HELLGRAU
        r += 1
    return r


def bedingte_formate(blatt, von, bis):
    """Farben nach Art der Aenderung. Sie haengen NICHT an der Spalte
    "Aenderung", sondern rechnen selbst: In eingefuegte Zeilen kopiert Excel
    keine Formeln, bedingte Formate dagegen dehnt es auf eingefuegte Zeilen
    aus - so wird eine neue Zeile gruen, obwohl in ihr keine Formel steht."""
    B, G, H, I, K = SP['text'], SP['original'], SP['nr'], SP['datei'], SP['art']
    bereich = f'{B}{von}:{B}{bis}'
    weg = loesch_bedingung(f'${B}{von}')
    # Gesperrte Zeilen (Tabellen, Bausteine) bleiben beim Einlesen, wie sie
    # sind - also auch nicht rot oder gelb faerben, das wuerde etwas
    # versprechen, das nicht passiert. Die Spalte "Aenderung" sagt es dort.
    offen = ','.join(f'${K}{von}<>"{t}"' for t in tb.GESPERRT)
    blatt.conditional_formatting.add(bereich, FormulaRule(
        formula=[f'AND(${I}{von}="",{offen},{weg})'], fill=ROT, font=Font(strike=True, color='9C0006'),
        stopIfTrue=True))
    blatt.conditional_formatting.add(bereich, FormulaRule(
        formula=[f'AND(${I}{von}="",${H}{von}="",${B}{von}<>"")'], fill=GRUEN, stopIfTrue=True))
    blatt.conditional_formatting.add(bereich, FormulaRule(
        formula=[f'AND(${I}{von}="",{offen},${H}{von}<>"",NOT(EXACT(${B}{von},${G}{von})))'], fill=GELB,
        stopIfTrue=True))
    blatt.conditional_formatting.add(f'{SP["typ"]}{von}:{SP["typ"]}{bis}', FormulaRule(
        formula=[f'AND(${I}{von}<>"",{weg})'], fill=ROT, stopIfTrue=True))


def seitenblatt(mappe, sprache, name, farbe, gruppen, stand_alt, basis_url, inhalt_name):
    """Ein Blatt mit einer oder mehreren Seiten. gruppen: Liste von
    (seite_oder_None, de_seite_oder_None, zeilen)."""
    L = T[sprache]
    b = mappe.create_sheet(name)
    b.sheet_properties.tabColor = farbe
    b.sheet_view.zoomScale = 110
    schluessel_zeile(b)
    erste = gruppen[0]
    ziel = erste[0] or erste[1]
    ueber = b.cell(row=2, column=1, value=name if len(gruppen) > 1 else ziel['titel'])
    ueber.font = Font(name=SCHRIFT, bold=True, size=14, color='1F3864')
    zur = b.cell(row=2, column=SPALTEN.index('aenderung') + 1, value=L['zurueck'])
    zur.hyperlink = f'#{zitat_name(inhalt_name)}!A1'
    zur.font = Font(name=SCHRIFT, size=10, color='0563C1', underline='single')
    if len(gruppen) == 1:
        adr = (erste[0] or {}).get('adresse') or tb.adresse_von(erste[1]['innen'], sprache)
        a = b.cell(row=3, column=1, value=adr)
        a.font = Font(name=SCHRIFT, size=9, color='595959')
        if erste[0]:
            live = b.cell(row=3, column=2, value=L['live'])
            live.hyperlink = basis_url.rstrip('/') + adr
            live.font = Font(name=SCHRIFT, size=9, color='0563C1', underline='single')
    hinweis = L['neu_hinweis'] if (len(gruppen) == 1 and not erste[0]) else L['seite_hinweis']
    h = b.cell(row=4, column=1, value=hinweis)
    h.font = Font(name=SCHRIFT, size=9, italic=True, color='595959')
    spaltenkopf(b, sprache, 5)
    b.freeze_panes = f'{SP["text"]}{ERSTE_ZEILE}'
    r = ERSTE_ZEILE
    for seite, de_seite, zeilen in gruppen:
        for z in zeilen:
            z['seite'] = zeilen[0]['datei']
        r = zeilen_schreiben(b, sprache, zeilen, r, stand_alt)
    letzte = r - 1
    # Textformat auch unterhalb der letzten Zeile. Ohne das nimmt Excel eine
    # Eingabe wie "- Punkt" oder "= 5" als Formel und zeigt #NAME?.
    for rr in range(letzte + 1, letzte + 101):
        c = b.cell(row=rr, column=SPALTEN.index('text') + 1)
        c.number_format = '@'
        c.alignment = Alignment(wrap_text=True, vertical='top')
    bedingte_formate(b, ERSTE_ZEILE, letzte + 400)
    typen = DataValidation(type='list', formula1='"%s"' % ','.join(L['einfuegbar']), allow_blank=True)
    b.add_data_validation(typen)
    typen.add(f'{SP["typ"]}{ERSTE_ZEILE}:{SP["typ"]}{letzte + 400}')
    stand = DataValidation(type='list', formula1='"%s"' % ','.join(L['stand']), allow_blank=True)
    b.add_data_validation(stand)
    stand.add(f'{SP["stand"]}{ERSTE_ZEILE}:{SP["stand"]}{letzte + 400}')
    return b, letzte


# ---------------------------------------------------------------------------
# Frueheren Stand einlesen (--uebernehmen)
# ---------------------------------------------------------------------------
def frueheren_stand_lesen(pfade):
    """Liest Stand, Bemerkung (je Zeile) und Zustaendig (je Seite) aus
    frueheren Mappen - neues Format, das alte mit einem Blatt "Texte", oder
    redaktion/stand.json (siehe stand_speichern).

    Spaetere Quellen gewinnen. Eine Zeile, die in einer neueren Mappe
    vorkommt, gilt dort auch dann, wenn Stand und Bemerkung leer sind - so
    laesst sich eine Bemerkung wieder loswerden."""
    zeilen, seiten = {}, {}
    for pfad in pfade:
        if pfad.endswith('.json'):
            import json
            with open(pfad, encoding='utf-8') as f:
                daten = json.load(f)
            for datei, text, st, bem in daten.get('zeilen', []):
                zeilen[(datei, text)] = (st, bem)
            for datei, zust, st, bem in daten.get('seiten', []):
                seiten[datei] = (zust, st, bem)
            continue
        try:
            m = load_workbook(pfad, data_only=True)
        except Exception as e:      # keine Excel-Datei: das meldet schon das Einlesen
            print(f'{pfad}: nicht lesbar, Stand nicht uebernommen ({e})', file=sys.stderr)
            continue
        if 'Texte' in m.sheetnames and 'Seiten' in m.sheetnames:       # altes Format
            t = m['Texte']
            kopf = [c.value for c in t[1]]
            s = {n: kopf.index(n) for n in kopf if n}
            for z in t.iter_rows(min_row=2, values_only=True):
                datei = z[s['Datei']]
                neu, alt = z[s['Text neu']], z[s['Text bisher']]
                text = neu if (neu and not re.search(r'!\s*l(ö|oe)schen\s*!', str(neu), re.I)) else alt
                st = stand_schluessel(z[s['Status']])
                bem = z[s['Bemerkung']]
                if st or bem:
                    zeilen[(datei, schluessel_text(text))] = (st, bem)
            sd = m['Seiten']
            kopf = [c.value for c in sd[1]]
            s = {n: kopf.index(n) for n in kopf if n}
            for z in sd.iter_rows(min_row=2, values_only=True):
                if z[s['Zustaendig']] or z[s['Bemerkung']]:
                    seiten[z[s['Datei']]] = (z[s['Zustaendig']], None, z[s['Bemerkung']])
            continue
        for blatt in m.worksheets:
            kopf = [c.value for c in blatt[1]]
            if 'text' in kopf and 'datei' in kopf and 'original' in kopf:
                s = {k: kopf.index(k) for k in SPALTEN if k in kopf}
                datei = None
                for z in blatt.iter_rows(min_row=2, values_only=True):
                    z = list(z) + [None] * (len(kopf) - len(z))
                    datei = z[s['seite']] if 'seite' in s and z[s['seite']] else (z[s['datei']] or datei)
                    st = stand_schluessel(z[s['stand']])
                    bem = z[s['bemerkung']]
                    if datei and (z[s['text']] or z[s['original']]):
                        # unter dem neuen UND dem alten Text: je nachdem, ob die
                        # Mappe inzwischen eingelesen wurde, steht der eine
                        # oder der andere in der Datei
                        for t in (z[s['original']], z[s['text']]):
                            if t:
                                zeilen[(datei, schluessel_text(t))] = (st, bem)
                        # Mehrere Absaetze in EINER Zelle (Leerzeile dazwischen)
                        # werden beim Einlesen mehrere Absaetze - jeder erbt
                        # Stand und Bemerkung der Zelle.
                        teile = re.split(r'\n\s*\n', str(z[s['text']] or '').replace('\r', ''))
                        if len(teile) > 1:
                            for t in teile:
                                if t.strip():
                                    zeilen.setdefault((datei, schluessel_text(t)), (st, bem))
            elif kopf and kopf[0] == 'inhalt':
                for z in blatt.iter_rows(min_row=2, values_only=True):
                    if len(z) > 9 and z[9]:
                        seiten[z[9]] = (z[6], stand_schluessel(z[7]), z[8])
    zeilen = {k: v for k, v in zeilen.items() if v[0] or v[1]}
    seiten = {k: v for k, v in seiten.items() if v[0] or v[1] or v[2]}
    return zeilen, seiten


# ---------------------------------------------------------------------------
# Eine Mappe
# ---------------------------------------------------------------------------
# Die Adresse der Website fuer die Links "auf der Website ansehen". In
# hugo.toml steht localhost (fuers Arbeiten am eigenen Rechner); die echte
# Adresse gibt hugo.yml beim Veroeffentlichen mit --basis-url mit. Das hier
# ist nur der Rueckfall, wenn die Mappe am eigenen Rechner entsteht.
LIVE_URL = 'https://kroeppster.github.io/nc-wiki/'
REDAKTION_ORDNER = 'https://github.com/Kroeppster/nc-wiki/tree/main/redaktion'


def basis_url_lesen(projekt):
    try:
        with open(os.path.join(projekt, 'hugo.toml'), encoding='utf-8') as f:
            m = re.search(r'^baseURL\s*=\s*["\']([^"\']+)', f.read(), re.M)
    except OSError:
        m = None
    url = m.group(1) if m else ''
    return LIVE_URL if (not url or 'localhost' in url or '127.0.0.1' in url) else url


def nicht_oeffentlich(seiten):
    """Pfade (innen) der Seiten, die nicht in eine veroeffentlichte Mappe
    gehoeren: Entwuerfe und passwortgeschuetzte Seiten samt allem darunter
    (Mitgliederbereich, Alpha). Die Mappen liegen sonst frei lesbar auf der
    Website - und die Texte hinter dem Passwort gleich mit."""
    gesperrt = set()
    for s in seiten:
        k = s['kopf']
        if k.get('draft') is True or k.get('geschuetzt') is True:
            gesperrt.add(s['innen'])
    ordner = {i[:-len('_index.md')] for i in gesperrt if i.endswith('_index.md')}
    return {s['innen'] for s in seiten if s['innen'] in gesperrt
            or any(o and s['innen'].startswith(o) for o in ordner)}


def mappe_erzeugen(projekt, sprache, ziel, stand_zeilen, stand_seiten, oeffentlich=False, basis_url=None):
    L = T[sprache]
    basis_url = basis_url or basis_url_lesen(projekt)
    eigene = tb.seiten(projekt, sprache)
    deutsch = {s['innen']: s for s in tb.seiten(projekt, 'de')} if sprache != 'de' else {}
    if oeffentlich:
        weg = nicht_oeffentlich(eigene) | nicht_oeffentlich(deutsch.values())
        eigene = [s for s in eigene if s['innen'] not in weg]
        deutsch = {i: s for i, s in deutsch.items() if i not in weg}
    eigene_nach_pfad = {s['innen']: s for s in eigene}

    # Welche Seiten, in welcher Reihenfolge? Die deutsche Reihenfolge gibt
    # den Takt vor - so stehen fehlende Uebersetzungen an der Stelle, an die
    # sie gehoeren, und nicht gesammelt am Ende.
    if sprache == 'de':
        liste = [(s, None) for s in eigene]
    else:
        liste = []
        for innen, de in deutsch.items():
            if innen in eigene_nach_pfad:
                liste.append((eigene_nach_pfad[innen], de))
            elif innen.startswith('alpha/') or (innen.startswith('ems/erfahrungsberichte/')
                                                and not innen.endswith('_index.md')):
                continue        # Werkbank und fremde Erfahrungsberichte nicht uebersetzen
            else:
                liste.append((None, de))
        for s in eigene:
            if s['innen'] not in deutsch:
                liste.append((s, None))

    mappe = Workbook()
    mappe.calculation.fullCalcOnLoad = True
    anleitung = mappe.active
    anleitung.title = L['anleitung']
    inhalt = mappe.create_sheet(L['inhalt'])

    vergeben = {L['anleitung'].lower(), L['inhalt'].lower()}
    berichte_gruppen, blaetter = [], []
    for seite, de in liste:
        innen = (seite or de)['innen']
        zeilen = zeilen_fuer_seite(sprache, seite, de, projekt)
        if innen.startswith('ems/erfahrungsberichte/') and not innen.endswith('_index.md'):
            berichte_gruppen.append((seite, de, zeilen))
            continue
        blaetter.append((seite, de, zeilen))

    # Die Erfahrungsberichte kommen mit ihrer Uebersichtsseite auf EIN Blatt:
    # zuerst die Uebersicht, dann alle Berichte, jeder mit seiner grauen
    # Seiten-Zeile. Gibt es (auf Franzoesisch etwa) keine Uebersichtsseite,
    # stehen die Berichte allein auf dem Blatt.
    uebersicht = next((i for i, (s_, d_, _) in enumerate(blaetter)
                       if (s_ or d_)['innen'] == 'ems/erfahrungsberichte/_index.md'), None)
    if berichte_gruppen:
        if uebersicht is None:
            blaetter.append(('berichte', None, None))
        else:
            blaetter[uebersicht] = ('berichte', blaetter[uebersicht], None)

    inhalt_zeilen = []
    for seite, de, zeilen in blaetter:
        if seite == 'berichte':
            gruppen = ([de] if de else []) + berichte_gruppen
            name = L['berichte']
            vergeben.add(name.lower())
            _, letzte = seitenblatt(mappe, sprache, name, FARBE['berichte'], gruppen, stand_zeilen,
                                    basis_url, L['inhalt'])
            alle = [z for g in gruppen for z in g[2]]
            if de:
                inhalt_zeilen.append((de[0] or de[1], de[0], name, letzte, alle,
                                      L['berichte_zusatz'].format(n=len(berichte_gruppen)), de[2]))
            else:
                inhalt_zeilen.append((None, None, name, letzte, alle,
                                      L['berichte_zusatz'].format(n=len(berichte_gruppen)), None))
            continue
        ziel_seite = seite or de
        farbe = FARBE.get(ziel_seite['bereich'], WEITERE)
        name = blattname(ziel_seite, vergeben)
        _, letzte = seitenblatt(mappe, sprache, name, farbe, [(seite, de, zeilen)], stand_zeilen,
                                basis_url, L['inhalt'])
        inhalt_zeilen.append((ziel_seite, seite, name, letzte, zeilen, '', zeilen))

    inhaltsblatt(inhalt, sprache, inhalt_zeilen, stand_seiten)
    anleitungsblatt(anleitung, sprache, basis_url)
    # Verzeichnis aller Seiten: Fehlt beim Einlesen eine davon (Zeilen oder
    # Blatt geloescht), wird das gemeldet statt stillschweigend uebergangen.
    v = mappe.create_sheet(VERZEICHNIS)
    v.sheet_state = 'veryHidden'
    v.append(['datei', 'summe', 'sprache'])
    for _, _, _, _, zeilen, _, _ in inhalt_zeilen:
        for z in zeilen:
            if z['art'] == 'seite':
                v.append([z['datei'], z['summe'], sprache])
    mappe.active = 1
    mappe.save(ziel)
    return dict(blaetter=len(inhalt_zeilen),
                seiten=sum(1 for s, d, z in blaetter if s != 'berichte') + len(berichte_gruppen)
                + sum(1 for s, d, z in blaetter if s == 'berichte' and d),
                neu=sum(1 for s, d, z in blaetter if s is None))


def inhaltsblatt(b, sprache, eintraege, stand_seiten):
    L = T[sprache]
    b.sheet_properties.tabColor = '1F3864'
    # Versteckte Schluesselzeile: so erkennt --uebernehmen das Blatt wieder
    for i, k in enumerate(['inhalt', '', '', '', '', '', 'zustaendig', 'stand', 'bemerkung', 'datei'], start=1):
        b.cell(row=1, column=i, value=k)
    b.row_dimensions[1].hidden = True
    t = b.cell(row=2, column=1, value=L['titel'])
    t.font = Font(name=SCHRIFT, bold=True, size=16, color='1F3864')
    for i, name in enumerate(L['inhalt_kopf'], start=1):
        z = b.cell(row=4, column=i, value=name)
        z.font = Font(name=SCHRIFT, bold=True, color='FFFFFF', size=10)
        z.fill = KOPF
    for sp, w in zip('ABCDEFGHI', (18, 42, 40, 13, 13, 22, 16, 13, 30)):
        b.column_dimensions[sp].width = w
    b.column_dimensions['J'].hidden = True
    b.freeze_panes = 'A5'
    normal = Font(name=SCHRIFT, size=10)
    link = Font(name=SCHRIFT, size=10, color='0563C1', underline='single')
    r = 5
    for ziel, seite, name, letzte, zeilen, zusatz, eigene_zeilen in eintraege:
        q = zitat_name(name)
        H, B, G, I = SP['nr'], SP['text'], SP['original'], SP['datei']
        e, l = ERSTE_ZEILE, letzte + 400
        aend = (f'=SUMPRODUCT(({q}!${H}${e}:${H}${l}<>"")*NOT(EXACT({q}!${B}${e}:${B}${l},{q}!${G}${e}:${G}${l})))'
                f'+COUNTIFS({q}!${H}${e}:${H}${l},"",{q}!${I}${e}:${I}${l},"",{q}!${B}${e}:${B}${l},"<>")')
        if ziel is None:        # nur Erfahrungsberichte, ohne Uebersichtsseite
            werte = [L['bereiche'].get('ems', 'EMS'), f'{name} {zusatz}', '', aend, '', '',
                     None, None, None, '']
        else:
            bereich = L['bereiche'].get(ziel['bereich'], L['weitere'])
            hat_b = any(z['art'] == 'beschreibung' and z.get('text') for z in eigene_zeilen)
            zeilen = eigene_zeilen
            if sprache == 'de':
                ueb = ''
            elif seite is None:
                ueb = L['neu_anlegen']
            else:
                fehlen = sum(1 for z in zeilen if z.get('nr') == '' and z.get('vorlage') and not z.get('_gesperrt'))
                ueb = (L['absatz_fehlt'] if fehlen == 1 else L['absaetze_fehlen'].format(n=fehlen)) \
                    if fehlen else L['vorhanden']
            alt = stand_seiten.get(zeilen[0]['datei'], (None, None, None))
            werte = [bereich, '  ' * max(0, ziel['tiefe'] - 1) + ziel['titel'] + (f' {zusatz}' if zusatz else ''),
                     (seite or {}).get('adresse', ''), aend, L['ja'] if hat_b else L['fehlt_wort'], ueb,
                     alt[0], L['stand'][STAND_SCHLUESSEL.index(alt[1])] if alt[1] else None, alt[2],
                     zeilen[0]['datei']]
        for i, w in enumerate(werte, start=1):
            c = b.cell(row=r, column=i, value=w)
            c.font = normal
        seite_zelle = b.cell(row=r, column=2)
        seite_zelle.hyperlink = f'#{q}!A1'
        seite_zelle.font = link
        if ziel is not None and not hat_b:
            b.cell(row=r, column=5).fill = ROT
        if sprache != 'de' and seite is None and ziel is not None:
            b.cell(row=r, column=6).fill = GRUEN
        for sp in (7, 8, 9):
            b.cell(row=r, column=sp).fill = GELB
        r += 1
    stand = DataValidation(type='list', formula1='"%s"' % ','.join(L['stand']), allow_blank=True)
    b.add_data_validation(stand)
    stand.add(f'H5:H{r}')
    b.cell(row=r + 1, column=1, value=L['zusammen']).font = Font(name=SCHRIFT, bold=True, size=10)
    b.cell(row=r + 1, column=2, value=f'=COUNTA(B5:B{r - 1})&" {L["seiten_wort"]}"').font = normal
    b.cell(row=r + 1, column=4, value=f'=SUM(D5:D{r - 1})').font = Font(name=SCHRIFT, bold=True, size=10)
    b.cell(row=r + 1, column=5, value=f'=COUNTIF(E5:E{r - 1},"{L["fehlt_wort"]}")&" {L["fehlt_wort"]}"').font = normal


def anleitungsblatt(b, sprache, basis_url):
    b.sheet_view.showGridLines = False
    b.column_dimensions['A'].width = 3
    b.column_dimensions['B'].width = 110
    r = 2
    mappe = basis_url.rstrip('/') + f'/redaktion/ncwiki-texte-{sprache}.xlsx'
    for art, text in ANLEITUNG[sprache]:
        text = text.replace('{mappe}', mappe).replace('{ordner}', REDAKTION_ORDNER)
        z = b.cell(row=r, column=2, value=text)
        if art == 'titel':
            z.font = Font(name=SCHRIFT, bold=True, size=16, color='1F3864')
            r += 1
        elif art == 'kopf':
            r += 1
            z = b.cell(row=r - 1, column=2, value=None)
            z = b.cell(row=r, column=2, value=text)
            z.font = Font(name=SCHRIFT, bold=True, size=11, color='1F3864')
        else:
            z.font = Font(name=SCHRIFT, size=10)
            z.alignment = Alignment(wrap_text=True, vertical='top')
            b.row_dimensions[r].height = 14 * (1 + len(text) // 100)
        r += 1
    # Farbschluessel
    r += 1
    L = T[sprache]
    for fuellung, text in ((GELB, L['geaendert']), (GRUEN, L['neu']), (ROT, L['weg'])):
        z = b.cell(row=r, column=2, value=text)
        z.fill = fuellung
        z.font = Font(name=SCHRIFT, size=10)
        r += 1


def stand_speichern(pfad, projekt, zeilen, seiten):
    """Stand, Bemerkungen und Zustaendigkeiten als JSON ablegen
    (redaktion/stand.json). Der Einlese-Workflow schreibt das nach jeder
    hochgeladenen Mappe fort, und die Mappen, die mit der Website
    veroeffentlicht werden, uebernehmen es - so geht beim Hin und Her nichts
    verloren. Eintraege zu Seiten oder Texten, die es nicht mehr gibt,
    fallen dabei weg."""
    import json
    texte = {}

    def vorhanden(datei, text):
        if datei not in texte:
            p = os.path.join(projekt, datei)
            texte[datei] = {schluessel_text(b['text']) for b in tb.bausteine(p)} if os.path.isfile(p) else None
        return texte[datei] is not None and (text is None or text in texte[datei])

    zl = sorted([d, t, st, bem] for (d, t), (st, bem) in zeilen.items() if vorhanden(d, t))
    sl = sorted([d, z, st, bem] for d, (z, st, bem) in seiten.items() if vorhanden(d, None))
    # Eine Zeile je Eintrag: so zeigt der Pull Request lesbar, was sich tut.
    liste = lambda xs: ('[\n' + ',\n'.join('  ' + json.dumps(x, ensure_ascii=False) for x in xs) + '\n ]'
                        if xs else '[]')
    with open(pfad, 'w', encoding='utf-8') as f:
        f.write('{\n "hinweis": "Stand, Bemerkung und Zustaendig aus den Textmappen - gepflegt von '
                '.github/workflows/texte-einlesen.yml, siehe docs/WARTUNG.md 2b. Zeilen: [Datei, '
                'Pruefsumme des Textes, Stand, Bemerkung]. Seiten: [Datei, Zustaendig, Stand, Bemerkung].",\n'
                f' "zeilen": {liste(zl)},\n "seiten": {liste(sl)}\n}}\n')
    return len(zl), len(sl)


def main():
    ap = argparse.ArgumentParser(description='Textlisten erzeugen (eine Mappe je Sprache).')
    ap.add_argument('--sprachen', default='de,fr,it')
    ap.add_argument('--ziel', default=None, help='Ordner fuer die Mappen (Vorgabe: Projektordner)')
    ap.add_argument('--projekt', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--uebernehmen', nargs='*', default=[],
                    help='fruehere Mappen oder stand.json, deren Stand uebernommen wird')
    ap.add_argument('--stand-speichern', metavar='JSON',
                    help='nur den uebernommenen Stand als JSON speichern, keine Mappen erzeugen')
    ap.add_argument('--oeffentlich', action='store_true',
                    help='fuer die Veroeffentlichung: ohne geschuetzte Seiten und Entwuerfe')
    ap.add_argument('--basis-url', help='Adresse der Website (Vorgabe: aus hugo.toml bzw. LIVE_URL)')
    a = ap.parse_args()
    stand_zeilen, stand_seiten = frueheren_stand_lesen([p for p in a.uebernehmen if os.path.exists(p)])
    if a.uebernehmen:
        print(f'Uebernommen: Stand/Bemerkung fuer {len(stand_zeilen)} Zeilen, Zustaendig fuer {len(stand_seiten)} Seiten')
    if a.stand_speichern:
        nz, ns = stand_speichern(a.stand_speichern, a.projekt, stand_zeilen, stand_seiten)
        print(f'{a.stand_speichern}: {nz} Zeilen, {ns} Seiten')
        return
    ziel = a.ziel or a.projekt
    os.makedirs(ziel, exist_ok=True)
    for sprache in a.sprachen.split(','):
        pfad = os.path.join(ziel, f'ncwiki-texte-{sprache}.xlsx')
        e = mappe_erzeugen(a.projekt, sprache, pfad, stand_zeilen, stand_seiten, a.oeffentlich, a.basis_url)
        extra = f', davon {e["neu"]} neu anzulegen' if sprache != 'de' else ''
        print(f'{pfad}: {e["seiten"]} Seiten auf {e["blaetter"]} Blaettern{extra}')


if __name__ == '__main__':
    main()
