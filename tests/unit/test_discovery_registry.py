"""Unit tests for discovery plugin registry and CLI flag (PR 7)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from simulation_11 import cli
from simulation_11.discovery import registry


def test_discovery_choices():
    assert registry.DISCOVERY_CHOICES == ("none", "45", "50", "all")


def test_default_discovery_is_none():
    parser = cli._build_parser()
    args = parser.parse_args([])
    assert args.discoveries == "none"


def test_discoveries_cli_choices():
    parser = cli._build_parser()
    for choice in ("none", "45", "50", "all"):
        args = parser.parse_args(["--discoveries", choice])
        assert args.discoveries == choice


def test_help_includes_discoveries_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--help"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "--discoveries" in captured.out


def test_list_plugins_returns_registered_plugins():
    plugins = registry.list_plugins()
    assert [plugin.plugin_id for plugin in plugins] == ["45", "50"]
    assert plugins[0].entrypoint == "run_45_discoveries_synthesis"
    assert plugins[1].entrypoint == "print_mega_sentez_raporu"


def test_resolve_plugins_none_returns_empty():
    assert registry.resolve_plugins("none") == []


def test_resolve_plugins_single_ids():
    plugin_45 = registry.resolve_plugins("45")
    assert len(plugin_45) == 1
    assert plugin_45[0].plugin_id == "45"

    plugin_50 = registry.resolve_plugins("50")
    assert len(plugin_50) == 1
    assert plugin_50[0].plugin_id == "50"


def test_resolve_plugins_all_returns_both():
    plugins = registry.resolve_plugins("all")
    assert [plugin.plugin_id for plugin in plugins] == ["45", "50"]


def test_resolve_plugins_invalid_raises():
    with pytest.raises(ValueError, match="Unknown discovery selection"):
        registry.resolve_plugins("99")


def test_run_plugin_45_returns_messages_and_data():
    messages, data = registry.run_plugin("45")
    assert len(messages) == 4
    assert len(data) == len(registry.DEFAULT_45_VERI_DIZISI)
    assert all(isinstance(value, float) for value in data)


def test_run_discoveries_all_returns_two_results():
    results = registry.run_discoveries("all")
    assert len(results) == 2

    messages, data = results[0]
    assert len(messages) == 4
    assert len(data) == len(registry.DEFAULT_45_VERI_DIZISI)

    mega_results = results[1]
    assert isinstance(mega_results, dict)
    assert "hudhud" in mega_results
    assert "R11" in mega_results


def test_run_plugin_50_prints_report(capsys):
    result = registry.run_plugin("50")
    captured = capsys.readouterr()
    assert "MEGA SENTEZ" in captured.out
    assert isinstance(result, dict)
    assert "halley_celali" in result


@patch.object(cli, "_run_discovery_plugins")
@patch.object(cli, "_run_v133")
@patch.object(cli, "_configure_pandas")
def test_cli_runs_discoveries_after_orchestrator(mock_pd, mock_v133, mock_run_disc):
    assert cli.main(["--orchestrator", "v133", "--discoveries", "45"]) == 0
    mock_v133.assert_called_once()
    mock_run_disc.assert_called_once_with("45")


@patch.object(cli, "_run_discovery_plugins")
@patch.object(cli, "_run_v133")
@patch.object(cli, "_configure_pandas")
def test_cli_default_skips_discoveries(mock_pd, mock_v133, mock_run_disc):
    assert cli.main(["--orchestrator", "v133"]) == 0
    mock_v133.assert_called_once()
    mock_run_disc.assert_called_once_with("none")


@patch.object(cli, "_run_discovery_plugins")
@patch.object(cli, "_run_v175")
@patch.object(cli, "_configure_pandas")
def test_cli_discoveries_all_invokes_registry(mock_pd, mock_v175, mock_run_disc):
    assert cli.main(["--orchestrator", "v175", "--discoveries", "all"]) == 0
    mock_v175.assert_called_once()
    mock_run_disc.assert_called_once_with("all")