"""zb_shared.ki_client — kanonischer KI-Zugang fuer alle Zitzelsberger-Apps.

Loest die kopierten vertex_embeddings.py + die per-App ANTHROPIC_BACKEND-Switches ab
(Konsolidierung P2.3, [d-303]). EU-Default (DSGVO, [d-211]):
  * Embeddings: Vertex text-multilingual-embedding-002 (768 Dim, europe-west3)
  * Claude:     Vertex AI (europe-west1); im Betrieb (Render) ausschliesslich, lokal per
                ANTHROPIC_BACKEND=direct auch die US-API (siehe IM_BETRIEB unten)

Credentials (Pro-Dienst-Secret statt geteilter Datei, P2.3):
  * GOOGLE_APPLICATION_CREDENTIALS_JSON  — kompletter Service-Account-JSON-Inhalt (Render-Secret), ODER
  * GOOGLE_APPLICATION_CREDENTIALS       — Pfad zur .json (lokal)

Hintergrund [L-188]: nur google-auth (kein grpc) + httpx-REST, damit der gRPC-DNS-Resolver
im Docker-Container die httpx-Aufrufe nicht zerschiesst.
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
from typing import Literal

from zb_shared import logschutz as _logschutz

# Protokollschutz fuer jede App, die den KI-Client nutzt (v0.2.7, Vorfall 09.11.2026).
_logschutz.einschalten()

# ── Modell-/Region-Registry (EINE zentrale Stelle) ───────────────────────────
EMBED_MODEL = os.getenv("VERTEX_EMBED_MODEL", "text-multilingual-embedding-002")
EMBED_DIM = 768
EMBED_LOCATION = os.getenv("VERTEX_EMBED_LOCATION", "europe-west3")
CLAUDE_LOCATION = os.getenv("VERTEX_CLAUDE_LOCATION", "europe-west1")
# Seit 2026-11-03 (v0.2.6): Im Betrieb (Render, Env RENDER gesetzt) laeuft Claude NUR ueber
# Vertex AI in der EU. Google hat bestaetigt, dass Anthropic dabei kein Unterauftragsverarbeiter
# ist (Google hostet die Modelle, kein Training, EU) — Auftragsverarbeiter ist allein Google.
# Fehlt ANTHROPIC_BACKEND auf Render, gilt 'vertex'; steht dort 'direct', liefert get_anthropic_*
# None (Aufrufer blendet die KI-Funktion aus) statt still an api.anthropic.com (USA) zu gehen.
# Bewusste Ausnahme nur mit ANTHROPIC_DIREKT_AUSNAHME=<Begruendung> (z. B. ai-news-agent:
# web_search gibt es nur auf der Direkt-API, keine Personendaten). Lokal bleibt 'direct' moeglich.
IM_BETRIEB = bool(os.getenv("RENDER"))
ANTHROPIC_BACKEND = os.getenv("ANTHROPIC_BACKEND", "vertex" if IM_BETRIEB else "direct").strip().lower()
DIREKT_AUSNAHME = os.getenv("ANTHROPIC_DIREKT_AUSNAHME", "").strip()


def direkt_erlaubt() -> bool:
    """US-Direktweg nur lokal oder mit ausdruecklicher, begruendeter Ausnahme."""
    return (not IM_BETRIEB) or bool(DIREKT_AUSNAHME)


if IM_BETRIEB and ANTHROPIC_BACKEND != "vertex":
    import logging as _logging
    _logging.getLogger("zb_shared.ki_client").error(
        "ANTHROPIC_BACKEND=%r im Betrieb: %s", ANTHROPIC_BACKEND,
        f"Direktweg per Ausnahme erlaubt ({DIREKT_AUSNAHME})" if DIREKT_AUSNAHME
        else "Claude-Aufrufe werden verweigert (nur Vertex EU erlaubt)")
CLAUDE_MODEL_DIRECT = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
# EU-Default: in europe-west1 ist (Stand 2026-06-26) als aktuelles Claude NUR
# claude-sonnet-4-5@20250929 verfuegbar (sonnet-4-6 existiert dort NICHT -> 404). [L-356]
CLAUDE_MODEL_VERTEX = os.getenv("ANTHROPIC_MODEL_VERTEX", "claude-sonnet-4-5@20250929")


def claude_model() -> str:
    """Das passende Claude-Modell je Backend (Vertex braucht den @version-Suffix)."""
    return CLAUDE_MODEL_VERTEX if ANTHROPIC_BACKEND == "vertex" else CLAUDE_MODEL_DIRECT


def using_vertex() -> bool:
    return ANTHROPIC_BACKEND == "vertex"


# ── GCP-Credentials-Bootstrap (Render-Secret -> ADC) ─────────────────────────
def ensure_gcp_creds() -> bool:
    """Stellt Application-Default-Credentials bereit: GOOGLE_APPLICATION_CREDENTIALS_JSON
    (Inhalt) -> Temp-Datei -> GOOGLE_APPLICATION_CREDENTIALS. True, wenn Creds verfuegbar."""
    pfad = (os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or "").strip()
    if pfad.startswith("{"):
        # v0.2.7: Schlüssel-INHALT steht in der Pfad-Variable (Vorfall 09.11.2026). Früher hiess
        # es hier „vorhanden“, google-auth versuchte den Inhalt als Datei zu oeffnen und schrieb
        # ihn in die Fehlermeldung. Jetzt: wie _JSON behandeln, Pfad-Variable ersetzen, warnen
        # (ohne Inhalt).
        import logging as _logging
        _logging.getLogger("zb_shared.ki_client").warning(
            "GOOGLE_APPLICATION_CREDENTIALS enthaelt JSON statt eines Dateipfads — bitte in "
            "GOOGLE_APPLICATION_CREDENTIALS_JSON umbenennen. Wird diesmal automatisch umgesetzt.")
        os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "").strip():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = pfad
        pfad = ""
    if pfad:
        return True
    raw = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "").strip()
    if not raw:
        return False
    try:
        info = json.loads(raw)
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(info, f)
        f.close()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name
        return True
    except Exception:
        return False


# ── Vertex-Embeddings (REST, kein grpc) ──────────────────────────────────────
_creds = None
_creds_lock = threading.Lock()


def _vertex_credentials():
    from google.oauth2 import service_account
    import google.auth.transport.requests

    global _creds
    if _creds is None:
        with _creds_lock:
            if _creds is None:
                scopes = ["https://www.googleapis.com/auth/cloud-platform"]
                j = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "").strip()
                if j:
                    _creds = service_account.Credentials.from_service_account_info(
                        json.loads(j), scopes=scopes)
                else:
                    p = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
                    if not p:
                        raise RuntimeError(
                            "Keine GCP-Credentials: GOOGLE_APPLICATION_CREDENTIALS_JSON (Inhalt) "
                            "oder GOOGLE_APPLICATION_CREDENTIALS (Pfad) setzen.")
                    _creds = service_account.Credentials.from_service_account_file(p, scopes=scopes)
    if not _creds.valid:
        _creds.refresh(google.auth.transport.requests.Request())
    return _creds


def _embed_endpoint() -> str:
    creds = _vertex_credentials()
    pid = creds.project_id
    if not pid:
        raise RuntimeError("Service-Account-JSON enthaelt keine project_id.")
    return (f"https://{EMBED_LOCATION}-aiplatform.googleapis.com/v1/"
            f"projects/{pid}/locations/{EMBED_LOCATION}/"
            f"publishers/google/models/{EMBED_MODEL}:predict")


def _payload(texts: list[str], kind: str) -> dict:
    task = "RETRIEVAL_DOCUMENT" if kind == "passage" else "RETRIEVAL_QUERY"
    return {"instances": [{"content": t, "task_type": task} for t in texts]}


def embed_batch_sync(texts: list[str], kind: Literal["passage", "query"] = "passage") -> list[list[float]]:
    """Synchrone Vertex-Embeddings (768 Dim, EU). Vertex-Limit 5 instances/Call -> intern gebatcht."""
    import httpx
    if not texts:
        return []
    creds = _vertex_credentials()
    endpoint = _embed_endpoint()
    out: list[list[float]] = []
    with httpx.Client(timeout=30.0) as c:
        for i in range(0, len(texts), 5):
            r = c.post(endpoint,
                       headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"},
                       json=_payload(texts[i:i + 5], kind))
            if r.status_code != 200:
                raise RuntimeError(f"Vertex Embed HTTP {r.status_code}: {r.text[:300]}")
            for p in r.json().get("predictions", []):
                out.append(list(p["embeddings"]["values"]))
    return out


async def embed_batch_async(texts: list[str], kind: Literal["passage", "query"] = "passage") -> list[list[float]]:
    """Async-Variante (FastAPI). Identischer Vektor-Raum wie embed_batch_sync."""
    import httpx
    if not texts:
        return []
    creds = _vertex_credentials()
    endpoint = _embed_endpoint()
    out: list[list[float]] = []
    async with httpx.AsyncClient(timeout=30.0) as c:
        for i in range(0, len(texts), 5):
            r = await c.post(endpoint,
                             headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"},
                             json=_payload(texts[i:i + 5], kind))
            if r.status_code != 200:
                raise RuntimeError(f"Vertex Embed HTTP {r.status_code}: {r.text[:300]}")
            for p in r.json().get("predictions", []):
                out.append(list(p["embeddings"]["values"]))
    return out


def embed_query(text: str) -> list[float]:
    return embed_batch_sync([text], kind="query")[0]


async def embed_query_async(text: str) -> list[float]:
    """Async-Einzel-Query-Embedding (768 Dim, EU). Identischer Vektor-Raum wie embed_query."""
    return (await embed_batch_async([text], kind="query"))[0]


def gcp_credentials():
    """Refreshte GCP-Service-Account-Credentials (mit .token) fuer Apps, die selbst Vertex-REST-Calls
    bauen (z. B. vertex_gemini). Ersetzt das fruehere per-App vertex_embeddings._get_credentials()."""
    return _vertex_credentials()


# ── Claude-Client: direct (US) oder Vertex (EU) ──────────────────────────────
def get_anthropic_async():
    """AsyncAnthropic (direct) ODER AsyncAnthropicVertex (EU) je ANTHROPIC_BACKEND.
    None, wenn Voraussetzungen fehlen (Key/Creds) -> Aufrufer blendet KI-Funktion aus."""
    try:
        import anthropic
    except ImportError:
        return None
    try:
        if ANTHROPIC_BACKEND == "vertex":
            if not ensure_gcp_creds():
                return None
            from anthropic import AsyncAnthropicVertex
            return AsyncAnthropicVertex(region=CLAUDE_LOCATION, project_id=_vertex_credentials().project_id)
        if not direkt_erlaubt():
            return None
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            return None
        return anthropic.AsyncAnthropic(api_key=key)
    except Exception:
        return None


def get_anthropic_sync():
    """Synchrone Variante (Skripte/Hintergrund)."""
    try:
        import anthropic
    except ImportError:
        return None
    try:
        if ANTHROPIC_BACKEND == "vertex":
            if not ensure_gcp_creds():
                return None
            from anthropic import AnthropicVertex
            return AnthropicVertex(region=CLAUDE_LOCATION, project_id=_vertex_credentials().project_id)
        if not direkt_erlaubt():
            return None
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            return None
        return anthropic.Anthropic(api_key=key)
    except Exception:
        return None
