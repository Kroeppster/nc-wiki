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

### Wie lange gilt das Passwort?

**Zwei Stunden ab dem letzten Aufruf einer Mitglieder-Seite.** Man gibt es einmal
ein und kann danach frei zwischen Übersicht, Events und Spesenformular wechseln –
auch über die Sprachen hinweg. Jeder weitere Aufruf schiebt die zwei Stunden neu
nach vorn; wer den Rechner liegen lässt, ist danach wieder draussen.

Vorher war das anders: Jede der neun geschützten Seiten fragte einzeln, der Klick
von der Übersicht zu „Events" also gleich wieder. Das war nicht beabsichtigt.

Was dabei im Browser gespeichert wird, ist **nicht das Passwort**, sondern ein
daraus gerechneter, gesalzener Prüfwert. Wer ihn aus einem fremden Browser
ausliest, kann damit die Seiten entsperren, aber das Passwort nicht zurückrechnen.

Die Dauer steht in `scripts/passwort-vorlage.html` ganz oben als
`MERKDAUER_MINUTEN`. Kürzer ist sicherer, länger bequemer – zwei Stunden sind der
Kompromiss für einen Uni-Rechner, an dem nach dir jemand anderes sitzt.

**Sofort abmelden** geht, indem man `?staticrypt_logout` an die Adresse hängt,
zum Beispiel `…/mitglieder/?staticrypt_logout`. Den Browser ganz zu schliessen
reicht nicht – dafür ist die Zeit da.

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

Das Salz in `scripts/encrypt-protected-pages.mjs` (`SALZ`) bleibt dabei
unverändert – es ist kein Geheimnis und muss nur für alle neun Seiten dasselbe
sein, damit eine Eingabe für den ganzen Bereich gilt.

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

## 11b. Die Website auf Fehler prüfen

Sechs Skripte im Ordner `scripts/` prüfen die fertig gebaute Website. Sie
ersetzen kein Auge, finden aber zuverlässig die Fehlerarten, die sonst erst
jemandem auf dem Handy auffallen.

```bash
npm run build                 # public/ erzeugen
npx http-server public -p 8099 -s &

BREITEN=1280,768,390 MODI=light,dark node scripts/seiten-pruefen.mjs
python3 scripts/struktur-pruefen.py
```

Beide suchen sich die zu prüfenden Seiten selbst aus `public/` zusammen – es
ist nichts vorzubereiten. Läuft der Server auf einem anderen Port, sagt man das
mit `ADRESSE=http://127.0.0.1:8123` davor.

**`seiten-pruefen.mjs`** ruft jede Seite in einem echten Browser auf und misst:
seitliches Scrollen, sich überlappende oder aneinanderstossende Kästen,
abgeschnittenen Text, Elemente ausserhalb des Bildes, fehlende Bilder und
Textkontrast. Oben in der Datei steht zu jeder Prüfung, welchen echten Fehler
sie einmal gefunden hat.

**`struktur-pruefen.py`** beantwortet drei Fragen, die man der Website nicht
ansieht: doppelte Inhalte unter verschiedenen Adressen, von der Startseite aus
unerreichbare Seiten, und Links ins Leere.

**`verhalten-pruefen.mjs`** ist das Gegenstück zum ersten: Er lädt keine Seiten,
sondern **bedient** sie. Dunkelmodus-Umschalter, Sprachwahl, Suche, Filter der
Erfahrungsberichte, Uni-Vergleich, der ganze Prüfungsmodus (Uhr, Pause,
Abbrechen, automatisch gerechnete Zeit, Expertenmodus) und die Formulare.

```bash
npx pagefind --site public          # der Suchtest braucht den Suchindex!
node scripts/verhalten-pruefen.mjs
```

Formspree wird dabei abgefangen – es geht **nie** eine echte Nachricht raus.

**Die beiden Generatoren haben je ein eigenes Skript,** weil sie bei jedem
Aufruf etwas anderes auswürfeln und man einem einzelnen Durchlauf nicht ansieht,
ob er der Normalfall war:

