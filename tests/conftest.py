"""Pytest configuration — shared fixtures and external-service mocks (PR 5)."""

from __future__ import annotations

import random
import sys
import types
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def mock_sirlar(monkeypatch: pytest.MonkeyPatch) -> types.ModuleType:
    """Inject a stub ``sirlar`` module so imports never touch real secrets."""
    sirlar = types.ModuleType("sirlar")
    sirlar.GOOGLE_API_KEY = "pytest-stub-google-api-key"
    monkeypatch.setitem(sys.modules, "sirlar", sirlar)
    return sirlar


@pytest.fixture
def mock_gemini(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock ``google.generativeai`` so no Gemini API calls are made."""
    genai = MagicMock(name="google.generativeai")
    model = MagicMock(name="GenerativeModel")
    response = MagicMock()
    response.text = "mocked-gemini-response"
    model.generate_content.return_value = response
    genai.GenerativeModel.return_value = model
    genai.configure = MagicMock()

    google_pkg = types.ModuleType("google")
    google_pkg.generativeai = genai
    monkeypatch.setitem(sys.modules, "google", google_pkg)
    monkeypatch.setitem(sys.modules, "google.generativeai", genai)
    return genai


@pytest.fixture
def mock_requests(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Stub ``requests.get`` with a canned 200 JSON response."""
    response = MagicMock(name="requests.Response")
    response.status_code = 200
    response.ok = True
    response.text = '{"status":"ok","source":"pytest"}'
    response.json.return_value = {"status": "ok", "source": "pytest"}
    response.raise_for_status = MagicMock()

    get_mock = MagicMock(name="requests.get", return_value=response)
    monkeypatch.setattr("requests.get", get_mock)
    return get_mock


@pytest.fixture
def temp_db(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Point ``SIMULATION_DB_PATH`` at an isolated sqlite file."""
    db_path = tmp_path / "levhi_test.db"
    db_path.write_bytes(b"")
    monkeypatch.setenv("SIMULATION_DB_PATH", str(db_path))
    return db_path


@pytest.fixture(autouse=True)
def _apply_test_harness_mocks(
    mock_sirlar: types.ModuleType,
    mock_gemini: MagicMock,
    mock_requests: MagicMock,
    temp_db: Path,
) -> Generator[None, None, None]:
    """Apply deterministic network/AI/DB mocks for every test."""
    with patch.object(random, "random", return_value=0.5):
        yield