# Wartung der NCWiki-Website

Diese Anleitung ist für Leute, die die Website pflegen sollen, aber **Hugo nicht kennen
und nur einen Browser** haben – kein Programm muss installiert werden. Alles hier geht
über die normale GitHub-Weboberfläche (github.com).

Wer doch lokal arbeiten will/kann: dann helfen `docs/vorlage-news.md`,
`docs/vorlage-erfahrungsbericht.md` und die Dateien in `archetypes/` zusätzlich weiter.

Dies ist die **Kurzfassung** für die alltäglichen Aufgaben (neue Seite, PDF hochladen,
News schreiben, Datei löschen, Bild einfügen). Für alles Seltenere – Navigation umbauen,
Logo/Sponsor:innen/Team pflegen, Farben & Design, Countdown-Datum, Google Analytics,
Formulare, Übersetzungsdateien und mehr – siehe die ausführliche Version:
[`docs/WARTUNG-DETAILLIERT.md`](WARTUNG-DETAILLIERT.md).

---

## 1. Aufbau des Projekts in einfachen Worten

Die Website wird aus einfachen Textdateien gebaut. Man schreibt eine Textdatei, lädt sie
ins Repository ("Repo") hoch, und ein Roboter (GitHub Actions, siehe Abschnitt 7) baut
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
| **GitHub Actions** | Baut die Website bei jeder Änderung an `main` automatisch neu und prüft dabei, ob interne Links noch stimmen (siehe Abschnitt 7). Kein eigenständiger Dienst, sondern Teil von GitHub selbst. | `.github/workflows/` |
| **Formspree** | Nimmt Formular-Einsendungen entgegen, da die Website selbst keinen eigenen Server hat. Drei Formulare sind eingerichtet: Kontaktformular (`kontakt`-Seite), Erfahrungsbericht-Formular (löst zusätzlich automatisch einen Pull Request aus, siehe `.github/workflows/erfahrungsbericht-intake.yml`), und ein Fehlermelde-Formular auf der Übungsaufgaben-Übersicht. **Letzteres teilt sich vorläufig die Adresse mit dem Kontaktformular**, weil es dafür noch kein eigenes Formspree-Formular gibt – die Meldungen landen also im Kontakt-Postfach und sind dort am Betreff „Fehlermeldung Uebungsaufgaben (Website)" erkennbar. | `layouts/partials/contact-form.html`, `experience-form.html`, `report-error-general.html` |
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
- **Das Passwort des Mitgliederbereichs** – auf GitHub als Secret `MITGLIEDER_PASSWORT`
  hinterlegt und dort nicht mehr auslesbar, nur überschreibbar. Deshalb gehört es
  zusätzlich in den Passwort-Manager, sonst kennt es irgendwann niemand mehr
  (siehe Abschnitt 11).
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

---

## 8. Wie lösche ich eine Datei?

Egal ob PDF, Bild oder eine ganze Seite (`.md`-Datei) – das Löschen läuft für jede Datei
gleich ab:

1. Im Repo zur Datei navigieren und sie anklicken, damit sie geöffnet wird.
2. Oben rechts auf das Papierkorb-Symbol klicken (bei manchen Dateitypen stattdessen über
   die drei Punkte "..." → "Delete file").
3. Unten bei "Commit changes" – genau wie beim Anlegen einer Seite (Abschnitt 2) –
   **"Create a new branch for this commit and start a pull request"** wählen, nicht
   direkt in `main` speichern.
4. Pull Request erstellen. Jemand aus dem Team schaut kurz drüber und merged ihn.

Nach dem Merge verschwindet die Datei automatisch von der Live-Seite (derselbe
automatische Bau-Vorgang wie bei jeder anderen Änderung).

**Achtung bei Übungsserien-PDFs:** Löscht man nur die Aufgaben-Datei, aber nicht die
zugehörige `..._Loesung`-Datei (oder umgekehrt), bleibt die andere als eigener,
einzelner Eintrag stehen (siehe `assets/downloads/uebungsaufgaben/README.md`) – meist
will man beide zusammen löschen.

