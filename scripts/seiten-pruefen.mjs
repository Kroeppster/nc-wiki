/*
 * ============================================================================
 * DARSTELLUNGS-PRUEFSTAND: JEDE SEITE, JEDE BREITE, BEIDE FARBMODI
 * ============================================================================
 * Ruft jede gebaute Seite in einem echten Browser auf und misst, was man auf
 * einem Bildschirmfoto sehen wuerde. Er ersetzt kein Auge, aber er findet die
 * Fehlerarten, die sonst erst jemandem auf dem Handy auffallen.
 *
 *   npm run bauen                 # public/ erzeugen
 *   npx http-server public -p 8099 -s &      (oder ein anderer Server)
 *   node scripts/seiten-pruefen.mjs
 *
 * Die Liste der Seiten kommt aus /tmp/alle-seiten.txt:
 *   cd public && find . -name index.html | sed 's|^\.||; s|/index\.html$|/|' \
 *     | sort > /tmp/alle-seiten.txt
 *
 * Umgebungsvariablen:
 *   BREITEN=1280,768,390   welche Fensterbreiten (Standard 1280,390)
 *   MODI=light,dark        welche Farbmodi (Standard light)
 *
 * WAS GEPRUEFT WIRD - und warum jede Pruefung existiert:
 *   1 seite-scrollt-quer        Die ganze Seite laesst sich seitlich schieben.
 *                               Fand eine zu lange Adresse im Uniguide, die
 *                               auf dem Handy 8px Ueberhang erzeugte.
 *   2 kaesten-ueberlappen       Zwei Geschwister im Textfluss liegen
 *     kaesten-stossen-aneinander uebereinander oder ohne Abstand aneinander.
 *                               Fand den Mitglieder-Hinweis, der sich neben
 *                               den Zurueck-Link draengte.
 *   3 inhalt-abgeschnitten      Text verschwindet hinter overflow:hidden.
 *   4 ragt-aus-dem-bild         Ein Element steht seitlich ausserhalb.
 *   5 bild-laedt-nicht          Bild fehlt oder ist kaputt.
 *   6 kontrast-zu-schwach       Text unter WCAG AA.
 *
 * WICHTIG - FEHLALARME KOSTEN VERTRAUEN. Die Pruefungen schliessen bewusst
 * aus, was nur wie ein Fehler aussieht: SVG-Formen (liegen absichtlich
 * uebereinander), Felder nur fuer Vorleseprogramme (stehen absichtlich
 * ausserhalb), Inhalte in einem Scroll-Kasten (duerfen breiter sein),
 * inline-Elemente ueber mehrere Zeilen (ihre Kaesten ueberlappen immer),
 * Tabellenzellen (stossen immer aneinander) und Text auf einem VERLAUF
 * (dessen Kontrast laesst sich nicht ausrechnen - wer es doch versucht,
 * misst gegen Weiss und meldet einwandfreie Stellen als fehlerhaft).
 *
 * Wer eine Pruefung ergaenzt: erst gegen einen ECHTEN, bekannten Fehler
 * testen. Eine Pruefung, die den Fehler nicht findet, den sie finden soll,
 * ist schlimmer als keine - sie macht ruhig.
 * ============================================================================
 */
import pw from '/opt/node22/lib/node_modules/playwright/index.js';
import { readFileSync } from 'node:fs';
const { chromium } = pw;

const PFADE = readFileSync('/tmp/alle-seiten.txt','utf8').split('\n').filter(Boolean);
const BASIS = 'http://127.0.0.1:8099';
const BREITEN = process.env.BREITEN ? process.env.BREITEN.split(',').map(Number) : [1280, 390];
const MODI   = process.env.MODI ? process.env.MODI.split(',') : ['light'];
const PARALLEL = 6;

