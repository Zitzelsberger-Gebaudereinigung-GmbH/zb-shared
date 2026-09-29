"""zb_shared.replikat — KI-Replikate: persoenliche Sprach-Abbilder einer echten Person.

Ein KI-Replikat (Begriff nach Sven Gabor Janszky, "2035 — The Future Begins Today") ist
KEIN Allzweck-Assistent, sondern das Abbild EINES Menschen: Sprache, Modulation, Wortwahl
und Humor werden nachgebildet, das Wissen bleibt auf das begrenzt, was die Person wirklich
weiss. Dieses Modul setzt genau die drei Merkmale technisch um:

1. Persoenliches Abbild  -> `Stilprofil` (aus eigenen Texten gelernt) + `Persona.weiss_ueber`
                            / `weiss_nicht`. Das Replikat erfindet nichts, was das Original
                            nicht wissen kann, und sagt "weiss ich nicht" in DESSEN Worten.
2. Mehrfachnutzung       -> mehrere Personas pro Mensch, je Lebensbereich (arbeit, familie,
                            mentoring, uebersetzung). `VORLAGEN` liefert Startprofile,
                            gespeichert wird je Persona eine JSON-Datei.
3. Stimme als Hauptkanal -> `fuer_stimme()` macht aus Chat-Text sprechbaren Text (keine
                            Listen, keine Abkuerzungen, kurze Saetze), `sprich()` erzeugt
                            per Google Cloud TTS (EU-Endpunkt) MP3-Bytes.

Design-Prinzipien (analog mailer/pdf, [d-303]):
- Transport ausschliesslich ueber `zb_shared.ki_client` (Claude direct/Vertex-EU, EU-Default).
  Dieses Modul kennt weder API-Keys noch Regionen.
- App-spezifisch BLEIBT app-seitig: Wissensquelle (RAG/DB), Audio-Aufnahme, UI. Die
  Wissensquelle wird als Callable uebergeben (`Replikat(..., wissensquelle=...)`).
- Schwere Importe (httpx, anthropic) sind lazy — `import zb_shared.replikat` kostet nichts.
- Datenschutz: Profile sind personenbezogene Daten. Sie liegen ausserhalb des Repos
  (REPLIKAT_PROFIL_DIR) und gehoeren NICHT in Git.

API:
    Stilprofil / Stimme / Persona          — Datenmodell (JSON-serialisierbar)
    vorlage(bereich, name, ...)            — Startprofil je Lebensbereich
    speichere_persona / lade_persona / liste_personas
    stilprofil_aus_texten(...)             — Stil aus eigenen Texten lernen (sync/async)
    texte_aus_verzeichnis(...)             — eigene Texte einsammeln
    system_prompt(persona, ...)            — Replikat-Systemprompt
    Replikat(persona).antwort_sync(frage)  — Dialog (sync + async)
    fuer_stimme(text) / sprich(text, ...)  — Sprachkanal

CLI:  python -m zb_shared.replikat neu|lernen|chat|sprich|personas
"""
from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable, Optional, Union

from . import ki_client

logger = logging.getLogger(__name__)

# Wissensquelle: bekommt die Frage, liefert Kontexttext (oder "" wenn nichts passt).
# Sync ODER async — beides wird unterstuetzt.
Wissensquelle = Callable[[str], Union[str, Awaitable[str]]]

MAX_VERLAUF = 12          # gespeicherte Dialog-Nachrichten (User+Assistant), FIFO
MAX_TOKENS_TEXT = 1200
MAX_TOKENS_STIMME = 400   # Stimme = kurze Antworten, sonst redet das Replikat den Nutzer tot


