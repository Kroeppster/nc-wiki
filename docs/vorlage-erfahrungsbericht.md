# Vorlage: Neuer Erfahrungsbericht

**Der normale Weg für Erfahrungsberichte ist das Formular auf der Website**
(`ems/erfahrungsberichte/bericht-einreichen/`) – das legt automatisch einen Pull
Request an, ganz ohne GitHub-Kenntnisse. Diese Vorlage hier ist für den Fall, dass
jemand aus dem Team einen Bericht direkt im Repo einpflegen möchte (z. B. weil er auf
anderem Weg eingegangen ist, oder zur Überarbeitung eines eingereichten Berichts).

Wer lokal an der Website arbeitet, kann statt dieser Vorlage auch
`hugo new --kind erfahrungsbericht content/de/ems/erfahrungsberichte/dein-dateiname.md`
verwenden – das erzeugt automatisch die gleiche Vorlage mit Erklärungen (siehe
`archetypes/erfahrungsbericht.md`).

## So gehst du vor

1. Im Repo zu `content/de/ems/erfahrungsberichte/` navigieren.
2. Auf **"Add file" → "Create new file"** klicken.
3. Als Dateiname `bericht-vorname-x.md` eingeben (siehe Hinweise zum Dateinamen unten),
   z. B. `bericht-lena-h.md`.
4. Den kompletten Block unter "Zum Kopieren" unten in das leere Textfeld einfügen.
5. Die Platzhalter (`___`) durch den echten Text ersetzen.
6. Unten bei "Commit changes" **"Create a new branch for this commit and start a pull
   request"** auswählen und den Pull Request erstellen – nicht direkt in `main` committen.
7. Jemand aus dem Team prüft den PR (Inhalt, Ton) und merged ihn. Danach ist der
   Bericht live (sofern `draft: false` gesetzt ist, siehe unten).

**Dateiname:** Muster `bericht-<name-in-kleinbuchstaben>.md`, z. B. `bericht-lena-h.md`.
Klein geschrieben, nur Buchstaben/Zahlen/Bindestriche, keine Umlaute (ä→ae, ö→oe, ü→ue,
ß→ss) und keine Leerzeichen (durch `-` ersetzen). Existiert der Name schon, eine Zahl
anhängen (`bericht-lena-h-2.md`).

**Kein `title`-Feld einfügen** – die Überschrift wird automatisch aus `name` und `jahr`
gebaut. Ein zusätzliches `title`-Feld würde einfach ignoriert.

**Datenschutz:** Nur den angezeigten Namen/das Pseudonym übernehmen, keine E-Mail-Adresse
oder andere Kontaktdaten in die Datei schreiben – der Pull Request ist öffentlich sichtbar.

---

## Zum Kopieren

```markdown
---
name: "___Anzeigename, z. B. Vorname + Initiale, oder Pseudonym___"
jahr: 2027
ort: "___Studienort, optional – Zeile löschen, wenn nicht bekannt___"
tags: []
draft: true
---

## Wie hast du dich vorbereitet?

___Antwort hier___

## Was hat dir am meisten geholfen?

___Antwort hier___

## Dein Tipp an zukünftige Teilnehmende?

___Antwort hier___
```

---

## Felder erklärt

| Feld | Pflicht? | Bedeutung |
| --- | --- | --- |
| `name` | ja | Angezeigter Name der berichtenden Person. Vorname + Initiale reicht, oder ein Pseudonym. |
| `jahr` | ja | EMS-Jahrgang als Zahl, ohne Anführungszeichen. Bestimmt Sortierung und den Jahres-Filter auf der Übersichtsseite. Ohne dieses Feld erscheint der Bericht gar nicht in der Übersicht. |
| `ort` | nein | Studienort/Hochschulstandort. Zeile ganz weglassen, wenn unbekannt. |
| `tags` | nein | Liste von Schlagworten, z. B. `["Naturwissenschaften", "Testsimulation"]`. Leere Liste `[]` ist ok. |
| `draft` | ja | Solange `true`, erscheint der Bericht **nicht** auf der echten Website, auch nach dem Merge nicht. Erst auf `false` setzen, wenn er freigegeben ist. |

Die drei Überschriften (`## Wie hast du dich vorbereitet?` usw.) genau so übernehmen –
das ist dieselbe Struktur, die auch beim automatischen Formular verwendet wird. Unter
jeder Überschrift steht die Antwort als normaler Fliesstext, kein weiteres Markdown nötig.
