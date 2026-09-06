# PDFs für den Mitgliederbereich

In diesen Ordner kommen die PDF-Dateien, die auf der Seite
"Spesenformular" im Mitgliederbereich zum Herunterladen angeboten werden
(`content/<sprache>/mitglieder/spesenformular.md`). Einfach die Datei hier
ablegen - sie erscheint beim nächsten Bauen der Website automatisch in der
Liste, es muss nichts weiter eingetragen werden. Passt der automatisch
erzeugte Anzeigename nicht, lässt er sich in `data/downloads.yaml`
überschreiben (gleiche Funktionsweise wie bei allen anderen
Download-Ordnern, siehe `assets/downloads/uebungsaufgaben/README.md`).

# WICHTIG: Diese PDFs sind NICHT passwortgeschützt

Die *Seite*, auf der diese Dateien verlinkt sind, wird beim Veröffentlichen
mit einem Passwort geschützt. Die PDF-Dateien selbst sind es nicht: Sie
liegen ganz normal auf dem Webserver und sind für jede Person abrufbar, die
ihre genaue Adresse kennt oder errät. Der Schutz besteht praktisch darin,
dass diese Adressen nirgends öffentlich stehen - nicht darin, dass der
Server jemanden abweisen würde.

Daraus folgt: In diesen Ordner gehören interne Formulare und Merkblätter -
also Dinge, die schlicht niemanden ausserhalb des Vereins interessieren.
NICHT hierher gehören Personendaten von Mitgliedern, Kontoauszüge,
Bewerbungsunterlagen oder irgendetwas anderes, das echten Schaden
anrichtet, wenn es an die Öffentlichkeit gerät.

Mehr dazu in `docs/WARTUNG.md`, Abschnitt "Mitgliederbereich".
