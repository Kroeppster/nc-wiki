/*
 * KAMERA-LABOR: VIELE SZENARIEN
 * =============================
 *   node scripts/kamera-labor/batch.mjs scripts/kamera-labor/szenarien.json AUSGABEORDNER
 *        [--port 8151] [--site public] [--behalten]      (PYTHON=... für szene.py)
 *
 * szenarien.json: [{ "name": "ab-dunkel-1", "szene": {...Konfig für szene.py...},
 *                    "laeufe": [{"weg": "foto"}, {"weg": "stapel"}, {"weg": "stapel", "sprache": "fr"},
 *                               {"weg": "foto", "ausloesen": "manuell:6"}],
 *                    "hochladen": true }, ...]
 * (laeufe fehlt: foto und stapel; hochladen fehlt: true)
 * "erwartet": "fehler" - das Bild ist absichtlich unbrauchbar (Finger auf dem
 * Blatt, Kamera zu grob): richtig ist dann eine Meldung statt eines Ergebnisses.
 *
 * Am Schluss eine Zusammenfassung; der Lauf endet mit Code 1, wenn irgendwo
 * eine Zeile oder ein Zeichen still falsch gelesen wurde (FALSCH) oder ein
 * absichtlich unbrauchbares Bild trotzdem ein Ergebnis gab.
 *
 * Je Szenario: Video rendern (szene.py), jeden Lauf durchspielen (lauf.mjs),
 * Ergebnis als eine Zeile in AUSGABEORDNER/ergebnisse.jsonl. Das Video (70 MB)
 * wird danach gelöscht, ausser bei --behalten oder wenn ein Lauf FALSCH war
 * (dann bleibt es für die Nachprüfung, höchstens 6 Videos je Ausgabeordner).
 * Je Lauf bleibt das ausgewertete Bild (quelle-<weg>.png) liegen.
 */
import { spawnSync } from 'node:child_process';
import { readFileSync, appendFileSync, mkdirSync, existsSync, rmSync, readdirSync, renameSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HIER = dirname(fileURLToPath(import.meta.url));
const PY = process.env.PYTHON || 'python3';   // mit numpy, pymupdf, pillow, pyyaml
const [LISTE, AUS] = process.argv.slice(2);
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i < 0 ? d : (process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[i + 1] : true); };
const PORT = arg('port', '8151'), SITE = arg('site', join(HIER, '..', '..', 'public')), BEHALTEN = !!arg('behalten');
const szenarien = JSON.parse(readFileSync(LISTE, 'utf8'));
mkdirSync(AUS, { recursive: true });
const videos = () => readdirSync(AUS).filter(d => existsSync(join(AUS, d, 'video.mjpeg'))).length;

const bilanz = [];
for (const s of szenarien) {
  const ordner = join(AUS, s.name);
  mkdirSync(ordner, { recursive: true });
  const t0 = Date.now();
  if (!existsSync(join(ordner, 'wahrheit.json')) || !existsSync(join(ordner, 'video.mjpeg'))) {
    writeFileSync(join(ordner, 'konfig.json'), JSON.stringify(s.szene, null, 1));
    const r = spawnSync(PY, [join(HIER, 'szene.py'), join(ordner, 'konfig.json'), ordner], { encoding: 'utf8' });
    if (r.status !== 0) {
      appendFileSync(join(AUS, 'ergebnisse.jsonl'), JSON.stringify({ name: s.name, fehler_szene: (r.stderr || '').slice(-800) }) + '\n');
      console.log(s.name, 'SZENE FEHLER', (r.stderr || '').slice(-300));
      continue;
    }
  }
  const renderS = Math.round((Date.now() - t0) / 1000);
  const laeufe = s.laeufe || [{ weg: 'foto' }, { weg: 'stapel' }];
  const zeile = { name: s.name, szene: s.szene, render_s: renderS, laeufe: [] };
  let falsch = false;
  laeufe.forEach((l, i) => {
    const out = join(ordner, `lauf-${i}-${l.weg || 'foto'}${l.sprache ? '-' + l.sprache : ''}.json`);
    const a = [join(HIER, 'lauf.mjs'), '--szene', ordner, '--port', PORT, '--site', SITE, '--out', out, '--quelle',
      '--weg', l.weg || 'foto', '--sprache', l.sprache || 'de', '--ausloesen', l.ausloesen || 'auto', '--timeout', String(l.timeout || 45)];
    if (i === 0 && s.hochladen !== false) a.push('--hochladen');
    const r = spawnSync('node', a, { encoding: 'utf8', timeout: 180000 });
    if (existsSync(join(ordner, 'quelle.png'))) renameSync(join(ordner, 'quelle.png'), join(ordner, `quelle-${i}-${l.weg || 'foto'}.png`));
    let e = null;
    try { e = JSON.parse(readFileSync(out, 'utf8')); } catch (x) { e = { lauf_fehler: (r.stderr || r.stdout || '').slice(-500) }; }
    const k = o => o && { ergebnis: o.ergebnis, falsch_ohne_hinweis: o.falsch_ohne_hinweis, falsch_mit_hinweis: (o.falsch_mit_hinweis || []).length,
      unsicher: o.unsicher, unnoetig_unsicher: o.unnoetig_unsicher ? o.unnoetig_unsicher.length : undefined, fehlertext: o.fehlertext,
      punkte_soll: o.punkte_soll, punkte_ist: o.punkte_ist, rohwert_soll: o.rohwert_soll, rohwert_ist_gelesen: o.rohwert_ist_gelesen,
      ausloeser: o.ausloeser, ausgeloest_s: o.ausgeloest_s, dauer_s: o.dauer_s, stapel: o.stapel, letzter_hinweis: o.hinweise ? (o.hinweise[o.hinweise.length - 1] || [])[1] : undefined };
    zeile.laeufe.push({ ...l, live: k(e.live), hochgeladen: k(e.hochgeladen), js_fehler: e.js_fehler, lauf_fehler: e.lauf_fehler });
    if ((e.live && e.live.ergebnis === 'FALSCH') || (e.hochgeladen && e.hochgeladen.ergebnis === 'FALSCH')) falsch = true;
    console.log((r.stdout || '').trim() || (r.stderr || '').slice(-200));
  });
  appendFileSync(join(AUS, 'ergebnisse.jsonl'), JSON.stringify(zeile) + '\n');
  const ergebnisse = zeile.laeufe.flatMap(l => [l.live, l.hochgeladen].filter(Boolean)).map(o => o.ergebnis);
  const schlecht = s.erwartet === 'fehler' ? ergebnisse.filter(e => e !== 'fehler' && e !== 'timeout') : ergebnisse.filter(e => e === 'FALSCH');
  bilanz.push([s.name, schlecht.length ? 'NICHT OK' : 'ok', ergebnisse.join(' ')]);
  if (!BEHALTEN && !(falsch && videos() <= 6)) rmSync(join(ordner, 'video.mjpeg'), { force: true });
}
console.log('\n==== Kamera-Labor ====');
bilanz.forEach(b => console.log((b[1] === 'ok' ? '  OK    ' : '  FEHLT ') + b[0].padEnd(28) + b[2]));
const nicht = bilanz.filter(b => b[1] !== 'ok').length;
console.log(`==== ${bilanz.length - nicht} in Ordnung, ${nicht} nicht ====`);
process.exit(nicht ? 1 : 0);
