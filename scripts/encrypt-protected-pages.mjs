/*
 * ============================================================================
 * PASSWORTSCHUTZ FÜR DEN MITGLIEDERBEREICH
 * ============================================================================
 * Dieses Skript läuft ganz am Ende des Bauens der Website, kurz bevor sie
 * veröffentlicht wird (siehe .github/workflows/hugo.yml). Es sucht im fertig
 * gebauten Ordner "public/" alle Seiten heraus, die im Frontmatter
 * "geschuetzt: true" stehen hatten, und legt eine Passwort-Abfrage davor.
 *
 * Wie es die richtigen Seiten erkennt: layouts/partials/head.html schreibt in
 * genau diese Seiten eine unsichtbare Markierung (<meta name="ncwiki-
 * geschuetzt">) sowie die Beschriftungen für die Passwort-Abfrage (Titel,
 * Hinweistext, Knopf...) aus i18n/de|fr|it.yaml. Dieses Skript liest beides
 * wieder aus - so bleiben alle sichtbaren Texte an der gewohnten Stelle
 * pflegbar, obwohl die Passwort-Seite selbst nicht von Hugo gebaut wird.
 *
 * Verschlüsselt wird mit StatiCrypt (ein fertiges, verbreitetes Werkzeug,
 * siehe package.json). Aus der fertigen Seite wird dabei ein unlesbarer
 * Zeichensalat, der erst im Browser der Besucherin wieder zusammengesetzt
 * wird, nachdem sie das richtige Passwort eingegeben hat.
 *
 * ---------------------------------------------------------------------------
 * WAS DIESER SCHUTZ LEISTET - UND WAS NICHT
 * ---------------------------------------------------------------------------
 * Er hält Suchmaschinen und zufällige Besucher:innen zuverlässig fern. Er ist
 * KEIN richtiger Login:
 *
 *  - Alle Mitglieder teilen sich EIN Passwort. Wer es weitergibt, kann nicht
 *    einzeln ausgesperrt werden - es hilft nur, das Passwort für alle zu
 *    ändern.
 *  - Der verschlüsselte Zeichensalat liegt öffentlich im Netz. Wer ihn
 *    herunterlädt, kann in aller Ruhe Passwörter durchprobieren, ohne dass
 *    das jemand mitbekommt oder bremsen könnte. Deshalb MUSS das Passwort
 *    lang und zufällig sein (siehe docs/WARTUNG.md) - ein kurzes oder
 *    erratbares Passwort ist hier praktisch kein Schutz.
 *  - Die verlinkten PDF-Dateien sind NICHT geschützt (siehe
 *    assets/downloads/mitglieder/README.md).
 *
 * Kurz: gut genug für interne Termine und Formulare, NICHT geeignet für
 * Personendaten, Finanzunterlagen oder sonst irgendetwas, dessen
 * Veröffentlichung echten Schaden anrichten würde.
 *
 * ---------------------------------------------------------------------------
 * AUFRUF
 * ---------------------------------------------------------------------------
 *   node scripts/encrypt-protected-pages.mjs [ordner] [--ohne-passwort-erlauben]
 *
 * "ordner" ist der fertig gebaute Website-Ordner (Standard: "public").
 * Das Passwort kommt aus der Umgebungsvariable STATICRYPT_PASSWORD, die im
 * Workflow aus dem GitHub-Secret MITGLIEDER_PASSWORT befüllt wird.
 *
 * Fehlt das Passwort, bricht das Skript mit einem Fehler ab - ABSICHTLICH:
 * sonst würden die Seiten unbemerkt unverschlüsselt online gehen. Nur mit
 * "--ohne-passwort-erlauben" wird stattdessen bloss gewarnt; das wird für
 * lokale Test-Builds und für Pull-Request-Prüfläufe verwendet, die ohnehin
 * nie veröffentlicht werden.
 * ============================================================================
 */

import { readdirSync, readFileSync, writeFileSync, mkdtempSync, rmSync, existsSync } from "node:fs";
import { join, basename, relative } from "node:path";
import { tmpdir } from "node:os";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

// --- Aufrufparameter -------------------------------------------------------
const args = process.argv.slice(2);
const ohnePasswortErlauben = args.includes("--ohne-passwort-erlauben");
const zielOrdner = args.find((a) => !a.startsWith("--")) || "public";

