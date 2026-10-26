/*
 * KAMERA-LABOR: FESTE BILDER, ZWEI STÄNDE
 * =======================================
 *   node scripts/kamera-labor/bilder.mjs SITE_A [SITE_B] -- BILD...
 *
 * Liest jedes Bild (standbild.jpg, quelle-*.png aus batch.mjs-Läufen; die
 * Wahrheit liegt daneben als wahrheit.json) mit der gebauten Website SITE_A
 * und, falls angegeben, SITE_B - ohne Kamera, ohne Zufall, also genau
 * vergleichbar. Ausgegeben werden je Bild die orange markierten Zeilen
 * (Antwortbogen) bzw. Zeichen (Konztest) und die still falsch gelesenen,
 * Zeilen mit einem Unterschied zwischen den Ständen mit «≠», am Schluss die
 * Summen. Endet mit Code 1, wenn SITE_B irgendwo mehr still falsch liest als
 * SITE_A.
 *
 * Gedacht für Änderungen an der Auswertung: Die Live-Läufe schwanken mit dem
 * Zeitpunkt des Auslösens, hier nicht. (Oktober 2026 so gefunden: eine neue
 * Rauschschätzung hatte auf 130 Bildern stille Fehler und doppelt so viele
 * orange Zeilen gebracht, was in einzelnen Live-Läufen nicht auffiel.)
 *
 *   z. B. alter Stand in einem zweiten Arbeitsbaum:
 *   git worktree add /tmp/alt HEAD~1 && (cd /tmp/alt && hugo --minify -d /tmp/site-alt)
 *   hugo --minify -d /tmp/site-neu
 *   node scripts/kamera-labor/bilder.mjs /tmp/site-alt /tmp/site-neu -- labor/*\/standbild.jpg
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { join, extname, dirname, resolve } from 'node:path';

const trenn = process.argv.indexOf('--');
if (trenn < 3) { console.error('Aufruf: node bilder.mjs SITE_A [SITE_B] -- BILD...'); process.exit(2); }
const SITES = process.argv.slice(2, trenn).map(s => resolve(s));
const BILDER = process.argv.slice(trenn + 1);

async function oeffnen(site, port) {
  const server = createServer((req, res) => {
    let f = join(site, decodeURIComponent(req.url.split('?')[0]));
    if (!f.startsWith(site)) { res.writeHead(403); return res.end(); }
    try { if (statSync(f).isDirectory()) f = join(f, 'index.html'); } catch (e) {}
    if (!existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': extname(f) === '.html' ? 'text/html; charset=utf-8' : extname(f) === '.js' ? 'text/javascript' : 'application/octet-stream' });
    res.end(readFileSync(f));
  });
  await new Promise(ok => server.listen(port, '127.0.0.1', ok));
  const browser = await pw.chromium.launch();
  const p = await (await browser.newContext()).newPage();
  await p.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });
  await p.goto(`http://127.0.0.1:${port}/alpha/`, { waitUntil: 'load' });
  return { p, zu: async () => { await browser.close(); server.close(); } };
}

// Ein Bild lesen wie beim Hochladen; zurück: [unsicher, still falsch] oder die Meldung
async function lesen(p, bild, w) {
  const daten = (bild.endsWith('.png') ? 'data:image/png;base64,' : 'data:image/jpeg;base64,') + readFileSync(bild).toString('base64');
  if (w.art === 'antwortbogen') {
    const r = await p.evaluate(async d => {
      const A = window.NCWikiAntwortbogen, img = await A.laden(await (await fetch(d)).blob());
      const r = A.bogenLesen(A.bildAus(img));
      return r.fehler ? { fehler: r.fehler } : { a: r.antworten, u: r.unsicher };
    }, daten);
    if (r.fehler) return r.fehler;
    const soll = w.antworten.split('').map(x => x === '.' ? '' : x);
    return [r.u.filter(Boolean).length, r.a.filter((x, z) => !r.u[z] && x !== soll[z]).length];
  }
  // Konztest: die Seite selbst (Testsimulation wählen, Bild hochladen), wie konztest-pruefen.mjs
  await p.selectOption('#kt-testsim', w.konztest);
  const r = await p.evaluate(async d => {
    const I = window.NCWikiKonztestIntern, Bm = window.NCWikiBild, img = await Bm.laden(await (await fetch(d)).blob());
    const e = I.bogenLesen(Bm.bildAus(img));
    return e.fehler ? { fehler: e.fehler } : { m: [].concat.apply([], e.markiert), u: e.unsicher };
  }, daten).catch(x => ({ fehler: String(x.message).slice(0, 80) }));
  if (r.fehler) return r.fehler;
  const soll = w.markiert;
  return [r.u.filter(Boolean).length, r.m.filter((x, i) => !r.u[i] && (x ? '1' : '0') !== soll[i]).length];
}

const ergebnisse = SITES.map(() => []);
for (let s = 0; s < SITES.length; s++) {
  const { p, zu } = await oeffnen(SITES[s], 8560 + s);
  for (const bild of BILDER) {
    const w = JSON.parse(readFileSync(join(dirname(bild), 'wahrheit.json'), 'utf8'));
    ergebnisse[s].push(await lesen(p, bild, w).catch(x => 'Fehler: ' + String(x.message).slice(0, 60)));
  }
  await zu();
}
const zeigen = r => typeof r === 'string' ? ('Meldung: ' + r).slice(0, 34).padEnd(34) : `unsicher ${String(r[0]).padStart(3)}  still ${r[1]}`.padEnd(34);
const summe = SITES.map(() => [0, 0, 0]);
let schlechter = false;
BILDER.forEach((bild, i) => {
  const rs = ergebnisse.map(e => e[i]);
  rs.forEach((r, s) => { if (typeof r === 'string') summe[s][2]++; else { summe[s][0] += r[0]; summe[s][1] += r[1]; } });
  const anders = rs.length > 1 && JSON.stringify(rs[0]) !== JSON.stringify(rs[1]);
  if (rs.length > 1 && typeof rs[1] !== 'string' && rs[1][1] > (typeof rs[0] === 'string' ? 0 : rs[0][1])) schlechter = true;
  console.log((anders ? '≠ ' : '  ') + bild.slice(-60).padEnd(60) + ' ' + rs.map(zeigen).join(' | '));
});
SITES.forEach((s, i) => console.log(`${s}: unsicher ${summe[i][0]}, still falsch ${summe[i][1]}, Meldungen ${summe[i][2]} (${BILDER.length} Bilder)`));
if (schlechter) { console.log('SITE_B liest mindestens ein Bild mit mehr still falschen Stellen.'); process.exit(1); }
