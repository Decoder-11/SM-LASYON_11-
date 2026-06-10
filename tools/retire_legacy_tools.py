"""One-off PR 8 helper: archive legacy root scripts and write retirement stubs."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "legacy_tools"
MAIN_REPO = Path(r"C:\Users\soldi\IdeaProjects\simülation-11")

# Appendix B: archive + stub (filename -> short category for README grouping)
LEGACY_TOOLS: dict[str, str] = {
    "apply_patch.py": "patch injectors",
    "apply_patch2.py": "patch injectors",
    "fix_issues.py": "dashboard patches",
    "fix_issues2.py": "dashboard patches",
    "fix_colab_ctrl_c.py": "colab workarounds",
    "fix_colab_werkzeug.py": "colab workarounds",
    "fix_imports.py": "one-off fixes",
    "fix_lmc.py": "one-off fixes",
    "fix_monte.py": "one-off fixes",
    "fix_encoding.py": "one-off fixes",
    "fix_top.py": "one-off fixes",
    "fix_and_append.py": "one-off fixes",
    "fix_missing_file.py": "one-off fixes",
    "fix_dashboard_syntax.py": "one-off fixes",
    "fix_rapor_append.py": "one-off fixes",
    "update_main.py": "injection scripts",
    "update_dashboard.py": "injection scripts",
    "update_reporting.py": "injection scripts",
    "update_checkup_deep.py": "injection scripts",
    "upgrade_checkup.py": "checkup injectors",
    "add_checkup.py": "checkup injectors",
    "add_middleware.py": "dashboard patches",
    "add_error_handler.py": "dashboard patches",
    "inject_middleware_correctly.py": "dashboard patches",
    "add_extra_s19.py": "sentez-19 injectors",
    "add_s19_call.py": "sentez-19 injectors",
    "inject_s19.py": "sentez-19 injectors",
    "inject.py": "code appenders",
    "append_code.py": "code appenders",
    "append_synthesis.py": "code appenders",
    "append_scales.py": "code appenders",
    "append_docs.py": "code appenders",
    "mega_merger.py": "merger tools",
    "super_joiner.py": "merger tools",
    "synthesize_mega_kernel.py": "merger tools",
    "synthesize_kernel.py": "merger tools",
    "force_synthesize.py": "merger tools",
    "triple_splitter.py": "splitters",
    "undo_oversplit.py": "splitters",
    "master_splitter.py": "splitters",
    "master_splitter_v2.py": "splitters",
    "elif_splitter.py": "splitters",
    "master_stabilizer.py": "stabilizers",
    "master_stabilizer_v2.py": "stabilizers",
    "master_stabilizer_v3.py": "stabilizers",
    "extract_blocks.py": "extraction",
    "block_aligner.py": "extraction",
    "collapser.py": "extraction",
    "insert_project_files.py": "extraction",
    "verify2.py": "ad-hoc verify",
    "simulasyon_11_MEGA.py": "kernel backups",
    "simulasyon_11_temp.py": "kernel backups",
    "simulasyon_11_backup_march2.py": "kernel backups",
    "gemini-code-1781040785404.py": "generated junk",
    "metin-1.py": "generated junk",
    "SENTEZ_SES.py.py": "generated junk",
    "simule3_manifesto_motoru.py": "superseded simule3",
    "simule3_manifesto_motoru_V2.py": "superseded simule3",
    "simule3_manifesto_motoru_V3.py": "superseded simule3",
    "simule3_galaktik_tavaf.py": "superseded simule3",
    "simule3_nihai_uretim.py": "superseded simule3",
}


def stub_text(filename: str) -> str:
    archive_rel = f"archive/legacy_tools/{filename}"
    return (
        f'"""Legacy tool retired (PR 8) — archived to {archive_rel}."""\n\n'
        "raise ImportError(\n"
        f'    "{filename} was a one-off legacy maintenance script and has been retired. "\n'
        f'    "Source preserved at {archive_rel}. "\n'
        '    "Use `uv run simulation-11` for orchestration or edit `simulation_11/` directly."\n'
        ")\n"
    )


def resolve_source(filename: str) -> Path | None:
    root_path = ROOT / filename
    if root_path.exists():
        return root_path
    main_path = MAIN_REPO / filename
    if main_path.exists():
        return main_path
    return None


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    archived: list[str] = []
    stubbed_only: list[str] = []

    for filename in sorted(LEGACY_TOOLS):
        source = resolve_source(filename)
        dest = ARCHIVE / filename
        if source is not None and not dest.exists():
            shutil.copy2(source, dest)
            archived.append(filename)
        elif dest.exists():
            archived.append(filename)
        else:
            stubbed_only.append(filename)

        (ROOT / filename).write_text(stub_text(filename), encoding="utf-8")

    readme_lines = [
        "# Legacy Tools Archive (PR 8)",
        "",
        "One-off merge, patch, splitter, and injection scripts retired during the",
        "simulation-11 phased refactor. Root copies were replaced with stubs that raise",
        "`ImportError` pointing here.",
        "",
        "Use `uv run simulation-11` for orchestration. Edit `simulation_11/` for",
        "package changes.",
        "",
        "## Archived tools",
        "",
        "| File | Category |",
        "|------|----------|",
    ]
    for filename, category in sorted(LEGACY_TOOLS.items()):
        readme_lines.append(f"| `{filename}` | {category} |")

    readme_lines.extend(
        [
            "",
            f"**Total:** {len(LEGACY_TOOLS)} tools",
            "",
            "Scripts only present in the main repo history were copied from the",
            "canonical workspace when missing from this worktree.",
        ]
    )
    (ARCHIVE / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    print(f"Archived/checked: {len(archived)}")
    print(f"Stub-only (no source found): {stubbed_only}")
    print(f"README: {ARCHIVE / 'README.md'}")


if __name__ == "__main__":
    main()