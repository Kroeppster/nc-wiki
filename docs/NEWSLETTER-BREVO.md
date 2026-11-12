# Newsletter mit Brevo einrichten

Anleitung, um den Newsletter von NCWiki mit **Brevo** (früher Sendinblue) aufzusetzen.
Der Einbau auf der Website ist fertig und live (`newsletter_url` in `hugo.toml` ist
gesetzt, siehe Schritt 5).

Die Menünamen beschreiben den Stand von Oktober/November 2026. Brevo ändert sie ab und zu – wenn
etwas leicht anders heisst, den sinngemässen Punkt suchen. Zeitaufwand: etwa 45 Minuten.
Für Schritt 2 braucht es die Person mit Zugang zur Domain nc-wiki.ch.

> **Hier nie Passwörter oder Zugangsdaten eintragen** – das Repository ist öffentlich.
> Die Formular-Adressen aus Schritt 4 sind dagegen unbedenklich.

## Stand

Abhaken, was erledigt ist (direkt in dieser Datei auf GitHub, Stift-Symbol):

- [x] 1. Konto angelegt (mit info@nc-wiki.ch)
- [ ] 2. Absender und Domain bestätigt – **Domain-Bestätigung (2b) noch offen, vor dem
  Live-Schalten der Anmeldung nötig** (sonst landen schon die Bestätigungsmails im Spam)
- [x] 3. Drei Listen angelegt (DE, FR, IT)
- [x] 4. Drei Anmeldeformulare angelegt (mit doppelter Bestätigung und Weiterleitung)
- [x] 5. Einbau auf der Website – live seit November 2026 (Test mit eigener Adresse
  erfolgreich). Offen: Weiterleitung nach der Bestätigung in allen drei Brevo-Formularen
  eintragen (Schritt 4.4), sonst zeigt Brevo nach dem Klick seine eigene Seite
- [ ] 6. Abmeldeseite geprüft
- [ ] 7. Erster Newsletter verschickt

Die drei Formular-Adressen (`…sibforms.com/serve/…`) stehen in **`data/newsletter.yaml`**
(je eine für DE, FR, IT). Legt ihr ein Formular in Brevo neu an, dort die neue Adresse
eintragen.

---

## Warum Brevo

| | Brevo | MailerLite | Mailchimp | Formspree (schon im Einsatz) |
| --- | --- | --- | --- | --- |
| Gratis-Plan | unbegrenzt Kontakte, ca. 300 Mails/Tag | bis ca. 1000 Kontakte | ca. 500 Kontakte | kein Newsletter-Dienst |
| Server | EU (Frankreich) | EU | USA | USA |
| Doppelte Bestätigung | ja | ja | ja | nein |
| Abmeldelink in jedem Mail | automatisch | automatisch | automatisch | von Hand |

Daten in der EU, keine Obergrenze bei den Kontakten, An- und Abmeldung rechtlich sauber.
Gratis-Grenzen vor dem Entscheid auf der Preisseite nachprüfen.

---

## Schritt 1: Konto anlegen

1. Auf **brevo.com** auf «Sign up free» gehen.
2. Mit der Vereinsadresse **info@nc-wiki.ch** registrieren, **nicht mit einer privaten
   Adresse**. Das Passwort im Passwort-Manager des Vereins ablegen.
3. Bestätigungsmail öffnen und auf den Link klicken.
4. Beim Profil den **Verein** als Firma angeben: Name «NCWiki», Adresse wie im Impressum.
   Die Adresse erscheint unten in jedem Newsletter (Pflicht).
5. Plan **Free** wählen.

**Login-Adresse später ändern:** geht, in der Regel unter **Mein Profil** bzw.
**Kontoeinstellungen → Login-E-Mail** (Brevo schickt eine Bestätigung an die neue Adresse).
Wer mit einer privaten Adresse startet, muss sie ändern, **bevor** die Person den Verein
verlässt. Die Absenderadresse der Newsletter ist davon unabhängig (siehe Schritt 2).

## Schritt 2: Absender und Domain bestätigen

