# Ansagen für den Prüfungsmodus

Die Seite `/ems/pruefungsmodus/` sagt an, was als Nächstes kommt, sagt „Start"
und am Ende „Stopp". **Liegt hier eine passende Datei, wird sie abgespielt** –
sonst liest die Sprachausgabe des Geräts vor, die je nach Handy oder Computer
sehr unterschiedlich klingt.

Es muss nichts eingetragen oder umgestellt werden: Datei mit dem richtigen Namen
in den richtigen Sprachordner legen, fertig. Genau wie bei den PDF-Downloads.
Fehlt eine einzelne Datei, wird nur dieser eine Satz vorgelesen.

## Was gerade da ist

| Sprache | Aufnahmen | Stimme | Lizenz des Datensatzes |
| --- | --- | --- | --- |
| Deutsch | 15 | Thorsten (Piper, low) | CC0 – keine Auflagen |
| Französisch | 15 | SIWIS (Piper, medium) | CC-BY 4.0 – Namensnennung nötig |
| Italienisch | – | – | offen, siehe unten |

Die vorhandenen Dateien sind **maschinell erzeugt** (siehe
`scripts/ansagen-erzeugen.py`). Sie klingen deutlich ruhiger und gleichmässiger
als die Browserstimmen, aber es bleibt eine Maschine.

**Am besten wären echte Aufnahmen aus dem Verein.** Wer eine Datei einspricht,
überschreibt einfach die erzeugte – die Seite merkt keinen Unterschied. Es sind
15 kurze Sätze pro Sprache, in einer ruhigen halben Stunde machbar.

## Italienisch fehlt bewusst

Für Italienisch gab es zwar eine Stimme, aber die Lizenz des zugrunde liegenden
Datensatzes (M-AILABS) liess sich nicht eindeutig klären. Statt etwas zu
veröffentlichen, dessen Rechtslage unklar ist, liest auf Italienisch weiterhin
die Sprachausgabe des Geräts vor. Das funktioniert – es klingt nur weniger gut.
Wer die Lizenzfrage klärt oder die Sätze selbst einspricht, schliesst die Lücke.

## Namensnennung (Französisch)

Die französische Stimme beruht auf dem SIWIS-Datensatz der University of
Edinburgh, veröffentlicht unter CC-BY 4.0:
<https://datashare.is.ed.ac.uk/handle/10283/2353>. Wird die französische
Sprachfassung öffentlich genutzt, gehört dieser Hinweis dazu – deshalb steht er
hier und im Erzeugungsskript.

## Format

- **MP3**, Endung `.mp3` (andere Endungen werden nicht gefunden)
- Mono genügt, 96 kbit/s genügt
- Vorne und hinten je etwa eine halbe Sekunde Stille, sonst klingt der Einsatz
  abgehackt
- Ruhig und eher langsam sprechen. Das vertritt eine Aufsichtsperson im
  Testsaal, keine Werbung.

## Dateiname = was gesprochen wird

Wichtig bei den zusammengesetzten Sätzen (`stopp-weiter`, `fertig-*`): Sie
werden als **ein** Stück abgespielt, also auch in einem Stück aufnehmen.


---

## Deutsch  (`de/`)

| Datei | Gesprochener Text |
| --- | --- |
| `muster-zuordnen.mp3` | Muster zuordnen, dieser Untertest umfasst 18 Aufgaben, Sie haben 16 Minuten Zeit. |
| `med-nat-grundverstaendnis.mp3` | Medizinisch-naturwissenschaftliches Grundverständnis, dieser Untertest umfasst 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `objekte-im-raum.mp3` | Objekte im Raum, dieser Untertest umfasst 18 Aufgaben, Sie haben 10 Minuten Zeit. |
| `quantitative-probleme.mp3` | Quantitative und formale Probleme, dieser Untertest umfasst 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `figuren-einpraegen.mp3` | Figuren einprägen (Einprägephase), Sie haben 4 Minuten Zeit. |
| `fakten-einpraegen.mp3` | Fakten einprägen (Einprägephase), Sie haben 6 Minuten Zeit. |
| `textverstaendnis.mp3` | Textverständnis, dieser Untertest umfasst 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `figuren-reproduktion.mp3` | Figuren einprägen (Reproduktion), dieser Untertest umfasst 18 Aufgaben, Sie haben 5 Minuten Zeit. |
| `fakten-reproduktion.mp3` | Fakten einprägen (Reproduktion), dieser Untertest umfasst 18 Aufgaben, Sie haben 6 Minuten Zeit. |
| `diagramme-tabellen.mp3` | Diagramme und Tabellen, dieser Untertest umfasst 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `konzentriertes-arbeiten.mp3` | Konzentriertes und sorgfältiges Arbeiten, Sie haben 8 Minuten Zeit. |
| `beginne.mp3` | Start. |
| `stopp-weiter.mp3` | Stopp. Blättern Sie jetzt zum nächsten Untertest. |
| `fertig-einzeln.mp3` | Stopp. Die Übung ist beendet. |
| `fertig-komplett.mp3` | Stopp. Die Simulation ist beendet. |

