#!/usr/bin/env node
/*
================================================================================
WEB-EDITOR-RUNDLAUF: Laesst Pages CMS die Website heil?
================================================================================
    node scripts/editor-rundlauf.mjs              # pruefen
    node scripts/editor-rundlauf.mjs --behalten   # Arbeitsordner behalten

Speichert JEDE Seite, die der Web-Editor (Pages CMS, .pages.yml) erreicht, so
wie Pages CMS es taete - in einer Kopie des Projekts -, baut danach beide
Fassungen mit Hugo und vergleicht Seite fuer Seite. Nach jeder Aenderung an
.pages.yml oder an der Art, wie Seiten geschrieben sind, laufen lassen.

Nachgestellt wird, was Pages CMS beim Speichern macht (nachgelesen im
Quellcode, github.com/pagescms/pages-cms, MIT-Lizenz; die Stellen stehen bei
den Funktionen unten):
  - Seitenkopf mit der Bibliothek "yaml" lesen, nur die konfigurierten Felder
    bearbeiten, mit dem alten Kopf zusammenfuehren (settings.content.merge),
    leere Felder weglassen und den ganzen Kopf neu schreiben.
  - Den Seitentext durch den Editor (TipTap mit Markdown) laden und wieder
    speichern - so, als haette jemand ein Komma geaendert. Dabei wird die
    GANZE Seite neu geschrieben.
Eine Datei, die von zwei Listen aus erreichbar ist (z. B. ein Bericht im
Seitenbaum und unter "Erfahrungsberichte"), wird von beiden aus gespeichert.

EINMALIG VORBEREITEN - die Pakete gehoeren nicht zur Website und kommen
deshalb in einen eigenen Ordner, package.json bleibt, wie es ist:
    mkdir -p ~/ncwiki-editor-test && cd ~/ncwiki-editor-test && npm init -y
    npm install yaml lodash.mergewith jsdom @tiptap/core @tiptap/pm \
      @tiptap/starter-kit @tiptap/markdown @tiptap/extension-underline \
      @tiptap/extension-link @tiptap/extension-image @tiptap/extension-table \
      @tiptap/extension-table-row @tiptap/extension-table-header \
      @tiptap/extension-table-cell
Einen anderen Ordner nennt --pakete ORDNER oder NCWIKI_EDITOR_PAKETE.
Hugo: aus dem PATH, ~/bin/hugo oder der Umgebungsvariable HUGO.
================================================================================
*/
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';

const PROJEKT = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const args = process.argv.slice(2);
const behalten = args.includes('--behalten');
const paketeArg = args.includes('--pakete') ? args[args.indexOf('--pakete') + 1] : null;

// --- Pakete finden ----------------------------------------------------------
function paketeLaden() {
  const orte = [paketeArg, process.env.NCWIKI_EDITOR_PAKETE, PROJEKT,
    path.join(os.homedir(), 'ncwiki-editor-test')].filter(Boolean);
  for (const ort of orte) {
    const req = createRequire(path.join(path.resolve(ort), 'x.js'));
    try { req.resolve('@tiptap/markdown'); req.resolve('yaml'); return req; } catch { /* weiter */ }
  }
  console.error('Pakete fehlen. Einmalig vorbereiten - siehe Kopf dieses Skripts (npm install ... in ~/ncwiki-editor-test).');
  process.exit(2);
}
const req = paketeLaden();
const YAML = req('yaml');
const mergeWith = req('lodash.mergewith');

