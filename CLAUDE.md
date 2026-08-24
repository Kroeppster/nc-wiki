# NCWiki

Mehrsprachige Hugo-Website (statisch) für einen Schweizer Studierendenverein, der
kostenlose EMS-Vorbereitung (Eignungstest Medizinstudium) anbietet. Deutsch ist die
Standardsprache ohne URL-Präfix, Französisch liegt unter `/fr/`, Italienisch unter `/it/`.
Deploy auf GitHub Pages via GitHub Actions bei jedem Push auf `main`.

Live: https://kroeppster.github.io/nc-wiki/
Repo: `Kroeppster/nc-wiki`

## Befehle

```bash
npm install          # einmalig
hugo server -D       # lokaler Dev-Server, http://localhost:1313/
npm run build        # Produktions-Build: hugo --minify && pagefind-Suchindex
```

Hugo Extended wird gebraucht (Version siehe `.github/workflows/hugo.yml`), auf Windows via
`winget install Hugo.Hugo.Extended`.

Vor einem Commit immer lokal mit `hugo --minify` bzw. `hugo server -D` prüfen, dass der
Build fehlerfrei durchläuft — der CI-Workflow prüft zusätzlich interne Links und schlägt
sonst fehl.

## Struktur

| Ordner | Inhalt |
| --- | --- |
| `content/de\|fr\|it/` | Seiteninhalte, parallele Struktur pro Sprache. `_index.md` = Übersichtsseite eines Ordners, alle anderen `.md` = Einzelseiten. |
| `data/*.yaml` | Tabellarische Daten statt Hardcoding: `subtests.yaml` (Untertest-Liste), `unis.yaml`, `faq.yaml`, `sponsors.yaml`, `downloads.yaml`. |
| `i18n/de\|fr\|it.yaml` | Feste UI-Texte (Buttons, Menüs, Labels) — jede neue UI-Zeichenkette in allen drei Dateien ergänzen. |
| `layouts/` | Templates: `_default/baseof.html` (Grundgerüst), `partials/` (header, footer, head, Formulare, Grids), `_default/list.html` + `single.html` (generisch für alle Bereiche), `index.html` (Startseite). |
| `assets/css/style.css`, `static/css/style.css` | Design, unverändert aus der ursprünglichen HTML-Vorlage übernommen. |
| `archetypes/`, `docs/vorlage-*.md` | Copy-Paste-Vorlagen für neue Seiten (News, Erfahrungsbericht, Jahresbericht). |
| `docs/WARTUNG.md`, `docs/WARTUNG-DETAILLIERT.md` | Redaktions-Anleitung für Nicht-Entwickler:innen (Kurz- bzw. Langfassung) — bei Änderungen an Navigation, Design, Formularen etc. mitpflegen. |
| `.github/workflows/hugo.yml` | Build + interner Link-Check laufen bei jedem PR gegen `main` und bei Push; **Deploy läuft nur bei Push auf `main`**, nie bei PRs. |

## Konventionen

- Referenz-Design für neue Seiten/Komponenten: **ncwiki-new.ch** (Navigation, Team-Seite,
  Übungsaufgaben-Layout, Flip-Clock-Countdown wurden explizit danach nachgebaut).
- Neue sichtbare Texte immer dreisprachig anlegen (`content/de|fr|it/...` bzw.
  `i18n/de|fr|it.yaml`) — nie nur Deutsch.
- Harte Links vermeiden, stattdessen Hugo-Funktionen: `relLangURL`, `.Site.Menus`,
  `.Parent` (für Zurück-Links zur Übersichtsseite), `{{< ref >}}`.
- Übungsaufgaben-Inhalte (`content/*/ems/uebungsaufgaben/` und zugehörige PDFs unter
  `assets/downloads/uebungsaufgaben/`) stehen unter CC BY-NC 4.0 — Lizenzhinweis nicht
  entfernen.
- Commits: `git -c user.name="Kroeppster" -c user.email="kronmustafa@gmail.com" commit ...`
- Nach jedem Push den GitHub-Actions-Run per API prüfen (`.../actions/runs?per_page=1`),
  bis `conclusion: success`, bevor die Aufgabe als erledigt gilt.
