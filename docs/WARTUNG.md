# Wartung der NCWiki-Website

Diese Anleitung ist für Leute, die die Website pflegen sollen, aber **Hugo nicht kennen
und nur einen Browser** haben – kein Programm muss installiert werden. Alles hier geht
über die normale GitHub-Weboberfläche (github.com).

Wer doch lokal arbeiten will/kann: dann helfen `docs/vorlage-news.md`,
`docs/vorlage-erfahrungsbericht.md` und die Dateien in `archetypes/` zusätzlich weiter.

---

## 1. Aufbau des Projekts in einfachen Worten

Die Website wird aus einfachen Textdateien gebaut. Man schreibt eine Textdatei, lädt sie
ins Repository ("Repo") hoch, und ein Roboter (GitHub Actions, siehe Abschnitt 8) baut
daraus automatisch die fertige Website neu – innerhalb von ein bis zwei Minuten.

Die wichtigsten Ordner:

| Ordner | Was steckt drin | Muss ich das anfassen? |
| --- | --- | --- |
| `content/` | Alle Texte der Website, aufgeteilt nach Sprache. **Das ist der Ordner, mit dem du fast immer arbeitest.** | Ja, ständig |
| `content/de/`, `content/fr/`, `content/it/` | Dieselbe Seitenstruktur, einmal pro Sprache. Deutsch ist die Hauptsprache. | Ja |
| `data/` | Tabellenartige Daten als Textdatei (FAQ, Sponsor:innen-Liste, Uni-Liste, Anzeigenamen für PDFs) | Gelegentlich |
| `assets/downloads/` und `static/downloads/` | PDF-Dateien | Ja, beim Hochladen von Material (siehe Abschnitt 3) |
| `archetypes/`, `docs/vorlage-*.md` | Fertige Vorlagen zum Kopieren für neue Seiten | Als Hilfe, nicht bearbeiten |
| `layouts/`, `hugo.toml`, `i18n/` | Das Design, die Seitenstruktur-Logik und feste Bedienelement-Texte (Knöpfe, Menüs) der ganzen Website | **Nein** – hier braucht es Hugo-Kenntnisse, im Zweifel jemanden fragen, der/die sich damit auskennt |
| `.github/workflows/` | Die Automatisierung (Bauen, Veröffentlichen, Link-Prüfung) | Nein |

Innerhalb von `content/<sprache>/` gibt es einen Ordner pro Themenbereich (z. B. `news/`,
`ems/erfahrungsberichte/`, `ueber-uns/jahresberichte/`). Zwei Arten von Dateien:

- **`_index.md`** – der Text für die Übersichtsseite eines Ordners selbst (z. B.
  `content/de/news/_index.md` ist die Einleitung ganz oben auf der News-Übersicht).
- **Alle anderen `.md`-Dateien** – je eine einzelne Unterseite (ein News-Beitrag, ein
  Erfahrungsbericht, usw.).

Jede Datei beginnt mit einem Block zwischen zwei `---`-Zeilen (das "Frontmatter") –
das sind strukturierte Angaben wie Titel oder Datum, kein normaler Fliesstext. Danach
kommt der eigentliche Inhalt als normaler Text (Markdown: `**fett**`, `[Link](url)`,
Zeilen mit `- ` für Listen).

---

## 2. Wie lege ich eine neue Seite an?

**Für News-Beiträge und Erfahrungsberichte** gibt es fertige Copy-Paste-Vorlagen –
diese zuerst anschauen, dort ist alles Schritt für Schritt erklärt:

- News-Beitrag → [`docs/vorlage-news.md`](vorlage-news.md)
- Erfahrungsbericht → [`docs/vorlage-erfahrungsbericht.md`](vorlage-erfahrungsbericht.md)
  (der normale Weg dafür ist aber das Formular auf der Website selbst, nicht diese Datei –
  siehe dort)

**Für einen Jahresbericht:** wie ein normaler PDF-Upload mit eigener Seite, siehe
Abschnitt 3 weiter unten (Fall B) sowie `archetypes/jahresbericht.md` als Vorlage.