# ── Datenmodell ──────────────────────────────────────────────────────────────
@dataclass
class Stilprofil:
    """Das sprachliche Fingerabdruck-Profil einer Person. Wird aus eigenen Texten gelernt
    (`stilprofil_aus_texten`) oder von Hand gepflegt."""
    anrede: str = "du"                                    # "du" | "sie"
    satzbau: str = ""                                     # z.B. "kurze Hauptsaetze, selten Nebensatz"
    tempo: str = ""                                       # Modulation/Sprechtempo fuer den Stimmkanal
    humor: str = ""                                       # Art des Humors (trocken, ironisch, ...)
    wortwahl: list[str] = field(default_factory=list)     # typische Woerter/Floskeln
    vermeiden: list[str] = field(default_factory=list)    # Woerter, die die Person NIE benutzt
    begruessung: list[str] = field(default_factory=list)
    verabschiedung: list[str] = field(default_factory=list)
    unsicherheit: list[str] = field(default_factory=list) # wie die Person "weiss ich nicht" sagt
    o_ton: list[str] = field(default_factory=list)        # woertliche Beispielsaetze (Few-Shot)

    def als_prompt_block(self) -> str:
        """Der Stil als Prompt-Abschnitt. Leere Felder werden weggelassen."""
        zeilen: list[str] = []
        if self.anrede:
            zeilen.append(f"- Anrede: {'duzen' if self.anrede.lower().startswith('du') else 'siezen'}")
        for label, wert in (("Satzbau", self.satzbau), ("Sprechtempo/Modulation", self.tempo),
                            ("Humor", self.humor)):
            if wert:
                zeilen.append(f"- {label}: {wert}")
        for label, werte in (("Typische Wörter/Floskeln", self.wortwahl),
                             ("Niemals benutzen", self.vermeiden),
                             ("Begrüßt so", self.begruessung),
                             ("Verabschiedet sich so", self.verabschiedung),
                             ("Sagt Nichtwissen so", self.unsicherheit)):
            if werte:
                zeilen.append(f"- {label}: " + "; ".join(str(w) for w in werte))
        if self.o_ton:
            zeilen.append("- O-Ton (Originalsätze, Ton treffen, NICHT wörtlich wiederholen):")
            zeilen += [f'    "{s}"' for s in self.o_ton]
        return "\n".join(zeilen)


@dataclass
class Stimme:
    """Stimm-Einstellungen fuer den Hauptkanal Sprache (Google Cloud TTS)."""
    stimme_id: str = "de-DE-Wavenet-B"
    sprache: str = "de-DE"
    tempo: float = 1.0        # speakingRate 0.25 - 4.0
    tonhoehe: float = 0.0     # pitch -20.0 - 20.0


@dataclass
class Persona:
    """Ein Replikat-Profil = ein Lebensbereich eines Menschen (Janszky: Mehrfachnutzung)."""
    id: str
    name: str                                                  # Name des Originals
    lebensbereich: str = "arbeit"                              # arbeit|familie|mentoring|uebersetzung|...
    rolle: str = ""                                            # "Geschaeftsfuehrer der ..."
    auftrag: str = ""                                          # wofuer dieses Replikat da ist
    sprachen: list[str] = field(default_factory=lambda: ["Deutsch"])
    stil: Stilprofil = field(default_factory=Stilprofil)
    weiss_ueber: list[str] = field(default_factory=list)        # Wissensgebiete des Originals
    weiss_nicht: list[str] = field(default_factory=list)        # bewusste Wissensluecken
    freigabe_pflichtig: list[str] = field(default_factory=list) # nur das Original entscheidet
    tabus: list[str] = field(default_factory=list)
    offenlegung: bool = True                                   # sagt auf Nachfrage: ich bin ein Replikat
    stimme: Stimme = field(default_factory=Stimme)
    modell: Optional[str] = None                               # None -> ki_client.claude_model()

    # ── JSON ──
    def as_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Persona":
        d = dict(d or {})
        stil = d.pop("stil", None) or {}
        stimme = d.pop("stimme", None) or {}
        bekannt = {f for f in cls.__dataclass_fields__}
        unbekannt = [k for k in d if k not in bekannt]
        for k in unbekannt:                      # Vorwaertskompatibilitaet: Unbekanntes ignorieren
            logger.debug("Persona-Feld '%s' unbekannt — ignoriert", k)
            d.pop(k)
        return cls(
            stil=Stilprofil(**{k: v for k, v in stil.items() if k in Stilprofil.__dataclass_fields__}),
            stimme=Stimme(**{k: v for k, v in stimme.items() if k in Stimme.__dataclass_fields__}),
            **d,
        )