**Falls die gelöschte Datei noch irgendwo verlinkt ist:** Der automatische Link-Check
(Abschnitt 7) macht den nächsten Build rot, sobald ein interner Link ins Leere zeigt –
das ist gewollt und zeigt zuverlässig, wo noch aufgeräumt werden muss.

---

## 9. Wie füge ich ein Bild hinzu?

Bilder werden nicht mitten im Fliesstext eingefügt, sondern als **ein** Titelbild pro
Seite (erscheint oben auf der Seite selbst und als Vorschaubild in Übersichten, z. B.
bei News-Beiträgen).

1. Bilddatei hochladen nach `assets/images/<bereich>/<dateiname>.jpg` (oder `.png`),
   z. B. `assets/images/news/testsimulation-2027.jpg` – **"Add file" → "Upload files"**,
   Pull Request erstellen wie in Abschnitt 2 beschrieben.
2. Im Frontmatter der Seite zwei Felder ergänzen:

   ```yaml
   featured_image: "news/testsimulation-2027.jpg"
   featured_image_alt: "Kurze Bildbeschreibung für Screenreader"
   ```

   `featured_image` ist der Pfad relativ zu `assets/images/` (ohne `assets/images/`
   davor). `featured_image_alt` ist **Pflicht**, sobald ein Bild gesetzt ist – ohne
   Beschreibung schlägt der Bau der Website fehl (wichtig für Sehbehinderte, die die
   Seite per Screenreader nutzen). Eine Vorlage mit beiden Feldern gibt es in
   `archetypes/news.md`.

Hugo erzeugt daraus beim Bauen automatisch mehrere verkleinerte Kopien – nichts
weiter nötig, auch nicht bei sehr grossen Originaldateien.

---

## 10. Wie zeige ich einen Teil eines Beitrags erst ab einer bestimmten Uhrzeit?

Für Fälle wie "der Anmeldelink soll erst heute Abend um 22:00 Uhr sichtbar werden" –
der Rest des Beitrags bleibt sofort sichtbar, nur der markierte Teil erscheint
automatisch zum eingetragenen Zeitpunkt (ohne dass jemand die Seite neu laden muss).

Im Beitragstext den betreffenden Teil so einrahmen:

```
{{< reveal-at when="2026-08-10T22:00:00+02:00" >}}
[Jetzt anmelden](https://...)
{{< /reveal-at >}}
```

`when` ist Datum und Uhrzeit im Format `JJJJ-MM-TTTHH:MM:SS+ZZ:ZZ` – die Zeitzone am
Ende **muss** dabei sein (`+02:00` = Schweizer Sommerzeit, `+01:00` = Winterzeit),
sonst ist nicht eindeutig gemeint, wann genau. Fehlt `when` oder ist das Datum
ungültig, bleibt der Inhalt absichtlich für immer versteckt statt sofort zu
erscheinen.

**Wichtig zu wissen:** Das Verstecken passiert nur im Browser (per CSS/JavaScript) –
im Seiten-Quelltext steht der Inhalt schon vor dem Freigabe-Zeitpunkt, nur unsichtbar.
Für einen Link, der zur richtigen Zeit öffentlich auffindbar werden soll, reicht das
– für etwas, das wirklich geheim bleiben muss (z. B. ein Passwort), nicht geeignet.

---

## 11. Mitgliederbereich (passwortgeschützte Seiten)

Unter `content/de|fr|it/mitglieder/` liegen Seiten, die nicht zufällig gefunden werden
sollen – aktuell die Mitgliederevents und das Spesenformular. Sie sind **absichtlich
nicht im Menü verlinkt** und bekommen beim Veröffentlichen eine Passwort-Abfrage
vorgeschaltet.

### Was der Schutz leistet – und was nicht

**Bitte einmal ganz lesen, bevor etwas in diesen Bereich gestellt wird.**

Der Schutz hält Suchmaschinen und zufällige Besucher:innen zuverlässig fern. Er ist
**kein richtiger Login**:

- Alle Mitglieder teilen sich **ein** Passwort. Wer es weitergibt, lässt sich nicht
  einzeln aussperren – es hilft nur, das Passwort für alle zu ändern.
