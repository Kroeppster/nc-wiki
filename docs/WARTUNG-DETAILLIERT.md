# Wartung der NCWiki-Website – ausführliche Anleitung

Das hier ist die **lange Version** von [`docs/WARTUNG.md`](WARTUNG.md). Die kurze Version
deckt die alltäglichen Aufgaben ab (neue Seite, PDF hochladen, News schreiben, Datei
löschen, Bild einfügen). Dieses Dokument geht zusätzlich auf alles ein, was seltener
vorkommt, aber irgendwann garantiert mal ansteht: Navigation umbauen, Logo/Icons
austauschen, Sponsoren pflegen, Farben/Schrift anpassen, die verschiedenen `data/`-Listen
(FAQ, Uniguide, Untertests) verwalten, Übersetzungen der festen Bedienelement-Texte,
Countdown-Datum, Cookie-Banner/Google Analytics, Formulare, und eine klare Grenze, ab
wann eine Aufgabe wirklich Hugo-Kenntnisse braucht statt nur Copy-Paste.

Wie im Kurzguide gilt: alles hier geht über die normale GitHub-Weboberfläche
(github.com), kein Programm muss installiert werden – **ausser bei den wenigen Stellen,
die das ausdrücklich anders sagen** (z. B. Favicon neu erzeugen).

Genau wie im Kurzguide: neue Seiten/Änderungen immer als **eigener Branch + Pull
Request**, nie direkt in `main`. Das wird unten nicht bei jedem einzelnen Schritt
wiederholt, gilt aber überall.

---

## Inhalt

