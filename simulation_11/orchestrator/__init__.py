"""Simulation orchestrators (PR 3)."""

from __future__ import annotations

from typing import Any

__all__ = ["Simule3_Lab_V133", "Simule3_Lab_V175", "Simulation_AutoPilot"]


def __getattr__(name: str) -> Any:
    if name in ("Simule3_Lab_V133", "Simulation_AutoPilot"):
        from simulation_11.orchestrator.v133 import Simule3_Lab_V133, Simulation_AutoPilot

        return {
            "Simule3_Lab_V133": Simule3_Lab_V133,
            "Simulation_AutoPilot": Simulation_AutoPilot,
        }[name]
    if name == "Simule3_Lab_V175":
        from simulation_11.orchestrator.v175 import Simule3_Lab_V175

        return Simule3_Lab_V175
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")