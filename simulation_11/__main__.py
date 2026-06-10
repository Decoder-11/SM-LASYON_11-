"""Allow ``python -m simulation_11`` after ``uv sync``."""

from simulation_11.cli import main

if __name__ == "__main__":
    raise SystemExit(main())