// Farben der Website (assets/css/style.css: --color-signal / --color-paper),
// damit die Passwort-Abfrage nicht nach fremdem Werkzeug aussieht.
const FARBE_PRIMAER = "#223FCB";
const FARBE_HINTERGRUND = "#F5F7FB";

// --- Kleine Helfer ---------------------------------------------------------

/** Alle .html-Dateien unterhalb eines Ordners einsammeln. */
function htmlDateien(ordner) {
  const gefunden = [];
  for (const eintrag of readdirSync(ordner, { withFileTypes: true })) {
    const pfad = join(ordner, eintrag.name);
    if (eintrag.isDirectory()) gefunden.push(...htmlDateien(pfad));
    else if (eintrag.name.endsWith(".html")) gefunden.push(pfad);
  }
  return gefunden;
}

/** &amp; & Co. wieder in echte Zeichen zurückverwandeln. */
function echteZeichen(text) {
  return text
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#34;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, "&");
}

/**
 * Den Inhalt einer <meta name="...">-Angabe herauslesen.
 * Muss tolerant sein: "hugo --minify" lässt die Anführungszeichen weg, wo sie
 * technisch nicht nötig sind (aus content="ja" wird content=ja).
 */
function metaInhalt(html, name) {
  const tag = html.match(new RegExp("<meta[^>]*\\bname=([\"']?)" + name + "\\1[\\s>][^>]*>", "i"));
  if (!tag) return "";
  const wert = tag[0].match(/\bcontent=(?:"([^"]*)"|'([^']*)'|([^\s>]+))/i);
  if (!wert) return "";
  return echteZeichen(wert[1] ?? wert[2] ?? wert[3] ?? "");
}

