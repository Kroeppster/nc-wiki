/*
 * ============================================================================
 * PRUEFSTAND FUER DEN FAKTEN-GENERATOR AUF FRANZOESISCH UND ITALIENISCH
 * ============================================================================
 *   ~/bin/hugo --minify && (Server auf public/, Port 8123)
 *   node scripts/fakten-generator-sprachen-pruefen.mjs            # fr und it
 *   SPRACHEN=fr RUNDEN=200 node scripts/fakten-generator-sprachen-pruefen.mjs
 *
 * Gegenstueck zu scripts/fakten-generator-pruefen.mjs (Deutsch). Dieselben
 * inhaltlichen Pruefungen, aber ohne deutsche Satzmuster - und dazu, was nur
 * in FR/IT schiefgehen kann:
 *  - Merkmale stehen in der Form des Geschlechts der gefragten Person, auch
 *    bei den Ablenkern ("La patiente … est nerveuse / curieuse …").
 *  - Artikel vor Berufen: "L'avocate", "Lo psicologo", "Il cuoco".
 *  - "de" vor einer Diagnose wird vor Vokal zu "d'" ("souffrant d'asthme").
 *  - Kein deutsches Wort auf der Seite, in den Fragen oder im Druck.
 * Die Regeln fuer Artikel und Elision sind hier UNABHAENGIG vom Generator
 * nachgebaut - wuerden sie aus dem Generator uebernommen, pruefte der Test
 * nur, dass der Generator mit sich selbst uebereinstimmt.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execSync } from 'node:child_process';
const { chromium } = pw;
const SPRACHEN = (process.env.SPRACHEN || 'fr,it').split(',');
const RUNDEN = Number(process.env.RUNDEN || 80);
const ABLAGE = mkdtempSync(join(tmpdir(), 'fakten-sprachen-'));
let ok = 0, fail = 0;
const pruef = (n, c, i = '') => { if (c) { ok++; console.log('  OK    ' + n); } else { fail++; console.log('  FEHLT ' + n + '  ' + String(i).slice(0, 400)); } };
const zeig = l => l.length + (l.length ? ' z.B. ' + l.slice(0, 3).join(' || ') : '');

// Woerter, die auf einer franzoesischen/italienischen Seite nie vorkommen duerfen
const DEUTSCH = /\b(Lernzeit|Bearbeitungszeit|Einprägephase|Reproduktionsphase|Jahre|Testteil|Antwortbogen|Lösung|Lösungen|Fakten lernen|Figuren lernen|umblättern|Patientin|Patient|heisst|von Beruf|Beispiel)\b/;
const VOKAL = /^[aeiouàâäéèêëîïôöùûüœæ]/i, VOKAL_H = /^[aeiouàâäéèêëîïôöùûüœæh]/i;
const REGELN = {
  fr: {
    alter: a => `env. ${a} ans`, alterIm: (a) => ` de ${a} ans `,
    derPatient: { m: 'Le patient', w: 'La patiente' },
    artikel: (wort, g) => VOKAL_H.test(wort) ? "L'" + wort : (g === 'm' ? 'Le ' : 'La ') + wort,
    diagnoseIm: k => ' souffrant ' + (VOKAL_H.test(k) ? "d'" : 'de ') + k + ' ',
    elisionFalsch: t => / de [aeiouàâäéèêëîïôöùûüœæh]/i.test(t),
  },
  it: {
    alter: a => `circa ${a} anni`, alterIm: (a) => ` di ${a} anni `,
    derPatient: { m: 'Il paziente', w: 'La paziente' },
    artikel: (wort, g) => VOKAL_H.test(wort) ? "L'" + wort
      : g === 'm' ? (/^(s[^aeiouàèéìòù]|z|gn|ps|pn|x|y)/i.test(wort) ? 'Lo ' : 'Il ') + wort : 'La ' + wort,
    diagnoseIm: (k, W) => ' con ' + W.dativ[k] + ' ',
    elisionFalsch: t => / (il|lo|la) [aeiouàèéìòù]/i.test(t),
  },
};

const b = await chromium.launch();
for (const sprache of SPRACHEN) {
  const R = REGELN[sprache];
  console.log(`\n######## ${sprache.toUpperCase()} ########`);
  const ctx = await b.newContext({ viewport: { width: 1100, height: 1000 }, reducedMotion: 'reduce' });
  await ctx.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });
  const p = await ctx.newPage(); const js = [];
  p.on('pageerror', e => { if (!/PagefindUI/.test(String(e.message))) js.push(String(e.message).slice(0, 110)); });
  await p.addInitScript(() => { window.__gedruckt = 0; window.print = function () { window.__gedruckt++; }; });
  await p.goto(`http://127.0.0.1:8123/${sprache}/alpha/`, { waitUntil: 'networkidle' });

  console.log('=== Seite und Lern-Generator ===');
  const start = await p.evaluate(() => ({
    keineListe: !document.getElementById('lg-keine-fakten').hidden,
    faktenAn: !document.getElementById('lg-mit-fakten').disabled,
    text: document.querySelector('main').innerText }));
  pruef('Wortliste vorhanden, Fakten waehlbar', !start.keineListe && start.faktenAn, JSON.stringify({ keineListe: start.keineListe, faktenAn: start.faktenAn }));
  pruef('kein deutsches Wort auf der Seite', !DEUTSCH.test(start.text), (start.text.match(DEUTSCH) || [])[0]);
  const W = await p.evaluate(() => JSON.parse(document.getElementById('fg-daten').textContent));
  pruef(`Wortliste ist die ${sprache}-Liste`, W.grammatik === sprache, W.grammatik);

  // Formen -> Merkmal-Eintrag und Geschlecht
  const merkmalVon = {};   // Form -> { m, w }
  [].concat(W.merkmale.charakter, W.merkmale.zustand).forEach(e => {
    const o = typeof e === 'string' ? { m: e, w: e } : e;
    merkmalVon[o.m] = o; merkmalVon[o.w] = o;
  });
  const geschlecht = {};
  Object.values(W.berufe).forEach(l => l.forEach(x => { geschlecht[x.m] = 'm'; geschlecht[x.w] = 'w'; }));

  // Ein Durchlauf mit Ablenkung: Texte auf Deutsch?
  await p.uncheck('#lg-mit-figuren'); await p.fill('#lg-pause', '0');
  await p.click('#lg-los'); await p.waitForTimeout(150);
  const blattLernen = await p.evaluate(() => document.getElementById('lg-wurzel').innerText);
  pruef('Einpraegephase ohne deutsche Woerter', !DEUTSCH.test(blattLernen), (blattLernen.match(DEUTSCH) || [])[0]);
  await p.click('#lg-weiter'); await p.waitForTimeout(150);
  const blattAbfrage = await p.evaluate(() => document.getElementById('lg-wurzel').innerText);
  pruef('Abfrage ohne deutsche Woerter', !DEUTSCH.test(blattAbfrage), (blattAbfrage.match(DEUTSCH) || [])[0]);
  await p.click('#lg-weiter'); await p.waitForTimeout(150);

  console.log(`=== ${RUNDEN} Sets, jede Frage gegen die Einpraegeliste ===`);
  const fehler = { loesung: [], eindeutig: [], optionen: [], geschlecht: [], merkmalform: [], artikel: [], elision: [],
                   namen: [], verraten: [], deutsch: [], gruppe: [] };
  const typen = {}, beispiele = new Map();
  for (let r = 0; r < RUNDEN; r++) {
    if (r) { await p.click('#lg-nochmal'); await p.click('#lg-los'); await p.click('#lg-weiter'); await p.click('#lg-weiter'); }
    const d = await p.evaluate(() => ({
      liste: [...document.querySelectorAll('#lg-loesungen .ems-gruppe')].map(g => [...g.querySelectorAll('.ems-zeile')].map(z => [...z.children].map(c => c.textContent))),
      fragen: [...document.querySelectorAll('#lg-loesungen .ems-frage')].map(f => ({
        text: f.querySelector('.ems-frage-text').textContent,
        optionen: [...f.querySelectorAll('.ems-option')].map(o => o.children[1].textContent),
        richtig: [...f.querySelectorAll('.ems-option')].findIndex(o => o.classList.contains('fg-ist-richtig')) })) }));
    const leute = [];
    d.liste.forEach((g, gi) => g.forEach(([n, a, rest]) => {
      const m = rest.match(/^(.*?), (.*?) - (.*)$/);
      leute.push({ name: n.replace(/\s*:$/, ''), alter: +a.match(/\d+/)[0], beruf: m[1], merkmal: m[2], krankheit: m[3], gruppe: gi, g: geschlecht[m[1]] });
    }));
    leute.forEach(x => { if (merkmalVon[x.merkmal] && merkmalVon[x.merkmal][x.g] !== x.merkmal) fehler.merkmalform.push(`Liste: ${x.beruf} ist ${x.merkmal}`); });
    d.liste.forEach(g => {
      const namen = g.map(z => z[0].replace(/\s*:$/, ''));
      if (!(W.namensgruppen || []).some(ng => namen.every(n => ng.includes(n)))) fehler.gruppe.push(namen.join('/'));
    });
    const genannt = {};
    d.fragen.forEach(f => {
      const t = ' ' + f.text.replace(/ …$/, '') + ' ';
      if (DEUTSCH.test(f.text + ' ' + f.optionen.join(' '))) fehler.deutsch.push(f.text);
      if (R.elisionFalsch(t)) fehler.elision.push(f.text);
      // Wonach wird gefragt?
      const art = ['name', 'beruf', 'krankheit'].find(k => f.optionen.every(o => leute.some(x => x[k] === o)))
        || (f.optionen.every(o => merkmalVon[o]) ? 'merkmal' : null)
        || (f.optionen.every(o => leute.some(x => R.alter(x.alter) === o)) ? 'alter' : null);
      if (!art || new Set(f.optionen).size !== 5) { fehler.optionen.push(f.text + ' :: ' + f.optionen.join('|')); return; }
      // Wer ist gemeint?
      const grenze = s => new RegExp("(^|[\\s'])" + s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + "(?=\\s)");
      let kandidaten = leute.map(x => {
        const treffer = [];
        if (grenze(x.name).test(t)) treffer.push('name');
        if (grenze(x.beruf).test(t)) treffer.push('beruf');
        if (t.includes(R.diagnoseIm(x.krankheit, W))) treffer.push('krankheit');
        if (t.includes(' ' + R.derPatient[x.g] + ' ' + x.merkmal + ' ')) treffer.push('merkmal');
        if (t.includes(' ' + R.derPatient[x.g] + R.alterIm(x.alter))) treffer.push('alter');
        return { x, treffer };
      }).filter(k => k.treffer.length);
      // "L'ingénieur aéronautique" enthaelt "ingénieur": Passt ein Beruf nur,
      // weil er in einem laengeren Beruf derselben Frage steckt, zaehlt er nicht.
      const berufe = kandidaten.filter(k => k.treffer.includes('beruf')).map(k => k.x.beruf);
      kandidaten = kandidaten.filter(k => !(k.treffer.length === 1 && k.treffer[0] === 'beruf'
        && berufe.some(b => b !== k.x.beruf && b.includes(k.x.beruf))));
      if (kandidaten.length !== 1) { fehler.eindeutig.push(f.text + ' -> ' + kandidaten.map(k => k.x.name).join(',')); return; }
      const { x, treffer } = kandidaten[0];
      const typ = treffer[0] + '>' + art;
      typen[typ] = (typen[typ] || 0) + 1;
      if (!beispiele.has(typ)) beispiele.set(typ, f.text + ' (' + f.optionen.join(' / ') + ')');
      const soll = art === 'alter' ? R.alter(x.alter) : x[art];
      if (f.optionen[f.richtig] !== soll) fehler.loesung.push(`${f.text} markiert ${f.optionen[f.richtig]}, richtig ${soll}`);
      // Artikel vor einem Beruf am Satzanfang
      if (treffer[0] === 'beruf' && !f.text.startsWith(R.artikel(x.beruf, x.g))) fehler.artikel.push(`${f.text} (erwartet: ${R.artikel(x.beruf, x.g)})`);
      // Merkmal-Antworten alle in der Form der gefragten Person
      if (art === 'merkmal' && !f.optionen.every(o => merkmalVon[o][x.g] === o)) fehler.merkmalform.push(f.text + ' :: ' + f.optionen.join('|'));
      // Berufsfrage, die das Geschlecht nennt: alle fuenf Berufe dieses Geschlechts
      if (art === 'beruf' && (treffer.includes('name') || treffer.includes('alter')) && !f.optionen.every(o => geschlecht[o] === x.g))
        fehler.geschlecht.push(f.text + ' :: ' + f.optionen.join('|'));
      if (art === 'name') {
        const nachbarn = leute.filter(y => y.gruppe === x.gruppe && y !== x).map(y => y.name);
        if (!nachbarn.every(n => f.optionen.includes(n))) fehler.namen.push(f.text + ' :: ' + f.optionen.join('|'));
      }
      (genannt[x.name] = genannt[x.name] || []).push([treffer[0], art]);
    });
    Object.entries(genannt).forEach(([n, l]) => {
      for (let i = 0; i < l.length; i++) for (let k = i + 1; k < l.length; k++)
        if (l[i].some(a => l[k].includes(a))) fehler.verraten.push(`${n}: ${l[i].join('>')} / ${l[k].join('>')}`);
    });
  }
  pruef('markierte Loesung ist die der gemeinten Person', !fehler.loesung.length, zeig(fehler.loesung));
  pruef('jede Frage passt auf genau eine Person', !fehler.eindeutig.length, zeig(fehler.eindeutig));
  pruef('fuenf verschiedene Antworten derselben Art', !fehler.optionen.length, zeig(fehler.optionen));
  pruef('Merkmale in der Form der Person (Liste und Antworten)', !fehler.merkmalform.length, zeig(fehler.merkmalform));
  pruef('Berufsfragen mit Geschlecht: alle Berufe gleichen Geschlechts', !fehler.geschlecht.length, zeig(fehler.geschlecht));
  pruef('Artikel vor Berufen (L\'/Lo/Il/La/Le)', !fehler.artikel.length, zeig(fehler.artikel));
  pruef('keine fehlende Elision ("de asthme", "la asma")', !fehler.elision.length, zeig(fehler.elision));
  pruef('Namensfragen enthalten die aehnlichen Namen der Gruppe', !fehler.namen.length, zeig(fehler.namen));
  pruef('drei Personen einer Altersgruppe aus einer Namensgruppe', !fehler.gruppe.length, zeig(fehler.gruppe));
  pruef('keine Frage verraet die Antwort einer anderen', !fehler.verraten.length, zeig(fehler.verraten));
  pruef('keine deutschen Woerter in Fragen und Antworten', !fehler.deutsch.length, zeig(fehler.deutsch));
  const n = Object.keys(typen).length;
  if (RUNDEN >= 50) pruef('alle zwoelf Fragetypen kommen vor', n === 12, Object.keys(typen).join(', '));
  console.log('    Beispiele je Fragetyp:');
  [...beispiele.entries()].sort().forEach(([k, v]) => console.log(`      ${k.padEnd(18)} ${v}`));

  console.log('=== Druck ===');
  await p.click('#lg-drucken-ende'); await p.waitForTimeout(300);
  await p.emulateMedia({ media: 'print' });
  const pdf = join(ABLAGE, `fakten-${sprache}.pdf`);
  await p.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  await p.emulateMedia({ media: 'screen' });
  const info = JSON.parse(execSync(`python3 -c "import pymupdf,json,sys;d=pymupdf.open(sys.argv[1]);print(json.dumps({'seiten':d.page_count,'text':' '.join(s.get_text() for s in d)}))" ${pdf}`).toString());
  pruef('Druck: sechs Seiten', info.seiten === 6, String(info.seiten));
  pruef('Druck ohne deutsche Woerter', !DEUTSCH.test(info.text), (info.text.match(DEUTSCH) || [])[0]);
  await p.evaluate(() => window.dispatchEvent(new Event('afterprint')));

  console.log('=== Figuren (nur Sprache) ===');
  await p.click('#lg-nochmal').catch(() => {});
  await p.check('#lg-mit-figuren'); await p.uncheck('#lg-mit-fakten');
  await p.click('#lg-los'); await p.waitForTimeout(300);
  const fig = await p.evaluate(() => document.getElementById('lg-wurzel').innerText);
  pruef('Figuren-Einpraegephase ohne deutsche Woerter', !DEUTSCH.test(fig), (fig.match(DEUTSCH) || [])[0]);
  pruef('keine JS-Fehler', js.length === 0, js.join(' | '));
  await ctx.close();
}
console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
await b.close();
process.exit(fail ? 1 : 0);