// TipTap braucht ein DOM - jsdom stellt eins bereit, BEVOR TipTap geladen wird.
const { JSDOM } = req('jsdom');
const dom = new JSDOM('<!doctype html><html><body></body></html>');
for (const k of ['window', 'document', 'Node', 'HTMLElement', 'Element', 'DOMParser', 'MutationObserver', 'getComputedStyle']) {
  const v = k === 'window' ? dom.window : (k === 'getComputedStyle' ? dom.window.getComputedStyle.bind(dom.window) : dom.window[k]);
  Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
}
const { Editor } = req('@tiptap/core');
const StarterKit = req('@tiptap/starter-kit').default ?? req('@tiptap/starter-kit');
const Underline = req('@tiptap/extension-underline').default;
const Link = req('@tiptap/extension-link').default;
const Image = req('@tiptap/extension-image').default;
const { Table } = req('@tiptap/extension-table');
const TableRow = req('@tiptap/extension-table-row').default;
const TableHeader = req('@tiptap/extension-table-header').default;
const TableCell = req('@tiptap/extension-table-cell').default;
const { Markdown } = req('@tiptap/markdown');

// Der Editor von Pages CMS (components/ui/editor/index.tsx): dieselben
// Erweiterungen, gleich eingestellt; Platzhalter und Slash-Befehle aendern am
// Markdown nichts und fehlen hier. Beim Speichern richtet Pages CMS
// ausserdem Tabellenzeilen neu aus (normalizeMarkdownTables).
function editorRundlauf(markdown) {
  const e = new Editor({
    element: document.createElement('div'),
    extensions: [
      StarterKit.configure({ link: false, underline: false }),
      Underline,
      Link.configure({ openOnClick: false, enableClickSelection: true, HTMLAttributes: { rel: null, target: null } }),
      Image, Table, TableRow, TableHeader, TableCell, Markdown,
    ],
    content: markdown, contentType: 'markdown',
  });
  const raus = tabellenAusrichten(e.getMarkdown());
  e.destroy();
  return raus;
}
function tabellenAusrichten(md) {
  const zeile = /^\s*\|.*\|\s*$/, trenner = /^:?-{3,}:?$/, nbsp = /^(?:&nbsp;|\u00A0)+$/i;
  const zellen = z => {
    const t = z.trim();
    if (t.length < 2 || !t.startsWith('|') || !t.endsWith('|')) return [];
    const r = t.slice(1, -1), raus = [];
    let start = 0;
    for (let i = 0; i < r.length; i++) {
      if (r[i] !== '|') continue;
      let n = 0;
      for (let j = i - 1; j >= 0 && r[j] === '\\'; j--) n++;
      if (n % 2 === 1) continue;
      raus.push(r.slice(start, i)); start = i + 1;
    }
    raus.push(r.slice(start));
    return raus;
  };
  return md.split('\n').map(z => {
    if (!zeile.test(z)) return z;
    const c = zellen(z);
    if (!c.length || c.every(x => trenner.test(x.trim()))) return z;
    return `| ${c.map(x => (nbsp.test(x.trim()) ? '' : x.trim())).join(' | ')} |`;
  }).join('\n');
}

