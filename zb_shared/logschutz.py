# -*- coding: utf-8 -*-
"""Protokollschutz: keine Schlüssel und Kennwörter im Render-Protokoll.

Anlass 09.11.2026: Der Inhalt eines Google-Dienstkonto-Schlüssels stand versehentlich in
GOOGLE_APPLICATION_CREDENTIALS (erwartet einen Dateipfad). google-auth meldete
„File {…private_key…} was not found“, und weil Apps Fehlertexte ungefiltert protokollieren,
stand der private Schlüssel im Render-Protokoll. Die Apps haben zusammen rund 350 solcher
Protokollstellen — deshalb hier EIN Schutz für alle:

`einschalten()` legt einen Filter vor die Erzeugung JEDER Protokollzeile (LogRecord-Factory,
greift unabhängig von Handlern und Loggern, auch für uvicorn). Er ersetzt in Meldung,
Argumenten und Fehlertext:
  * PEM-Blöcke (-----BEGIN … KEY----- … -----END … KEY-----),
  * JSON-Felder "private_key", "client_secret", "refresh_token", "password", "api_key",
  * Bearer-Tokens und sk-…-Schlüssel.
Tracebacks bleiben erhalten, nur der geheime Teil wird ersetzt.

Wird beim Import von `zb_shared.ki_client` automatisch eingeschaltet (idempotent).
"""
from __future__ import annotations

import logging
import re

ERSATZ = "[entfernt: Geheimnis]"

_MUSTER = [
    re.compile(r"-----BEGIN [A-Z ]*?(?:PRIVATE )?KEY-----.*?-----END [A-Z ]*?KEY-----", re.S),
    re.compile(r"-----BEGIN [A-Z ]*?PRIVATE KEY-----[^\"']*", re.S),          # abgeschnittener Block
    re.compile(r'("(?:private_key|private_key_id|client_secret|refresh_token|password|passwort|api_key|apikey)"\s*:\s*)"(?:[^"\\]|\\.)*"', re.I),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
]


def schwaerzen(text: str) -> str:
    """Ersetzt bekannte Geheimnis-Muster im Text. Unverdächtiger Text bleibt unverändert."""
    if not text or not isinstance(text, str):
        return text
    out = text
    for m in _MUSTER:
        if m.groups:
            out = m.sub(lambda x: x.group(1) + ('"' + ERSATZ + '"' if x.group(1).rstrip().endswith(":") else ERSATZ), out)
        else:
            out = m.sub(ERSATZ, out)
    return out


def _verdaechtig(text: str) -> bool:
    return schwaerzen(text) != text


_aktiv = False


def einschalten() -> None:
    """Schutz für alle Protokollzeilen dieses Prozesses einschalten (mehrfacher Aufruf schadet nicht)."""
    global _aktiv
    if _aktiv:
        return
    alt = logging.getLogRecordFactory()

    def fabrik(*args, **kwargs):
        rec = alt(*args, **kwargs)
        try:
            msg = rec.getMessage()
            sauber = schwaerzen(msg)
            if sauber != msg:
                rec.msg, rec.args = sauber, None
            if rec.exc_info and rec.exc_info[1] is not None and _verdaechtig(str(rec.exc_info[1])):
                typ = type(rec.exc_info[1]).__name__
                rec.msg = f"{rec.msg} [{typ}: {ERSATZ}]"
                rec.args = None
                rec.exc_info = None          # Traceback würde den Fehlertext erneut ausgeben
                rec.exc_text = None
        except Exception:  # noqa: BLE001 — Protokollieren darf nie wegen des Schutzes scheitern
            pass
        return rec

    logging.setLogRecordFactory(fabrik)
    _aktiv = True