```bash
node scripts/fakten-generator-pruefen.mjs /tmp/probe   # prüft auch das erzeugte PDF
node scripts/figuren-generator-pruefen.mjs             # würfelt 12 Sets und misst nach
python3 scripts/figuren-vergleichen.py 14              # gegen die echten Serien
```

**Erwartetes Ergebnis:** Beim Struktur-Skript genau zehn unerreichbare Seiten –
der Mitgliederbereich (neun) und die Alpha-Seite, alle absichtlich nirgends
verlinkt. Alles andere ist ein Fund.

**Wer eine Prüfung ergänzt, testet sie zuerst gegen einen echten, bekannten
Fehler.** Eine Prüfung, die den Fehler nicht findet, für den sie gedacht ist,
ist schlimmer als keine – sie macht ruhig. Genauso wichtig: Fehlalarme
abschalten. Ein Prüfstand, der bei jedem Lauf hundert harmlose Stellen meldet,
wird nach zwei Wochen nicht mehr gelesen.

---

## 11b-2. Der Fakten-Generator

Auf der Seite „Figuren & Fakten lernen" steht ein Generator, der immer neue
Einpräge-Sets würfelt. **Warum es ihn gibt:** Material für diesen Untertest ist
einmalig verwendbar – wer eine Serie einmal auswendig gelernt hat, kann sie nie
wieder zum Üben brauchen. Bei allen anderen Untertests kann man eine Serie nach
Monaten nochmal rechnen, hier nicht. Deshalb ein Generator statt weiterer PDFs.

**Wortlisten:** `data/fakten-generator/<sprache>.yaml`. Aktuell gibt es nur
`de.yaml`; auf Französisch und Italienisch erscheint ein Hinweis statt eines
Sets. Sobald `fr.yaml` bzw. `it.yaml` existiert, taucht der Generator dort von
selbst auf – am Template ist nichts zu ändern.

**Neue Wörter ergänzen:** einfach unten in der passenden Kategorie eintragen.
Oben in der Datei steht ausführlich, warum die Kategorien nicht beliebig sind –
kurz: Eine echte EMS-Serie würfelt nicht, sondern gibt jeder Altersgruppe drei
Berufe aus **einem** Feld und drei Krankheiten aus **drei verschiedenen** Arten.
Genau das macht die Menge lernbar. Wer die Kategorien auflöst, erzeugt Sets, die
deutlich schwerer sind als die Prüfung.

**Wo er auf der Seite steht,** bestimmt ihr: Der Shortcode `{{</* fakten-generator */>}}`
lässt sich im Text der Seite beliebig verschieben.

**Was die Wörter ursprünglich gefüllt hat:** `scripts/fakten-listen-auslesen.py`
liest sie aus den eigenen Übungs-PDFs aus. Das Skript **überschreibt die
YAML-Datei nicht**, es gibt die gefundenen Wörter nur aus – die Kategorien und
Geschlechtsangaben darin kann kein Skript erraten und wären sonst weg.

**Auf Papier üben:** Neben „Set erzeugen und starten" (Durchlauf am
Bildschirm mit Uhr) gibt es „Set als PDF / drucken". Der Druck enthält drei
Blätter wie die echten Serien – Einprägeblatt, Aufgabenblatt, Lösungen. Es
wird keine PDF-Bibliothek geladen: Der Browser druckt die Seite selbst und
bietet im Druckdialog „Als PDF sichern" an. Beide Wege stehen nebeneinander,
man muss den getakteten Durchlauf nicht starten, um drucken zu können.

**Wer an den Druckregeln etwas ändert,** liest zuerst den Kommentar bei
`@media print` in `assets/css/style.css`. Dort stehen zwei Lösungen, die
nicht funktioniert haben und warum – das spart den nächsten zwei Anläufen die
Zeit. Kurz: Der Druckbehälter wird beim Drucken nach `<body>` verschoben, weil
er sonst entweder den ganzen Artikel mitbringt oder dessen Platz als leere
Seiten stehen bleibt. Die Druckregeln hängen bewusst an `body.fg-druckt` und
verändern das Drucken anderer Seiten nicht.

