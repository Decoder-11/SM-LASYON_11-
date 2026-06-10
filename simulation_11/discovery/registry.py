"""Discovery module plugin registry (PR 7)."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Callable

DISCOVERY_CHOICES = ("none", "45", "50", "all")
DEFAULT_DISCOVERY = "none"

DEFAULT_45_VERI_DIZISI = [11.0, 33.0, 111.0, 333.0, 1111.0, 3333.0, 11111.0]


@dataclass(frozen=True)
class DiscoveryPlugin:
    """Registered discovery synthesis plugin."""

    plugin_id: str
    label: str
    module: str
    entrypoint: str


_PLUGINS: dict[str, DiscoveryPlugin] = {
    "45": DiscoveryPlugin(
        plugin_id="45",
        label="45 Discovery Synthesis",
        module="simulation_11.discovery.plugins.yeni_kesif_45_modulu",
        entrypoint="run_45_discoveries_synthesis",
    ),
    "50": DiscoveryPlugin(
        plugin_id="50",
        label="50+ Mega Discovery Synthesis",
        module="simulation_11.discovery.plugins.yeni_kesif_50_mega_modulu",
        entrypoint="print_mega_sentez_raporu",
    ),
}


def list_plugins() -> list[DiscoveryPlugin]:
    """Return registered discovery plugins in stable order."""
    return [_PLUGINS[key] for key in sorted(_PLUGINS)]


def resolve_plugins(selection: str) -> list[DiscoveryPlugin]:
    """Map CLI selection to the plugins that should run."""
    if selection == "none":
        return []
    if selection == "all":
        return list_plugins()
    if selection in _PLUGINS:
        return [_PLUGINS[selection]]
    raise ValueError(
        f"Unknown discovery selection: {selection!r}. "
        f"Expected one of {DISCOVERY_CHOICES!r}."
    )


def _load_entrypoint(plugin: DiscoveryPlugin) -> Callable[..., Any]:
    module = importlib.import_module(plugin.module)
    fn = getattr(module, plugin.entrypoint, None)
    if fn is None:
        raise AttributeError(
            f"Plugin {plugin.plugin_id!r} missing entrypoint {plugin.entrypoint!r} "
            f"in {plugin.module!r}"
        )
    return fn


def run_plugin(
    plugin_id: str,
    *,
    veri_dizisi: list[float] | None = None,
) -> Any:
    """Run a single discovery plugin by id."""
    plugins = resolve_plugins(plugin_id)
    if len(plugins) != 1:
        raise ValueError(f"run_plugin expects a single plugin id, got {plugin_id!r}")

    plugin = plugins[0]
    entrypoint = _load_entrypoint(plugin)

    if plugin.plugin_id == "45":
        data = veri_dizisi if veri_dizisi is not None else DEFAULT_45_VERI_DIZISI
        return entrypoint(data)

    return entrypoint()


def run_discoveries(
    selection: str,
    *,
    veri_dizisi: list[float] | None = None,
) -> list[Any]:
    """Run all plugins resolved from a CLI discovery selection."""
    results: list[Any] = []
    for plugin in resolve_plugins(selection):
        results.append(run_plugin(plugin.plugin_id, veri_dizisi=veri_dizisi))
    return results