#!/usr/bin/env python3
"""PDFs ausgewählter Ordner über GitHub-Releases ausliefern statt über die Website.

Welche Ordner: params.downloads_release in hugo.toml (Ordner = Release-Tag).
Die Dateien bleiben im Repo unter assets/<ordner>/ (deutsch direkt, fr/ und it/
als Unterordner) und werden wie alle anderen hochgeladen. Die Website verlinkt
sie auf https://github.com/<repo>/releases/download/<tag>/<name>
(layouts/partials/download-adresse.html).

Name im Release: Dateiname, bei fr/ bzw. it/ mit «_fr» bzw. «_it» vor «.pdf».
Dieselbe Regel steht in download-adresse.html - beide immer zusammen ändern.

Aufrufe:
  python3 scripts/downloads-release.py liste
      Zeigt, welche Datei unter welchem Namen in welches Release gehört.
  python3 scripts/downloads-release.py links public
      Prüft die gebaute Website: Jeder Release-Link zeigt auf eine Datei, die
      es im Repo gibt, jede solche Datei ist verlinkt, und keine davon liegt
      zusätzlich in public/. Ohne Netz; läuft bei jedem Bau.
  python3 scripts/downloads-release.py abgleichen [--trocken]
      Gleicht die Releases mit den Ordnern ab: fehlende oder geänderte
      Dateien hochladen, nicht mehr vorhandene löschen, danach nachprüfen.
      Braucht `gh` und GH_TOKEN mit contents: write. Läuft in hugo.yml
      (Job «pdf-release») vor jeder Veröffentlichung.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
SPRACHEN = ("fr", "it")
NAME_OK = re.compile(r"^[A-Za-z0-9._-]+$")


def einstellungen():
    with open(WURZEL / "hugo.toml", "rb") as f:
        params = tomllib.load(f).get("params", {})
    return params.get("downloads_repo", ""), params.get("downloads_release", {}) or {}


def name_im_release(datei: Path, sprache: str | None) -> str:
    if sprache:
        return f"{datei.stem}_{sprache}.pdf"
    return datei.name


def erwartet():
    """{tag: {name: pfad}} aus den Ordnern; bricht bei unerwarteten Dateien ab."""
    _, ordner = einstellungen()
    fehler, alle = [], {}
    for rel, tag in ordner.items():
        basis = WURZEL / "assets" / rel
        if not basis.is_dir():
            fehler.append(f"Ordner fehlt: assets/{rel}")
            continue
        dateien = {}
        for p in sorted(basis.rglob("*")):
            if p.is_dir():
                if p.parent == basis and p.name in SPRACHEN:
                    continue
                fehler.append(f"Unerwarteter Unterordner: {p.relative_to(WURZEL)}")
                continue
            teile = p.relative_to(basis).parts
            sprache = teile[0] if len(teile) == 2 else None
            if p.suffix != ".pdf" or len(teile) > 2:
                fehler.append(f"Unerwartete Datei (nur PDFs, nur fr/ und it/): {p.relative_to(WURZEL)}")
                continue
            name = name_im_release(p, sprache)
            if not NAME_OK.match(name):
                fehler.append(f"Dateiname nur mit Buchstaben, Ziffern, Punkt, _ und -: {p.relative_to(WURZEL)}")
            if name in dateien:
                fehler.append(f"Doppelter Name im Release {tag}: {name}")
            dateien[name] = p
        alle[tag] = dateien
    if fehler:
        sys.exit("\n".join(["FEHLER:"] + fehler))
    return alle


def liste():
    for tag, dateien in erwartet().items():
        print(f"[{tag}] {len(dateien)} Dateien, {sum(p.stat().st_size for p in dateien.values()) / 1e6:.0f} MB")
        for name, p in dateien.items():
            print(f"  {name:60s} <- {p.relative_to(WURZEL)}")


def links(public: Path):
    repo, ordner = einstellungen()
    soll = erwartet()
    muster = re.compile(r"https://github\.com/" + re.escape(repo) + r"/releases/download/([^/\"' >]+)/([^\"' >]+)")
    gefunden = set()
    for html in public.rglob("*.html"):
        for tag, name in muster.findall(html.read_text(encoding="utf-8", errors="replace")):
            gefunden.add((tag, name))
    fehler = []
    for tag, name in sorted(gefunden):
        if name not in soll.get(tag, {}):
            fehler.append(f"Link ins Leere: {tag}/{name}")
    for tag, dateien in soll.items():
        for name in dateien:
            if (tag, name) not in gefunden:
                fehler.append(f"Nirgends verlinkt: {tag}/{name}")
    for rel in ordner:
        if (public / rel).exists() and any((public / rel).rglob("*.pdf")):
            fehler.append(f"PDFs liegen trotzdem auf der Website: public/{rel}")
    if fehler:
        sys.exit("\n".join(["FEHLER:"] + fehler))
    print(f"Release-Links in Ordnung: {len(gefunden)} Links, {len(soll)} Releases")


def gh(*args, json_out=False):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)}: {r.stderr.strip()}")
    return json.loads(r.stdout) if json_out else r.stdout


def assets_holen(repo, tag):
    try:
        rel = gh("api", f"repos/{repo}/releases/tags/{tag}", json_out=True)
    except RuntimeError as e:
        if "404" in str(e) or "Not Found" in str(e):
            return None
        raise
    assets, seite = [], 1
    while True:
        teil = gh("api", f"repos/{repo}/releases/{rel['id']}/assets?per_page=100&page={seite}", json_out=True)
        assets += teil
        if len(teil) < 100:
            break
        seite += 1
    return {a["name"]: a for a in assets}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def gleich(asset, p: Path) -> bool:
    if asset.get("state") != "uploaded" or asset.get("size") != p.stat().st_size:
        return False
    digest = asset.get("digest") or ""
    if digest.startswith("sha256:"):
        return digest[7:] == sha256(p)
    return True  # ältere Assets ohne Prüfsumme: gleiche Grösse genügt


def abgleichen(trocken: bool):
    repo, _ = einstellungen()
    soll = erwartet()
    for tag, dateien in soll.items():
        vorhanden = assets_holen(repo, tag)
        if vorhanden is None:
            print(f"[{tag}] Release fehlt, wird angelegt")
            if not trocken:
                gh("release", "create", tag, "--repo", repo, "--title", f"Downloads: {tag}",
                   "--notes", "Von der Website verlinkte PDFs, automatisch nachgeführt "
                   "(scripts/downloads-release.py). Bitte nicht von Hand ändern: Neue oder "
                   "geänderte Dateien kommen wie immer ins Repo unter assets/downloads/.",
                   "--latest=false")
            vorhanden = {}
        hoch = [n for n, p in dateien.items() if n not in vorhanden or not gleich(vorhanden[n], p)]
        weg = [n for n in vorhanden if n not in dateien]
        print(f"[{tag}] {len(dateien)} Dateien: {len(hoch)} hochladen, {len(weg)} löschen")
        for n in hoch:
            print(f"  hoch: {n}")
        for n in weg:
            print(f"  weg:  {n}")
        if trocken:
            continue
        if hoch:
            with tempfile.TemporaryDirectory() as tmp:
                pfade = []
                for n in hoch:
                    ziel = Path(tmp) / n
                    shutil.copyfile(dateien[n], ziel)
                    pfade.append(str(ziel))
                for i in range(0, len(pfade), 10):
                    gh("release", "upload", tag, "--repo", repo, "--clobber", *pfade[i:i + 10])
        for n in weg:
            gh("api", "-X", "DELETE", f"repos/{repo}/releases/assets/{vorhanden[n]['id']}")
        # Nachprüfen: Erst wenn alles da ist, darf die Website veröffentlicht werden.
        nachher = assets_holen(repo, tag) or {}
        falsch = [n for n, p in dateien.items() if n not in nachher or not gleich(nachher[n], p)]
        if falsch:
            sys.exit(f"FEHLER: [{tag}] nach dem Hochladen fehlen oder weichen ab: {', '.join(falsch)}")
        print(f"[{tag}] nachgeprüft: alle {len(dateien)} Dateien vorhanden")


if __name__ == "__main__":
    befehl = sys.argv[1] if len(sys.argv) > 1 else ""
    if befehl == "liste":
        liste()
    elif befehl == "links" and len(sys.argv) == 3:
        links(Path(sys.argv[2]))
    elif befehl == "abgleichen":
        abgleichen("--trocken" in sys.argv)
    else:
        sys.exit(__doc__)
