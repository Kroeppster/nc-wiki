---
# Titel des News-Beitrags. Erscheint als Überschrift auf der Beitragsseite, als
# Kartentitel in der News-Übersicht und im Vorschau-Ausschnitt auf der Startseite.
title: "{{ replace .File.ContentBaseName "-" " " | title }}"

# Veröffentlichungsdatum (JJJJ-MM-TT, optional mit Uhrzeit). Bestimmt die Sortierung
# (neuestes zuerst) auf der News-Übersicht und in den 2 Vorschaukarten auf der Startseite.
date: {{ .Date }}

# Kurzes Schlagwort über dem Titel, z.B. "Update", "Anmeldung offen", "Termin".
# Frei wählbar, kein festes Vokabular - erscheint sowohl auf der Übersicht als auch
# in der Vorschau auf der Startseite.
eyebrow: ""

# Optional: Bild für die Beitragsseite und die Kartenvorschau. Pfad relativ zu
# assets/images/, z.B. "news/testsimulation-2027.jpg". Zeile auskommentiert lassen,
# wenn kein Bild vorhanden ist - der Beitrag erscheint dann einfach ohne Bild.
# featured_image: ""

# Pflicht, sobald featured_image gesetzt ist: Alt-Text fürs Bild (Bildbeschreibung
# für Screenreader/SEO). Ohne featured_image wird dieses Feld ignoriert.
# featured_image_alt: ""

# Solange draft: true gesetzt ist, erscheint die Seite NICHT im veröffentlichten Build
# (auch nicht nach dem Push). Vor dem Fertigstellen auf false setzen.
draft: true
---

Kurzer Einleitungstext (1-2 Sätze). Das ist der Text, der als Vorschau in der
News-Übersicht und auf der Startseite erscheint - entweder automatisch die ersten
Wörter, oder bis zu einer optionalen Markierung `<!--more-->` im Text.

Der restliche Beitragstext folgt hier in normalem Markdown (Absätze, **fett**,
[Links](/), Listen etc.).
