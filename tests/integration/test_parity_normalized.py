"""Integration tests for normalized parity capture/compare (PR 5)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from simulation_11 import parity

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "reference_outputs.json"


@pytest.mark.parametrize("baseline", ["legacy_dual", "v133_only", "v175_only"])
def test_compare_baseline_matches_fixture(baseline: str):
    errors = parity.compare_baseline(baseline, fixture=FIXTURE)
    assert errors == []


def test_fixture_contains_all_normalized_baselines():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert set(data["baselines"]) == {"legacy_dual", "v133_only", "v175_only"}
    assert data["tolerance"]["float_relative"] == 0.015


def test_capture_and_compare_round_trip(tmp_path: Path):
    output = tmp_path / "captured.json"
    snapshot = parity.capture_baseline("v133_only", output=output)
    errors = parity.compare_baseline("v133_only", fixture=output)
    assert errors == []
    assert snapshot["orchestrator"] == "v133"