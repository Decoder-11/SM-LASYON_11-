"""Unit tests migrated from test_modul_levhmahfuz.py (Appendix A)."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from simulation_11.modules.levh_scan import Modul_LevhMahfuzTarama


@pytest.fixture
def modul() -> Modul_LevhMahfuzTarama:
    return Modul_LevhMahfuzTarama()


def test_calculate_shift_date_zero_shift(modul: Modul_LevhMahfuzTarama):
    target_date = date(2023, 1, 1)
    assert modul.calculate_shift_date(target_date, 0) == target_date


def test_calculate_shift_date_positive_one_year(modul: Modul_LevhMahfuzTarama):
    target_date = date(2023, 1, 1)
    result = modul.calculate_shift_date(target_date, 1)
    expected = target_date - timedelta(days=365)
    assert result == expected


def test_calculate_shift_date_negative_one_year(modul: Modul_LevhMahfuzTarama):
    target_date = date(2023, 1, 1)
    result = modul.calculate_shift_date(target_date, -1)
    expected = target_date + timedelta(days=366)
    assert result == expected


def test_calculate_shift_date_with_datetime(modul: Modul_LevhMahfuzTarama):
    target_dt = datetime(2023, 1, 1, 12, 0, 0)
    result = modul.calculate_shift_date(target_dt, 1)
    expected = target_dt - timedelta(days=365.2422)
    assert result == expected
    assert result.time() != target_dt.time()