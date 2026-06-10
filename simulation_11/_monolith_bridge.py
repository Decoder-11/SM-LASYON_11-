"""Re-exports for monolith symbols not yet extracted (PR 3 strangler bridge)."""

from __future__ import annotations

import importlib
from typing import Any

_MODULE = None
_LOADING = False


def _mono():
    """Load monolith once; guard against re-entrant import during orchestrator init."""
    global _MODULE, _LOADING
    if _MODULE is not None:
        return _MODULE
    if _LOADING:
        raise RuntimeError(
            "Circular import: simulasyon_11 is still loading while bridge resolved a symbol"
        )
    _LOADING = True
    try:
        _MODULE = importlib.import_module("simulasyon_11")
        return _MODULE
    finally:
        _LOADING = False


def _snowball_synthesis15(mono: Any) -> type:
    """Adapter: canonical V133 expects Snowball_Synthesis15_CosmicUnification(const)."""
    sentez15 = mono.Sentez15_CosmicUnification

    class Snowball_Synthesis15_CosmicUnification:
        def __init__(self, const: Any):
            self.const = const
            self._impl = sentez15()
            self._impl.const = const

        def run_all(self) -> Any:
            return self._impl.run_all()

    Snowball_Synthesis15_CosmicUnification.__name__ = "Snowball_Synthesis15_CosmicUnification"
    return Snowball_Synthesis15_CosmicUnification


def get(name: str) -> Any:
    """Explicit lazy resolver for orchestrator modules."""
    mono = _mono()
    if name == "Simule3_Lab":
        return getattr(mono, "Simule3_Lab_V103", mono.Simule3_Lab)
    if name == "Snowball_Synthesis15_CosmicUnification":
        return _snowball_synthesis15(mono)
    return getattr(mono, name)


def __getattr__(name: str) -> Any:
    return get(name)