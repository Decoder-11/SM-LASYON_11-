"""Unit tests migrated from test_sentez_9_lambda_correction.py (Appendix A)."""

from __future__ import annotations

import pytest

from levhi_mahfuz import KarTopuSentezConstants


@pytest.fixture
def kts() -> KarTopuSentezConstants:
    return KarTopuSentezConstants()


def test_q_over_1000_equals_lambda(kts: KarTopuSentezConstants):
    assert kts.Q_QUANTUM / 1000 == pytest.approx(kts.LAMBDA_FREQ_MHZ, abs=0.001)


def test_88_times_halley_adjusted_equals_root(kts: KarTopuSentezConstants):
    assert 88 * kts.HALLEY_DUZELTILMIS == pytest.approx(kts.Q_QUANTUM, abs=0.001)


def test_lambda_constants_match_sentez9(kts: KarTopuSentezConstants):
    assert kts.LAMBDA_FREQ_MHZ == pytest.approx(6.666, abs=0.001)
    assert kts.ESCAPE_FREQ_MHZ == pytest.approx(23.90, abs=0.01)
    assert kts.LAMBDA_GERCEK_MHZ == pytest.approx(6.666, abs=0.001)