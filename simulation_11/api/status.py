"""Quiet validation status from levhi_mahfuz (PR 6)."""

from __future__ import annotations

from typing import Any

from levhi_mahfuz import LevhiMahfuzFormulas, LevhiMahfuzPatterns


def get_validation_status() -> dict[str, Any]:
    """Run Levhi-Mahfuz consistency checks without console output."""
    tests: list[dict[str, Any]] = []

    is_valid, calc, expected = LevhiMahfuzFormulas.weekly_packet_verification()
    tests.append(
        {
            "name": "weekly_packet",
            "passed": bool(is_valid),
            "detail": f"11!/66 = {calc} (expected {expected})",
        }
    )

    halley = LevhiMahfuzFormulas.halley_resonance()
    tests.append(
        {
            "name": "halley_resonance",
            "passed": halley == 814,
            "detail": f"74 × 11 = {halley}",
        }
    )

    boot = LevhiMahfuzFormulas.digital_boot_formula()
    tests.append(
        {
            "name": "digital_boot",
            "passed": boot == 1998,
            "detail": f"666 × 3 = {boot}",
        }
    )

    duration, ideal = LevhiMahfuzFormulas.simulation_duration_check()
    tests.append(
        {
            "name": "simulation_duration",
            "passed": abs(duration - ideal) < 100,
            "detail": f"Flood-Reset span {duration} ≈ {ideal}",
        }
    )

    divs = LevhiMahfuzPatterns.extract_eleven_patterns(LevhiMahfuzPatterns.ELEVEN_MULTIPLES)
    tests.append(
        {
            "name": "eleven_patterns",
            "passed": len(divs) == len(LevhiMahfuzPatterns.ELEVEN_MULTIPLES),
            "detail": f"{len(divs)}/{len(LevhiMahfuzPatterns.ELEVEN_MULTIPLES)} multiples",
        }
    )

    passed = sum(1 for test in tests if test["passed"])
    total = len(tests)
    return {
        "ok": passed == total,
        "passed": passed,
        "total": total,
        "tests": tests,
    }