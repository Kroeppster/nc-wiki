---
# Titel der Seite, z.B. "Jahresbericht 2027". Erscheint als Überschrift auf der
# Beitragsseite und als Kartentitel in der Übersicht unter Über uns -> Jahresberichte.
title: "Jahresbericht {{ now.Year }}"

# Datum bestimmt die Sortierung (neuestes zuerst) auf der Übersichtsseite. Reicht,
# wenn nur das Jahr stimmt (z.B. 2027-01-01), muss kein exaktes Publikationsdatum sein.
date: {{ .Date }}

# Optional: kurzes Label über dem Titel in der Kartenübersicht, z.B. "Tätigkeitsbericht".
# eyebrow: ""

# PDF(s) zum Download. "path" ist relativ zum static/-Ordner - die Datei muss dort
# genau unter diesem Pfad liegen, z.B. bei path "downloads/jahresberichte/2027.pdf"
# gehört die Datei nach static/downloads/jahresberichte/2027.pdf. "label" ist der
# angezeigte Linktext; die Dateigrösse wird automatisch dazu ergänzt.
downloads:
  - path: "downloads/jahresberichte/DATEINAME.pdf"
    label: "Jahresbericht {{ now.Year }} (PDF)"

# Solange draft: true gesetzt ist, erscheint die Seite NICHT im veröffentlichten Build
# (auch nicht nach dem Push). Vor dem Fertigstellen auf false setzen.
draft: true
---

Kurze Zusammenfassung des Berichtsjahres (2-4 Sätze) - erscheint als Vorschautext auf
der Übersichtsseite. Der PDF-Download erscheint automatisch unterhalb dieses Texts.
