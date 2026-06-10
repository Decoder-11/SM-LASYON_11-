"""PR 3 extraction tests — bridge, duplicate removal, import smoke."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from simulation_11._monolith_bridge import get as bridge_get
from simulation_11._optional_deps import ensure_optional_deps


ROOT = Path(__file__).resolve().parent.parent.parent
MONOLITH = ROOT / "simulasyon_11.py"
IMPORT_GRAPH = ROOT / "archive" / "audits" / "import_graph.json"


def _monolith_class_names() -> set[str]:
    tree = ast.parse(MONOLITH.read_text(encoding="utf-8"), filename=str(MONOLITH))
    return {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }


def test_v133_not_defined_in_monolith_ast():
    assert "Simule3_Lab_V133" not in _monolith_class_names()


def test_bridge_resolves_simule3_lab_v103_base():
    ensure_optional_deps()
    base = bridge_get("Simule3_Lab")
    import simulasyon_11 as mono

    assert base is mono.Simule3_Lab_V103


def test_v133_imports_without_circular_error():
    ensure_optional_deps()
    from simulation_11.orchestrator.v133 import Simule3_Lab_V133

    assert Simule3_Lab_V133.__name__ == "Simule3_Lab_V133"


def test_v175_imports_without_circular_error():
    ensure_optional_deps()
    from simulation_11.orchestrator.v175 import Simule3_Lab_V175

    assert Simule3_Lab_V175.__name__ == "Simule3_Lab_V175"


def test_monolith_lazy_getattr_reexports_v133():
    ensure_optional_deps()
    import simulasyon_11 as mono
    from simulation_11.orchestrator.v133 import Simule3_Lab_V133 as pkg_v133

    assert mono.Simule3_Lab_V133 is pkg_v133


def test_import_graph_v133_not_duplicate_class():
    data = json.loads(IMPORT_GRAPH.read_text(encoding="utf-8"))
    assert "Simule3_Lab_V133" not in data.get("duplicate_class_names", [])


def test_levh_scan_exported_from_modules_package():
    from simulation_11.modules import Modul_LevhMahfuzTarama

    assert Modul_LevhMahfuzTarama.__name__ == "Modul_LevhMahfuzTarama"


def test_cli_import_orchestrators_resolves_real_symbols():
    from simulation_11 import cli
    from simulation_11.orchestrator.v133 import Simule3_Lab_V133 as V133
    from simulation_11.orchestrator.v175 import Simule3_Lab_V175 as V175

    ensure_optional_deps()
    v133, v175, autopilot = cli._import_orchestrators()
    assert v133 is V133
    assert v175 is V175
    assert callable(autopilot)