# Vorlage: Neuer News-Beitrag

Für alle, die direkt im GitHub-Browser arbeiten und kein Hugo installiert haben.
Wer stattdessen lokal an der Website arbeitet, kann auch `hugo new content/de/news/dein-titel.md`
verwenden – das erzeugt automatisch die gleiche Vorlage mit Erklärungen (siehe `archetypes/news.md`).

## So gehst du vor

1. Im Repo zu `content/de/news/` navigieren.
2. Auf **"Add file" → "Create new file"** klicken.
3. Als Dateiname `dein-titel.md` eingeben (siehe Hinweise zum Dateinamen unten),
   z. B. `neue-anmeldefrist-2027.md`.
4. Den kompletten Block unter "Zum Kopieren" unten in das leere Textfeld einfügen.
5. Die Platzhalter (`___`) durch deinen eigenen Text ersetzen.
6. Unten bei "Commit changes" **"Create a new branch for this commit and start a pull request"**
   auswählen und den Pull Request erstellen – nicht direkt in `main` committen.
7. Jemand aus dem Team prüft den PR kurz und merged ihn. Danach ist der Beitrag live
   (sofern `draft: false` gesetzt ist, siehe unten).

**Dateiname:** klein geschrieben, nur Buchstaben/Zahlen/Bindestriche, keine Umlaute
(ä→ae, ö→oe, ü→ue, ß→ss) und keine Leerzeichen (durch `-` ersetzen). Er wird Teil der
Web-Adresse des Beitrags.

**Nur Deutsch nötig.** Eine FR/IT-Version ist willkommen, aber nicht Pflicht – dafür
dieselbe Datei mit demselben Namen zusätzlich unter `content/fr/news/` bzw.
`content/it/news/` anlegen, mit übersetztem Inhalt.

---

## Zum Kopieren

```markdown
---
title: "___Titel des Beitrags___"
date: 2027-03-15
eyebrow: "___Kurzes Schlagwort, z. B. Update / Anmeldung offen / Termin___"
draft: true
---

___Kurzer Einleitungstext (1-2 Sätze) - das ist die Vorschau, die auf der
News-Übersicht und der Startseite erscheint.___

___Restlicher Beitragstext hier.___
```

---

## Felder erklärt

| Feld | Pflicht? | Bedeutung |
| --- | --- | --- |
| `title` | ja | Überschrift des Beitrags. Erscheint auf der Beitragsseite, in der News-Übersicht und in der Vorschau auf der Startseite. |
| `date` | ja | Datum im Format `JJJJ-MM-TT`. Bestimmt die Reihenfolge (neuestes zuerst). Muss nicht exakt der Veröffentlichungstag sein. |
| `eyebrow` | ja | Kurzes Schlagwort über dem Titel, z. B. "Update", "Anmeldung offen", "Termin". Frei wählbar. |
| `draft` | ja | Solange `true`, wird der Beitrag **nicht** auf der echten Website angezeigt, auch nach dem Merge nicht. Erst auf `false` setzen, wenn der Beitrag fertig und freigegeben ist. |

**Optional** (nur nötig, wenn ein Bild dabei sein soll – im Beispiel oben weggelassen):

```yaml
featured_image: "news/dein-bild.jpg"
featured_image_alt: "___Beschreibung des Bildes für Screenreader___"
```

Das Bild selbst muss zusätzlich als Datei nach `assets/images/news/dein-bild.jpg`
hochgeladen werden (im GitHub-Browser über "Add file" → "Upload files" im passenden
Ordner). Ohne `featured_image` erscheint der Beitrag einfach ohne Bild – völlig normal.

Alles nach der zweiten `---`-Zeile ist der eigentliche Beitragstext und kann normales
Markdown enthalten (Absätze, `**fett**`, `[Links](https://...)`, Listen mit `- `, usw.).