**Noch offen:** Die Kategorien sind vorsortiert und von keinem Menschen
freigegeben. Für echte Abwechslung wären rund 80 Einträge je Kategorie gut,
aktuell sind es etwa 40.

**Die Vorgabezeiten kommen aus `data/testablauf.yaml`,** sie stehen nicht im
Template. Wer dort eine Untertest-Zeit ändert, ändert sie hier automatisch mit.
Die vorgeschlagene Pause ist die **echte Lücke** zwischen Einprägen und
Reproduktion – am Testtag liegen Textverständnis und die Figuren-Reproduktion
dazwischen, zusammen 50 Minuten. Genau diese Lücke macht den Untertest schwer,
deshalb steht sie so in der Vorgabe und nicht als bequeme Drei-Minuten-Pause.

---

## 11b-3. Die Alpha-Seite und der Figuren-Generator

**Was die Alpha-Seite ist:** `content/de/alpha/` – eine Werkbank für neue
Funktionen, bevor sie auf eine echte Seite kommen. Sie liegt hinter demselben
Passwort wie der Mitgliederbereich (`geschuetzt: true` im Frontmatter, siehe
Abschnitt 11), ist in keinem Menü verlinkt, steht nicht in der Sitemap, wird
von der Suche nicht gefunden und trägt `noindex`.

Sie gibt es **absichtlich nur auf Deutsch**. Sonst gilt hier die Regel, dass
jeder sichtbare Text dreisprachig sein muss – diese Seite sieht aber niemand
ausser euch, und drei Fassungen einer Werkbank zu pflegen wäre nur Arbeit ohne
Nutzen. Sobald eine Funktion von der Alpha-Seite auf eine echte Seite wandert,
gilt die Regel wieder voll.

**Eine neue Funktion zum Testen dazulegen:** In `content/de/alpha/_index.md`
einen Abschnitt schreiben, der sagt, *was zu beurteilen ist* (nicht nur, was es
tut), und den Shortcode darunter setzen. Ist die Funktion freigegeben, wandert
derselbe Shortcode auf die richtige Seite und der Abschnitt hier wird gelöscht.

**Der Figuren-Generator** (`{{</* figuren-generator */>}}`) würfelt 18 Figuren wie im
Untertest „Figuren lernen": jede in fünf verschieden grosse Felder geteilt,
genau eines schwarz. Nach der Pause kommen dieselben Figuren in anderer
Reihenfolge und mit Feldern A–E beschriftet zurück. Gleiche Begründung wie beim
Fakten-Generator: Material für diesen Untertest ist einmalig verwendbar. Er
kann dasselbe wie der Fakten-Generator, Durchlauf am Bildschirm und Druck mit
drei Blättern, und holt seine Vorgabezeiten ebenfalls aus `data/testablauf.yaml`
(die Pause dort ist die Lücke aus Fakten-Einprägen und Textverständnis).

Er braucht **keine Datendatei** – die Figuren entstehen im Browser. Deshalb
funktioniert er in allen drei Sprachen, sobald er auf eine echte Seite kommt;
nur die Beschriftungen stehen in `i18n/de|fr|it.yaml` (Präfix `fig_`).

**Jede Serie würfelt zuerst ihren eigenen Stil.** Das ist der wichtigste Punkt
am ganzen Generator, und er war anfangs falsch gelöst. Würfelt jede Figur ihre
Form aus denselben festen Bereichen, sehen alle Serien gleich aus – über acht
erzeugte Serien lag der Füllgrad zwischen 0.68 und 0.70, bei elf echten Serien
zwischen 0.63 und 0.79.

Heute zieht zuerst die **Serie** einen Stil (Eckenzahl, Zackigkeit, Figurgrösse
und ihre Streuung, Schwung der Trennlinien, Strichstärke, Bauart), und die 18
Figuren folgen ihm mit kleinen Abweichungen. Das ist auch inhaltlich richtig
herum: Dass sich die Figuren **innerhalb** einer Serie ähneln, macht den
Untertest ja aus – man muss sie auseinanderhalten können. Verschiedene Serien
dürfen und sollen deutlich anders aussehen, genau wie unsere echten Serien
2022, 2025 und 2026 untereinander.

