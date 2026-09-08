# Aufnahmen für den Prüfungsmodus

Der Prüfungsmodus (`/ems/pruefungsmodus/`) liest die Anweisungen standardmässig
mit der Sprachausgabe des Geräts vor. Das funktioniert überall und sofort,
klingt aber maschinell.

**Wird hier eine Datei abgelegt, wird stattdessen sie abgespielt.** Es muss
nichts umgestellt oder eingetragen werden – Datei mit dem richtigen Namen in den
richtigen Sprachordner legen, fertig. Genau wie bei den PDF-Downloads.

Die Sammlung muss nicht auf einmal vollständig sein: Für jeden Satz, zu dem eine
Aufnahme fehlt, wird weiterhin vorgelesen. Man kann also mit den vier kurzen
Ansagen anfangen (`beginne`, `stopp`, `fertig-einzeln`, `fertig-komplett`) – die
hört man bei jeder einzelnen Übung, sie lohnen sich zuerst.

## Format

- **MP3**, Dateiendung `.mp3` (andere Endungen werden nicht gefunden)
- Mono reicht, 128 kbit/s reicht
- Vorne und hinten je etwa eine halbe Sekunde Stille – sonst klingt der Einsatz
  abgehackt
- Ruhig und eher langsam sprechen. Das hier ersetzt eine Aufsichtsperson im
  Testsaal, keine Werbung.

## Dateiname = was gesprochen wird

Unten steht pro Sprache, welche Datei welchen Satz enthalten soll. Die Texte
sind exakt die, die sonst vorgelesen würden – wer möchte, darf beim Einsprechen
natürlicher formulieren, solange die Aussage dieselbe bleibt.

Ändert sich später ein Text in `i18n/*.yaml` oder in `data/testablauf.yaml`,
passt die zugehörige Aufnahme nicht mehr dazu. Dann entweder neu aufnehmen oder
die Datei löschen – ohne Datei wird wieder der aktuelle Text vorgelesen.


---

## Deutsch  (`de/`)

| Datei | Gesprochener Text |
| --- | --- |
| `beginne.mp3` | Beginne jetzt. |
| `stopp.mp3` | Stopp. Leg den Stift weg. |
| `fertig-einzeln.mp3` | Geschafft. |
| `fertig-komplett.mp3` | Simulation beendet. Alle elf Blöcke geschafft. |
| `muster-zuordnen.mp3` | Muster zuordnen. Du hast dafür 16 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `med-nat-grundverstaendnis.mp3` | Medizinisch-naturwissenschaftliches Grundverständnis. Du hast dafür 45 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `objekte-im-raum.mp3` | Objekte im Raum. Du hast dafür 10 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `quantitative-probleme.mp3` | Quantitative und formale Probleme. Du hast dafür 45 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `figuren-einpraegen.mp3` | Figuren einprägen (Einprägephase). Du hast dafür 4 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. Nach dieser Phase folgt zuerst ein anderer Untertest. Erst danach wird abgefragt, was du dir gemerkt hast. |
| `fakten-einpraegen.mp3` | Fakten einprägen (Einprägephase). Du hast dafür 6 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. Auch hier folgt zuerst ein anderer Untertest, bevor abgefragt wird. |
| `textverstaendnis.mp3` | Textverständnis. Du hast dafür 45 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `figuren-reproduktion.mp3` | Figuren einprägen (Reproduktion). Du hast dafür 5 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `fakten-reproduktion.mp3` | Fakten einprägen (Reproduktion). Du hast dafür 6 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `diagramme-tabellen.mp3` | Diagramme und Tabellen. Du hast dafür 45 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. |
| `konzentriertes-arbeiten.mp3` | Konzentriertes und sorgfältiges Arbeiten. Du hast dafür 8 Minuten. Leg dir Aufgabenblatt und Antwortbogen bereit. Zurückblättern zu früheren Untertests ist nicht erlaubt. Die Streichbedingung steht auf deinem Blatt. Präge sie dir jetzt genau ein. Während der acht Minuten solltest du nicht mehr nachschlagen müssen. |

---

## Français  (`fr/`)

