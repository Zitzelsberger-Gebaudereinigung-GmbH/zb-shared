"""Tests fuer zb_shared.replikat — nur netzwerkfreie Teile (Datenmodell, Prompt, Stimme).

Ausfuehren:  pip install pytest && pytest -q
Die KI-Aufrufe (antwort/stilprofil_aus_texten) werden mit einem Fake-Client getestet,
es geht KEIN Request raus.
"""
from __future__ import annotations

import json

import pytest

from zb_shared import replikat as rp


# ── Fake-Client (Anthropic-Message-Form: .content[i].text) ───────────────────
class _Block:
    def __init__(self, text): self.text = text


class _Antwort:
    def __init__(self, text): self.content = [_Block(text)]


class _Messages:
    def __init__(self, text, aufrufe): self._text, self.aufrufe = text, aufrufe

    def create(self, **kw):
        self.aufrufe.append(kw)
        return _Antwort(self._text)


class FakeClient:
    def __init__(self, text="Passt, mach ich."):
        self.aufrufe: list[dict] = []
        self.messages = _Messages(text, self.aufrufe)


# ── Datenmodell / Persistenz ─────────────────────────────────────────────────
def test_vorlage_je_lebensbereich():
    for bereich in rp.VORLAGEN:
        p = rp.vorlage(bereich, "Oliver Strobel")
        assert p.lebensbereich == bereich
        assert p.id == f"oliver-strobel-{bereich}"
        assert "Oliver Strobel" in p.auftrag
        assert p.freigabe_pflichtig, "jede Vorlage braucht Freigabe-Themen"


def test_vorlage_unbekannter_bereich():
    with pytest.raises(ValueError):
        rp.vorlage("raumschiff", "Oliver")


def test_persona_roundtrip(tmp_path):
    p = rp.vorlage("arbeit", "Oliver Strobel", rolle="Geschaeftsfuehrer")
    p.stil = rp.Stilprofil(anrede="du", humor="trocken", wortwahl=["passt", "sauber"],
                           o_ton=["Das kriegen wir hin."])
    p.stimme = rp.Stimme(stimme_id="de-DE-Wavenet-D", tempo=1.1)

    pfad = rp.speichere_persona(p, tmp_path)
    assert pfad.exists()
    assert rp.liste_personas(tmp_path) == [p.id]

    geladen = rp.lade_persona(p.id, tmp_path)
    assert geladen == p                      # Dataclass-Vergleich: alles identisch
    assert geladen.stil.wortwahl == ["passt", "sauber"]
    assert geladen.stimme.tempo == 1.1


def test_lade_persona_fehlt(tmp_path):
    with pytest.raises(FileNotFoundError):
        rp.lade_persona("gibtsnicht", tmp_path)


def test_from_dict_ignoriert_unbekannte_felder():
    p = rp.Persona.from_dict({"id": "x", "name": "Oliver", "zukunftsfeld": 42,
                              "stil": {"humor": "trocken", "quatsch": 1}})
    assert p.name == "Oliver" and p.stil.humor == "trocken"


def test_profil_verzeichnis_aus_env(monkeypatch, tmp_path):
    monkeypatch.setenv("REPLIKAT_PROFIL_DIR", str(tmp_path / "profile"))
    assert rp.profil_verzeichnis() == tmp_path / "profile"
    assert rp.profil_verzeichnis(tmp_path / "anders") == tmp_path / "anders"


# ── Systemprompt: die drei Replikat-Merkmale muessen drinstehen ──────────────
def test_system_prompt_enthaelt_abbild_und_grenzen():
    p = rp.vorlage("arbeit", "Oliver Strobel", rolle="Geschaeftsfuehrer")
    p.stil = rp.Stilprofil(humor="trocken", wortwahl=["passt"], unsicherheit=["Da muss ich passen."])
    p.weiss_nicht = ["Steuerrecht"]
    p.tabus = ["Gehälter"]
    s = rp.system_prompt(p)

    assert "Oliver Strobel" in s and "Geschaeftsfuehrer" in s
    assert "NICHT allwissend" in s                     # Abbild statt Allwissen
    assert "Steuerrecht" in s and "Da muss ich passen." in s
    assert "trocken" in s and "passt" in s             # Stil
    assert "Preise und Angebote" in s                  # Freigabepflicht aus der Vorlage
    assert "Gehälter" in s                             # Tabu
    assert "KI-Replikat" in s                          # Offenlegung
    assert "Kanal: Stimme" not in s                    # Textkanal -> keine Sprechregeln