Es gibt drei **Bauarten**, jede mit eigenem Charakter – auch das ist aus dem
eigenen Material abgeschaut: **frei** (Felder frei verteilt, wie 2025),
**Nabe** (ein Feld in der Mitte, vier drumherum, wie 2026) und **Band** (fünf
Bänder quer durch die Figur; das erklärt die ruhigeren Serien wie 2022 S01).

**Wie nah die Figuren an den echten sind, wird gemessen, nicht geschätzt.**

```bash
python3 scripts/figuren-vergleichen.py 14
```

Das Skript würfelt 14 Serien, misst sie und die echten mit demselben Massstab
und stellt beides nebeneinander. Es braucht `pip install pymupdf numpy scipy
pillow`. Der Bericht hat **zwei Teile, und der zweite ist der wichtigere**:

- **Teil 1** vergleicht einzelne Figuren: Sieht eine Figur aus wie eine echte?
- **Teil 2** vergleicht ganze Serien: Sehen zwei Durchläufe verschieden aus?
  Teil 1 kann tadellos sein, während Teil 2 zeigt, dass alle Serien einander
  gleichen. Genau dieser Fall lag vor, bevor der Stil je Serie gewürfelt wurde.

Am meisten sagt die Zeile **Nachbarschaften** aus: Wie viele der zehn möglichen
Feldpaare grenzen aneinander? Fünf Streifen untereinander ergeben vier – eine
Kette. Die echten Figuren liegen bei 7.9 – ein Netz. Genau dieser Unterschied
ist das, was man auf den ersten Blick sieht, und der erste Entwurf lag mit 6.6
sichtbar daneben.

**Eine Falle beim Stil-Würfeln,** die man sonst zweimal baut: Die Grenzwerte
einer Serie müssen zueinander passen. Verlangt ein Stil sehr unterschiedlich
grosse Felder **und** enge Grenzen, scheitert fast jede Figur, die Serie wird
verworfen und neu gewürfelt – am Ende überleben nur die grosszügigen Stile, und
die Unterschiede zwischen den Serien sind wieder weg. Im Skript sind die beiden
Werte deshalb aneinander gekoppelt.

**Wer am Zeichnen etwas ändert,** liest zuerst den Kommentarkopf in
`layouts/shortcodes/figuren-generator.html` und die vier Abschnitte im Skript.
Dort steht, was in den bisherigen Anläufen schiefging – und jeder dieser Fehler
kostet Zeit, wenn man ihn nochmal macht:

- **Doppelte Clip-Kennungen.** Dieselbe Figur erscheint zweimal auf der Seite.
  Bei gleicher Kennung beschneidet die Form der einen auch die andere, und
  Trennlinien ragen aus der Form. (Derselbe Fehler passierte später nochmal im
  Prüfwerkzeug, als es Figuren aus mehreren Seitenaufrufen zusammenklebte.)
- **Trennlinien quer über die Figur.** Sah gestreift aus statt aufgeteilt – und
  schlimmer: In einer eingebuchteten Form konnte ein Feld in zwei Flecken
  zerfallen oder ganz verschwinden. Dann zeigte die Figur vier oder sechs
  Flecken, obwohl fünf Antworten zur Wahl stehen. Das war bei zwei von drei
  Figuren so. Heute: ein gewichtetes Voronoi-Muster in einem verbogenen Raum,
  und jedes Feld wird zwangsweise auf einen zusammenhängenden Klumpen reduziert.
- **Jede Feldkontur einzeln geglättet.** Aus der Ferne richtig, aus der Nähe
  nicht: Zwei Nachbarfelder glätten dieselbe Grenze unterschiedlich, es bleiben
  weisse Keile an den Knotenpunkten stehen und die Trennlinie wird doppelt
  gezeichnet. Heute werden die Grenzen einmal als Netz von Bögen berechnet, aus
  denen sich alle fünf Felder zusammensetzen.
- **Buchstabe im Schwerpunkt seines Feldes.** Bei einem dünnen, gebogenen Feld
  liegt der Schwerpunkt fast auf der Kante, und zwei Buchstaben rutschen
  übereinander (gemessen: 47 von 216 Figuren). Heute steht der Buchstabe an der
  Stelle, die am tiefsten im Feld steckt.

