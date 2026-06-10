"""Unit tests for simulation_11.parity (PR 2)."""

from __future__ import annotations

import json

from simulation_11 import parity


def test_compare_baseline_legacy_dual():
    errors = parity.compare_baseline("legacy_dual")
    assert errors == []


def test_compare_baseline_missing(tmp_path):
    fixture = tmp_path / "empty.json"
    fixture.write_text(
        json.dumps({"version": 1, "baselines": {}, "tolerance": {}}),
        encoding="utf-8",
    )
    errors = parity.compare_baseline("legacy_dual", fixture=fixture)
    assert len(errors) == 1
    assert "not found" in errors[0]


def test_capture_baseline_writes_expected_schema(tmp_path):
    output = tmp_path / "reference_outputs.json"
    snapshot = parity.capture_baseline("v133_only", output=output)

    assert snapshot["orchestrator"] == "v133"
    assert snapshot["key_constants"]["BASE_SYSTEM"] == 11
    assert snapshot["key_constants"]["R11"] == 11111111111
    assert snapshot["key_constants"]["IDEAL_EARTH_RADIUS"] == 6666

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["version"] == 1
    assert "v133_only" in data["baselines"]
    assert data["tolerance"]["float_relative"] == 0.015


def test_compare_snapshots_within_float_tolerance():
    errors = parity.compare_snapshots(
        {"ratio": 100.0},
        {"ratio": 101.0},
        {"float_relative": 0.015},
    )
    assert errors == []


def test_compare_snapshots_outside_float_tolerance():
    errors = parity.compare_snapshots(
        {"ratio": 100.0},
        {"ratio": 102.0},
        {"float_relative": 0.015},
    )
    assert len(errors) == 1
    assert "numeric mismatch" in errors[0]


def test_baseline_alias_mapping():
    assert parity.BASELINE_ALIASES["legacy_dual"] == "all"
    assert parity.BASELINE_ALIASES["v133_only"] == "v133"
    assert parity.BASELINE_ALIASES["v175_only"] == "v175"