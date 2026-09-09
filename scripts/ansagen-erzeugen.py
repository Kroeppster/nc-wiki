# -*- coding: utf-8 -*-
"""Erzeugt die Ansagen des Prüfungsmodus als MP3-Dateien.

WOZU: Die Seite /ems/pruefungsmodus/ liest die Ansagen sonst mit der
Sprachausgabe des Browsers vor - die klingt je nach Gerät unterschiedlich und
teilweise ziemlich blechern. Diese Dateien geben allen dieselbe, ruhigere
Stimme.

DIE TEXTE STEHEN NICHT HIER. Das Skript liest sie aus der GEBAUTEN Seite
(public/.../pm-daten). Damit ist ausgeschlossen, dass die Aufnahme etwas
anderes sagt als der Bildschirm - es gibt nur eine Quelle, nämlich
i18n/*.yaml und data/testablauf.yaml.

NEU ERZEUGEN (nötig, sobald sich ein pm_-Text oder eine Bearbeitungszeit
ändert):

    npm run build                 # public/ muss aktuell sein
    python3 -m venv .venv && .venv/bin/pip install piper-tts lameenc
    # Stimmen holen (einmalig, liegen NICHT im Repo - zu gross):
    #   https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz
    #   https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-fr-siwis-medium.tar.gz
    # entpacken nach voices/<name>/
    .venv/bin/python scripts/ansagen-erzeugen.py assets/audio/pruefungsmodus

BESSER ALS DIESES SKRIPT sind echte Aufnahmen von Vereinsmitgliedern. Sobald
eine Datei von Hand eingesprochen wird, einfach die erzeugte überschreiben -
die Seite merkt keinen Unterschied. Welche Datei welchen Satz enthält, steht
in assets/audio/pruefungsmodus/README.md.

STIMMEN UND LIZENZEN:
  Deutsch      Thorsten (piper, low)  - Datensatz CC0, keine Auflagen
  Französisch  SIWIS (piper, medium)  - Datensatz CC-BY 4.0, Namensnennung
                                        nötig (siehe README.md im Audio-Ordner)
  Italienisch  bewusst NICHT erzeugt: Die Lizenz des verfügbaren italienischen
               Datensatzes (M-AILABS) war nicht eindeutig zu klären. Italienisch
               liest weiterhin die Sprachausgabe des Browsers vor - das
               funktioniert, klingt nur weniger gut.
"""
import io, json, os, re, sys, wave
from piper import PiperVoice, SynthesisConfig
import lameenc

# Verzeichnis, in dem gearbeitet wird: das Repo-Wurzelverzeichnis
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(SP, 'public')
ZIEL = sys.argv[1]
SPRACHEN = {
    'de': (os.path.join(SP, 'voices/de-thorsten-low/de-thorsten-low.onnx'), 'ems/pruefungsmodus/index.html'),
    'fr': (os.path.join(SP, 'voices/fr-siwis-medium/fr-siwis-medium.onnx'), 'fr/ems/pruefungsmodus/index.html'),
}

def saetze(html_pfad):
    s = io.open(html_pfad, encoding='utf-8').read()
    d = json.loads(re.search(r'id=pm-daten[^>]*>(.*?)</script>', s, re.S).group(1))
    t = d['texte']
    raus = {}
    for b in d['bloecke']:
        raus[b['key']] = b['ansage']
    raus['beginne'] = t['beginne']
    # Die zusammengesetzten Sätze müssen als EIN Stück aufgenommen werden -
    # genau so ruft das Skript sie auf (siehe pruefungsmodus.html).
    raus['stopp-weiter'] = t['stopp'] + ' ' + t['stoppWeiter']
    raus['fertig-einzeln'] = t['stopp'] + ' ' + t['fertigEinzeln']
    raus['fertig-komplett'] = t['stopp'] + ' ' + t['fertigKomplett']
    return raus

def mp3_schreiben(pfad, pcm, rate, kanaele):
    enc = lameenc.Encoder()
    enc.set_bit_rate(96)
    enc.set_in_sample_rate(rate)
    enc.set_channels(kanaele)
    enc.set_quality(2)
    daten = enc.encode(pcm) + enc.flush()
    with open(pfad, 'wb') as f:
        f.write(daten)
    return len(daten)

gesamt = 0
for lang, (modell, seite) in SPRACHEN.items():
    stimme = PiperVoice.load(modell)
    # Etwas langsamer als Normaltempo: Das hier vertritt eine Aufsichtsperson,
    # die deutlich und ohne Eile ansagt.
    konf = SynthesisConfig(length_scale=1.12)
    ordner = os.path.join(ZIEL, lang)
    os.makedirs(ordner, exist_ok=True)
    for name, text in saetze(os.path.join(PUBLIC, seite)).items():
        wav_pfad = os.path.join(ordner, name + '.wav')
        with wave.open(wav_pfad, 'wb') as w:
            stimme.synthesize_wav(text, w, syn_config=konf)
        with wave.open(wav_pfad, 'rb') as w:
            rate, kanaele, rahmen = w.getframerate(), w.getnchannels(), w.getnframes()
            pcm = w.readframes(rahmen)
        groesse = mp3_schreiben(os.path.join(ordner, name + '.mp3'), pcm, rate, kanaele)
        os.remove(wav_pfad)
        gesamt += groesse
        print('%s/%-26s %5.1f s  %6.1f KB  %s' % (lang, name + '.mp3', rahmen / rate, groesse/1024, text[:52]))
print('\nGesamt: %.1f KB' % (gesamt/1024))
