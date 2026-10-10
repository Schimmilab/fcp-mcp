"""Lokaler Zweig (Sicherheitspruefung 10.10.2026): noise_threshold darf keinen ffmpeg-Filtergraph einschleusen."""
import pytest

from fcp_mcp import _server_runtime as rt


@pytest.mark.parametrize("wert", ["-30dB,ametadata=mode=print:file=/tmp/x", "-30dB:d=1", "0.01", "x"])
def test_muss_rot_injektion_wird_abgelehnt(wert, tmp_path):
    with pytest.raises(ValueError):
        rt.media_detect_silence.__wrapped__(str(tmp_path / "a.wav"), noise_threshold=wert) if hasattr(rt.media_detect_silence, "__wrapped__") else rt.media_detect_silence(str(tmp_path / "a.wav"), noise_threshold=wert)


@pytest.mark.parametrize("wert", ["-30dB", "-40.5dB", "0dB"])
def test_gueltige_werte_passieren_die_pruefung(wert):
    import re
    assert re.fullmatch(r"-?\d+(\.\d+)?dB", wert)


def test_bundle_id_umgebungsvariable_hat_vorrang(monkeypatch):
    from fcp_mcp.automation import osascript as a
    monkeypatch.setenv("FCP_MCP_FCP_BUNDLE_ID", "com.example.Test")
    assert a.fcp_bundle_id() == "com.example.Test"
    assert "com.example.Test" in a.OsaProgram("AppleScript", 'tell application id "__FCP_BUNDLE__"').source


def test_muss_rot_kein_platzhalter_bleibt_stehen():
    from fcp_mcp.automation import osascript as a
    progs = [v for v in vars(a).values() if isinstance(v, a.OsaProgram)]
    assert progs and all("__FCP_BUNDLE__" not in p.source and '"Final Cut Pro"' not in p.source for p in progs)
