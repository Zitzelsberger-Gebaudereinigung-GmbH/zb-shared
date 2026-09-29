# zb-shared

Geteilte Bibliotheken für die Zitzelsberger-Apps — **eine Quelle statt kopierter Module**
(Konsolidierungsplan P2.2/P2.3, Entscheidung `[d-303]`). Kartografie: `wissen/kartografie.md` K6.

## Einbinden (pro App)

In die `requirements.txt` der App:

```
zb-shared @ git+https://github.com/Marketing-Zizzi/zb-shared@v0.3.0
```

(Version pinnen = reproduzierbar. Update = Tag erhöhen + neu deployen.)

## Module

### `zb_shared.ki_client` — kanonischer KI-Zugang (EU-Default)
Ersetzt die kopierten `vertex_embeddings.py` + per-App `ANTHROPIC_BACKEND`-Switches.

```python
from zb_shared import ki_client

vecs = ki_client.embed_batch_sync(["text"], kind="passage")   # Vertex 768, EU (europe-west3)
qv   = ki_client.embed_query("frage")
claude = ki_client.get_anthropic_async()   # AsyncAnthropic (direct/US) ODER AsyncAnthropicVertex (EU)
model  = ki_client.claude_model()          # passendes Modell je Backend (@version bei Vertex)
```

**Konfiguration (ENV, pro Dienst):**
- `ANTHROPIC_BACKEND` = `vertex` (EU) | `direct` (US, Default)
- `GOOGLE_APPLICATION_CREDENTIALS_JSON` = kompletter Service-Account-JSON (Render-Secret) — **Pro-Dienst-Secret** statt geteilter Datei (P2.3)
- optional: `VERTEX_EMBED_LOCATION` (europe-west3), `VERTEX_CLAUDE_LOCATION` (europe-west1), `ANTHROPIC_MODEL_VERTEX`

### `zb_shared.replikat` — KI-Replikate (persönliches Sprach-Abbild)

Ein **KI-Replikat** (Begriff nach Sven Gábor Jánszky, *2035 — The Future Begins Today*) ist kein
Allzweck-Assistent, sondern das Abbild **eines** Menschen: Sprache, Modulation, Wortwahl und Humor
werden nachgebildet, das Wissen bleibt auf das begrenzt, was die Person wirklich weiß. Die drei
Merkmale sind 1:1 im Modul abgebildet:

| Merkmal | Umsetzung |
|---|---|
| Persönliches Abbild, nicht allwissend | `Stilprofil` (aus eigenen Texten gelernt) + `Persona.weiss_ueber` / `weiss_nicht` — das Replikat erfindet nichts und sagt „weiß ich nicht" in **deinen** Worten |
| Mehrfachnutzung je Lebensbereich | mehrere Personas pro Mensch (`arbeit`, `familie`, `mentoring`, `uebersetzung`), je eine JSON-Datei |
| Stimme als Hauptkanal | `fuer_stimme()` (sprechbarer Text statt Chat-Text) + `sprich()` → MP3 via Google Cloud TTS (EU-Endpunkt) |

**In vier Schritten zum eigenen Replikat** (CLI, Profile liegen in `REPLIKAT_PROFIL_DIR`, Default `~/.zb/replikate`):

```bash
# 1. Profil aus Vorlage anlegen (ein Replikat je Lebensbereich)
python -m zb_shared.replikat neu --name "Oliver Strobel" --bereich arbeit --rolle "Geschäftsführer"

# 2. Eigene Texte sammeln: E-Mail-Exporte, Notizen, Gesprächstranskripte als .txt/.md in einen Ordner
#    (Faustregel: 50-200 eigene Texte; je mehr O-Ton, desto genauer das Abbild)

# 3. Stil lernen — Claude destilliert Satzbau, Floskeln, Humor, O-Ton in das Profil
python -m zb_shared.replikat lernen --persona oliver-strobel-arbeit --texte ~/replikat-texte

# 4. Sprechen
python -m zb_shared.replikat chat   --persona oliver-strobel-arbeit --stimme
python -m zb_shared.replikat sprich --persona oliver-strobel-arbeit --text "Passt, machen wir." --out antwort.mp3
```

**In einer App einbinden** — das Wissen bleibt app-seitig und kommt als Callable rein (RAG/DB/Kalender):

```python
from zb_shared.replikat import Replikat, lade_persona

async def wissen(frage: str) -> str:
    qv = await ki_client.embed_query_async(frage)     # eigene Vektorsuche der App
    return "\n".join(treffer_texte(qv))

r = Replikat(lade_persona("oliver-strobel-arbeit"), wissensquelle=wissen, kanal="stimme")
text  = await r.antwort("Wie läuft die Glasreinigung im Objekt Nord?")
audio = r.sprich(text)                                 # MP3-Bytes
```

**Grenzen bewusst gesetzt** (Profilfelder): `weiss_nicht` = Wissenslücken, `freigabe_pflichtig` =
Themen ohne verbindliche Zusage (Preise, Verträge, Personal), `tabus`, `offenlegung` = sagt auf
Nachfrage, dass es ein Replikat ist. Diese Regeln stehen im Systemprompt — nicht in der App.

**Datenschutz:** Profile und Trainingstexte sind personenbezogene Daten. Sie liegen außerhalb des
Repos (`REPLIKAT_PROFIL_DIR`) und sind in `.gitignore` geblockt. Die KI-Aufrufe laufen über
`ki_client`, also mit `ANTHROPIC_BACKEND=vertex` komplett in der EU.

**Eigene Stimme:** Standardstimmen (`de-DE-Wavenet-B`) klingen nach Katalog. Für die echte eigene
Stimme eine geklonte Stimme anlegen (Google *Instant Custom Voice* o. ä.) und nur
`Persona.stimme.stimme_id` darauf setzen. Spracheingabe kommt aus der geplanten `stt`-Lib.

### geplant (P2.2 Audit-Libs)
`stt` (Spracherkennung-Switcher — auch Eingabekanal für `replikat`), `exif` (Foto-Plausibilität), `vision` (Foto-KI) — extrahiert aus Reklamation/QualiCheck/Objektaudit/Objektbesuch.

## Tests

```bash
pip install -e ".[dev]" && pytest -q     # netzwerkfrei (Fake-KI-Client)
```

## Stand
v0.3.0 — `ki_client`, `mailer`, `pdf`, `vertex_transkript`, `replikat` fertig. Weitere Audit-Libs folgen Reihe-für-Reihe.
