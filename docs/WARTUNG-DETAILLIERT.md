# Website pflegen – ausführliche Anleitung

**Deutsch** · [Français](WARTUNG-DETAILLIERT.fr.md) · [Italiano](WARTUNG-DETAILLIERT.it.md)

Die Alltagsaufgaben (Texte, News, PDFs, Bilder, Löschen) stehen in der
**[Kurzanleitung](WARTUNG.md)**. Hier steht alles andere – vom Menü über Startseite,
Team und Design bis zur Technik dahinter. Die meisten Abschnitte gehen im Browser auf
github.com; wo es einen eigenen Rechner oder Programmierkenntnisse braucht, steht das
dabei.

## Inhalt

1. [Aufbau des Projekts](#1-aufbau-des-projekts)
2. [Seiten, Menü und Navigation](#2-seiten-menü-und-navigation)
3. [Textmappen (Excel) im Detail](#3-textmappen-excel-im-detail)
4. [Web-Editor (Pages CMS) im Detail](#4-web-editor-pages-cms-im-detail)
5. [Links, Bausteine und zeitgesteuerte Inhalte](#5-links-bausteine-und-zeitgesteuerte-inhalte)
6. [Startseite](#6-startseite)
7. [Team und neue Saison](#7-team-und-neue-saison)
8. [Unterstützen, Spenden, Sponsoren](#8-unterstützen-spenden-sponsoren)
9. [FAQ, Uniguide, Untertests, Download-Namen](#9-faq-uniguide-untertests-download-namen)
10. [Prüfungsmodus](#10-prüfungsmodus)
11. [Lern-Generatoren und Alpha-Seite](#11-lern-generatoren-und-alpha-seite)
12. [Mitgliederbereich](#12-mitgliederbereich)
13. [Formulare](#13-formulare)
14. [Einstellungen in hugo.toml](#14-einstellungen-in-hugotoml)
15. [Feste Texte (i18n)](#15-feste-texte-i18n)
16. [Design: Farben, Schrift, Logo, Abschnittsliste](#16-design-farben-schrift-logo-abschnittsliste)
17. [Einen ganzen Bereich löschen](#17-einen-ganzen-bereich-löschen)
18. [Automatisierungen (GitHub Actions)](#18-automatisierungen-github-actions)
19. [Die Website prüfen](#19-die-website-prüfen)
20. [Drittdienste und Zugänge](#20-drittdienste-und-zugänge)
21. [Wo hört „nur ausfüllen“ auf?](#21-wo-hört-nur-ausfüllen-auf)

---

## 1. Aufbau des Projekts

Die Website wird mit [Hugo](https://gohugo.io/) aus Textdateien gebaut. Jede Änderung auf
`main` löst einen Bau aus; nach ein bis zwei Minuten ist die neue Fassung auf GitHub Pages
live (`kroeppster.github.io/nc-wiki/`).

| Ordner / Datei | Inhalt | Anfassen? |
| --- | --- | --- |
| `content/de\|fr\|it/` | Alle Seiten, gleiche Struktur je Sprache | ständig |
| `data/*.yaml` | Listen: FAQ, Unis, Untertests, Testablauf, Sponsoren, Download-Namen, Spenden-/Sponsoring-Kontakt, Wortlisten | gelegentlich |
| `assets/downloads/` | PDFs, die automatisch aufgelistet werden | beim Hochladen |
| `assets/images/`, `static/images/` | Bilder (Titelbilder, Logos) bzw. Logo und feste Grafiken | gelegentlich |
| `i18n/de\|fr\|it.yaml` | feste Texte (Knöpfe, Formulare, Ansagen) | selten |
| `hugo.toml` | Einstellungen (Countdown, Analytics, Social Media) | selten |
| `layouts/`, `assets/css/` | Aussehen und Logik | nur mit Kenntnissen |
| `.github/workflows/` | Automatisierungen | nur mit Kenntnissen |
| `redaktion/` | Ablage für hochgeladene Textmappen | beim Hochladen |
| `scripts/` | Hilfsprogramme (Textmappen, Prüfungen, Bilder) | nur mit Kenntnissen |
| `archetypes/`, `docs/vorlage-*.md` | Vorlagen zum Kopieren | als Hilfe |

In jedem Ordner unter `content/` ist **`_index.md`** die Übersichtsseite des Ordners; jede
andere `.md`-Datei ist eine einzelne Seite. Ein neuer Bereich braucht immer zuerst eine
`_index.md` – ohne sie gibt es den Ordner für Hugo nicht.

Jede Datei beginnt mit einem **Seitenkopf** zwischen zwei `---`-Zeilen (Titel,
Beschreibung, Menü, Datum …), danach folgt der Text in Markdown (`**fett**`,
`[Link](/pfad)`, `- ` für Listen, `## ` für Zwischentitel).

**Lokal arbeiten** (nur wer will): Hugo Extended installieren (Version siehe
`.github/workflows/hugo.yml`), dann `npm install` und `hugo server -D` –
die Seite läuft auf http://localhost:1313/. `npm run build` baut wie auf GitHub.

---

## 2. Seiten, Menü und Navigation

### Wichtige Felder im Seitenkopf

| Feld | Wirkung |
| --- | --- |
| `title` | Seitentitel |
| `description` | Text unter dem Titel in Google; höchstens ~160 Zeichen |
| `draft: true` | Seite wird nicht veröffentlicht |
| `date` | bei News und Jahresberichten: Sortierung |
| `featured_image`, `featured_image_alt` | Titelbild, siehe Kurzanleitung 6 |
| `menu` | Menüpunkt, siehe unten |
| `aliases` | alte Adressen, die hierher weiterleiten |
| `downloads` | eigene PDF-Liste (Jahresberichte) |
| `download_ordner` | automatische PDF-Liste aus einem Ordner unter `assets/` |
| `geschuetzt: true` | Passwortschutz, siehe [12](#12-mitgliederbereich) |
| `layout` | besondere Vorlage, z. B. `spenden` |

### Das Menü

Das Hauptmenü setzt sich **nur aus den Seitenköpfen** zusammen – es gibt keine eigene
Menüdatei. Oberste Ebene heute: Startseite, News, EMS, Unterstützer:innen, Über uns,
Kontakt.

```yaml
menu:
  main:
    parent: ueber-uns   # unter welchem Menüpunkt
    weight: 5           # Reihenfolge, kleiner = weiter vorne
    name: "Kurzname"    # optional, sonst gilt der title
```

- `parent` ist der Ordnername des übergeordneten Bereichs (`ems`, `ueber-uns`,
  `unterstuetzer-innen`); ohne `parent` wird die Seite ein Punkt der obersten Ebene.
- `weight` darf auch eine Kommazahl sein (`2.5`), um etwas dazwischenzuschieben.
- Der Menüblock muss in **jeder Sprachfassung** stehen.
- Die Fusszeile hat ein eigenes Menü `legal` (Impressum, Datenschutz …), gleich aufgebaut.
- Untermenüs öffnen per Maus und per Tippen; auf dem Handy nur per Tippen. Dafür ist
  nichts einzustellen.

### Seite umbenennen oder verschieben

Die Adresse ändert sich mit. Damit alte Links weiter funktionieren, am **neuen** Ort:

```yaml
aliases:
  - /alter/pfad/
```

Links innerhalb der Website zeigen danach ins Leere, bis sie angepasst sind – der Bau
nennt jede Stelle.

### Jahresbericht und andere Einzeldokumente

1. PDF hochladen nach `static/downloads/jahresberichte/2027.pdf`.
2. Neue Seite unter `content/de/ueber-uns/jahresberichte/2027.md` (Vorlage:
   `archetypes/jahresbericht.md`):

   ```yaml
   ---
   title: "Jahresbericht 2027"
   date: 2027-01-01
   downloads:
     - path: "downloads/jahresberichte/2027.pdf"   # relativ zu static/
       label: "Jahresbericht 2027 (PDF)"
   ---
   Zwei, drei Sätze zum Jahr.
   ```

   Die Dateigrösse wird automatisch ergänzt. Dasselbe in FR und IT.

### Automatische PDF-Listen

`download_ordner: "downloads/mitglieder"` im Seitenkopf listet alle PDFs aus
`assets/downloads/mitglieder/` auf. Übungsaufgaben, Testsimulationen und Kursskripte
haben ihre Listen fest eingebaut. Schönere Anzeigenamen als den Dateinamen: in
`data/downloads.yaml` (dort steht das Format, mit Übersetzungen).

---

## 3. Textmappen (Excel) im Detail

Ablauf für Redaktion: [Kurzanleitung 2](WARTUNG.md#2-texte-ändern-mit-der-excel-textmappe).

### Wie die Mappen entstehen

`.github/workflows/textmappen.yml` erzeugt nach jeder Änderung auf `main` drei Mappen
(`scripts/texte-ausgeben.py`) und hängt sie an das GitHub-Release **„Textmappen“** – bewusst
nicht auf die Website. Sie enthalten keine Entwürfe und keine passwortgeschützten Seiten.

Aufbau: Blatt „Anleitung“ (in der Sprache der Mappe), Blatt „Inhalt“ (Link zu jeder Seite,
Änderungszähler, fehlende Beschreibungen, Spalten Zuständig/Stand/Bemerkung), danach ein
Blatt je Seite in der Reihenfolge der Navigation. Jedes Seitenblatt ist eine
**Excel-Tabelle** mit der berechneten Spalte „Änderung“ – fügt man in Excel eine Zeile
ein, steht dort automatisch „+ neu“. (LibreOffice, Numbers und Google Tabellen rechnen das
nicht mit; der Text wird trotzdem grün.) Versteckte Spalten merken sich, zu welchem Absatz
eine Zeile gehört.

### Ansicht-Blätter für Startseite und Team

„Startseite – Ansicht“ und „Team – Ansicht“ (orange Lasche) sind wie die Website
aufgebaut: Kopfbereich, Zeitstrahl-Etappen und Kacheln nebeneinander, im Team je Ressort
eine Reihe Karten. Nur die weissen Felder sind beschreibbar (Blattschutz ohne Passwort).

- Team: leere Karte = neue Person, `!Löschen!` im Namen = Person weg, im Ressort-Titel =
  ganzes Ressort weg; unten stehen zwei leere Ressorts für neue bereit.
- Auf FR/IT steht der deutsche Text als Kommentar an der Zelle.
- Das Team jeder Sprache wird in der Mappe dieser Sprache gepflegt.

Code: `scripts/texte_ansicht.py`.

### Uniguide-Blatt

„Uniguide – Ansicht“ zeigt die ganze Tabelle aus `data/unis.yaml`: je Uni eine Zeile,
je Angabe eine Spalte (Name, Kanton, Sprachen, Studiengänge, EMS, Zulassungsverfahren,
Besonderheiten, Studienplätze, Anmeldefrist, Studienbeginn, Semestergebühr, Links, Stand,
Quelle).

- **Grüne Spaltenköpfe** (Kanton, Zulassungsverfahren, Besonderheiten, Anmeldefrist,
  Studienbeginn, Semestergebühr) sind Texte und gelten nur für die Sprache der Mappe.
  Fehlt eine Übersetzung, zeigt die Website den deutschen Text.
- **Dunkle Spaltenköpfe** gelten für alle Sprachen und lassen sich in jeder Mappe ändern.
- Mehrere Besonderheiten: je eine pro Zeile in der Zelle. Sprachen mit Komma, in jeder
  Schreibweise („deutsch, français“). EMS: ja / nein / teilweise. Studienplätze: nur die
  Zahl. Links mit `https://`.
- Leere Zelle löscht nichts, `!Löschen!` leert das Feld. Ungültige Eingaben (keine Zahl,
  kein Link …) werden nicht übernommen und im Bericht genannt.
- Beim Einlesen ändert sich in `data/unis.yaml` nur genau das Feld; die Kommentare bleiben.
- Nur eintragen, was auf einer offiziellen Seite steht, und dann „Stand“ und „Quelle“
  mitändern. Eine neue Uni anlegen geht nicht über die Mappe (siehe [9](#9-faq-uniguide-untertests-download-namen)).

Code: `scripts/texte_uniguide.py`.

### Was beim Einlesen passiert

`.github/workflows/texte-einlesen.yml` liest hochgeladene Mappen mit
`scripts/texte-einlesen.py` ein, baut die Website probeweise und eröffnet einen Pull
Request mit Bericht. Jede geänderte Seite wird aus den Zeilen ihres Blatts neu
zusammengesetzt; unveränderte Absätze bleiben zeichengenau, unveränderte Seiten werden
nicht angefasst. Lieber eine Meldung als ein falscher Text:

| Fall | Was passiert |
| --- | --- |
| Seite wurde inzwischen anderswo geändert | Seite wird übersprungen, Rest kommt an – Änderung in frischer Mappe neu eintragen |
| Dieselbe Mappe zweimal hochgeladen | schadet nicht („schon übernommen“) |
| Leere Zelle / gelöschte Zeile | Absatz bleibt – gelöscht wird nur mit `!Löschen!` (auch `!Supprimer!`, `!Eliminare!`) |
| Tabellen, Bausteine, Code (grau, kursiv) | bleiben unverändert; die ändert man in der Datei |
| Blatt sortiert | Seite bleibt, Meldung |
| Zellen statt ganzer Zeilen verschoben | wird an der Formel in „Änderung“ erkannt; die Seite wird so übernommen, wie sie **zu sehen** ist, jeder weggefallene Absatz steht im Bericht |
| Zeile aus anderer Seite hineinkopiert, graue Seiten-Zeile gelöscht | erkannt und gemeldet |
| Titel und alle Texte mit `!Löschen!` | Seite wird gelöscht |
| Seite löschen, auf die noch verlinkt wird | wird gelöscht, Bericht nennt die Links (sonst wird der Bau rot) |
| Übersichtsseite (`_index.md`) löschen | nur, wenn alle Seiten darunter ebenfalls markiert sind |
| Französische/italienische Seite fehlt | Blatt ausfüllen → Seite wird mit dem Kopf der deutschen Seite angelegt |
| Feld „Neue Saison“ im Team-Blatt | Saisonwechsel wie [7](#7-team-und-neue-saison) |

„Stand“, „Bemerkung“ und „Zuständig“ gehen nicht auf die Website; der Workflow speichert
sie in `redaktion/stand.json` (je Text nur eine Prüfsumme), die nächste Mappe hat sie
wieder.

### Einmalig einzustellen

*Settings → Actions → General → Workflow permissions → „Allow GitHub Actions to create and
approve pull requests“*. Sonst schlägt der letzte Schritt fehl; der Bericht steht dann in
der Zusammenfassung des Laufs. Ein vom Workflow eröffneter Pull Request bekommt keinen
Bau-Haken von `hugo.yml` (GitHub lässt Workflows keine Workflows starten) – deshalb baut
`texte-einlesen.yml` selbst und schreibt ✅/❌ in den Pull Request.

### Am eigenen Rechner

```bash
pip install openpyxl pyyaml
python3 scripts/texte-ausgeben.py --uebernehmen redaktion/stand.json   # drei Mappen
python3 scripts/texte-einlesen.py ncwiki-texte-de.xlsx --probe         # nur zeigen
python3 scripts/texte-einlesen.py ncwiki-texte-de.xlsx                 # schreiben
```

`--sprachen fr` erzeugt nur eine Mappe. Mappen gehören nicht ins Repo (`.gitignore`).

### Wer an den Skripten etwas ändert

Die Zerlegung einer Seite in Absätze steht genau einmal, in `scripts/texte_bausteine.py`.
Danach immer **`python3 scripts/texte-mappe-pruefen.py`**: Es arbeitet in einer Kopie des
Projekts wie eine Redaktorin (ändern, einfügen, verschieben, löschen, Ansicht-Blätter,
neue Saison, Konflikte …), prüft jede Seite und baut die Kopie. Die echten Dateien fasst es
nicht an. Die Formeln der Mappen prüft es in Python nach (Bezüge, Bereiche, keine
Funktionen neuer als Excel 2007). Die Spalte „Text“ ist als Text formatiert, sonst hielte
Excel „- Punkt“ für eine Formel.

---

## 4. Web-Editor (Pages CMS) im Detail

Bedienung: [Kurzanleitung 3](WARTUNG.md#3-kleine-korrekturen-im-web-editor).

### Einrichten (einmalig)

1. Auf [app.pagescms.org](https://app.pagescms.org) mit GitHub anmelden.
2. *Install GitHub App* und das Repository `Kroeppster/nc-wiki` freigeben.
3. Repository öffnen, Branch `main`. Die Einstellungen stehen in
   [`.pages.yml`](../.pages.yml).
4. Mitschreibende unter *Collaborators* per E-Mail einladen – sie brauchen kein
   GitHub-Konto.

### Was drin ist – und was absichtlich nicht

Je Sprache: **Seiten** (ganzer Baum), **News**, **Erfahrungsberichte**. Anlegen geht,
umbenennen und löschen nicht (das bricht Links).

Nicht im Editor: **Mitgliederbereich** und **Alpha** (ein erklärender Kommentar im
Seitenkopf ginge verloren), **`data/*.yaml`** (voller Kommentare, die der Editor löschen
würde), **Bilder hochladen**.

### Was der Editor an Dateien ändert

Beim Speichern schreibt Pages CMS die ganze Datei neu: Anführungszeichen im Kopf fallen
weg, lange Texte werden umbrochen, Listen untereinander geschrieben, `&` wird `&amp;`,
Tabellen neu ausgerichtet. Für Hugo ist das dasselbe. `scripts/editor-rundlauf.mjs`
speichert jede Seite so, wie Pages CMS es tut, baut beide Fassungen und vergleicht –
zuletzt 440 von 440 Seiten gleich. Die Textmappen kommen mit den umbrochenen Texten
zurecht.

### Wer `.pages.yml` ändert

- **`settings.content.merge: true` muss bleiben.** Sonst schreibt Pages CMS nur die dort
  genannten Felder zurück – Menü, Reihenfolge, Tags und die Startseite (`hero`, `weg`,
  `material`) wären nach dem ersten Speichern weg.
- Danach `node scripts/editor-rundlauf.mjs` (braucht einmalig ein paar npm-Pakete in
  einem eigenen Ordner, siehe Kopf des Skripts).
- Unbekannte Schlüssel lehnt Pages CMS ab; wiederverwendete Felder stehen deshalb als
  YAML-Anker (`&titel`, `*titel`) beim Deutschen.

---

## 5. Links, Bausteine und zeitgesteuerte Inhalte

### Interne Links

Normale Markdown-Links mit Pfad, ohne Sprache und ohne `/nc-wiki/`:
`[Uniguide](/ems/uniguide)`. Der Render-Hook
`layouts/_default/_markup/render-link.html` macht daraus die richtige Adresse in der
Sprache der Seite und bricht den Bau ab, wenn es das Ziel nicht gibt.

**Kein `{{< ref >}}` und keine anderen Shortcodes im Text.** Der Web-Editor schreibt sie
beim Speichern kaputt – schon, wenn jemand auf der Seite nur ein Komma ändert.

### Bausteine

Als Code-Block mit der Sprache `baustein` (`layouts/_default/_markup/render-codeblock-baustein.html`):

| Name | Was | Daten |
| --- | --- | --- |
| `testablauf` | Tabelle Tagesablauf | `data/testablauf.yaml` |
| `team-leitung` | Karten des Leitungsteams | `ressorts:` im Kopf der Team-Seite |
| `fakten-generator` | Fakten-Generator | `data/fakten-generator/` |
| `figuren-generator` | Figuren-Generator | – |
| `sponsoring-kontakt` | E-Mail-/Telefon-Knopf | `data/sponsoring.yaml` |

Ein Tippfehler im Namen bricht den Bau ab. Neue Bausteine: Partial unter
`layouts/partials/bausteine/` anlegen und den Namen in die Liste `$erlaubt` im Render-Hook
aufnehmen.

### Etwas erst ab einer bestimmten Uhrzeit zeigen

```
{{< reveal-at when="2027-02-10T22:00:00+01:00" >}}
[Jetzt anmelden](https://...)
{{< /reveal-at >}}
```

Zeitzone ist Pflicht (`+01:00` Winter, `+02:00` Sommer); ohne gültiges Datum bleibt der
Inhalt versteckt. Das Verstecken passiert nur im Browser – nicht für Geheimes geeignet.
**Achtung:** Das ist ein Shortcode. Die Seite danach nicht im Web-Editor speichern, und den
Block nach dem Termin wieder entfernen.

---

## 6. Startseite

Die Startseite wird aus dem **Seitenkopf** von `content/de|fr|it/_index.md` gebaut
(Vorlage `layouts/index.html`). Texte am einfachsten über das Blatt „Startseite – Ansicht“
der Textmappe; sonst in allen drei Dateien.

### Reihenfolge der Abschnitte

Hero → News → „Was du wann brauchst“ (Zeitstrahl) → „Das Material selbst“ → die acht
Untertests → Mission → Marken-Band → Spendenaufruf. Umsortieren: die `<section>`-Blöcke
in `layouts/index.html` verschieben und dabei die Klasse `section-surface` so verteilen,
dass sich helle und getönte Abschnitte abwechseln.

### Hero

```yaml
hero:
  bild: "testsimulationen/testsimulation-2023.jpg"   # relativ zu assets/images/
  bild_alt: "Voller Hörsaal während einer Testsimulation …"
```

`bild_alt` ist Pflicht, sobald ein Bild gesetzt ist (in jeder Sprache übersetzt). Ohne
`bild` erscheint kein Foto. Das Foto soll zeigen, dass hier Echtes passiert – kein
Symbolbild.

### Zeitstrahl (`weg:`)

```yaml
weg:
  eyebrow: "Von der Anmeldung bis zum Resultat"
  heading: "Was du wann brauchst"
  etappen:
    - wann: "Bis 15. Februar"
      titel: "Entscheiden und anmelden"
      text: "…"
      mittel:
        - titel: "Uniguide"
          url: "ems/uniguide/"
```

Die Termine folgen dem offiziellen Zeitplan von swissuniversities. Im Zeitstrahl stehen
keine Zahlen. Die vier Teile einer Etappe müssen im Template direkte Kinder von
`.weg-etappe` bleiben (CSS `subgrid` richtet sie über alle Spalten aus; ein zusätzliches
`<div>` zerstört das lautlos).

### Material-Kacheln (`material:`)

```yaml
material:
  items:
    - key: uebungsaufgaben        # nicht übersetzen
      titel: "Übungsserien"
      zahlen: ["uebungen"]        # füllt {1}
      text: "{1} Serien zu allen acht Untertests, mit Lösungen."
```

Erlaubte `key`: `uebungsaufgaben`, `testsimulationen`, `vorbereitungskurse`, `community`.

**Zahlen nie von Hand schreiben.** `layouts/partials/angebot-zahlen.html` zählt bei jedem
Bau neu: Übungsserien ohne Lösungs-PDFs, Testsimulationen als Jahrgänge, Unis und Fragen
aus den Datendateien, Erfahrungsberichte je Sprache. In den Text kommt `{1}`, `{2}` …

Welche Bilder eine Kachel zeigt, steht in `layouts/partials/material-grid.html` (Block
`$quellen`). PDF-Seiten werden immer **ganz** gezeigt (`papier: true`, weisser Grund,
`object-fit: contain`) – die Quell-PDFs sind teils A4, teils US Letter. Fotos dürfen
angeschnitten werden. Ein Name mit Endung wird unter `assets/images/` gesucht, einer ohne
unter `assets/images/angebot/`. Neu erzeugen mit `python3 scripts/angebot-bilder-erzeugen.py`
(braucht `pip install pymupdf`; oben im Skript stehen PDF und Seite je Bild). Die
Discord-Karte ist bewusst kein nachgemachter Screenshot.

Etappen und Kacheln entfernen oder umsortieren: Eintrag in allen drei Dateien löschen bzw.
verschieben. Eine ganz neue Kachel braucht einen Eintrag in `$quellen` (Entwickler-Schritt).

Achtung im Template: Ein Hugo-Kommentar `{{/* */}}` innerhalb eines `dict` bricht den Bau.

---

## 7. Team und neue Saison

### Leitungsteam

Steht im Kopf von `content/<sprache>/ueber-uns/team/_index.md` unter `ressorts:`; der
Baustein `team-leitung` macht daraus die Karten.

```yaml
ressorts:
  - titel: "Präsidium"
    mitglieder:
      - name: "Vorname Nachname"
        rolle: "Co-Präsident"
        foto: "team/vorname-nachname.jpg"   # optional, relativ zu assets/images/
```

Reihenfolge der Blöcke = Reihenfolge auf der Seite. Ohne Foto erscheint ein farbiger
Kreis mit Initialen. Namen sind in allen Sprachen gleich, `titel` und `rolle` werden
übersetzt. Am einfachsten über das Blatt „Team – Ansicht“ der Textmappe.

### Neue Saison

Zwei Wege, beide machen dasselbe (`scripts/texte_saison.py`):

- in der Textmappe, Blatt „Team – Ansicht“, das Feld „Neue Saison starten“ ausfüllen und
  hochladen, **oder**
- auf GitHub *Actions → Neue Saison starten → Run workflow*, Saison eintragen (ergibt
  einen Pull Request).

In allen drei Sprachen wandert der Abschnitt „Team Saison …“ samt einer Liste des
Leitungsteams ins Archiv (`ueber-uns/archiv/`, zuoberst unter „Frühere Saisons“), und auf
der Team-Seite beginnt die neue Saison mit einem Platzhalter-Satz. Das Leitungsteam
selbst bleibt stehen; wer wechselt, wird danach geändert. Ein zweiter Lauf mit derselben
Saison tut nichts.

### Archiv

`content/<sprache>/ueber-uns/archiv/_index.md` ist normaler Text: frühere Saisons,
ehemalige Verantwortliche, ältere Kursskripte (automatische Liste aus
`assets/downloads/archiv-kursskripte/`) und darunter die früheren News
(`ueber-uns/archiv/news/`).

---

## 8. Unterstützen, Spenden, Sponsoren

### „Jetzt unterstützen“

`content/<sprache>/unterstuetzer-innen/jetzt-unterstuetzen.md` hat `layout: spenden`
(`layouts/_default/spenden.html`):

- die **erste** `##`-Überschrift mit ihrem Text steht links neben dem grossen TWINT-Code,
  darunter der Knopf „Spenden mit Überweisung“;
- die **zweite** `##`-Überschrift bildet den Sponsoring-Teil mit dem Knopf „Weitere
  Informationen“ (zur Seite Sponsoren).

Die Texte bleiben also normaler Seitentext (Mappe, Editor). Knopf-Beschriftungen:
`i18n`, Präfix `spenden_`. TWINT-Code austauschen: `assets/images/unterstuetzen/twint-qr.png`
ersetzen (quadratisch). Er steht auch im Dunkelmodus auf Weiss, damit die App ihn liest.
Die Kontoangaben stehen auf `unterstuetzer-innen/spenden-ueberweisung.md`.
Kartenzahlung gibt es noch nicht.

### Sponsoren-Seite

`unterstuetzer-innen/sponsoren.md` ist normaler Text; am Ende steht der Baustein
`sponsoring-kontakt`. E-Mail und Telefon in `data/sponsoring.yaml` – ist `telefon` leer,
erscheint kein Telefon-Knopf.

### Sponsoren-Logos

Die Logos auf „Unterstützer:innen“ kommen aus `data/sponsors.yaml` (in der Datei Feld für
Feld erklärt):

1. Logo nach `assets/images/sponsors/` hochladen (SVG bevorzugt).
2. Eintrag ergänzen:

   ```yaml
   - name: "Firmenname"
     logo: "dateiname.svg"
     website: "https://beispiel.ch/"
   ```

Reihenfolge in der Datei = Reihenfolge der Kacheln. Entfernen: Eintrag löschen. Dunkle
Logos bekommen automatisch einen hellen Hintergrund-Chip (`.sponsor-logo`).

---

## 9. FAQ, Uniguide, Untertests, Download-Namen

### FAQ (`data/faq.yaml`)

```yaml
- id: "eindeutige-kurzbezeichnung"
  frage:   { de: "…?", fr: "… ?", it: "…?" }
  antwort: { de: "…",  fr: "…",   it: "…" }
```

Reihenfolge in der Datei = Reihenfolge auf der Seite. Die Frage „Welche Untertests gibt
es?“ hängt automatisch die Liste aus `data/subtests.yaml` an (`dynamic: subtests`); der
Satz davor („9 Untertests“) steht fest in der FAQ.

### Uniguide (`data/unis.yaml`)

Eine Datei speist die Tabelle `/ems/uniguide/`, jede Uni-Seite und den Vergleich. Jede Uni
braucht zusätzlich eine fast leere Seite `content/<sprache>/ems/uniguide/<slug>.md` mit
`title` und `uni_slug`. Bearbeiten am einfachsten über das Blatt „Uniguide – Ansicht“ der
Textmappe ([3](#3-textmappen-excel-im-detail)). `kanton`, `auswahlverfahren` und `besonderheiten` stehen je Sprache
(`de:`/`fr:`/`it:`), die Namen der Unterrichtssprachen kommen aus `i18n` (`sprache_…`).

**Nichts schätzen.** Felder wie `website_medizin`, `anmeldefrist`, `studienbeginn`,
`semestergebuehr`, `studienplaetze` bleiben `null`, bis der Wert auf einer offiziellen
Seite steht – dann `stand` (Datum) und `quelle` (Link) mitändern. Leere Felder erscheinen
nicht; stattdessen zeigt die Uni-Seite den Kasten „Diese Angaben fehlen noch“.

`berichte_ort` muss genau dem `ort:` der Erfahrungsberichte entsprechen; dann erscheinen
die drei neuesten Berichte auf der Uni-Seite. Im Vergleich lassen sich bis zu vier Unis
nebeneinander stellen (`var MAX = 4` in `layouts/partials/uniguide-table.html`; weitere
Zeilen im Abschnitt „VERGLEICHSANSICHT“ – Entwickler-Schritt).

### Untertests (`data/subtests.yaml`)

Speist die Untertest-Kacheln. **Reihenfolge = Reihenfolge am Testtag** und muss zu
`data/testablauf.yaml` passen. `slug` = Ordnername unter
`content/<sprache>/ems/uebungsaufgaben/`; `number` wird nicht angezeigt. Beim Umsortieren
auch das `weight` der Übungsseiten nachziehen. Die Website hat 8 Übungsseiten, weil
„Figuren & Fakten lernen“ zwei offizielle Untertests zusammenfasst – der echte EMS hat 9.

Ein zusätzlicher Hinweis bei den Downloads einer Übungsseite:
`downloads_notice: "Neues Layout!"` im Kopf (je Sprache).

### Download-Namen (`data/downloads.yaml`)

Überschreibt den automatisch aus dem Dateinamen gebauten Namen eines PDFs, mit
Übersetzungen. Beispiele stehen in der Datei.

---

## 10. Prüfungsmodus

`/ems/pruefungsmodus/`: liest Anweisungen vor, zeigt eine Vollbild-Uhr und sagt „Stopp“ –
für einen Untertest oder den ganzen Testtag ohne Pausen. Die Aufgaben kommen aus den PDFs.

### Zeiten und Reihenfolge

Alles in **`data/testablauf.yaml`**: Blöcke in der Reihenfolge des Testtags mit
`minuten`, Aufgabenzahl, Punkten und Namen in drei Sprachen. Die Datei speist die Tabelle
auf `/ems/` (Baustein `testablauf`), den Prüfungsmodus und die Vorgabezeiten der
Generatoren. Die Gesamtzeit wird zusammengezählt. **Sorgfältig ändern** – eine falsche
Zahl heisst monatelanges Üben mit falscher Dauer.

### Eigener Ablauf

- **Normal:** Untertests und Aufgabenzahl wählen; die Zeit rechnet sich im Tempo des
  echten EMS (7 Aufgaben „Muster zuordnen“ = 6:13). Intern wird in **Sekunden** gerechnet.
- `aufgaben_fest: true` (Figuren/Fakten einprägen): dort ist die **Zeit** einstellbar
  statt der Anzahl.
- **Expertenmodus:** Minuten und Pausen frei. Ein geteilter Link, der das braucht, schaltet
  ihn selbst ein. Zeitformat im Link `6m13` (reine Zahlen gelten als Minuten, alte Links
  bleiben gültig).
- Die Zusammenstellung lässt sich als Link teilen; nichts wird auf einem Server
  gespeichert.

### Ansagen

Texte in `i18n/*.yaml`, Präfix `pm_` – kurz, ohne Klammern und Abkürzungen, sie werden
gesprochen. Anrede **Sie**, wie eine Aufsichtsperson. Für DE und FR liegen 15 Aufnahmen
unter `assets/audio/pruefungsmodus/<sprache>/` (Liste im README dort; FR-Stimme CC-BY 4.0,
Namensnennung im README); eine Aufnahme hat Vorrang vor der Sprachausgabe des Browsers.
Italienisch liest das Gerät vor. Nach einer Änderung an einem `pm_`-Text die Aufnahme
löschen oder mit `scripts/ansagen-erzeugen.py` neu erzeugen. Echte Aufnahmen aus dem
Verein: Datei mit gleichem Namen überschreiben.

### Technisches, das man kennen muss

- Die Uhr merkt sich einen **Endzeitpunkt** statt Sekunden zu zählen (Browser bremsen
  Hintergrund-Tabs).
- Wake-Lock hält den Bildschirm an; Vollbild ist nur Zugabe.
- Zwischen Blöcken wird nicht gewartet, eine Endzeit wird nie angezeigt, die Pause ist
  als „nur zum Üben“ beschriftet.
- Geänderte Aufgabenzahl/Zeit → der Satz wird vorgelesen statt der Aufnahme (die nennt die
  echten Werte). `{dauer}` nutzt `pm_dauer_min`/`pm_dauer_min_sek`.
- `safeJS` in `layouts/partials/pruefungsmodus.html` nicht entfernen – sonst bleibt die
  Seite stumm.

---

## 11. Lern-Generatoren und Alpha-Seite

Material für „Figuren & Fakten lernen“ ist nur einmal brauchbar – deshalb würfeln zwei
Generatoren immer neue Sets. Beide lassen sich am Bildschirm mit Uhr durchspielen oder als
sechsseitiges Testheft drucken (Anleitung, Einprägeseite, Fragen, Antwortbogen,
Lösungsblatt; Kopfzeile, Seitenzahl, CC-BY-NC-Signet). Vorgabezeiten und die Pause (die
echte Lücke am Testtag) kommen aus `data/testablauf.yaml`.

### Heftformat

Masse aus dem privaten **NCWiki-Formatierungstool** (`vorlage/ems.typ`). Gemeinsamer Rahmen:
`layouts/partials/bausteine/ems-heft.html`, Stile in `assets/css/style.css`
(„EMS-Heft“). Ein Mass zuerst im Tool ändern, dann dieselbe Zahl übernehmen. **Nur das
Format übernehmen, nie Inhalte** – das Tool ist privat, die Website öffentlich. Vor
Änderungen an den Druckregeln den Kommentar bei `@media print` lesen (Heftseiten kommen
in einen eigenen Behälter unter `<body>`; Regeln hängen an `body.fg-druckt`).

### Fakten-Generator

Wortlisten in `data/fakten-generator/<sprache>.yaml` (aktuell nur `de.yaml`; sobald
`fr.yaml`/`it.yaml` existiert, erscheint er dort von selbst). Kategorien nicht auflösen: Eine
echte Serie gibt jeder Altersgruppe drei Berufe aus **einem** Feld und drei Krankheiten aus
**drei** Arten. Fragen entstehen aus Satzvorlagen (`fragen`), dazu `namensgruppen`,
`dativ`, `nicht_attributiv`. `scripts/fakten-listen-auslesen.py` liest Wörter aus den PDFs,
überschreibt die YAML aber nicht. Offen: Kategorien noch nicht menschlich freigegeben; ~40
statt ~80 Einträge je Kategorie.

### Figuren-Generator

Braucht keine Datendatei, Beschriftungen in `i18n` (Präfix `fig_`). Jede **Serie** würfelt
zuerst ihren Stil (Ecken, Zackigkeit, Grösse, Bauart frei/Nabe/Band), die 18 Figuren folgen
ihm – sonst sähen alle Serien gleich aus. Messen statt schätzen:
`python3 scripts/figuren-vergleichen.py 14 [--original <PDF>]` (braucht `pymupdf numpy
scipy pillow`; das offizielle Beispiel-PDF von swissuniversities liegt nicht im Repo).
Vor Änderungen am Zeichnen den Kommentarkopf in
`layouts/partials/bausteine/figuren-generator.html` lesen – dort stehen die bisherigen
Fehler (doppelte Clip-Kennungen, zerfallende Felder, getrennt geglättete Konturen,
Buchstaben im Schwerpunkt, Logo als Figur mitgemessen).

### Alpha-Seite

`content/de/alpha/` ist die Werkbank für neue Funktionen: passwortgeschützt, nirgends
verlinkt, **nur Deutsch**. Pro Funktion ein Abschnitt, der sagt, was zu beurteilen ist.
Ist sie freigegeben, wandert der Baustein auf die echte Seite (dann dreisprachig).

---

## 12. Mitgliederbereich

`content/<sprache>/mitglieder/` – nicht im Menü, beim Veröffentlichen mit Passwort
verschlüsselt (StatiCrypt, `scripts/encrypt-protected-pages.mjs`).

### Was der Schutz leistet

Er hält Suchmaschinen und Zufallsbesuche fern, ist aber **kein Login**: ein gemeinsames
Passwort; die verschlüsselte Seite ist öffentlich und kann offline durchprobiert werden;
**verlinkte PDFs sind nicht geschützt** (wer die Adresse kennt, kann sie laden). Also nur
Internes ohne Schadenspotenzial – keine Personendaten, Kontoauszüge, Bewerbungen.

### Neue geschützte Seite

Wie jede Seite, zusätzlich `geschuetzt: true` im Kopf (in allen drei Sprachen). Das setzt
`noindex`, nimmt die Seite aus Suche, Sitemap und RSS und verschlüsselt sie. PDF-Liste:
`download_ordner: "downloads/mitglieder"`.

### Passwort

- Gilt **zwei Stunden** ab dem letzten Aufruf, für alle Mitgliederseiten und Sprachen
  (`MERKDAUER_MINUTEN` in `scripts/passwort-vorlage.html`). Im Browser liegt ein gesalzener
  Prüfwert, nicht das Passwort. Abmelden: `?staticrypt_logout` an die Adresse hängen.
- **Ändern:** *Settings → Secrets and variables → Actions →* `MITGLIEDER_PASSWORT` →
  neues Passwort (mindestens 16 zufällige Zeichen) → danach *Actions → Deploy Hugo site
  to GitHub Pages → Run workflow*. Neues Passwort in den Passwort-Manager und an die
  Mitglieder. Das `SALZ` im Skript bleibt.
- **Bau rot mit „Kein Passwort gesetzt“:** Secret fehlt – der Bau bricht absichtlich ab,
  statt unverschlüsselt zu veröffentlichen. Bei Pull Requests nur Warnung.
- Lokal: `npm run build && STATICRYPT_PASSWORD='test' npm run schuetzen`, Ergebnis in
  `public/mitglieder/`.

---

## 13. Formulare

Die Website hat keinen Server; Formulare laufen über **Formspree**.

| Formular | Wo | Formspree-ID | Datei |
| --- | --- | --- | --- |
| Kontakt | `/kontakt/` | `mvkpgrpl` | `layouts/partials/contact-form.html` |
| Fehlermeldung Übungsaufgaben | Übungsaufgaben-Seiten | ebenfalls `mvkpgrpl` | `layouts/partials/report-error-general.html` |
| Erfahrungsbericht | `/ems/erfahrungsberichte/` | `xaewqwoj` | `layouts/partials/experience-form.html` |

Fehlermeldungen landen vorläufig im Kontakt-Postfach, mit festem Betreff „Fehlermeldung
Uebungsaufgaben (Website)“ zum Filtern. Eigene Adresse später: nur in
`report-error-general.html` eintragen.

**Die Erfahrungsbericht-Adresse nicht umhängen:** Eine Einsendung löst über
`repository_dispatch` den Workflow `erfahrungsbericht-intake.yml` aus, der Datei und Pull
Request baut (der dafür nötige GitHub-Token ist nur in Formspree hinterlegt).

Das Senden im Hintergrund erledigt ein gemeinsames Skript in
`layouts/partials/footer.html` für alle Formulare mit der Klasse `report-error`. Ein neues
Formular an neuer Stelle ist ein Entwickler-Schritt.

---

## 14. Einstellungen in hugo.toml

Unter `[params]`:

| Feld | Wirkung |
| --- | --- |
| `ems_exam_date = '2027-07-09T08:00:00+02:00'` | Ziel des Countdowns auf der Startseite (Zeitzone Pflicht) |
| `google_analytics_id` | Google Analytics; leer = aus |
| `social_instagram`, `social_discord`, `social_linkedin` | Knöpfe in der Fusszeile; leer = kein Knopf |
| `newsletter_url` | Newsletter-Anmeldung; leer = kein Newsletter-Block |

Google Analytics lädt **nur**, wenn im Cookie-Banner „Akzeptieren“ gewählt wurde. Texte
des Banners: `i18n`, Präfix `cookie_`.

---

## 15. Feste Texte (i18n)

`i18n/de.yaml`, `fr.yaml`, `it.yaml` enthalten alle Texte, die nicht zu einer Seite
gehören: Knöpfe, Formulare, Cookie-Banner, Ansagen, Beschriftungen. Links steht der
Schlüssel, rechts der Text; **alle drei Dateien haben dieselben Schlüssel**. Einen Text
immer in allen drei Dateien ändern. Ein neuer Schlüssel wirkt nur, wenn er in `layouts/`
auch benutzt wird.

---

## 16. Design: Farben, Schrift, Logo, Abschnittsliste

### Farben

Alles in `assets/css/style.css`, oben als Variablen. Es gibt **zwei Paletten**: `:root{…}`
(hell) und `:root[data-theme="dark"]{…}` (dunkel) – eine Farbänderung immer in beiden.

- `--color-signal` ist die Link- und Markenfarbe, `--color-btn-bg` der Hintergrund
  gefüllter Knöpfe. Im Dunkelmodus unterscheiden sie sich absichtlich (heller Text-Link,
  aber genug Kontrast für weisse Knopfschrift) – beide anpassen.
- `--cta-from`/`--cta-to` und `--color-avatar-0…5` stehen nur hell, weil weisser Text
  darauf steht – nie zu hell machen.
- Tiefe: `--shadow-sm|md|lg`, `--glow-*`, `--band-*`, `--color-section-alt`. Schatten sind
  im Dunkelmodus kräftiger.
- Vor jeder Farbänderung Kontrast prüfen („WCAG contrast checker“): Text 4.5 : 1,
  grosse Überschriften 3 : 1, in beiden Modi.

### Schrift

**Poppins** (Überschriften) und **Inter** (Text), selbst ausgeliefert aus `static/fonts/`
(nicht von Google geladen – Datenschutz). Austauschen: `.woff2` dort ablegen **und** den
`@font-face`-Block sowie `--font-display`/`--font-body` anpassen.

### Logo und Favicon

Logo: `static/images/logo.svg` (Kopfzeile, Hero, Marken-Band). Es ist dunkel gezeichnet und
wird im Dunkelmodus und im dunklen Band per Filter weiss (`--logo-filter`,
`.brand-band-logo`). Ein mehrfarbiges neues Logo braucht dafür eine eigene Lösung.
Favicon (`static/favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`) wird nicht
automatisch erzeugt – bei neuem Logo mit einem Bild- oder Favicon-Werkzeug neu machen und
unter denselben Namen hochladen.

### Abschnittsliste („Auf dieser Seite“)

Entsteht automatisch aus den `##`-Überschriften (erst ab zwei). Ab 1100 px rechts neben
dem Text, darunter zugeklappt über dem Text. Code: `layouts/partials/seiten-uebersicht.html`,
Raster `.seite-raster`/`.mit-liste` in `single.html`/`list.html`, Beschriftung
`auf_dieser_seite`. Nicht zurückbauen zu: Block zwischen Titel und Text, Leiste erst beim
Scrollen, waagrechte Scroll-Reihe. Das Skript wartet auf `DOMContentLoaded`, sammelt auch
Überschriften aus Vorlagen, holt sich Platz aus dem Seitenrand (`--rand-ausbruch`) und
braucht `--sprung-abstand`/`--kopf-hoehe`, damit Sprungziele nicht unter der Kopfzeile
landen.

---

## 17. Einen ganzen Bereich löschen

- `_index.md` und alle Seiten darunter löschen, **in allen drei Sprachen**. Der Menüpunkt
  verschwindet mit.
- Der Bau wird rot, solange noch Links auf den Bereich zeigen – die Stellen anpassen.
- PDFs und Bilder unter `assets/` bzw. `static/` werden nicht mitgelöscht.
- Alternativ in der Textmappe: Titel und alle Texte mit `!Löschen!` markieren.

---

## 18. Automatisierungen (GitHub Actions)

| Workflow | Wann | Was |
| --- | --- | --- |
| `hugo.yml` | jede Änderung an `main`, jeder Pull Request | bauen, Suche (Pagefind), interne Links prüfen (bricht ab), externe Links (nur Warnung), Mitgliederbereich verschlüsseln, veröffentlichen (nur `main`) |
| `textmappen.yml` | jede Änderung an `main` | frische Textmappen ans Release „Textmappen“ |
| `texte-einlesen.yml` | Mappe in `redaktion/` hochgeladen | einlesen, probeweise bauen, Pull Request mit Bericht |
| `neue-saison.yml` | von Hand (*Run workflow*) | Saisonwechsel als Pull Request |
| `erfahrungsbericht-intake.yml` | Formspree-Einsendung | neue Erfahrungsbericht-Datei als Pull Request |

Ein fehlgeschlagener Bau nimmt die Website nicht offline; es bleibt die letzte gute
Fassung. Hugo-Version: in `hugo.yml` fest eingetragen – beim Erhöhen auch lokal testen.

---

## 19. Die Website prüfen

Der Bau prüft interne Links selbst. Zusätzlich gibt es Prüfskripte (lokal, mit gebauter
Seite unter `public/`):

```bash
npm run build
npx http-server public -p 8099 -s &
BREITEN=1280,768,390 MODI=light,dark node scripts/seiten-pruefen.mjs  # Layout, Kontrast, Bilder
python3 scripts/struktur-pruefen.py                                  # Duplikate, unerreichbare Seiten, tote Links
npx pagefind --site public && node scripts/verhalten-pruefen.mjs     # Bedienung, Formulare (Formspree abgefangen)
node scripts/fakten-generator-pruefen.mjs                            # 150 Sets + PDF
node scripts/figuren-generator-pruefen.mjs                           # 12 Sets + PDF
python3 scripts/texte-mappe-pruefen.py                               # Textmappen
node scripts/editor-rundlauf.mjs                                     # Web-Editor
```

Anderer Port: `ADRESSE=http://127.0.0.1:8123` davor. Erwartet: genau zehn unerreichbare
Seiten (Mitgliederbereich und Alpha). Eine neue Prüfung zuerst an einem echten, bekannten
Fehler testen und Fehlalarme abschalten – sonst liest sie bald niemand mehr.

---

## 20. Drittdienste und Zugänge

| Dienst | Wofür |
| --- | --- |
| GitHub Pages / Actions | Hosting und Automatisierung. Umzug auf `nc-wiki.ch` ist vorbereitet, aber nicht aktiv (keine `CNAME`, DNS nicht umgestellt). |
| Formspree | Formulare ([13](#13-formulare)) |
| Pages CMS | Web-Editor ([4](#4-web-editor-pages-cms-im-detail)) |
| Pagefind | Suche, läuft ganz im Browser |
| Google Analytics | nur nach Einwilligung |
| Instagram, Discord | nur Links |

**Zugänge gehören nie ins Repository** – auch gelöschte Dateien bleiben in der Geschichte
lesbar. Sie gehören in einen gemeinsamen Passwort-Manager des Vereins, mindestens:
Owner/Admins des Repos, `MITGLIEDER_PASSWORT`, Formspree-Login (welche ID wozu, welche
Empfänger-Adresse), der GitHub-Token in Formspree, Admins von Instagram/Discord, Registrar
und Zugang der Domain `nc-wiki.ch`, das Postfach `sponsoring@nc-wiki.ch`.

---

## 21. Wo hört „nur ausfüllen“ auf?

**Selbst machen:** alles, was sich als „Feld X in Datei Y auf Wert Z setzen“ beschreiben
lässt, wo Y eine der hier genannten Dateien ist.

**Hilfe holen** (jemand mit Hugo-/Web-Kenntnissen oder ein KI-Assistent mit Repo-Zugriff):

- neue Art von Seite, Abschnitt, Formular oder interaktivem Element;
- Änderungen unter `layouts/`, `assets/css/` oder `.github/workflows/`;
- neue Schrift, neues Favicon;
- alles, was mehrere Stellen gleichzeitig betrifft (Farbvariablen,
  `data/testablauf.yaml`, `data/subtests.yaml`).
