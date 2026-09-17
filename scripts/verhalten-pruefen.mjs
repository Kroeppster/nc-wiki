/*
 * ============================================================================
 * VERHALTENS-PRUEFSTAND: KLICKT DIE WEBSITE DURCH
 * ============================================================================
 * Der andere Pruefstand (seiten-pruefen.mjs) LAEDT Seiten und misst sie - er
 * klickt nichts. Dieser hier tut das Gegenteil: Er bedient die beweglichen
 * Teile und prueft nach, ob sie tun, was sie sollen.
 *
 *   ~/bin/hugo --minify && npx pagefind --site public
 *   (Server auf public/ starten, Port 8123)
 *   node scripts/verhalten-pruefen.mjs
 *
 * Der Suchindex muss vorhanden sein, sonst prueft der Suchtest gegen nichts -
 * "hugo" allein genuegt NICHT, pagefind gehoert dazu.
 *
 * GEPRUEFT WIRD:
 *   Dunkelmodus      Umschalter wirkt und die Wahl ueberlebt das Neuladen
 *   Sprachwahl       fuehrt auf die Entsprechung in der anderen Sprache
 *   Suche            liefert zu einem echten Begriff Treffer
 *   Erfahrungsberichte  Filter veraendert die Anzahl sichtbarer Karten
 *   Uniguide         Vergleich zweier Universitaeten erscheint
 *   Pruefungsmodus   Uhr zaehlt, Pause haelt an, Abbrechen schliesst
 *   Pruefungsmodus   Zeit folgt der Aufgabenzahl, Experte gibt sie frei
 *   Pruefungsmodus   Figuren/Fakten: nur Zeit, nie die Aufgabenzahl
 *   Formulare        leer wird nicht gesendet, ausgefuellt schon
 *
 * ZWEI FALLEN, die hier schon Zeit gekostet haben:
 *
 *  1. DIALOGE. "Abbrechen" im Pruefungsmodus fragt per confirm() nach.
 *     Playwright VERWIRFT Dialoge automatisch, wenn kein Handler registriert
 *     ist - die Rueckfrage wird also mit "Nein" beantwortet, die Uebung laeuft
 *     weiter, und der Test meldet faelschlich einen Fehler. Jeder Kontext
 *     bekommt deshalb unten einen Dialog-Handler.
 *
 *  2. KNOEPFE NACH TEXT SUCHEN. Ein Durchlauf, der Knoepfe nach Textmuster
 *     anklickt, startet irgendwann versehentlich den Pruefungsmodus; dessen
 *     Buehne faengt danach alle weiteren Klicks ab und der Lauf laeuft in
 *     einen Timeout. Deshalb nur echte Kennungen aus dem Markup verwenden
 *     (data-pm-start, #pm-los, .pm-c-aufgaben ...).
 *
 * Formspree wird abgefangen und beantwortet - es geht NIE eine echte
 * Nachricht raus.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
const { chromium } = pw;
const B = 'http://127.0.0.1:8123';
const b = await chromium.launch();
let ok = 0, fail = 0;
const pruef = (name, bedingung, info='') => {
  if (bedingung) { ok++; console.log(`  OK    ${name}`); }
  else { fail++; console.log(`  FEHLT ${name}  ${info}`); }
};
async function neu(opts={}) {
  const ctx = await b.newContext({ viewport:{width:1280,height:900}, ...opts });
  await ctx.addInitScript(() => { try{ localStorage.setItem('alpha-notice-seen','1'); localStorage.setItem('cookie-consent','accepted'); }catch(e){} });
  const p = await ctx.newPage();
  const jsFehler = [];
  p.on('pageerror', e => { if(!/PagefindUI/.test(String(e.message))) jsFehler.push(String(e.message).slice(0,90)); });
  // Siehe Falle 1 im Kopf dieser Datei: ohne Handler verwirft Playwright
  // jede Rueckfrage, und "Abbrechen wirklich?" wird mit Nein beantwortet.
  p.on('dialog', d => d.accept());
  return { ctx, p, jsFehler, js: jsFehler };
}

// ============ 1) DUNKELMODUS-UMSCHALTER ============
console.log('\n=== Dunkelmodus-Umschalter ===');
{
  const { ctx, p, jsFehler } = await neu();
  await p.goto(B + '/', { waitUntil:'networkidle' });
  const vorher = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
  const knopf = await p.$('.theme-toggle, [class*=theme], button[aria-label*=Farb], button[aria-label*=Dark], button[aria-label*=Hell], button[aria-label*=dunk]');
  pruef('Umschalter vorhanden', !!knopf);
  if (knopf) {
    await knopf.click(); await p.waitForTimeout(400);
    const nachher = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
    pruef('Hintergrund aendert sich', vorher !== nachher, `${vorher} -> ${nachher}`);
    // ueberlebt Neuladen?
    await p.reload({ waitUntil:'networkidle' }); await p.waitForTimeout(300);
    const nachReload = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
    pruef('Wahl ueberlebt Neuladen', nachher === nachReload, `${nachher} -> ${nachReload}`);
  }
  pruef('keine JS-Fehler', jsFehler.length===0, jsFehler.join(' | '));
  await ctx.close();
}

// ============ 2) SPRACHWAHL ============
console.log('\n=== Sprachwahl ===');
{
  const { ctx, p, jsFehler } = await neu();
  await p.goto(B + '/ems/uniguide/', { waitUntil:'networkidle' });
  const t = await p.$('.lang-switch .submenu-toggle');
  if (t) { await t.click(); await p.waitForTimeout(300); }
  const links = await p.$$eval('.lang-switch a', as => as.map(a => a.getAttribute('href')));
  pruef('Sprachlinks vorhanden', links.length >= 2, JSON.stringify(links));
  const fr = links.find(h => h && h.includes('/fr/'));
  if (fr) {
    await p.goto(B + fr, { waitUntil:'networkidle' });
    const lang = await p.evaluate(() => document.documentElement.lang);
    pruef('Sprachwechsel fuehrt auf FR-Entsprechung', lang.startsWith('fr') && p_url_ok(p.url()), p.url());
  }
  function p_url_ok(u){ return u.includes('/fr/'); }
  pruef('keine JS-Fehler', jsFehler.length===0, jsFehler.join(' | '));
  await ctx.close();
}

// ============ 3) SUCHE ============
console.log('\n=== Suche ===');
{
  const { ctx, p, jsFehler } = await neu();
  await p.goto(B + '/', { waitUntil:'networkidle' });
  const sKnopf = await p.$('[class*=search], button[aria-label*=Such]');
  pruef('Such-Knopf vorhanden', !!sKnopf);
  if (sKnopf) {
    await sKnopf.click(); await p.waitForTimeout(800);
    const feld = await p.$('input[type=text][class*=pagefind], .pagefind-ui input, input[placeholder*=uch]');
    pruef('Suchfeld erscheint', !!feld);
    if (feld) {
      await feld.fill('Testsimulation');
      await p.waitForTimeout(2500);
      const treffer = await p.$$eval('.pagefind-ui__result, [class*=result]', e => e.length).catch(()=>0);
      pruef('Suche liefert Treffer', treffer > 0, `Treffer: ${treffer}`);
    }
  }
  pruef('keine JS-Fehler', jsFehler.length===0, jsFehler.join(' | '));
  await ctx.close();
}

// ============ 4) ERFAHRUNGSBERICHTE: FILTER ============
console.log('\n=== Erfahrungsberichte: Filter ===');
{
  const { ctx, p, jsFehler } = await neu();
  await p.goto(B + '/ems/erfahrungsberichte/', { waitUntil:'networkidle' });
  const alle = await p.$$eval('.card, li[class*=card]', e => e.filter(x=>x.offsetParent!==null).length);
  pruef('Berichte werden gezeigt', alle > 0, `${alle} sichtbar`);
  const knoepfe = await p.$$('.filter-btn, [class*=filter] button, button[data-jahr], [data-filter]');
  pruef('Filter-Knoepfe vorhanden', knoepfe.length > 0, `${knoepfe.length} Knoepfe`);
  if (knoepfe.length > 1) {
    await knoepfe[1].click(); await p.waitForTimeout(500);
    const nachher = await p.$$eval('.card, li[class*=card]', e => e.filter(x=>x.offsetParent!==null).length);
    pruef('Filter veraendert die Anzahl', nachher !== alle && nachher > 0, `${alle} -> ${nachher}`);
  }
  pruef('keine JS-Fehler', jsFehler.length===0, jsFehler.join(' | '));
  await ctx.close();
}

// ============ 5) UNIGUIDE: VERGLEICH ============
console.log('\n=== Uniguide: Vergleich ===');
{
  const { ctx, p, jsFehler } = await neu();
  await p.goto(B + '/ems/uniguide/', { waitUntil:'networkidle' });
  const boxen = await p.$$('input[type=checkbox]');
  pruef('Vergleichs-Kaestchen vorhanden', boxen.length >= 2, `${boxen.length}`);
  if (boxen.length >= 2) {
    await boxen[0].check(); await boxen[1].check();
    await p.waitForTimeout(600);
    const spalten = await p.$$eval('.compare-col, [class*=compare]', e => e.filter(x=>x.offsetParent!==null).length);
    pruef('Vergleichsansicht erscheint', spalten > 0, `${spalten} Elemente`);
  }
  pruef('keine JS-Fehler', jsFehler.length===0, jsFehler.join(' | '));
  await ctx.close();
}


console.log('\n=== Prüfungsmodus: Uhr laeuft und laesst sich stoppen ===');
{
  const {ctx,p,js}=await neu();
  await p.goto(B+'/ems/pruefungsmodus/',{waitUntil:'networkidle'});
  await p.click('[data-pm-start="0"]');
  await p.waitForTimeout(500);
  const buehneAuf = await p.$eval('#pm-buehne', e=>!e.hidden).catch(()=>false);
  pruef('Bühne oeffnet sich', buehneAuf);
  // Anweisungsphase ueberspringen: "Los" druecken falls sichtbar
  const los = await p.$('#pm-los');
  if (los && await los.isVisible()) { await los.click(); await p.waitForTimeout(600); }
  const u1 = await p.$eval('.pm-uhr', e=>e.textContent.trim()).catch(()=>null);
  await p.waitForTimeout(2300);
  const u2 = await p.$eval('.pm-uhr', e=>e.textContent.trim()).catch(()=>null);
  pruef('Uhr zaehlt', u1&&u2&&u1!==u2, `${u1} -> ${u2}`);
  // Pause
  const pause=await p.$('#pm-pause');
  if(pause && await pause.isVisible()){
    await pause.click(); await p.waitForTimeout(200);
    const a=await p.$eval('.pm-uhr',e=>e.textContent.trim());
    await p.waitForTimeout(1600);
    const bb=await p.$eval('.pm-uhr',e=>e.textContent.trim());
    pruef('Pause haelt die Uhr an', a===bb, `${a} -> ${bb}`);
  }
  const stop=await p.$('#pm-stop');
  if(stop){ await stop.click(); await p.waitForTimeout(600); }
  const zu = await p.$eval('#pm-buehne', e=>e.hidden).catch(()=>true);
  pruef('Stopp schliesst die Bühne', zu);
  pruef('keine JS-Fehler', js.length===0, js.join(' | '));
  await ctx.close();
}

console.log('\n=== Prüfungsmodus: Zeit folgt der Aufgabenzahl ===');
{
  const {ctx,p,js}=await neu();
  await p.goto(B+'/ems/pruefungsmodus/',{waitUntil:'networkidle'});
  const reihen = await p.$$('#pm-custom tr');
  pruef('Tabelle des individuellen Laufs vorhanden', reihen.length>0, `${reihen.length} Zeilen`);
  const a0 = await p.$('.pm-c-aufgaben');
  const z0 = await p.$('.pm-c-zeit');
  const vorher = z0 ? (await z0.textContent()||'').trim() : null;
  if (a0){
    await a0.fill('9'); await a0.dispatchEvent('input'); await p.waitForTimeout(400);
    const nachher = z0 ? (await z0.textContent()||'').trim() : null;
    pruef('Zeit wird automatisch neu gerechnet', vorher!==nachher, `${vorher} -> ${nachher}`);
  }
  const exp = await p.$('#pm-c-experte');
  pruef('Experten-Schalter vorhanden', !!exp);
  if (exp){
    const vorEing = await p.$$eval('.pm-c-zeit-eingabe', e=>e.filter(x=>x.offsetParent!==null).length);
    await exp.check(); await p.waitForTimeout(400);
    const nachEing = await p.$$eval('.pm-c-zeit-eingabe', e=>e.filter(x=>x.offsetParent!==null).length);
    pruef('Experte gibt die Zeitfelder frei', nachEing>vorEing, `${vorEing} -> ${nachEing} sichtbare Felder`);
  }
  pruef('keine JS-Fehler', js.length===0, js.join(' | '));
  await ctx.close();
}

console.log('\n=== Prüfungsmodus: Figuren/Fakten nur Zeit, nicht Aufgabenzahl ===');
{
  const {ctx,p,js}=await neu();
  await p.goto(B+'/ems/pruefungsmodus/',{waitUntil:'networkidle'});
  await p.check('#pm-c-experte'); await p.waitForTimeout(400);
  const daten = await p.$$eval('#pm-custom tr', rs => rs.map(r => ({
    text: (r.textContent||'').replace(/\s+/g,' ').trim().slice(0,30),
    hatAufgaben: !!r.querySelector('.pm-c-aufgaben'),
    aufgabenGesperrt: (()=>{const a=r.querySelector('.pm-c-aufgaben');return a? a.disabled : null;})(),
    hatZeitfeld: !!r.querySelector('.pm-c-zeit-eingabe'),
  })));
  const feste = daten.filter(d => /Figuren|Fakten/i.test(d.text));
  pruef('Figuren/Fakten-Zeilen gefunden', feste.length>0, `${feste.length}`);
  feste.forEach(d=>{
    pruef(`"${d.text}": Aufgabenzahl nicht aenderbar`, d.aufgabenGesperrt===true || d.hatAufgaben===false,
          `hatFeld=${d.hatAufgaben} gesperrt=${d.aufgabenGesperrt}`);
    pruef(`"${d.text}": Zeit aenderbar`, d.hatZeitfeld===true);
  });
  pruef('keine JS-Fehler', js.length===0, js.join(' | '));
  await ctx.close();
}

console.log('\n=== Formulare: Pflichtfelder und Absenden ===');
for (const [name, url, sel, fuellen] of [
  ['Kontakt','/kontakt/','form.contact-form', async p=>{ await p.fill('#cf-name','Testperson'); await p.fill('#cf-email','test@example.org'); await p.fill('#cf-message','Testnachricht.'); }],
  ['Fehlermeldung','/ems/uebungsaufgaben/','form.report-error-general', async p=>{ await p.fill('#ef-item','Muster zuordnen'); await p.fill('#ef-desc','Aufgabe 3 hat zwei richtige Antworten.'); }],
]) {
  const {ctx,p,js}=await neu();
  let gesendet=null;
  await p.route('**/formspree.io/**', r=>{ gesendet=r.request().postData(); r.fulfill({status:200,contentType:'application/json',body:'{"ok":true}'}); });
  await p.goto(B+url,{waitUntil:'networkidle'});
  const f=await p.$(sel);
  pruef(`${name}: Formular vorhanden`, !!f);
  if(f){
    const det = await p.$(`${sel} >> xpath=ancestor::details`);
    if (det) { await p.evaluate(s=>{const d=document.querySelector(s).closest('details'); if(d) d.open=true;}, sel); await p.waitForTimeout(300); }
    await p.click(`${sel} [type=submit]`).catch(()=>{});
    await p.waitForTimeout(400);
    pruef(`${name}: leer wird nicht gesendet`, gesendet===null);
    await fuellen(p);
    await p.click(`${sel} [type=submit]`); await p.waitForTimeout(1500);
    pruef(`${name}: ausgefuellt wird gesendet`, gesendet!==null, String(gesendet).slice(0,70));
  }
  pruef(`${name}: keine JS-Fehler`, js.length===0, js.join(' | '));
  await ctx.close();
}


console.log(`\n==== ${ok} bestanden, ${fail} nicht ====`);
await b.close();
