"""Unit tests for simulation_11 CLI and SIMULATION_SHIM rollback (PR 2)."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from simulation_11 import cli


def test_main_returns_zero_with_help(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--help"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "--orchestrator" in captured.out


def test_default_orchestrator_is_all():
    parser = cli._build_parser()
    args = parser.parse_args([])
    assert args.orchestrator == "all"


def test_default_auto_interval_is_11():
    parser = cli._build_parser()
    args = parser.parse_args([])
    assert args.auto_interval == 11


def test_orchestrator_choices():
    parser = cli._build_parser()
    for choice in ("all", "v133", "v175", "auto"):
        args = parser.parse_args(["--orchestrator", choice])
        assert args.orchestrator == choice


@patch.object(cli, "_run_v133")
@patch.object(cli, "_run_v175")
@patch.object(cli, "_configure_pandas")
def test_orchestrator_all_runs_v133_then_v175(mock_pd, mock_v175, mock_v133):
    assert cli.main(["--orchestrator", "all"]) == 0
    mock_pd.assert_called_once()
    mock_v133.assert_called_once()
    mock_v175.assert_called_once()


@patch.object(cli, "_run_v133")
@patch.object(cli, "_configure_pandas")
def test_orchestrator_v133_only(mock_pd, mock_v133):
    assert cli.main(["--orchestrator", "v133"]) == 0
    mock_v133.assert_called_once()


@patch.object(cli, "_run_v175")
@patch.object(cli, "_configure_pandas")
def test_orchestrator_v175_only(mock_pd, mock_v175):
    assert cli.main(["--orchestrator", "v175"]) == 0
    mock_v175.assert_called_once()


@patch.object(cli, "_run_auto")
@patch.object(cli, "_configure_pandas")
def test_orchestrator_auto(mock_pd, mock_auto):
    assert cli.main(["--orchestrator", "auto", "--auto-interval", "5"]) == 0
    mock_auto.assert_called_once_with(interval_minutes=5)


@patch.object(cli, "_run_auto")
@patch.object(cli, "_configure_pandas")
def test_legacy_auto_flag_routes_to_run_auto(mock_pd, mock_auto):
    assert cli.main(["--auto"]) == 0
    mock_auto.assert_called_once_with(interval_minutes=11)


@patch.object(cli, "_legacy_dual_run", return_value=0)
def test_simulation_shim_legacy_dual(mock_legacy):
    with patch.dict(os.environ, {"SIMULATION_SHIM": "legacy_dual"}, clear=False):
        assert cli.main(["--orchestrator", "v133"]) == 0
    mock_legacy.assert_called_once()


@patch.object(cli, "_run_v133")
@patch.object(cli, "_run_v175")
@patch.object(cli, "_configure_pandas")
def test_legacy_dual_run_sequence(mock_pd, mock_v175, mock_v133):
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("SIMULATION_SHIM", None)
    assert cli._legacy_dual_run() == 0
    mock_v133.assert_called_once()
    mock_v175.assert_called_once()


@patch.object(cli, "_import_orchestrators")
def test_import_orchestrators_lazy(mock_import):
    mock_import.return_value = (MagicMock(), MagicMock(), MagicMock())
    v133, v175, autopilot = cli._import_orchestrators()
    mock_import.assert_called_once()
    assert v133 is not None
    assert v175 is not None
    assert autopilot is not None