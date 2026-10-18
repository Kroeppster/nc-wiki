#!/usr/bin/env python3
"""
================================================================================
NEUE SAISON: DAS AKTUELLE TEAM INS ARCHIV
================================================================================
    python3 scripts/texte_saison.py 2026/27            # alle drei Sprachen
    python3 scripts/texte_saison.py 2026/27 --probe    # nur zeigen

Wird auch von .github/workflows/neue-saison.yml (Knopf "Run workflow" auf
GitHub) und beim Einlesen einer Mappe benutzt (Feld "Neue Saison" im Blatt
"Team - Ansicht").

WAS PASSIERT, je Sprache:
  1. Auf der Team-Seite (content/<sprache>/ueber-uns/team/_index.md) stehen
     Ueberschriften "## ..." mit der laufenden Saison wie 2025/26 darin
     ("Leitungsteam 2025/26", "Weitere Verantwortliche 2025/26"). Die erste
     davon nennt die Saison, der Abschnitt unter der letzten ist das Team.
  2. Ins Archiv (content/<sprache>/ueber-uns/archiv/_index.md) kommt vor die
     erste "## "-Ueberschrift ein neuer Abschnitt "## Saison 2025/26" (FR
     "Saison", IT "Stagione"): darin "### Leitungsteam" als Liste (aus dem
     Feld "ressorts" im Seitenkopf) und danach der Team-Abschnitt - so wie
     die frueheren Saisons im Archiv aufgebaut sind.
  3. Auf der Team-Seite tragen die Ueberschriften danach die neue Saison, und
     der Team-Abschnitt enthaelt nur einen Platzhalter-Satz. Das Leitungsteam
     (ressorts) BLEIBT stehen - meist bleibt ein Teil der Leute, und so muss
     man nur aendern, wer wechselt (Blatt "Team - Ansicht" in der Mappe).

Laeuft ein zweites Mal mit derselben Saison: nichts passiert (die Saison ist
schon die aktuelle). So schadet es nicht, wenn zwei Sprach-Mappen dieselbe
neue Saison eintragen.
================================================================================
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texte_bausteine as tb

PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEAM = 'content/{s}/ueber-uns/team/_index.md'
ARCHIV = 'content/{s}/ueber-uns/archiv/_index.md'
SAISON = re.compile(r'^\d{4}/\d{2}$')
TEXTE = {
    'de': dict(saison='Saison {s}', leitung='Leitungsteam',
               platzhalter='Die weiteren Verantwortlichen dieser Saison stellen wir hier bald vor.'),
    'fr': dict(saison='Saison {s}', leitung='Équipe dirigeante',
               platzhalter='Nous présenterons bientôt ici les autres responsables de cette saison.'),
    'it': dict(saison='Stagione {s}', leitung='Team dirigente',
               platzhalter='Presto presenteremo qui gli altri responsabili di questa stagione.'),
}


def lesen(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def schreiben(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def leitung_als_liste(kopf):
    import yaml
    daten = yaml.safe_load(kopf.strip().strip('-')) or {}
    zeilen = []
    for r in daten.get('ressorts') or []:
        leute = ', '.join('%s (%s)' % (m.get('name', ''), m.get('rolle', '')) if m.get('rolle') else m.get('name', '')
                          for m in r.get('mitglieder') or [] if m.get('name'))
        if leute:
            zeilen.append('- **%s:** %s' % (r.get('titel', ''), leute))
    return '\n'.join(zeilen)


def wechsel_sprache(projekt, sprache, neu, probe=False):
    """Gibt eine Meldung zurueck (str) oder None, wenn nichts zu tun war."""
    tp, ap = (os.path.join(projekt, x.format(s=sprache)) for x in (TEAM, ARCHIV))
    if not (os.path.isfile(tp) and os.path.isfile(ap)):
        return None
    roh = lesen(tp)
    kopf, koerper, _ = tb.kopf_trennen(roh)
    titel = list(re.finditer(r'^## (.*?(\d{4}/\d{2}))[ \t]*$', koerper, re.MULTILINE))
    if not titel:
        return f'{sprache}: auf der Team-Seite keine Überschrift mit einer Saison (z. B. "## Weitere Verantwortliche 2025/26") gefunden - nichts archiviert.'
    alt = titel[0].group(2)
    if alt == neu:
        return None
    m = titel[-1]
    ende = re.search(r'^## ', koerper[m.end():], re.MULTILINE)
    ende = m.end() + ende.start() if ende else len(koerper)
    inhalt = koerper[m.end():ende].strip()
    teile = ['## ' + TEXTE[sprache]['saison'].format(s=alt)]
    leitung = leitung_als_liste(kopf)
    if leitung:
        teile.append('### %s\n\n%s' % (TEXTE[sprache]['leitung'], leitung))
    if inhalt and inhalt != TEXTE[sprache]['platzhalter']:
        teile.append(inhalt)
    block = '\n\n'.join(teile) + '\n\n'

    aroh = lesen(ap)
    akopf, akoerper, _ = tb.kopf_trennen(aroh)
    h = re.search(r'^## ', akoerper, re.MULTILINE)
    if h:
        akoerper = akoerper[:h.start()] + block + akoerper[h.start():]
    else:
        akoerper = akoerper.rstrip('\n') + '\n\n' + block
    neuer_koerper = (koerper[:m.start()] + '## ' + m.group(1).replace(alt, neu) + '\n\n'
                     + TEXTE[sprache]['platzhalter'] + '\n\n' + koerper[ende:].lstrip('\n'))
    for t in reversed(titel[:-1]):
        neuer_koerper = (neuer_koerper[:t.start()] + '## ' + t.group(1).replace(alt, neu)
                         + neuer_koerper[t.end():])
    if not probe:
        schreiben(ap, akopf + akoerper.rstrip('\n') + '\n')
        schreiben(tp, kopf + neuer_koerper.rstrip('\n') + '\n')
    return f'{sprache}: Saison {alt} ins Archiv verschoben, neue Saison {neu} begonnen.'


def saison_wechsel(projekt, neu, probe=False, sprachen=tb.SPRACHEN):
    neu = neu.strip()
    if not SAISON.match(neu):
        return [f'"{neu}" ist keine Saison - bitte in der Form 2026/27 angeben.']
    return [x for x in (wechsel_sprache(projekt, s, neu, probe) for s in sprachen) if x]


def main():
    ap = argparse.ArgumentParser(description='Neue Saison: aktuelles Team ins Archiv.')
    ap.add_argument('saison', help='die neue Saison, z. B. 2026/27')
    ap.add_argument('--probe', action='store_true')
    ap.add_argument('--projekt', default=PROJEKT)
    a = ap.parse_args()
    meldungen = saison_wechsel(a.projekt, a.saison, a.probe)
    print('\n'.join(meldungen) or 'Nichts zu tun - die Saison ist schon die aktuelle.')
    if meldungen and meldungen[0].startswith('"'):
        sys.exit(1)


if __name__ == '__main__':
    main()