**Für alle anderen, ganz normalen Seiten** (z. B. eine neue Unterseite unter "Über uns"):

1. Im Repo zum passenden Ordner unter `content/de/...` navigieren.
2. **"Add file" → "Create new file"** klicken.
3. Dateiname vergeben: klein geschrieben, keine Umlaute (ä→ae, ö→oe, ü→ue, ß→ss), keine
   Leerzeichen (mit `-` ersetzen), endet auf `.md`. Der Dateiname wird Teil der
   Web-Adresse.
4. Frontmatter + Text eingeben, mindestens:

   ```markdown
   ---
   title: "Titel der Seite"
   draft: true
   ---

   Text der Seite hier.
   ```

5. Soll die Seite im Hauptmenü erscheinen, zusätzlich einen `menu`-Block einfügen (nur
   bei Übersichtsseiten/`_index.md` eines neuen Ordners sinnvoll, nicht bei jeder
   Unterseite):

   ```yaml
   menu:
     main:
       parent: ueber-uns
       weight: 5
   ```

   `parent` ist der Menüpunkt, unter dem die Seite erscheinen soll (siehe die anderen
   `_index.md`-Dateien im selben Bereich für Beispiele), `weight` bestimmt die
   Reihenfolge (kleinere Zahl = weiter oben/vorne).
6. Unten bei "Commit changes" **"Create a new branch for this commit and start a pull
   request"** wählen, nicht direkt in `main` speichern.
7. Pull Request erstellen. Jemand aus dem Team schaut kurz drüber und merged ihn.
8. Erst wenn die Seite fertig und geprüft ist: `draft: true` in der Datei auf
   `draft: false` ändern (neuer Commit/PR) – sonst bleibt sie unsichtbar, auch nach dem
   Merge.

**Für Text in mehreren Sprachen:** dieselbe Datei mit demselben Namen zusätzlich unter
`content/fr/...` bzw. `content/it/...` anlegen, mit übersetztem Inhalt. Nicht Pflicht,
aber schön, wenn's geht.

---

## 3. Wie füge ich ein PDF hinzu?

Es gibt zwei verschiedene Wege, je nachdem, worum es geht.

### Fall A: Übungsserie, Testsimulation oder Kursskript

Das sind die Materialien unter "Übungsaufgaben", "Testsimulationen" und
"Vorbereitungskurse". Dafür reicht es, die PDF-Datei einfach in den richtigen Ordner
hochzuladen – **kein Frontmatter, kein Code nötig**, sie erscheint automatisch:

1. Zum passenden Ordner navigieren:
   - Testsimulationen: `assets/downloads/testsimulationen/`
   - Kursskripte: `assets/downloads/kursskripte/`
   - Übungsserien: `assets/downloads/uebungsaufgaben/<untertest>/` (ein Unterordner pro
     Untertest, z. B. `muster-zuordnen`, `textverstaendnis` – die Ordnernamen stehen
     schon da)
2. **"Add file" → "Upload files"**, PDF hochladen, Pull Request erstellen wie oben.
3. Der angezeigte Name wird automatisch aus dem Dateinamen abgeleitet (z. B.
   `2027_Muster_A1.pdf` → "Muster – A1 (2027)"). Soll stattdessen ein schönerer,
   von Hand gewählter Name erscheinen: einen Eintrag in `data/downloads.yaml`
   ergänzen (dort steht ein Beispiel für das Format, inkl. Übersetzung pro Sprache).

### Fall B: Jahresbericht oder sonstiges Einzeldokument

Für alles, was nicht in Fall A passt (z. B. ein Jahresbericht), braucht die PDF-Datei
eine eigene Seite mit Frontmatter:

1. PDF hochladen nach `static/downloads/<bereich>/<dateiname>.pdf`, z. B.
   `static/downloads/jahresberichte/2027.pdf` (Ordner ggf. beim Hochladen neu anlegen).
