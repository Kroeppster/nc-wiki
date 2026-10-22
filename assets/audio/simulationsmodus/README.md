# Ansagen für den Simulationsmodus

Der Simulationsmodus (Abschnitt auf `/ems/testsimulationen/`) sagt an, was als Nächstes
kommt, sagt «Start» und am Ende «Stopp». **Liegt hier eine passende Datei, wird sie
abgespielt** – sonst liest die Sprachausgabe des Geräts denselben Text vor.

Es muss nichts eingetragen werden: Datei mit dem richtigen Namen in den richtigen
Sprachordner legen, fertig. Fehlt eine einzelne Datei, wird nur dieser Satz vorgelesen.

## Was gerade da ist

Alle drei Sprachen, je 31 Dateien, erzeugt im Oktober 2026 mit **Google AI Studio**
(Modell «Gemini 3.8 Flash TTS», Stimme «Cruz») und dieser Stilanweisung:

> A calm, composed exam supervisor in a large lecture hall. Adult voice, around 35 to 45
> years old, mid-range pitch. Neutral and matter-of-fact, clear articulation, steady and
> rather slow pace. Friendly but not chatty, no theatrical emphasis, no excitement. Speaks
> German, French and Italian natively, each without a foreign accent. Sounds like a reliable
> official reading instructions aloud to a room full of test takers.

Dazu für die 30 kurzen Ansagen «After each line, pause for two full seconds of silence
before the next line.», für die Instruktion «Read slowly, with short pauses between
sentences and about three seconds of silence after each paragraph.»

Echte Aufnahmen aus dem Verein gehen genauso: Datei mit gleichem Namen überschreiben.

## Wann welche Datei läuft

- `<untertest>.mp3` – Ansage mit den echten Zahlen (ganze Simulation, einzelner Untertest,
  eigener Ablauf mit unveränderten Werten).
- `<untertest>-kurz.mp3` – nur der Name: im eigenen Ablauf, wenn Zeit oder Aufgabenzahl
  geändert wurden. Die Zahlen stehen dann nur auf dem Bildschirm.
- `beginne`, `stopp-weiter`, `fertig-einzeln`, `fertig-komplett`, `pause`, `pause-vorbei`.
- Nur in der ganzen Simulation: `einleitung` (zu Beginn), `teil-b` (vor Textverständnis).
- `konz-instruktion` – vor dem Konzentrationstest (ganze Simulation und einzeln).

Die Texte stehen in `i18n/*.yaml` (Präfix `pm_`). Ändert sich dort ein Satz, muss die
passende Aufnahme neu – sonst sagt die Stimme etwas anderes als der Bildschirm.

## Neu aufnehmen

1. In AI Studio pro Sprache **eine** Aufnahme mit allen 30 Sätzen aus der Tabelle unten,
   in dieser Reihenfolge, ein Satz pro Zeile (Stilanweisung oben). Die Instruktion separat.
2. Schneiden, Lautstärke angleichen, MP3 erzeugen:

   ```
   python3 scripts/ansagen-schneiden.py ansagen-de.wav de assets/audio/simulationsmodus/de
   python3 scripts/ansagen-schneiden.py konz-instruktion-de.wav de assets/audio/simulationsmodus/de --instruktion
   ```

   Das Skript liest die Sätze aus der Tabelle hier, findet die Grenzen auch bei kurzen
   Pausen (über die erwartete Länge jedes Satzes) und prüft, dass jede Kurzansage wie der
   Anfang der passenden langen Ansage klingt. Bei der Instruktion verlängert es die Pause
   nach dem Satz zum Beispiel auf 10 Sekunden.

## Format

- **MP3**, mono, 96 kbit/s, Lautheit etwa −18 LUFS
- vorne und hinten je eine halbe Sekunde Stille

---

## Deutsch (`de/`)