| Datei | Gesprochener Text |
| --- | --- |
| `beginne.mp3` | Commence maintenant. |
| `stopp.mp3` | Stop. Pose ton stylo. |
| `fertig-einzeln.mp3` | Terminé. |
| `fertig-komplett.mp3` | Simulation terminée. Les onze blocs sont faits. |
| `muster-zuordnen.mp3` | Association de motifs. Tu disposes de 16 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `med-nat-grundverstaendnis.mp3` | Compréhension médico-scientifique. Tu disposes de 45 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `objekte-im-raum.mp3` | Objets dans l'espace. Tu disposes de 10 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `quantitative-probleme.mp3` | Problèmes quantitatifs et formels. Tu disposes de 45 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `figuren-einpraegen.mp3` | Mémorisation de figures (phase d'apprentissage). Tu disposes de 4 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. Après cette phase vient d'abord un autre sous-test. Ce n'est qu'ensuite que l'on te demandera ce que tu as retenu. |
| `fakten-einpraegen.mp3` | Mémorisation de faits (phase d'apprentissage). Tu disposes de 6 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. Ici aussi, un autre sous-test suit avant que l'on ne te pose des questions. |
| `textverstaendnis.mp3` | Compréhension de textes. Tu disposes de 45 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `figuren-reproduktion.mp3` | Mémorisation de figures (reproduction). Tu disposes de 5 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `fakten-reproduktion.mp3` | Mémorisation de faits (reproduction). Tu disposes de 6 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `diagramme-tabellen.mp3` | Diagrammes et tableaux. Tu disposes de 45 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. |
| `konzentriertes-arbeiten.mp3` | Travail avec soin et concentration. Tu disposes de 8 minutes. Prépare la feuille d'exercices et la feuille de réponses. Il est interdit de revenir aux sous-tests précédents. La condition de biffage figure sur ta feuille. Mémorise-la maintenant avec précision. Pendant les huit minutes, tu ne devrais plus avoir à la relire. |

---

## Italiano  (`it/`)

| Datei | Gesprochener Text |
| --- | --- |
| `beginne.mp3` | Inizia adesso. |
| `stopp.mp3` | Stop. Posa la penna. |
| `fertig-einzeln.mp3` | Fatto. |
| `fertig-komplett.mp3` | Simulazione conclusa. Tutti e undici i blocchi sono fatti. |
| `muster-zuordnen.mp3` | Abbinamento di schemi. Hai 16 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `med-nat-grundverstaendnis.mp3` | Comprensione medico-scientifica. Hai 45 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `objekte-im-raum.mp3` | Oggetti nello spazio. Hai 10 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `quantitative-probleme.mp3` | Problemi quantitativi e formali. Hai 45 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `figuren-einpraegen.mp3` | Memorizzazione di figure (fase di apprendimento). Hai 4 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. Dopo questa fase segue prima un altro sottotest. Solo in seguito ti verrà chiesto che cosa hai memorizzato. |
| `fakten-einpraegen.mp3` | Memorizzazione di fatti (fase di apprendimento). Hai 6 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. Anche qui segue prima un altro sottotest, prima delle domande. |
| `textverstaendnis.mp3` | Comprensione del testo. Hai 45 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `figuren-reproduktion.mp3` | Memorizzazione di figure (riproduzione). Hai 5 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `fakten-reproduktion.mp3` | Memorizzazione di fatti (riproduzione). Hai 6 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `diagramme-tabellen.mp3` | Diagrammi e tabelle. Hai 45 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. |
| `konzentriertes-arbeiten.mp3` | Lavoro concentrato e accurato. Hai 8 minuti. Prepara il foglio degli esercizi e quello delle risposte. Non è permesso tornare ai sottotest precedenti. La condizione di cancellatura è sul tuo foglio. Memorizzala ora con precisione. Durante gli otto minuti non dovresti più doverla rileggere. |

---

Insgesamt sind das **15 Aufnahmen pro Sprache**. Am meisten bringt die deutsche
Fassung: Die vier kurzen Ansagen hört man bei jeder Übung, die elf Anweisungen
je einmal pro Block.
