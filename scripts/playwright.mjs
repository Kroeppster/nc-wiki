/*
 * ============================================================================
 * PLAYWRIGHT LADEN (fuer alle Pruefstaende in diesem Ordner)
 * ============================================================================
 * Die Pruefstaende (seiten-pruefen.mjs, verhalten-pruefen.mjs, ...) steuern
 * einen Browser ueber Playwright. Frueher stand in jedem von ihnen ein fester
 * Pfad, der nur auf einem bestimmten Rechner stimmte. Jetzt wird der Reihe
 * nach versucht:
 *
 *   1. PLAYWRIGHT=<Pfad zu .../playwright/index.js>   (Umgebungsvariable)
 *   2. das Paket "playwright", wie es "npm install playwright" hinlegt
 *      (danach einmalig: npx playwright install chromium)
 *   3. der bisherige feste Pfad
 *
 * Playwright steht bewusst NICHT in package.json: Die Website selbst braucht
 * es nicht, und der Bau in GitHub Actions soll nicht bei jedem Lauf einen
 * Browser herunterladen.
 * ============================================================================
 */
const ORTE = [process.env.PLAYWRIGHT, 'playwright', '/opt/node22/lib/node_modules/playwright/index.js'].filter(Boolean);
let modul = null;
for (const ort of ORTE) {
  try { modul = await import(ort); break; } catch (e) { /* naechster Ort */ }
}
if (!modul) {
  console.error('Playwright nicht gefunden. Einmalig: npm install playwright && npx playwright install chromium\n' +
                '(oder PLAYWRIGHT=<Pfad zu playwright/index.js> setzen). Siehe scripts/playwright.mjs.');
  process.exit(2);
}
export default modul.default || modul;