def test_system_prompt_stimme_ergaenzt_sprechregeln():
    s = rp.system_prompt(rp.vorlage("familie", "Oliver"), kanal="stimme")
    assert "Kanal: Stimme" in s and "Markdown" in s


def test_system_prompt_ohne_offenlegung():
    p = rp.vorlage("uebersetzung", "Oliver")
    p.offenlegung = False
    assert "KI-Replikat von Oliver bist" not in rp.system_prompt(p)


def test_stilprofil_leer_liefert_leeren_block():
    assert "Humor" not in rp.Stilprofil(anrede="").als_prompt_block()


# ── Dialog (Fake-Client, kein Netz) ──────────────────────────────────────────
def test_antwort_sync_nutzt_persona_und_merkt_verlauf():
    c = FakeClient("Passt, mach ich.")
    r = rp.Replikat(rp.vorlage("arbeit", "Oliver"), client=c, modell="test-modell")

    assert r.antwort_sync("Alles klar?") == "Passt, mach ich."
    kw = c.aufrufe[0]
    assert kw["model"] == "test-modell"
    assert "Oliver" in kw["system"]
    assert kw["messages"] == [{"role": "user", "content": "Alles klar?"}]
    assert r.verlauf[-1] == {"role": "assistant", "content": "Passt, mach ich."}

    r.antwort_sync("Und weiter?")
    assert len(c.aufrufe[1]["messages"]) == 3          # Verlauf wird mitgeschickt
    r.verlauf_zuruecksetzen()
    assert r.verlauf == []


def test_verlauf_wird_gekappt_und_beginnt_mit_user():
    c = FakeClient("ok")
    r = rp.Replikat(rp.vorlage("familie", "Oliver"), client=c, max_verlauf=4)
    for i in range(5):
        r.antwort_sync(f"Frage {i}")
    assert len(r.verlauf) <= 4
    assert r.verlauf[0]["role"] == "user"


def test_wissensquelle_landet_im_prompt():
    c = FakeClient("ok")
    r = rp.Replikat(rp.vorlage("arbeit", "Oliver"), client=c,
                    wissensquelle=lambda f: "Objekt Nord: Glasreinigung 14-tägig")
    r.antwort_sync("Wie oft Glas im Objekt Nord?")
    inhalt = c.aufrufe[0]["messages"][0]["content"]
    assert "Glasreinigung 14-tägig" in inhalt and "Frage: Wie oft Glas" in inhalt


def test_wissensquelle_fehler_bricht_dialog_nicht_ab():
    def kaputt(_):
        raise RuntimeError("DB weg")
    c = FakeClient("ok")
    r = rp.Replikat(rp.vorlage("arbeit", "Oliver"), client=c, wissensquelle=kaputt)
    assert r.antwort_sync("Hallo?") == "ok"


def test_stimmkanal_kuerzt_tokens_und_glaettet_antwort():
    c = FakeClient("**Klar!**\n- Punkt eins\n- Punkt zwei")
    r = rp.Replikat(rp.vorlage("mentoring", "Oliver"), client=c, kanal="stimme")
    antwort = r.antwort_sync("Und?")
    assert "*" not in antwort and "-" not in antwort
    assert c.aufrufe[0]["max_tokens"] == rp.MAX_TOKENS_STIMME


def test_ohne_client_keine_antwort(monkeypatch):
    monkeypatch.setattr(rp.ki_client, "get_anthropic_sync", lambda: None)
    r = rp.Replikat(rp.vorlage("arbeit", "Oliver"))
    assert r.antwort_sync("Hallo?") == ""


