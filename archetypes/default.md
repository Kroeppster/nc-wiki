+++
# Das ist Hugos eingebaute Standard-Vorlage, die automatisch verwendet wird,
# wenn jemand eine neue Seite über den lokalen Befehl "hugo new" anlegt und
# es KEINE spezielle Vorlage dafür gibt (siehe archetypes/news.md,
# erfahrungsbericht.md, jahresbericht.md für die spezielleren Vorlagen mit
# ausführlicheren Erklärungen zu den einzelnen Feldern).
date = '{{ .Date }}'
draft = true
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
+++