# ── Vorlagen je Lebensbereich (Janszky: mehrere Replikate pro Mensch) ────────
VORLAGEN: dict[str, dict] = {
    "arbeit": {
        "auftrag": "Beantwortet berufliche Fragen von Team, Kunden und Partnern so, wie "
                   "{name} sie beantworten würde — Entscheidungen bleiben beim Original.",
        "weiss_ueber": ["das eigene Unternehmen und seine Abläufe", "die eigenen Kunden und Projekte",
                        "die eigene Branche"],
        "weiss_nicht": ["Interna anderer Unternehmen", "alles nach dem letzten Wissensstand-Update"],
        "freigabe_pflichtig": ["Preise und Angebote", "Verträge und Kündigungen",
                               "Personalentscheidungen", "rechtlich bindende Zusagen"],
    },
    "familie": {
        "auftrag": "Ist für Familie und enge Freunde da: erzählt, erinnert, hört zu — im "
                   "privaten Ton von {name}.",
        "weiss_ueber": ["die eigene Familiengeschichte", "gemeinsame Erlebnisse", "persönliche Vorlieben"],
        "weiss_nicht": ["berufliche Interna", "was nach dem letzten Update passiert ist"],
        "freigabe_pflichtig": ["Geld und Finanzen", "gesundheitliche Auskünfte", "Termine zusagen"],
    },
    "mentoring": {
        "auftrag": "Begleitet Mitarbeitende und Mentees mit den Erfahrungen von {name}: "
                   "fragt nach, ordnet ein, gibt Rat aus eigener Praxis.",
        "weiss_ueber": ["die eigene Berufsbiografie", "eigene Fehler und was daraus wurde",
                        "Führung im eigenen Alltag"],
        "weiss_nicht": ["Fachgebiete außerhalb der eigenen Erfahrung", "persönliche Daten Dritter"],
        "freigabe_pflichtig": ["Beurteilungen von Personen", "Gehalt und Karrierezusagen"],
    },
    "uebersetzung": {
        "auftrag": "Gibt das Gesagte von {name} in einer anderen Sprache wieder — gleiche "
                   "Aussage, gleicher Ton, gleiche Direktheit.",
        "weiss_ueber": ["die eigenen Themen und Fachbegriffe"],
        "weiss_nicht": ["alles, was das Original nicht gesagt hat — nichts hinzuerfinden"],
        "freigabe_pflichtig": ["inhaltliche Zusagen, die im Original nicht stehen"],
    },
}


def vorlage(lebensbereich: str, name: str, *, persona_id: str = "", rolle: str = "",
            stil: Optional[Stilprofil] = None) -> Persona:
    """Startprofil fuer einen Lebensbereich. Der Stil kommt spaeter aus `stilprofil_aus_texten`."""
    bereich = (lebensbereich or "arbeit").strip().lower()
    v = VORLAGEN.get(bereich)
    if v is None:
        raise ValueError(f"Unbekannter Lebensbereich '{lebensbereich}'. Bekannt: {', '.join(VORLAGEN)}")
    pid = persona_id or f"{_slug(name)}-{bereich}"
    return Persona(
        id=pid,
        name=name,
        lebensbereich=bereich,
        rolle=rolle,
        auftrag=v["auftrag"].format(name=name),
        stil=stil or Stilprofil(),
        weiss_ueber=list(v["weiss_ueber"]),
        weiss_nicht=list(v["weiss_nicht"]),
        freigabe_pflichtig=list(v["freigabe_pflichtig"]),
    )


def _slug(text: str) -> str:
    umlaute = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    t = "".join(umlaute.get(c, c) for c in (text or "").lower())
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "replikat"


# ── Persistenz (Profile sind personenbezogene Daten -> ausserhalb des Repos) ──
def profil_verzeichnis(verzeichnis: Optional[Union[str, Path]] = None) -> Path:
    """Ablageort der Profile: Argument > ENV REPLIKAT_PROFIL_DIR > ~/.zb/replikate."""
    p = verzeichnis or os.getenv("REPLIKAT_PROFIL_DIR") or (Path.home() / ".zb" / "replikate")
    return Path(p).expanduser()


