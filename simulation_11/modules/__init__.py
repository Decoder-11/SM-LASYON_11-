"""Extracted simulation modules (PR 3)."""

from __future__ import annotations

from typing import Any

from simulation_11.modules.embedded import (
    CainCipherConstants,
    GeneravityEngine,
    GobeklitepeConstants,
    Modul_KarTopu_V5_Sentez_V2,
    Modul_KarTopu_V5_V3_Phase3,
    SpinalCipherConstants,
)

__all__ = [
    "CainCipherConstants",
    "GeneravityEngine",
    "GobeklitepeConstants",
    "Modul_KarTopu_V5_Sentez_V2",
    "Modul_KarTopu_V5_V3_Phase3",
    "Modul_LevhMahfuzTarama",
    "SpinalCipherConstants",
]


def __getattr__(name: str) -> Any:
    if name == "Modul_LevhMahfuzTarama":
        from simulation_11.modules.levh_scan import Modul_LevhMahfuzTarama

        return Modul_LevhMahfuzTarama
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")