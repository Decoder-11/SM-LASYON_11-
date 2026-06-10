"""PR 6 — dashboard imports without the simulasyon_11 monolith."""

from __future__ import annotations

import importlib
import sys
from types import ModuleType


class _MonolithImportBlocker:
    """Prevent accidental monolith imports during dashboard bootstrap."""

    def find_module(self, name: str, path=None, target=None):  # noqa: ANN001
        if name == "simulasyon_11" or name.startswith("simulasyon_11."):
            raise ImportError(f"Blocked monolith import: {name}")
        return None


def _purge_modules(prefixes: tuple[str, ...]) -> None:
    for module_name in list(sys.modules):
        if any(module_name == prefix or module_name.startswith(f"{prefix}.") for prefix in prefixes):
            del sys.modules[module_name]


def _monolith_modules(modules: set[str]) -> set[str]:
    return {name for name in modules if name == "simulasyon_11" or name.startswith("simulasyon_11.")}


def test_dashboard_imports_without_simulasyon_11():
    blocker = _MonolithImportBlocker()
    sys.meta_path.insert(0, blocker)
    try:
        _purge_modules(("dashboard_11", "simulation_11"))
        before = set(sys.modules)

        dashboard_pkg = importlib.import_module("dashboard_11")
        app_module = importlib.import_module("dashboard_11.app")
        api_constants = importlib.import_module("simulation_11.api.constants")
        api_status = importlib.import_module("simulation_11.api.status")

        newly_loaded = set(sys.modules) - before
        assert not _monolith_modules(newly_loaded)

        assert dashboard_pkg.app is app_module.app
        assert app_module.app.name == "dashboard_11.app"
        assert api_constants.KADIM_SABITLER
        assert api_status.get_validation_status()["total"] == 5
    finally:
        sys.meta_path.remove(blocker)


def test_dashboard_package_reexports_public_api():
    _purge_modules(("dashboard_11",))

    package = importlib.import_module("dashboard_11")

    assert package.app is not None
    assert callable(package.main)
    assert callable(package.rapor_sun)
    assert package.DB_YOLU.endswith("levhi_hafiza.db")
    assert isinstance(package, ModuleType)