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
| `data/*.yaml` | Tabellarische Daten statt Hardcoding: `subtests.yaml` (Untertest-Liste), `unis.yaml`, `faq.yaml`, `sponsors.yaml`, `downloads.yaml`, `antwortbogen.yaml` (Lösungen der Testsimulationen für «Antwortbogen auswerten», erzeugt von `scripts/antwortbogen-loesungen.py`, nie von Hand). |
| `i18n/de\|fr\|it.yaml` | Feste UI-Texte (Buttons, Menüs, Labels) — jede neue UI-Zeichenkette in allen drei Dateien ergänzen. |
| `layouts/` | Templates: `_default/baseof.html` (Grundgerüst), `partials/` (header, footer, head, Formulare, Grids), `_default/list.html` + `single.html` (generisch für alle Bereiche), `index.html` (Startseite). |
| `assets/css/style.css`, `static/css/style.css` | Design, unverändert aus der ursprünglichen HTML-Vorlage übernommen. |
| `archetypes/`, `docs/vorlage-*.md` | Copy-Paste-Vorlagen für neue Seiten (News, Erfahrungsbericht, Jahresbericht). |
| `docs/STYLEGUIDE.md` | Schreibregeln für alle Texte (Anrede, Ton, Titel, Begriffe, Schreibweisen). |
| `docs/WARTUNG.md`, `docs/WARTUNG-DETAILLIERT.md` (+ `.fr.md`, `.it.md`) | Kurzanleitung (nur Alltag: Mappe, Web-Editor, News, PDF, Bild, Löschen) bzw. ausführliche Anleitung (alles andere) — dreisprachig; bei Änderungen an Navigation, Design, Formularen etc. alle Sprachfassungen mitpflegen. |
| `.github/workflows/hugo.yml` | Build + interner Link-Check laufen bei jedem PR gegen `main` und bei Push; **Deploy läuft nur bei Push auf `main`**, nie bei PRs. |
| `.github/workflows/textmappen.yml` | Legt nach jedem Push auf `main` frische Textmappen und die Wortliste des Fakten-Generators an das GitHub-Release `textmappen` (bewusst nicht auf die Website). |
| `.pages.yml` | Web-Editor Pages CMS (app.pagescms.org). `settings.content.merge: true` nie entfernen (sonst verschwinden Menü & Co. beim Speichern). Nach Änderungen `node scripts/editor-rundlauf.mjs` (baut alles nach einem simulierten Speichern jeder Seite und vergleicht). Siehe `docs/WARTUNG-DETAILLIERT.md` 4. |
| `redaktion/`, `.github/workflows/texte-einlesen.yml` | Textmappen (Excel, eine je Sprache, `scripts/texte-*.py`): hochgeladen in `redaktion/` → Workflow liest ein und eröffnet einen PR. `redaktion/stand.json` = Stand/Bemerkungen, vom Workflow gepflegt. Ansicht-Blätter für Startseite, Team, Uniguide und Q&A (`texte_ansicht.py`, `texte_uniguide.py` → `data/unis.yaml` + `data/uniguide-spalten.yaml`, `texte_faq.py` → `data/faq.yaml`, `texte_zeitstrahl.py` → Zeitstrahl-Tabelle der Startseite). Siehe `docs/WARTUNG-DETAILLIERT.md` 3; nach Änderungen an den Skripten `scripts/texte-mappe-pruefen.py`. |
| `scripts/wortliste.py`, `.github/workflows/wortliste-einlesen.yml` | Wortliste des Fakten-Generators (`data/fakten-generator/de.yaml`) als **eigene** Excel `ncwiki-wortliste-fakten-generator.xlsx` (nicht Teil der Textmappen): erzeugen/einlesen mit Prüfung (Mindestmengen, Duplikate), hochgeladen in `redaktion/` → Workflow prüft, liest ein, eröffnet einen PR (bei Fehlern kein PR, Lauf rot). Ersetzt nur die Wortlisten-Blöcke, der Erklärkommentar bleibt. Siehe `docs/WARTUNG-DETAILLIERT.md` 11; nach Änderungen `scripts/wortliste-pruefen.py`. |

## Konventionen

- Referenz-Design für neue Seiten/Komponenten: **ncwiki-new.ch** (Navigation, Team-Seite,
  Übungsaufgaben-Layout, Flip-Clock-Countdown wurden explizit danach nachgebaut).
- Texte schreiben wir nach `docs/STYLEGUIDE.md` (du-Anrede, Begriffe wie «Uniguide», «Häufige Fragen»,
  «Übungsserien», EMS statt NC, Genderstern, «Guillemets», Datum «9. Juli 2027»).
- Neue sichtbare Texte immer dreisprachig anlegen (`content/de|fr|it/...` bzw.
  `i18n/de|fr|it.yaml`) — nie nur Deutsch.
- Harte Links vermeiden, stattdessen Hugo-Funktionen: `relLangURL`, `.Site.Menus`,
  `.Parent` (für Zurück-Links zur Übersichtsseite). Im Seitentext interne Links als
  normale Markdown-Links schreiben (`[Uniguide](/ems/uniguide)`) – der Render-Hook
  `layouts/_default/_markup/render-link.html` macht daraus die Adresse in der richtigen
  Sprache und bricht den Build bei toten Links ab. **Kein `{{< ref >}}` und keine
  Shortcodes im Inhalt**: Der Web-Editor (Pages CMS) zerstört sie beim Speichern.
  Eingebettete Bausteine stattdessen als Code-Block ```` ```baustein ```` (siehe
  `render-codeblock-baustein.html`).
- Übungsaufgaben-Inhalte (`content/*/ems/uebungsaufgaben/` und zugehörige PDFs unter
  `assets/downloads/uebungsaufgaben/`) stehen unter CC BY-NC 4.0 — Lizenzhinweis nicht
  entfernen.
- Commit-Identität: Es ist bewusst keine globale Git-Identität gesetzt. Nach einem
  frischen Clone einmalig `git config --local user.name "..."` und
  `git config --local user.email "..."` setzen — danach genügen normale `git commit`
  ohne `-c`-Flags. `.git/config` ist nicht versioniert, die Angaben landen also nicht
  im Repo.
- Nach jedem Push den GitHub-Actions-Run per API prüfen (`.../actions/runs?per_page=1`),
  bis `conclusion: success`, bevor die Aufgabe als erledigt gilt.
