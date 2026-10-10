/*
 * ============================================================================
 * PRUEFSTAND FUER «KONZTEST AUSWERTEN» (Alpha-Seite)
 * ============================================================================
 *   ~/bin/hugo --minify && (Server auf public/, Port 8123)
 *   python3 scripts/konztest-testbilder.py /tmp/kt     # braucht pymupdf pillow numpy pyyaml
 *   node scripts/konztest-pruefen.mjs /tmp/kt
 *
 * Laedt jedes Testbild in den Baustein auf /alpha/ und vergleicht die
 * gelesenen Markierungen mit denen, die konztest-testbilder.py gesetzt hat
 * (Scan, schraeg, kopfueber, quer, Bleistift), dazu ein Bild ohne Konztest
 * (muss eine Meldung ergeben), die Live-Kamera (Chromiums Fake-Kamera) und
 * das Korrigieren durch Tippen.
 *
 * Gezaehlt wird streng: Ein falsch gelesenes Zeichen, das NICHT als unsicher
 * markiert ist, ist ein Fehler. Unsichere Zeichen sind erlaubt (sie stehen
 * orange da), aber hoechstens eine Handvoll je Blatt.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const { chromium } = pw;
const ADRESSE = (process.env.ADRESSE || 'http://127.0.0.1:8123') + '/alpha/';
const ORDNER = process.argv[2] || '/tmp/kt';
const erwartet = JSON.parse(readFileSync(join(ORDNER, 'erwartet.json'), 'utf8'));
const MAX_UNSICHER = 8;
let ok = 0, fail = 0;
const pruef = (n, c, i = '') => { if (c) { ok++; console.log('  OK    ' + n); } else { fail++; console.log('  FEHLT ' + n + '  ' + String(i).slice(0, 300)); } };
const js = [];
const fehlerSammeln = p => p.on('pageerror', e => { if (!/PagefindUI/.test(String(e.message))) js.push(String(e.message).slice(0, 160)); });
const vorbereiten = ctx => ctx.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });

// Was die Seite gelesen hat: die Markierungen stehen nur im Bild (Kreise),
// deshalb liest der Test den Zustand des Bausteins (NCWikiKonztestStand).
const lesen = p => p.evaluate(() => {
  const st = window.NCWikiKonztestStand && window.NCWikiKonztestStand();
  return st ? { markiert: st.markiert.map(z => z.map(m => m ? '1' : '0').join('')).join(''),
    unsicher: st.unsicher.map((u, i) => u ? i : -1).filter(i => i >= 0), summe: document.getElementById('kt-summe').textContent } : null;
});
function wertung(markiert, ziele) {
  let letztes = -1; for (let i = 0; i < 1600; i++) if (markiert[i] === '1') letztes = i;
  let r = 0, f = 0, a = 0;
  for (let i = 0; i < 1600; i++) { const m = markiert[i] === '1', z = ziele[i] === '1'; if (m && z) r++; else if (m) f++; else if (z && i < letztes) a++; }
  return r - f - a;
}

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1200, height: 1000 } });
await vorbereiten(ctx);
const p = await ctx.newPage(); fehlerSammeln(p);
await p.goto(ADRESSE, { waitUntil: 'networkidle' });
pruef('Baustein vorhanden', !!(await p.$('#kt-wurzel')));
const ziele = await p.evaluate(() => JSON.parse(document.getElementById('kt-daten').textContent).testsimulationen[0].ziele.join(''));
pruef('Loesung: 400 Zielzeichen, 10 je Zeile', ziele.split('').filter(c => c === '1').length === 400);

for (const [name, e] of Object.entries(erwartet)) {
  if (name.startsWith('_')) continue;
  console.log('\n=== ' + name + ' ===');
  await p.evaluate(() => { document.getElementById('kt-status').textContent = ''; document.getElementById('kt-status').className = 'ab-status'; document.getElementById('kt-ergebnis').hidden = true; });
  const t0 = Date.now();
  await p.setInputFiles('#kt-datei', join(ORDNER, name));
  await p.waitForFunction(() => !document.getElementById('kt-ergebnis').hidden
    || document.getElementById('kt-status').classList.contains('ab-fehler'), null, { timeout: 120000 });
  const zeit = Date.now() - t0;
  const fehler = await p.evaluate(() => document.getElementById('kt-status').classList.contains('ab-fehler') ? document.getElementById('kt-status').textContent : null);
  if (e.fehler) { pruef('Meldung statt Ergebnis', !!fehler, ''); console.log('        ' + fehler); continue; }
  pruef('gelesen (' + zeit + ' ms)', !fehler, fehler);
  if (fehler) continue;
  const r = await lesen(p);
  const falsch = [];
  for (let i = 0; i < 1600; i++) if (r.markiert[i] !== e.markiert[i] && !r.unsicher.includes(i)) falsch.push('Z' + (Math.floor(i / 40) + 1) + '/' + (i % 40 + 1) + ':' + e.markiert[i] + '->' + r.markiert[i]);
  pruef('keine falsch gelesene Markierung ohne Hinweis', falsch.length === 0, falsch.length + ': ' + falsch.slice(0, 12).join(' '));
  pruef('hoechstens ' + MAX_UNSICHER + ' unsichere Zeichen (' + r.unsicher.length + ')', r.unsicher.length <= MAX_UNSICHER);
  const soll = wertung(e.markiert, ziele);
  if (r.markiert === e.markiert) pruef('Rohwert stimmt (' + soll + ')', r.summe.includes(' ' + soll + ' '), r.summe);
}

console.log('\n=== Korrigieren durch Tippen ===');
{
  await p.setInputFiles('#kt-datei', join(ORDNER, 'scan.png'));
  await p.waitForFunction(() => !document.getElementById('kt-ergebnis').hidden, null, { timeout: 120000 });
  const vorher = await lesen(p);
  // Ein ausgelassenes Zielzeichen (vor dem letzten markierten) antippen:
  // eins mehr richtig, eins weniger ausgelassen -> Rohwert +2
  const letztes = vorher.markiert.lastIndexOf('1');
  const i = [...Array(letztes).keys()].find(k => ziele[k] === '1' && vorher.markiert[k] === '0');
  if (i === undefined) pruef('ausgelassenes Zielzeichen zum Antippen gefunden', false);
  else {
    // Das Ergebnis rollt weich ins Bild: erst warten, sonst trifft der Klick
    // ein Nachbarzeichen
    await p.waitForTimeout(1200);
    await p.locator('#kt-bild').scrollIntoViewIfNeeded();
    const pos = await p.evaluate(k => window.NCWikiKonztestPunkt(Math.floor(k / 40), k % 40), i);
    const box = await p.locator('#kt-bild').boundingBox();
    await p.mouse.click(box.x + pos[0] * box.width, box.y + pos[1] * box.height);
    const nachher = await lesen(p);
    const n = s => +(s.match(/-?\d+/) || [])[0];
    pruef('angetippt -> markiert, Rohwert +2', nachher.markiert[i] === '1' && n(nachher.summe) === n(vorher.summe) + 2, vorher.summe + ' -> ' + nachher.summe);
  }
}
await b.close();

console.log('\n=== Live-Kamera ===');
if (erwartet._kamera) {
  const kb = await chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
    '--use-file-for-fake-video-capture=' + join(ORDNER, erwartet._kamera.datei)] });
  const kc = await kb.newContext({ viewport: { width: 420, height: 900 }, permissions: ['camera'] });
  await vorbereiten(kc);
  const kp = await kc.newPage(); fehlerSammeln(kp);
  await kp.goto(ADRESSE, { waitUntil: 'networkidle' });
  pruef('Knopf «Live-Kamera» sichtbar', await kp.isVisible('#kt-live'));
  await kp.click('#kt-live');
  const hinweise = new Set();
  for (let i = 0; i < 300; i++) {
    await kp.waitForTimeout(100);
    const h = await kp.evaluate(() => { const e = document.querySelector('#kt-kamera-feld .bl-kamera-hinweis'); return e ? e.textContent : null; });
    if (h) hinweise.add(h);
    if (!(await kp.evaluate(() => document.getElementById('kt-ergebnis').hidden))) break;
  }
  const liste = [...hinweise].join(' | ');
  pruef('Sucher meldet erst das fehlende Raster, dann «ruhig halten»', /Rasters/.test(liste) && /ruhig/.test(liste), liste);
  const r = await lesen(kp);
  const soll = erwartet._kamera.markiert;
  const falsch = r ? [...Array(1600).keys()].filter(i => r.markiert[i] !== soll[i] && !r.unsicher.includes(i)) : null;
  pruef('selbst ausgeloest und richtig gelesen', r && falsch.length === 0, r ? falsch.length + ' falsch' : 'kein Ergebnis');
  await kb.close();
}
pruef('keine JS-Fehler', js.length === 0, js.join(' | '));
console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
process.exit(fail ? 1 : 0);
