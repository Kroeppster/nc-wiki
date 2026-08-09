# NCWiki

Kostenlose Vorbereitung auf den Eignungstest fürs Medizinstudium (EMS) – von
Studierenden für Studierende, schweizweit. Übungsmaterial, Testsimulationen und
Vorbereitungskurse, mehrsprachig (Deutsch, Français, Italiano).

🔗 Live: https://kroeppster.github.io/nc-wiki/

## Website pflegen (Texte ändern, News schreiben, PDFs hochladen)

Dafür gibt es eine eigene Anleitung, geschrieben für Leute ohne Programmierkenntnisse –
alles läuft über die normale GitHub-Weboberfläche, nichts muss installiert werden:

👉 **[docs/WARTUNG.md](docs/WARTUNG.md)**

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
