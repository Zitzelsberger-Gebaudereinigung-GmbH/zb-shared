# -*- coding: utf-8 -*-
"""Audio-Transkription ueber Gemini (Vertex AI) — gemeinsamer Baustein.

HERKUNFT UND ZWECK
------------------
Dieser Baustein ist der **Transkriptions-Ausschnitt** aus
`Mitarbeiter-App/backend/vertex_gemini.py` (dort 1020 Zeilen, zusaetzlich mit
Bild-Analyse und Etikettenlesern, 19 abhaengige Module). Er wandert hierher,
damit ihn auch der Objektbesuch-Agent nutzen kann, ohne ihn zu kopieren
([log-1646]).

**Wichtig fuer den, der das spaeter aufraeumt:** Die MA-App nutzt vorerst
weiter ihre eigene Fassung, weil sie auf einen noch nicht gemergten Branch
gepinnt ist (`claude/ki-replikat-erstellen-nuqp1l`, PR #1). Sobald der gemergt
und der Pin auf einen Tag umgestellt ist, gehoert `vertex_gemini.transcribe_*`
dort durch einen Import aus diesem Modul ersetzt. Bis dahin existiert die
Strecke zweimal — bewusst und befristet, nicht aus Versehen.

WARUM DIE KOMMENTARE HIER STEHEN BLEIBEN
----------------------------------------
Der Code sieht laenger aus, als er sein muesste. Jede der folgenden Stellen
geht auf einen echten Vorfall zurueck; wer sie beim naechsten Aufraeumen
"vereinfacht", holt den Vorfall zurueck:

* **Nur EU-Regionen.** Bis 2026-08-15 stand `europe-west1,global,us-central1`
  in der Vorgabe. Der Rueckfall lief STILL: Antwortete Europa einmal nicht mit
  200, ging dieselbe Anfrage nach `global` und danach in die USA — ohne Hinweis,
  ohne Protokolleintrag. Betroffen waren Unfallhergaenge, Ticket-Texte,
  Gefaehrdungsbeurteilungen. Jetzt: zwei EU-Regionen als Rueckfall fuereinander,
  keine ausserhalb. Scheitern beide, scheitert der Aufruf **sichtbar**.
* **Regionswechsel wird protokolliert** ([log-1258]). Wer nicht sieht, dass
  europe-west1 ausgefallen ist, merkt auch nicht, dass die Anfrage woanders lief.
* **Wiederholung nur bei 429/5xx** — Quota- und Gateway-Stoerungen sind meist
  Sekunden spaeter weg. Bei Timeout/Netzfehler KEINE Wiederholung: Der
  Erstversuch hat dann schon die volle Zeit verbraucht.
* **Alle Ausfallgruende sammeln, nicht nur den letzten** ([log-1597]).
* **`MAX_TOKENS` erkennen** ([log-1396]). Bis 2026-09-15 fehlte ab etwa zehn
  Minuten Aufnahme der Rest des Gespraechs — ohne Fehlermeldung.

Zugangsdaten kommen aus `ki_client.gcp_credentials()` und bleiben damit
einquellig.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os

import httpx

from .ki_client import gcp_credentials as _get_credentials

GEMINI_MODEL = os.getenv("VERTEX_GEMINI_MODEL", "gemini-2.5-flash")

#: NUR EU. Siehe Modulkopf — eine nicht-europaeische Region hier ist ein Befund,
#: kein Feature. Die Umgebungsvariable bleibt, damit im Notfall ohne Deploy
#: nachgesteuert werden kann; ein Verstoss wird beim Start protokolliert.
GEMINI_LOCATIONS = [
    l.strip() for l in os.getenv(
        "VERTEX_GEMINI_LOCATIONS", "europe-west1,europe-west4"
    ).split(",") if l.strip()
]

_NICHT_EU = [l for l in GEMINI_LOCATIONS if not l.startswith("europe-")]
if _NICHT_EU:
    logging.getLogger(__name__).warning(
        "VERTEX_GEMINI_LOCATIONS enthaelt Region(en) ausserhalb der EU: %s. "
        "Personenbezogene Inhalte koennen dorthin abfliessen — bitte pruefen, "
        "ob das gewollt und im Verzeichnis der Verarbeitungstaetigkeiten "
        "hinterlegt ist.", ", ".join(_NICHT_EU))

#: HTTP-Status, bei denen ein zweiter Versuch Sinn hat. Bei 400/401/403 waere die
#: Wiederholung sinnlos — eine abgelehnte Anfrage bleibt abgelehnt.
_VORUEBERGEHEND = {429, 500, 502, 503, 504}
_WIEDERHOLUNGEN = 2
_WARTEN_SEK = 1.5

#: Denk-Tokens zaehlen bei Gemini 2.5 in dieselbe Ausgabegrenze; 4.096 reichten
#: nur fuer rund zehn Minuten, weil der Text doppelt (original + deutsch) kam.
TRANSKRIPT_MAX_TOKENS = 32768
TRANSKRIPT_TIMEOUT = 180.0


class KiAntwortAbgeschnitten(RuntimeError):
    """Das Modell hat seine Ausgabegrenze erreicht — die Antwort ist unvollstaendig."""


def _endpoint(location: str, project_id: str) -> str:
    host = ("aiplatform.googleapis.com" if location == "global"
            else f"{location}-aiplatform.googleapis.com")
    return (f"https://{host}/v1/projects/{project_id}/locations/{location}/"
            f"publishers/google/models/{GEMINI_MODEL}:generateContent")


def _pruefe_abbruch(cand: dict, location: str) -> None:
    if (cand or {}).get("finishReason") == "MAX_TOKENS":
        raise KiAntwortAbgeschnitten(
            f"{location}: Ausgabegrenze erreicht (finishReason=MAX_TOKENS)")


async def _generate(parts: list[dict], generation_config: dict | None = None,
                    timeout: float = 90.0, pruefe_abbruch: bool = False) -> str:
    """Schickt `parts` an Gemini (Vertex), EU-Regionen der Reihe nach."""
    creds = _get_credentials()
    project_id = getattr(creds, "project_id", None)
    if not project_id:
        raise RuntimeError("Service-Account-JSON enthaelt keine project_id")

    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": generation_config or
            {"temperature": 0.0, "maxOutputTokens": 4096}}
    headers = {"Authorization": f"Bearer {creds.token}",
               "Content-Type": "application/json"}

    gruende: list[str] = []
    log = logging.getLogger(__name__)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for location in GEMINI_LOCATIONS:
            for versuch in range(1, _WIEDERHOLUNGEN + 1):
                try:
                    res = await client.post(_endpoint(location, project_id),
                                            headers=headers, json=body)
                    if res.status_code != 200:
                        gruende.append(f"{location} (Versuch {versuch}): "
                                       f"HTTP {res.status_code}: {res.text[:200]}")
                        if res.status_code in _VORUEBERGEHEND and versuch < _WIEDERHOLUNGEN:
                            log.warning("Vertex Gemini: %s antwortete mit HTTP %s — "
                                        "Wiederholung in %.1f s",
                                        location, res.status_code, _WARTEN_SEK)
                            await asyncio.sleep(_WARTEN_SEK)
                            continue
                        log.warning("Vertex Gemini: %s antwortete mit HTTP %s — "
                                    "versuche naechste Region", location, res.status_code)
                        break
                    data = res.json()
                    cands = data.get("candidates") or []
                    if not cands:
                        pf = data.get("promptFeedback") or {}
                        grund = pf.get("blockReason")
                        if grund:
                            gruende.append(f"{location}: von der Sicherheitspruefung "
                                           f"abgelehnt (blockReason={grund})")
                            # Die naechste Region lehnt dasselbe genauso ab.
                            raise RuntimeError("Gemini-Aufruf fehlgeschlagen — "
                                               + "; ".join(gruende))
                        gruende.append(f"{location}: keine candidates ({str(data)[:160]})")
                        break
                    if pruefe_abbruch:
                        _pruefe_abbruch(cands[0], location)
                    parts_out = (cands[0].get("content") or {}).get("parts") or []
                    return "".join(p.get("text", "") for p in parts_out).strip()
                except KiAntwortAbgeschnitten:
                    raise            # Die naechste Region wuerde genauso abbrechen.
                except httpx.HTTPError as e:
                    # KEINE Wiederholung: Der Erstversuch hat schon `timeout`
                    # Sekunden verbraucht.
                    gruende.append(f"{location}: {type(e).__name__}: {e}")
                    break
                except RuntimeError:
                    raise
                except Exception as e:  # noqa: BLE001
                    gruende.append(f"{location}: {type(e).__name__}: {e}")
                    break
    raise RuntimeError("Gemini-Aufruf fehlgeschlagen — "
                       + ("; ".join(gruende) or "kein Grund ermittelt"))


def _parse_json_lenient(text: str) -> dict:
    """Robustes JSON-Parsing: schneidet ```json-Fences und Vorrede ab."""
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1] if "```" in t[3:] else t[3:]
        if t.lstrip().startswith("json"):
            t = t.lstrip()[4:]
    a, b = t.find("{"), t.rfind("}")
    if a >= 0 and b > a:
        t = t[a:b + 1]
    return json.loads(t)