1. [Neue Seiten und Bereiche – vertieft](#1-neue-seiten-und-bereiche--vertieft)
2. [Navigationsleiste ändern](#2-navigationsleiste-ändern)
3. [Logo und Favicon austauschen](#3-logo-und-favicon-austauschen)
4. [Sponsor:innen verwalten](#4-sponsorinnen-verwalten)
5. [Team-Seite pflegen](#5-team-seite-pflegen)
6. [FAQ verwalten](#6-faq-verwalten)
7. [Uniguide (Universitäts-Liste) verwalten](#7-uniguide-universitäts-liste-verwalten)
8. [Untertests verwalten](#8-untertests-verwalten)
9. [Countdown-Datum ändern](#9-countdown-datum-ändern)
10. [Cookie-Banner und Google Analytics](#10-cookie-banner-und-google-analytics)
11. [Formulare (Formspree) ändern oder ergänzen](#11-formulare-formspree-ändern-oder-ergänzen)
12. [Feste Bedienelement-Texte übersetzen (i18n)](#12-feste-bedienelement-texte-übersetzen-i18n)
13. [Social-Media-Links und Newsletter](#13-social-media-links-und-newsletter)
14. [Farben, Schrift und generelles Design](#14-farben-schrift-und-generelles-design)
15. [Eine ganze Seite/einen ganzen Bereich löschen](#15-eine-ganze-seiteinen-ganzen-bereich-löschen)
16. [Wo hört "nur Copy-Paste" auf?](#16-wo-hört-nur-copy-paste-auf)
17. [Startseite: die Kacheln "Was du hier findest"](#17-startseite-die-kacheln-was-du-hier-findest)
18. [Prüfungsmodus: Uhr, Ansagen und der Testablauf](#18-prüfungsmodus-uhr-ansagen-und-der-testablauf)

---

## 1. Neue Seiten und Bereiche – vertieft

Der Kurzguide (Abschnitt 2) zeigt die Grundschritte. Ergänzend:

### Übersichtsseite vs. Unterseite

- **`_index.md`** in einem Ordner = die Übersichtsseite dieses Ordners selbst (z. B.
  `content/de/ems/uebungsaufgaben/_index.md` ist der Text ganz oben auf der
  Übungsaufgaben-Übersicht, bevor die einzelnen Untertests aufgelistet werden).
- **Jede andere `.md`-Datei** im selben Ordner = eine eigenständige Unterseite.

Ein komplett neuer Bereich (z. B. eine neue Rubrik neben "Übungsaufgaben") braucht immer
zuerst eine `_index.md` in einem neuen Unterordner von `content/de/` (bzw. `content/fr/`,
`content/it/`) – ohne `_index.md` "gibt es den Ordner für Hugo nicht".

### Menü-Platzierung im Detail

Ein `menu`-Block im Frontmatter macht aus einer Seite einen Menüpunkt:

```yaml
menu:
  main:
    parent: ems
    weight: 5
```

- **`parent`** muss der `identifier` eines bestehenden Menüpunkts sein. Für Seiten ist
  das automatisch der Dateiname des Ordners (z. B. `content/de/ems/_index.md` hat
  implizit den Identifier `ems`). Für die beiden reinen Dropdown-Überschriften
  "Vorbereitung" und "Austausch" (die zu keiner eigenen Seite gehören) ist der Identifier
  in `hugo.toml` festgelegt (`vorbereitung`, `austausch`) – siehe Abschnitt 2 unten.
- **`weight`** bestimmt die Reihenfolge unter Geschwister-Menüpunkten (kleinere Zahl =
  weiter vorne). Beim Einfügen eines neuen Punkts dazwischen: die anderen `weight`-Werte
  im selben `parent` müssen nicht zwingend angepasst werden, solange die neue Zahl
  irgendwo dazwischen passt (auch Kommazahlen wie `2.5` funktionieren).
- **Fehlt `parent`**, erscheint der Punkt als eigener Top-Level-Punkt im Hauptmenü statt
  als Kind eines Dropdowns.
- Dasselbe `menu`-Frontmatter muss in **jeder Sprachversion** der Seite einzeln gesetzt
  werden (mit dem übersetzten `name`, falls einer angegeben ist – ohne `name` wird
  automatisch der `title` der Seite verwendet).

### Alias/Weiterleitung für eine umbenannte Seite

Wird eine Seite umbenannt oder verschoben (neuer Dateiname/Pfad), ändert sich ihre
Web-Adresse – alte Links (von aussen, z. B. aus Social Media oder E-Mails) würden dann
ins Leere führen. Um das zu vermeiden, im Frontmatter der Seite an ihrem NEUEN Ort:

```yaml
aliases:
  - /alter/pfad/
```

Hugo erzeugt dann unter der alten Adresse automatisch eine Weiterleitung auf die neue.

---

## 2. Navigationsleiste ändern

Wichtig zu verstehen: **Es gibt keine einzige Datei, in der "das Menü" steht.** Es setzt
sich automatisch aus zwei Quellen zusammen:

1. **Menüpunkte, die zu einer echten Seite gehören** – gesteuert über den
   `menu:`-Frontmatter-Block der jeweiligen Seite (siehe Abschnitt 1 oben). Um z. B. den
   Menüpunkt "Team" von "Über Uns" nach "Kontakt" zu verschieben, ändert man `parent:
   ueber-uns` auf `parent: kontakt` in `content/<sprache>/ueber-uns/team/_index.md`.
2. **Die beiden reinen Dropdown-Überschriften "Vorbereitung" und "Austausch"** – diese
   gehören zu keiner echten Seite (ein Klick auf "Vorbereitung" selbst führt nirgendwo
   hin, nur seine Kinder sind anklickbar). Sie stehen in `hugo.toml`, einmal pro Sprache:

   ```toml
   [[languages.de.menu.main]]
     identifier = 'vorbereitung'
     name = 'Vorbereitung'
     weight = 3
   ```

   Um z. B. eine **dritte** solche Dropdown-Gruppe einzuführen (weder an eine Seite
   gebunden), denselben Block mit neuem `identifier`/`name`/`weight` in **allen drei**
   Sprachblöcken (`languages.de`, `languages.fr`, `languages.it`) von `hugo.toml`
   ergänzen, und danach bei den gewünschten Seiten `parent: <neuer-identifier>` setzen.

**Reihenfolge der Top-Level-Punkte** (Startseite, Übungsaufgaben, Vorbereitung, Austausch,
News, Über Uns, Unterstützen, Kontakt) ergibt sich rein aus den `weight`-Werten aller
Top-Level-Menüpunkte zusammen (egal ob sie aus einer Seite oder aus `hugo.toml` kommen) –
sie werden nicht getrennt behandelt.

**Menüpunkt umbenennen** (z. B. "Übungsaufgaben" → "Übungsserien"): für einen
Seiten-Menüpunkt entweder den `title` der Seite ändern (ändert dann auch die
Seitenüberschrift selbst) oder gezielt nur die Menü-Beschriftung mit einem eigenen `name`
im `menu`-Block überschreiben:

```yaml
menu:
  main:
    parent: ems
    weight: 1
    name: "Übungsserien"
```

**Neuer Top-Level-Punkt, der auf eine bestehende Seite zeigt:** einfach `parent`
weglassen (siehe Abschnitt 1).

**Technisches Verhalten der Dropdowns** (keine Codeänderung nötig, nur zum Verständnis):
Untermenüs öffnen sowohl per Maus-Hover als auch per Klick/Tap (wichtig für
Touch-Geräte) – die Logik dafür liegt in `layouts/partials/footer.html` (gemeinsamer
`<script>`-Block) und reagiert automatisch auf jeden Menüpunkt mit Kindern, unabhängig
davon, wie viele es sind. Auf schmalen Bildschirmen (Hamburger-Menü) verschwindet die
Maus-Hover-Öffnung automatisch und es bleibt nur Klick/Tap.

---

## 3. Logo und Favicon austauschen

**Das Logo** liegt unter `static/images/logo.svg` und wird an genau drei Stellen
eingebunden: in der Kopfzeile jeder Seite (`layouts/partials/header.html`), im
dekorativen Banner auf der Startseite (`layouts/partials/brand-band.html`), und als
Quelle für das Favicon (siehe unten). Es einfach zu ersetzen reicht für die ersten beiden
Stellen: neue Datei mit demselben Namen (`logo.svg`) hochladen, alte überschreiben lassen
(GitHub fragt beim Hochladen automatisch danach).

**Wichtig:** Wird das Logo ersetzt, sollte es aus denselben Gründen wie das aktuelle
(Lesbarkeit in Hell- **und** Dunkelmodus, siehe Abschnitt 14 unten zum Theme-System)
entweder als reines Liniensymbol ohne Hintergrundfläche gestaltet sein, oder es braucht
zusätzlich eine eigene Behandlung für den Dunkelmodus – im Zweifel jemanden mit
CSS-Kenntnissen dazuholen, damit das Logo im Dunkelmodus nicht z. B. schwarz auf
dunkelblau unsichtbar wird.

**Im dunklen Banner unten wird das Logo automatisch weiss dargestellt.** Genau dieses
Problem trat dort nämlich auf: Das aktuelle Logo ist eine Rastergrafik (sechs eingebettete
PNG-Bilder in einer SVG-Datei), seine Farben lassen sich also nicht per CSS umfärben – und
sein "WIKI"-Schriftzug ist schwarz und war auf dem dunkelblauen Band praktisch unsichtbar.
Seit dem 8. September 2026 liegt deshalb in `assets/css/style.css` auf
`.brand-band-logo` ein Filter (`brightness(0) invert(1)`), der das Logo dort vollständig
weiss einfärbt. Die Logodatei selbst bleibt davon unberührt – in der Kopfzeile auf hellem
Grund erscheint sie weiterhin in Originalfarben.

Für ein neues Logo heisst das:

- Ist es ebenfalls dunkel gezeichnet, passt alles – der Filter macht es im Banner weiss.
- Ist es **mehrfarbig und sollen die Farben auch im Banner erhalten bleiben**, muss dieser
  Filter entfernt und stattdessen eine helle Fassung des Logos hinterlegt werden. Das ist
  ein CSS-Schritt, siehe Abschnitt 16.

**Das Favicon** (Browser-Tab-Icon, drei Dateien: `static/favicon.ico`,
`static/favicon-32.png`, `static/apple-touch-icon.png`) wird **nicht automatisch** beim
Bauen der Website aus `logo.svg` erzeugt, sondern ist einmalig vorab generiert worden
(kleiner Ausschnitt des Logos, ohne den "WIKI"-Schriftzug, der bei 16×16px ohnehin
unlesbar wäre) – siehe Kommentar in `layouts/partials/head.html`. Ändert sich das Logo
grundlegend, sollten diese drei Dateien neu erzeugt werden, sonst zeigt der Browser-Tab
weiterhin das alte Icon.

**Das ist die eine Stelle in diesem ganzen Dokument, die nicht rein über die
GitHub-Weboberfläche geht** – dafür braucht es ein Programm, das aus einer SVG-Datei
kleine PNG/ICO-Ausschnitte erzeugt (z. B. ein Bildbearbeitungswerkzeug oder ein
Online-Favicon-Generator). Alternativ: jemanden mit Hugo-Kenntnissen (oder einen
KI-Assistenten mit Dateizugriff aufs Repo) bitten, das zu übernehmen – die neuen drei
Dateien werden dann einfach unter denselben drei Namen wie oben hochgeladen.

---

## 4. Sponsor:innen verwalten

Sponsor:innen-Logos auf der "Unterstützer:innen"-Seite kommen aus `data/sponsors.yaml` –
die Datei ist direkt im Repo ausführlich kommentiert (Feld für Feld), kurz
zusammengefasst:

1. Logo-Datei hochladen nach `assets/images/sponsors/<dateiname>` (SVG bevorzugt, geht
   aber auch als PNG/JPG).
2. In `data/sponsors.yaml` einen neuen Eintrag ergänzen:

   ```yaml
   - name: "Firmenname"
     logo: "dateiname.svg"
     website: "https://beispiel.ch/"
   ```

3. Reihenfolge der Kacheln = Reihenfolge der Einträge in der Datei (kein separates
   `weight`-Feld nötig – einfach den Eintrag an die gewünschte Stelle in der Liste
   verschieben).
4. Sponsor entfernen: den entsprechenden Eintrag (die 3 Zeilen mit `- name:` bis
   `website:`) löschen. Die Logo-Datei kann zusätzlich gelöscht werden, muss aber nicht
   (sie wird dann einfach nirgends mehr verwendet).

**Kontrast-Hinweis:** Ist ein Logo sehr dunkel (z. B. reines Schwarz ohne eigenen
Hintergrund), kann es auf den dunklen Kacheln im Dunkelmodus schlecht lesbar sein. Für
diesen Fall gibt es in `assets/css/style.css` einen hellen Hintergrund-Chip
(`.sponsor-logo`), der konsistent auf allen Logo-Kacheln liegt – kein Grund, deswegen die
Logo-Datei selbst zu bearbeiten.

---

## 5. Team-Seite pflegen

Die Team-Seite (`content/de/ueber-uns/team/_index.md`, plus `content/fr/...` und
`content/it/...`) hat zwei verschiedene Bereiche, die unterschiedlich gepflegt werden:

### Aktuelles Leitungsteam (Foto-Karten-Raster)

Dieser Bereich wird NICHT als Fliesstext gepflegt, sondern als strukturierte Liste im
Frontmatter jeder der drei Dateien, Feld `leitungsteam:`:

```yaml
leitungsteam:
  - name: "Alessio Iseli"
    rolle: "Koordinator"
  - name: "Kron Mustafa"
    rolle: "Events & Qualitätskontrolle"
```

Der Shortcode `{{</* team-leitung */>}}` im Markdown-Text (direkt unter der Überschrift
"Aktuelles Leitungsteam") liest diese Liste aus und baut daraus automatisch das
Karten-Raster (siehe `layouts/shortcodes/team-leitung.html`).

**Foto oder Platzhalter:** Jeder Eintrag kann zusätzlich ein Feld `foto:` bekommen, mit
dem Pfad zum Foto relativ zu `assets/images/`, z. B.:

```yaml
  - name: "Alessio Iseli"
    rolle: "Koordinator"
    foto: "team/alessio-iseli.jpg"
```

Die Bilddatei kommt dann nach `assets/images/team/alessio-iseli.jpg` (Ordner bei Bedarf
neu anlegen). **Fehlt das Feld `foto:` (der Normalfall, solange noch nicht für alle
Personen ein Foto vorliegt), erscheint automatisch ein farbiger Kreis mit den Initialen
als Platzhalter** – dieselbe Darstellung, die auch bei Erfahrungsberichten ohne Foto
verwendet wird. Es muss also nichts Zusätzliches eingerichtet werden, damit die Seite
auch ohne Fotos sauber aussieht.

Da es sich um drei separate Dateien handelt (eine pro Sprache), muss ein neues
Teammitglied (Name **und** übersetzte Rolle) in allen dreien nachgezogen werden. Der
Name bleibt dabei überall gleich, nur `rolle:` wird pro Sprache übersetzt.

### Frühere Saisons, Content Creators, Ehemalige Verantwortliche

Alles unterhalb von "Aktuelles Leitungsteam" bleibt ganz normaler Markdown-Fliesstext mit
Überschriften und Aufzählungen (keine Fotos, kein Karten-Raster) – neue Namen werden
einfach als neue Aufzählungspunkte ergänzt. Beim Saisonwechsel wandert die bisherige
Besetzung des Leitungsteams (aus `leitungsteam:` oben) sinnvollerweise als neuer
Textabschnitt unter "Frühere Saisons", nach demselben Muster wie die bereits dort
stehenden Jahrgänge, bevor `leitungsteam:` mit der neuen Besetzung überschrieben wird.

---

## 6. FAQ verwalten

Die FAQ-Sektion kommt aus `data/faq.yaml` – jeder Eintrag hat eine `id`, sowie Frage und
Antwort **einmal pro Sprache**:

```yaml
- id: "eindeutige-kurzbezeichnung"
  frage:
    de: "Frage auf Deutsch?"
    fr: "Question en français ?"
    it: "Domanda in italiano?"
  antwort:
    de: "Antwort auf Deutsch."
    fr: "Réponse en français."
    it: "Risposta in italiano."
```

Neue Frage hinzufügen: neuen Eintrag mit eindeutiger `id` ergänzen (wird intern
verwendet, erscheint nirgends sichtbar). Reihenfolge auf der Seite = Reihenfolge in der
Datei. Frage entfernen: kompletten Eintrag löschen.

---

## 7. Uniguide (Universitäts-Liste) verwalten

Die Uniguide-Vergleichstabelle und die Detailseiten kommen aus `data/unis.yaml` – auch
diese Datei ist im Repo bereits ausführlich Feld für Feld kommentiert. Zwei wichtige
Besonderheiten:

- **Jede Universität braucht zwei Dinge gleichzeitig:** einen Eintrag in
  `data/unis.yaml` **und** eine eigene, fast leere Seite unter
  `content/<sprache>/ems/uniguide/<slug>.md` (nur `title` und `uni_slug` im
  Frontmatter). Fehlt die Seite, führt der Link aus der Tabelle ins Leere.
- **Nichts erfinden/schätzen:** Ist eine Angabe (z. B. Studienplatz-Zahl) nicht sicher
  bekannt, bleibt das Feld leer (`null`) statt eine Zahl zu raten – das sollte so
  bleiben, bis der echte Wert auf der offiziellen Uni-Website nachgeprüft wurde. Bei
  jeder inhaltlichen Änderung auch das Feld `stand:` (Datum der letzten Prüfung) **und**
  `quelle:` (Link zur verwendeten Seite) aktualisieren.

### Die noch leeren Felder

Am 8. September 2026 sind pro Universität vier weitere Felder dazugekommen. Sie stehen
**alle auf `null`**, weil sie noch nicht an offizieller Stelle nachgeprüft sind:

| Feld | Was hinein gehört | Beispiel |
| --- | --- | --- |
| `website_medizin` | Direktlink zur medizinischen Fakultät, nicht zur Uni-Startseite | `"https://medizin.unibas.ch"` |
| `anmeldefrist` | Frist als Text | `"15. Februar"` |
| `studienbeginn` | Wann das Studium startet | `"Mitte September"` |
| `semestergebuehr` | Betrag inkl. Währung, als Text | `"CHF 850 pro Semester"` |

**Was passiert, solange ein Feld leer ist:** Es erscheint auf der Website gar nicht – es
gibt also keine leeren Zeilen und keine Platzhalter mitten in den Angaben. Stattdessen
steht auf der Uni-Seite ein gelber Kasten "Diese Angaben fehlen noch", der genau die
fehlenden Felder aufzählt und zum Melden einlädt. Sobald ein Feld gefüllt ist,
verschwindet es aus diesem Kasten und taucht bei den Angaben auf. Es ist also **kein
Fehler**, wenn dieser Kasten erscheint – er ist der ehrliche Zwischenstand.

### Erfahrungsberichte automatisch bei der Universität anzeigen

Das Feld `berichte_ort` verknüpft eine Universität mit den Erfahrungsberichten. Sein Wert
muss **genau** dem entsprechen, was in den Berichten im Frontmatter unter `ort:` steht
(z. B. `"Zürich"`). Passt es, erscheinen auf der Uni-Seite automatisch die drei neuesten
Berichte von diesem Ort. Gibt es zu diesem Ort keine, bleibt der Abschnitt weg – dann
einfach `""` eintragen.

Dieses Feld wird **nie angezeigt**, es ist reine Technik. Deshalb wird es auch nicht
übersetzt: Es steht in `data/unis.yaml` genau einmal und gilt für alle drei Sprachen.

### Der Vergleich ("mehrere Unis nebeneinander")

In der Tabelle lassen sich in der ersten Spalte bis zu **vier** Universitäten ankreuzen.
Unten erscheint dann eine Leiste; ein Klick auf "Vergleichen" stellt sie nebeneinander –
eine Spalte pro Universität, eine Zeile pro Angabe.

**Daran gibt es nichts zu pflegen.** Der Vergleich zieht dieselben Felder aus
`data/unis.yaml`; ein neu gefülltes Feld erscheint automatisch auch dort. Zwei Dinge sind
Entwickler-Schritte (Abschnitt 16):

- eine **weitere Zeile** in den Vergleich aufnehmen → `layouts/partials/uniguide-table.html`,
  Abschnitt "VERGLEICHSANSICHT"
- die **Obergrenze von vier** ändern → dieselbe Datei, ganz unten im Skript `var MAX = 4;`.
  Die Grenze ist bewusst gesetzt: Mehr Spalten passen auf einem Handy nicht mehr
  nebeneinander.

---

## 8. Untertests verwalten

Die nummerierte Kachel-Übersicht auf der Startseite wird aus `data/subtests.yaml`
erzeugt. Jeder Eintrag hat eine Nummer, einen Slug (muss zum Ordnernamen unter
`content/<sprache>/ems/uebungsaufgaben/` passen) und einen Namen pro Sprache. Auf der
Q&A-Seite hängt die Antwort zur Frage "Welche Untertests gibt es?" (siehe
`data/faq.yaml`, Feld `dynamic: subtests`) automatisch dieselbe Liste als Aufzählung an –
die Liste selbst muss also nur an dieser einen Stelle gepflegt werden.

**Wichtig, seit der Zusammenlegung von "Figuren einprägen" und "Fakten einprägen" zu
"Figuren & Fakten lernen" (2026-08-16):** `data/subtests.yaml` zählt jetzt bewusst nur
noch 8 Einträge, weil zwei thematisch sehr ähnliche Übungsaufgaben-Seiten zu einer
zusammengefasst wurden. Das ist eine reine Organisationsentscheidung für die
Übungsseiten dieser Website – die echte EMS-Prüfung hat nach wie vor 9 offiziell
getaktete Untertests (siehe Tagesablauf-Tabelle auf `/ems/`). Die FAQ-Antwort selbst
("Der EMS besteht aus 9 Untertests...") ist deshalb bewusst **nicht** automatisch aus
`data/subtests.yaml` abgeleitet, sondern ein fest formulierter Satz in `data/faq.yaml` –
nur die darunter angehängte Aufzählung kommt aus `data/subtests.yaml`. Ändert sich die
offizielle Anzahl oder Reihenfolge der echten EMS-Untertests (kommt selten vor, aber
offiziell schon passiert), beide Stellen prüfen: den Text in `data/faq.yaml` UND die
Liste in `data/subtests.yaml`.

Wird ein Eintrag in `data/subtests.yaml` umbenannt oder verschoben, das gleiche `weight:`
(Reihenfolge) im Frontmatter der passenden Seite unter `content/<sprache>/ems/
uebungsaufgaben/` nachziehen, damit die (unnummerierte) Kartenliste auf der
Übungsaufgaben-Übersichtsseite dieselbe Reihenfolge zeigt.

### Zusatz-Hinweis bei den Downloads einer Übungsaufgaben-Seite

Direkt beim Download-Bereich jeder Übungsaufgaben-Unterseite erscheint automatisch ein
kleines "CC BY-NC 4.0"-Badge (zusätzlich zum grossen Lizenzhinweis oben unter dem
Titel). Braucht eine Serie mal einen zusätzlichen, auffälligen Hinweis daneben – z. B.
weil sich das Format kürzlich geändert hat –, im Frontmatter der jeweiligen Seite
einfach ergänzen:

```yaml
downloads_notice: "Neues Layout!"
```

Ohne dieses Feld erscheint nur das Lizenz-Badge, kein zusätzlicher Hinweis. Der Text ist
frei wählbar und wird nicht automatisch übersetzt – bei Bedarf pro Sprachdatei einzeln
eintragen.

---

## 9. Countdown-Datum ändern

Der Countdown auf der Startseite ("noch X Tage bis zum EMS") zählt auf das Datum in
`hugo.toml` unter `[params]` → `ems_exam_date` herunter:

```toml
ems_exam_date = '2027-07-09T08:00:00+02:00'
```

Format: `JJJJ-MM-TTTHH:MM:SS+ZZ:ZZ`. Die Zeitzone am Ende (`+02:00` = Schweizer
Sommerzeit, `+01:00` = Winterzeit) muss dabei sein.

---

## 10. Cookie-Banner und Google Analytics

Der Cookie-Banner (erscheint beim ersten Website-Besuch) bietet echte
Akzeptieren/Ablehnen-Wahl. Google Analytics wird **nur** geladen, wenn aktiv
"Akzeptieren" gewählt wurde – ohne Einwilligung lädt kein Google-Skript und wird kein
Cookie gesetzt.

Die Google-Analytics-ID steht in `hugo.toml` unter `[params]` → `google_analytics_id`
(Format `G-XXXXXXXXXX`, zu finden in Google Analytics unter Verwaltung → Datenstreams →
[Datenstream auswählen]). Feld leeren, um Google Analytics komplett zu deaktivieren – der
Cookie-Banner zeigt dann weiterhin Akzeptieren/Ablehnen an, aber ohne Wirkung.

Die Cookie-Banner-**Texte** selbst (was genau dem/der Besucher:in erklärt wird) stehen in
`i18n/de.yaml`, `i18n/fr.yaml`, `i18n/it.yaml` unter den Schlüsseln, die mit `cookie_`
beginnen – siehe Abschnitt 12 unten zur allgemeinen Funktionsweise dieser Dateien.

---

## 11. Formulare (Formspree) ändern oder ergänzen

Die Website hat keinen eigenen Server, darum laufen alle Formulare (Kontakt,
Erfahrungsbericht-Einreichung, "Fehler melden" bei PDFs) über den externen Dienst
Formspree. Jedes Formular ist über eine eigene Formspree-Adresse (Format
`https://formspree.io/f/xxxxxxxx`) mit dem jeweiligen Formspree-Konto verbunden – diese
Adresse steht direkt im jeweiligen Partial:

| Formular | Datei |
| --- | --- |
| Kontaktformular | `layouts/partials/contact-form.html` |
| Erfahrungsbericht-Einreichung | `layouts/partials/experience-form.html` |
| Fehlermeldungen zu den Übungsaufgaben | `layouts/partials/report-error-general.html` |

Um ein Formular an ein anderes Formspree-Konto/-Formular umzuhängen: die Adresse in der
jeweiligen Datei ersetzen. Der Zugang zum Formspree-Konto selbst (Login) gehört in den
gemeinsamen Passwort-Manager des Teams, nicht ins Repo (siehe Kurzguide, Abschnitt 6).

**Zwei Adressen, drei Formulare.** Das Fehlermelde-Formular auf der
Übungsaufgaben-Übersicht sendet vorläufig an **dieselbe** Adresse wie das
Kontaktformular. Vorher stand dort ein Platzhalter: Jede Fehlermeldung ging ins Leere,
während die meldende Person eine Bestätigung sah – schlimmer als gar kein Formular.

Damit die Meldungen im gemeinsamen Postfach nicht untergehen, setzt das Formular über ein
verstecktes Feld `_subject` den festen Betreff **"Fehlermeldung Uebungsaufgaben
(Website)"**. Danach lässt sich filtern oder eine Regel anlegen. Der Betreff ist immer
deutsch, unabhängig von der Sprache der Besucherin – er ist eine interne Sortierhilfe, und
ein Filter funktioniert nur bei immer gleichem Wortlaut.

Sobald ein eigenes Formspree-Formular für Fehlermeldungen besteht, genügt es, dessen
Adresse in `report-error-general.html` einzutragen. Das versteckte `_subject`-Feld kann
dann bleiben oder weg – es stört nicht.

**Die Erfahrungsbericht-Adresse bitte nicht mit umhängen.** An ihr hängt mehr als ein
Postfach: Eine Einsendung löst über `repository_dispatch` den Workflow
`.github/workflows/erfahrungsbericht-intake.yml` aus, der daraus automatisch eine neue
Datei und einen Pull Request baut. Wird diese Adresse geändert, ohne die Weiterleitung
mit anzupassen, bricht diese Automatisierung.

Der frühere "Fehler melden"-Knopf bei **jedem einzelnen** PDF-Download existiert nicht
mehr – er wurde durch dieses eine zentrale Formular ersetzt. In `download-list.html` gibt
es deshalb kein Formular mehr.

Beide neuen Formulare nutzen dieselbe generische Klasse `report-error` wie die
bestehenden PDF-Fehlermeldungen – das dazugehörige JavaScript (Senden per Fetch im
Hintergrund, Status-Text im Knopf) liegt zentral in `layouts/partials/footer.html`
(Teil 5) und muss für ein neues Formular dieser Art NICHT angepasst werden, solange das
Formular die Klasse `report-error` und einen `button[type="submit"]` hat.

Ein **neues** Formular an einer anderen Stelle der Website einzubauen, ist keine reine
Copy-Paste-Aufgabe mehr (neues HTML-Formular + neue Formspree-Adresse einrichten) – siehe
Abschnitt 16.

---

## 12. Feste Bedienelement-Texte übersetzen (i18n)

Nicht zu verwechseln mit den Seiteninhalten selbst (die liegen unter `content/`)! Die
`i18n/de.yaml`, `i18n/fr.yaml`, `i18n/it.yaml`-Dateien enthalten stattdessen alle **festen
Texte, die überall auf der Website gleich wiederverwendet werden** – Knopf-Beschriftungen
("Senden", "Mehr erfahren"), Menü-Hilfstexte für Screenreader, Formular-Labels,
Fehlermeldungen, Cookie-Banner-Texte usw.

Jede Zeile hat links einen "Schlüssel" (z. B. `cookie_reject:`) und rechts den
tatsächlichen Text. **Alle drei Dateien haben dieselben Schlüssel**, nur mit übersetztem
Text rechts. Einen bestehenden Text ändern: den Wert rechts vom Doppelpunkt in **allen
drei** Dateien anpassen (nicht nur in einer, sonst zeigen die anderen beiden Sprachen
weiter den alten Text). Es dürfen keine neuen Schlüssel frei erfunden werden, ohne dass
sie auch irgendwo in `layouts/` tatsächlich abgerufen werden – das würde folgenlos
bleiben (der Text würde einfach nirgends erscheinen).

---

## 13. Social-Media-Links und Newsletter

In `hugo.toml` unter `[params]`:

```toml
social_instagram = 'https://www.instagram.com/ncwiki.ch/'
social_discord = 'https://discord.com/invite/DhgYpUGss9'
social_linkedin = ''
newsletter_url = ''
```

Bleibt eines dieser Felder leer (`''`), verschwindet der entsprechende Knopf/Bereich in
der Fusszeile automatisch komplett, statt auf eine leere oder kaputte Adresse zu
verlinken. Sobald z. B. ein LinkedIn-Auftritt existiert, einfach die echte Adresse
eintragen – der Knopf erscheint dann automatisch, ohne dass sonst etwas geändert werden
müsste.

---

## 14. Farben, Schrift und generelles Design

**Das gesamte Erscheinungsbild** (Farben, Schriftgrössen, Abstände) kommt aus einer
einzigen Datei: `assets/css/style.css`. Ganz oben stehen alle Grundfarben und
Schriftarten als benannte Variablen:

```css
:root{
  --color-signal:#223FCB;         /* Primärfarbe */
  --color-accent:#F5813C;
  --font-display:'Poppins','Trebuchet MS',system-ui,sans-serif;
  --font-body:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
  ...
}
```

Eine Variable dort ändern (z. B. `--color-signal`) wirkt sich **automatisch überall** auf
der Website aus, wo diese Farbe verwendet wird (Knöpfe, Links, Hervorhebungen) – nicht
einzeln pro Seite oder Element ändern.

**Zu den Schriften:** Die Website nutzt zwei Schriftarten – **Poppins** für Überschriften
und **Inter** für den Fliesstext. Beide liegen als Dateien im Ordner `static/fonts/` und
werden von dort ausgeliefert, **nicht** von Google Fonts nachgeladen: So bekommt Google
beim Besuch der Website keine IP-Adressen unserer Besucher:innen zu sehen. Wer eine
Schrift austauschen will, muss deshalb beides tun – die `.woff2`-Datei in `static/fonts/`
ablegen **und** den passenden `@font-face`-Block in `assets/css/style.css` anpassen; es
reicht nicht, nur den Namen in der Variable zu ändern.

Bis August 2026 waren hier Space Grotesk und Space Mono im Einsatz. Beide wurden ersetzt,
weil die Kombination technisch/"cyber" wirkte – für eine Lernplattform für Maturand:innen
der falsche Ton. Eine Monospace-Schrift gibt es seither gar nicht mehr: Labels und
Eyebrows tragen ihren Charakter jetzt über Versalien und Sperrung statt über die
Schriftart.

**Wichtig: Zwei getrennte Paletten für Hell- und Dunkelmodus.** Direkt unter dem ersten
`:root{...}`-Block (helle Palette) folgt weiter unten in derselben Datei ein zweiter
Block `:root[data-theme="dark"]{...}` mit denselben Variablennamen, aber den Werten für
den Dunkelmodus. **Beide Blöcke müssen bei einer Farbänderung zusammen angepasst
werden**, sonst stimmt z. B. die Primärfarbe im Hellmodus, aber im Dunkelmodus steht dort
noch die alte Farbe (oder ein schlecht lesbarer Kontrast).

### Tiefe: Schatten und Verläufe

Bis zum 8. September 2026 hatte die Website **keinen einzigen Schatten**. Jede Karte war
ein umrandetes Rechteck, in dieselbe Fläche gemalt wie alles andere – die Rückmeldung
lautete entsprechend "sehr viele einfarbige Flächen". Seither gibt es dafür eigene
Variablen im selben `:root`-Block:

| Variable | Wofür |
| --- | --- |
| `--shadow-sm` | Ruhezustand von Karten, Kacheln, Download-Knöpfen, Tabellen |
| `--shadow-md` | Zeigen mit der Maus ("hebt sich an") |
| `--shadow-lg` | Die wenigen Elemente, die wirklich schweben sollen: Countdown-Karte, Spenden-Aufruf |
| `--glow-signal`, `--glow-accent` | Zwei sehr blasse Farbwolken hinter der ganzen Seite |
| `--band-top`, `--band-glow`, `--band-texture` | Verlauf, Lichtschein und Punktraster im dunklen Band unten |
| `--color-section-alt` | Fläche der abwechselnd getönten Sektionen auf der Startseite |

**Schatten müssen im Dunkelmodus kräftiger sein.** Ein Schatten ist dunkel – auf dunklem
Grund ist ein zarter Schatten schlicht unsichtbar, und die Karten wären wieder flach.
Deshalb stehen im `:root[data-theme="dark"]`-Block deutlich höhere Deckkraft-Werte.

**`--color-section-alt` ist im Dunkelmodus absichtlich nicht dieselbe Farbe wie
`--color-surface`.** Die Karten in diesen Sektionen haben genau die Kartenfarbe und wären
sonst kaum vom Untergrund zu unterscheiden.

### Warum es einen eigenen Knopf-Hintergrund gibt

`--color-btn-bg` sieht im Hellmodus genauso aus wie `--color-signal` – im Dunkelmodus
aber nicht, und das ist Absicht. Der Dunkelmodus macht `--color-signal` bewusst **heller**,
damit Link-**Text** auf dunklem Grund lesbar bleibt. Als Hintergrund für weisse
Knopfbeschriftung ist genau das falsch: Dort kam die weisse Schrift nur auf 3.1 : 1,
gefordert sind 4.5 : 1. Wer die Markenfarbe ändert, muss deshalb **beide** Variablen
anpassen – `--color-signal` für Links und `--color-btn-bg` für gefüllte Knöpfe, jeweils in
beiden Paletten.

Dasselbe gilt für `--cta-from`/`--cta-to` (die blaue Spenden-Karte) und
`--color-avatar-0` bis `-5`: Diese Werte stehen bewusst **nur** im hellen Block und werden
im Dunkelmodus *nicht* überschrieben, weil auf ihnen weisser Text steht. Sie dürfen
deshalb nie so hell werden, dass Weiss darauf nicht mehr lesbar ist.

**Kontrast prüfen, bevor eine Farbe geändert wird.** Ein Online-Kontrastrechner
(Suchbegriff "WCAG contrast checker") reicht: Normaler Text braucht 4.5 : 1, grosse
Überschriften 3 : 1 – und zwar in **beiden** Modi.

**Schriftarten austauschen:** In `--font-display`/`--font-body` die erste
Schriftart in der Liste ersetzen (eine `--font-mono` gibt es seit dem Schriftwechsel
nicht mehr, siehe oben; die folgenden Namen sind reine Rückfall-Schriften,
falls die erste beim Besuch nicht verfügbar wäre). Eine komplett neue Schriftart
einzubinden (die nicht schon als Google Font o. Ä. im Projekt vorbereitet ist) braucht
zusätzliche technische Schritte (Schriftdatei einbinden/laden) – das ist keine reine
Ein-Zeilen-Änderung mehr, siehe Abschnitt 16.

**Grössere Layout-Änderungen** (neue Sektionen, andere Seitenaufteilung, neue
Komponenten) erfordern Kenntnisse über Hugo-Templates (`layouts/`) und gehören ebenfalls
zu Abschnitt 16.

---

## 15. Eine ganze Seite/einen ganzen Bereich löschen

Der Kurzguide (Abschnitt 8) erklärt das Löschen einer einzelnen Datei. Beim Löschen eines
**ganzen Bereichs** (mehrere Seiten auf einmal, z. B. ein kompletter Unterordner unter
`content/`) zusätzlich beachten:

- **Menüpunkt verschwindet automatisch**, sobald die zugehörige `_index.md` mit ihrem
  `menu`-Block gelöscht ist – nichts in `hugo.toml` oder `layouts/` muss dafür separat
  angepasst werden.
- **Alle drei Sprachversionen löschen**, nicht nur die deutsche – sonst bleibt z. B. die
  französische Version eines eigentlich entfernten Bereichs weiter online erreichbar
  (auch wenn sie im deutschen Menü nicht mehr auftaucht).
- **Interne Links prüfen:** Der automatische Link-Check (Kurzguide, Abschnitt 7) macht
  den nächsten Build zuverlässig rot, falls eine andere Seite noch auf den gelöschten
  Bereich verweist – das zeigt zuverlässig, wo noch aufgeräumt werden muss, sollte aber
  nicht einfach ignoriert werden, nur weil die Seite trotzdem online bleibt (siehe
  Kurzguide, Abschnitt 7: ein roter Build heisst nicht "offline", aber sollte trotzdem
  zeitnah behoben werden).
- **Zugehörige Downloads/Bilder** unter `assets/downloads/`, `static/downloads/` bzw.
  `assets/images/` werden beim Löschen der Seite **nicht automatisch mitgelöscht** – bei
  Bedarf separat entfernen, sonst bleiben verwaiste Dateien im Repo liegen (kein
  Sicherheitsproblem, nur unnötiger Ballast).

---

## 16. Wo hört "nur Copy-Paste" auf?

Die allermeisten Alltagsaufgaben in diesem Dokument und im Kurzguide sind reines Ausfüllen
bestehender Muster – Frontmatter-Felder setzen, YAML-Einträge ergänzen, Dateien
hochladen. Das reicht bewusst so weit wie möglich, damit Team-Mitglieder ohne
Hugo-Kenntnisse die Website selbstständig pflegen können.

**Folgende Aufgaben brauchen echte Hugo-/Web-Kenntnisse** und sollten an jemanden mit
diesem Hintergrund gehen (oder an einen KI-Assistenten mit Zugriff aufs Repo, der die
bestehenden Muster in `layouts/` versteht) statt per Trial-and-Error selbst versucht zu
werden:

- Eine **neue Art** von Seite/Komponente einführen, die es so noch nicht gibt (z. B. eine
  völlig neue Sektion auf der Startseite, ein neuer Formular-Typ, ein neues
  interaktives Element).
- Änderungen an Dateien unter `layouts/` (das eigentliche Design/die
  Seitenstruktur-Logik) oder an `.github/workflows/` (die Automatisierung).
- Eine neue Schriftart einbinden, die noch nicht vorbereitet ist.
- Das Favicon neu erzeugen (siehe Abschnitt 3 – braucht ein externes Werkzeug).
- Alles, wobei unklar ist, ob eine Änderung an einer Stelle unbeabsichtigt eine andere
  Stelle der Website mitbeeinflusst (z. B. weil eine Datei von mehreren Seiten
  gleichzeitig verwendet wird, wie `data/subtests.yaml` oder die Farbvariablen in
  `assets/css/style.css`).

**Faustregel:** Wenn eine Änderung sich als "Feld X in Datei Y auf Wert Z setzen"
beschreiben lässt und Y eine der in diesem Dokument genannten Dateien ist – selbst
machen. Wenn dafür neuer HTML/CSS/Template-Code geschrieben werden müsste, der so noch
nirgends im Projekt existiert – Hilfe holen.

---

## 17. Startseite: die Kacheln "Was du hier findest"

Direkt unter dem Hero steht seit dem 8. September 2026 ein Raster mit sechs Kacheln:
Übungsaufgaben, Testsimulationen, Vorbereitungskurse, Uniguide, Erfahrungsberichte,
Fragen & Antworten. Jede nennt eine grosse Zahl, den Bereich und einen Satz dazu.

Der Grund: Die Startseite zeigte vorher nur Hero, News, die acht Untertest-Kacheln, drei
Mission-Sätze und den Spendenaufruf. Der gesamte tatsächliche Bestand – über 150
Übungs-PDFs, die Testsimulationen, die Kursskripte, der Uniguide, die Erfahrungsberichte –
tauchte auf der Startseite nirgends auf. Die Seite wirkte dadurch leerer, als sie ist.

### Die Zahlen niemals von Hand eintragen

Sie werden bei **jedem Bauen der Website neu gezählt**: die PDFs direkt in den Ordnern
unter `assets/downloads/`, die Erfahrungsberichte aus den Seiten im jeweiligen
Sprachordner, die Universitäten und Fragen aus `data/unis.yaml` bzw. `data/faq.yaml`.
Werden zehn neue Übungsserien hochgeladen, steht dort beim nächsten Build automatisch die
neue Zahl.

Deshalb gehört in die Texte der Kacheln **keine Zahl** – sie wäre beim nächsten Upload
sofort falsch, während die grosse Zahl daneben stimmt.

Weil die Erfahrungsberichte nicht in allen Sprachen gleich weit übersetzt sind, zählt
jede Sprachfassung ihre eigenen (aktuell 66 auf Deutsch, 13 auf Französisch, 4 auf
Italienisch). Es steht also nie eine Zahl da, die es in dieser Sprache gar nicht gibt.

### Texte ändern

Überschrift und Kacheltexte stehen im Frontmatter der Startseite unter `angebot:` – und
zwar in **allen drei** Sprachdateien `content/de/_index.md`, `content/fr/_index.md`,
`content/it/_index.md`:

```yaml
angebot:
  eyebrow: "Was du hier findest"
  heading: "Alles kostenlos, alles von Studierenden gemacht"
  items:
    - key: uebungsaufgaben       # legt fest, was gezählt und wohin verlinkt wird
      title: "Übungsaufgaben"    # Überschrift der Kachel
      unit: "PDFs"               # steht klein neben der Zahl
      text: "Übungsserien zu allen acht Themenbereichen ..."
      link: "Zu den Übungsaufgaben →"
```

`key` ist der einzige Wert, der **nicht** übersetzt wird – er ist der interne Name und
muss in allen drei Sprachen gleich bleiben. Erlaubt sind: `uebungsaufgaben`,
`testsimulationen`, `vorbereitungskurse`, `uniguide`, `erfahrungsberichte`, `qa`.

Beim Übersetzen der Einheit (`unit`) darauf achten, dass sie zu einer **Mehrzahl** passt –
sie steht immer direkt hinter einer Zahl.

### Eine Kachel entfernen oder umsortieren

Den Eintrag in allen drei Dateien löschen bzw. verschieben. Das Raster richtet sich
automatisch nach der Anzahl; es müssen keine Spalten angepasst werden.

### Eine ganz neue Kachel

Dafür braucht es zusätzlich eine Ergänzung im Template
(`layouts/partials/angebot-grid.html`, Block `$quellen`): Dort steht pro `key`, welche
Zieladresse verlinkt und was gezählt wird. Das ist ein Entwickler-Schritt (Abschnitt 16) –
die Datei erklärt oben im Kommentar, was einzutragen ist.

---

## 18. Prüfungsmodus: Uhr, Ansagen und der Testablauf

Die Seite `/ems/pruefungsmodus/` stellt die Prüfungsbedingungen her: Anweisung
vorlesen, Zeit nehmen, "Stopp" sagen – einzeln oder für den ganzen Testtag.
Der Kurzguide (Abschnitt 14) erklärt, wie man Zeiten und Sätze ändert. Hier
steht, wie es aufgebaut ist.

### Eine Quelle für den Testablauf

`data/testablauf.yaml` enthält die elf Blöcke in der Reihenfolge des Testtags,
mit Dauer, Aufgabenzahl, Punktzahl und den Namen in allen drei Sprachen. Diese
Datei speist zwei Dinge:

| Wo | Wie |
| --- | --- |
| Tabelle „Tagesablauf" auf `/ems/` | Shortcode `testablauf`, siehe `layouts/shortcodes/testablauf.html` |
| Prüfungsmodus | `layouts/partials/pruefungsmodus.html` |

Die **Gesamtzeit** in der Tabelle wird aus den Einzelminuten zusammengezählt und
nicht eingetragen – sie kann dadurch gar nicht von den Einzelwerten abweichen.
Wer eine Dauer ändert, sieht die neue Gesamtzeit automatisch.

### Warum die Uhr nicht Sekunden zählt

Browser verlangsamen Zeitgeber in Hintergrund-Tabs. Eine Uhr, die einfach
Sekunden herunterzählt, ginge nach einer 45-Minuten-Runde deutlich falsch. Der
Prüfungsmodus merkt sich deshalb einen festen **Endzeitpunkt** und rechnet bei
jedem Bildaufbau die Differenz zur echten Uhrzeit aus. Wer daran etwas ändert,
sollte diesen Punkt kennen – es ist der Unterschied zwischen einer Übungsuhr und
einer, der man nicht trauen kann.

### Vorlesen

Über `SpeechSynthesis`, die Sprachausgabe des Browsers. Bewusst kein externer
Dienst und keine hochgeladenen Audiodateien:

- kein fremder Server erfährt, wer hier übt
- es sind keine Dateien zu pflegen
- es funktioniert automatisch in allen drei Sprachen, weil die Stimme der
  Seitensprache folgt (`lang`-Attribut am `html`-Tag)

Der Preis ist die maschinelle Stimme. **Sollen es echte Aufnahmen werden**, ist
im Skript nur die Funktion `sprich` auszutauschen: Sie bekommt einen Text und
eine Funktion, die aufgerufen wird, wenn fertig gesprochen ist – der ganze
übrige Ablauf hängt nur an dieser Zusage. Für Aufnahmen bräuchte es dann pro
Untertest und Sprache je eine Datei, also rund 35 Aufnahmen.

Wichtig beim Übersetzen der `pm_`-Einträge in `i18n/*.yaml`: Diese Sätze werden
**gesprochen**. Klammern, Abkürzungen und Halbsätze klingen vorgelesen falsch.

### Weitere Details, die leicht übersehen werden

- **Bildschirm bleibt an:** Über die Wake-Lock-Funktion des Browsers – sonst
  geht der Bildschirm mitten in einem 45-Minuten-Block aus, also genau dann,
  wenn man die Uhr braucht. Unterstützt das Gerät sie nicht, läuft alles normal
  weiter, der Bildschirm kann dann aber abschalten.
- **Vollbild ist nur eine Zugabe:** Die Bühne liegt ohnehin als fest
  positionierte Fläche über der Seite. Verlässt jemand das Vollbild mit Esc,
  bleibt die Übung sichtbar und läuft weiter.
- **Die Pause gibt es am echten EMS nicht.** Sie ist absichtlich eingebaut und
  ebenso absichtlich beschriftet („Am echten EMS gibt es keine Pause – diese
  hier gibt es nur zum Üben"). Zwischen zwei Blöcken der Simulation gibt es
  dagegen keine Rückfrage, nur die kurze Umblätter-Zeit aus
  `umblaettern_sekunden` in `data/testablauf.yaml`.
- **`safeJS` im Partial nicht entfernen.** Die Blöcke und Texte werden als JSON
  an das Skript übergeben. Ohne diesen Zusatz verpackt Hugo den fertigen
  JSON-Text ein zweites Mal, im Browser käme Text statt Daten an – und die
  Seite bliebe stumm, ohne sichtbare Fehlermeldung.