const pruefung = () => {
  const funde = [];
  const vw = document.documentElement.clientWidth;
  const sicht = el => {
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
  };
  // --- Was NICHT gemeldet werden darf, und warum ------------------------
  // SVG: Pfade und Rechtecke einer Zeichnung liegen absichtlich uebereinander.
  const istSvg = el => el instanceof SVGElement;
  // Nur-fuer-Vorleseprogramme: steht absichtlich ausserhalb des Bildes.
  const nurVorlese = el => !!el.closest('.visually-hidden-field');
  // Ein Vorfahr, der waagrecht scrollen darf (z.B. eine breite Tabelle in
  // ihrem eigenen Scroll-Kasten): dann ist Herausragen gewollt.
  const inScrollkasten = el => {
    let a = el.parentElement;
    while (a && a !== document.body) {
      const s = getComputedStyle(a);
      if (s.overflowX === 'auto' || s.overflowX === 'scroll') return true;
      a = a.parentElement;
    }
    return false;
  };
  // display:inline erstreckt sich ueber mehrere Zeilen; sein Kasten ist die
  // Vereinigung aller Zeilenkaesten und ueberlappt zwangslaeufig mit dem des
  // naechsten inline-Elements. Das ist kein Fehler.
  const eigenerKasten = el => getComputedStyle(el).display !== 'inline';
  const ignorieren = el => istSvg(el) || nurVorlese(el);

  // 1) Die ganze Seite scrollt waagrecht
  const ueber = document.documentElement.scrollWidth - vw;
  if (ueber > 1) funde.push({ art: 'seite-scrollt-quer', um: ueber });

  // 2) SICH ÜBERLAPPENDE GESCHWISTER im normalen Textfluss.
  //    Nur Geschwister, nur beide im Fluss (kein absolute/fixed/sticky),
  //    nur wenn sich die Kästen in BEIDEN Richtungen deutlich schneiden.
  //    So bleiben gewollte Überlagerungen (Badges, Menüs, Sticky-Leisten)
  //    aussen vor, echte Kollisionen wie Zurück-Link + Hinweis nicht.
  const imFluss = el => {
    const s = getComputedStyle(el);
    if (['absolute','fixed','sticky'].includes(s.position)) return false;
    if (s.float !== 'none') return false;
    if (parseFloat(s.marginTop) < 0 || parseFloat(s.marginLeft) < 0) return false;
    if (s.transform !== 'none') return false;
    if (ignorieren(el) || !eigenerKasten(el)) return false;
    // Tabellenzellen stossen per Definition ohne Abstand aneinander.
    if (['td','th','tr','thead','tbody','tfoot'].includes(el.tagName.toLowerCase())) return false;
    return sicht(el);
  };
  const eltern = new Set();
  document.querySelectorAll('main *').forEach(el => el.parentElement && eltern.add(el.parentElement));
  eltern.forEach(p => {
    const ps = getComputedStyle(p);
    if (ps.display.includes('grid')) return;          // Raster dürfen stapeln
    const kinder = [...p.children].filter(imFluss);
    for (let i = 0; i < kinder.length; i++) {
      for (let j = i + 1; j < kinder.length; j++) {
        const a = kinder[i].getBoundingClientRect(), b = kinder[j].getBoundingClientRect();
        if (a.width < 2 || a.height < 2 || b.width < 2 || b.height < 2) continue;
        const qx = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const qy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        const nameA = kinder[i].tagName.toLowerCase() + '.' + (kinder[i].className || '').toString().split(' ')[0];
        const nameB = kinder[j].tagName.toLowerCase() + '.' + (kinder[j].className || '').toString().split(' ')[0];
        if (qx > 4 && qy > 4) {
          funde.push({ art: 'kaesten-ueberlappen', a: nameA, b: nameB,
            um: `${Math.round(qx)}x${Math.round(qy)}` });
          continue;
        }
        // Zwei Kästen stossen ohne Abstand aneinander und stehen dabei
        // nebeneinander auf einer Zeile. Geometrisch ist das keine
        // Überlappung - optisch schon, sobald einer von beiden einen
        // eigenen Hintergrund oder Rahmen hat und höher ist als der andere.
        // Genau so sah der Mitglieder-Hinweis neben dem Zurück-Link aus.
        const kasten = el => {
          const s = getComputedStyle(el);
          const bg = s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent';
          const rand = parseFloat(s.borderTopWidth) > 0 || parseFloat(s.borderLeftWidth) > 0;
          return bg || rand;
        };
        if (qy > 4 && qx > -3 && qx <= 4 && (kasten(kinder[i]) || kasten(kinder[j]))) {
          funde.push({ art: 'kaesten-stossen-aneinander', a: nameA, b: nameB,
            abstand: Math.round(-qx) });
        }
      }
    }
  });

  // 3) Inhalt, der ABGESCHNITTEN wird.
  //    Nur bei overflow:hidden/clip - dort verschwindet wirklich etwas.
  //    Bei overflow:visible ragt ein Kind zwar über den Kasten der Eltern
  //    hinaus, bleibt aber sichtbar; das ist oft gewollt (die Seitenleiste
  //    "Auf dieser Seite" bricht absichtlich in den Seitenrand aus). Für
  //    "ragt aus dem Bild" ist Prüfung 4 zuständig.
  document.querySelectorAll('main *').forEach(el => {
    const s = getComputedStyle(el);
    if (!['hidden','clip'].includes(s.overflowX) || !sicht(el)) return;
    if (ignorieren(el)) return;
    if (el.scrollWidth - el.clientWidth > 2 && el.clientWidth > 0) {
      funde.push({ art: 'inhalt-abgeschnitten',
        el: el.tagName.toLowerCase() + '.' + (el.className || '').toString().split(' ')[0],
        um: el.scrollWidth - el.clientWidth,
        text: (el.textContent || '').trim().slice(0, 40) });
    }
  });

  // 4) Element ragt seitlich aus dem Sichtfeld
  document.querySelectorAll('main *').forEach(el => {
    if (!sicht(el) || ignorieren(el) || inScrollkasten(el)) return;
    const r = el.getBoundingClientRect();
    if (r.width > 0 && (r.left < -2 || r.right > vw + 2)) {
      funde.push({ art: 'ragt-aus-dem-bild',
        el: el.tagName.toLowerCase() + '.' + (el.className || '').toString().split(' ')[0],
        links: Math.round(r.left), rechts: Math.round(r.right - vw) });
    }
  });

  // 5) Bilder, die nicht laden (lazy weit unten ist kein Fehler)
  document.querySelectorAll('img').forEach(img => {
    if (img.complete && img.naturalWidth > 0) return;
    const r = img.getBoundingClientRect();
    const nah = r.top < innerHeight * 2 && r.bottom > -innerHeight;
    if (img.loading === 'lazy' && !nah) return;
    funde.push({ art: 'bild-laedt-nicht', src: img.getAttribute('src') });
  });

  // 6) Textkontrast (WCAG AA: 4.5:1 normal, 3:1 ab 24px bzw. 18.66px fett)
  const srgb = c => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
  const lum = (r,g,b) => 0.2126*srgb(r)+0.7152*srgb(g)+0.0722*srgb(b);
  const zahl = f => (f.match(/[\d.]+/g)||[]).map(Number);
  // Liefert die Hintergrundfarbe - oder null, wenn irgendwo auf dem Weg nach
  // oben ein VERLAUF oder Bild liegt. Ein Verlauf hat keine eine Farbe; wer
  // ihn ignoriert, rechnet gegen Weiss und meldet dann Fehlalarme. Genau so
  // erschienen das Markenband (echte 6.8:1, gemeldet 2.3:1) und die Uhr des
  // Prüfungsmodus (weiss auf dunklem Verlauf, gemeldet 1.07:1) als "zu
  // schwach". Solche Stellen werden übersprungen statt falsch gemeldet.
  const hinterGrund = el => {
    let a = el;
    while (a) {
      const s = getComputedStyle(a);
      if (s.backgroundImage && s.backgroundImage !== 'none') return null;
      const v = zahl(s.backgroundColor);
      if (v.length >= 3 && (v[3] === undefined || v[3] > 0.5)) return v;
      a = a.parentElement;
    }
    return [255,255,255];
  };
  const gesehenK = new Set();
  document.querySelectorAll('main p,main h1,main h2,main h3,main h4,main a,main li,main td,main th,main dt,main dd,main button,main label,main span,main strong,main em').forEach(el => {
    if (!sicht(el) || ignorieren(el)) return;
    const t = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
    if (!t) return;
    const s = getComputedStyle(el);
    const vg = zahl(s.color), hg = hinterGrund(el);
    if (hg === null) return;   // Verlauf: nicht analytisch messbar
    if (vg.length < 3) return;
    if (vg[3] !== undefined && vg[3] < 0.5) return;
    const l1 = lum(vg[0],vg[1],vg[2]), l2 = lum(hg[0],hg[1],hg[2]);
    const k = (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
    const px = parseFloat(s.fontSize), fett = parseInt(s.fontWeight) >= 700;
    const noetig = (px >= 24 || (fett && px >= 18.66)) ? 3 : 4.5;
    if (k < noetig - 0.05) {
      const key = el.tagName + (el.className||'') + Math.round(k*10);
      if (gesehenK.has(key)) return;
      gesehenK.add(key);
      funde.push({ art: 'kontrast-zu-schwach',
        el: el.tagName.toLowerCase() + '.' + (el.className||'').toString().split(' ')[0],
        kontrast: Math.round(k*100)/100, noetig, text: t.slice(0,35) });
    }
  });

  return funde;
};

const browser = await chromium.launch();
let geprueft = 0, gesamt = 0;
const berichte = [];
const weitergeleitet = [];

async function arbeite(liste, breite, modus) {
  const ctx = await browser.newContext({ viewport:{width:breite,height:900}, colorScheme:modus });
  await ctx.addInitScript(() => { try{ localStorage.setItem('alpha-notice-seen','1'); localStorage.setItem('cookie-consent','accepted'); }catch(e){} });
  const p = await ctx.newPage();
  for (const pfad of liste) {
    const res = await p.goto(BASIS + pfad, { waitUntil:'domcontentloaded' }).catch(()=>null);
    if (!res || res.status() >= 400) { berichte.push(`FEHLT  ${pfad} -> ${res?res.status():'—'}`); continue; }
    await p.waitForTimeout(80);
    // Manche Seiten leiten sofort weiter (Sprach-Weiche, Paginierung). Dann
    // stirbt der Auswertungs-Kontext mitten im Messen - das ist kein Fehler
    // der Seite, sie wird nur an ihrem Ziel geprueft.
    try {
      await p.evaluate(() => Promise.all([...document.querySelectorAll('img')]
      .filter(i => { const r=i.getBoundingClientRect(); return r.top<innerHeight*2 && r.bottom>-innerHeight; })
      .map(i => i.complete ? null : new Promise(f => { const t=setTimeout(f,3000);
        i.addEventListener('load',()=>{clearTimeout(t);f();},{once:true});
        i.addEventListener('error',()=>{clearTimeout(t);f();},{once:true}); }))));
    } catch (e) { weitergeleitet.push(pfad); continue; }
    geprueft++;
    let funde;
    try { funde = await p.evaluate(pruefung); }
    catch (e) {
      if (/context was destroyed|Target closed|Execution context/.test(String(e.message))) {
        weitergeleitet.push(pfad); continue;
      }
      throw e;
    }
    if (funde.length) {
      gesamt += funde.length;
      berichte.push(`\n### ${modus} ${breite}px ${pfad}`);
      const gesehen = new Set();
      funde.forEach(f => { const k = JSON.stringify(f); if (!gesehen.has(k)) { gesehen.add(k); berichte.push('    ' + k); } });
    }
  }
  await ctx.close();
}

for (const modus of MODI) {
  for (const breite of BREITEN) {
    const teile = Array.from({length:PARALLEL}, (_,k) => PFADE.filter((_,i) => i % PARALLEL === k));
    await Promise.all(teile.map(t => arbeite(t, breite, modus)));
  }
}
console.log(berichte.join('\n'));
console.log(`\n==== ${geprueft} Seitenaufrufe geprueft, ${gesamt} Funde ====`);
if (weitergeleitet.length) console.log(`(${weitergeleitet.length} Aufrufe uebersprungen, weil die Seite weiterleitet: ${[...new Set(weitergeleitet)].slice(0,6).join(', ')}${weitergeleitet.length>6?' ...':''})`);
await browser.close();
