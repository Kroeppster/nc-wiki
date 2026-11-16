#!/usr/bin/env python3
"""
================================================================================
EXTERNE LINKS DER GEBAUTEN WEBSITE PRÜFEN
================================================================================
    hugo --minify
    python3 scripts/links-extern-pruefen.py public

Ruft jede Adresse, die auf eine ANDERE Website zeigt, einmal auf und meldet,
was nicht mehr geht - mit den Seiten, auf denen der Link steht. Läuft einmal
pro Woche in .github/workflows/links-extern.yml; das Ergebnis steht dort in der
Zusammenfassung des Laufs.

WARUM EIN EIGENES SKRIPT: Bis November 2026 prüfte das Werkzeug "lychee". Bei
rund 45 Adressen blieb es einmal 20 Minuten hängen und wurde abgebrochen, ohne
ein einziges Ergebnis zu zeigen. Hier hat jeder Abruf eine feste Obergrenze
(ZEIT Sekunden, bis zu drei Versuche), der ganze Lauf dauert höchstens ein paar
Minuten, und was nicht prüfbar ist, wird trotzdem aufgelistet.

VIER ERGEBNISSE je Adresse:
  in Ordnung       Antwort 200-399.
  kaputt           Die Seite gibt es nicht mehr (404/410) oder die Adresse
                   der Website ist unbekannt (kein solcher Server). Nur das
                   macht den Lauf rot.
  gestört          Die andere Website antwortet mit einem Serverfehler (5xx)
                   oder gar nicht - auch nach drei Versuchen mit Pausen. Das
                   ist fast immer vorübergehend (am 16. November 2026 gab
                   www.unibas.ch einmal 502 und machte den Lauf rot, obwohl
                   der Link stimmt). Wird nur aufgelistet; steht dieselbe
                   Adresse zwei Wochen hintereinander hier, nachsehen.
  nicht prüfbar    401/403/405/429: Die Website weist automatische Abrufe ab
                   (z.B. usi.ch, Instagram), im Browser geht der Link meist.
                   Wird nur aufgelistet - ab und zu von Hand anklicken.

AUSGELASSEN: die eigene Website (localhost, ohne Adresse gebaut) und die
Empfänger der Formulare (Formspree, Brevo) - sie nehmen nur abgeschickte
Formulare an.

ADRESSEN AUSPROBIEREN: Zusätzliche Adressen in der Umgebungsvariable PROBE
(durch Leerzeichen getrennt) werden mitgeprüft - praktisch, um die richtige
Adresse für einen toten Link zu finden (im Workflow: Feld "adressen").
Mit SUCHE (ein Wortteil, z.B. "medicin") listet das Skript zusätzlich die
Links auf, die auf den ausprobierten Seiten stehen und das Wort enthalten -
so findet man die neue Adresse über die Übersichtsseite der anderen Website.
================================================================================
"""
import concurrent.futures
import glob
import html
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request

ZEIT = 12          # Sekunden je Versuch
GLEICHZEITIG = 8
PAUSEN = (0, 5, 20)  # Sekunden vor dem ersten, zweiten und dritten Versuch
AUSLASSEN = re.compile(r'^https?://(localhost|127\.0\.0\.1)|^https://formspree\.io/|sibforms\.com')
NICHT_PRUEFBAR = {401, 403, 405, 429, 999}
KOPF = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8', 'Accept-Language': 'de-CH,de;q=0.9,fr;q=0.8,it;q=0.7'}


def sammeln(ordner):
    """Adresse -> Seiten, auf denen sie steht."""
    wo = {}
    for datei in sorted(glob.glob(os.path.join(ordner, '**', '*.html'), recursive=True)):
        with open(datei, encoding='utf-8', errors='replace') as f:
            text = f.read()
        seite = '/' + os.path.relpath(datei, ordner).replace(os.sep, '/').replace('index.html', '')
        for m in re.finditer(r'(?:href|src)=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))', text):
            adresse = html.unescape(m.group(1) or m.group(2) or m.group(3)).split('#')[0]
            if re.match(r'^https?://', adresse) and not AUSLASSEN.search(adresse):
                wo.setdefault(adresse, set()).add(seite)
    return wo


