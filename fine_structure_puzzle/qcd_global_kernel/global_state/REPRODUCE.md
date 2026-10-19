# Reproduce the declared finite check

Run from /Users/carlzimmerman/new_physics/zimmerman-formula. The output directory must be fresh; replace run_001 and its result path together for a new reproduction. The unchanged contract and all declared inputs must be used. No installs or external data are needed.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_global_kernel/global_state/contract.json \
  --input fine_structure_puzzle/qcd_global_kernel/global_state/check_wall.py \
  --input fine_structure_puzzle/qcd_global_kernel/global_state/DERIVATION.md \
  --input fine_structure_puzzle/qcd_global_kernel/global_state/REPORT.md \
  --input fine_structure_puzzle/qcd_global_kernel/global_state/INPUTS.json \
  --input fine_structure_puzzle/qcd_global_kernel/global_state/SOURCE_RECEIPTS.json \
  --input fine_structure_puzzle/qcd_global_kernel/global_state/REPRODUCE.md \
  --output fine_structure_puzzle/qcd_global_kernel/global_state/run_001 \
  --result fine_structure_puzzle/qcd_global_kernel/global_state/run_001/RESULTS.json \
  --timeout 40 --max-output-bytes 65536 --max-cpu-seconds 30 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_global_kernel/global_state/check_wall.py \
  fine_structure_puzzle/qcd_global_kernel/global_state/run_001/RESULTS.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_global_kernel/global_state/run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The contract pins numerical fixture bounds and versioned software. No RLIMIT_AS is requested: the macOS address-space limit is deliberately unused. One conventional library thread is a requested environment cap, not an enforced CPU-affinity limit. The analytic theorem and its physical scope must be read separately from the process status.
