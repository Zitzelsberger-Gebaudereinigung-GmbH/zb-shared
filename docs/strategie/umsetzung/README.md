# Umsetzung ohne Claude-Zugriff — Übergabepaket

**Stand:** 17.11.2026 · **Geprüft gegen:** MA-App `cc697dc` (Build 914) · zb-shared v0.2.7
**Gehört zu:** `../2026-08-29_bauplan.md` (Züge A–E), fortgeschrieben auf den Stand von heute

Claude hat auf `zitzelsberger-mitarbeiter-app` nur Lesezugriff. Deshalb liegt hier alles
als **fertiges Artefakt**: einspielen, Erwartung prüfen, weiter. Jeder Schritt nennt den
Befehl, das erwartete Ergebnis und den Rückweg.

Beide Dateien in diesem Ordner sind in diesem Klon (Build 914) **ausgeführt und geprüft**,
nicht nur geschrieben:

| Datei | Zustand |
|---|---|
| `ki_register_nachtrag.json` | eingespielt, Wache lief danach ohne „NICHT IM REGISTER" |
| `routen_paritaet_test.py` | gegen 1.856 echte Routen gelaufen; Fund-, Verlust- und Umzugserkennung je einmal gegengeprüft |

---

## Schritt 0 · Welle C1a liegt fertig als Patch bereit

`0001-Build-915-Entflechtung-C1a-Geraete-Bestand-als-eigen.patch` enthält die **erste
Entflechtungswelle vollständig ausgeführt**: das Geräte-Bestand-Modul ist aus `main.py`
heraus, inklusive Register, Build-Bump, Paritätswerkzeug und Runbook. Schritt 1 und 2
unten sind darin bereits enthalten.

```bash
git checkout -b entflechtung-c1a origin/main
git am < 0001-Build-915-Entflechtung-C1a-Geraete-Bestand-als-eigen.patch
python scripts/routen_paritaet_test.py --vergleiche konsolidierung/c1a/routen-build914.json
```

| | vorher | nachher |
|---|---:|---:|
| `main.py` Zeilen | 22.729 | **22.036** |
| Routen in `main.py` | 458 | **443** |
| Routen gesamt | 1.856 | **1.856** |

**Geprüft** (gegen `cc697dc`, nach `git am` auf frischem Stand wiederholt): `py_compile`
beide Dateien · Routen-Parität 1.856 → 1.856, 15 umgezogen, 0 verloren, 0 neu · keine
unaufgelösten Namen im neuen Modul · unaufgelöste Namen in `main.py` vorher/nachher
identisch · Wache ohne Befund.

**Nicht geprüft:** Laufzeitverhalten — der Rauchtest in `konsolidierung/c1a/RUNBOOK.md`
Schritt 5 ist Pflicht vor dem Merge. Er ist so zugeschnitten, dass die vier Wege genau die
14 injizierten Helfer abdecken.

Der wichtigste Befund dabei: **sechs Helfer des Blocks werden vom Rest der `main.py` noch
gebraucht** (`_geraete_tuer`, `_ist_geraete_user`, `_ist_techdienst`, `_zentrallager_id`,
`_geraete_foto_upload`, `_norm_sn`) — `main.py` reicht sie an `geraete_verwaltung` und
`geraete_ersatzteile` weiter. Ein naiver Schnitt hätte vier Modul-Verdrahtungen zerrissen,
und weder `py_compile` noch der Paritätstest hätten das gemeldet. Diese Kollisionsprüfung
gehört vor jede weitere Welle.

---

## Schritt 1 · Register-Nachtrag (20 Minuten, kein Risiko)

Die Wache meldet zwei Module, die nach dem Prüfstand dazugekommen sind:
`fahrzeugkontrolle.py` (Build 886) und `objektmappe_ortsweg.py` (Build 894).

Beide sind in der Oberfläche **schon gekennzeichnet** — die Einträge tragen deshalb
`BELEGT`, nicht `PRUEFEN`, mit Fundstelle im Feld `kennzeichnung`.

```bash
# im Repo-Wurzelverzeichnis, Worktree sauber
python - <<'PY'
import json
reg  = "backend/ki_register.json"
nach = "<pfad>/ki_register_nachtrag.json"
d = json.load(open(reg, encoding="utf-8"))
n = json.load(open(nach, encoding="utf-8"))
d["module"].update(n["module"])
d["module"] = dict(sorted(d["module"].items()))
json.dump(d, open(reg, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Eintraege jetzt:", len(d["module"]))
PY

python scripts/ki_kennzeichnung_wache.py
```

