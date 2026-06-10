"""PR 4 — SIMULASYON_11_FINAL lineage consolidation shim."""

from __future__ import annotations

import importlib
import sys

import pytest


def test_final_shim_raises_import_error_with_archive_path():
    sys.modules.pop("SIMULASYON_11_FINAL", None)
    with pytest.raises(ImportError, match=r"archive/synthesis/final_reference\.py"):
        importlib.import_module("SIMULASYON_11_FINAL")