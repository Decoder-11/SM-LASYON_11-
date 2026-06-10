"""Discovery module plugin registry (PR 7)."""

from simulation_11.discovery.registry import (
    DEFAULT_DISCOVERY,
    DISCOVERY_CHOICES,
    DiscoveryPlugin,
    list_plugins,
    resolve_plugins,
    run_discoveries,
    run_plugin,
)

__all__ = [
    "DEFAULT_DISCOVERY",
    "DISCOVERY_CHOICES",
    "DiscoveryPlugin",
    "list_plugins",
    "resolve_plugins",
    "run_discoveries",
    "run_plugin",
]