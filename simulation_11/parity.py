"""Normalized parity capture/compare CLI (PR 2)."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from unittest.mock import patch

FIXTURES_PATH = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "reference_outputs.json"

EXCLUDED_SECTIONS = [
    "timestamps",
    "random_ids",
    "gemini_responses",
    "progress_bars",
]

BASELINE_ALIASES = {
    "legacy_dual": "all",
    "v133_only": "v133",
    "v175_only": "v175",
}


def _extract_key_constants() -> dict[str, Any]:
    """Read canonical constants from levhi_mahfuz (avoids monolith import in PR 2)."""
    from levhi_mahfuz import LevhiMahfuzConstants

    const = LevhiMahfuzConstants()
    return {
        "BASE_SYSTEM": const.BASE_SYSTEM,
        "R11": const.R11,
        "IDEAL_EARTH_RADIUS": const.IDEAL_EARTH_RADIUS,
    }


def _baseline_snapshot(orchestrator: str) -> dict[str, Any]:
    """Build a normalized snapshot without running full orchestrators."""
    return {
        "orchestrator": orchestrator,
        "modules_passed": None,
        "modules_total": None,
        "validation_summary": {"passed": None, "total": None},
        "key_constants": _extract_key_constants(),
        "excluded_sections": list(EXCLUDED_SECTIONS),
        "captured_at": "frozen",
    }


@contextmanager
def parity_mocks():
    """Apply deterministic mocks for parity capture/compare."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db", prefix="simulation_parity_")
    os.close(db_fd)

    env_patch = patch.dict(os.environ, {"SIMULATION_DB_PATH": db_path}, clear=False)
    random_patch = patch.object(random, "random", return_value=0.5)

    try:
        with env_patch, random_patch:
            yield {"db_path": db_path}
    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass


def _load_reference(path: Path | None = None) -> dict[str, Any]:
    fixture = path or FIXTURES_PATH
    with fixture.open(encoding="utf-8") as handle:
        return json.load(handle)


def _save_reference(data: dict[str, Any], path: Path | None = None) -> Path:
    fixture = path or FIXTURES_PATH
    fixture.parent.mkdir(parents=True, exist_ok=True)
    with fixture.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return fixture


def _compare_values(
    expected: Any,
    actual: Any,
    path: str,
    tolerance: dict[str, Any],
    errors: list[str],
) -> None:
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected:
            child = f"{path}.{key}" if path else key
            if key not in actual:
                errors.append(f"missing field: {child}")
                continue
            _compare_values(expected[key], actual[key], child, tolerance, errors)
        return

    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if expected == actual:
            return
        if expected == 0:
            if actual != 0:
                errors.append(f"numeric mismatch at {path}: expected {expected}, got {actual}")
            return
        rel = abs(actual - expected) / abs(expected)
        limit = tolerance.get("float_relative", 0.015)
        if rel > limit:
            errors.append(
                f"numeric mismatch at {path}: expected {expected}, got {actual} "
                f"(relative error {rel:.4f} > {limit})"
            )
        return

    if expected != actual:
        errors.append(f"value mismatch at {path}: expected {expected!r}, got {actual!r}")


def compare_snapshots(
    expected: dict[str, Any],
    actual: dict[str, Any],
    tolerance: dict[str, Any] | None = None,
) -> list[str]:
    tol = tolerance or {"float_relative": 0.015, "module_count_exact": True}
    errors: list[str] = []
    _compare_values(expected, actual, "", tol, errors)
    return errors


def capture_baseline(name: str, output: Path | None = None) -> dict[str, Any]:
    orchestrator = BASELINE_ALIASES.get(name, name)
    with parity_mocks():
        snapshot = _baseline_snapshot(orchestrator)

    reference = _load_reference() if FIXTURES_PATH.exists() else {"version": 1, "baselines": {}, "tolerance": {}}
    reference.setdefault("version", 1)
    reference.setdefault("baselines", {})
    reference.setdefault(
        "tolerance",
        {"float_relative": 0.015, "module_count_exact": True},
    )
    reference["baselines"][name] = snapshot

    _save_reference(reference, output)
    return snapshot


def compare_baseline(name: str, fixture: Path | None = None) -> list[str]:
    reference = _load_reference(fixture)
    baselines = reference.get("baselines", {})
    if name not in baselines:
        return [f"baseline '{name}' not found in reference_outputs.json"]

    orchestrator = BASELINE_ALIASES.get(name, name)
    with parity_mocks():
        actual = _baseline_snapshot(orchestrator)

    return compare_snapshots(baselines[name], actual, reference.get("tolerance"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="simulation_11.parity",
        description="Capture or compare normalized parity baselines.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    capture = sub.add_parser("capture", help="Capture baseline into reference_outputs.json")
    capture.add_argument(
        "--baseline",
        required=True,
        choices=["legacy_dual", "v133_only", "v175_only", "all", "v133", "v175"],
    )
    capture.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Override output fixture path",
    )

    compare = sub.add_parser("compare", help="Compare live snapshot against fixture baseline")
    compare.add_argument(
        "--baseline",
        required=True,
        choices=["legacy_dual", "v133_only", "v175_only"],
    )
    compare.add_argument(
        "--fixture",
        type=Path,
        default=None,
        help="Override fixture path",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "capture":
        snapshot = capture_baseline(args.baseline, args.output)
        print(json.dumps(snapshot, indent=2, sort_keys=True))
        return 0

    if args.command == "compare":
        errors = compare_baseline(args.baseline, args.fixture)
        if errors:
            for err in errors:
                print(f"PARITY FAIL: {err}", file=sys.stderr)
            return 1
        print(f"PARITY OK: baseline '{args.baseline}' matches fixture.")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())