def speichere_persona(persona: Persona, verzeichnis: Optional[Union[str, Path]] = None) -> Path:
    d = profil_verzeichnis(verzeichnis)
    d.mkdir(parents=True, exist_ok=True)
    pfad = d / f"{persona.id}.json"
    pfad.write_text(json.dumps(persona.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return pfad


def lade_persona(persona_id: str, verzeichnis: Optional[Union[str, Path]] = None) -> Persona:
    pfad = profil_verzeichnis(verzeichnis) / f"{persona_id}.json"
    if not pfad.exists():
        raise FileNotFoundError(f"Kein Replikat-Profil '{persona_id}' in {pfad.parent}")
    return Persona.from_dict(json.loads(pfad.read_text(encoding="utf-8")))


def liste_personas(verzeichnis: Optional[Union[str, Path]] = None) -> list[str]:
    d = profil_verzeichnis(verzeichnis)
    return sorted(p.stem for p in d.glob("*.json")) if d.exists() else []


# ── Systemprompt: das eigentliche Replikat ───────────────────────────────────
def system_prompt(persona: Persona, *, kanal: str = "text", zusatz: str = "") -> str:
    """Baut den Replikat-Systemprompt. `kanal="stimme"` ergaenzt die Sprechregeln."""
    p = persona
    teile: list[str] = []

    kopf = f"Du bist das KI-Replikat von {p.name}"
    if p.rolle:
        kopf += f" ({p.rolle})"
    kopf += (". Du bist kein allgemeiner Assistent, sondern das sprachliche Abbild dieses "
             "einen Menschen. Du antwortest in der Ich-Form als " + p.name + ".")
    teile.append(kopf)
    if p.auftrag:
        teile.append(f"Auftrag dieses Replikats ({p.lebensbereich}): {p.auftrag}")

    stil = p.stil.als_prompt_block()
    if stil:
        teile.append("So spricht " + p.name + " — halte dich exakt daran:\n" + stil)
    if p.sprachen:
        teile.append("Sprachen: " + ", ".join(p.sprachen) +
                     ". Antworte in der Sprache der Frage, der Ton bleibt derselbe.")

    # Kern des Replikat-Begriffs: Abbild statt Allwissen.
    grenzen = ["Du bist NICHT allwissend. Dein Wissen ist genau das Wissen von " + p.name + " — "
               "nicht mehr. Wissen, das dieser Mensch nicht hat, hast du auch nicht."]
    if p.weiss_ueber:
        grenzen.append("Kennt sich aus mit: " + "; ".join(p.weiss_ueber) + ".")
    if p.weiss_nicht:
        grenzen.append("Kennt sich NICHT aus mit: " + "; ".join(p.weiss_nicht) + ".")
    grenzen.append("Wenn du etwas nicht weißt: sag es so, wie " + p.name + " es sagen würde, "
                   "und biete an, das Original zu fragen. Erfinde niemals Fakten, Zahlen, "
                   "Termine oder Zusagen. Lieber eine kurze ehrliche Antwort als eine erfundene.")
    teile.append("\n".join(grenzen))

    if p.freigabe_pflichtig:
        teile.append("Freigabepflichtig — dazu triffst du KEINE Entscheidung und gibst keine "
                     "verbindliche Zusage, sondern verweist an " + p.name + " selbst: "
                     + "; ".join(p.freigabe_pflichtig) + ".")
    if p.tabus:
        teile.append("Tabuthemen (nicht beantworten, freundlich abbiegen): " + "; ".join(p.tabus) + ".")
    if p.offenlegung:
        teile.append("Wenn jemand fragt, ob er mit einem Menschen oder einer KI spricht: sag "
                     "klar, dass du das KI-Replikat von " + p.name + " bist. Behaupte nie, "
                     "der Mensch selbst zu sein.")

    if kanal == "stimme":
        teile.append(SPRECHREGELN)
    if zusatz:
        teile.append(zusatz.strip())
    return "\n\n".join(t for t in teile if t)


SPRECHREGELN = (
    "Kanal: Stimme (Ohrstöpsel/Brille). Deine Antwort wird vorgelesen, nicht gelesen:\n"
    "- Höchstens 3 bis 4 Sätze, dann eine Rückfrage oder ein Punkt.\n"
    "- Keine Aufzählungen, keine Überschriften, keine Sonderzeichen, kein Markdown.\n"
    "- Zahlen, Abkürzungen und Einheiten ausschreiben, wie man sie spricht.\n"
    "- Sprich wie im Gespräch: kurze Hauptsätze, Pausen durch Punkte statt Kommaketten."
)


# ── Dialog ───────────────────────────────────────────────────────────────────
class Replikat:
    """Ein sprechendes Replikat. Haelt Persona + Dialogverlauf, ruft Claude via ki_client.

        r = Replikat(lade_persona("oliver-arbeit"))
        print(r.antwort_sync("Wie läuft die Glasreinigung im Objekt Nord?"))

    `wissensquelle` ist die Bruecke zum App-Wissen (RAG, DB, Kalender): Callable(frage) ->
    Kontexttext, sync oder async. Sie bleibt app-seitig, damit dieses Modul keine DB kennt.
    """

    def __init__(self, persona: Persona, *, wissensquelle: Optional[Wissensquelle] = None,
                 kanal: str = "text", max_verlauf: int = MAX_VERLAUF,
                 modell: Optional[str] = None, client: Any = None):
        self.persona = persona
        self.wissensquelle = wissensquelle
        self.kanal = kanal
        self.max_verlauf = max(2, int(max_verlauf))
        self.modell = modell or persona.modell or ki_client.claude_model()
        self._client = client
        self.verlauf: list[dict] = []

    # ── Prompt/Nachrichten (netzwerkfrei, damit testbar) ──
    @property
    def system_prompt(self) -> str:
        return system_prompt(self.persona, kanal=self.kanal)

    def _nachrichten(self, frage: str, kontext: str = "") -> list[dict]:
        inhalt = frage
        if kontext:
            inhalt = ("Wissen aus deinen eigenen Unterlagen (nur nutzen, wenn es zur Frage "
                      "passt; kein Wort darüber, dass es 'Unterlagen' gibt):\n"
                      f"{kontext}\n\n---\nFrage: {frage}")
        return self.verlauf + [{"role": "user", "content": inhalt}]

    def _merke(self, frage: str, antwort: str) -> None:
        self.verlauf.append({"role": "user", "content": frage})
        self.verlauf.append({"role": "assistant", "content": antwort})
        if len(self.verlauf) > self.max_verlauf:
            self.verlauf = self.verlauf[-self.max_verlauf:]
            while self.verlauf and self.verlauf[0]["role"] != "user":  # Paare sauber halten
                self.verlauf.pop(0)

    def verlauf_zuruecksetzen(self) -> None:
        self.verlauf = []

    def _max_tokens(self) -> int:
        return MAX_TOKENS_STIMME if self.kanal == "stimme" else MAX_TOKENS_TEXT

    # ── Aufrufe ──
    async def antwort(self, frage: str, *, kontext: str = "") -> str:
        """Async-Antwort (FastAPI/WebSocket). Leerer String, wenn kein KI-Client verfuegbar ist."""
        client = self._client or ki_client.get_anthropic_async()
        if client is None:
            logger.warning("Kein Anthropic-Client (Key/Creds fehlen) — Replikat antwortet nicht")
            return ""
        if not kontext and self.wissensquelle is not None:
            kontext = await _wissen_async(self.wissensquelle, frage)
        r = await client.messages.create(
            model=self.modell,
            max_tokens=self._max_tokens(),
            system=self.system_prompt,
            messages=self._nachrichten(frage, kontext),
        )
        antwort = _text_aus_antwort(r)
        if self.kanal == "stimme":
            antwort = fuer_stimme(antwort)
        self._merke(frage, antwort)
        return antwort

    def antwort_sync(self, frage: str, *, kontext: str = "") -> str:
        """Synchrone Antwort (Skripte, CLI, Cron)."""
        client = self._client or ki_client.get_anthropic_sync()
        if client is None:
            logger.warning("Kein Anthropic-Client (Key/Creds fehlen) — Replikat antwortet nicht")
            return ""
        if not kontext and self.wissensquelle is not None:
            kontext = _wissen_sync(self.wissensquelle, frage)
        r = client.messages.create(
            model=self.modell,
            max_tokens=self._max_tokens(),
            system=self.system_prompt,
            messages=self._nachrichten(frage, kontext),
        )
        antwort = _text_aus_antwort(r)
        if self.kanal == "stimme":
            antwort = fuer_stimme(antwort)
        self._merke(frage, antwort)
        return antwort

    def sprich(self, text: str) -> bytes:
        """Antworttext -> MP3-Bytes mit der Stimme dieser Persona."""
        return sprich(text, stimme=self.persona.stimme)


async def _wissen_async(quelle: Wissensquelle, frage: str) -> str:
    try:
        erg = quelle(frage)
        if hasattr(erg, "__await__"):
            erg = await erg
        return str(erg or "")
    except Exception as e:                                   # Wissensquelle darf nie den Dialog killen
        logger.warning("Wissensquelle fehlgeschlagen: %s", e)
        return ""


def _wissen_sync(quelle: Wissensquelle, frage: str) -> str:
    try:
        erg = quelle(frage)
        if hasattr(erg, "__await__"):
            logger.warning("Async-Wissensquelle in antwort_sync — uebersprungen (antwort() nutzen)")
            if hasattr(erg, "close"):
                erg.close()          # Coroutine schliessen, sonst RuntimeWarning
            return ""
        return str(erg or "")
    except Exception as e:
        logger.warning("Wissensquelle fehlgeschlagen: %s", e)
        return ""


def _text_aus_antwort(response: Any) -> str:
    """Text aus einer Anthropic-Message (alle Text-Bloecke)."""
    teile = []
    for block in getattr(response, "content", None) or []:
        t = getattr(block, "text", None)
        if t:
            teile.append(t)
    return "\n".join(teile).strip()


# ── Training: Stil aus eigenen Texten lernen ─────────────────────────────────
_STIL_AUFTRAG = """Du analysierst den Schreib- und Sprechstil EINES Menschen: {name}.

Unten stehen Originaltexte dieser Person (E-Mails, Nachrichten, Gesprächsmitschriften).
Leite daraus das Stilprofil ab — nur was wirklich belegt ist, nichts Erfundenes.

Antworte ausschließlich mit JSON in genau dieser Form:
{{
  "anrede": "du" oder "sie",
  "satzbau": "ein Satz zur typischen Satzlänge und -struktur",
  "tempo": "ein Satz zu Sprechtempo/Modulation, falls erkennbar, sonst leer",
  "humor": "ein Satz zur Art des Humors, sonst leer",
  "wortwahl": ["typische Wörter und Floskeln, max. 15"],
  "vermeiden": ["Wörter/Formulierungen, die diese Person auffällig NIE benutzt, max. 8"],
  "begruessung": ["typische Begrüßungen, max. 5"],
  "verabschiedung": ["typische Verabschiedungen, max. 5"],
  "unsicherheit": ["wie diese Person ausdrückt, dass sie etwas nicht weiß, max. 5"],
  "o_ton": ["8 bis 12 besonders charakteristische Originalsätze, wörtlich aus den Texten"]
}}

Originaltexte:
---
{texte}
---"""


def _stil_prompt(name: str, texte: list[str], max_zeichen: int = 60000) -> str:
    korpus = "\n\n---\n\n".join(t.strip() for t in texte if t and t.strip())
    if len(korpus) > max_zeichen:
        korpus = korpus[:max_zeichen]
    return _STIL_AUFTRAG.format(name=name, texte=korpus)


def _json_aus_antwort(text: str) -> dict:
    """Robustes JSON-Parsen: mit/ohne ```-Fence, mit Vor-/Nachgeplapper."""
    t = (text or "").strip()
    fence = re.search(r"```(?:json)?\s*(.+?)```", t, re.S)
    if fence:
        t = fence.group(1).strip()
    if not t.startswith("{"):
        start, ende = t.find("{"), t.rfind("}")
        if start == -1 or ende <= start:
            raise ValueError("Keine JSON-Struktur in der Antwort gefunden")
        t = t[start:ende + 1]
    return json.loads(t)


def _stil_aus_json(d: dict) -> Stilprofil:
    erlaubt = Stilprofil.__dataclass_fields__
    return Stilprofil(**{k: v for k, v in (d or {}).items() if k in erlaubt})


def stilprofil_aus_texten(texte: list[str], name: str, *, modell: Optional[str] = None,
                          client: Any = None) -> Stilprofil:
    """Lernt das Stilprofil aus eigenen Texten (sync). Braucht einen KI-Client —
    ohne Client kommt ein leeres Stilprofil zurueck (Aufrufer blendet die Funktion aus)."""
    c = client or ki_client.get_anthropic_sync()
    if c is None:
        logger.warning("Kein Anthropic-Client — Stilprofil bleibt leer")
        return Stilprofil()
    r = c.messages.create(
        model=modell or ki_client.claude_model(),
        max_tokens=2000,
        messages=[{"role": "user", "content": _stil_prompt(name, texte)}],
    )
    return _stil_aus_json(_json_aus_antwort(_text_aus_antwort(r)))


async def stilprofil_aus_texten_async(texte: list[str], name: str, *, modell: Optional[str] = None,
                                      client: Any = None) -> Stilprofil:
    """Async-Variante von `stilprofil_aus_texten`."""
    c = client or ki_client.get_anthropic_async()
    if c is None:
        logger.warning("Kein Anthropic-Client — Stilprofil bleibt leer")
        return Stilprofil()
    r = await c.messages.create(
        model=modell or ki_client.claude_model(),
        max_tokens=2000,
        messages=[{"role": "user", "content": _stil_prompt(name, texte)}],
    )
    return _stil_aus_json(_json_aus_antwort(_text_aus_antwort(r)))


def texte_aus_verzeichnis(pfad: Union[str, Path], endungen: tuple[str, ...] = (".txt", ".md"),
                          max_dateien: int = 200) -> list[str]:
    """Sammelt eigene Texte (E-Mail-Exporte, Notizen, Transkripte) aus einem Ordner —
    rekursiv, alphabetisch, leere Dateien raus."""
    basis = Path(pfad).expanduser()
    if not basis.exists():
        raise FileNotFoundError(f"Textordner nicht gefunden: {basis}")
    out: list[str] = []
    for datei in sorted(basis.rglob("*")):
        if len(out) >= max_dateien:
            break
        if datei.is_file() and datei.suffix.lower() in endungen:
            try:
                inhalt = datei.read_text(encoding="utf-8", errors="ignore").strip()
            except OSError as e:
                logger.warning("Datei uebersprungen (%s): %s", datei.name, e)
                continue
            if inhalt:
                out.append(inhalt)
    return out


# ── Stimme (Hauptkanal) ──────────────────────────────────────────────────────
# Gesprochen statt geschrieben: Abkuerzungen ausschreiben, Markdown raus.
_ABKUERZUNGEN = [
    (r"\bz\.\s?B\.", "zum Beispiel"), (r"\bd\.\s?h\.", "das heißt"),
    (r"\bu\.\s?a\.", "unter anderem"), (r"\bbzw\.", "beziehungsweise"),
    (r"\bca\.", "circa"), (r"\bevtl\.", "eventuell"), (r"\bggf\.", "gegebenenfalls"),
    (r"\binkl\.", "inklusive"), (r"\bexkl\.", "exklusive"), (r"\bzzgl\.", "zuzüglich"),
    (r"\bMio\.", "Millionen"), (r"\bMrd\.", "Milliarden"), (r"\bNr\.", "Nummer"),
    (r"\bStk\.", "Stück"), (r"\bmind\.", "mindestens"), (r"\bmax\.", "maximal"),
    (r"\busw\.", "und so weiter"), (r"\betc\.", "et cetera"),
    (r"(\d)\s?%", r"\1 Prozent"), (r"(\d)\s?€", r"\1 Euro"), (r"€\s?(\d)", r"\1 Euro"),
    (r"(\d)\s?m²", r"\1 Quadratmeter"), (r"\bqm\b", "Quadratmeter"),
]


def fuer_stimme(text: str, max_saetze: int = 0) -> str:
    """Macht aus Chat-Text sprechbaren Text: Markdown raus, Abkuerzungen ausgeschrieben,
    Listenpunkte zu Saetzen. `max_saetze > 0` kuerzt zusaetzlich hart."""
    t = (text or "").strip()
    if not t:
        return ""
    t = re.sub(r"```.*?```", " ", t, flags=re.S)                  # Codebloecke
    t = re.sub(r"`([^`]*)`", r"\1", t)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)              # Links/Bilder
    t = re.sub(r"^\s{0,3}#{1,6}\s*", "", t, flags=re.M)           # Ueberschriften
    t = re.sub(r"(\*\*|__|\*|_)", "", t)                          # Fett/Kursiv
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.M)                # Bulletpoints
    t = re.sub(r"^\s*\d+[.)]\s+", "", t, flags=re.M)              # nummerierte Listen
    for muster, ersatz in _ABKUERZUNGEN:
        t = re.sub(muster, ersatz, t)
    t = t.replace("&", " und ")
    t = re.sub(r"[|>#~^]", " ", t)
    t = re.sub(r"\n{2,}", ". ", t)                                # Absatz -> Satzende
    t = re.sub(r"\n", ". ", t)
    t = re.sub(r"\.\s*\.(\s*\.)*", ". ", t)                       # doppelte Punkte
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    if max_saetze > 0:
        saetze = re.findall(r"[^.!?]+[.!?]?", t)
        t = "".join(saetze[:max_saetze]).strip()
    return t


