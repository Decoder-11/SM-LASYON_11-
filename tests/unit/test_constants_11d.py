"""Unit tests migrated from test_11_dimensional_constants.py (Appendix A)."""

from __future__ import annotations

import math

import pytest

from levhi_mahfuz import LevhiMahfuzConstants


@pytest.fixture
def lmc() -> LevhiMahfuzConstants:
    return LevhiMahfuzConstants()


def test_macro_cycle_equals_12442(lmc: LevhiMahfuzConstants):
    macro_cycle = abs(lmc.FLOOD_YEAR) + lmc.SIMULATION_END + 1331
    assert macro_cycle == 12442


def test_sirius_locks_to_11_cube(lmc: LevhiMahfuzConstants):
    ratio = lmc.SIRIUS_FREQUENCY_IHLAL / (11**3)
    assert ratio == pytest.approx(1.0, rel=1e-5)


def test_levhi_frequency_phi_sqrt2(lmc: LevhiMahfuzConstants):
    levhi_freq = lmc.IDEAL_EARTH_RADIUS * 1.6180339887 * math.sqrt(2)
    assert levhi_freq == pytest.approx(15253.45, rel=0.001)