Ohne diesen Schritt landen die Mails oft im Spam.

1. **Einstellungen → Absender, Domains & dedizierte IPs → Absender**: `info@nc-wiki.ch`
   mit dem Namen «NCWiki» hinzufügen und bestätigen.
2. **Domains**: `nc-wiki.ch` hinzufügen und **Authentifizieren** wählen.
3. Brevo zeigt 2–4 DNS-Einträge an (Brevo-Code, DKIM, DMARC). Die Person mit Domain-Zugang
   trägt sie beim Anbieter der Domain ein (dort, wo nc-wiki.ch registriert ist).
4. Nach einigen Minuten bis Stunden in Brevo auf **Überprüfen** klicken, bis alles grün ist.

Weitere Absender lassen sich jederzeit hinzufügen oder entfernen; Login, Listen und
Abonnent\*innen bleiben davon unberührt.

## Schritt 3: Drei Listen anlegen (eine je Sprache)

1. **Kontakte → Listen**: Ordner **«Newsletter»** erstellen.
2. Darin drei Listen: `Newsletter DE`, `Newsletter FR`, `Newsletter IT`.

So geht jede Ausgabe gezielt an eine Sprache.

## Schritt 4: Drei Anmeldeformulare (eines je Sprache)

Zuerst für Deutsch, danach gleich für FR und IT.

1. **Marketing → Formulare**, Reiter **«Anmeldung»** → **«Anmeldeformular erstellen»**,
   Name `Newsletter DE`. (Früher lag das unter «Kontakte → Formulare».)
2. **Felder:**
   - E-Mail (schon da)
   - **Einwilligungs-Häkchen** (DSGVO): «Ich möchte den Newsletter von NCWiki erhalten und
     habe die Datenschutzerklärung gelesen.»
   - Weitere Felder (z. B. Vorname) braucht es nicht: Das Formular auf der Website fragt nur
     die E-Mail-Adresse und das Häkchen ab.
   - Gestaltung egal – das Aussehen auf der Website wird dort gebaut.
3. **Liste:** `Newsletter DE`.
4. **Bestätigung:** **Doppelte Bestätigung (Double Opt-in)**.
   - Vorlage für die Bestätigungsmail wählen bzw. erstellen (Text in der jeweiligen Sprache).
   - **Weiterleitung nach Bestätigung:**
     - DE: `https://kroeppster.github.io/nc-wiki/newsletter-bestaetigt/`
     - FR: `https://kroeppster.github.io/nc-wiki/fr/newsletter-bestaetigt/`
     - IT: `https://kroeppster.github.io/nc-wiki/it/newsletter-bestaetigt/`

     (Diese Seiten gibt es auf der Website. Bleibt das Feld leer, klappt die Anmeldung
     trotzdem, Brevo zeigt nach dem Klick dann aber seine eigene graue Seite. Zieht die
     Website auf eine eigene Domain um, hier die Adressen anpassen.)
5. **Meldungen:** Erfolgs- und Fehlermeldung kurz in der Sprache anpassen (nur Ersatz – die
   Website zeigt eigene Texte).
6. **Speichern** → **Teilen → HTML-Code einbetten**.
7. Im Code steht eine Adresse wie `https://xxxxxxx.sibforms.com/serve/MUIFA…`.
   **Nur diese Adresse kopieren** und in `data/newsletter.yaml` bei der Sprache eintragen.

## Schritt 5: Einbau auf der Website

Erledigt und live:

- Seiten «Einschreiben» (DE/FR/IT, `newsletter_form: true` im Seitenkopf) mit eigenem
  Formular (`layouts/partials/newsletter-form.html`). Es schickt E-Mail-Adresse,
  Einwilligung und Sprache an das Brevo-Formular der Seitensprache aus
  `data/newsletter.yaml` – so landet die Person in der richtigen Liste und bekommt die
  Bestätigungsmail in ihrer Sprache.