**Noch zu beurteilen:** ob die Figuren schwer genug sind. Die Zahlen stimmen –
ob sich 18 davon in vier Minuten merken lassen, sagt keine Messung. Zum
Vergleich liegen die echten Serien unter Übungsaufgaben.

---

## 11c. Welches Formular geht an wen

| Formular | Wo | Adresse | Geht an |
| --- | --- | --- | --- |
| Kontakt | `/kontakt/` | `mvkpgrpl` | allgemeines Postfach |
| Fehlermeldung Übungsaufgaben | Übungsaufgaben-Seiten | **ebenfalls `mvkpgrpl`** | allgemeines Postfach |
| Erfahrungsbericht einreichen | `/ems/erfahrungsberichte/` | `xaewqwoj` | eigenes Postfach |

**Die Fehlermeldungen teilen sich absichtlich das Kontakt-Postfach** – das ist
eine Zwischenlösung, kein Versehen. Vorher stand dort ein Platzhalter, jede
Meldung ging ins Leere, während die meldende Person eine Bestätigung sah. Damit
sie trotzdem auffallen, setzt das Formular einen festen Betreff
(„Fehlermeldung Uebungsaufgaben (Website)"), nach dem sich filtern lässt.

Sobald eine eigene Formspree-Adresse für Fehlermeldungen besteht, genügt es,
sie in `layouts/partials/report-error-general.html` einzutragen – sonst ändert
sich nichts. Details in der Langfassung, Abschnitt 11.

---

## 12. Startseite: Hero-Bild, Logo, Zeitstrahl und Material

### Die Reihenfolge der Abschnitte

Von oben nach unten: Hero → **News** → „Was du wann brauchst" (Zeitstrahl) →
„Das Material selbst" → die acht Untertests → Mission → Unterstützer-Band →
Spendenaufruf. Gepflegt wird sie direkt in `layouts/index.html`, indem man die
`<section>`-Blöcke verschiebt.

Die News stehen bewusst **weit oben, gleich nach dem Hero**: Sie sind das
Einzige, was sich regelmässig ändert, und gehören deshalb dorthin, wo jemand
sie beim Wiederkommen sofort sieht. Alles darunter ändert sich fast nie.

**Beim Verschieben die Klasse `section-surface` mitziehen.** Die Startseite
wechselt von Abschnitt zu Abschnitt zwischen heller Kartenfläche und
Seitenhintergrund; ohne diesen Wechsel stehen zwei gleich getönte Blöcke
direkt aufeinander und die Grenze verschwindet. Aktuell tragen „Was du wann
brauchst" und die Untertests die Klasse, News, Material und Mission nicht.

### Das Bild im Hero austauschen

Oben rechts auf der Startseite steht ein Foto. Welches, steht im Frontmatter
der Startseite unter `hero:`:

```yaml
hero:
  bild: "testsimulationen/testsimulation-2023.jpg"
  bild_alt: "Voller Hörsaal während einer NCWiki-Testsimulation, im Vordergrund ..."
```

Der Pfad ist **relativ zu `assets/images/`**. Ein neues Bild dort ablegen, den
Pfad eintragen – Hugo erzeugt die verkleinerten Fassungen automatisch. Der
`bild_alt`-Text ist **Pflicht** (Screenreader); fehlt er bei vorhandenem Bild,
bricht der Build ab. Beides in allen drei Sprachdateien eintragen, der
`bild_alt`-Text natürlich übersetzt.

Lässt man `bild` weg, erscheint einfach kein Foto – die Seite bleibt heil.

**Worauf es bei der Bildwahl ankommt:** Das aktuelle Foto zeigt einen vollen
Hörsaal und im Vordergrund den dreisprachigen Antwortbogen mit dem NCWiki-Logo.
Es beantwortet ohne ein Wort, was hier passiert und dass es echt ist. Ein
beliebiges Symbolbild würde genau diese Wirkung verlieren.

### Das Logo

Im Hero steht das Logo gross. Es ist dieselbe Datei wie überall
(`static/images/logo.svg`); im Dunkelmodus wird es automatisch weiss
dargestellt, weil sein „WIKI"-Schriftzug schwarz ist und sonst verschwinden
würde. Das steuert die Variable `--logo-filter` in `assets/css/style.css` und
gilt ebenso für das kleine Logo in der Kopfzeile.

### Zwei Abschnitte statt Kacheln

Die Startseite zeigt das Angebot seit September 2026 auf zwei Arten
untereinander, und beide ersetzen die früheren Kacheln:

1. **„Was du wann brauchst"** ist ein Zeitstrahl: vier Etappen auf einer
   Linie, von der Anmeldung im Februar bis zum Resultat im August. Auf
   schmalen Bildschirmen wird die Linie senkrecht. Gepflegt im Frontmatter
   der Startseite unter `weg:`.
2. **„Das Material selbst"** zeigt echte Seiten aus den PDFs und echte Fotos
   statt Symbolbildern. Gepflegt unter `material:`; die Ausschnitte aus den
   PDFs erzeugt `scripts/angebot-bilder-erzeugen.py`.

### Der Zeitstrahl (`weg:`)

Jede Etappe hat vier Angaben – und **keine Zahl**: im Zeitstrahl stehen nur
die Namen der Angebote, damit die vier Etappen ruhig nebeneinander liegen.
Die Zahlen stehen weiter unten, bei „Das Material selbst".

```yaml
weg:
  eyebrow: "Von der Anmeldung bis zum Resultat"
  heading: "Was du wann brauchst"
  etappen:
    - wann: "Bis 15. Februar"          # kleine Zeile über dem Titel
      titel: "Entscheiden und anmelden"
      text: "Welche Universität, welche Priorität ..."
      mittel:                           # die Links unter dem Text
        - titel: "Uniguide"
          url: "ems/uniguide/"
        - titel: "Fragen & Antworten"
          url: "ems/qa/"
```

Die vier Etappen liegen in einem **unsichtbaren Raster** (CSS `subgrid`):
Zeitangabe, Titel, Text und Links beginnen in allen vier Spalten auf
derselben Höhe, auch wenn ein Titel zweizeilig wird. Dafür müssen die vier
Teile im Template direkte Kinder von `.weg-etappe` bleiben – wer sie in ein
zusätzliches `<div>` einpackt, zerstört die Ausrichtung.

### Das Material (`material:`)

```yaml
material:
  eyebrow: "Was du hier findest"
  heading: "Alles kostenlos, alles von Studierenden gemacht"
  items:
    - key: uebungsaufgaben        # legt fest, was gezählt und wohin verlinkt wird
      titel: "Übungsserien"
      zahlen: ["uebungen"]        # füllt {1} im Text
      text: "{1} Serien zu allen acht Untertests, mit Lösungen."
```

`key` ist der einzige Wert, der **nicht** übersetzt wird – er ist der interne
Name und muss in allen drei Sprachen gleich bleiben. Erlaubt sind:
`uebungsaufgaben`, `testsimulationen`, `vorbereitungskurse`, `community`.

### Die Bilder der vier Kacheln

Welche Bilder eine Kachel zeigt, steht im Template
(`layouts/partials/material-grid.html`, Block `$quellen`) – nicht im
Frontmatter, weil es ein Gestaltungs- und kein Redaktionsentscheid ist:

| Kachel | Bild |
| --- | --- |
| Übungsserien | neun **ganze Seiten**, drei pro Reihe: zuerst das Antwortblatt, dann die acht Untertests in der Reihenfolge des Testtags |
| Testhefte | Titelseite einer Testsimulation, ebenfalls ganz |
| Vorbereitungskurs | das vorhandene Kursfoto (`vorbereitungskurse/vorbereitungskurs-2024.jpg`) |
| Orientierung und Austausch | Uniguide-Tabelle, ein Erfahrungsbericht und die Discord-Karte übereinander |

Seiten aus PDFs werden **vollständig** gezeigt, nie angeschnitten: Kopfzeile,
Aufgabenzahl, Bearbeitungszeit, Logo und Lizenzhinweis gehören dazu, sonst sieht
ein Blatt aus wie ein willkürlicher Fetzen. Dafür ist im Template `papier: true`
gesetzt; das Stylesheet legt solche Bilder dann mit `object-fit: contain` auf
weissen Grund. Fotos und Bildschirmfotos stehen auf `papier: false` und dürfen
formatfüllend angeschnitten werden – sie haben keinen Rand, der etwas bedeutet.

Das ist auch nötig, weil die Quell-PDFs **nicht dasselbe Papierformat** haben:
sechs sind US Letter, drei sind A4. Auf ein gemeinsames Verhältnis geschnitten
würde bei der einen Hälfte der Rand fehlen.

Ein Name **mit** Punkt und Endung wird unter `assets/images/` gesucht, ein
Name **ohne** unter `assets/images/angebot/`. So kann eine Kachel entweder ein
eigens erzeugtes Bild oder ein schon vorhandenes Foto benutzen.

Die neun Ausschnitte und die übrigen erzeugten Bilder legt
`scripts/angebot-bilder-erzeugen.py` an (braucht `pip install pymupdf`):

```bash
python3 scripts/angebot-bilder-erzeugen.py
```

Oben in der Datei steht pro Ausschnitt, aus welchem PDF, welcher Seite und
welchem Bereich er kommt, sowie das Seitenverhältnis 1 : 1.30 (Hochformat).
Wer ein neues Übungs-PDF sauberer findet, ändert dort den Pfad und lässt das
Skript neu laufen – die Bilder werden dabei überschrieben.

### Die Zahlen musst du nicht pflegen

Sie werden bei **jedem Bauen der Website neu gezählt** – an einer einzigen
Stelle, `layouts/partials/angebot-zahlen.html`. Lädst du zehn neue
Übungsserien hoch, steht dort beim nächsten Build automatisch die neue Zahl.

**Deshalb bitte keine Zahlen in die Texte schreiben** – sie wären beim
nächsten Upload sofort falsch. Wo eine Zahl im Satz stehen soll, kommt ein
Platzhalter `{1}`, `{2}` … und der passende Eintrag in `zahlen:`.

**Was genau gezählt wird:** Übungsserien ohne die Lösungs-PDFs (eine Serie mit
Lösung ist eine Übung, nicht zwei), bei den Testsimulationen die Jahrgänge
(zu einem Jahrgang gehören mehrere Dateien), und die Erfahrungsberichte nur
in der jeweiligen Sprache.

### Texte ändern

Beide Abschnitte stehen im Frontmatter der Startseite – und zwar **in allen
drei Sprachdateien**:

- `content/de/_index.md`
- `content/fr/_index.md`
- `content/it/_index.md`

### Eine Etappe oder Kachel entfernen oder umsortieren

Einfach den Eintrag in allen drei Dateien löschen bzw. verschieben. Beide
Raster richten sich automatisch nach der Anzahl.

### Eine ganz neue Kachel

Dafür braucht es zusätzlich eine kleine Ergänzung im Template
(`layouts/partials/material-grid.html`, Block `$quellen`): dort steht pro
`key`, welche Zieladresse verlinkt und welche Bilder gezeigt werden. Das ist
ein Entwickler-Schritt – die Datei erklärt oben im Kommentar, was einzutragen
ist.

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

### Eigener Ablauf

Unter den beiden fertigen Modi können Leute sich selbst zusammenstellen, was
sie üben wollen. Das gibt es in **zwei Stufen**:

**Normal (so ist es voreingestellt):** Man wählt nur aus, *welche* Untertests
und *wie viele* Aufgaben. **Die Zeit rechnet sich daraus automatisch aus** –
im selben Tempo wie am echten EMS. Beispiel „Muster zuordnen": 18 Aufgaben in
16 Minuten, also ergeben 7 Aufgaben **6:13**. Unter der Zeit steht zusätzlich,
wie viele Sekunden das pro Aufgabe sind. Das ist fast immer das, was jemand
will: eine halbe Serie üben, aber unter dem richtigen Zeitdruck.

Die Zeit steht dabei in **Minuten und Sekunden**, nicht in ganzen Minuten. Auf
volle Minuten gerundet wäre der Schnitt pro Aufgabe ein anderer als am echten
Test – und genau der ist ja der Sinn der Sache.

**Eine Ausnahme: Figuren und Fakten einprägen.** Dort gibt das Übungsblatt vor,
wie viele Figuren darauf stehen – einstellen lässt sich deshalb die **Zeit**
statt der Anzahl. Das ist genau das, was die Übungsseite empfiehlt: am Anfang
bewusst mehr Zeit nehmen (10 statt 6 Minuten) und sie nach und nach verkürzen.
Gesteuert wird das über das Feld `aufgaben_fest: true` in
`data/testablauf.yaml` – wer es bei einem weiteren Block braucht, setzt es
dort, sonst ist nichts zu tun.

**Expertenmodus (Schalter über der Tabelle):** Erst hier lassen sich die
Minuten pro Block und die Pausen einzeln von Hand eintragen. Gedacht für Leute,
die bewusst etwas anderes trainieren wollen – etwa mit absichtlich zu wenig
Zeit, oder mit einer langen Pause zwischen Einprägen und Reproduktion.

Der Grund für die Zweiteilung: Eine Zeit von Hand einzutippen, die nicht zum
Tempo des Tests passt, macht das Üben wertlos. Wer das trotzdem will, soll es
können – aber bewusst, nicht aus Versehen.

Daran ist **nichts zu pflegen**: Die Auswahlliste und das Tempo kommen aus
derselben `data/testablauf.yaml`, vorbelegt sind immer die echten EMS-Werte.
Wer etwas ändert, sieht sofort die neue Gesamtdauer.

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

---

## 15. Die Abschnittsliste („Auf dieser Seite")

Auf langen Seiten steht eine Liste der Abschnitte. Ein Klick springt dorthin,
der Abschnitt, in dem man gerade liest, ist markiert.

Sie sieht je nach Platz anders aus:

- **Auf breiten Bildschirmen** (ab 1100 Pixel) steht sie als schmale Spalte
  **rechts neben dem Text** und läuft beim Scrollen mit. Sie kostet dort keine
  Zeile Höhe, und weil sie senkrecht ist, dürfen die Abschnittsnamen so lang
  sein, wie sie eben sind.
- **Auf Tablet und Handy** steht sie zugeklappt über dem Text: eine Zeile zum
  Auftippen. Auch da ist sie von Anfang an sichtbar, braucht aber nur eine
  Zeile.

**Daran ist nichts einzustellen und nichts zu pflegen.** Die Liste entsteht
automatisch aus den Zwischenüberschriften der Seite – also aus allem, was in
einer `.md`-Datei mit `##` beginnt. Wer eine Überschrift umbenennt,
verschiebt oder ergänzt, ändert damit automatisch auch die Liste.

Zwei Dinge, die manchmal Fragen aufwerfen:

- **Auf kurzen Seiten erscheint sie nicht.** Gibt es weniger als zwei
  Abschnitte, bleibt sie ganz weg – und dann bleibt auch die Spalte weg, der
  Text nutzt die volle Breite (das war beim Uniguide eine Zeitlang anders und
  hat die Tabelle grundlos abgeschnitten).
- **Sie nimmt dem Text keinen Platz weg**, solange der Bildschirm breit genug
  ist: Die Spalte steht im leeren Seitenrand rechts. Erst wenn der Rand
  schmaler ist als die Spalte, rückt der Text etwas zusammen.
- **Nur die oberste Ebene zählt.** `##` kommt in die Liste, `###` nicht. Sonst
  wird die Übersicht länger als der Text daneben.

Sie funktioniert auch auf Seiten ohne Fliesstext, zum Beispiel beim
Prüfungsmodus oder beim Uniguide: Dort sammelt die Seite ihre Abschnitte selbst
ein, nachdem sie geladen ist.

Die Beschriftung („Auf dieser Seite" / „Sur cette page" / „In questa pagina")
steht wie alle festen Texte in `i18n/de|fr|it.yaml`, beim Eintrag
`auf_dieser_seite`. Technisch steckt alles in einer einzigen Datei:
`layouts/partials/seiten-uebersicht.html`.
