# Repository archives

Nested duplicate repository trees were compressed into `repo_copies/*.tar.gz` during PR 1.

- See `MANIFEST.json` for SHA256 hashes, compressed sizes, and file counts.
- `.git/`, `.idea/`, and `__pycache__/` were excluded from archives (VCS/IDE artifacts).
- Root `levhi_hafiza.db` remains canonical; duplicate DB copies were not promoted.

## SIMULASYON_11_FINAL lineage (PR 4)

- Canonical read-only reference: `synthesis/final_reference.py` (relocated from root).
- Variant archives: `synthesis/*.py.gz` (STASHED, backup_files, refactored).
- Option C patch dry-run audit: `audits/final_patch_dryrun.txt`.
- Root `SIMULASYON_11_FINAL.py` is an `ImportError` shim — use `python -m simulation_11`.