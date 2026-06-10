"""CLI entry point for simulation-11 (PR 2)."""

from __future__ import annotations

import argparse
import os
import sys
import traceback
from typing import Callable

from simulation_11.discovery.registry import (
    DEFAULT_DISCOVERY,
    DISCOVERY_CHOICES,
    run_discoveries,
)

ORCHESTRATOR_CHOICES = ("all", "v133", "v175", "auto")
DEFAULT_ORCHESTRATOR = "all"


def _import_orchestrators():
    """Lazy-import orchestrators from simulation_11 package (PR 3)."""
    from simulation_11._optional_deps import ensure_optional_deps

    ensure_optional_deps()
    from simulation_11.orchestrator.v133 import Simule3_Lab_V133, Simulation_AutoPilot
    from simulation_11.orchestrator.v175 import Simule3_Lab_V175

    return Simule3_Lab_V133, Simule3_Lab_V175, Simulation_AutoPilot


def _ensure_requests_mock() -> None:
    """Handle missing or broken requests gracefully (V175 legacy behavior)."""
    from simulation_11._optional_deps import ensure_requests_mock

    ensure_requests_mock()


def _configure_pandas() -> None:
    import pandas as pd

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    pd.set_option("display.colheader_justify", "left")


def _run_v133() -> None:
    Simule3_Lab_V133, _, _ = _import_orchestrators()
    lab = Simule3_Lab_V133()
    lab.run_all()


def _run_v175() -> None:
    _, Simule3_Lab_V175, _ = _import_orchestrators()
    _ensure_requests_mock()
    lab = Simule3_Lab_V175()
    lab.run_all()


def _run_auto(interval_minutes: int = 11) -> None:
    _, _, Simulation_AutoPilot = _import_orchestrators()
    Simulation_AutoPilot(interval_minutes=interval_minutes)


def _run_discovery_plugins(selection: str) -> None:
    """Run optional discovery synthesis plugins (PR 7)."""
    if selection == "none":
        return
    run_discoveries(selection)


def _legacy_dual_run() -> int:
    """Sequential V133 then V175 — restores pre-PR-2 dual __main__ behavior."""
    _configure_pandas()
    try:
        _run_v133()
        _run_v175()
    except Exception as exc:
        print(f"\n[CRITICAL ERROR] legacy_dual shim crash: {exc}")
        traceback.print_exc()
        return 1
    return 0


def _resolve_runner(orchestrator: str) -> Callable[[], None]:
    if orchestrator == "v133":
        return _run_v133
    if orchestrator == "v175":
        return _run_v175
    if orchestrator == "auto":
        return _run_auto
    if orchestrator == "all":

        def _run_all() -> None:
            _run_v133()
            _run_v175()

        return _run_all
    raise ValueError(f"Unknown orchestrator: {orchestrator}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="simulation-11",
        description=(
            "11-Dimensional Universe Simulation System. "
            "Default --orchestrator all runs V133 then V175 (v2.0.x legacy dual-run)."
        ),
        allow_abbrev=False,
    )
    parser.add_argument(
        "--orchestrator",
        choices=ORCHESTRATOR_CHOICES,
        default=DEFAULT_ORCHESTRATOR,
        dest="orchestrator",
        help="Orchestrator selection (default: all = V133 then V175)",
    )
    parser.add_argument(
        "--auto",
        action="store_const",
        const="auto",
        dest="orchestrator",
        help="Run autopilot scheduler (legacy flag; same as --orchestrator auto)",
    )
    parser.add_argument(
        "--auto-interval",
        type=int,
        default=11,
        metavar="MINUTES",
        help="Autopilot interval when --orchestrator auto or --auto (default: 11)",
    )
    parser.add_argument(
        "--discoveries",
        choices=DISCOVERY_CHOICES,
        default=DEFAULT_DISCOVERY,
        dest="discoveries",
        help="Discovery synthesis plugins to run after orchestrator (default: none)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Entry point.

    BREAKING CHANGE NOTE (v2.0.x):
      Default --orchestrator all matches legacy dual-run (V133 then V175).
      v2.1+ will default to v175 only — see KD11 in design doc.
    """
    if os.environ.get("SIMULATION_SHIM") == "legacy_dual":
        return _legacy_dual_run()

    parser = _build_parser()
    args = parser.parse_args(argv)

    _configure_pandas()

    try:
        if args.orchestrator == "auto":
            _run_auto(interval_minutes=args.auto_interval)
        else:
            runner = _resolve_runner(args.orchestrator)
            runner()
        _run_discovery_plugins(args.discoveries)
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
        return 130
    except Exception as exc:
        print(f"\n[CRITICAL ERROR] Simulation crash: {exc}")
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())