def _transkript_config(json_antwort: bool) -> dict:
    """Denk-Tokens bringen bei einer Transkription nichts und kosten Laenge —
    bei Flash-Modellen abschalten. Pro-Modelle erlauben das nicht (HTTP 400)."""
    cfg: dict = {"temperature": 0.0, "maxOutputTokens": TRANSKRIPT_MAX_TOKENS}
    if json_antwort:
        cfg["responseMimeType"] = "application/json"
    if "flash" in (GEMINI_MODEL or "").lower():
        cfg["thinkingConfig"] = {"thinkingBudget": 0}
    return cfg


_TRANSKRIPT_PROMPT = (
    "Transkribiere die folgende Audioaufnahme wörtlich und vollständig auf Deutsch. "
    "Gib NUR den gesprochenen Text zurück — ohne Vorrede, ohne Anführungszeichen, "
    "ohne Zeitstempel, ohne Sprecher-Labels. Wenn nichts Verständliches zu hören ist, "
    "gib eine leere Antwort zurück."
)

_MULTILANG_PROMPT = (
    "Du transkribierst eine Audioaufnahme aus dem Arbeitsalltag einer Gebäudereinigungs-Firma. "
    "Der Sprecher kann Deutsch ODER eine andere Sprache sprechen (häufig Türkisch, Polnisch, "
    "Rumänisch, Kroatisch/Bosnisch/Serbisch, Englisch). "
    "Erkenne die gesprochene Sprache, transkribiere wörtlich und liefere eine korrekte deutsche "
    "Übersetzung. Korrigiere offensichtliche Erkennungsfehler sinnvoll. "
    "Antworte AUSSCHLIESSLICH als JSON mit genau diesen Feldern:\n"
    '{\n'
    '  "sprache": "<Sprache des Sprechers auf Deutsch, z.B. Deutsch, Türkisch, Polnisch>",\n'
    '  "original": "<wörtliche Transkription in der Originalsprache>",\n'
    '  "deutsch": "<deutsche Fassung; bei deutschem Original identisch zur Transkription>"\n'
    '}\n'
    "Wenn nichts Verständliches zu hören ist, gib leere Strings zurück."
)


