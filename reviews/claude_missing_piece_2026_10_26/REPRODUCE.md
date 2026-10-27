# Reproduce the bounded diagnostics

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula` with the existing
Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4 and mpmath 1.3.0 environment.
No installation or download is required.

The saved completed runs are `run_stress_checked` and `run_df`. Their commands,
input hashes, versions and scope are in their v2 manifests. To independently
repeat without overwriting those runs:

```bash
mkdir -p /tmp/claude_review_recheck_20261026
python3 reviews/claude_missing_piece_2026_10_26/check_stress.py /tmp/claude_review_recheck_20261026/stress.json
python3 reviews/claude_missing_piece_2026_10_26/check_burkert_df.py /tmp/claude_review_recheck_20261026/df.json
```

These two direct commands do not generate new provenance manifests. Use the
installed mathbox computation-audit runner and the supplied contracts if a new
bounded record is needed; use a fresh output directory. Both scripts accept
their result path as the first argument.

Validate the saved manifests:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/claude_missing_piece_2026_10_26/run_stress_checked/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/claude_missing_piece_2026_10_26/run_df/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

`independent_lensing/` retains the other reviewer's script, results and original
manifest unchanged. That manifest uses original absolute-location paths
relative to `/`, including `/tmp/x53_lensing_audit_20261026`. The retained copies
preserve the original bytes; they do not rewrite its provenance. Its script
reconstructs scoring from the repository's released covariance and saved model
predictions, rather than regenerating the halo profiles. Run it only while the
pinned repository inputs remain available; it writes to its original `/tmp`
directory. Its original run had no hard resource limit, used one thread, and
completed in less than one second.

`run_stress/` is the preserved failed first run. It failed on JSON serialization
of a NumPy boolean, before producing its result file. `source_at_failure.py`
retains the exact original source. Do not treat that run as positive evidence.
The current script's boolean conversion differs, so validating its old input
hash against the current script is expected to fail.
