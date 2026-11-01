# Reproduction and evidence

Execute from repository root with Python3 and one numerical thread. Each
script accepts a fresh result path; use the computation-audit v2 runner for
fresh execution rather than overwriting any historical run. The exact argv,
thread/CPU/wall limits, input hashes and declared result hashes are in each
manifest.

1. `gaugino_threshold.py RESULT.json`: full finite-F scalar/vector threshold,
   ordinary messenger/SUSY/gauge/scale controls. Current record: run_003.
2. `ir_matching.py RESULT.json`: mass-basis gauge threshold/anomaly traces,
   formal scales and conditional helicity dispersion. Current: run_ir_001.
3. `nullspace.py RESULT.json`: thirteen-dimensional neutral external-space
   check. Current: run_null_001.

The imported TP03 full model and TP01 tensor are read-only pinned inputs.
The scripts disable bytecode writes before importing them. No random
sampling, numerical heavy simulation, TSIL or external-source download occurs.

Validate a record with

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/radial_ir_cold_2026_11_01/gapless_charge/run_003/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

Repeat with run_ir_001 and run_null_001. Manifest validation does not itself
verify source formulas, universal accuracy, or physical interpretation. Those
are reviewed separately in DERIVATION.md and SOURCE_RECORD.md. Historical
run_001 and run_002 failed; neither is silently relabeled completed.
