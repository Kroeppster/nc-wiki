/*
 * ============================================================================
 * PRUEFSTAND FUER DEN FAKTEN-GENERATOR UND SEINEN DRUCK
 * ============================================================================
 *   ~/bin/hugo --minify && (Server auf public/, Port 8123)
 *   node scripts/fakten-generator-pruefen.mjs [/pfad/fuer/das/test-pdf]
 *
 * Ohne Pfad landet das Test-PDF im Temp-Ordner. (Frueher fehlte der Standard:
 * Wer das Argument vergass, hatte hinterher einen Ordner namens "undefined"
 * im Projekt stehen.)
 *
 * Prueft, dass ein erzeugtes Set die Struktur einer echten Serie hat und dass
 * der Druck drei brauchbare Blaetter liefert - inklusive einer Kontrolle des
 * ERZEUGTEN PDFs selbst (braucht pymupdf).
 *
 * DREI FALLEN, die hier alle schon zugeschlagen haben:
 *
 *  1. window.print() blockiert den Lauf. Wird im Test durch einen Zaehler
 *     ersetzt.
 *  2. Nach dem Drucken raeumt der Generator nach 1.5 s selbst auf. Wer danach
 *     misst, sieht einen Zustand, den es waehrend des Drucks nie gibt - der
 *     erste Versuch meldete deshalb Fehler, die keine waren.
 *  3. getComputedStyle(...).display taugt NICHT als Sichtbarkeitspruefung:
 *     Ein Kind eines display:none-Vorfahren behaelt seinen eigenen Wert
 *     ("block"), obwohl es nicht gerendert wird. Gefragt ist
 *     getClientRects().length.
 *
 * Und: DREI BLAETTER SIND NICHT DREI SEITEN. Das Aufgabenblatt mit 18
 * Aufgaben zu je fuenf Antworten braucht von sich aus mehrere Seiten -
 * geprueft wird deshalb die Reihenfolge, nicht eine feste Seitenzahl.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { mkdtempSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
const { chromium } = pw;
const ABLAGE = process.argv[2] || mkdtempSync(join(tmpdir(), 'fakten-'));
mkdirSync(ABLAGE, { recursive: true });
const b=await chromium.launch();
let ok=0,fail=0;
const pruef=(n,c,i='')=>{ if(c){ok++;console.log('  OK    '+n);} else {fail++;console.log('  FEHLT '+n+'  '+i);} };
const ctx=await b.newContext({viewport:{width:1100,height:1000}});
await ctx.addInitScript(()=>{try{localStorage.setItem('alpha-notice-seen','1');localStorage.setItem('cookie-consent','accepted');}catch(e){}});
const p=await ctx.newPage(); const js=[];
p.on('pageerror',e=>{if(!/PagefindUI/.test(String(e.message)))js.push(String(e.message).slice(0,110));});
// window.print() abfangen, sonst blockiert der Dialog den Lauf
await p.addInitScript(()=>{ window.__gedruckt=0; window.print=function(){ window.__gedruckt++; }; });
await p.goto('http://127.0.0.1:8123/ems/uebungsaufgaben/figuren-fakten-lernen/',{waitUntil:'networkidle'});

pruef('Startknopf da (Modus bleibt)', !!(await p.$('#fg-los')));
pruef('Druckknopf da', !!(await p.$('#fg-drucken')));
await p.click('#fg-drucken'); await p.waitForTimeout(500);
pruef('print() wurde aufgerufen', (await p.evaluate(()=>window.__gedruckt))===1);

const inhalt = await p.evaluate(()=>{
  const d=document.getElementById('fg-druck');
  return { blaetter:d.querySelectorAll('.fg-blatt').length,
           zeilen:d.querySelectorAll('.fg-tabelle tbody tr').length,
           fragen:d.querySelectorAll('.fg-druck-fragen > li').length,
           haken:d.querySelectorAll('.fg-druck-fragen strong').length,
           titel:[...d.querySelectorAll('.fg-blatt h2')].map(h=>h.textContent) };
});
console.log('   ', JSON.stringify(inhalt));
pruef('drei Blaetter', inhalt.blaetter===3, String(inhalt.blaetter));
pruef('15 Personen auf dem Einpraegeblatt', inhalt.zeilen===15, String(inhalt.zeilen));
pruef('36 Aufgaben (18 Aufgaben + 18 Loesungen)', inhalt.fragen===36, String(inhalt.fragen));
pruef('genau 18 Haken auf dem Loesungsblatt', inhalt.haken===18, String(inhalt.haken));

// Druckdarstellung pruefen - WAEHREND des Drucks, nicht danach. Der frueherere
// Versuch mass nach dem Aufraeum-Timeout (1.5 s) und setzte die Klasse selbst
// wieder: Gemessen wurde ein Zustand, den es so nie gibt.
await p.emulateMedia({media:'print'});
const sichtbar = await p.evaluate(()=>{
  // NICHT getComputedStyle(...).display abfragen: Ein Kind eines
  // display:none-Vorfahren behaelt seinen EIGENEN Wert ("block"), obwohl es
  // nicht gerendert wird. Gefragt ist, ob etwas tatsaechlich auf dem Papier
  // landet - das sagt getClientRects().
  const gerendert = e => !!e && e.getClientRects().length > 0;
  return { druck: gerendert(document.getElementById('fg-druck')),
           kopf:  gerendert(document.querySelector('header.site')),
           start: gerendert(document.getElementById('fg-start')) };
});
console.log('   ', JSON.stringify(sichtbar));
pruef('Druckblatt im Druck sichtbar', sichtbar.druck===true, String(sichtbar.druck));
pruef('Kopfzeile im Druck weg', sichtbar.kopf===false, String(sichtbar.kopf));
pruef('Startkarte im Druck weg', sichtbar.start===false, String(sichtbar.start));
await p.pdf({path:ABLAGE+'/fakten-set.pdf', format:'A4', printBackground:false});
// Das eigentliche Kriterium: Was steht im PDF? Die Sichtbarkeitspruefung
// oben reichte nicht - sie war gruen, waehrend das PDF 15 Seiten hatte und
// mit Navigation und Artikeltext begann.
{
  const { execSync } = await import('node:child_process');
  const info = JSON.parse(execSync('python3 -c "' +
    'import pymupdf,json,sys;d=pymupdf.open(sys.argv[1]);' +
    'print(json.dumps({\'seiten\':d.page_count,\'erste\':d[0].get_text(),\'text\':\' \'.join(s.get_text() for s in d)}))' +
    '" ' + ABLAGE + '/fakten-set.pdf').toString());
  // DREI BLAETTER sind nicht drei Seiten: Das Aufgabenblatt mit 18 Aufgaben
  // zu je fuenf Antworten braucht von sich aus mehrere Seiten. Geprueft wird
  // deshalb der Rahmen und die Reihenfolge, nicht eine feste Zahl.
  pruef('PDF hat eine plausible Seitenzahl (3-12)', info.seiten>=3 && info.seiten<=12, String(info.seiten));
  pruef('PDF beginnt mit dem Einpraegeblatt', /^\s*Fakten lernen . Einpr/.test(info.erste), info.erste.slice(0,40));
  pruef('Reihenfolge Einpraegen -> Aufgaben -> Loesungen',
    info.text.indexOf('Einprägephase') < info.text.indexOf('Reproduktionsphase')
    && info.text.indexOf('Reproduktionsphase') < info.text.lastIndexOf('Lösungen'));
  pruef('PDF enthaelt KEINE Navigation', !/AUF DIESER SEITE|Übungsaufgaben \|/.test(info.text));
  pruef('PDF enthaelt KEINEN Artikeltext', !info.text.includes('Wieso sind diese Untertests'));
  pruef('PDF enthaelt das Einpraegeblatt', info.text.includes('Einprägephase'));
  pruef('PDF enthaelt die Loesungen', info.text.includes('Lösungen'));
}
await p.emulateMedia({media:'screen'});

// Aufraeumen nach dem Druck
await p.evaluate(()=>{ window.dispatchEvent(new Event('afterprint')); });
await p.waitForTimeout(300);
pruef('nach dem Druck wieder aufgeraeumt',
  (await p.evaluate(()=>!document.body.classList.contains('fg-druckt')
     && document.getElementById('fg-druck').innerHTML===''
     && document.getElementById('fg-druck').parentElement.id !== ''  // wieder im Generator, nicht am <body>
  ))); 
pruef('keine JS-Fehler', js.length===0, js.join(' | '));
console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
await b.close();
