"""Re-exports for monolith symbols not yet extracted (PR 3 strangler bridge)."""

from __future__ import annotations

import importlib
from typing import Any

_MODULE = None


def _mono():
    global _MODULE
    if _MODULE is None:
        _MODULE = importlib.import_module("simulasyon_11")
    return _MODULE


def __getattr__(name: str) -> Any:
    mono = _mono()
    if name == "Simule3_Lab":
        return getattr(mono, "Simule3_Lab_V103", mono.Simule3_Lab)
    return getattr(mono, name)