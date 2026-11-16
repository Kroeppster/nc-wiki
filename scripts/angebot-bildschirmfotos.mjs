/*
 * ============================================================================
 * BILDSCHIRMFOTOS FÜR DIE KACHEL "ORIENTIERUNG UND AUSTAUSCH" (Startseite)
 * ============================================================================
 *   hugo --minify && (Server auf public/, Port 8123)
 *   node scripts/angebot-bildschirmfotos.mjs
 *
 * Erzeugt je Sprache zwei Bilder in assets/images/angebot/:
 *   uniguide.png / .fr.png / .it.png   Kopf und vier Zeilen der Vergleichstabelle
 *   berichte.png / .fr.png / .it.png   die erste Erfahrungsbericht-Karte
 * Deutsch ohne Kürzel; layouts/partials/material-grid.html nimmt für eine
 * Sprache zuerst das Bild mit ihrem Kürzel.
 *
 * Die Seiten aus PDFs (Testheft, Kursskript, Übungsserien) erzeugt
 * scripts/angebot-bilder-erzeugen.py. Neu laufen lassen, wenn sich die
 * Tabelle oder die Karten sichtbar geändert haben - nicht bei jedem neuen
 * Bericht, die Kachel zeigt nur, WIE es aussieht.
 * ============================================================================
 */
import pw from './playwright.mjs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const ZIEL = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'assets', 'images', 'angebot');
const ADRESSE = process.env.ADRESSE || 'http://127.0.0.1:8123';
const b = await pw.chromium.launch();
// Schmal wie ein Handy im Querformat: Dann zeigt die Tabelle nur die
// wichtigsten Spalten, und der Text ist in der kleinen Kachel noch lesbar.
const c = await b.newContext({ viewport: { width: 600, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
await c.addInitScript(() => { try { localStorage.setItem('alpha-notice-seen', '1'); localStorage.setItem('cookie-consent', 'accepted'); localStorage.setItem('theme', 'light'); } catch (e) {} });
const p = await c.newPage();
for (const lang of ['de', 'fr', 'it']) {
  const vor = lang === 'de' ? '' : '/' + lang, kuerzel = lang === 'de' ? '' : '.' + lang;
  await p.goto(ADRESSE + vor + '/ems/uniguide/', { waitUntil: 'networkidle' });
  const t = await p.evaluate(() => {
    const tab = document.getElementById('uniguide-table'), r = tab.getBoundingClientRect();
    const z4 = tab.querySelectorAll('tbody tr')[3].getBoundingClientRect();
    return { x: r.x + scrollX, y: r.y + scrollY, w: Math.min(r.width, innerWidth - r.x), h: z4.bottom - r.top };
  });
  await p.screenshot({ path: path.join(ZIEL, `uniguide${kuerzel}.png`), fullPage: true, clip: { x: t.x, y: t.y, width: t.w, height: t.h } });
  // Die Karte in Desktopbreite (zwei Karten nebeneinander): schmal hat sie kaum Rand.
  await p.setViewportSize({ width: 1280, height: 900 });
  await p.goto(ADRESSE + vor + '/ems/erfahrungsberichte/', { waitUntil: 'networkidle' });
  const k = await p.evaluate(() => { const r = document.querySelector('.report-card').getBoundingClientRect(); return { x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: Math.min(r.height, 240) }; });
  await p.screenshot({ path: path.join(ZIEL, `berichte${kuerzel}.png`), fullPage: true, clip: { x: k.x, y: k.y, width: k.w, height: k.h } });
  await p.setViewportSize({ width: 600, height: 900 });
  console.log(lang, 'uniguide', Math.round(t.w) + 'x' + Math.round(t.h), 'berichte', Math.round(k.w) + 'x' + Math.round(k.h));
}
await b.close();