- Die verschlüsselte Seite liegt öffentlich im Netz. Wer sie herunterlädt, kann in
  aller Ruhe Passwörter durchprobieren, ohne dass das jemand bemerkt oder bremst.
  Deshalb **muss** das Passwort lang und zufällig sein (siehe unten).
- **Die verlinkten PDF-Dateien sind nicht geschützt.** Nur die *Seite* liegt hinter
  dem Passwort. Die PDFs selbst liegen ganz normal auf dem Webserver und sind für
  jede Person abrufbar, die ihre genaue Adresse kennt oder errät. Der Schutz besteht
  praktisch darin, dass diese Adressen nirgends öffentlich stehen – nicht darin, dass
  der Server jemanden abweisen würde.

Daraus folgt: In den Mitgliederbereich gehören interne Termine, Formulare und
Merkblätter – also Dinge, die schlicht niemanden ausserhalb des Vereins interessieren.
**Nicht** hierher gehören Personendaten von Mitgliedern, Kontoauszüge,
Bewerbungsunterlagen oder sonst irgendetwas, dessen Veröffentlichung echten Schaden
anrichten würde.

### Wie füge ich eine neue geschützte Seite hinzu?

Genau wie jede andere Seite (siehe Abschnitt 2), mit **einer** Ergänzung im
Frontmatter – und wie immer in allen drei Sprachen:

```
---
title: "Titel der Seite"
geschuetzt: true
---
```

Das `geschuetzt: true` erledigt alles Weitere automatisch: Die Seite bekommt
`noindex`, fällt aus der Suchfunktion, aus der `sitemap.xml` und aus allen
RSS-Feeds heraus, und bekommt beim Veröffentlichen die Passwort-Abfrage.

Soll auf einer Seite eine automatische PDF-Liste erscheinen, zusätzlich:

```
download_ordner: "downloads/mitglieder"
```

Die PDFs kommen dann nach `assets/downloads/mitglieder/` (siehe die README-Datei
dort und Abschnitt 3).

### Wie ändere ich das Passwort?

Das Passwort steht **nicht im Repository** (es gehört dort auch nicht hin, siehe
Abschnitt 6), sondern in einem GitHub-Secret:

1. Auf GitHub im Repo `Kroeppster/nc-wiki` auf **Settings** → in der linken Spalte
   **Secrets and variables** → **Actions**.
2. Beim Eintrag **`MITGLIEDER_PASSWORT`** auf das Stift-Symbol klicken
   (bzw. **New repository secret**, falls er noch nicht existiert).
3. Neues Passwort eintragen und speichern. **Mindestens 16 zufällige Zeichen** – am
   besten vom Passwort-Manager erzeugen lassen, kein selbst ausgedachtes Wort.
4. Das Passwort wirkt erst nach dem nächsten Bauen der Website. Entweder auf die
   nächste inhaltliche Änderung warten, oder auf GitHub unter **Actions** den
   Workflow "Deploy Hugo site to GitHub Pages" auswählen und **Run workflow** auf
   `main` starten.
5. Das neue Passwort im gemeinsamen Passwort-Manager hinterlegen (Abschnitt 6) und
   den Mitgliedern mitteilen.

**Wo ist das Passwort dokumentiert?** Im gemeinsamen Passwort-Manager des Vereins,
zusammen mit den übrigen Zugängen – siehe Abschnitt 6. Nicht in git, nicht in einer
Datei im Repo, auch nicht in einer "privaten": Die Historie eines Repos bleibt für
immer einsehbar, auch wenn eine Datei später gelöscht wird.

### Der Build ist rot und meldet etwas mit "Kein Passwort gesetzt"

Dann fehlt das Secret `MITGLIEDER_PASSWORT` oder es ist falsch geschrieben. Der
Ablauf bricht an dieser Stelle **absichtlich** ab, statt den Mitgliederbereich
unverschlüsselt zu veröffentlichen. Secret wie oben beschrieben anlegen, danach den
Workflow erneut starten. Die zuletzt erfolgreich gebaute Version der Website bleibt
in der Zwischenzeit online (siehe Abschnitt 7).