# Google Cloud Text-to-Speech, EU-Endpunkt (DSGVO, [d-211]); Auth ueber dieselben
# Service-Account-Credentials wie Vertex (ki_client.gcp_credentials).
TTS_ENDPOINT = os.getenv("TTS_ENDPOINT", "https://eu-texttospeech.googleapis.com/v1/text:synthesize")


def sprich(text: str, stimme: Optional[Stimme] = None, *, timeout: float = 30.0) -> bytes:
    """Text -> MP3-Bytes (Google Cloud TTS). Wirft bei HTTP-Fehler (analog ki_client).

    Hinweis: Standardstimmen klingen nach Katalog, nicht nach dir. Fuer die echte eigene
    Stimme braucht es eine geklonte Stimme (Google 'Instant Custom Voice' o. ae.) — dann
    nur `Stimme.stimme_id` auf die geklonte Stimme setzen, der Rest bleibt gleich.
    """
    inhalt = fuer_stimme(text)
    if not inhalt:
        return b""

    import base64
    import httpx

    s = stimme or Stimme()
    creds = ki_client.gcp_credentials()
    payload = {
        "input": {"text": inhalt},
        "voice": {"languageCode": s.sprache, "name": s.stimme_id},
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": s.tempo, "pitch": s.tonhoehe},
    }
    with httpx.Client(timeout=timeout) as c:
        r = c.post(TTS_ENDPOINT,
                   headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"},
                   json=payload)
    if r.status_code != 200:
        raise RuntimeError(f"TTS HTTP {r.status_code}: {r.text[:300]}")
    return base64.b64decode(r.json()["audioContent"])


