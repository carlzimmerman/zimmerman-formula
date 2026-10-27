# Reproduction

From `/Users/carlzimmerman/new_physics/zimmerman-formula`, validate the saved run:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_global_kernel/sea_flavor/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

A new bounded reproduction must use a fresh output directory, for example:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula \
 --contract fine_structure_puzzle/qcd_global_kernel/sea_flavor/COMPUTATION_CONTRACT.json \
 --input fine_structure_puzzle/qcd_global_kernel/sea_flavor/check_flavor.py \
 --input fine_structure_puzzle/qcd_global_kernel/sea_flavor/DERIVATION.md \
 --input fine_structure_puzzle/qcd_global_kernel/sea_flavor/CONTRACT.md \
 --input fine_structure_puzzle/qcd_global_kernel/sea_flavor/INPUTS.json \
 --output fine_structure_puzzle/qcd_global_kernel/sea_flavor/reproduction_001 \
 --result fine_structure_puzzle/qcd_global_kernel/sea_flavor/reproduction_001/result.json \
 --timeout 45 --max-output-bytes 1048576 --max-cpu-seconds 35 --max-threads 1 \
 -- python3 fine_structure_puzzle/qcd_global_kernel/sea_flavor/check_flavor.py \
 --output fine_structure_puzzle/qcd_global_kernel/sea_flavor/reproduction_001/result.json
```

No memory/affinity limit is asserted. The finite symbolic check needs Python
3.9.6 and SymPy 1.14.0 as recorded; no network or random sampling is used.
The three original determinant matrices, vertices, seagulls and gauge weights
are explicit in the script. New ensemble input is necessary to evaluate QCD;
rerunning this benchmark cannot produce it.
