"""Thin shim — delegates to dashboard_11.app (PR 6)."""

from dashboard_11.app import DB_YOLU, app, main, rapor_sun

__all__ = ["DB_YOLU", "app", "main", "rapor_sun"]

if __name__ == "__main__":
    main()