# ── CLI: python -m zb_shared.replikat ────────────────────────────────────────
def _cli(argv: Optional[list[str]] = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(prog="zb_shared.replikat", description="KI-Replikate verwalten und sprechen")
    sub = ap.add_subparsers(dest="befehl", required=True)

    sub.add_parser("personas", help="vorhandene Profile auflisten")

    p_neu = sub.add_parser("neu", help="Profil aus Vorlage anlegen")
    p_neu.add_argument("--name", required=True, help="Name des Originals")
    p_neu.add_argument("--bereich", default="arbeit", choices=sorted(VORLAGEN), help="Lebensbereich")
    p_neu.add_argument("--rolle", default="", help='z.B. "Geschaeftsfuehrer Zitzelsberger"')
    p_neu.add_argument("--id", default="", help="Profil-ID (Default: name-bereich)")

    p_lern = sub.add_parser("lernen", help="Stilprofil aus eigenen Texten lernen")
    p_lern.add_argument("--persona", required=True)
    p_lern.add_argument("--texte", required=True, help="Ordner mit eigenen Texten (.txt/.md)")

    p_chat = sub.add_parser("chat", help="Dialog im Terminal")
    p_chat.add_argument("--persona", required=True)
    p_chat.add_argument("--stimme", action="store_true", help="Sprechkanal (kurze Antworten)")

    p_spr = sub.add_parser("sprich", help="Text als MP3 ausgeben")
    p_spr.add_argument("--persona", required=True)
    p_spr.add_argument("--text", required=True)
    p_spr.add_argument("--out", default="replikat.mp3")

    a = ap.parse_args(argv)

    if a.befehl == "personas":
        ids = liste_personas()
        print("\n".join(ids) if ids else f"(keine Profile in {profil_verzeichnis()})")
        return 0

    if a.befehl == "neu":
        p = vorlage(a.bereich, a.name, persona_id=a.id, rolle=a.rolle)
        pfad = speichere_persona(p)
        print(f"Profil angelegt: {pfad}\nNaechster Schritt: lernen --persona {p.id} --texte <ordner>")
        return 0

    if a.befehl == "lernen":
        p = lade_persona(a.persona)
        texte = texte_aus_verzeichnis(a.texte)
        if not texte:
            print("Keine Texte gefunden (.txt/.md).")
            return 1
        p.stil = stilprofil_aus_texten(texte, p.name)
        pfad = speichere_persona(p)
        print(f"Stilprofil aus {len(texte)} Texten gelernt -> {pfad}")
        return 0

    if a.befehl == "chat":
        r = Replikat(lade_persona(a.persona), kanal="stimme" if a.stimme else "text")
        print(f"Replikat '{r.persona.id}' bereit ({r.modell}). Beenden mit Strg-D.\n")
        while True:
            try:
                frage = input("> ").strip()
            except EOFError:
                print()
                return 0
            if not frage:
                continue
            print(r.antwort_sync(frage) or "(keine Antwort — KI-Client fehlt)", "\n")

    if a.befehl == "sprich":
        p = lade_persona(a.persona)
        Path(a.out).write_bytes(sprich(a.text, p.stimme))
        print(f"MP3 geschrieben: {a.out}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(_cli())
