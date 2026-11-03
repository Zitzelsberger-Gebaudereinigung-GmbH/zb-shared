"""v0.2.6: Claude im Betrieb (Render) nur ueber Vertex EU — Direktweg verweigert, ausser begruendete Ausnahme."""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _lade(monkeypatch, **env):
    for k in ("RENDER", "ANTHROPIC_BACKEND", "ANTHROPIC_DIREKT_AUSNAHME", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    import zb_shared.ki_client as ki
    return importlib.reload(ki)


def test_betrieb_ohne_variable_vertex(monkeypatch):
    ki = _lade(monkeypatch, RENDER="true")
    assert ki.ANTHROPIC_BACKEND == "vertex" and ki.using_vertex()
    assert ki.claude_model().endswith("@20250929")


def test_betrieb_direct_verweigert(monkeypatch):
    ki = _lade(monkeypatch, RENDER="true", ANTHROPIC_BACKEND="direct", ANTHROPIC_API_KEY="x")
    assert ki.get_anthropic_async() is None
    assert ki.get_anthropic_sync() is None


def test_betrieb_direct_mit_ausnahme(monkeypatch):
    ki = _lade(monkeypatch, RENDER="true", ANTHROPIC_BACKEND="direct", ANTHROPIC_API_KEY="x",
               ANTHROPIC_DIREKT_AUSNAHME="ai-news web_search")
    assert ki.get_anthropic_sync() is not None


def test_lokal_direct_moeglich(monkeypatch):
    ki = _lade(monkeypatch, ANTHROPIC_API_KEY="x")
    assert ki.ANTHROPIC_BACKEND == "direct"
    assert ki.get_anthropic_sync() is not None
