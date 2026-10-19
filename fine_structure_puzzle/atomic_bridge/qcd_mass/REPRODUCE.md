# Reproduce FSP-Q-002

From the repository root, choose a fresh directory `run_003` (the runner refuses to overwrite a run). Current code is v2, which includes the electron threshold:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/atomic_bridge/qcd_mass/contract_v2.json \
  --input fine_structure_puzzle/atomic_bridge/qcd_mass/discriminator_v2.py \
  --input fine_structure_puzzle/atomic_bridge/qcd_mass/SOURCES.json \
  --input fine_structure_puzzle/atomic_bridge/qcd_mass/INPUTS.json \
  --output fine_structure_puzzle/atomic_bridge/qcd_mass/run_003 \
  --result fine_structure_puzzle/atomic_bridge/qcd_mass/run_003/results.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 fine_structure_puzzle/atomic_bridge/qcd_mass/discriminator_v2.py \
  --output fine_structure_puzzle/atomic_bridge/qcd_mass/run_003/results.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/atomic_bridge/qcd_mass/run_002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The second command validates the retained current run; use `run_003` to validate a reproduction. Required: Python and SymPy; recorded versions 3.9.6 and 1.14.0. Source PDFs are not required to rerun the algebra; their exact identities and extracted equation locators are pinned in `SOURCES.json`. No data values or fitted parameters are required. Initial code/run are preserved for the documented electron-threshold bookkeeping correction.