def test_antwort_async_mit_fake_client():
    import asyncio

    class _AsyncMessages:
        def __init__(self, aufrufe): self.aufrufe = aufrufe

        async def create(self, **kw):
            self.aufrufe.append(kw)
            return _Antwort("Servus, alles im Griff.")

    class _AsyncClient:
        def __init__(self): self.aufrufe = []; self.messages = _AsyncMessages(self.aufrufe)

    c = _AsyncClient()

    async def wissen(frage):                       # async Wissensquelle
        return "Kontextwissen"

    r = rp.Replikat(rp.vorlage("arbeit", "Oliver"), client=c, wissensquelle=wissen)
    assert asyncio.run(r.antwort("Wie steht's?")) == "Servus, alles im Griff."
    assert "Kontextwissen" in c.aufrufe[0]["messages"][0]["content"]


# ── Training ─────────────────────────────────────────────────────────────────
def test_stilprofil_aus_texten_parst_json():
    daten = {"anrede": "du", "humor": "trocken", "wortwahl": ["passt"], "unbekannt": 1}
    c = FakeClient("Hier das Profil:\n```json\n" + json.dumps(daten, ensure_ascii=False) + "\n```")
    stil = rp.stilprofil_aus_texten(["Mail eins", "Mail zwei"], "Oliver", client=c)
    assert stil.anrede == "du" and stil.humor == "trocken" and stil.wortwahl == ["passt"]
    assert "Mail eins" in c.aufrufe[0]["messages"][0]["content"]


def test_json_aus_antwort_varianten():
    assert rp._json_aus_antwort('{"a": 1}') == {"a": 1}
    assert rp._json_aus_antwort('```json\n{"a": 1}\n```') == {"a": 1}
    assert rp._json_aus_antwort('Bitte:\n{"a": 1}\nFertig.') == {"a": 1}
    with pytest.raises(ValueError):
        rp._json_aus_antwort("gar kein JSON")


def test_texte_aus_verzeichnis(tmp_path):
    (tmp_path / "unter").mkdir()
    (tmp_path / "a.txt").write_text("Erster Text", encoding="utf-8")
    (tmp_path / "unter" / "b.md").write_text("Zweiter Text", encoding="utf-8")
    (tmp_path / "leer.txt").write_text("   ", encoding="utf-8")
    (tmp_path / "bild.png").write_bytes(b"\x89PNG")
    assert sorted(rp.texte_aus_verzeichnis(tmp_path)) == ["Erster Text", "Zweiter Text"]
    with pytest.raises(FileNotFoundError):
        rp.texte_aus_verzeichnis(tmp_path / "weg")


def test_stil_prompt_kuerzt_korpus():
    p = rp._stil_prompt("Oliver", ["x" * 1000], max_zeichen=100)
    assert "x" * 100 in p and "x" * 101 not in p


# ── Stimme ───────────────────────────────────────────────────────────────────
def test_fuer_stimme_entfernt_markdown_und_schreibt_abkuerzungen_aus():
    t = rp.fuer_stimme("## Überschrift\n**Wichtig:** z.B. 20 % bzw. ca. 5 € pro qm.\n"
                       "- Punkt eins\n- Punkt zwei\n\nPasst.")
    assert "#" not in t and "*" not in t
    assert "zum Beispiel" in t and "20 Prozent" in t and "beziehungsweise" in t
    assert "circa" in t and "5 Euro" in t and "Quadratmeter" in t
    assert "Punkt eins. Punkt zwei" in t


def test_fuer_stimme_entfernt_code_und_links():
    t = rp.fuer_stimme("Siehe [Handbuch](https://example.org) und `pip install x`.\n```\ncode\n```")
    assert "http" not in t and "```" not in t
    assert "Handbuch" in t and "pip install x" in t


def test_fuer_stimme_kuerzt_auf_saetze():
    t = rp.fuer_stimme("Eins. Zwei. Drei. Vier.", max_saetze=2)
    assert t == "Eins. Zwei."


def test_fuer_stimme_leer():
    assert rp.fuer_stimme("") == "" and rp.fuer_stimme(None) == ""


def test_sprich_ohne_text_ohne_netz():
    assert rp.sprich("   ") == b""            # kein Request, kein Credential noetig
