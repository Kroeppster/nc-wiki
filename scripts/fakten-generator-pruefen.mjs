/*
 * ============================================================================
 * PRUEFSTAND FUER DEN FAKTEN-GENERATOR UND SEIN TESTHEFT
 * ============================================================================
 *   ~/bin/hugo --minify && (Server auf public/, Port 8123)
 *   node scripts/fakten-generator-pruefen.mjs [/pfad/fuer/das/test-pdf]
 *   RUNDEN=300 node scripts/fakten-generator-pruefen.mjs     # mehr Sets
 *
 * Ohne Pfad landet das Test-PDF im Temp-Ordner.
 *
 * DREI TEILE:
 *  1. Ein Durchlauf: Format wie im Testheft (Ueberschrift, Kasten, Liste in
 *     fuenf Gruppen, 18 Fragen zweispaltig, STOPP).
 *  2. VIELE SETS, jede Frage INHALTLICH gegen die Einpraegeliste geprueft -
 *     nicht bloss gezaehlt: Ist die als richtig markierte Antwort wirklich
 *     die der gemeinten Person? Gibt es genau eine Person, auf die die Frage
 *     passt? Sind bei "Frau Koskinen ist …" alle fuenf Berufe weiblich? Heissen
 *     die drei Personen einer Altersgruppe aehnlich? Verraet keine Frage die
 *     Antwort einer anderen? Ein Wurf zeigt so etwas nicht zuverlaessig -
 *     deshalb viele.
 *  3. Der Druck als PDF: sechs A4-Seiten in der Reihenfolge des Hefts, ohne
 *     Navigation, und das Loesungsblatt stimmt mit der Auswertung ueberein.
 *
 * FALLEN, die hier schon zugeschlagen haben:
 *  - window.print() blockiert den Lauf. Wird durch einen Zaehler ersetzt;
 *    dadurch kommt auch kein afterprint, und der Druckbehaelter bleibt fuer
 *    die Messung stehen. Aufgeraeumt wird am Ende von Hand (afterprint).
 *  - getComputedStyle(...).display taugt NICHT als Sichtbarkeitspruefung:
 *    Ein Kind eines display:none-Vorfahren behaelt seinen eigenen Wert.
 *    Gefragt ist getClientRects().length.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { mkdtempSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execSync } from 'node:child_process';
const { chromium } = pw;
const ABLAGE = process.argv[2] || mkdtempSync(join(tmpdir(), 'fakten-'));
const RUNDEN = Number(process.env.RUNDEN || 150);
mkdirSync(ABLAGE, { recursive: true });
const b = await chromium.launch();
let ok = 0, fail = 0;
const pruef = (n, c, i = '') => { if (c) { ok++; console.log('  OK    ' + n); } else { fail++; console.log('  FEHLT ' + n + '  ' + String(i).slice(0, 300)); } };
const ctx = await b.newContext({ viewport: { width: 1100, height: 1000 } });
await ctx.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });
const p = await ctx.newPage(); const js = [];
p.on('pageerror', e => { if (!/PagefindUI/.test(String(e.message))) js.push(String(e.message).slice(0, 110)); });
await p.addInitScript(() => { window.__gedruckt = 0; window.print = function () { window.__gedruckt++; }; });
await p.goto('http://127.0.0.1:8123/ems/uebungsaufgaben/figuren-fakten-lernen/', { waitUntil: 'networkidle' });

console.log('=== Ein Durchlauf ===');
const W = await p.evaluate(() => JSON.parse(document.getElementById('fg-daten').textContent));
await p.fill('#fg-min-pause', '0');
await p.click('#fg-los'); await p.waitForTimeout(200);
const lern = await p.evaluate(() => {
  const b = document.getElementById('fg-blatt-lernen');
  return { kopf: b.querySelector('.ems-kopf')?.textContent, kasten: b.querySelector('.ems-kasten')?.textContent,
           gruppen: [...b.querySelectorAll('.ems-gruppe')].map(g => g.querySelectorAll('.ems-zeile').length),
           stopp: !!b.querySelector('.ems-marke-stopp') };
});
pruef('Ueberschrift wie im Heft', /Fakten lernen \(Einprägephase\)\s*Lernzeit: 6 Minuten/.test(lern.kopf), lern.kopf);
pruef('Anleitung im Wortlaut des Hefts, mit Beispiel', /15 Patienten werden Ihnen vorgestellt/.test(lern.kasten)
  && /Meier: ca\. 40 Jahre, Polizistin, ledig - Oberarmfraktur/.test(lern.kasten) && /richtige Antwort wäre \(C\)/.test(lern.kasten));
pruef('fuenf Gruppen zu drei Personen', JSON.stringify(lern.gruppen) === '[3,3,3,3,3]', JSON.stringify(lern.gruppen));
pruef('STOPP am Ende der Einpraegephase', lern.stopp);
await p.click('#fg-fertig-lernen'); await p.waitForTimeout(200);
const ab = await p.evaluate(() => {
  const b = document.getElementById('fg-blatt-abfrage');
  return { kopf: b.querySelector('.ems-kopf')?.textContent, fragen: b.querySelectorAll('.ems-frage').length,
           wahl: [...b.querySelectorAll('.ems-frage')].map(f => f.querySelectorAll('input[type=radio]').length),
           nummern: [...b.querySelectorAll('.ems-nr')].map(n => n.textContent).join(' '),
           spalten: getComputedStyle(b.querySelector('.ems-fragen')).columnCount };
});
pruef('Ueberschrift der Abfrage', /Fakten lernen \(Reproduktionsphase\)\s*Bearbeitungszeit: 6 Minuten/.test(ab.kopf), ab.kopf);
pruef('18 Fragen, je fuenf Antworten', ab.fragen === 18 && ab.wahl.every(n => n === 5), JSON.stringify(ab.wahl));
pruef('nummeriert 1) bis 18)', ab.nummern === Array.from({ length: 18 }, (_, i) => (i + 1) + ')').join(' '), ab.nummern);
pruef('zweispaltig wie im Heft', ab.spalten === '2', ab.spalten);

// --- 2. Viele Sets, jede Frage gegen die Liste --------------------------------
console.log(`\n=== ${RUNDEN} Sets, jede Frage gegen die Einpraegeliste ===`);
const geschlecht = {};
Object.values(W.berufe).forEach(l => l.forEach(x => { geschlecht[x.wort] = x.geschlecht === 'w' ? 'w' : 'm'; }));
const attributiv = m => (/e$/.test(m) ? m : /el$/.test(m) ? m.slice(0, -2) + 'le' : m + 'e');
const fehler = { loesung: [], eindeutig: [], optionen: [], geschlecht: [], namen: [], alter: [], verraten: [], dativ: [], gruppe: [], sortiert: [] };
const typen = {};
for (let r = 0; r < RUNDEN; r++) {
  if (r) { await p.click('#fg-nochmal'); await p.click('#fg-los'); await p.click('#fg-fertig-lernen'); }
  await p.click('#fg-auswerten');
  const d = await p.evaluate(() => ({
    liste: [...document.querySelectorAll('#fg-blatt-set .ems-gruppe')].map(g => [...g.querySelectorAll('.ems-zeile')].map(z => [...z.children].map(c => c.textContent))),
    fragen: [...document.querySelectorAll('#fg-blatt-loesung .ems-frage')].map(f => ({
      text: f.querySelector('.ems-frage-text').textContent,
      optionen: [...f.querySelectorAll('.ems-option')].map(o => o.children[1].textContent),
      richtig: [...f.querySelectorAll('.ems-option')].findIndex(o => o.classList.contains('fg-ist-richtig')) })) }));
  // Personen aus der Liste zurueckgewinnen: "Meier:" | "ca. 35 Jahre" | "Beruf, Merkmal - Diagnose"
  const leute = [];
  d.liste.forEach((g, gi) => g.forEach(([n, a, rest]) => {
    const m = rest.match(/^(.*?), (.*?) - (.*)$/);
    leute.push({ name: n.replace(/:$/, ''), alter: +a.match(/\d+/)[0], beruf: m[1], merkmal: m[2], krankheit: m[3], gruppe: gi });
  }));
  const alter = [...new Set(leute.map(x => x.alter))];
  if (alter.some((a, i) => i && a - alter[i - 1] < (W.altersgruppen_abstand || 5))) fehler.alter.push(alter.join(','));
  d.liste.forEach(g => {
    const namen = g.map(z => z[0].replace(/:$/, ''));
    if (!(W.namensgruppen || []).some(ng => namen.every(n => ng.includes(n)))) fehler.gruppe.push(namen.join('/'));
  });
  const genannt = {};   // je Person: Angaben, die ihre Fragen nennen oder fragen
  d.fragen.forEach(f => {
    const t = ' ' + f.text + ' ';
    // Wonach wird gefragt? Das verraten die Antworten.
    const art = ['name', 'beruf', 'merkmal', 'krankheit'].find(k => f.optionen.every(o => leute.some(x => x[k] === o)))
      || (f.optionen.every(o => /^ca\. \d+ Jahre alt$/.test(o)) ? 'alter' : null);
    if (!art || new Set(f.optionen).size !== 5) { fehler.optionen.push(f.text + ' :: ' + f.optionen.join('|')); return; }
    // Wer ist gemeint? Genau eine Person muss auf den Text passen.
    const dativ = k => (W.dativ && W.dativ[k]) || k;
    const kandidaten = leute.map(x => {
      const treffer = [];
      if (t.includes(' ' + x.name + ' ')) treffer.push('name');
      if (t.includes(' ' + x.beruf + ' ')) treffer.push('beruf');
      if (t.includes(' mit ' + dativ(x.krankheit) + ' ')) treffer.push('krankheit');
      if (t.includes(' ' + attributiv(x.merkmal) + ' Patient')) treffer.push('merkmal');
      if (t.includes(' ' + x.alter + '-jährige ' + (geschlecht[x.beruf] === 'w' ? 'Patientin' : 'Patient') + ' ')) treffer.push('alter');
      return { x, treffer };
    }).filter(k => k.treffer.length);
    if (kandidaten.length !== 1) { fehler.eindeutig.push(f.text + ' -> ' + kandidaten.map(k => k.x.name).join(',')); return; }
    const { x, treffer } = kandidaten[0];
    typen[treffer[0] + '>' + art] = (typen[treffer[0] + '>' + art] || 0) + 1;
    const soll = art === 'alter' ? `ca. ${x.alter} Jahre alt` : x[art];
    if (f.optionen[f.richtig] !== soll) fehler.loesung.push(`${f.text} markiert ${f.optionen[f.richtig]}, richtig ${soll}`);
    if (/ mit (Herzprobleme|Ohrgeräusche) /.test(t)) fehler.dativ.push(f.text);
    if (art === 'alter' && f.optionen.join() !== [...f.optionen].sort((a, c) => parseInt(a.slice(4)) - parseInt(c.slice(4))).join()) fehler.sortiert.push(f.optionen.join('|'));
    // "Frau Koskinen ist …" / "Die 55-jaehrige Patientin ist von Beruf …": alle Berufe gleichen Geschlechts
    if (art === 'beruf' && (treffer.includes('name') || treffer.includes('alter'))
        && !f.optionen.every(o => geschlecht[o] === geschlecht[x.beruf])) fehler.geschlecht.push(f.text + ' :: ' + f.optionen.join('|'));
    // Namensfragen: die beiden Namen aus derselben Gruppe stehen als Ablenker da
    if (art === 'name') {
      const nachbarn = leute.filter(y => y.gruppe === x.gruppe && y !== x).map(y => y.name);
      if (!nachbarn.every(n => f.optionen.includes(n))) fehler.namen.push(f.text + ' :: ' + f.optionen.join('|'));
    }
    (genannt[x.name] = genannt[x.name] || []).push([treffer[0], art]);
  });
  // Zwei Fragen zur selben Person duerfen keine Angabe teilen - sonst nennt
  // die eine, was die andere fragt.
  Object.entries(genannt).forEach(([n, l]) => {
    for (let i = 0; i < l.length; i++) for (let k = i + 1; k < l.length; k++)
      if (l[i].some(a => l[k].includes(a))) fehler.verraten.push(`${n}: ${l[i].join('>')} / ${l[k].join('>')}`);
  });
}
const zeig = l => l.length + (l.length ? ' z.B. ' + l.slice(0, 2).join(' || ') : '');
pruef('markierte Loesung ist die der gemeinten Person', !fehler.loesung.length, zeig(fehler.loesung));
pruef('jede Frage passt auf genau eine Person', !fehler.eindeutig.length, zeig(fehler.eindeutig));
pruef('fuenf verschiedene Antworten derselben Art', !fehler.optionen.length, zeig(fehler.optionen));
pruef('"Frau X ist …": alle Berufe gleichen Geschlechts', !fehler.geschlecht.length, zeig(fehler.geschlecht));
pruef('Namensfragen enthalten die aehnlichen Namen der Gruppe', !fehler.namen.length, zeig(fehler.namen));
pruef('drei Personen einer Altersgruppe aus einer Namensgruppe', !fehler.gruppe.length, zeig(fehler.gruppe));
pruef('Altersgruppen mit Abstand', !fehler.alter.length, zeig(fehler.alter));
pruef('Altersantworten aufsteigend wie im Heft', !fehler.sortiert.length, zeig(fehler.sortiert));
pruef('keine Frage verraet die Antwort einer anderen', !fehler.verraten.length, zeig(fehler.verraten));
pruef('Plural-Diagnosen im Dativ ("mit Herzproblemen")', !fehler.dativ.length, zeig(fehler.dativ));
const n = Object.keys(typen).length;
console.log('    Fragetypen (nennt>fragt): ' + Object.entries(typen).sort((a, c) => c[1] - a[1]).map(([k, v]) => k + ' ' + v).join(', '));
// Erst ab 50 Sets gewertet: "Der 42-jaehrige Patient ist von Beruf …" geht
// nur, wenn in der Altersgruppe genau eine Person ihres Geschlechts steckt,
// und macht deshalb nur rund 4 % der Fragen aus. Bei 5 Sets fehlte sie in
// 2 von 20 Laeufen - ein Zufall der kleinen Stichprobe, kein Fehler.
if (RUNDEN >= 50) pruef('alle zwoelf Fragetypen kommen vor', n === 12, String(n));
else console.log('    (Fragetypen erst ab RUNDEN=50 gewertet)');

// --- 3. Der Druck ---------------------------------------------------------------
console.log('\n=== Druck ===');
const erwartet = await p.evaluate(() => [...document.querySelectorAll('#fg-blatt-loesung .ems-frage')]
  .map(f => 'ABCDE'[[...f.querySelectorAll('.ems-option')].findIndex(o => o.classList.contains('fg-ist-richtig'))]).join(''));
await p.click('#fg-drucken-ende'); await p.waitForTimeout(300);
pruef('print() aufgerufen', (await p.evaluate(() => window.__gedruckt)) === 1);
const dr = await p.evaluate(() => { const d = document.getElementById('ems-druck');
  return { seiten: d.querySelectorAll('.ems-seite').length, amBody: d.parentElement === document.body,
           fragen: d.querySelectorAll('.ems-frage').length, zeilen: d.querySelectorAll('.ems-zeile').length,
           bogen: d.querySelectorAll('.ems-bogen-zeile').length, rand: !!document.getElementById('ems-druck-seite') }; });
pruef('sechs Heftseiten', dr.seiten === 6, String(dr.seiten));
pruef('15 Personen, 18 Fragen, 18 Zeilen Antwortbogen', dr.zeilen === 15 && dr.fragen === 18 && dr.bogen === 18, JSON.stringify(dr));
pruef('Druckbehaelter direkt unter <body>, Seitenrand nur fuer diesen Druck', dr.amBody && dr.rand);
await p.emulateMedia({ media: 'print' });
const sichtbar = await p.evaluate(() => {
  const gerendert = e => !!e && e.getClientRects().length > 0;
  return { druck: gerendert(document.getElementById('ems-druck')), kopf: gerendert(document.querySelector('header.site')),
           start: gerendert(document.getElementById('fg-wurzel')) };
});
pruef('im Druck nur das Heft', sichtbar.druck && !sichtbar.kopf && !sichtbar.start, JSON.stringify(sichtbar));
await p.pdf({ path: ABLAGE + '/fakten-set.pdf', preferCSSPageSize: true, printBackground: true });
await p.emulateMedia({ media: 'screen' });
const info = JSON.parse(execSync('python3 -c "' +
  'import pymupdf,json,sys;d=pymupdf.open(sys.argv[1]);' +
  'print(json.dumps({\'seiten\':d.page_count,\'masse\':[[round(s.rect.width),round(s.rect.height)] for s in d],\'texte\':[s.get_text() for s in d]}))' +
  '" ' + ABLAGE + '/fakten-set.pdf').toString());
pruef('PDF: genau sechs A4-Seiten', info.seiten === 6 && info.masse.every(m => m[0] === 595 && m[1] === 842), JSON.stringify(info.masse));
const t = info.texte;
pruef('S. 1: Einpraegephase, Testteil A, Anleitung', /Testteil A/.test(t[0]) && /Fakten lernen \(Einprägephase\)/.test(t[0]) && /15 Patienten/.test(t[0]));
pruef('S. 2: Liste mit 15 Personen und STOPP', (t[1].match(/ca\. \d+ Jahre\n/g) || []).length === 15 && /STOPP/.test(t[1]), (t[1].match(/ca\. \d+ Jahre/g) || []).length);
pruef('S. 3: Reproduktionsphase, Testteil B, Fragen 1-8, Pfeil', /Testteil B/.test(t[2]) && /Reproduktionsphase/.test(t[2]) && /\n8\)/.test(t[2]) && !/\n9\)/.test(t[2]) && /umblättern und/.test(t[2]));
pruef('S. 4: Fragen 9-18 und STOPP', /\n9\)/.test(t[3]) && /\n18\)/.test(t[3]) && /STOPP/.test(t[3]));
pruef('S. 5: Antwortbogen', /Antwortbogen/.test(t[4]));
const loes = (t[5].match(/^[A-E]$/gm) || []).join('');
pruef('S. 6: Loesungen stimmen mit der Auswertung ueberein', loes === erwartet, loes + ' / ' + erwartet);
pruef('PDF ohne Navigation und Artikeltext', !t.join(' ').includes('Wieso ist dieser Untertest') && !/Unterstützer:innen/.test(t.join(' ')));

await p.evaluate(() => window.dispatchEvent(new Event('afterprint')));
pruef('nach dem Druck aufgeraeumt', await p.evaluate(() => !document.body.classList.contains('fg-druckt')
  && !document.getElementById('ems-druck') && !document.getElementById('ems-druck-seite')));
pruef('keine JS-Fehler', js.length === 0, js.join(' | '));
console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
await b.close();
process.exit(fail ? 1 : 0);
