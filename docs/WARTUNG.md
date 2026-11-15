# Website pflegen – Kurzanleitung

**Deutsch** · [Français](WARTUNG.fr.md) · [Italiano](WARTUNG.it.md)

Hier steht nur das, was im Alltag vorkommt: Texte ändern, News schreiben, PDFs und
Bilder hochladen, etwas löschen. Alles geht im Browser, installieren musst du nichts.
Alles andere (Startseite, Team, Menü, Design, Formulare, Mitgliederbereich, Technik)
steht in der **[ausführlichen Anleitung](WARTUNG-DETAILLIERT.md)**.

---

## Bevor du anfängst

**Was du brauchst**

- Ein kostenloses Konto auf [github.com](https://github.com) und eine Einladung zum
  Repository `Kroeppster/nc-wiki`. Die Einladung vergibt, wer die Website betreut; ohne
  sie kannst du alles lesen, aber nichts ändern.
- Für die Textmappe: Excel.
- Sonst nichts. Du musst kein Programm installieren und nicht programmieren können.

**Kaputt machen kannst du fast nichts.** GitHub merkt sich zu jeder Änderung den Stand
davor; er lässt sich zurückholen ([Abschnitt 12](#12-kontrollieren-und-rückgängig-machen)).
Findet die automatische Prüfung in deiner Änderung einen Fehler, bleibt die bisherige
Website einfach online.

**Wörter, die immer wieder vorkommen**

| Wort | Was es heisst |
| --- | --- |
| Repository | der Ordner mit allen Dateien der Website, auf GitHub |
| `main` | der gültige Stand. Was auf `main` liegt, wird veröffentlicht |
| Commit, «Commit changes» | Speichern. Jede gespeicherte Änderung bekommt eine kurze Beschreibung, damit andere sehen, was sich geändert hat |
| Pull Request | ein Änderungsvorschlag, der noch nicht gilt (so kommen die Textmappen herein) |
| Merge | den Vorschlag übernehmen. Erst danach liegt er auf `main` |
| Bau, «Actions» | Nach jedem Speichern baut GitHub die Website neu und prüft sie. Grüner Haken: live. Rotes Kreuz: [Abschnitt 10](#10-wenn-der-bau-rot-ist) |
| Markdown, `.md` | einfache Textdateien, aus denen die Seiten entstehen ([Abschnitt 14](#14-schreibhilfe-für-texte)) |
| Seitenkopf | die Zeilen zwischen den beiden `---` ganz oben in einer `.md`-Datei: Titel, Datum, Beschreibung |

**Die Adressen:** Website [kroeppster.github.io/nc-wiki](https://kroeppster.github.io/nc-wiki/) ·
Dateien [github.com/Kroeppster/nc-wiki](https://github.com/Kroeppster/nc-wiki) ·
Web-Editor [app.pagescms.org](https://app.pagescms.org)

---

## 1. Welcher Weg wofür?

| Du willst … | Weg | Abschnitt |
| --- | --- | --- |
| viele Texte durchsehen, übersetzen, Startseite oder Team ändern | **Excel-Textmappe** | [2](#2-texte-ändern-mit-der-excel-textmappe) |
| schnell einen Tippfehler auf einer Seite korrigieren | **Web-Editor** (Pages CMS) | [3](#3-kleine-korrekturen-im-web-editor) |
| einen News-Beitrag schreiben | Web-Editor oder GitHub | [4](#4-einen-news-beitrag-schreiben) |
| ein PDF oder Bild hochladen, eine Datei löschen | **GitHub** | [5](#5-ein-pdf-hochladen) – [8](#8-eine-datei-oder-seite-löschen) |
| eine bestehende Seite direkt auf GitHub ändern | **GitHub** | [11](#11-eine-datei-direkt-auf-github-ändern) |
| sehen, ob die Änderung live ist, oder etwas rückgängig machen | **GitHub** | [12](#12-kontrollieren-und-rückgängig-machen) |
| das Datum des nächsten EMS ändern, die Website aufs neue Jahr umstellen | mehrere | [13](#13-checkliste-für-das-neue-jahr) |
| wissen, wie man fett schreibt, eine Liste oder einen Link setzt | – | [14](#14-schreibhilfe-für-texte) |

Alle Wege ändern dieselben Dateien. Nach jeder Änderung auf `main` baut GitHub die
Website neu, nach ein bis zwei Minuten ist sie live.

---

## 2. Texte ändern mit der Excel-Textmappe

Es gibt **eine Mappe je Sprache** (DE, FR, IT) mit allen sichtbaren Texten der Website –
jede Seite auf einem eigenen Blatt, vorne eine Anleitung und ein Inhaltsverzeichnis.

1. **Frische Mappe holen:** auf GitHub rechts unter *Releases → Textmappen*, oder direkt:
   [DE](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-de.xlsx) ·
   [FR](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-fr.xlsx) ·
   [IT](https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-it.xlsx).
   Sie wird nach jeder Änderung automatisch neu erzeugt. **Immer mit einer frischen
   Mappe beginnen.**
2. **In den Zellen arbeiten:**

   | Was | Wie |
   | --- | --- |
   | Text ändern | in der Spalte „Text“ überschreiben (wird gelb) |
   | Neuer Absatz | in derselben Zelle nach einer Leerzeile (zweimal Alt+Enter, Mac: Ctrl+Option+Enter) |
   | Neue Zeile / Überschrift | **ganze Zeile** einfügen (Zeilennummer → Rechtsklick → Zeilen einfügen), in „Typ“ die Art wählen (wird grün) |
   | Absatz löschen | `!Löschen!` in die Zelle (wird rot) |
   | Ganze Seite löschen | `!Löschen!` in die graue Zeile „Seite“ |
   | Reihenfolge ändern | ganze Zeile ausschneiden und an der neuen Stelle einfügen |

   Immer **ganze Zeilen** einfügen oder verschieben, nie einzelne Zellen. Eine leere
   Zelle löscht nichts – gelöscht wird nur mit `!Löschen!`.
3. **Startseite und Team** haben je ein Blatt „… – Ansicht“ (orange Lasche), aufgebaut
   wie die Website. Nur in die weissen Felder schreiben. Im Team: leere Karte ausfüllen =
   neue Person, `!Löschen!` im Namen = Person weg.
   **Uniguide – Ansicht** enthält die ganze Uni-Tabelle: je Uni eine Zeile, je Angabe eine
   Spalte. Texte (grüne Spaltenköpfe) gelten für die Sprache der Mappe, der Rest für alle.
   Spaltennamen lassen sich in Zeile 4 überschreiben, rechts gibt es leere Spalten für neue
   Angaben, Zeile 5 bestimmt, wo eine Angabe erscheint.
   **Häufige Fragen – Ansicht** enthält alle Fragen: leere Zeile unten ausfüllen = neue Frage,
   `!Löschen!` in „Frage“ = Frage weg (in allen Sprachen).
4. **Neue Saison:** im Team-Blatt oben „Neue Saison starten“ ausfüllen (z. B. 2027/28).
   Das bisherige Team kommt dann in allen drei Sprachen ins Archiv.
5. **Hochladen:** auf GitHub in den Ordner [`redaktion/`](../redaktion/) → *Add file →
   Upload files* → *Commit changes*. Nach ein, zwei Minuten gibt es unter *Pull requests*
   einen Vorschlag mit einem Bericht (was übernommen, was übersprungen wurde).
   **Live ist es erst, wenn jemand den Vorschlag übernimmt (Merge).**
   **So übernimmst du den Vorschlag:** oben auf *Pull requests* → den neuen Vorschlag
   anklicken → den Bericht lesen. Der Reiter *Files changed* zeigt rot, was wegfällt, und
   grün, was dazukommt. Stimmt alles: zurück auf *Conversation*, ganz unten **Merge pull
   request** → **Confirm merge**. Steht im Bericht ein ❌ (die Website baut nicht oder
   die Prüfung meldet Funde), noch nicht übernehmen: erst die genannte Stelle in einer
   frischen Mappe korrigieren und neu hochladen.

Französisch und Italienisch zeigen den deutschen Text als Vorlage daneben; fehlende
Übersetzungen stehen als leere Zeilen da und müssen nur ausgefüllt werden. Das Team auf
Französisch und Italienisch wird in der jeweiligen Mappe gepflegt.

> **Das Repository ist öffentlich.** Alles, was in einer hochgeladenen Mappe steht – auch
> Bemerkungen –, bleibt für alle lesbar.

Mehr dazu (was beim Einlesen genau passiert, Fehlerfälle): ausführliche Anleitung,
[Abschnitt 3](WARTUNG-DETAILLIERT.md#3-textmappen-excel-im-detail).

---

## 3. Kleine Korrekturen im Web-Editor

**[app.pagescms.org](https://app.pagescms.org)** – mit GitHub oder über die
Einladungs-E-Mail anmelden, Repository `Kroeppster/nc-wiki` öffnen. Links wählst du die
Sprache und Seiten, News oder Erfahrungsberichte, änderst den Text wie in einem
Textprogramm und klickst **Save**. Das ist sofort eine Änderung auf `main` und nach ein
bis zwei Minuten live.

Drei Regeln:

- Graue Kästen mit `baustein` (Team, Testablauf, Generatoren …) stehen lassen, nicht
  hineinschreiben.
- Links auf eigene Seiten nur mit dem Pfad schreiben, z. B. `/ems/uniguide` (siehe
  [Abschnitt 9](#9-links-und-bausteine-im-text)).
- Umbenennen und Löschen von Seiten nicht im Editor, sondern auf GitHub
  ([Abschnitt 8](#8-eine-datei-oder-seite-löschen)).

Die Startseite (Zeitstrahl, Kacheln) und das Team pflegt man besser über die Excel-Mappe.

---

## 4. Einen News-Beitrag schreiben

**Im Web-Editor:** *News* der gewünschten Sprache → neuen Eintrag anlegen → Titel, Datum,
Schlagwort (z. B. „Update“) und Text ausfüllen → **Save**.

**Auf GitHub:** in `content/de/news/` eine neue Datei `mein-titel.md` anlegen (*Add file →
Create new file*). Eine fertige Vorlage zum Kopieren steht in
[`docs/vorlage-news.md`](vorlage-news.md).

Die ersten Sätze erscheinen automatisch als Vorschau auf der News-Übersicht und der
Startseite. Solange im Kopf `draft: true` steht, bleibt der Beitrag unsichtbar.
Denselben Beitrag bitte auch auf Französisch und Italienisch anlegen (gleicher Dateiname
unter `content/fr/news/` bzw. `content/it/news/`).

Zwei Dinge, die oft übersehen werden:

- **Gleicher Dateiname in allen Sprachen.** Der Web-Editor schlägt den Dateinamen aus dem
  Titel vor, und der lautet in jeder Sprache anders. Trag beim Anlegen in allen drei
  Sprachen denselben Namen ein (z. B. `testsimulation-2027.md`), sonst führt die
  Sprachwahl oben rechts nicht zur anderen Fassung.
- **Ein Datum in der Zukunft** hält den Beitrag zurück: Er erscheint erst, wenn der Tag
  erreicht ist und die Website danach das nächste Mal gebaut wird.

---

## 5. Ein PDF hochladen

**Übungsserie, Testsimulation, Kursskript** – einfach in den richtigen Ordner hochladen,
es erscheint automatisch auf der Website:

| Material | Ordner |
| --- | --- |
| Übungsserien | `assets/downloads/uebungsaufgaben/<untertest>/` (Unterordner gibt es schon) |
| Testsimulationen | `assets/downloads/testsimulationen/` |
| Kursskripte | `assets/downloads/kursskripte/` |
| Mitgliederbereich | `assets/downloads/mitglieder/` |

Auf GitHub zum Ordner gehen → *Add file → Upload files* → PDF hineinziehen → *Commit
changes*. Übungsserien heissen `<Jahr>_<Ordnername>_S<Nummer>.pdf`, z. B.
`2027_muster-zuordnen_S02.pdf`; die Lösung gleich mit `_Loesung` am Ende. Daraus entsteht
der Name auf der Website automatisch.

**Französisch und Italienisch:** Die Dateien dieser Sprachen kommen in den Unterordner
`fr/` bzw. `it/` des jeweiligen Ordners (z. B. `assets/downloads/uebungsaufgaben/muster-zuordnen/fr/`),
gleich benannt. Jede Sprachfassung der Website zeigt nur die Dateien ihrer Sprache.

**Jahresbericht und andere Einzeldokumente** brauchen eine eigene Seite – siehe
ausführliche Anleitung, [Abschnitt 2](WARTUNG-DETAILLIERT.md#2-seiten-menü-und-navigation).

---

## 6. Ein Bild einfügen

Jede Seite kann **ein** Titelbild haben (oben auf der Seite und als Vorschau in
Übersichten).

1. Bild hochladen nach `assets/images/<bereich>/`, z. B.
   `assets/images/news/testsimulation-2027.jpg`.
2. Im Kopf der Seite ergänzen:

   ```yaml
   featured_image: "news/testsimulation-2027.jpg"
   featured_image_alt: "Kurze Beschreibung, was auf dem Bild zu sehen ist"
   ```

   Der Pfad beginnt **nach** `assets/images/`. Die Beschreibung ist Pflicht (für
   Menschen mit Screenreader); ohne sie schlägt der Bau fehl.

Grosse Bilder sind kein Problem – die Website verkleinert sie selbst.

**Bilder im Text** (z. B. Screenshots in einem News-Beitrag): Bild ebenfalls nach
`assets/images/<bereich>/` hochladen und im Text auf einer eigenen Zeile einfügen:

```markdown
![Was auf dem Bild zu sehen ist](news/neue-website/uniguide.png "Bildunterschrift")
```

Die Beschreibung in den eckigen Klammern ist Pflicht, die Bildunterschrift in
Anführungszeichen freiwillig. Der Pfad beginnt auch hier **nach** `assets/images/`.
Stimmt er nicht, schlägt der Bau mit einer Meldung fehl.

---

## 7. Eine neue Seite anlegen

1. Auf GitHub zum passenden Ordner unter `content/de/` gehen → *Add file → Create new
   file*.
2. Dateiname: klein, ohne Umlaute und Leerzeichen, endet auf `.md`
   (z. B. `neue-seite.md`). Er wird Teil der Adresse und muss in allen drei Sprachen
   **gleich** sein.
3. Inhalt:

   ```markdown
   ---
   title: "Titel der Seite"
   description: "Ein Satz, der in Google unter dem Titel erscheint (max. 160 Zeichen)."
   ---

   Text der Seite.
   ```

4. Dieselbe Datei mit übersetztem Text unter `content/fr/` und `content/it/` anlegen.

Soll die Seite im Menü erscheinen, siehe ausführliche Anleitung,
[Abschnitt 2](WARTUNG-DETAILLIERT.md#2-seiten-menü-und-navigation).

---

## 8. Eine Datei oder Seite löschen

Datei auf GitHub öffnen → oben rechts **…** → *Delete file* → *Commit changes*.

- Eine Seite in **allen drei Sprachen** löschen.
- Bei Übungsserien Aufgabe **und** `_Loesung` löschen.
- Zeigt noch ein Link auf die gelöschte Seite, wird der Bau rot und nennt die Stelle –
  dort den Link entfernen.

---

## 9. Links und Bausteine im Text

**Interne Links** als normalen Link mit dem Pfad, ohne Sprache:

```markdown
Mehr dazu im [Uniguide](/ems/uniguide).
```

Auf der französischen Seite wird daraus automatisch der Link zur französischen Seite.
Gibt es die Zielseite nicht, bricht der Bau mit einer Meldung ab – so geht nie ein toter
Link online.

**Bausteine** (Team-Karten, Testablauf-Tabelle, Generatoren, Sponsoring-Kontakt) stehen
als grauer Kasten im Text:

````markdown
```baustein
team-leitung
```
````

Man darf sie verschieben, aber nicht hineinschreiben. Keine `{{< … >}}`-Klammern in den
Text schreiben – der Web-Editor zerstört sie.

---

## 10. Wenn der Bau rot ist

**Die Website bleibt online** – es fehlt nur die neueste Änderung, bis der Fehler behoben
ist.

1. Auf GitHub oben **Actions** → den obersten Lauf mit rotem ✗ öffnen → Job **build**.
2. Den Schritt mit ✗ aufklappen; meist steht dort die betroffene Datei.

| Rot bei | Meist | Was tun |
| --- | --- | --- |
| „Check internal links“ oder „Build with Hugo“ mit „Link“ | ein Link zeigt ins Leere | Link in der genannten Datei korrigieren |
| „Build with Hugo“ | Fehler im Seitenkopf (Anführungszeichen, Einrückung, fehlende Bildbeschreibung) | mit einer funktionierenden Datei vergleichen |
| „Check built site“ | eine Seite ohne Titel, Beschreibung oder Hauptüberschrift, eine Adresse ohne `/nc-wiki/` oder Text aus dem Mitgliederbereich, der ungeschützt irgendwo steht | die Meldung nennt Art und Datei; das in der genannten Datei korrigieren |

Links auf fremde Websites prüft ein eigener Ablauf einmal pro Woche („Externe Links
prüfen“); ist er rot, ist ein solcher Link kaputt, die Website selbst läuft normal.
Ebenso „Prüfstand“ (jede Nacht): Er klickt die Website im Browser durch und ändert
nichts an ihr. Kommst du nicht weiter: unter *Issues → New issue* den Link zum roten Lauf posten.

Bei einem Pull Request läuft dieselbe Prüfung schon vor dem Übernehmen – ein rotes ✗
dort heisst: noch nicht mergen.

---

## 11. Eine Datei direkt auf GitHub ändern

Für alles, was der Web-Editor nicht anbietet, oder wenn du lieber auf GitHub arbeitest.

1. [github.com/Kroeppster/nc-wiki](https://github.com/Kroeppster/nc-wiki) öffnen und
   anmelden.
2. **Die Datei finden.** Die Seiten liegen unter `content/de/` (Französisch: `content/fr/`,
   Italienisch: `content/it/`), aufgebaut wie die Adressen der Website:

   | Adresse der Seite | Datei |
   | --- | --- |
   | `…/nc-wiki/impressum/` | `content/de/impressum.md` |
   | `…/nc-wiki/ems/` | `content/de/ems/_index.md` (Übersichtsseite eines Ordners) |
   | `…/nc-wiki/fr/ems/uniguide/` | `content/fr/ems/uniguide/_index.md` |

   Schneller: oben im Feld *Go to file* einen Teil des Namens tippen.
3. Datei anklicken → oben rechts das **Stift-Symbol** (*Edit this file*).
4. Text ändern. Im Seitenkopf (zwischen den `---`) nur das ändern, was in
   Anführungszeichen steht; die Wörter vor dem Doppelpunkt und die Einrückung bleiben.
5. Oben rechts **Commit changes…** → in einem Satz beschreiben, was du geändert hast →
   **Commit changes**.
6. Ein bis zwei Minuten warten und die Seite neu laden
   ([Abschnitt 12](#12-kontrollieren-und-rückgängig-machen)).

---

## 12. Kontrollieren und rückgängig machen

**Ist meine Änderung live?** Auf GitHub oben **Actions**. Der oberste Lauf «Deploy Hugo
site to GitHub Pages» zeigt den Stand:

| Zeichen | Bedeutung |
| --- | --- |
| gelber Kreis | der Bau läuft noch (etwa zwei Minuten) |
| grüner Haken | fertig, die Änderung ist live |
| rotes Kreuz | ein Fehler, die Änderung ist **nicht** live ([Abschnitt 10](#10-wenn-der-bau-rot-ist)) |

Danach die Seite im Browser neu laden, am besten ohne Zwischenspeicher: Ctrl+F5
(Windows) oder Cmd+Shift+R (Mac).

**Die Änderung erscheint nicht?** Der Reihe nach prüfen:

1. Ist der Bau grün? (siehe oben)
2. Textmappe hochgeladen: Wurde der Vorschlag unter *Pull requests* schon übernommen?
3. Steht im Seitenkopf `draft: true`, oder liegt das Datum in der Zukunft? Dann bleibt
   die Seite verborgen.
4. Schaust du die richtige Sprache an? Eine Änderung unter `content/de/` zeigt sich nur
   auf der deutschen Seite.
5. Liegt die Datei im richtigen Ordner und endet auf `.md`?

**Etwas rückgängig machen**

- **Eine übernommene Textmappe (Pull Request):** *Pull requests* → *Closed* → den
  Vorschlag öffnen → unten **Revert** → es entsteht ein neuer Vorschlag, der alles
  zurücknimmt → diesen übernehmen (Merge).
- **Eine einzelne Datei:** Datei öffnen → oben rechts **History**. Dort steht jede
  Fassung mit Datum und Beschreibung. Die Fassung anklicken, die noch gestimmt hat →
  oben rechts **…** → *View file* → den Text kopieren. Zurück zur heutigen Datei,
  Stift-Symbol, alles durch den kopierten Text ersetzen, **Commit changes**.
- **Eine gelöschte Datei oder wenn du unsicher bist:** unter *Issues → New issue*
  beschreiben, was passiert ist. Es geht nichts verloren; jemand mit mehr Erfahrung holt
  es zurück.

---

## 13. Checkliste für das neue Jahr

Einmal im Jahr, sobald das Datum des nächsten EMS feststeht.

| Was | Wo | Wie |
| --- | --- | --- |
| Datum des nächsten EMS (Countdown auf der Startseite) | Datei `hugo.toml`, Zeile `ems_exam_date` | wie in [Abschnitt 11](#11-eine-datei-direkt-auf-github-ändern): nur das Datum zwischen den Anführungszeichen ändern. Form: `2027-07-09T08:00:00+02:00` heisst 9. Juli 2027, 8 Uhr, Schweizer Sommerzeit. Der Text über dem Countdown übernimmt das Datum von selbst |
| Termine im Zeitstrahl der Startseite | Textmappe, Blatt «Startseite – Ansicht» | [Abschnitt 2](#2-texte-ändern-mit-der-excel-textmappe) |
| Datum in den Häufigen Fragen | Textmappe, Blatt «Häufige Fragen – Ansicht» | Abschnitt 2 |
| Datum auf der Seite «EMS» | Web-Editor, Seite «EMS» | [Abschnitt 3](#3-kleine-korrekturen-im-web-editor) |
| Fristen und «Stand» im Uniguide | Textmappe, Blatt «Uniguide – Ansicht» | Abschnitt 2; nur eintragen, was auf einer offiziellen Seite steht |
| neue Saison im Team | Textmappe, Blatt «Team – Ansicht», «Neue Saison starten» | Abschnitt 2 |
| neue Testsimulation, neue Übungsserien | PDFs hochladen | [Abschnitt 5](#5-ein-pdf-hochladen) |
| Lösungen für «Antwortbogen auswerten» und «Konztest auswerten» | braucht jemanden mit Technik-Kenntnissen | [ausführliche Anleitung, Abschnitt 11](WARTUNG-DETAILLIERT.md#11-lern-generatoren-und-alpha-seite) |

Zum Schluss auf der Website mit der Lupe nach dem alten Jahr suchen: Was noch
auftaucht und kein Rückblick ist, wurde vergessen.

---

## 14. Schreibhilfe für Texte

So schreibst du in einer `.md`-Datei und in der Spalte «Text» der Textmappe. Im
Web-Editor gibt es dafür Knöpfe.

| Du willst | Du schreibst |
| --- | --- |
| eine Zwischenüberschrift | `## Titel` (kleinere: `### Titel`). Nie nur ein `#`, die oberste Überschrift ist schon der Seitentitel |
| fett | `**wichtig**` |
| eine Aufzählung | jede Zeile beginnt mit `- ` |
| eine nummerierte Liste | jede Zeile beginnt mit `1. `, `2. ` … |
| einen neuen Absatz | eine Leerzeile dazwischen |
| einen Link auf eine eigene Seite | `[Uniguide](/ems/uniguide)` ([Abschnitt 9](#9-links-und-bausteine-im-text)) |
| einen Link auf eine fremde Seite | `[swissuniversities](https://www.swissuniversities.ch/)` |
| den Genderstern | `Tutor\*innen`, mit einem Rückstrich vor dem Stern. Ohne ihn macht Markdown aus zwei Sternen im selben Absatz Kursivschrift, und der Bau bricht mit einem Hinweis ab. Im Web-Editor einfach `*` tippen |
| Anführungszeichen | «so», nicht "so" |

Wie wir schreiben (du-Anrede, Begriffe, Datum «9. Juli 2027»), steht im
[Styleguide](STYLEGUIDE.md).

---

## 15. Die wichtigsten Regeln

- **Alles dreisprachig.** Neue sichtbare Texte immer auf Deutsch, Französisch und
  Italienisch.
- **Gleicher Dateiname in allen Sprachen.** Nur so findet die Sprachwahl die anderen
  Fassungen einer Seite.
- **Das Repository ist öffentlich.** Keine Passwörter, Personendaten oder internen Notizen
  in Dateien oder Textmappen. Zugänge gehören in den Passwort-Manager des Vereins.
- **Keine Zahlen erfinden.** Im Uniguide nur eintragen, was auf einer offiziellen Seite
  steht; Anzahlen auf der Startseite zählt die Website selbst.
- **Lizenzhinweis bleibt.** Die Übungsaufgaben stehen unter CC BY-NC 4.0; der Hinweis wird
  nicht entfernt.
- **Im Zweifel fragen**, bevor du an `layouts/`, `.github/` oder `hugo.toml` etwas
  änderst.