def abrufen(adresse):
    """-> ('ok' | 'kaputt' | 'gestoert' | 'unklar', Begründung)"""
    grund = ''
    for pause in PAUSEN:
        time.sleep(pause)
        try:
            anfrage = urllib.request.Request(urllib.request.quote(adresse, safe=':/?&=%#@+,;~!$*()\''), headers=KOPF)
            with urllib.request.urlopen(anfrage, timeout=ZEIT) as antwort:
                antwort.read(256)
                return 'ok', str(antwort.status)
        except urllib.error.HTTPError as e:
            if e.code in NICHT_PRUEFBAR:
                return 'unklar', 'Antwort %d' % e.code
            grund = 'Antwort %d' % e.code
            if e.code < 500:      # 404, 410 und andere endgültige Antworten
                return 'kaputt', grund
        except Exception as e:  # kein Server, Zeitüberschreitung, Zertifikat ...
            ursache = getattr(e, 'reason', e)
            grund = type(e).__name__ + ': ' + str(ursache)[:80]
            if isinstance(ursache, socket.gaierror):   # diese Website gibt es nicht (mehr)
                return 'kaputt', grund
    return 'gestoert', grund


def main():
    ordner = sys.argv[1] if len(sys.argv) > 1 else 'public'
    wo = sammeln(ordner)
    for adresse in os.environ.get('PROBE', '').split():
        wo.setdefault(adresse, set()).add('(zum Ausprobieren angegeben)')
    if not wo:
        sys.exit('Keine externen Links gefunden - ist "%s" die gebaute Website?' % ordner)
    adressen = sorted(wo)
    with concurrent.futures.ThreadPoolExecutor(GLEICHZEITIG) as becken:
        ergebnisse = dict(zip(adressen, becken.map(abrufen, adressen)))
    kaputt = [a for a in adressen if ergebnisse[a][0] == 'kaputt']
    unklar = [a for a in adressen if ergebnisse[a][0] == 'unklar']
    gestoert = [a for a in adressen if ergebnisse[a][0] == 'gestoert']
    z = ['## Externe Links', '',
         '%d Adressen geprüft: **%d in Ordnung, %d kaputt, %d gestört, %d nicht prüfbar.**' % (
             len(adressen), len(adressen) - len(kaputt) - len(unklar) - len(gestoert), len(kaputt), len(gestoert), len(unklar)), '']
    for titel, liste in (('Kaputt – bitte ersetzen', kaputt),
                         ('Gestört – die andere Website antwortet im Moment nicht richtig; nur nachsehen, wenn es nächste Woche wieder hier steht', gestoert),
                         ('Nicht prüfbar – die Website weist automatische Abrufe ab, von Hand anklicken', unklar)):
        if liste:
            z += ['### ' + titel, '']
            for a in liste:
                seiten = sorted(wo[a])
                z.append('- %s (%s) – steht auf %s%s' % (a, ergebnisse[a][1], ', '.join('`%s`' % s for s in seiten[:6]),
                                                       ' und %d weiteren' % (len(seiten) - 6) if len(seiten) > 6 else ''))
            z.append('')
    probe = [a for a in os.environ.get('PROBE', '').split()]
    if probe:
        z += ['### Ausprobiert', ''] + ['- %s → %s (%s)' % (a, ergebnisse[a][0], ergebnisse[a][1]) for a in probe] + ['']
    suche = os.environ.get('SUCHE', '').strip().lower()
    if probe and suche:
        z += ['### Links mit «%s» auf den ausprobierten Seiten' % suche, '']
        for a in probe:
            if ergebnisse[a][0] != 'ok':
                continue
            try:
                with urllib.request.urlopen(urllib.request.Request(a, headers=KOPF), timeout=ZEIT) as antwort:
                    text = antwort.read(2_000_000).decode('utf-8', 'replace')
            except Exception as e:
                z.append('- %s: nicht lesbar (%s)' % (a, type(e).__name__))
                continue
            alle = (m.group(1) or m.group(2) or m.group(3) for m in re.finditer(r'href=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))', text))
            gefunden = sorted({html.unescape(g) for g in alle if suche in g.lower()})
            z += ['- %s:' % a] + ['  - %s' % g for g in gefunden[:40]] if gefunden else ['- %s: nichts gefunden' % a]
        z.append('')
    bericht = '\n'.join(z)
    print(bericht)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as f:
            f.write(bericht + '\n')
    sys.exit(1 if kaputt else 0)


if __name__ == '__main__':
    main()
