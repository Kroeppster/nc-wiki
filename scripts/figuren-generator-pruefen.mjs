/*
 * ============================================================================
 * PRUEFSTAND FUER DEN FIGUREN-GENERATOR (Alpha-Seite)
 * ============================================================================
 *   ~/bin/hugo --minify && (Server auf public/, Port 8123)
 *   node scripts/figuren-generator-pruefen.mjs
 *
 * Prueft einen Durchlauf des Generators auf /alpha/ und danach - in vielen
 * Wiederholungen - die einzige Eigenschaft, die man nur MESSEN kann:
 * ob sich zwei Buchstaben derselben Figur beruehren.
 *
 * WARUM DIE WIEDERHOLUNGEN. Der Generator wuerfelt jedes Mal neu. Ein
 * Bildschirmfoto zeigt genau einen Wurf; eine Schwaeche, die jede fuenfte
 * Figur trifft, kann darauf fehlen. Genau das ist passiert: Im ersten Entwurf
 * sass der Buchstabe im SCHWERPUNKT seines Feldes, und bei einem duennen,
 * gebogenen Streifen liegt der fast auf der Kante - gemessen ueberlappten 47
 * von 216 Figuren, auf dem ersten Foto sah man drei. Seit der Abstandskarte
 * (der Buchstabe steht an der Stelle, die am tiefsten im Feld steckt) sind es
 * null; steigt die Zahl wieder, ist dort etwas kaputtgegangen.
 *
 * ZWEI FALLEN:
 *  1. window.print() blockiert den Lauf - wird durch einen Zaehler ersetzt.
 *  2. Fuer einen zweiten Durchgang die Seite NEU LADEN. Waehrend ein
 *     Durchlauf laeuft, ist das Startformular ausgeblendet, und das Skript
 *     wartet dann 30 Sekunden auf ein Feld, das niemand sehen kann.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
const { chromium } = pw;
const ADRESSE = (process.env.ADRESSE || 'http://127.0.0.1:8123') + '/alpha/';
const RUNDEN = Number(process.env.RUNDEN || 12);
const b = await chromium.launch();
let ok = 0, fail = 0;
const pruef = (n, c, i = '') => { if (c) { ok++; console.log('  OK    ' + n); } else { fail++; console.log('  FEHLT ' + n + '  ' + i); } };
const ctx = await b.newContext({ viewport: { width: 1200, height: 1000 } });
await ctx.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });
const p = await ctx.newPage(); const js = [];
p.on('pageerror', e => { if (!/PagefindUI/.test(String(e.message))) js.push(String(e.message).slice(0, 120)); });
await p.addInitScript(() => { window.__gedruckt = 0; window.print = function () { window.__gedruckt++; }; });
await p.goto(ADRESSE, { waitUntil: 'networkidle' });

console.log('=== Ein Durchlauf ===');
pruef('Alpha-Seite erreichbar', (await p.title()).length > 0);
pruef('Generator vorhanden', !!(await p.$('#fig-wurzel')));

// Die Vorgabezeiten kommen aus data/testablauf.yaml. Die Pause ist die ECHTE
// Luecke zwischen Einpraegen und Reproduktion (Fakten einpraegen 6 +
// Textverstaendnis 45 = 51), nicht eine bequeme kurze Pause.
const vor = await p.evaluate(() => ({
  l: +document.getElementById('fig-min-lernen').value,
  p: +document.getElementById('fig-min-pause').value,
  a: +document.getElementById('fig-min-abfrage').value }));
pruef('Vorgabe: Einpraegen 4 Min', vor.l === 4, String(vor.l));
pruef('Vorgabe: Abfrage 5 Min', vor.a === 5, String(vor.a));
pruef('Vorgabe: echte Pause (51 Min)', vor.p === 51, String(vor.p));

await p.fill('#fig-min-lernen', '1'); await p.fill('#fig-min-pause', '0'); await p.fill('#fig-min-abfrage', '9');
await p.click('#fig-los'); await p.waitForTimeout(2500);
const lern = await p.evaluate(() => {
  // Nur das Raster - im Anleitungskasten darueber stehen zwei Beispielfiguren.
  const svgs = [...document.querySelectorAll('#fig-blatt-lernen .fig-raster .fig-svg')];
  return { anzahl: svgs.length,
    schwarzProFigur: svgs.map(s => [...s.querySelectorAll('path[fill="#000"]')].length),
    clipIds: new Set([...document.querySelectorAll('clipPath')].map(c => c.id)).size,
    clipGesamt: document.querySelectorAll('clipPath').length };
});
pruef('18 Figuren', lern.anzahl === 18, String(lern.anzahl));
pruef('je genau ein schwarzes Feld', lern.schwarzProFigur.every(n => n === 1), JSON.stringify([...new Set(lern.schwarzProFigur)]));
// Gleiche Clip-Kennung = der Clip der einen Figur greift auf die andere zu,
// und die Trennlinien ragen aus der Form heraus. Genau das war der erste Bug.
pruef('Clip-Kennungen eindeutig', lern.clipIds === lern.clipGesamt, `${lern.clipIds}/${lern.clipGesamt}`);
// Format wie im Testheft: Ueberschrift, Kasten mit Beispielfigur, STOPP.
const heft = await p.evaluate(() => {
  const b = document.getElementById('fig-blatt-lernen'), k = b.querySelector('.ems-kasten');
  const bsp = [...k.querySelectorAll('.fig-svg')];
  const schwarz = bsp[0] ? [...bsp[0].querySelectorAll('g > path[fill]')].findIndex(e => e.getAttribute('fill') === '#000') : -1;
  return { kopf: b.querySelector('.ems-kopf').textContent, beispiele: bsp.length, schwarz,
    buchstaben: bsp[1] ? [...bsp[1].querySelectorAll('text')].map(t => t.textContent).join('') : '',
    loesung: (k.textContent.match(/Lösung wäre dann \(([A-E])\)/) || [])[1], stopp: !!b.querySelector('.ems-marke-stopp') };
});
pruef('Ueberschrift wie im Heft', /Figuren lernen \(Einprägephase\)\s*Lernzeit: 1 Minute$/.test(heft.kopf), heft.kopf);
pruef('Anleitung mit Beispielfigur (schwarz) und abgefragter Fassung (A-E)', heft.beispiele === 2 && heft.schwarz >= 0 && heft.buchstaben === 'ABCDE', JSON.stringify(heft));
pruef('"Die Loesung waere dann (X)" nennt das schwarze Feld der Beispielfigur', heft.loesung === 'ABCDE'[heft.schwarz], JSON.stringify(heft));
pruef('STOPP am Ende', heft.stopp);

await p.click('#fig-fertig-lernen'); await p.waitForTimeout(800);
const ab = await p.evaluate(() => {
  const felder = [...document.querySelectorAll('#fig-blatt-abfrage .fig-feld')];
  return { anzahl: felder.length, nummern: felder.map(f => f.querySelector('.fig-nr').textContent).join(' '),
    buchstabenProFigur: felder.map(f => [...f.querySelectorAll('text')].map(t => t.textContent).join('')),
    wahl: felder.map(f => f.querySelectorAll('input[type=radio]').length),
    schwarz: [...document.querySelectorAll('#fig-blatt-abfrage path[fill="#000"]')].length };
});
pruef('18 Aufgaben', ab.anzahl === 18, String(ab.anzahl));
pruef('nummeriert 1) bis 18), zeilenweise', ab.nummern === Array.from({ length: 18 }, (_, i) => (i + 1) + ')').join(' '), ab.nummern);
pruef('jede Figur zeigt A-E', ab.buchstabenProFigur.every(s => s === 'ABCDE'), JSON.stringify([...new Set(ab.buchstabenProFigur)]).slice(0, 60));
pruef('je 5 Auswahlfelder', ab.wahl.every(n => n === 5), JSON.stringify([...new Set(ab.wahl)]));
// In der Abfrage darf nichts schwarz sein - sonst waere die Loesung zu sehen.
pruef('in der Abfrage ist NICHTS schwarz', ab.schwarz === 0, String(ab.schwarz));

await p.evaluate(() => { document.querySelectorAll('#fig-blatt-abfrage input[type=radio][value="0"]').forEach(r => { r.checked = true; }); });
await p.click('#fig-auswerten'); await p.waitForTimeout(700);
const erg = await p.evaluate(() => ({ text: document.getElementById('fig-punkte').textContent,
  richtig: document.querySelectorAll('#fig-blatt-loesung .fg-ist-richtig').length,
  buchstaben: [...document.querySelectorAll('#fig-blatt-loesung .fg-ist-richtig')].map(e => e.textContent.trim()[0]).join('') }));
pruef('Auswertung erscheint', /\d+\s*von\s*18/.test(erg.text), erg.text);
pruef('genau 18 Loesungen markiert', erg.richtig === 18, String(erg.richtig));

await p.click('#fig-drucken-ende'); await p.waitForTimeout(600);
const dr = await p.evaluate(() => { const d = document.getElementById('ems-druck');
  return { seiten: d.querySelectorAll('.ems-seite').length, svgs: d.querySelectorAll('.fig-svg').length,
    zellen: d.querySelectorAll('.ems-fl-zelle').length, bogen: d.querySelectorAll('.ems-bogen-zeile').length,
    loesungen: [...d.querySelectorAll('.ems-loesung b')].map(e => e.textContent).join('') }; });
pruef('Druck: sechs Heftseiten', dr.seiten === 6, String(dr.seiten));
pruef('Druck: 38 Figuren (2 Beispiele + 18 + 18) auf festen Plaetzen', dr.svgs === 38 && dr.zellen === 36, JSON.stringify(dr));
pruef('Druck: Antwortbogen mit 18 Zeilen', dr.bogen === 18, String(dr.bogen));
pruef('Druck: Loesungsblatt = Auswertung am Bildschirm', dr.loesungen === erg.buchstaben, dr.loesungen + ' / ' + erg.buchstaben);
await p.emulateMedia({ media: 'print' });
await p.pdf({ path: (process.env.ABLAGE || '/tmp') + '/figuren-set.pdf', preferCSSPageSize: true, printBackground: true });
await p.emulateMedia({ media: 'screen' });
{
  const { execSync } = await import('node:child_process');
  const info = JSON.parse(execSync('python3 -c "import pymupdf,json,sys;d=pymupdf.open(sys.argv[1]);print(json.dumps({\'masse\':[[round(s.rect.width),round(s.rect.height)] for s in d],\'texte\':[s.get_text() for s in d]}))" '
    + (process.env.ABLAGE || '/tmp') + '/figuren-set.pdf').toString());
  pruef('PDF: sechs A4-Seiten', info.masse.length === 6 && info.masse.every(m => m[0] === 595 && m[1] === 842), JSON.stringify(info.masse));
  pruef('PDF: Teil A Einpraegephase, Teil B Reproduktionsphase, Antwortbogen, Loesungen',
    /Testteil A/.test(info.texte[0]) && /Einprägephase/.test(info.texte[0]) && /STOPP/.test(info.texte[1])
    && /Testteil B/.test(info.texte[2]) && /Reproduktionsphase/.test(info.texte[2]) && /18\)/.test(info.texte[3])
    && /Antwortbogen/.test(info.texte[4]) && /Lösungen/.test(info.texte[5]));
}
await p.evaluate(() => window.dispatchEvent(new Event('afterprint')));

console.log(`\n=== Buchstaben-Abstaende ueber ${RUNDEN} Runden ===`);
let schlimmste = 0, faelle = 0, figuren = 0;
for (let runde = 0; runde < RUNDEN; runde++) {
  await p.reload({ waitUntil: 'networkidle' });
  await p.fill('#fig-min-lernen', '1'); await p.fill('#fig-min-pause', '0'); await p.fill('#fig-min-abfrage', '9');
  await p.click('#fig-los'); await p.waitForTimeout(400);
  await p.click('#fig-fertig-lernen'); await p.waitForTimeout(400);
  const r = await p.evaluate(() => {
    const raus = [];
    document.querySelectorAll('#fig-blatt-abfrage .fig-feld svg').forEach(svg => {
      const t = [...svg.querySelectorAll('text')].map(e => e.getBoundingClientRect());
      let max = 0;
      for (let a = 0; a < t.length; a++) for (let d = a + 1; d < t.length; d++) {
        const ux = Math.min(t[a].right, t[d].right) - Math.max(t[a].left, t[d].left);
        const uy = Math.min(t[a].bottom, t[d].bottom) - Math.max(t[a].top, t[d].top);
        if (ux > 0 && uy > 0) max = Math.max(max, Math.min(ux, uy));
      }
      raus.push(max);
    });
    return raus;
  });
  r.forEach(v => { figuren++; if (v > 0) { faelle++; schlimmste = Math.max(schlimmste, v); } });
}
console.log(`    ${figuren} Figuren, ${faelle} mit sich beruehrenden Buchstaben, groesste Ueberlappung ${schlimmste.toFixed(1)} px`);
pruef('keine sich beruehrenden Buchstaben', faelle === 0, `${faelle}/${figuren}`);
pruef('keine JS-Fehler', js.length === 0, js.join(' | '));
console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
await b.close();
process.exit(fail ? 1 : 0);
