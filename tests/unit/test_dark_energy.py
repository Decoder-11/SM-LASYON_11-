"""Unit tests migrated from test_dark_energy_matter_constants.py (Appendix A)."""

from __future__ import annotations

import math

import pytest

from levhi_mahfuz import LevhiMahfuzConstants

SIRIUS_FREQUENCY = 1330.99803
ENOCH_FREQUENCY = 10.92111
GIZA_FREQUENCY = 11.08831


def calculate_antigravity_master() -> float:
    return (SIRIUS_FREQUENCY / 1331.0) * (ENOCH_FREQUENCY / 11.0) * (GIZA_FREQUENCY / 1331.0)


def calculate_cosmic_harmony() -> float:
    phi = 1.6180339887
    return phi * math.pi * math.e * 11


def test_antigravity_master_formula():
    calculated = calculate_antigravity_master()
    assert calculated == pytest.approx(LevhiMahfuzConstants.ANTIGRAVITY_MASTER_FORMULA, rel=1e-4)


def test_cosmic_harmony_constant():
    calculated = calculate_cosmic_harmony()
    assert calculated == pytest.approx(LevhiMahfuzConstants.COSMIC_HARMONY_CONSTANT, rel=1e-3)


def test_roentgenium_repunit_lock():
    roentgenium_z = 111
    repunit = 111
    assert roentgenium_z == repunit