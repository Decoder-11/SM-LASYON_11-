"""Verify PR 5 conftest mocks are active."""

from __future__ import annotations

import os
import sys

import pytest
import requests


def test_sirlar_stub_available():
    import sirlar

    assert sirlar.GOOGLE_API_KEY == "pytest-stub-google-api-key"


def test_gemini_stub_available():
    import google.generativeai as genai

    model = genai.GenerativeModel("gemini-test")
    response = model.generate_content("ping")
    assert response.text == "mocked-gemini-response"


def test_requests_get_stubbed():
    response = requests.get("https://example.invalid/nasa")
    assert response.status_code == 200
    assert response.json()["source"] == "pytest"


def test_temp_db_env_points_to_isolated_file(temp_db):
    assert os.environ["SIMULATION_DB_PATH"] == str(temp_db)
    assert temp_db.exists()