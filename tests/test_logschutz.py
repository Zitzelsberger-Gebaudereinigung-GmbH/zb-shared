# -*- coding: utf-8 -*-
"""v0.2.7: keine Schlüssel im Protokoll; JSON in GOOGLE_APPLICATION_CREDENTIALS wird erkannt."""
import json
import logging

from zb_shared import ki_client, logschutz

PEM = "-----BEGIN PRIVATE KEY-----\nMIIEabc123geheim\n-----END PRIVATE KEY-----\n"
SA = json.dumps({"type": "service_account", "project_id": "p", "private_key_id": "7906abc",
                 "private_key": PEM, "client_email": "x@p.iam.gserviceaccount.com"})


def test_schwaerzen_pem_und_json():
    t = logschutz.schwaerzen(f"File {SA} was not found.")
    assert "MIIEabc123geheim" not in t and "7906abc" not in t
    assert "service_account" in t and "x@p.iam" in t       # Rest bleibt lesbar
    assert logschutz.schwaerzen("Timeout nach 30s") == "Timeout nach 30s"
    assert "abcdefghijklmnop1234" not in logschutz.schwaerzen("Authorization: Bearer abcdefghijklmnop1234")


def test_filter_greift_in_jeder_protokollzeile(caplog):
    logschutz.einschalten()
    log = logging.getLogger("app.test")
    with caplog.at_level(logging.WARNING):
        log.warning("KI-Fehler: %s", FileNotFoundError(f"File {SA} was not found."))
        try:
            raise FileNotFoundError(f"File {SA} was not found.")
        except FileNotFoundError:
            log.exception("Absturz")
    text = caplog.text
    assert "MIIEabc123geheim" not in text and "7906abc" not in text
    assert logschutz.ERSATZ in text and "FileNotFoundError" in text


def test_json_in_pfadvariable_wird_umgesetzt(monkeypatch, tmp_path):
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", SA)
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", raising=False)
    assert ki_client.ensure_gcp_creds() is True
    import os
    pfad = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    assert not pfad.startswith("{") and os.path.isfile(pfad)
    assert json.load(open(pfad, encoding="utf-8"))["private_key_id"] == "7906abc"


def test_import_schaltet_schutz_ein():
    assert logschutz._aktiv is True
