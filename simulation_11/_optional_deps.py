"""Optional dependency stubs for CLI/orchestrator paths (PR 3 review fix)."""

from __future__ import annotations

import sys
import types


def ensure_genai_mock() -> None:
    """Stub google.generativeai when absent so monolith import succeeds."""
    if "google.generativeai" in sys.modules:
        return

    class _MockModel:
        def generate_content(self, *_args, **_kwargs):
            return types.SimpleNamespace(text="[mock]")

    genai = types.ModuleType("google.generativeai")
    genai.GenerativeModel = lambda *_a, **_k: _MockModel()
    genai.configure = lambda *_a, **_k: None

    google = sys.modules.get("google")
    if google is None:
        google = types.ModuleType("google")
        sys.modules["google"] = google
    google.generativeai = genai
    sys.modules["google.generativeai"] = genai


def ensure_requests_mock() -> None:
    """Stub requests when absent (V175 legacy behavior)."""
    if "requests" in sys.modules:
        return

    class MockResponse:
        def __init__(self):
            self.status_code = 200
            self.text = "{}"

        def json(self):
            return {}

    class MockRequests:
        def get(self, *_args, **_kwargs):
            return MockResponse()

        def post(self, *_args, **_kwargs):
            return MockResponse()

    sys.modules["requests"] = MockRequests()


def ensure_optional_deps() -> None:
    ensure_genai_mock()
    ensure_requests_mock()