| Datei | Gesprochener Text |
| --- | --- |
| `muster-zuordnen.mp3` | Muster zuordnen. 18 Aufgaben, Sie haben 16 Minuten Zeit. |
| `med-nat-grundverstaendnis.mp3` | Medizinisch-naturwissenschaftliches Grundverständnis. 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `objekte-im-raum.mp3` | Objekte im Raum. 18 Aufgaben, Sie haben 10 Minuten Zeit. |
| `quantitative-probleme.mp3` | Quantitative und formale Probleme. 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `figuren-einpraegen.mp3` | Figuren lernen, Einprägephase. Legen Sie den Stift weg, Notizen sind nicht erlaubt. Sie haben 4 Minuten Zeit. |
| `fakten-einpraegen.mp3` | Fakten lernen, Einprägephase. Sie haben 6 Minuten Zeit. |
| `textverstaendnis.mp3` | Textverständnis. 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `figuren-reproduktion.mp3` | Figuren lernen, Reproduktionsphase. 18 Aufgaben, Sie haben 5 Minuten Zeit. |
| `fakten-reproduktion.mp3` | Fakten lernen, Reproduktionsphase. 18 Aufgaben, Sie haben 6 Minuten Zeit. |
| `diagramme-tabellen.mp3` | Diagramme und Tabellen. 18 Aufgaben, Sie haben 45 Minuten Zeit. |
| `konzentriertes-arbeiten.mp3` | Konzentriertes und sorgfältiges Arbeiten. Nehmen Sie einen dicken schwarzen oder blauen Fineliner und beginnen Sie in Zeile 1. Sie haben 8 Minuten Zeit. |
| `beginne.mp3` | Start. |
| `stopp-weiter.mp3` | Stopp. Blättern Sie zum nächsten Untertest. |
| `fertig-einzeln.mp3` | Stopp. Legen Sie den Stift weg. Die Übung ist beendet. |
| `fertig-komplett.mp3` | Stopp. Legen Sie den Stift weg. Die Simulation ist beendet. |
| `muster-zuordnen-kurz.mp3` | Muster zuordnen. |
| `med-nat-grundverstaendnis-kurz.mp3` | Medizinisch-naturwissenschaftliches Grundverständnis. |
| `objekte-im-raum-kurz.mp3` | Objekte im Raum. |
| `quantitative-probleme-kurz.mp3` | Quantitative und formale Probleme. |
| `figuren-einpraegen-kurz.mp3` | Figuren lernen, Einprägephase. Notizen sind nicht erlaubt. |
| `fakten-einpraegen-kurz.mp3` | Fakten lernen, Einprägephase. |
| `textverstaendnis-kurz.mp3` | Textverständnis. |
| `figuren-reproduktion-kurz.mp3` | Figuren lernen, Reproduktionsphase. |
| `fakten-reproduktion-kurz.mp3` | Fakten lernen, Reproduktionsphase. |
| `diagramme-tabellen-kurz.mp3` | Diagramme und Tabellen. |
| `konzentriertes-arbeiten-kurz.mp3` | Konzentriertes und sorgfältiges Arbeiten. Beginnen Sie in Zeile 1. |
| `pause.mp3` | Pause. |
| `pause-vorbei.mp3` | Die Pause ist vorbei. |
| `einleitung.mp3` | Willkommen zur Testsimulation. Bearbeiten Sie nur den angesagten Untertest und markieren Sie Ihre Antworten auf dem Antwortbogen. Beginnen Sie erst bei «Start» und legen Sie den Stift bei «Stopp» sofort weg. Viel Erfolg. |
| `teil-b.mp3` | Ende von Teil A. Legen Sie Teil A weg und bearbeiten Sie ihn nicht mehr. Es folgt Teil B. |
| `konz-instruktion.mp3` | Instruktion zum Konzentrationstest, Wortlaut: `pm_konz_instruktion_ansage` in `i18n/de.yaml` (mit 10 s Pause nach dem Satz zum Beispiel) |

---

## Français (`fr/`)

| Datei | Gesprochener Text |
| --- | --- |
| `muster-zuordnen.mp3` | Association de motifs. 18 exercices, vous disposez de 16 minutes. |
| `med-nat-grundverstaendnis.mp3` | Compréhension médico-scientifique. 18 exercices, vous disposez de 45 minutes. |
| `objekte-im-raum.mp3` | Objets dans l'espace. 18 exercices, vous disposez de 10 minutes. |
| `quantitative-probleme.mp3` | Problèmes quantitatifs et formels. 18 exercices, vous disposez de 45 minutes. |
| `figuren-einpraegen.mp3` | Mémorisation de figures, phase d'apprentissage. Posez votre crayon, les notes ne sont pas autorisées. Vous disposez de 4 minutes. |
| `fakten-einpraegen.mp3` | Mémorisation de faits, phase d'apprentissage. Vous disposez de 6 minutes. |
| `textverstaendnis.mp3` | Compréhension de texte. 18 exercices, vous disposez de 45 minutes. |
| `figuren-reproduktion.mp3` | Mémorisation de figures, phase de reproduction. 18 exercices, vous disposez de 5 minutes. |
| `fakten-reproduktion.mp3` | Mémorisation de faits, phase de reproduction. 18 exercices, vous disposez de 6 minutes. |
| `diagramme-tabellen.mp3` | Diagrammes et tableaux. 18 exercices, vous disposez de 45 minutes. |
| `konzentriertes-arbeiten.mp3` | Travail concentré et soigné. Prenez un feutre épais noir ou bleu et commencez à la ligne 1. Vous disposez de 8 minutes. |
| `beginne.mp3` | Départ. |
| `stopp-weiter.mp3` | Stop. Passez au sous-test suivant. |
| `fertig-einzeln.mp3` | Stop. Posez votre crayon. L'exercice est terminé. |
| `fertig-komplett.mp3` | Stop. Posez votre crayon. La simulation est terminée. |
| `muster-zuordnen-kurz.mp3` | Association de motifs. |
| `med-nat-grundverstaendnis-kurz.mp3` | Compréhension médico-scientifique. |
| `objekte-im-raum-kurz.mp3` | Objets dans l'espace. |
| `quantitative-probleme-kurz.mp3` | Problèmes quantitatifs et formels. |
| `figuren-einpraegen-kurz.mp3` | Mémorisation de figures, phase d'apprentissage. Les notes ne sont pas autorisées. |
| `fakten-einpraegen-kurz.mp3` | Mémorisation de faits, phase d'apprentissage. |
| `textverstaendnis-kurz.mp3` | Compréhension de texte. |
| `figuren-reproduktion-kurz.mp3` | Mémorisation de figures, phase de reproduction. |
| `fakten-reproduktion-kurz.mp3` | Mémorisation de faits, phase de reproduction. |
| `diagramme-tabellen-kurz.mp3` | Diagrammes et tableaux. |
| `konzentriertes-arbeiten-kurz.mp3` | Travail concentré et soigné. Commencez à la ligne 1. |
| `pause.mp3` | Pause. |
| `pause-vorbei.mp3` | La pause est terminée. |
| `einleitung.mp3` | Bienvenue à la simulation de test. Ne traitez que le sous-test annoncé et reportez vos réponses sur la feuille de réponses. Ne commencez qu'au signal « Départ » et posez immédiatement votre crayon au signal « Stop ». Bonne chance. |
| `teil-b.mp3` | Fin de la partie A. Mettez la partie A de côté et ne la traitez plus. Voici la partie B. |
| `konz-instruktion.mp3` | Instruktion zum Konzentrationstest, Wortlaut: `pm_konz_instruktion_ansage` in `i18n/fr.yaml` (mit 10 s Pause nach dem Satz zum Beispiel) |

