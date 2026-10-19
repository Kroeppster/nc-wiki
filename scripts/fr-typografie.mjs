// ============================================================================
// FRANZÖSISCH: KEIN ZEILENUMBRUCH VOR « ! ? : ; » UND NACH «
// ============================================================================
// Im Französischen steht vor ! ? : ; » und nach « ein Leerzeichen. Ist es ein
// normales, darf der Browser dort umbrechen, und Chrome tut das auch: Dann
// steht z. B. ein einzelnes «!» oder «?» am Anfang der nächsten Zeile. Dieses
// Skript ersetzt nach dem Bauen in allen Seiten unter public/fr/ genau diese
// Leerzeichen durch geschützte (U+00A0, sieht gleich aus, bricht nicht um).
// So muss beim Schreiben (Web-Editor, Textmappen) niemand daran denken.
//
// Geändert wird nur sichtbarer Text, nie Skripte, Styles, Code-Beispiele oder
// Attribute. Mehrfaches Ausführen ändert nichts mehr.
//
// Aufruf (nach "hugo --minify", vor Pagefind):  node scripts/fr-typografie.mjs public
// ============================================================================
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const NBSP = '\u00a0';

// Kommentare, Skripte/Styles/Textfelder (als Ganzes) und alle übrigen Tags.
const TOKEN = /<!--[\s\S]*?-->|<(script|style|textarea)\b[\s\S]*?<\/\1\s*>|<(\/?)([a-zA-Z][\w-]*)(?:"[^"]*"|'[^']*'|[^'">])*>/gi;
const OHNE = new Set(['pre', 'code', 'kbd', 'samp']);

function text(t) {
  return t
    .replace(/ (?=[!?:;»]|&raquo;|&#187;)/g, NBSP)
    .replace(/(«|&laquo;|&#171;) /g, '$1' + NBSP);
}

export function seite(html) {
  let aus = '', pos = 0, tiefe = 0, m;
  TOKEN.lastIndex = 0;
  while ((m = TOKEN.exec(html))) {
    const t = html.slice(pos, m.index);
    aus += tiefe ? t : text(t);
    aus += m[0];
    const name = (m[3] || '').toLowerCase();
    if (OHNE.has(name)) tiefe = Math.max(0, tiefe + (m[2] ? -1 : 1));
    pos = TOKEN.lastIndex;
  }
  const rest = html.slice(pos);
  return aus + (tiefe ? rest : text(rest));
}

function dateien(ordner) {
  return readdirSync(ordner).flatMap((n) => {
    const p = join(ordner, n);
    return statSync(p).isDirectory() ? dateien(p) : n.endsWith('.html') ? [p] : [];
  });
}

if (import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const wurzel = join(process.argv[2] || 'public', 'fr');
  let geaendert = 0;
  for (const f of dateien(wurzel)) {
    const alt = readFileSync(f, 'utf8');
    const neu = seite(alt);
    if (neu !== alt) { writeFileSync(f, neu); geaendert++; }
  }
  console.log(`fr-typografie: ${geaendert} Seiten angepasst`);
}