---

## Français  (`fr/`)

| Datei | Gesprochener Text |
| --- | --- |
| `muster-zuordnen.mp3` | Association de motifs, ce sous-test comprend 18 exercices, vous disposez de 16 minutes. |
| `med-nat-grundverstaendnis.mp3` | Compréhension médico-scientifique, ce sous-test comprend 18 exercices, vous disposez de 45 minutes. |
| `objekte-im-raum.mp3` | Objets dans l'espace, ce sous-test comprend 18 exercices, vous disposez de 10 minutes. |
| `quantitative-probleme.mp3` | Problèmes quantitatifs et formels, ce sous-test comprend 18 exercices, vous disposez de 45 minutes. |
| `figuren-einpraegen.mp3` | Mémorisation de figures (phase d'apprentissage), vous disposez de 4 minutes. |
| `fakten-einpraegen.mp3` | Mémorisation de faits (phase d'apprentissage), vous disposez de 6 minutes. |
| `textverstaendnis.mp3` | Compréhension de textes, ce sous-test comprend 18 exercices, vous disposez de 45 minutes. |
| `figuren-reproduktion.mp3` | Mémorisation de figures (reproduction), ce sous-test comprend 18 exercices, vous disposez de 5 minutes. |
| `fakten-reproduktion.mp3` | Mémorisation de faits (reproduction), ce sous-test comprend 18 exercices, vous disposez de 6 minutes. |
| `diagramme-tabellen.mp3` | Diagrammes et tableaux, ce sous-test comprend 18 exercices, vous disposez de 45 minutes. |
| `konzentriertes-arbeiten.mp3` | Travail avec soin et concentration, vous disposez de 8 minutes. |
| `beginne.mp3` | Départ. |
| `stopp-weiter.mp3` | Stop. Passez maintenant au sous-test suivant. |
| `fertig-einzeln.mp3` | Stop. L'exercice est terminé. |
| `fertig-komplett.mp3` | Stop. La simulation est terminée. |

---

## Italiano  (`it/`)

_Aktuell keine Aufnahmen – die Sprachausgabe des Geräts liest vor._

| Datei | Gesprochener Text |
| --- | --- |
| `muster-zuordnen.mp3` | Abbinamento di schemi, questo sottotest comprende 18 esercizi, avete 16 minuti di tempo. |
| `med-nat-grundverstaendnis.mp3` | Comprensione medico-scientifica, questo sottotest comprende 18 esercizi, avete 45 minuti di tempo. |
| `objekte-im-raum.mp3` | Oggetti nello spazio, questo sottotest comprende 18 esercizi, avete 10 minuti di tempo. |
| `quantitative-probleme.mp3` | Problemi quantitativi e formali, questo sottotest comprende 18 esercizi, avete 45 minuti di tempo. |
| `figuren-einpraegen.mp3` | Memorizzazione di figure (fase di apprendimento), avete 4 minuti di tempo. |
| `fakten-einpraegen.mp3` | Memorizzazione di fatti (fase di apprendimento), avete 6 minuti di tempo. |
| `textverstaendnis.mp3` | Comprensione del testo, questo sottotest comprende 18 esercizi, avete 45 minuti di tempo. |
| `figuren-reproduktion.mp3` | Memorizzazione di figure (riproduzione), questo sottotest comprende 18 esercizi, avete 5 minuti di tempo. |
| `fakten-reproduktion.mp3` | Memorizzazione di fatti (riproduzione), questo sottotest comprende 18 esercizi, avete 6 minuti di tempo. |
| `diagramme-tabellen.mp3` | Diagrammi e tabelle, questo sottotest comprende 18 esercizi, avete 45 minuti di tempo. |
| `konzentriertes-arbeiten.mp3` | Lavoro concentrato e accurato, avete 8 minuti di tempo. |
| `beginne.mp3` | Via. |
| `stopp-weiter.mp3` | Stop. Passate ora al sottotest successivo. |
| `fertig-einzeln.mp3` | Stop. L'esercizio è terminato. |
| `fertig-komplett.mp3` | Stop. La simulazione è terminata. |
