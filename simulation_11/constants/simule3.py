"""Key Simule3 constants extracted from monolith (PR 3)."""

from __future__ import annotations


class Simule3Constants:
    """Canonical subset used by CLI, parity, and orchestrators."""

    BASE_SYSTEM = 11
    R11 = 11111111111
    IDEAL_EARTH_RADIUS = 6666
    YEAR_SIM = 363.0
    YEAR_REAL = 365.2422
    HALLEY_IDEAL = 74.0
    FLOOD_YEAR = -9048
    CELALI_CYCLE = 33
    RAMADAN_SHIFT = 11
    SIM_DURATION = 11111
    C_IDEAL = 333333.333
    C_REAL = 299792.458


KEY_CONSTANTS = {
    "BASE_SYSTEM": Simule3Constants.BASE_SYSTEM,
    "R11": Simule3Constants.R11,
    "IDEAL_EARTH_RADIUS": Simule3Constants.IDEAL_EARTH_RADIUS,
}