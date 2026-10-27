# Reproduction

From /Users/carlzimmerman/new_physics/zimmerman-formula, keep run_001 immutable and use a fresh output directory. The contract execution_artifacts exactly lists code, inputs, derivation and source-admission note. The actual command is:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/CONTRACT.json --input fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/check_sea.py --input fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/INPUTS.json --input fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/DERIVATION.md --input fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/SOURCES.json --output fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/run_REPRODUCE --result fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/run_REPRODUCE/result.json --timeout 120 --max-cpu-seconds 100 --max-output-bytes 1048576 --max-threads 1 -- python3 fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/check_sea.py fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/run_REPRODUCE/result.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_hard_vacuum/coordinator/sea_hodge/run_REPRODUCE/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The model definition supplies the finite quantities; no external source curve or numerical alpha is read. Validation checks recorded execution and freshness, not physical continuum equivalence. No RLIMIT_AS or affinity cap was requested.
