"""simulation_11 package — CLI and extracted simulation modules (PR 3)."""

from __future__ import annotations

import sys

__version__ = "2.0.0"

# Normalize console encoding on Windows and legacy terminals (PR 8).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
