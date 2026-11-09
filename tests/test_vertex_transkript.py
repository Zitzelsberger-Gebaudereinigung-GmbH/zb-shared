# -*- coding: utf-8 -*-
"""DSB-Auflage M16: Spracheingabe nur in EU-Regionen, sonst sichtbarer Fehler."""
import asyncio
import importlib

import pytest

import zb_shared.vertex_transkript as vt


def _neu_laden(monkeypatch, wert):
    if wert is None:
        monkeypatch.delenv("VERTEX_GEMINI_LOCATIONS", raising=False)
    else:
        monkeypatch.setenv("VERTEX_GEMINI_LOCATIONS", wert)
    return importlib.reload(vt)


@pytest.fixture(autouse=True)
def _zuruecksetzen(monkeypatch):
    yield
    monkeypatch.delenv("VERTEX_GEMINI_LOCATIONS", raising=False)
    importlib.reload(vt)


def test_vorgabe_ist_eu(monkeypatch):
    m = _neu_laden(monkeypatch, None)
    assert m.GEMINI_LOCATIONS == ["europe-west1", "europe-west4"]
    assert m.VERWORFENE_REGIONEN == []


@pytest.mark.parametrize("region", ["europe-west2", "europe-west6", "global",
                                    "us-central1", "europe-west99", "asia-east1"])
def test_nicht_eu_wird_verworfen(monkeypatch, region):
    m = _neu_laden(monkeypatch, f"europe-west3,{region}")
    assert m.GEMINI_LOCATIONS == ["europe-west3"]
    assert m.VERWORFENE_REGIONEN == [region]


def test_alle_eu_regionen_bleiben(monkeypatch):
    liste = ",".join(sorted(vt.EU_REGIONEN))
    m = _neu_laden(monkeypatch, liste)
    assert sorted(m.GEMINI_LOCATIONS) == sorted(vt.EU_REGIONEN)


def test_keine_eu_region_liefert_klaren_fehler(monkeypatch):
    m = _neu_laden(monkeypatch, "europe-west2,global,us-central1")
    assert m.GEMINI_LOCATIONS == []
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "{}")
    assert m.verfuegbar() is False

    def _darf_nicht(*a, **k):
        raise AssertionError("ohne EU-Region darf nichts nach aussen gehen")
    monkeypatch.setattr(m, "_get_credentials", _darf_nicht)

    with pytest.raises(m.SpracheingabeNichtVerfuegbar,
                       match="Spracheingabe nicht verfügbar"):
        asyncio.run(m.transcribe_audio_async("AAAA"))
    # Bestehende Aufrufer fangen RuntimeError — muss weiter greifen.
    assert issubclass(m.SpracheingabeNichtVerfuegbar, RuntimeError)