// --- Pages CMS nachgestellt -------------------------------------------------
// lib/serialization.ts: parse() und stringify()
function lesen(inhalt) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n([\s\S]*))?$/.exec(inhalt);
  if (!m) return { body: inhalt };
  const obj = m[1].trim() ? YAML.parse(m[1], { strict: false, uniqueKeys: false }) : {};
  obj.body = (m[2] || '').replace(/^\r?\n/, '');
  return obj;
}
function schreiben(obj) {
  const kopie = JSON.parse(JSON.stringify(obj));
  const body = kopie.body || '';
  delete kopie.body;
  let kopf = Object.keys(kopie).length ? YAML.stringify(kopie) : '';
  kopf = kopf.trim() ? kopf.trim() + '\n' : '';
  return `---\n${kopf}---\n${body}`;
}
// lib/schema.ts: sanitizeObject() - leere Werte fallen weg
function leerenEntfernen(o) {
  const leer = v => v == null || v === '';
  if (Array.isArray(o)) return o.map(v => (v && typeof v === 'object' ? leerenEntfernen(v) : v)).filter(v => !leer(v));
  if (o && typeof o === 'object') {
    const k = { ...o };
    for (const key of Object.keys(k)) {
      if (k[key] && typeof k[key] === 'object') k[key] = leerenEntfernen(k[key]);
      const v = k[key];
      if ((Array.isArray(v) && v.every(leer)) || (v && typeof v === 'object' && !Array.isArray(v) && !Object.keys(v).length) || leer(v)) delete k[key];
    }
    return k;
  }
  return o;
}
// fields/core/*: was ein Feld beim Oeffnen und Speichern mit dem Wert macht
function feldWert(feld, wert) {
  switch (feld.type) {
    case 'rich-text': return editorRundlauf(wert ?? '');
    case 'boolean': return Boolean(wert);                 // fehlt -> false
    case 'number': return wert == null || wert === '' ? undefined : Number(wert);
    case 'date': return wert == null ? '' : String(wert).slice(0, 10);   // yyyy-MM-dd hin und zurueck
    default:
      if (feld.list) return Array.isArray(wert) ? wert.map(String) : [];
      return wert == null ? '' : String(wert);
  }
}
// app/api/.../files/[path]/route.ts: nur konfigurierte Felder (zod entfernt
// alle anderen), dann mit dem alten Inhalt zusammenfuehren (Listen ersetzen)
function speichern(inhalt, sammlung, merge) {
  const alt = lesen(inhalt);
  const neu = {};
  for (const f of sammlung.fields) {
    const w = feldWert(f, alt[f.name]);
    if (w !== undefined) neu[f.name] = w;
  }
  const zusammen = merge ? mergeWith({}, lesen(inhalt), neu, (a, b) => (Array.isArray(b) ? b : undefined)) : neu;
  return schreiben(leerenEntfernen(JSON.parse(JSON.stringify(zusammen))));
}

// --- Welche Liste erreicht welche Datei? -----------------------------------
function sammlungen(konfig) {
  const raus = [];
  const gehe = eintraege => eintraege.forEach(e => (e.type === 'group' ? gehe(e.items || []) : raus.push(e)));
  gehe(konfig.content || []);
  return raus;
}
function erreicht(sammlung, rel) {
  if (sammlung.type === 'file') return sammlung.path === rel;
  if (!rel.startsWith(sammlung.path + '/') || !rel.endsWith('.md')) return false;
  const teile = rel.slice(sammlung.path.length + 1).split('/');
  if (teile.length > 1 && sammlung.subfolders === false) return false;
  return !teile.some(t => (sammlung.exclude || []).includes(t));
}

// --- Los --------------------------------------------------------------------
const konfigText = fs.readFileSync(path.join(PROJEKT, '.pages.yml'), 'utf8');
const dokument = YAML.parseDocument(konfigText, { strict: false, prettyErrors: false });
if (dokument.errors.length) {
  console.error('.pages.yml ist kein gueltiges YAML:', dokument.errors.map(e => e.message).join('; '));
  process.exit(1);
}
const konfig = dokument.toJSON();
const merge = konfig?.settings?.content?.merge === true;
const alle = sammlungen(konfig);

const hugo = process.env.HUGO || [path.join(os.homedir(), 'bin', 'hugo'), 'hugo'].find(h => {
  try { execFileSync(h, ['version'], { stdio: 'ignore' }); return true; } catch { return false; }
});
if (!hugo) { console.error('Hugo nicht gefunden (PATH, ~/bin/hugo oder HUGO=...).'); process.exit(2); }

const arbeit = fs.mkdtempSync(path.join(os.tmpdir(), 'ncwiki-editor-'));
const kopie = path.join(arbeit, 'projekt');
fs.mkdirSync(kopie);
for (const d of ['content', 'data', 'layouts', 'i18n', 'archetypes']) {
  if (fs.existsSync(path.join(PROJEKT, d))) fs.cpSync(path.join(PROJEKT, d), path.join(kopie, d), { recursive: true });
}
for (const d of ['assets', 'static']) {
  if (fs.existsSync(path.join(PROJEKT, d))) fs.symlinkSync(path.join(PROJEKT, d), path.join(kopie, d));
}
fs.copyFileSync(path.join(PROJEKT, 'hugo.toml'), path.join(kopie, 'hugo.toml'));

