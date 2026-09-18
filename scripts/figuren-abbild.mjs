/*
 * ============================================================================
 * BLATT MIT ERZEUGTEN FIGUREN - Vorlage fuer den Vergleich
 * ============================================================================
 *   ~/bin/hugo --minify && (Server auf public/, Port 8123)
 *   node scripts/figuren-abbild.mjs /pfad/blatt.png [anzahl]
 *
 * Holt Figuren vom Figuren-Generator und legt sie einzeln, gross und auf
 * weissem Grund ab - so, wie die echten Serien im PDF stehen. Nur dann
 * misst scripts/figuren-vergleichen.py beide Seiten mit demselben Massstab.
 *
 * Mit --je-serie entsteht statt eines Blattes EIN BLATT JE SERIE
 * (blatt-01.png, blatt-02.png ...), jedes mit den 18 Figuren eines
 * Durchlaufs. Das braucht der Vergleich, der fragt, wie stark sich ganze
 * Serien voneinander unterscheiden - und nicht, wie die Figuren im Mittel
 * aussehen.
 *
 * Normalerweise ruft das Vergleichsskript dieses hier selbst auf.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { writeFileSync, unlinkSync } from 'node:fs';
const ziel = process.argv[2];
if (!ziel) { console.error('Kein Zielpfad angegeben.'); process.exit(2); }
const jeSerie = process.argv.includes('--je-serie');
const wunsch = Number(process.argv[3] || 54);
const ADRESSE = (process.env.ADRESSE || 'http://127.0.0.1:8123') + '/alpha/';
const b = await pw.chromium.launch();
const c = await b.newContext({ viewport: { width: 1400, height: 1200 }, deviceScaleFactor: 2 });
await c.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); } catch (e) {} });
const p = await c.newPage();
// CLIP-KENNUNGEN NEU DURCHNUMMERIEREN. Die Figuren kommen aus mehreren
// Seitenaufrufen, und jeder faengt bei "figclip0" wieder an. Landen zwei
// gleiche Kennungen auf EINEM Blatt, beschneidet die Form der ersten Figur
// auch die zweite - dann fehlen dort Felder. Die Messung meldete daraufhin
// Figuren mit drei oder vier Feldern, obwohl der Generator saubere fuenf
// geliefert hatte; der Fehler lag allein hier im Pruefwerkzeug.
let zaehler = 0;
function blattBauen(svgs) {
  return '<html><body style="margin:0;background:#fff">' + svgs
    .map(s => s.replace(/figclip\d+/g, 'abb' + (zaehler++)))
    // Grosszuegiger Abstand: Die Messung trennt die Figuren ueber ihre
    // Umrisse, und zwei, die sich fast beruehren, gelten als eine.
    .map(s => `<div style="display:inline-block;margin:26px">${s.replace('<svg', '<svg style="width:220px;height:220px"')}</div>`)
    .join('') + '</body></html>';
}
async function ablegen(svgs, datei) {
  const zwischen = datei + '.html';
  writeFileSync(zwischen, blattBauen(svgs));
  await p.goto('file://' + zwischen);
  await p.waitForTimeout(400);
  await p.screenshot({ path: datei, fullPage: true });
  unlinkSync(zwischen);
}
async function eineSerie() {
  await p.goto(ADRESSE, { waitUntil: 'networkidle' });
  await p.fill('#fig-min-pause', '0');
  await p.click('#fig-los');
  await p.waitForSelector('#fig-tafel .fig-svg');
  await p.waitForTimeout(400);
  return p.evaluate(() => [...document.querySelectorAll('#fig-tafel .fig-svg')].map(s => s.outerHTML));
}
if (jeSerie) {
  const ohne = ziel.replace(/\.png$/, '');
  for (let i = 1; i <= wunsch; i++) {
    await ablegen(await eineSerie(), `${ohne}-${String(i).padStart(2, '0')}.png`);
  }
  console.log(`${wunsch} Serienblaetter neben ${ohne}-01.png`);
} else {
  const alle = [];
  while (alle.length < wunsch) alle.push(...await eineSerie());
  await ablegen(alle.slice(0, wunsch), ziel);
  console.log(`${wunsch} erzeugte Figuren in ${ziel}`);
}
await b.close();