Bei einem Pull Request ist das anders: Dort wird nur gewarnt und unverschlüsselt
weitergebaut, weil das Secret dort nicht immer zur Verfügung steht – veröffentlicht
wird bei einem Pull Request ohnehin nie.

### Lokal ausprobieren

`hugo server -D` zeigt die Seiten ganz normal ohne Passwort an – die Verschlüsselung
passiert erst beim Veröffentlichen. Wer die Passwort-Abfrage selbst sehen will:

```bash
npm run build
STATICRYPT_PASSWORD='test-passwort' npm run schuetzen
```

Danach liegt in `public/mitglieder/` die geschützte Fassung. Wichtig: `public/` ist
nur ein lokaler Bau-Ordner und landet nie in git.

---

## 12. Startseite: die Kacheln „Was du hier findest" ändern

Direkt unter dem Hero steht auf der Startseite ein Raster mit sechs Kacheln
(Übungsaufgaben, Testsimulationen, Vorbereitungskurse, Uniguide,
Erfahrungsberichte, Fragen & Antworten). Jede Kachel nennt eine grosse Zahl,
den Bereich und einen Satz dazu.

### Die Zahlen musst du nicht pflegen

Sie werden bei **jedem Bauen der Website neu gezählt**: die PDFs direkt in den
Ordnern unter `assets/downloads/`, die Erfahrungsberichte aus den Seiten im
jeweiligen Sprachordner, die Universitäten und Fragen aus `data/unis.yaml` bzw.
`data/faq.yaml`. Lädst du zehn neue Übungsserien hoch, steht dort beim nächsten
Build automatisch die neue Zahl.

**Deshalb bitte keine Zahlen in die Texte schreiben** – sie wären beim nächsten
Upload sofort falsch.

Weil die Erfahrungsberichte nicht in allen Sprachen gleich weit übersetzt sind,
zählt jede Sprachfassung ihre eigenen Berichte (aktuell 66 auf Deutsch, 13 auf
Französisch, 4 auf Italienisch). Es steht also nie eine Zahl da, die es in
dieser Sprache gar nicht gibt.

### Texte ändern

Überschrift und die Texte der Kacheln stehen im Frontmatter der Startseite,
unter `angebot:` – und zwar **in allen drei Sprachdateien**:

- `content/de/_index.md`
- `content/fr/_index.md`
- `content/it/_index.md`

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

`key` ist der einzige Wert, der **nicht** übersetzt wird – er ist der interne
Name und muss in allen drei Sprachen gleich bleiben. Erlaubt sind:
`uebungsaufgaben`, `testsimulationen`, `vorbereitungskurse`, `uniguide`,
`erfahrungsberichte`, `qa`.

### Eine Kachel entfernen oder umsortieren

Einfach den Eintrag in allen drei Dateien löschen bzw. verschieben. Das Raster
richtet sich automatisch nach der Anzahl.

### Eine ganz neue Kachel

Dafür braucht es zusätzlich eine kleine Ergänzung im Template
(`layouts/partials/angebot-grid.html`, Block `$quellen`): dort steht pro `key`,
welche Zieladresse verlinkt und was gezählt wird. Das ist ein Entwickler-Schritt
– die Datei erklärt oben im Kommentar, was einzutragen ist.

---

## 13. Uniguide: Angaben ergänzen und der Vergleich

### Wo die Angaben stehen

Alles zu den Universitäten steht in **einer** Datei: `data/unis.yaml`. Sie speist
beides – die Tabelle auf `/ems/uniguide/` und die Detailseite jeder einzelnen
Universität. Die Seiten unter `content/*/ems/uniguide/*.md` enthalten nur den
Titel und den technischen Namen (`uni_slug`), keine Angaben.

### Die noch leeren Felder füllen

Seit dem 8. September 2026 gibt es pro Universität diese zusätzlichen Felder.
Sie stehen absichtlich alle auf `null`, weil sie noch nicht an offizieller
Stelle nachgeprüft sind:

| Feld | Was hinein gehört | Beispiel |
| --- | --- | --- |
| `website_medizin` | Direktlink zur medizinischen Fakultät (nicht zur Uni-Startseite) | `"https://medizin.unibas.ch"` |
| `anmeldefrist` | Frist als Text | `"15. Februar"` |
| `studienbeginn` | Wann das Studium startet | `"Mitte September"` |
| `semestergebuehr` | Betrag inkl. Währung, als Text | `"CHF 850 pro Semester"` |
| `studienplaetze` | Zahl der Plätze (gab es vorher schon) | `180` |

**Bitte nur eintragen, was auf einer offiziellen Seite steht** – und im selben
Zug `stand` auf das heutige Datum und `quelle` auf die verwendete Seite setzen.
Solange ein Feld `null` ist, erscheint es auf der Website gar nicht; stattdessen
steht auf der Uni-Seite ein Kasten „Diese Angaben fehlen noch". Das ist Absicht:
Eine Lücke ist besser als eine Zahl, auf die sich jemand bei der Studienwahl
verlässt und die nicht stimmt.

### Erfahrungsberichte automatisch bei der Uni anzeigen

Das Feld `berichte_ort` verknüpft eine Universität mit den Erfahrungsberichten.
Sein Wert muss genau dem entsprechen, was in den Berichten im Frontmatter unter
`ort:` steht (z. B. `"Zürich"`). Passt es, erscheinen auf der Uni-Seite
automatisch die drei neuesten Berichte von diesem Ort. Gibt es keine, bleibt der
Abschnitt einfach weg – nichts weiter zu tun.

### Der Vergleich

In der Tabelle lassen sich in der ersten Spalte bis zu **vier** Universitäten
ankreuzen. Unten erscheint dann eine Leiste; „Vergleichen" stellt sie
untereinander in einer Tabelle nebeneinander – eine Spalte pro Universität, eine
Zeile pro Angabe.

