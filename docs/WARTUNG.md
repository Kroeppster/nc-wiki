# Website pflegen – Kurzanleitung

**Deutsch** · [Français](WARTUNG.fr.md) · [Italiano](WARTUNG.it.md)

Hier steht nur das, was im Alltag vorkommt: Texte ändern, News schreiben, PDFs und
Bilder hochladen, etwas löschen. Alles geht im Browser, installieren musst du nichts.
Alles andere (Startseite, Team, Menü, Design, Formulare, Mitgliederbereich, Technik)
steht in der **[ausführlichen Anleitung](WARTUNG-DETAILLIERT.md)**.

---

## 1. Welcher Weg wofür?

| Du willst … | Weg | Abschnitt |
| --- | --- | --- |
| viele Texte durchsehen, übersetzen, Startseite oder Team ändern | **Excel-Textmappe** | [2](#2-texte-ändern-mit-der-excel-textmappe) |
| schnell einen Tippfehler auf einer Seite korrigieren | **Web-Editor** (Pages CMS) | [3](#3-kleine-korrekturen-im-web-editor) |
| einen News-Beitrag schreiben | Web-Editor oder GitHub | [4](#4-einen-news-beitrag-schreiben) |
| ein PDF oder Bild hochladen, eine Datei löschen | **GitHub** | [5](#5-ein-pdf-hochladen) – [8](#8-eine-datei-oder-seite-löschen) |

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
   **Q&A – Ansicht** enthält alle Fragen: leere Zeile unten ausfüllen = neue Frage,
   `!Löschen!` in „Frage“ = Frage weg (in allen Sprachen).
4. **Neue Saison:** im Team-Blatt oben „Neue Saison starten“ ausfüllen (z. B. 2027/28).
   Das bisherige Team kommt dann in allen drei Sprachen ins Archiv.
5. **Hochladen:** auf GitHub in den Ordner [`redaktion/`](../redaktion/) → *Add file →
   Upload files* → *Commit changes*. Nach ein, zwei Minuten gibt es unter *Pull requests*
   einen Vorschlag mit einem Bericht (was übernommen, was übersprungen wurde).
   **Live ist es erst, wenn jemand den Vorschlag übernimmt (Merge).**

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

„Check external links“ ist nur eine Warnung und macht nichts kaputt. Kommst du nicht
weiter: unter *Issues → New issue* den Link zum roten Lauf posten.

Bei einem Pull Request läuft dieselbe Prüfung schon vor dem Übernehmen – ein rotes ✗
dort heisst: noch nicht mergen.

---

## 11. Die wichtigsten Regeln

- **Alles dreisprachig.** Neue sichtbare Texte immer auf Deutsch, Französisch und
  Italienisch.
- **Das Repository ist öffentlich.** Keine Passwörter, Personendaten oder internen Notizen
  in Dateien oder Textmappen. Zugänge gehören in den Passwort-Manager des Vereins.
- **Keine Zahlen erfinden.** Im Uniguide nur eintragen, was auf einer offiziellen Seite
  steht; Anzahlen auf der Startseite zählt die Website selbst.
- **Lizenzhinweis bleibt.** Die Übungsaufgaben stehen unter CC BY-NC 4.0; der Hinweis wird
  nicht entfernt.
- **Im Zweifel fragen**, bevor du an `layouts/`, `.github/` oder `hugo.toml` etwas
  änderst.