2. Eine neue Seite anlegen wie in Abschnitt 2 beschrieben, mit einem `downloads`-Block
   im Frontmatter:

   ```yaml
   downloads:
     - path: "downloads/jahresberichte/2027.pdf"
       label: "Jahresbericht 2027 (PDF)"
   ```

   `path` ist der Pfad relativ zu `static/` (ohne `static/` davor), `label` der
   angezeigte Linktext. Die Dateigrösse wird automatisch dazu ergänzt.

   Für Jahresberichte gibt's dafür eine fertige Vorlage: `archetypes/jahresbericht.md`.

---

## 4. Wie schreibe ich einen News-Beitrag?

Kurzfassung (Details und fertiger Copy-Paste-Block in
[`docs/vorlage-news.md`](vorlage-news.md)):

1. Neue Datei unter `content/de/news/dein-titel.md` anlegen (siehe Abschnitt 2).
2. Frontmatter mit `title`, `date`, `eyebrow` (kurzes Schlagwort wie "Update") und
   `draft: true` ausfüllen.
3. Darunter den Beitragstext schreiben – die ersten Sätze erscheinen automatisch als
   Vorschau auf der News-Übersicht und der Startseite.
4. Pull Request erstellen, prüfen lassen, mergen, `draft: false` setzen.

---

## 5. Welche Drittdienste sind im Einsatz – und wofür?

| Dienst | Wofür | Wo im Code sichtbar |
| --- | --- | --- |
| **GitHub Pages** | Hosting der fertigen Website. Aktuell erreichbar unter `kroeppster.github.io/nc-wiki/`; ein Umzug auf die eigene Domain `nc-wiki.ch` ist technisch vorbereitet, aber noch nicht aktiv (keine `CNAME`-Datei im Repo, DNS noch nicht umgestellt). | `.github/workflows/hugo.yml` |
| **GitHub Actions** | Baut die Website bei jeder Änderung an `main` automatisch neu und prüft dabei, ob interne Links noch stimmen (siehe Abschnitt 8). Kein eigenständiger Dienst, sondern Teil von GitHub selbst. | `.github/workflows/` |
| **Formspree** | Nimmt Formular-Einsendungen entgegen, da die Website selbst keinen eigenen Server hat. Drei Formulare sind eingerichtet: Kontaktformular (`kontakt`-Seite), Erfahrungsbericht-Formular (löst zusätzlich automatisch einen Pull Request aus, siehe `.github/workflows/erfahrungsbericht-intake.yml`), und ein "Fehler melden"-Link bei jedem PDF-Download – **letzterer ist noch nicht fertig eingerichtet** (zeigt aktuell `REPLACE_ME` in `layouts/partials/download-list.html`, muss noch durch eine echte Formspree-Adresse ersetzt werden). | `layouts/partials/contact-form.html`, `experience-form.html`, `download-list.html` |
| **Pagefind** | Die Suchfunktion oben im Header. Läuft komplett im Browser der Besucher:innen, kein externer Dienst zur Laufzeit – wird nur beim Bauen der Website als durchsuchbarer Index generiert. | `.github/workflows/hugo.yml`, `package.json` |
| **Newsletter** | **Noch nicht angebunden.** In `hugo.toml` gibt es dafür schon ein Feld (`newsletter_url` unter `[params]`), aber es ist absichtlich leer – der Newsletter-Block im Footer erscheint erst, sobald dort eine echte Anmelde-URL eines Newsletter-Anbieters (z. B. Mailchimp) eingetragen wird. | `hugo.toml`, `layouts/partials/footer.html` |
| **Instagram / Discord** | Nur als Links im Footer verlinkt (aus `hugo.toml`), keine technische Integration. | `hugo.toml` |

---

## 6. Wo ist dokumentiert, wer welche Zugänge hat?

**Ehrliche Antwort: aktuell nirgends im Repository – und das ist so beabsichtigt.**
Passwörter, Tokens und Zugangsdaten gehören nie in git, auch nicht in eine "private"
Datei dort – die komplette Historie eines Repos bleibt für immer einsehbar, selbst wenn
eine Datei später wieder gelöscht wird.

