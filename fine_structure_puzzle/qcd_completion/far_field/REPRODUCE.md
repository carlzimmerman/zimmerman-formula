# Reproduce the bounded bulk checks

The successful immutable evidence is `runs/bulk-002`. The first run,
`runs/bulk-001`, failed to launch under a macOS preexec address-space cap;
it is preserved and is not mathematical evidence.

The successful run used Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0 on
macOS 26.5.2 arm64. It used one conventional numerical-library thread,
30 CPU seconds, 40 wall seconds and 1 MiB maximum combined stdout/stderr.
No package installation, randomness or physical-data input was used.

Run from the repository root. The output directory must be fresh; use a new
name in both the runner options and the final script argument. This exact
recorded command created bulk-002:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_completion/far_field/COMPUTATION_CONTRACT.json \
  --input fine_structure_puzzle/qcd_completion/far_field/check_bulk.py \
  --input fine_structure_puzzle/qcd_completion/far_field/CONTRACT.md \
  --input fine_structure_puzzle/qcd_completion/far_field/RAW_STATIC_DERIVATION.md \
  --input fine_structure_puzzle/qcd_completion/far_field/RAW_KK_DERIVATION.md \
  --output fine_structure_puzzle/qcd_completion/far_field/runs/bulk-002 \
  --result fine_structure_puzzle/qcd_completion/far_field/runs/bulk-002/checks.json \
  --timeout 40 --max-output-bytes 1048576 --max-cpu-seconds 30 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_completion/far_field/check_bulk.py \
       fine_structure_puzzle/qcd_completion/far_field/runs/bulk-002
```

Validation executed successfully:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_completion/far_field/runs/bulk-002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The manifest pins all four input artifacts before and after the run,
repository commit/dirty state, software, hardware, limits and result hashes.
The exact symbolic assertions and the numerical sample population are in
COMPUTATION_CONTRACT.json; these finite checks supplement the analytic
derivation and do not evaluate any global finite-wall determinant.
