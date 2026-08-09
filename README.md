# NCWiki

Kostenlose Vorbereitung auf den Eignungstest fürs Medizinstudium (EMS) – von
Studierenden für Studierende, schweizweit. Übungsmaterial, Testsimulationen und
Vorbereitungskurse, mehrsprachig (Deutsch, Français, Italiano).

🔗 Live: https://kroeppster.github.io/nc-wiki/

## Website pflegen (Texte ändern, News schreiben, PDFs hochladen)

Dafür gibt es eine eigene Anleitung, geschrieben für Leute ohne Programmierkenntnisse –
alles läuft über die normale GitHub-Weboberfläche, nichts muss installiert werden:

👉 **[docs/WARTUNG.md](docs/WARTUNG.md)**

## Inhalte gegenlesen (6-Augen-Prinzip)

Vor dem Livegang soll jede Seite von 3 Personen kontrolliert werden. Wer
Zeit hat, trägt sich einfach in die Tabelle ein:

👉 **[docs/INHALTS-REVIEW.md](docs/INHALTS-REVIEW.md)**

## Technisch

Statische Website, gebaut mit [Hugo](https://gohugo.io/) und
[Pagefind](https://pagefind.app/) (Suchfunktion), automatisch veröffentlicht auf
GitHub Pages via GitHub Actions bei jedem Merge auf `main` (siehe
`.github/workflows/hugo.yml`).

### Lokal starten

Voraussetzungen: [Hugo Extended](https://gohugo.io/installation/) (aktuell getestete
Version: `0.164.0`, siehe `.github/workflows/hugo.yml`) und [Node.js](https://nodejs.org/).

```bash
npm install
hugo server
```

Die Seite ist danach unter `http://localhost:1313/` erreichbar. Für einen kompletten
Produktions-Build inklusive Suchindex:

```bash
npm run build
```

Vorlagen für neue Inhaltstypen (News, Erfahrungsbericht, Jahresbericht) liegen unter
`archetypes/`; reine Copy-Paste-Vorlagen für den Browser unter `docs/vorlage-*.md`.

## Lizenz

Die **Übungsaufgaben** (Inhalte unter `content/*/ems/uebungsaufgaben/` sowie die
zugehörigen Aufgabenblätter unter `assets/downloads/uebungsaufgaben/`) stehen unter
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.de) –
Weitergabe mit Namensnennung erlaubt, keine kommerzielle Nutzung. Siehe auch
[`assets/downloads/uebungsaufgaben/README.md`](assets/downloads/uebungsaufgaben/README.md).

Für den Rest der Website (Code, Layouts, übrige Inhalte) gibt es aktuell keine
gesonderte Lizenz.
