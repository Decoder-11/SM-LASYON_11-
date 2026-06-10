# Legacy Tools Archive (PR 8)

One-off merge, patch, splitter, and injection scripts retired during the
simulation-11 phased refactor. Root copies were replaced with stubs that raise
`ImportError` pointing here.

Use `uv run simulation-11` for orchestration. Edit `simulation_11/` for
package changes.

## Archived tools

| File | Category |
|------|----------|
| `SENTEZ_SES.py.py` | generated junk |
| `add_checkup.py` | checkup injectors |
| `add_error_handler.py` | dashboard patches |
| `add_extra_s19.py` | sentez-19 injectors |
| `add_middleware.py` | dashboard patches |
| `add_s19_call.py` | sentez-19 injectors |
| `append_code.py` | code appenders |
| `append_docs.py` | code appenders |
| `append_scales.py` | code appenders |
| `append_synthesis.py` | code appenders |
| `apply_patch.py` | patch injectors |
| `apply_patch2.py` | patch injectors |
| `block_aligner.py` | extraction |
| `collapser.py` | extraction |
| `elif_splitter.py` | splitters |
| `extract_blocks.py` | extraction |
| `fix_and_append.py` | one-off fixes |
| `fix_colab_ctrl_c.py` | colab workarounds |
| `fix_colab_werkzeug.py` | colab workarounds |
| `fix_dashboard_syntax.py` | one-off fixes |
| `fix_encoding.py` | one-off fixes |
| `fix_imports.py` | one-off fixes |
| `fix_issues.py` | dashboard patches |
| `fix_issues2.py` | dashboard patches |
| `fix_lmc.py` | one-off fixes |
| `fix_missing_file.py` | one-off fixes |
| `fix_monte.py` | one-off fixes |
| `fix_rapor_append.py` | one-off fixes |
| `fix_top.py` | one-off fixes |
| `force_synthesize.py` | merger tools |
| `gemini-code-1781040785404.py` | generated junk |
| `inject.py` | code appenders |
| `inject_middleware_correctly.py` | dashboard patches |
| `inject_s19.py` | sentez-19 injectors |
| `insert_project_files.py` | extraction |
| `master_splitter.py` | splitters |
| `master_splitter_v2.py` | splitters |
| `master_stabilizer.py` | stabilizers |
| `master_stabilizer_v2.py` | stabilizers |
| `master_stabilizer_v3.py` | stabilizers |
| `mega_merger.py` | merger tools |
| `metin-1.py` | generated junk |
| `simulasyon_11_MEGA.py` | kernel backups |
| `simulasyon_11_backup_march2.py` | kernel backups |
| `simulasyon_11_temp.py` | kernel backups |
| `simule3_galaktik_tavaf.py` | superseded simule3 |
| `simule3_manifesto_motoru.py` | superseded simule3 |
| `simule3_manifesto_motoru_V2.py` | superseded simule3 |
| `simule3_manifesto_motoru_V3.py` | superseded simule3 |
| `simule3_nihai_uretim.py` | superseded simule3 |
| `super_joiner.py` | merger tools |
| `synthesize_kernel.py` | merger tools |
| `synthesize_mega_kernel.py` | merger tools |
| `triple_splitter.py` | splitters |
| `undo_oversplit.py` | splitters |
| `update_checkup_deep.py` | injection scripts |
| `update_dashboard.py` | injection scripts |
| `update_main.py` | injection scripts |
| `update_reporting.py` | injection scripts |
| `upgrade_checkup.py` | checkup injectors |
| `verify2.py` | ad-hoc verify |

**Total:** 61 tools

Scripts only present in the main repo history were copied from the
canonical workspace when missing from this worktree.