Diese Zuordnung gehört stattdessen in einen gemeinsamen Passwort-Manager fürs Team
(z. B. eine Bitwarden- oder 1Password-Organisation). Falls es noch keinen gibt, wäre
das Einrichten eines solchen sinnvoll – darin sollte mindestens festgehalten werden:

- **GitHub:** wer Owner/Admin des Repos `Kroeppster/nc-wiki` ist.
- **Formspree:** Login-Zugang zum Konto, und welches der drei Formulare
  (`mvkpgrpl`, `xaewqwoj`, das noch fehlende dritte) wozu gehört, sowie welche
  E-Mail-Adresse die Einsendungen empfängt.
- **Der GitHub-Zugriffstoken, der in den Formspree-Einstellungen des
  Erfahrungsbericht-Formulars hinterlegt ist** – er ermöglicht Formspree, automatisch
  einen Pull Request in diesem Repo zu öffnen. Diese Verbindung ist nur im
  Formspree-Dashboard konfiguriert, im Code selbst nicht sichtbar.
- **Instagram / Discord:** wer Admin-Rechte hat.
- **Domain `nc-wiki.ch`:** bei welchem Registrar sie liegt und wer dort Zugriff hat
  (relevant für den geplanten Umzug weg vom `github.io`-Unterpfad).

---

## 7. Was tun, wenn der Build rot wird?

**Wichtig zu wissen: ein roter Build heisst nicht, dass die Website offline ist.** Die
zuletzt erfolgreich gebaute Version bleibt online, bis der Fehler behoben ist und ein
neuer Build erfolgreich durchläuft. Es besteht also kein Zeitdruck, aber der Fix sollte
trotzdem zeitnah passieren, sonst fehlen neuere Änderungen auf der Live-Seite.

**Auch wichtig:** Die Prüfung läuft **nicht** direkt auf einem Pull Request, sondern erst
*nachdem* er in `main` gemerged wurde. Man sieht also keine rote Markierung beim
Erstellen des Pull Requests selbst – erst danach, im Actions-Tab.

**So findet man die Ursache:**

1. Oben im Repo auf den Tab **"Actions"** klicken.
2. Der oberste Eintrag mit rotem ✗ ist der fehlgeschlagene Build.
3. Darauf klicken, dann auf den Job **"build"**.
4. Der Schritt mit dem roten ✗ ist die Fehlerquelle – aufklappen und den roten Text
   lesen. Meistens wird darin der betroffene Dateiname direkt genannt.

**Häufigste Ursachen:**

| Fehlgeschlagener Schritt | Typische Ursache | Was tun |
| --- | --- | --- |
| "Check internal links" | Ein Link in einer Seite zeigt auf eine Adresse, die es nicht (mehr) gibt (z. B. Tippfehler, oder eine verlinkte Seite wurde gelöscht/umbenannt). | In der genannten Datei den Link korrigieren. |
| "Build with Hugo" | Fehler im Frontmatter einer Datei – meist ein fehlendes Anführungszeichen, eine falsche Einrückung, oder ein Pflichtfeld fehlt (z. B. Bild ohne `featured_image_alt`). | Die genannte Datei/Zeile öffnen und mit einer ähnlichen, funktionierenden Datei vergleichen. |

Der Schritt **"Check external links"** kann rot **im Job-Summary** auftauchen (defekte
Links zu anderen Websites, z. B. weil die verlinkte Seite umgezogen ist), lässt den
Build selbst aber absichtlich **nicht** fehlschlagen – das ist nur eine Warnung, kein
Grund zur Eile.

**Wenn man selbst nicht weiterkommt:** ein Issue im Repo eröffnen (Tab "Issues" →
"New issue") mit einem Link zum fehlgeschlagenen Actions-Lauf, damit jemand mit
Hugo-Kenntnissen es sich anschauen kann.
