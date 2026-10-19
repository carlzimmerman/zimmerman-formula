# Exact finite-ensemble audit

From the repository root, choose a new output directory, for example
runs/weyl-rerun, and replace both output/result occurrences accordingly:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/COMPUTATION_CONTRACT.json --input fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/check_weyl.py --input fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/DERIVATION.md --input fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/INPUTS.json --input fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/SOURCE_RECEIPTS.json --output fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/runs/weyl-rerun --result fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/runs/weyl-rerun/results.json --timeout 35 --max-output-bytes 65536 --max-cpu-seconds 25 --max-threads 1 -- python3 fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/check_weyl.py --result fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/runs/weyl-rerun/results.json
```

Validate the existing completed record without rerunning:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_nonborn_vacuum/vacuum_global/runs/weyl-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

No address-space limit is requested on macOS. This runs rational algebra
fixtures and source-action symmetry checks, not a QCD ensemble or data fit.