**Erwartung:** `Eintraege jetzt: 93` · Wache meldet **kein** „NICHT IM REGISTER" mehr.
Es bleiben genau zwei bekannte, dokumentierte Punkte stehen:
`kontakt_agent.py` (bewusst Trockenlauf, DSB Nr. 249) und `video_doku_service.py`
(von seiner Natur her Annex-III-Kandidat).

**Vor dem Commit einmal gegenlesen:** Die Einträge nennen Zeilennummern
(`fahrzeugkontrolle.py:68`, `ortsweg.js:390`, `ortsweg.js:381`). Sie stimmten am
17.11.2026. Wenn sich die Dateien seither bewegt haben, Zahlen anpassen.

**Rückweg:** Datei aus git zurückholen — `git checkout backend/ki_register.json`.

---

## Schritt 2 · Das Paritätswerkzeug (C0, ein halber Tag)

`routen_paritaet_test.py` nach `scripts/` kopieren. Es braucht **nichts**: keinen Import
von `main.py`, keine Umgebungsvariablen, keine Datenbank, keinen laufenden Dienst — es
liest die Dekoratoren mit `ast` aus dem Quellcode.

```bash
cp <pfad>/routen_paritaet_test.py scripts/
python scripts/routen_paritaet_test.py
```

**Erwartung heute (Build 914):**

```
[paritaet] 1856 Routen in 147 Modulen
           davon 458 in main.py — modularer Anteil 75 %
```

Weicht die Zahl ab, ist seit dem 17.11. Code dazugekommen — kein Problem, das ist dann
euer neuer Referenzstand.

