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
 * das Korrigieren durch Tippen; dazu ein eigener Konztest aus PDF (Aufgabe
 * und Loesung hochladen): Der Browser muss dasselbe lesen wie
 * scripts/konztest-loesungen.py. Aus dem Repo-Ordner starten (liest die PDFs
 * unter assets/downloads/).
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
const ziele = await p.evaluate(() => JSON.parse(document.getElementById('kt-daten').textContent).konztests[0].ziele.join(''));
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
  pruef('selbst ausgeloest und richtig gelesen', r && falsch.length === 0, r ? falsch.length + ' falsch' : 'kein Ergebnis: ' + await kp.evaluate(() => document.getElementById('kt-status').textContent));
  await kb.close();
}
// Eigener Konztest: Aufgabe und Loesung als PDF hochladen. Der Browser muss
// dasselbe lesen wie scripts/konztest-loesungen.py (data/konztest.yaml).
console.log('\n=== Eigener Konztest aus PDF (wie das Skript?) ===');
{
  const UE = 'assets/downloads/uebungsaufgaben/konzentriertes-arbeiten/', TS = 'assets/downloads/testsimulationen/';
  const faelle = [
    ['s2025-07', [UE + '2025_konzentriertes-arbeiten_S07.pdf']],
    ['s2024-02', [UE + '2024_konzentriertes-arbeiten_S02.pdf']],
    ['s2025-04', [UE + '2025_konzentriertes-arbeiten_S04.pdf']],
    ['s2025-12', [UE + '2025_konzentriertes-arbeiten_S12.pdf']],
    ['ts2026', [TS + '2026_testsimulationen_Testsimulation.pdf', TS + '2026_testsimulationen_Loesung.pdf']],
  ];
  const eb = await chromium.launch();
  const ec = await eb.newContext({ viewport: { width: 1200, height: 1000 } });
  await vorbereiten(ec);
  const ep = await ec.newPage(); fehlerSammeln(ep);
  await ep.goto(ADRESSE, { waitUntil: 'networkidle' });
  // was das Skript gelesen hat: data/konztest.yaml, so wie es in der Seite steht
  const daten = await ep.evaluate(() => JSON.parse(document.getElementById('kt-daten').textContent));
  await ep.selectOption('#kt-testsim', 'eigen');
  pruef('Feld fuer eigenen Konztest sichtbar', await ep.isVisible('#kt-eigen-datei') || !(await ep.evaluate(() => document.getElementById('kt-eigen').hidden)));
  for (const [id, dateien] of faelle) {
    const soll = daten.konztests.find(k => k.id === id);
    await ep.evaluate(() => { localStorage.removeItem('ncwiki-kt-eigen'); document.getElementById('kt-eigen-status').textContent = ''; });
    const t0 = Date.now();
    await ep.setInputFiles('#kt-eigen-datei', dateien);
    await ep.waitForFunction(() => /\(/.test(document.getElementById('kt-eigen-status').textContent) && !/…/.test(document.getElementById('kt-eigen-status').textContent)
      || document.getElementById('kt-eigen-status').classList.contains('ab-fehler'), null, { timeout: 300000 });
    const k = await ep.evaluate(() => JSON.parse(localStorage.getItem('ncwiki-kt-eigen')));
    if (!k) { pruef(id + ': gelesen', false, await ep.evaluate(() => document.getElementById('kt-eigen-status').textContent)); continue; }
    const lage = Math.max(...k.x.map((v, i) => Math.abs(v - soll.x[i])), ...k.y.map((v, i) => Math.abs(v - soll.y[i])));
    // Die Klassen muessen nicht gleich heissen und nicht gleich fein sein
    // (pdf.js zeichnet anders als MuPDF). Pruefstein ist die Regel: Alle
    // Regeln haengen nur vom Zeichen und seinem Nachbarn ab - fasst der
    // Browser zwei verschiedene Zeichen zusammen, widersprechen sich Paare.
    const regel = (Z, ziele) => Math.min(...[1, -1, 0].map(nb => { const je = new Map();
      for (let R = 0; R < 40; R++) for (let C = 0; C < 40; C++) { const n = C + nb >= 0 && C + nb < 40 ? Z[R][C + nb] : '-', key = Z[R][C] + n;
        if (!je.has(key)) je.set(key, [0, 0]); je.get(key)[+ziele[R][C]]++; }
      let w = 0; for (const v of je.values()) w += Math.min(...v); return w; }));
    const wJs = regel(k.zeichen, k.ziele), wPy = regel(soll.zeichen, soll.ziele), arten = new Set(k.zeichen.join('')).size;
    const zf = [...Array(1600).keys()].filter(i => k.ziele.join('')[i] !== soll.ziele.join('')[i]).length;
    pruef(id + ': wie das Skript (Lage ' + lage.toFixed(2) + ' pt, ' + arten + ' Zeichenarten, Regelprobe ' + wJs + ' (Skript ' + wPy + '), '
      + zf + ' Ziele anders, ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s)', lage < 1 && zf === 0 && wJs <= wPy + 5);
  }
  // Mit dem zuletzt gelesenen eigenen Konztest (2026 aus dem PDF) ein Foto auswerten
  await ep.setInputFiles('#kt-datei', join(ORDNER, 'foto-schraeg.jpg'));
  await ep.waitForFunction(() => !document.getElementById('kt-ergebnis').hidden || document.getElementById('kt-status').classList.contains('ab-fehler'), null, { timeout: 120000 });
  const re = await lesen(ep), se = erwartet['foto-schraeg.jpg'].markiert;
  const fe = re ? [...Array(1600).keys()].filter(i => re.markiert[i] !== se[i] && !re.unsicher.includes(i)).length : -1;
  pruef('eigener Konztest: Foto richtig gelesen', fe === 0, re ? fe + ' falsch' : await ep.evaluate(() => document.getElementById('kt-status').textContent));
  await eb.close();
}
pruef('keine JS-Fehler', js.length === 0, js.join(' | '));
console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
process.exit(fail ? 1 : 0);
