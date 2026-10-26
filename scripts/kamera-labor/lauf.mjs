/*
 * KAMERA-LABOR: EIN LAUF
 * ======================
 * Spielt ein von szene.py erzeugtes Video als Handykamera in Chromium ab,
 * öffnet die Alpha-Seite (Antwortbogen auswerten / Konzentrationstest
 * auswerten), startet «Live-Kamera» und vergleicht das Gelesene mit der
 * Wahrheit (wahrheit.json).
 *
 *   node lauf.mjs --szene ORDNER [--port 8141] [--sprache de|fr|it]
 *        [--weg foto|stapel|stapel1] [--ausloesen auto|manuell:SEK] [--timeout 45]
 *        [--hochladen] [--nurhochladen [--bilddatei BILD]] [--quelle] [--site ORDNER]
 *        [--out ergebnis.json] [--bild]
 *
 *   --weg foto     Android-Weg: ImageCapture.takePhoto (Standard)
 *         stapel   iPhone-Weg: kein ImageCapture, 5 Videobilder mitteln
 *         stapel1  wie stapel, aber nur ein Bild (ältere Fassung)
 *   --ausloesen manuell:SEK  nach SEK Sekunden selbst auf «Auslösen» drücken,
 *                falls die Seite bis dahin nicht selbst ausgelöst hat
 *   --hochladen    zusätzlich standbild.jpg über «Datei wählen» auswerten
 *   --nurhochladen ohne Live-Kamera nur das Standbild (oder --bilddatei) auswerten
 *   --quelle       das Bild, das die Auswertung wirklich gelesen hat, als quelle.png
 *   --bild         das ausgewertete Bild der Seite als ergebnis-bild.png ablegen
 *   --site         die gebaute Website (Standard: public/ im Repo)
 *
 * Gezählt wird wie in scripts/antwortbogen-pruefen.mjs / konztest-pruefen.mjs:
 * falsch_ohne_hinweis = falsch gelesen und NICHT orange markiert (der Fehler,
 * den niemand sieht); unsicher = orange markiert (darf sein, aber wenige).
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { createServer } from 'node:http';
import { readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HIER = dirname(fileURLToPath(import.meta.url));
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i < 0 ? d : (process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[i + 1] : true); };
const SZENE = arg('szene');
if (!SZENE) { console.error('--szene ORDNER fehlt'); process.exit(2); }
const PORT = +arg('port', 8141);
const SPRACHE = arg('sprache', 'de');
const WEG = arg('weg', 'foto');
const AUSL = String(arg('ausloesen', 'auto'));
const TIMEOUT = +arg('timeout', 45) * 1000;
const SITE = arg('site', join(HIER, '..', '..', 'public'));   // die gebaute Website (hugo --minify)
const OUT = arg('out', join(SZENE, 'ergebnis.json'));
const w = JSON.parse(readFileSync(join(SZENE, 'wahrheit.json'), 'utf8'));
const video = join(SZENE, existsSync(join(SZENE, 'video.mjpeg')) ? 'video.mjpeg' : 'video.y4m');

// --- kleiner Webserver für die eingefrorene Website ---------------------------
const TYP = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.mp3': 'audio/mpeg', '.pdf': 'application/pdf', '.wasm': 'application/wasm',
  '.ico': 'image/x-icon', '.xml': 'application/xml', '.txt': 'text/plain', '.mjpeg': 'video/x-motion-jpeg' };
const server = createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  let f = join(SITE, p);
  if (!f.startsWith(SITE)) { res.writeHead(403); return res.end(); }
  try { if (statSync(f).isDirectory()) f = join(f, 'index.html'); } catch (e) {}
  if (!existsSync(f)) { res.writeHead(404); return res.end('404'); }
  res.writeHead(200, { 'Content-Type': TYP[extname(f)] || 'application/octet-stream' });
  res.end(readFileSync(f));
});
await new Promise((ok, f) => { server.once('error', f); server.listen(PORT, '127.0.0.1', ok); });

const { chromium } = pw;
const b = await chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
  '--use-file-for-fake-video-capture=' + video] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
  permissions: ['camera'], locale: { de: 'de-CH', fr: 'fr-CH', it: 'it-CH' }[SPRACHE] });
await ctx.addInitScript(([weg]) => {
  try { for (const [k, v] of [['alpha-notice-seen', '1'], ['cookie-consent', 'accepted']]) localStorage.setItem(k, v); } catch (e) {}
  if (weg !== 'foto') { try { delete window.ImageCapture; } catch (e) {} window.ImageCapture = undefined; }
  if (weg === 'stapel1') window.NCWikiKameraStapel = 1;
  // Das Bild festhalten, das die Auswertung wirklich liest (bildAus)
  let nb;
  Object.defineProperty(window, 'NCWikiBild', { configurable: true, get() { return nb; }, set(v) {
    const orig = v.bildAus;
    v.bildAus = function (q) { const b = orig.apply(this, arguments); (window.__quellen = window.__quellen || []).push(b.leinwand); return b; };
    nb = v; } });
}, [WEG]);
const p = await ctx.newPage();
const jsFehler = [];
p.on('pageerror', e => { if (!/PagefindUI/.test(String(e.message))) jsFehler.push(String(e.message).slice(0, 200)); });
p.on('console', m => { if (m.type() === 'error' && !/favicon|404|pagefind|ERR_TUNNEL|ERR_PROXY|ERR_NAME/i.test(m.text())) jsFehler.push('console: ' + m.text().slice(0, 200)); });
const praefix = SPRACHE === 'de' ? '' : '/' + SPRACHE;
await p.goto(`http://127.0.0.1:${PORT}${praefix}/alpha/`, { waitUntil: 'networkidle' });
await p.evaluate(() => { for (const s of ['#alphaNoticeBackdrop', '.alpha-notice', '.cookie-banner', '#cookieBanner']) document.querySelectorAll(s).forEach(e => e.remove()); });

const AB = w.art === 'antwortbogen';
const P = AB ? 'ab' : 'kt';
await p.selectOption('#' + P + '-testsim', AB ? String(w.jahr) : w.konztest);
await p.waitForTimeout(300);
// die Lösungen so, wie sie in der Seite stehen (data/antwortbogen.yaml)
const LOESUNGEN = AB ? await p.evaluate(j => JSON.parse(document.getElementById('ab-daten').textContent)
  .testsimulationen.filter(t => t.jahr === j)[0].loesungen.join(''), w.jahr) : null;

async function ergebnisLesen() {
  return p.evaluate(([AB, P]) => {
    const st = document.getElementById(P + '-status');
    const r = { fehler: st.classList.contains('ab-fehler') ? st.textContent : null, status: st.textContent,
      summe: (document.getElementById(P + '-summe') || {}).textContent || '',
      meldungen: [...document.querySelectorAll('#' + P + '-meldungen li')].map(l => l.textContent) };
    if (AB) {
      r.antworten = [...document.querySelectorAll('#ab-zeilen select[data-nr]')].map(s => s.value || '.').join('');
      r.unsicherNr = [...document.querySelectorAll('#ab-zeilen tr.ab-unsicher select')].map(s => +s.dataset.nr);
    } else {
      const s = window.NCWikiKonztestStand && window.NCWikiKonztestStand();
      if (s) {
        r.markiert = s.markiert.map(z => z.map(m => m ? '1' : '0').join('')).join('');
        r.unsicherNr = s.unsicher.map((u, i) => u ? i : -1).filter(i => i >= 0);
      }
    }
    return r;
  }, [AB, P]);
}
const fertig = () => p.evaluate(P => !document.getElementById(P + '-ergebnis').hidden
  || document.getElementById(P + '-status').classList.contains('ab-fehler'), P);

// Markierungen, die kein schraeger Strich sind (Vorgabe Oktober 2026): Ein
// Strich muss erkannt werden. Kreuz, Ausmalen und Kreis werden nicht eigens
// gefiltert - gelesen oder leer, beides richtig; dass ein Kreis ein
// Nachbarzeichen oder -kaestchen markiert erscheinen laesst, wird hingenommen
// (kreis_nachbar). Andere Stile (Haken, kurz, Unterstrich ...) sind nicht
// festgelegt: Abweichungen stehen gesondert in stil_offen, nicht als Fehler.
const STILE = w.stile || {}, DARF = ['kreuz', 'ausmalen', 'kreis'];
const stil = i => STILE[String(i)];
function bewerten(r) {
  const aus = {};
  if (r.fehler) { aus.ergebnis = 'fehler'; aus.fehlertext = r.fehler; return aus; }
  if (AB) {
    if (!r.antworten || r.antworten.length !== 144) { aus.ergebnis = 'kein_ergebnis'; return aus; }
    const radiert = w.radiert || [], soll = w.antworten;
    const falsch = [], falschMit = [], unnoetig = [], offen = [], kreisNachbar = [];
    for (let i = 0; i < 144; i++) {
      const u = r.unsicherNr.includes(i), s = stil(i), ist = r.antworten[i], text = (i + 1) + ':' + soll[i] + '->' + ist + (s ? ' (' + s + ')' : '');
      if (ist === soll[i]) { if (u && !(soll[i] === '*') && !radiert.includes(i)) unnoetig.push((i + 1) + ':' + soll[i]); continue; }
      if (DARF.includes(s) && ist === '.') continue;                                   // Kreuz, Ausmalen, Kreis: gelesen oder leer
      if (s === 'kreis') { kreisNachbar.push(text); continue; }                          // Kreis ragt ins Nachbarkaestchen
      if (s && !DARF.includes(s)) { offen.push(text); continue; }                        // nicht festgelegt
      (u ? falschMit : falsch).push(text);
    }
    const loes = LOESUNGEN;
    aus.punkte_soll = [...soll].filter((a, i) => a === loes[i] && 'ABCDE'.includes(a)).length;
    aus.punkte_ist = +((r.summe.match(/\d+/) || [])[0]);
    Object.assign(aus, { falsch_ohne_hinweis: falsch, falsch_mit_hinweis: falschMit, unnoetig_unsicher: unnoetig,
      unsicher: r.unsicherNr.length, stil_offen: offen, kreis_nachbar: kreisNachbar });
    aus.ergebnis = falsch.length ? 'FALSCH' : (unnoetig.length + falschMit.length > 6 ? 'zu_viele_unsicher' : 'ok');
  } else {
    if (!r.markiert) { aus.ergebnis = 'kein_ergebnis'; return aus; }
    const soll = w.markiert, falsch = [], falschMit = [], offen = [], kreisNachbar = [];
    const kreise = Object.keys(STILE).filter(k => STILE[k] === 'kreis').map(Number);
    for (let i = 0; i < 1600; i++) {
      const ist = r.markiert[i], s = stil(i);
      if (ist === soll[i]) continue;
      const text = i + ':' + soll[i] + '->' + ist + (s ? ' (' + s + ')' : '');
      if (DARF.includes(s)) continue;                                                     // Kreuz, Ausmalen, Kreis: gelesen oder leer
      if (ist === '1' && kreise.some(k => k !== i && Math.abs(Math.floor(k / 40) - Math.floor(i / 40)) <= 1 && Math.abs(k % 40 - i % 40) <= 1)) { kreisNachbar.push(text); continue; }
      if (s) { offen.push(text); continue; }                                              // nicht festgelegt
      (r.unsicherNr.includes(i) ? falschMit : falsch).push(text);
    }
    const wert = m => { let l = -1; for (let i = 0; i < 1600; i++) if (m[i] === '1') l = i;
      let a = 0, f = 0, x = 0; for (let i = 0; i < 1600; i++) { const mm = m[i] === '1', z = w.ziele[i] === '1'; if (mm && z) a++; else if (mm) f++; else if (z && i < l) x++; } return a - f - x; };
    Object.assign(aus, { falsch_ohne_hinweis: falsch, falsch_mit_hinweis: falschMit, unsicher: r.unsicherNr.length, stil_offen: offen, kreis_nachbar: kreisNachbar,
      rohwert_soll: wert(soll), rohwert_ist_gelesen: wert(r.markiert), summe_text: r.summe });
    aus.ergebnis = falsch.length ? 'FALSCH' : (r.unsicherNr.length > 8 ? 'zu_viele_unsicher' : 'ok');
  }
  return aus;
}

// --- Live-Kamera ------------------------------------------------------------------
// --nurhochladen: ohne Live-Kamera, nur das Standbild (oder --bilddatei) hochladen
const NUR = !!arg('nurhochladen');
await p.evaluate(() => { window.__quellen = []; });
const t0 = Date.now();
if (!NUR) await p.click('#' + P + '-live');
const hinweise = [];
let ausgeloest = null, manuell = false, letzter = null;
const manuellNach = AUSL.startsWith('manuell:') ? +AUSL.split(':')[1] * 1000 : null;
let ende = null;
while (!NUR && Date.now() - t0 < TIMEOUT) {
  await p.waitForTimeout(100);
  const h = await p.evaluate(P => { const e = document.querySelector('#' + P + '-kamera-feld .bl-kamera-hinweis'); return e ? e.textContent : null; }, P);
  const t = Date.now() - t0;
  if (h && h !== letzter) { hinweise.push([+(t / 1000).toFixed(1), h]); letzter = h; }
  if (h && /^(Aufnahme|Prise de vue|Scatto) /.test(h) && ausgeloest === null) ausgeloest = t;
  if (await fertig()) { ende = t; break; }
  if (manuellNach !== null && t > manuellNach && ausgeloest === null && !manuell) {
    manuell = true; ausgeloest = t;
    await p.click('#' + P + '-kamera-feld .bl-kamera-knoepfe button >> nth=0').catch(() => {});
  }
}
let r = await ergebnisLesen();
const live = { ...bewerten(r), dauer_s: ende ? +(ende / 1000).toFixed(1) : null, ausgeloest_s: ausgeloest ? +(ausgeloest / 1000).toFixed(1) : null,
  ausloeser: manuell ? 'manuell' : (ausgeloest !== null || ende ? 'auto' : 'nie'), hinweise,
  stapel: await p.evaluate(() => window.NCWikiKameraStapelInfo || null), meldungen: r.meldungen, summe: r.summe };
if (!ende) live.ergebnis = live.ergebnis === 'kein_ergebnis' || !live.ergebnis ? 'timeout' : live.ergebnis;
if (NUR) { for (const k of Object.keys(live)) delete live[k]; live.ergebnis = 'uebersprungen'; }
if (arg('bild')) {
  const d = await p.evaluate(P => { const c = document.getElementById(P + '-bild'); return c && c.width ? c.toDataURL('image/png') : null; }, P);
  if (d) writeFileSync(join(SZENE, 'ergebnis-bild.png'), Buffer.from(d.split(',')[1], 'base64'));
}
if (arg('quelle')) {
  const d = await p.evaluate(() => window.__quellen && window.__quellen[0] ? window.__quellen[0].toDataURL('image/png') : null);
  if (d) writeFileSync(join(SZENE, 'quelle.png'), Buffer.from(d.split(',')[1], 'base64'));
  live.quellen = await p.evaluate(() => (window.__quellen || []).length);
}
const aus = { szene: SZENE, art: w.art, jahr: w.jahr, konztest: w.konztest, sprache: SPRACHE, weg: WEG, ausloesen: AUSL, live };

// --- zum Vergleich: dasselbe Standbild hochgeladen --------------------------------
const STANDBILD = arg('bilddatei') || join(SZENE, 'standbild.jpg');
if ((arg('hochladen') || NUR) && existsSync(STANDBILD)) {
  await p.evaluate(P => { document.getElementById(P + '-status').textContent = ''; document.getElementById(P + '-status').classList.remove('ab-fehler'); document.getElementById(P + '-ergebnis').hidden = true; }, P);
  const t1 = Date.now();
  await p.setInputFiles('#' + P + '-datei', STANDBILD);
  await p.waitForFunction(P => !document.getElementById(P + '-ergebnis').hidden || document.getElementById(P + '-status').classList.contains('ab-fehler'), P, { timeout: 90000 }).catch(() => {});
  r = await ergebnisLesen();
  aus.hochgeladen = { ...bewerten(r), dauer_s: +((Date.now() - t1) / 1000).toFixed(1), meldungen: r.meldungen };
}
aus.js_fehler = jsFehler;
writeFileSync(OUT, JSON.stringify(aus, null, 1));
const kurz = o => o ? `${o.ergebnis} falsch=${(o.falsch_ohne_hinweis || []).length} mitHinweis=${(o.falsch_mit_hinweis || []).length} unsicher=${o.unsicher ?? '-'}` : '';
console.log(`${SZENE.split('/').pop()} | ${w.art} ${w.jahr || w.konztest} ${SPRACHE} ${WEG} | live: ${kurz(live)} ausl=${live.ausloeser}@${live.ausgeloest_s}s fertig=${live.dauer_s}s`
  + (live.fehlertext ? ' «' + live.fehlertext + '»' : '') + (aus.hochgeladen ? ' | hochgeladen: ' + kurz(aus.hochgeladen) : '') + (jsFehler.length ? ' | JS: ' + jsFehler.join(' / ') : ''));
await b.close();
server.close();
process.exit(0);