async def transcribe_audio_detail_async(audio_b64: str,
                                        mime_type: str = "audio/webm") -> dict:
    """Mehrsprachige Transkription. Gibt {text, original, sprache} zurueck:

    * ``text``     — deutsche Fassung (immer Deutsch, ggf. uebersetzt)
    * ``original`` — woertliche Transkription in der gesprochenen Sprache
    * ``sprache``  — erkannte Sprache (deutsche Bezeichnung)

    Bei Parsing-Problemen faellt die Funktion robust auf reine
    Deutsch-Transkription zurueck.
    """
    parts = [{"inlineData": {"mimeType": mime_type, "data": audio_b64}},
             {"text": _MULTILANG_PROMPT}]
    raw = await _generate(parts, _transkript_config(json_antwort=True),
                          timeout=TRANSKRIPT_TIMEOUT, pruefe_abbruch=True)
    try:
        d = _parse_json_lenient(raw)
        deutsch = (d.get("deutsch") or "").strip()
        original = (d.get("original") or "").strip()
        sprache = (d.get("sprache") or "").strip()
        # Bei deutscher Aufnahme bleibt `original` laut Prompt leer — die Aufrufer
        # erwarten dort aber den Wortlaut.
        return {"text": deutsch or original,
                "original": original or deutsch,
                "sprache": sprache}
    except KiAntwortAbgeschnitten:
        raise
    except Exception:
        text = await _generate(
            [{"inlineData": {"mimeType": mime_type, "data": audio_b64}},
             {"text": _TRANSKRIPT_PROMPT}],
            _transkript_config(json_antwort=False),
            timeout=TRANSKRIPT_TIMEOUT, pruefe_abbruch=True)
        return {"text": text, "original": text, "sprache": "Deutsch"}


async def transcribe_audio_async(audio_b64: str, mime_type: str = "audio/webm") -> str:
    """Reiner deutscher Transkript-Text (rueckwaertskompatibel)."""
    detail = await transcribe_audio_detail_async(audio_b64, mime_type)
    return detail.get("text", "")


def verfuegbar() -> bool:
    """True, wenn Google-Zugangsdaten bereitstehen — fuer Capability-Anzeigen.

    Bewusst ohne Netzaufruf: Die Oberflaeche will wissen, ob sie den Knopf
    anbieten darf, nicht ob Vertex gerade antwortet.
    """
    return bool(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "").strip()
                or os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip())