---

## Italiano (`it/`)

| Datei | Gesprochener Text |
| --- | --- |
| `muster-zuordnen.mp3` | Abbinamento di schemi. 18 esercizi, avete 16 minuti. |
| `med-nat-grundverstaendnis.mp3` | Comprensione medico-scientifica. 18 esercizi, avete 45 minuti. |
| `objekte-im-raum.mp3` | Oggetti nello spazio. 18 esercizi, avete 10 minuti. |
| `quantitative-probleme.mp3` | Problemi quantitativi e formali. 18 esercizi, avete 45 minuti. |
| `figuren-einpraegen.mp3` | Memorizzazione di figure, fase di apprendimento. Mettete via la matita, non è consentito prendere appunti. Avete 4 minuti. |
| `fakten-einpraegen.mp3` | Memorizzazione di fatti, fase di apprendimento. Avete 6 minuti. |
| `textverstaendnis.mp3` | Comprensione del testo. 18 esercizi, avete 45 minuti. |
| `figuren-reproduktion.mp3` | Memorizzazione di figure, fase di riproduzione. 18 esercizi, avete 5 minuti. |
| `fakten-reproduktion.mp3` | Memorizzazione di fatti, fase di riproduzione. 18 esercizi, avete 6 minuti. |
| `diagramme-tabellen.mp3` | Diagrammi e tabelle. 18 esercizi, avete 45 minuti. |
| `konzentriertes-arbeiten.mp3` | Lavoro concentrato e accurato. Usate un fineliner spesso nero o blu e iniziate dalla riga 1. Avete 8 minuti. |
| `beginne.mp3` | Via. |
| `stopp-weiter.mp3` | Stop. Passate al sottotest successivo. |
| `fertig-einzeln.mp3` | Stop. Posate la penna. L'esercizio è terminato. |
| `fertig-komplett.mp3` | Stop. Posate la penna. La simulazione è terminata. |
| `muster-zuordnen-kurz.mp3` | Abbinamento di schemi. |
| `med-nat-grundverstaendnis-kurz.mp3` | Comprensione medico-scientifica. |
| `objekte-im-raum-kurz.mp3` | Oggetti nello spazio. |
| `quantitative-probleme-kurz.mp3` | Problemi quantitativi e formali. |
| `figuren-einpraegen-kurz.mp3` | Memorizzazione di figure, fase di apprendimento. Non è consentito prendere appunti. |
| `fakten-einpraegen-kurz.mp3` | Memorizzazione di fatti, fase di apprendimento. |
| `textverstaendnis-kurz.mp3` | Comprensione del testo. |
| `figuren-reproduktion-kurz.mp3` | Memorizzazione di figure, fase di riproduzione. |
| `fakten-reproduktion-kurz.mp3` | Memorizzazione di fatti, fase di riproduzione. |
| `diagramme-tabellen-kurz.mp3` | Diagrammi e tabelle. |
| `konzentriertes-arbeiten-kurz.mp3` | Lavoro concentrato e accurato. Iniziate dalla riga 1. |
| `pause.mp3` | Pausa. |
| `pause-vorbei.mp3` | La pausa è finita. |
| `einleitung.mp3` | Benvenuti alla simulazione del test. Lavorate solo sul sottotest annunciato e segnate le risposte sul foglio delle risposte. Iniziate solo al segnale «Via» e posate subito la matita al segnale «Stop». In bocca al lupo. |
| `teil-b.mp3` | Fine della parte A. Mettete da parte la parte A e non lavorateci più. Segue la parte B. |
| `konz-instruktion.mp3` | Instruktion zum Konzentrationstest, Wortlaut: `pm_konz_instruktion_ansage` in `i18n/it.yaml` (mit 10 s Pause nach dem Satz zum Beispiel) |