> **Eine harmlose Meldung:** Auf Python 3.11 warnt das Werkzeug bei
> `prozessboard_pdf.py` („f-string expression part cannot include a backslash"). Die
> Datei enthält **0 Routen**, das Ergebnis ist also vollständig. Ab Python 3.12 erscheint
> die Meldung nicht mehr.

### Referenzinventar ziehen und wegheften

```bash
python scripts/routen_paritaet_test.py --schreibe konsolidierung/routen-build914.json
git add konsolidierung/routen-build914.json
```

Das ist der Vergleichspunkt für jede Entflechtungswelle. Ins Repo damit, nicht ins
Temp-Verzeichnis — er muss Wochen später noch da sein.

### Die zwei Betriebsarten

| Aufruf | Was er prüft |
|---|---|
| `--schreibe X.json` / `--vergleiche X.json` | Routen im **Quellcode**. Läuft im Worktree, vor jedem Deploy. |
| `--von-openapi http://localhost:8008` | Routen, die FastAPI **tatsächlich registriert** hat. Strenger: fängt auch ein vergessenes `include_router`, bei dem die Route im Code steht, aber nicht mehr hängt. |

Beide schreiben dasselbe Format, sind also untereinander vergleichbar. Für Zug C:
statisch im Worktree arbeiten, nach dem Deploy einmal gegen `--von-openapi` gegenprüfen.

### Nützlich beim Zuschneiden einer Welle

```bash
python scripts/routen_paritaet_test.py --zeige geraetebestand
```

Listet jede Route der Gruppe mit Methode, Pfad, Modul und Funktionsname — die Arbeitsliste
für das Herauslösen.

### Exit-Code

Anders als die Wachen (die melden und mit 0 enden, Hauslinie `[log-1367]`) endet dieser
Test bei einer Abweichung mit **1**. Er läuft nicht im Hook, sondern von Hand im
Umbauschritt — da ist ein harter Fehlschlag gewollt: Der Vergleich **ist** das Tor T3.

---

## Schritt 3 · Welle C1 (die erste Entflechtung)

Der Zuschnitt aus dem Bauplan gilt unverändert — und ist dringlicher geworden. In
`main.py` liegen heute **59 KI-Aufrufstellen** (im August: 7) unter einem Registereintrag,
der „Sammelposten" heißt.

Gruppen für C1, alle heute noch in `main.py`:

| Gruppe | Routen | Zielrouter |
|---|---:|---|
| `geraetebestand` | 13 | `geraet` |
| `gespraechsprotokoll` | 11 | `gespraech` |
| `wissen`, `assistent`, `transcribe`, `translate` | 5 | `wissen` |

Klein, in sich geschlossen — und `gespraechsprotokoll` berührt Personalgespräche, hat also
den höchsten Nutzen pro herausgelöster Zeile.

### Ablauf (Runbook-Muster aus `phase1/RUNBOOK.md`)

1. **Lane frei?** `git status` sauber, andere Session gepusht.
2. Worktree + Branch `entflechtung-c1`, von `origin/main`.
3. **Vorher messen:** `python scripts/routen_paritaet_test.py --schreibe vorher.json`
4. Gruppe herauslösen: neues `backend/<bereich>_router.py` mit
   `router = APIRouter(prefix="/api/<bereich>", tags=["<bereich>"])`, Routen **1:1**
   übernehmen — Pfad, Methode, Signatur und Zugriffswächter unverändert —,
   `include_router` in `main.py`, alte Definitionen entfernen.
5. **Je KI-Stelle ein eigener Registereintrag.** Kein `PRUEFEN` als Endzustand. Die
   `#`-Notation, die ihr für `main.py#bewerberpool_passung` eingeführt habt, wird hier
   überflüssig: Die Funktion hat jetzt eine eigene Datei.
6. `python -m py_compile` über die berührten Dateien.
7. `APP_BUILD` +1, Titel „Entflechtung C1 — Wissen/Gerät/Gespräch", Datum.
8. **Nachher vergleichen:** `python scripts/routen_paritaet_test.py --vergleiche vorher.json`
   → **muss** „Paritaet erfuellt" melden. Umgezogene Routen sind erwünscht und werden
   als solche ausgewiesen; verschwundene oder neue sind ein Fehler.
9. Rauchtest, Deploy-Frage, Merge → Push → Render-Deploy.
10. Live: `/version` = neuer Build · je Gruppe ein echter Klickpfad ·
    `python scripts/ki_kennzeichnung_wache.py` · einmal `--von-openapi` gegenprüfen.

**Rückweg:** `git revert -m 1 <merge-commit>; git push`. In Zug C gibt es keine
DB-Migration — der Rückweg ist immer datenverlustfrei.

---

## Schritt 4 · T4 vorbereiten (blockiert Zug E)

Der Leistungskatalog hat weiterhin **vier** Schreiber. Dieser Befehl zeigt sie:

```bash
for f in backend/*.py; do
  n=$(grep -o 'table("qm_checkliste_\(vorlagen\|items\)")\.\(insert\|update\|upsert\|delete\)' "$f" | wc -l)
  [ "$n" -gt 0 ] && echo "  $(basename $f): $n Schreibstellen"
done
```

**Stand 17.11.2026:**

| Modul | Schreibstellen | |
|---|---:|---|
| `leistungsverzeichnis_service.py` | 8 | der designierte Owner |
| `lv_aenderung_service.py` | 7 | prüfen: Teil des Owners oder eigener Schreiber? |
| **`main.py`** | **9** | die meisten — und nach C-Welle „qualität" ohnehin umzuziehen |
| `raumanker_service.py` | 1 | prüfen: schreibt es fachlich oder nur Anker? |

19 weitere Module lesen mit. Der Befund aus dem Playbook P2.4 steht also unverändert.

**Die Entscheidung, die kein Werkzeug ersetzt:** Wer wird benannter Schreib-Owner, und wer
darf den Katalog fachlich ändern? Ohne diese Antwort startet Zug E nicht — ein Kalkulator
auf Owner-loser Katalogbasis erzeugt plausible, falsche Preise.

---

## So arbeiten wir weiter, ohne dass Claude Schreibzugriff braucht

Das Muster: **Ihr führt aus und schickt Messwerte, Claude baut daraus das nächste Artefakt.**
Lesezugriff genügt, um den Code zu verstehen; gebraucht wird nur, was Claude von außen
nicht sehen kann.

Diese vier Ausgaben reichen als Rückmeldung:

```bash
python scripts/ki_kennzeichnung_wache.py                       # Registerstand
python scripts/routen_paritaet_test.py                         # Routenverteilung
python scripts/routen_paritaet_test.py --vergleiche vorher.json # Ergebnis einer Welle
git log --oneline -15                                           # was dazugekommen ist
```

Dazu die Dinge, die nur ihr sehen könnt:

- `select id, public from storage.buckets order by public desc;` — offene PII-Buckets (A5)
- `select count(*), min(created_at), max(created_at) from ur_query_cache;` — füllt sich der
  Fragen-Zwischenspeicher? Davon hängt ab, ob das Goldset aus **echten** Fragen entstehen
  kann (Zug B) oder erst gesammelt werden muss
- die vier offenen Punkte aus `../2026-08-29_bauplan.md` § 14

Mit einer dieser Ausgaben im Chat kann Claude den nächsten Schritt wieder als fertige
Datei liefern — Routerdatei, Registereintrag, Migration, Runbook —, und ihr spielt ihn ein.

Soll Claude doch direkt committen, reicht es, `zitzelsberger-mitarbeiter-app` in einer
Sitzung mit Schreibrecht anzubinden; am Verfahren oben ändert das nichts, es spart nur
das Kopieren.
