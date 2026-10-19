// ============================================================================
// GESCHÜTZTE LEERZEICHEN: KEIN ZEILENUMBRUCH, WO ER STÖRT
// ============================================================================
// Ein normales Leerzeichen darf der Browser umbrechen. An einigen Stellen sieht
// das falsch aus, deshalb ersetzt dieses Skript nach dem Bauen dort das
// Leerzeichen durch ein geschütztes (U+00A0, sieht gleich aus, bricht nicht um):
//
//   Französisch   vor ! ? : ; » und nach «   (sonst steht z. B. ein «?» allein
//                 am Zeilenanfang – Chrome bricht dort um)
//   Deutsch       in Abkürzungen wie «z. B.», «d. h.», «u. a.»
//   alle          in Daten («9. Juli», «9 juillet», «9 luglio») und bei «CHF 300»
//
// So muss beim Schreiben (Web-Editor, Textmappen) niemand daran denken. Die
// Sprache einer Seite steht in <html lang="...">.
//
// Geändert wird nur sichtbarer Text, nie Skripte, Styles, Code-Beispiele oder
// Attribute. Mehrfaches Ausführen ändert nichts mehr.
//
// Aufruf (nach "hugo --minify", vor Pagefind):  node scripts/typografie.mjs public
// ============================================================================
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const NBSP = ' ';

// Kommentare, Skripte/Styles/Textfelder (als Ganzes) und alle übrigen Tags.
const TOKEN = /<!--[\s\S]*?-->|<(script|style|textarea)\b[\s\S]*?<\/\1\s*>|<(\/?)([a-zA-Z][\w-]*)(?:"[^"]*"|'[^']*'|[^'">])*>/gi;
const OHNE = new Set(['pre', 'code', 'kbd', 'samp']);

const MONATE = {
  de: 'Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember',
  fr: 'janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre',
  it: 'gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre',
};
const DATUM = Object.fromEntries(Object.entries(MONATE).map(([l, m]) =>
  [l, new RegExp(`\\b(\\d{1,2}\\.?|1er) (?=(?:${m})\\b)`, 'g')]));
// Einzelbuchstabe, Punkt, Leerzeichen, Einzelbuchstabe, Punkt: z. B., d. h., i. d. R.
const ABKUERZUNG = /(?<!\p{L})(\p{L})\. (?=\p{L}\.)/gu;

function regeln(lang) {
  return (t) => {
    t = t.replace(/\bCHF (?=\d)/g, 'CHF' + NBSP);
    if (DATUM[lang]) t = t.replace(DATUM[lang], '$1' + NBSP);
    if (lang === 'de') t = t.replace(ABKUERZUNG, '$1.' + NBSP);
    if (lang === 'fr') {
      t = t
        .replace(/ (?=[!?:;»]|&raquo;|&#187;)/g, NBSP)
        .replace(/(«|&laquo;|&#171;) /g, '$1' + NBSP);
    }
    return t;
  };
}

export function seite(html, lang) {
  lang ??= (html.match(/<html\b[^>]*\blang="?([a-z]{2})/i) || [])[1];
  const text = regeln(lang);
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

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  let geaendert = 0;
  for (const f of dateien(process.argv[2] || 'public')) {
    const alt = readFileSync(f, 'utf8');
    const neu = seite(alt);
    if (neu !== alt) { writeFileSync(f, neu); geaendert++; }
  }
  console.log(`typografie: ${geaendert} Seiten angepasst`);
}
