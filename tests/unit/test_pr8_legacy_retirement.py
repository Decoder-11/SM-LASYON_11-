"""PR 8: encoding sentinel and legacy tool retirement stubs."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_simulation_11_package_configures_utf8_streams(monkeypatch: pytest.MonkeyPatch):
    recorded: list[tuple[str, str, str]] = []

    class FakeStream:
        def reconfigure(self, *, encoding: str, errors: str) -> None:
            recorded.append(("stream", encoding, errors))

    fake_stdout = FakeStream()
    fake_stderr = FakeStream()
    monkeypatch.setattr(sys, "stdout", fake_stdout)
    monkeypatch.setattr(sys, "stderr", fake_stderr)

    import simulation_11

    importlib.reload(simulation_11)

    assert ("stream", "utf-8", "replace") in recorded
    assert len(recorded) == 2


@pytest.mark.parametrize(
    "module_name",
    ["apply_patch", "fix_issues", "mega_merger"],
)
def test_legacy_tool_stubs_raise_import_error(module_name: str):
    if module_name in sys.modules:
        del sys.modules[module_name]
    with pytest.raises(ImportError, match="legacy_tools"):
        importlib.import_module(module_name)


def test_levhi_mahfuz_has_single_main_block():
    source = (ROOT / "levhi_mahfuz.py").read_text(encoding="utf-8")
    assert source.count('if __name__ == "__main__":') == 1
    assert "def _main() -> None:" in source


def test_legacy_tools_readme_lists_minimum_stubs():
    readme = (ROOT / "archive" / "legacy_tools" / "README.md").read_text(encoding="utf-8")
    for name in ("apply_patch.py", "fix_issues.py", "mega_merger.py"):
        assert name in readme