let gespeichert = 0, veraendert = 0, draussen = 0, fehler = 0;
const dateien = fs.readdirSync(path.join(kopie, 'content'), { recursive: true })
  .map(d => 'content/' + d.split(path.sep).join('/')).filter(d => d.endsWith('.md')).sort();
for (const rel of dateien) {
  // Erst der Seitenbaum, dann die spezielleren Listen
  const wege = alle.filter(s => erreicht(s, rel)).sort((a, b) => a.path.length - b.path.length);
  if (!wege.length) { draussen++; continue; }
  const p = path.join(kopie, rel);
  const vorher = fs.readFileSync(p, 'utf8');
  let inhalt = vorher;
  for (const s of wege) {
    try { inhalt = speichern(inhalt, s, merge); gespeichert++; }
    catch (e) { fehler++; console.log(`  FEHLER beim Speichern von ${rel} ueber "${s.name}": ${String(e).slice(0, 160)}`); }
  }
  if (inhalt !== vorher) veraendert++;
  fs.writeFileSync(p, inhalt);
}
console.log(`${dateien.length} Seiten: ${dateien.length - draussen} ueber den Web-Editor erreichbar ` +
  `(${gespeichert}-mal gespeichert, ${veraendert} Dateien dabei neu geschrieben), ${draussen} nicht im Editor.`);

function bauen(quelle, ziel) {
  try {
    execFileSync(hugo, ['--source', quelle, '--destination', ziel, '--quiet'], { stdio: ['ignore', 'pipe', 'pipe'] });
    return null;
  } catch (e) { return String(e.stderr || e.stdout || e).slice(-600); }
}
const fehlerVorher = bauen(PROJEKT, path.join(arbeit, 'vorher'));
const fehlerNachher = bauen(kopie, path.join(arbeit, 'nachher'));
if (fehlerVorher) { console.log('Die Website baut schon vorher nicht:\n' + fehlerVorher); process.exit(1); }
if (fehlerNachher) { console.log('NACH dem Speichern baut die Website nicht:\n' + fehlerNachher); process.exit(1); }

const norm = s => s.replace(/\s+/g, ' ');
let gleich = 0; const anders = [];
const seiten = fs.readdirSync(path.join(arbeit, 'vorher'), { recursive: true })
  .filter(d => d.endsWith('.html') && !d.startsWith('pagefind'));
for (const s of seiten) {
  const b = path.join(arbeit, 'nachher', s);
  if (!fs.existsSync(b)) { anders.push([s, 'fehlt nachher']); continue; }
  const x = norm(fs.readFileSync(path.join(arbeit, 'vorher', s), 'utf8'));
  const y = norm(fs.readFileSync(b, 'utf8'));
  if (x === y) { gleich++; continue; }
  let i = 0; while (i < x.length && x[i] === y[i]) i++;
  anders.push([s, `vorher …${x.slice(Math.max(0, i - 60), i + 80)}…\n      nachher …${y.slice(Math.max(0, i - 60), i + 80)}…`]);
}
console.log(`Gebaute Website: ${gleich} von ${seiten.length} Seiten Zeichen fuer Zeichen gleich.`);
for (const [s, w] of anders.slice(0, 8)) console.log(`  ANDERS ${s}\n      ${w}`);
if (!merge) console.log('ACHTUNG: settings.content.merge ist nicht true - Felder ausserhalb von .pages.yml gehen beim Speichern verloren.');
if (behalten) console.log('Arbeitsordner: ' + arbeit); else fs.rmSync(arbeit, { recursive: true, force: true });
process.exit(anders.length || fehler || !merge ? 1 : 0);
