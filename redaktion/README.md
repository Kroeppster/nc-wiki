# Texte über Excel bearbeiten

**1. Frische Mappe holen** – eine je Sprache, nach jeder Änderung automatisch neu,
auf der Repo-Startseite rechts unter *Releases → Textmappen*:

- Deutsch: <https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-de.xlsx>
- Français : <https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-fr.xlsx>
- Italiano: <https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-texte-it.xlsx>

**2. Bearbeiten** – direkt in den Zellen. Wie, steht vorne in der Mappe im Blatt
„Anleitung": Text überschreiben (wird gelb), neuer Absatz in derselben Zelle
nach einer Leerzeile (Alt+Enter), ganze Zeile einfügen (grün),
`!Löschen!` in die Zelle (rot), `!Löschen!` in die graue Zeile „Seite" für eine
ganze Seite.

**3. Hier hochladen** – in diesem Ordner oben rechts *Add file → Upload files*,
Datei hineinziehen, unten *Commit directly to the main branch* → *Commit changes*.

Nach ein, zwei Minuten gibt es unter *Pull requests* einen Vorschlag mit einem
Bericht: was geändert wurde, was übersprungen wurde und warum. Live ist es erst,
wenn jemand den Vorschlag übernimmt (*Merge*). Die hochgeladene Datei wird dabei
wieder entfernt.

> **Das Repository ist öffentlich.** Was in der Mappe steht – auch Bemerkungen
> und Zuständigkeiten – ist nach dem Hochladen für alle sichtbar.

`stand.json` merkt sich „Stand", „Bemerkung" und „Zuständig" aus den
hochgeladenen Mappen, damit sie in der nächsten frischen Mappe wieder drinstehen.
Nicht von Hand bearbeiten.

---

# Wortliste des Fakten-Generators (eigene Excel)

Die Wörter des Fakten-Generators auf der Alpha-Seite (Nachnamen, Berufe, Krankheiten,
Merkmale) pflegst du in einer **eigenen** Excel-Datei, getrennt von den Textmappen:

<https://github.com/Kroeppster/nc-wiki/releases/download/textmappen/ncwiki-wortliste-fakten-generator.xlsx>

Auch sie ist immer frisch (nach jeder Änderung neu). Ein Blatt je Liste; „Anleitung“ und
„Übersicht“ stehen vorne – die Übersicht zählt mit, ob genug Wörter da sind.

**Hochladen** wie oben (*Add file → Upload files* in diesem Ordner), der Dateiname muss mit
`ncwiki-wortliste` beginnen. Die Automatisierung prüft die Datei:

- **In Ordnung** → Pull Request mit Bericht (was neu ist, was wegfällt, was zu beachten ist),
  die Datei wird entfernt. Live erst nach dem *Merge*.
- **Fehler** (zu wenige Wörter, ein Wort doppelt, Geschlecht nicht m/w …) → es wird **nichts**
  übernommen und kein Pull Request eröffnet. Unter *Actions → Wortliste einlesen* steht jeder
  Fehler mit Blatt und Zeile. Korrigieren und noch einmal hochladen.

Die Datei ersetzt die **ganze** Liste: immer von der frischen Datei ausgehen, nie von einer
alten Kopie (der Bericht warnt, wenn sie veraltet ist). Wie die Datei aufgebaut ist und was
der Generator braucht: [docs/WARTUNG-DETAILLIERT.md, Abschnitt 11](../docs/WARTUNG-DETAILLIERT.md#fakten-generator).

---

Nur eine Seite schnell korrigieren? Dafür gibt es auch den Web-Editor
[app.pagescms.org](https://app.pagescms.org) – siehe
[docs/WARTUNG.md, Abschnitt 3](../docs/WARTUNG.md#3-kleine-korrekturen-im-web-editor).

Alles Weitere: [docs/WARTUNG.md, Abschnitt 2](../docs/WARTUNG.md#2-texte-ändern-mit-der-excel-textmappe) und [docs/WARTUNG-DETAILLIERT.md, Abschnitt 3](../docs/WARTUNG-DETAILLIERT.md#3-textmappen-excel-im-detail).