Zu pflegen gibt es daran nichts: Der Vergleich zieht dieselben Felder aus
`data/unis.yaml`. Ein neu gefülltes Feld erscheint automatisch auch dort. Wer
eine **weitere Zeile** in den Vergleich aufnehmen will, ergänzt sie in
`layouts/partials/uniguide-table.html` (Abschnitt „VERGLEICHSANSICHT") – das ist
ein Entwickler-Schritt.

Die Obergrenze von vier ist bewusst gesetzt: Mehr Spalten passen auf einem Handy
nicht mehr sinnvoll nebeneinander. Sie steht in derselben Datei ganz unten im
Skript als `var MAX = 4;`.

---

## 14. Prüfungsmodus (Uhr und Ansagen)

Unter `/ems/pruefungsmodus/` können Leute unter echten Bedingungen üben: Die
Seite liest die Anweisung vor, nimmt die Zeit auf einer Vollbild-Uhr und sagt
am Ende „Stopp". Entweder für einen einzelnen Untertest oder für den ganzen
Testtag am Stück, ohne Pausen dazwischen – wie am echten EMS.

Es ist **kein Aufgaben-Generator**: Die Aufgaben kommen weiterhin aus den PDFs,
die man sich vorher bereitlegt.

### Eine Bearbeitungszeit ändern

Alle Zeiten stehen in **einer** Datei: `data/testablauf.yaml`. Dort den Wert bei
`minuten:` anpassen – fertig. Damit ändert sich automatisch **beides**:

- die Tabelle „Tagesablauf" auf `/ems/` (in allen drei Sprachen)
- der Prüfungsmodus

Vorher stand diese Tabelle von Hand in den drei Sprachdateien; eine geänderte
Zeit musste also an drei Stellen nachgeführt werden, und der Prüfungsmodus
hätte eine vierte gebraucht.

**Bitte sehr sorgfältig:** Eine falsche Zahl hier ist kein Schönheitsfehler.
Jemand übt dann monatelang mit der falschen Dauer.

### Die Reihenfolge ändern

Zwischen zwei Blöcken gibt es **keine Wartezeit**: Wie am echten EMS heisst es
„Stopp, blättern Sie jetzt zum nächsten Untertest" – und praktisch unmittelbar
danach kommt die nächste Ansage und „Start".

Die Reihenfolge der Einträge in `data/testablauf.yaml` **ist** die Reihenfolge
am Testtag. Die komplette Simulation spielt die Blöcke genau so nacheinander ab,
und die Tabelle zeigt sie in derselben Folge. Einträge verschieben genügt.

### Einen Zusatzhinweis zu einem Untertest

Optional lässt sich pro Block ein Satz hinterlegen, der nach der allgemeinen
Anweisung erscheint und mit vorgelesen wird – dafür gibt es die Felder
`hinweis_de`, `hinweis_fr` und `hinweis_it`. Aktuell genutzt bei den beiden
Einprägephasen und beim Konzentrationstest („Die Streichbedingung steht auf
deinem Blatt …"). Feld weglassen, wenn es nichts Besonderes zu sagen gibt.

### Eigener Ablauf

Unter den beiden fertigen Modi können Leute sich selbst zusammenstellen, was
sie üben wollen: welche Untertests, wie viele Aufgaben, wie viele Minuten – und
ob dazwischen Pausen liegen, wahlweise überall gleich lang oder einzeln
festgelegt.

Daran ist **nichts zu pflegen**: Die Auswahlliste kommt aus derselben
`data/testablauf.yaml`, vorbelegt sind immer die echten EMS-Werte. Wer etwas
ändert, sieht sofort die neue Gesamtdauer.

Die Zusammenstellung merkt sich der Browser und lässt sich über „Als Link
kopieren" weitergeben – praktisch für Lerngruppen („so üben wir am Samstag").
Der Link enthält die ganze Abfolge, es wird nichts auf einem Server gespeichert.

**Ein Detail, das wichtig ist:** Sobald jemand die Aufgabenzahl oder die Zeit
eines Untertests ändert, wird dieser Satz **vorgelesen** statt die Aufnahme
abgespielt. Die Aufnahmen nennen die echten EMS-Werte – bei „12 Aufgaben in 30
Minuten" würden sie sonst die falsche Zahl ansagen.

### Die vorgelesenen Sätze ändern

Alles Gesprochene ausser den Zusatzhinweisen steht in `i18n/de|fr|it.yaml` bei
den Einträgen, die mit `pm_` beginnen – zum Beispiel `pm_beginne` („Beginne
jetzt.") oder `pm_stopp` („Stopp. Leg den Stift weg."). Beim Ändern darauf
achten, dass die Sätze **gesprochen** natürlich klingen: kurz, keine Klammern,
keine Abkürzungen.

**Achtung, wenn du einen `pm_`-Text änderst:** Für Deutsch und Französisch
liegen fertige Aufnahmen unter `assets/audio/pruefungsmodus/`. Die sagen dann
noch den alten Satz. Entweder die betroffene Datei löschen – dann wird der neue
Text vorgelesen – oder sie neu einsprechen bzw. neu erzeugen lassen (siehe
`scripts/ansagen-erzeugen.py`).

### Die Ansagen als Aufnahme statt Roboterstimme

Für Deutsch und Französisch liegen je 15 fertige MP3-Dateien im Repo; sie werden
automatisch statt der Sprachausgabe abgespielt. Auf Italienisch liest weiterhin
das Gerät vor – dort war die Lizenz der verfügbaren Stimme nicht eindeutig zu
klären.

Diese Dateien sind maschinell erzeugt. **Echte Aufnahmen aus dem Verein wären
besser**, und der Austausch ist denkbar einfach: die vorhandene Datei mit der
eigenen überschreiben, gleicher Name, fertig. Es sind 15 kurze Sätze pro
Sprache. Welche Datei welchen Satz enthält, steht in
`assets/audio/pruefungsmodus/README.md`.

Die Anredeform in den Ansagen ist bewusst das **Sie** ("Sie haben 16 Minuten
Zeit"), obwohl die Website sonst durchgehend duzt: Die Ansage gibt eine
Aufsichtsperson im Testsaal wieder.
