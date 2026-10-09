/*
 * ============================================================================
 * PRUEFSTAND FUER «ANTWORTBOGEN AUSWERTEN» (Alpha-Seite)
 * ============================================================================
 *   ~/bin/hugo --minify && (Server auf public/, Port 8123)
 *   python3 scripts/antwortbogen-testbilder.py /tmp/ab     # braucht pymupdf pillow numpy
 *   node scripts/antwortbogen-pruefen.mjs /tmp/ab
 *
 * Laedt jedes Testbild in den Baustein auf /alpha/ und vergleicht, was
 * gelesen wurde, mit den Kreuzen, die antwortbogen-testbilder.py gesetzt
 * hat: ein sauberer Scan und mehrere «Handyfotos» (schraeg, gedreht,
 * kopfueber, quer, Bleistift, Schatten, JPG). Dazu zwei Bilder, die einen
 * Fehler ergeben muessen (Bogen zu klein, gar kein Bogen).
 *
 * Gezaehlt wird streng: Eine falsch gelesene Zeile, die NICHT als unsicher
 * markiert ist, ist ein Fehler - die sieht niemand nach. Eine unsichere
 * Zeile ist erlaubt (sie steht orange da und laesst sich korrigieren), aber
 * mehr als eine Handvoll je Bogen waere laestig.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const { chromium } = pw;
const ADRESSE = (process.env.ADRESSE || 'http://127.0.0.1:8123') + '/alpha/';
const ORDNER = process.argv[2] || '/tmp/ab';
const erwartet = JSON.parse(readFileSync(join(ORDNER, 'erwartet.json'), 'utf8'));
const MAX_UNSICHER = 6;
const b = await chromium.launch();
let ok = 0, fail = 0;
const pruef = (n, c, i = '') => { if (c) { ok++; console.log('  OK    ' + n); } else { fail++; console.log('  FEHLT ' + n + '  ' + String(i).slice(0, 300)); } };
const ctx = await b.newContext({ viewport: { width: 1200, height: 1000 } });
await ctx.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });
const p = await ctx.newPage(); const js = [];
p.on('pageerror', e => { if (!/PagefindUI/.test(String(e.message))) js.push(String(e.message).slice(0, 120)); });
await p.goto(ADRESSE, { waitUntil: 'networkidle' });
pruef('Baustein vorhanden', !!(await p.$('#ab-wurzel')));
const jahre = await p.$$eval('#ab-testsim option', o => o.map(x => x.value));
pruef('Testsimulationen 2022 bis 2026 waehlbar', ['2026', '2025', '2024', '2023', '2022'].every(j => jahre.includes(j)), jahre.join(','));
await p.selectOption('#ab-testsim', '2026');
const loesung = await p.evaluate(() => JSON.parse(document.getElementById('ab-daten').textContent)
  .testsimulationen.filter(t => t.jahr === 2026)[0].loesungen.join(''));

for (const [name, e] of Object.entries(erwartet)) {
  if (name.startsWith('_')) continue;
  console.log('\n=== ' + name + ' ===');
  await p.evaluate(() => { document.getElementById('ab-status').textContent = ''; document.getElementById('ab-ergebnis').hidden = true; });
  const t0 = Date.now();
  await p.setInputFiles('#ab-datei', join(ORDNER, name));
  await p.waitForFunction(() => !document.getElementById('ab-ergebnis').hidden
    || document.getElementById('ab-status').classList.contains('ab-fehler'), null, { timeout: 60000 });
  const zeit = Date.now() - t0;
  const r = await p.evaluate(() => ({
    fehler: document.getElementById('ab-status').classList.contains('ab-fehler') ? document.getElementById('ab-status').textContent : null,
    antworten: [...document.querySelectorAll('#ab-zeilen select[data-nr]')].map(s => s.value || '.').join(''),
    unsicher: [...document.querySelectorAll('#ab-zeilen tr')].map(z => z.classList.contains('ab-unsicher')).filter(Boolean).length,
    unsicherNr: [...document.querySelectorAll('#ab-zeilen tr.ab-unsicher select')].map(s => +s.dataset.nr),
    summe: document.getElementById('ab-summe').textContent,
    meldungen: document.getElementById('ab-meldungen').textContent }));
  if (e.fehler) { pruef('Fehlermeldung statt Ergebnis', !!r.fehler, JSON.stringify(r).slice(0, 200)); console.log('        ' + r.fehler); continue; }
  pruef('gelesen (' + zeit + ' ms)', !r.fehler, r.fehler);
  if (r.fehler) continue;
  const falsch = [];
  for (let i = 0; i < 144; i++) if (r.antworten[i] !== e.antworten[i] && !r.unsicherNr.includes(i)) falsch.push((i + 1) + ':' + e.antworten[i] + '->' + r.antworten[i]);
  pruef('keine falsch gelesene Zeile ohne Markierung', falsch.length === 0, falsch.join(' '));
  // Mehrere Kreuze in einer Zeile stehen immer als unsicher da (so will es
  // das Tool: zum Nachsehen). Gezaehlt werden nur die uebrigen.
  const unnoetig = r.unsicherNr.filter(n => !(e.antworten[n] === '*' && r.antworten[n] === '*'));
  pruef('hoechstens ' + MAX_UNSICHER + ' unnoetig unsichere Zeilen (' + unnoetig.length + ')', unnoetig.length <= MAX_UNSICHER,
    unnoetig.map(n => (n + 1) + ':' + e.antworten[n] + '/' + r.antworten[n]).join(' '));
  const soll = [...e.antworten].filter((a, i) => a === loesung[i]).length;
  const ist = +(r.summe.match(/\d+/) || [])[0];
  if (r.antworten === e.antworten) pruef('Punkte stimmen (' + soll + ')', ist === soll, r.summe);
  if (r.meldungen) console.log('        Hinweise: ' + r.meldungen);
}

// Korrigieren: eine Antwort von Hand aendern rechnet die Punkte neu
console.log('\n=== Korrigieren ===');
{
  await p.setInputFiles('#ab-datei', join(ORDNER, 'scan.png'));
  await p.waitForFunction(() => !document.getElementById('ab-ergebnis').hidden, null, { timeout: 60000 });
  const vorher = +(await p.textContent('#ab-summe')).match(/\d+/)[0];
  const nr = await p.evaluate(l => { const s = [...document.querySelectorAll('#ab-zeilen select[data-nr]')]
    .find(s => s.value !== l[+s.dataset.nr]); return s ? +s.dataset.nr : -1; }, loesung);
  await p.selectOption(`#ab-zeilen select[data-nr="${nr}"]`, loesung[nr]);
  const nachher = +(await p.textContent('#ab-summe')).match(/\d+/)[0];
  pruef('Antwort korrigiert -> ein Punkt mehr', nachher === vorher + 1, vorher + ' -> ' + nachher);
}
// Eigener Loesungsschluessel (wie aus dem Tool): erst der Bogen, dann der
// Schluessel; Aufgaben ohne Loesung zaehlen nicht mit.
console.log('\n=== Eigener Loesungsschluessel ===');
{
  const sch = erwartet._schluessel, scan = erwartet['scan.png'].antworten;
  const mit = [...sch.loesungen].filter(l => l !== '.').length;
  const soll = [...scan].filter((a, i) => a === sch.loesungen[i]).length;
  await p.selectOption('#ab-testsim', 'eigen');
  pruef('Feld fuer den Schluessel erscheint', await p.isVisible('#ab-schluessel'));
  await p.setInputFiles('#ab-datei', join(ORDNER, 'scan.png'));
  await p.waitForFunction(() => /Lösungsschlüssel/.test(document.getElementById('ab-status').textContent), null, { timeout: 60000 });
  pruef('ohne Schluessel: Bogen gelesen, Hinweis statt Ergebnis', await p.evaluate(() => document.getElementById('ab-ergebnis').hidden));
  for (const datei of sch.dateien) {
    await p.evaluate(() => { document.getElementById('ab-schluessel-status').textContent = ''; });
    await p.setInputFiles('#ab-schluessel-datei', join(ORDNER, datei));
    await p.waitForFunction(() => /\d/.test(document.getElementById('ab-schluessel-status').textContent)
      || document.getElementById('ab-schluessel-status').classList.contains('ab-fehler'), null, { timeout: 60000 });
    const st = await p.textContent('#ab-schluessel-status');
    pruef(datei + ': ' + mit + ' Aufgaben mit Loesung erkannt', st.includes(String(mit)) && !/nicht eindeutig/.test(st), st);
    const summe = await p.textContent('#ab-summe');
    pruef(datei + ': Punkte ' + soll + ' von ' + mit, summe.startsWith(soll + ' ') && summe.includes(' ' + mit + ' '), summe);
  }
  const ohne = await p.$$eval('#ab-zeilen tr.ab-ohne', z => z.length);
  pruef('Aufgaben ohne Loesung als solche markiert (' + (144 - mit) + ')', ohne === 144 - mit, String(ohne));
  await p.setInputFiles('#ab-schluessel-datei', join(ORDNER, 'kein-bogen.png'));
  await p.waitForFunction(() => document.getElementById('ab-schluessel-status').classList.contains('ab-fehler'), null, { timeout: 60000 });
  pruef('kein Schluessel im Bild -> Meldung', true);
  await p.selectOption('#ab-testsim', '2026');
  pruef('zurueck auf 2026: Feld fuer den Schluessel weg', !(await p.isVisible('#ab-schluessel')));
}
// Live-Kamera: Chromium spielt ein Video als Kamera ab (erst leerer Tisch,
// dann der Bogen). Erwartet: zuerst der Hinweis auf die fehlenden Ecken,
// dann loest die Seite selbst aus und liest den Bogen richtig.
console.log('\n=== Live-Kamera ===');
if (erwartet._kamera) {
  const kb = await chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
    '--use-file-for-fake-video-capture=' + join(ORDNER, erwartet._kamera.datei)] });
  const kc = await kb.newContext({ viewport: { width: 420, height: 900 }, permissions: ['camera'] });
  await kc.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });
  const kp = await kc.newPage();
  kp.on('pageerror', e => { if (!/PagefindUI/.test(String(e.message))) js.push(String(e.message).slice(0, 120)); });
  await kp.goto(ADRESSE, { waitUntil: 'networkidle' });
  pruef('Knopf «Live-Kamera» sichtbar', await kp.isVisible('#ab-live'));
  await kp.selectOption('#ab-testsim', '2026');
  await kp.click('#ab-live');
  const hinweise = new Set();
  for (let i = 0; i < 150; i++) {
    await kp.waitForTimeout(100);
    const h = await kp.evaluate(() => { const e = document.querySelector('.bl-kamera-hinweis'); return e ? e.textContent : null; });
    if (h) hinweise.add(h);
    if (!(await kp.evaluate(() => document.getElementById('ab-ergebnis').hidden))) break;
  }
  const liste = [...hinweise].join(' | ');
  pruef('Sucher meldet erst fehlende Ecken, dann «ruhig halten»', /0 von 4/.test(liste) && /ruhig/.test(liste), liste);
  const gelesen = await kp.evaluate(() => [...document.querySelectorAll('#ab-zeilen select[data-nr]')].map(s => s.value || '.').join(''));
  const unsicherNr = await kp.evaluate(() => [...document.querySelectorAll('#ab-zeilen tr.ab-unsicher select')].map(s => +s.dataset.nr));
  const soll = erwartet._kamera.antworten;
  const falsch = [];
  for (let i = 0; i < 144; i++) if (gelesen[i] !== soll[i] && !unsicherNr.includes(i)) falsch.push((i + 1) + ':' + soll[i] + '->' + gelesen[i]);
  pruef('selbst ausgeloest und richtig gelesen', gelesen.length === 144 && falsch.length === 0, gelesen.length + ' ' + falsch.join(' '));
  pruef('Kamera danach wieder aus', await kp.evaluate(() => document.getElementById('ab-kamera-feld').hidden));
  await kb.close();
}
pruef('keine JS-Fehler', js.length === 0, js.join(' | '));
console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
await b.close();
process.exit(fail ? 1 : 0);
