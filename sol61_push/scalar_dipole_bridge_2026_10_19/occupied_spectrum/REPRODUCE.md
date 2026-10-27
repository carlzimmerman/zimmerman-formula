# Reproduction

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Existing run
directories are immutable evidence; use a fresh directory and pass the same
name as the script's final argument. Python 3.9.6, NumPy 1.26.2 and SciPy
1.11.4 were observed for the completed run.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/contract.json \
  --input sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/occupied_spectrum_checks.py \
  --input sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/parameters.json \
  --input sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/source_pins.json \
  --output sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/run_003 \
  --result sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/run_003/results.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/occupied_spectrum_checks.py run_003

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/scalar_dipole_bridge_2026_10_19/occupied_spectrum/run_002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The first command is provided for future reproduction and has not been run
as `run_003`. `run_002` was the completed scientific run. The runner pins the
actual script, parameters and source-hash inventory before and after the
command. The pinned source documents are context, while the computation
uses only the declared analytic formulas and numeric parameters. The parent
note should recheck those source bytes before claiming historical freshness.
