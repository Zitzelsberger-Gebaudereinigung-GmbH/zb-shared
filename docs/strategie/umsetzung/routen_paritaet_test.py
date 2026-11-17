# -*- coding: utf-8 -*-
"""Routen-Paritaets-Test: beweist, dass eine Entflechtung nichts verloren hat.

WOZU
----
Zug C des Bauplans loest Routengruppen aus `backend/main.py` in Fachrouter heraus.
Der Umbau darf nach aussen NICHTS aendern. Ohne Beweis bleibt das eine Behauptung:
Bei 458 Routen in `main.py` faellt eine vergessene Route erst auf, wenn ein Mensch
sie im Betrieb vermisst. Dieser Test macht aus der Behauptung eine Messung.

Die Linie ist dieselbe wie bei `phase1/RUNBOOK.md`: vorher messen, umbauen,
nachher messen, vergleichen. Erst wenn der Vergleich leer ist, geht der Zug raus.

ZWEI BETRIEBSARTEN
------------------
1. **Statisch** (Standard, braucht nichts): liest den Quellcode mit `ast` und
   findet jede Route an ihrem Dekorator. Kein Import von `main.py`, keine
   Umgebungsvariablen, keine Datenbank, kein laufender Dienst. Damit laeuft der
   Test auch im Worktree, bevor irgendetwas deployt ist.

2. **Aus dem laufenden Dienst** (`--von-openapi URL`): holt `/openapi.json` und
   nimmt die Routen, die FastAPI tatsaechlich registriert hat. Das ist der
   strengere Beweis — er faengt auch Routen, die durch ein vergessenes
   `include_router` gar nicht mehr haengen. Braucht nur, dass der Dienst laeuft;
   `/openapi.json` ist nicht angemeldet.

Beide Arten schreiben dasselbe Format, sind also untereinander vergleichbar.

AUFRUF
------
    # vor dem Umbau (im Worktree):
    python scripts/routen_paritaet_test.py --schreibe vorher.json

    # nach dem Umbau:
    python scripts/routen_paritaet_test.py --vergleiche vorher.json

    # gegen den laufenden Dienst (strenger):
    python scripts/routen_paritaet_test.py --von-openapi http://localhost:8008 \
        --schreibe vorher-live.json

    # nur ansehen, was gefunden wird:
    python scripts/routen_paritaet_test.py --zeige geraetebestand

EXIT-CODE
---------
Anders als die Wachen (`ki_kennzeichnung_wache.py` & Co., die MELDEN und mit 0
enden, Hauslinie [log-1367]) endet dieser Test bei einer Abweichung mit 1. Er
laeuft nicht im Hook, sondern von Hand im Umbauschritt — da ist ein harter
Fehlschlag gewollt: Der Vergleich IST das Tor T3.

WAS ER NICHT PRUEFT
-------------------
Verhalten. Gleiche Route heisst nicht gleiche Antwort. Der Rauchtest je Welle
(ein echter Klickpfad je Gruppe) bleibt Pflicht — dieser Test sichert nur zu,
dass keine Route verschwunden, hinzugekommen oder verschoben ist.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
import urllib.request
from pathlib import Path

# Die Windows-Konsole faellt auf cp1252 zurueck und wirft bei jedem Sonderzeichen
# einen UnicodeEncodeError — derselbe Stolperstein wie bei der KI-Wache am
# 21.08.2026. Deshalb hier gleich zu Anfang umstellen.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

WURZEL = Path(__file__).resolve().parents[1]
BACKEND = WURZEL / "backend"

METHODEN = {"get", "post", "put", "patch", "delete", "head", "options"}


# ── Statisch: Routen aus dem Quellcode lesen ────────────────────────────────
def _praefixe(baum: ast.Module) -> dict[str, str]:
    """Welche Variable haelt welchen APIRouter-Praefix.

    Erkennt `router = APIRouter(prefix="/api/lv")` ebenso wie einen zweiten
    Router im selben Modul (`intern = APIRouter(prefix="/api/internal")`).
    `app` ist die FastAPI-Instanz und hat nie einen Praefix.
    """
    gefunden: dict[str, str] = {}
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Assign):
            continue
        wert = knoten.value
        if not isinstance(wert, ast.Call):
            continue
        name = wert.func.attr if isinstance(wert.func, ast.Attribute) else getattr(wert.func, "id", "")
        if name not in ("APIRouter", "FastAPI"):
            continue
        praefix = ""
        for kw in wert.keywords:
            if kw.arg == "prefix" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                praefix = kw.value.value
        for ziel in knoten.targets:
            if isinstance(ziel, ast.Name):
                gefunden[ziel.id] = praefix
    return gefunden


def _routen_einer_datei(pfad: Path) -> list[dict]:
    try:
        quelle = pfad.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    try:
        baum = ast.parse(quelle)
    except SyntaxError as e:
        print(f"  [warnung] {pfad.name}: nicht lesbar ({e.msg}, Zeile {e.lineno}) — uebersprungen")
        return []

    praefixe = _praefixe(baum)
    treffer: list[dict] = []

    for knoten in ast.walk(baum):
        if not isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dek in knoten.decorator_list:
            if not isinstance(dek, ast.Call) or not isinstance(dek.func, ast.Attribute):
                continue
            methode = dek.func.attr.lower()
            if methode not in METHODEN:
                continue
            basis = getattr(dek.func.value, "id", None)
            if basis is None or basis not in praefixe:
                continue  # z. B. ein Dekorator auf einem fremden Objekt
            if not dek.args or not isinstance(dek.args[0], ast.Constant):
                continue
            teilpfad = dek.args[0].value
            if not isinstance(teilpfad, str):
                continue
            treffer.append({
                "methode": methode.upper(),
                "pfad": (praefixe[basis] + teilpfad) or "/",
                "funktion": knoten.name,
                "modul": pfad.name,
            })
    return treffer


def inventar_statisch() -> list[dict]:
    alle: list[dict] = []
    for datei in sorted(BACKEND.glob("*.py")):
        alle.extend(_routen_einer_datei(datei))
    return alle


# ── Aus dem laufenden Dienst ────────────────────────────────────────────────
def inventar_openapi(basis_url: str) -> list[dict]:
    url = basis_url.rstrip("/") + "/openapi.json"
    with urllib.request.urlopen(url, timeout=30) as antwort:  # noqa: S310 — eigene URL
        daten = json.loads(antwort.read().decode("utf-8"))
    alle: list[dict] = []
    for pfad, methoden in (daten.get("paths") or {}).items():
        for methode, beschreibung in methoden.items():
            if methode.lower() not in METHODEN:
                continue
            alle.append({
                "methode": methode.upper(),
                "pfad": pfad,
                "funktion": (beschreibung or {}).get("operationId", ""),
                "modul": "(openapi)",
            })
    return alle


# ── Vergleich ───────────────────────────────────────────────────────────────
def _schluessel(eintrag: dict) -> tuple[str, str]:
    """Identitaet einer Route: Methode + Pfad. Modul und Funktionsname duerfen
    sich beim Herausloesen aendern — genau das ist der Zweck des Umbaus."""
    return (eintrag["methode"], eintrag["pfad"])


def vergleiche(vorher: list[dict], nachher: list[dict]) -> int:
    v = {_schluessel(e): e for e in vorher}
    n = {_schluessel(e): e for e in nachher}

    fehlen = sorted(set(v) - set(n))
    neu = sorted(set(n) - set(v))
    verschoben = sorted(
        k for k in (set(v) & set(n))
        if v[k].get("modul") != n[k].get("modul") and "(openapi)" not in (v[k]["modul"], n[k]["modul"])
    )

    print(f"[paritaet] vorher {len(vorher)} Routen, nachher {len(nachher)} Routen")

    if fehlen:
        print(f"\n  \U0001f534 {len(fehlen)} Route(n) VERSCHWUNDEN — das ist ein Fehler:")
        for methode, pfad in fehlen:
            print(f"      {methode:6} {pfad}        (war in {v[(methode, pfad)]['modul']})")

    if neu:
        print(f"\n  \u26a0 {len(neu)} Route(n) NEU — bei einer reinen Entflechtung unerwartet:")
        for methode, pfad in neu:
            print(f"      {methode:6} {pfad}        (jetzt in {n[(methode, pfad)]['modul']})")

    if verschoben:
        print(f"\n  \u2139 {len(verschoben)} Route(n) in ein anderes Modul umgezogen — so soll es sein:")
        for methode, pfad in verschoben:
            print(f"      {methode:6} {pfad}")
            print(f"             {v[(methode, pfad)]['modul']}  \u2192  {n[(methode, pfad)]['modul']}")

    if not fehlen and not neu:
        zusatz = f", {len(verschoben)} umgezogen" if verschoben else ""
        print(f"\n  \u2705 Paritaet erfuellt: keine Route verschwunden, keine hinzugekommen{zusatz}.")
        return 0

    print("\n  Tor T3 NICHT erfuellt. Der Zug geht so nicht raus.")
    return 1


# ── Bericht ─────────────────────────────────────────────────────────────────
def zeige_verteilung(inventar: list[dict], filter_text: str | None) -> None:
    je_modul: dict[str, int] = {}
    for e in inventar:
        if filter_text and filter_text.lower() not in (e["pfad"] + e["modul"]).lower():
            continue
        je_modul[e["modul"]] = je_modul.get(e["modul"], 0) + 1

    if filter_text:
        print(f"[paritaet] Routen zu \u201e{filter_text}\u201c:\n")
        for e in sorted(inventar, key=lambda x: (x["pfad"], x["methode"])):
            if filter_text.lower() in (e["pfad"] + e["modul"]).lower():
                print(f"  {e['methode']:6} {e['pfad']:52} {e['modul']}  \u00b7  {e['funktion']}")
        print()

    gesamt = sum(je_modul.values())
    in_main = je_modul.get("main.py", 0)
    print(f"[paritaet] {gesamt} Routen in {len(je_modul)} Modulen")
    if in_main and not filter_text:
        anteil = 100.0 * (gesamt - in_main) / gesamt if gesamt else 0.0
        print(f"           davon {in_main} in main.py \u2014 modularer Anteil {anteil:.0f} %")
    print("\n  Die zehn groessten Module:")
    for modul, anzahl in sorted(je_modul.items(), key=lambda x: -x[1])[:10]:
        print(f"      {anzahl:4}  {modul}")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Routen-Inventar schreiben und zwei Inventare vergleichen (Tor T3 des Bauplans).")
    p.add_argument("--schreibe", metavar="DATEI", help="Inventar als JSON schreiben")
    p.add_argument("--vergleiche", metavar="DATEI", help="gegen dieses frueher geschriebene Inventar vergleichen")
    p.add_argument("--von-openapi", metavar="URL",
                   help="Routen aus dem laufenden Dienst holen (z. B. http://localhost:8008) statt aus dem Quellcode")
    p.add_argument("--zeige", metavar="TEXT", nargs="?", const="",
                   help="Verteilung ausgeben; mit TEXT nur passende Routen")
    args = p.parse_args()

    if args.von_openapi:
        try:
            inventar = inventar_openapi(args.von_openapi)
            quelle = f"openapi @ {args.von_openapi}"
        except Exception as e:  # noqa: BLE001 — Netzfehler sollen lesbar sein
            print(f"[paritaet] /openapi.json nicht erreichbar: {type(e).__name__}: {e}")
            return 2
    else:
        inventar = inventar_statisch()
        quelle = "Quellcode (ast)"

    if not inventar:
        print(f"[paritaet] keine Routen gefunden ({quelle}) \u2014 stimmt der Pfad zu backend/?")
        return 2

    if args.schreibe:
        Path(args.schreibe).write_text(
            json.dumps(sorted(inventar, key=lambda e: (e["pfad"], e["methode"])), ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"[paritaet] {len(inventar)} Routen aus {quelle} \u2192 {args.schreibe}")

    if args.vergleiche:
        vorher = json.loads(Path(args.vergleiche).read_text(encoding="utf-8"))
        return vergleiche(vorher, inventar)

    if args.zeige is not None:
        zeige_verteilung(inventar, args.zeige or None)
    elif not args.schreibe:
        zeige_verteilung(inventar, None)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