/** Erkennt an der Markierung aus head.html, ob eine Seite geschützt gehört. */
const MARKIERUNG = /<meta[^>]*\bname=(["']?)ncwiki-geschuetzt\1[\s>]/i;

// --- 1. Betroffene Seiten suchen -------------------------------------------
if (!existsSync(zielOrdner)) {
  console.error(`FEHLER: Der Ordner "${zielOrdner}" existiert nicht. Zuerst die Website bauen (npm run build).`);
  process.exit(1);
}

const geschuetzte = htmlDateien(zielOrdner).filter((datei) =>
  MARKIERUNG.test(readFileSync(datei, "utf8"))
);

if (geschuetzte.length === 0) {
  console.log("Keine geschützten Seiten gefunden - nichts zu tun.");
  console.log('(Geschützt = "geschuetzt: true" im Frontmatter, siehe content/*/mitglieder/.)');
  process.exit(0);
}

console.log(`${geschuetzte.length} geschützte Seite(n) gefunden:`);
for (const d of geschuetzte) {
  console.log("  - " + relative(zielOrdner, d).split("\\").join("/"));
}

// --- 2. Passwort prüfen ----------------------------------------------------
const passwort = process.env.STATICRYPT_PASSWORD || "";

if (!passwort) {
  const text =
    "Kein Passwort gesetzt (Umgebungsvariable STATICRYPT_PASSWORD ist leer).\n" +
    "Im Workflow wird sie aus dem GitHub-Secret MITGLIEDER_PASSWORT befüllt -\n" +
    "fehlt das Secret, ist es dort nicht (oder falsch benannt) hinterlegt.\n" +
    'Siehe docs/WARTUNG.md, Abschnitt "Mitgliederbereich".';
  if (ohnePasswortErlauben) {
    console.warn("\nWARNUNG: " + text);
    console.warn("Die Seiten bleiben deshalb UNVERSCHLÜSSELT. Das ist bei lokalen Test-Builds und");
    console.warn("Pull-Request-Prüfläufen so gewollt - veröffentlicht wird dabei nichts.\n");
    process.exit(0);
  }
  console.error("\nFEHLER: " + text + "\n");
  console.error("Abbruch, damit die Seiten nicht versehentlich unverschlüsselt online gehen.");
  process.exit(1);
}

if (passwort.length < 16) {
  console.warn(
    `\nWARNUNG: Das Passwort ist mit ${passwort.length} Zeichen kurz. Weil der verschlüsselte\n` +
    "Inhalt öffentlich im Netz liegt, kann man Passwörter unbemerkt und beliebig oft\n" +
    "durchprobieren - empfohlen sind mindestens 16 zufällige Zeichen (siehe docs/WARTUNG.md).\n"
  );
}

// --- 3. Verschlüsseln ------------------------------------------------------
// StatiCrypt direkt über Node aufrufen (statt über npx), damit es auf Windows
// und auf dem Linux-Server von GitHub gleich funktioniert.
const staticryptCli = require.resolve("staticrypt/cli/index.js");
const arbeitsordner = mkdtempSync(join(tmpdir(), "ncwiki-schutz-"));
let fehler = 0;

try {
  for (const [nummer, datei] of geschuetzte.entries()) {
    const html = readFileSync(datei, "utf8");
    const ausgabeOrdner = join(arbeitsordner, String(nummer));

    // Beschriftungen der Passwort-Abfrage - kommen aus i18n/<sprache>.yaml und
    // stecken als <meta>-Angaben in der Seite (siehe head.html). Fehlt eine,
    // nimmt StatiCrypt seinen eigenen englischen Standardtext.
    const beschriftung = [];
    const uebernehmen = (metaName, option) => {
      const wert = metaInhalt(html, metaName);
      if (wert) beschriftung.push(option, wert);
    };
    uebernehmen("ncwiki-schutz-titel", "--template-title");
    uebernehmen("ncwiki-schutz-hinweis", "--template-instructions");
    uebernehmen("ncwiki-schutz-button", "--template-button");
    uebernehmen("ncwiki-schutz-platzhalter", "--template-placeholder");
    uebernehmen("ncwiki-schutz-fehler", "--template-error");

    execFileSync(
      process.execPath,
      [
        staticryptCli,
        datei,
        // "-c false": keine .staticrypt.json-Konfigurationsdatei anlegen.
        "-c", "false",
        // "--remember false": kein "Angemeldet bleiben"-Häkchen. Das würde das
        // Passwort im Browser speichern - auf gemeinsam genutzten Geräten
        // (Uni-Rechner!) unerwünscht.
        "--remember", "false",
        "-d", ausgabeOrdner,
        "--template-color-primary", FARBE_PRIMAER,
        "--template-color-secondary", FARBE_HINTERGRUND,
        ...beschriftung,
      ],
      {
        // Das Passwort wird NICHT als Aufrufparameter übergeben (das wäre in
        // der Prozessliste des Rechners mitlesbar), sondern über die
        // Umgebung - StatiCrypt liest STATICRYPT_PASSWORD von sich aus.
        env: process.env,
        stdio: ["ignore", "pipe", "pipe"],
      }
    );

    // StatiCrypt legt die fertige Datei unter ihrem blossen Dateinamen ab
    // (bei Hugo heissen praktisch alle Seiten "index.html", deshalb bekommt
    // jede ihren eigenen Unterordner).
    const erzeugt = join(ausgabeOrdner, basename(datei));
    if (!existsSync(erzeugt)) {
      console.error(`FEHLER: StatiCrypt hat für ${datei} keine Ausgabe erzeugt.`);
      fehler++;
      continue;
    }

    let verschluesselt = readFileSync(erzeugt, "utf8");

    // Sicherheitsnetz: Die Passwort-Abfrage von StatiCrypt bringt selbst KEIN
    // "noindex" mit - ohne diese Zeile dürfte eine Suchmaschine ausgerechnet
    // die Hülle indexieren und damit die Adresse der geschützten Seite in den
    // Suchergebnissen auftauchen lassen. Das "noindex" aus head.html hilft
    // hier nicht: das steckt jetzt mit im verschlüsselten Teil.
    verschluesselt = verschluesselt.replace(
      /<head>/i,
      '<head>\n        <meta name="robots" content="noindex, nofollow" />'
    );

    // Letzte Kontrolle vor dem Überschreiben: Ist der Klartext wirklich weg?
    // Sollte sich StatiCrypt einmal anders verhalten als erwartet, bricht der
    // Build lieber ab, statt stillschweigend Klartext zu veröffentlichen.
    if (MARKIERUNG.test(verschluesselt)) {
      console.error(`FEHLER: ${datei} sieht nach dem Verschlüsseln immer noch unverschlüsselt aus.`);
      fehler++;
      continue;
    }

    writeFileSync(datei, verschluesselt, "utf8");
  }
} finally {
  rmSync(arbeitsordner, { recursive: true, force: true });
}

if (fehler > 0) {
  console.error(`\n${fehler} Seite(n) konnten nicht geschützt werden - Abbruch.`);
  process.exit(1);
}

console.log(`\nFertig: ${geschuetzte.length} Seite(n) mit Passwort geschützt.`);
