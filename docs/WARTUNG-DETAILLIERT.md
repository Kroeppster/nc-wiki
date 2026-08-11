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
`content/it/...`) ist **keine Datenliste**, sondern ganz normaler Markdown-Fliesstext mit
Überschriften und Aufzählungen – neue Team-Mitglieder werden einfach als neue
Aufzählungspunkte unter der passenden Überschrift ergänzt bzw. beim Saisonwechsel der
ganze Abschnitt "Aktuelles Leitungsteam" durch die neue Besetzung ersetzt (die bisherige
Besetzung wandert dann sinnvollerweise unter "Frühere Saisons", nach demselben Muster
wie die bereits dort stehenden Jahrgänge).

Da es sich um drei separate Dateien handelt (eine pro Sprache), muss eine Namensänderung
oder ein neues Teammitglied in allen dreien nachgezogen werden, damit die Seite überall
gleich aktuell ist.

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
  bekannt, steht dort bewusst `"TODO: prüfen"` statt einer geratenen Zahl – das sollte so
  bleiben, bis der echte Wert auf der offiziellen Uni-Website nachgeprüft wurde. Bei
  jeder inhaltlichen Änderung auch das Feld `stand:` (Datum der letzten Prüfung)
  aktualisieren.

---

## 8. Untertests verwalten

Die "9 Untertests"-Übersicht (Startseite, Übungsaufgaben-Raster, FAQ-Antwort) wird aus
`data/subtests.yaml` erzeugt. Jeder Eintrag hat eine Nummer, einen Namen (pro Sprache)
und einen Kurzbeschrieb. Ändert sich die offizielle Anzahl oder Reihenfolge der
EMS-Untertests (kommt selten vor, aber offiziell schon vorgekommen), hier die Liste
anpassen – die Startseite, das Übungsaufgaben-Raster und die FAQ-Antwort ziehen die Zahl
automatisch aus dieser Datei nach, nirgends muss die Zahl von Hand an mehreren Stellen im
Text geändert werden.

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
| "Fehler melden" bei PDF-Downloads | `layouts/partials/download-list.html` |

Um ein Formular an ein anderes Formspree-Konto/-Formular umzuhängen: die Adresse in der
jeweiligen Datei ersetzen. Der Zugang zum Formspree-Konto selbst (Login) gehört in den
gemeinsamen Passwort-Manager des Teams, nicht ins Repo (siehe Kurzguide, Abschnitt 6).

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
  --color-accent:#E2792E;
  --font-display:'Space Grotesk','Arial Narrow',sans-serif;
  --font-body:'Source Sans 3',system-ui,-apple-system,sans-serif;
  ...
}
```

Eine Variable dort ändern (z. B. `--color-signal`) wirkt sich **automatisch überall** auf
der Website aus, wo diese Farbe verwendet wird (Knöpfe, Links, Hervorhebungen) – nicht
einzeln pro Seite oder Element ändern.

**Wichtig: Zwei getrennte Paletten für Hell- und Dunkelmodus.** Direkt unter dem ersten
`:root{...}`-Block (helle Palette) folgt weiter unten in derselben Datei ein zweiter
Block `:root[data-theme="dark"]{...}` mit denselben Variablennamen, aber den Werten für
den Dunkelmodus. **Beide Blöcke müssen bei einer Farbänderung zusammen angepasst
werden**, sonst stimmt z. B. die Primärfarbe im Hellmodus, aber im Dunkelmodus steht dort
noch die alte Farbe (oder ein schlecht lesbarer Kontrast).

**Schriftarten austauschen:** In `--font-display`/`--font-body`/`--font-mono` die erste
Schriftart in der Liste ersetzen (die folgenden Namen sind reine Rückfall-Schriften,
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