- Seiten «Anmeldung bestätigt» (`newsletter-bestaetigt.md`, DE/FR/IT) – Ziel der
  Weiterleitung aus Schritt 4. Sie tragen `noindex: true`: nie in Suchmaschinen, Sitemap
  oder Website-Suche, man erreicht sie nur über den Link in der Bestätigungsmail.
- Seiten «Abmelden» mit Erklärung zum Abmeldelink in jedem Newsletter.
- Abschnitt «Newsletter» in der Datenschutzerklärung (DE/FR/IT) und Brevo unter «Dienste
  von Dritten».
- Prüfung in `scripts/verhalten-pruefen.mjs`: Die Anfrage an Brevo wird abgefangen, es geht
  nie eine echte Anmeldung raus.

**Live schalten** (so wurde es gemacht; gilt auch, falls der Newsletter einmal
vorübergehend ausgeblendet war – dafür `newsletter_url = ''` setzen):

1. Mit einer eigenen Adresse testen, je Sprache: Die Seiten sind schon jetzt direkt
   erreichbar, z. B. `https://kroeppster.github.io/nc-wiki/newsletter-einschreiben/`
   (bzw. `/fr/…`, `/it/…`). Prüfen: Bestätigungsmail kommt an (nicht im Spam), der Link
   darin führt auf «Anmeldung bestätigt», der Kontakt steht danach in der richtigen Liste.
2. In `hugo.toml` `newsletter_url = '/newsletter-einschreiben/'` setzen. Dann erscheinen
   der Newsletter-Teil in der Fusszeile und der Knopf «Newsletter abonnieren» auf der
   Startseite, und die Seiten «Einschreiben»/«Abmelden» kommen in Suche und Sitemap.

## Schritt 6: Abmelden einrichten (einmalig)

1. **Einstellungen → Abmeldeseite / Abmeldeformular** prüfen, dass die Abmeldung per Klick
   funktioniert.
2. Texte möglichst neutral oder dreisprachig, z. B. «Du bist abgemeldet / Tu es
   désinscrit·e / Sei disiscritto·a».

Den Abmeldelink unten in jedem Newsletter fügt Brevo automatisch ein. Ein eigenes
Abmeldeformular braucht es deshalb nicht; die Seite «Abmelden» auf der Website erklärt das
und nennt info@nc-wiki.ch für Fälle, in denen der Link nicht weiterhilft.

## Schritt 7: Ersten Newsletter verschicken

1. **Kampagnen → E-Mail → Kampagne erstellen**, Name z. B. «Newsletter Oktober 2026 DE».
2. Empfänger: Liste `Newsletter DE`.
3. Absender `NCWiki <info@nc-wiki.ch>`, Betreff eingeben.
4. Im Drag-and-Drop-Editor gestalten; als Vorlage speichern, um sie für FR und IT
   wiederzuverwenden.
5. **Test senden** an euch selbst, auf dem Handy anschauen.
6. **Planen** oder **Jetzt senden**.
7. Für FR und IT kopieren, Text und Liste austauschen.

## Gut zu wissen

- **Gratis-Plan:** ca. 300 Mails pro Tag. Bei mehr Abonnent\*innen den Versand auf mehrere
  Tage verteilen (z. B. eine Sprache pro Tag). Unten im Mail steht ein kleines Brevo-Logo.
- **Mehrere Personen:** **Einstellungen → Benutzer** – im Gratis-Plan evtl. begrenzt, dann
  das Vereinskonto teilen.
- **Öffnungs- und Klickstatistik:** Die Datenschutzerklärung sagt, dass Brevo erfasst, ob
  ein Newsletter geöffnet und welche Links angeklickt werden (so ist Brevo eingestellt,
  wenn man nichts ändert). Schaltet ihr das in Brevo ab, den Satz im Abschnitt
  «Newsletter» der Datenschutzerklärung (DE/FR/IT) streichen.
- **Datenschutz:** Kontakte **nie** von Hand importieren, wenn die Personen nicht selbst
  zugestimmt haben (z. B. aus alten Kurs-Anmeldelisten). Nur wer sich über das Formular
  angemeldet und bestätigt hat, bekommt den Newsletter.
