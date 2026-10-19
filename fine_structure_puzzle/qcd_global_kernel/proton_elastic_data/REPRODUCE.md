# Reproduce the finite source-data functional

From `/Users/carlzimmerman/new_physics/zimmerman-formula`, run the command below in a fresh output directory. For a reproduction change both occurrences of `run_001` to another unused suffix. Existing scientific results must not be overwritten.

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/COMPUTATION_CONTRACT.json \
  --input fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/check_elastic.py \
  --input fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/INPUTS.json \
  --input fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/SOURCE_RECEIPTS.json \
  --input fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/DERIVATION.md \
  --input fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/sources/src/table_ffs.tex \
  --output fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/run_001 \
  --result fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/run_001/RESULTS.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/check_elastic.py \
  fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/run_001/RESULTS.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_global_kernel/proton_elastic_data/run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The program uses retained primary-source data and performs no network requests or Q² fits. No address-space cap is requested; the recorded macOS environment supports the stated CPU/wall/log/thread caps. Source archive extraction and PDF rendering were data-acquisition operations, not scientific numerical results: the full archive inventory, source hashes and a PDF page image are retained.
