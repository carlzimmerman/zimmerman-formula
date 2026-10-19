# Reproduce the bounded kernel calculation

From the project root `/Users/carlzimmerman/new_physics/zimmerman-formula`, with the recorded Python/SymPy/mpmath environment, run the following command. The output directory must be new; choose another suffix for a reproduction and change both occurrences of it. No sources are downloaded by the computation.

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_global_kernel/proton_kernel/COMPUTATION_CONTRACT.json \
  --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/check_kernel.py \
  --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/INPUTS.json \
  --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/DERIVATION.md \
  --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/SOURCE_RECEIPTS.json \
  --output fine_structure_puzzle/qcd_global_kernel/proton_kernel/run_001 \
  --result fine_structure_puzzle/qcd_global_kernel/proton_kernel/run_001/RESULTS.json \
  --timeout 60 --max-output-bytes 1048576 --max-cpu-seconds 50 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_global_kernel/proton_kernel/check_kernel.py \
  fine_structure_puzzle/qcd_global_kernel/proton_kernel/run_001/RESULTS.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_global_kernel/proton_kernel/run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

No optional address-space cap is requested because the prior macOS runs established that it can prevent launching the installed interpreter. Wall, CPU, log and conventional numerical-thread bounds are explicit. A completed manifest records finite assertions, not a proof of full QCD. Source PDF hashes can be checked against SOURCE_RECEIPTS.json; the numerical command uses their already authenticated formulas, not a PDF parser.

The separate elementary Dirac finite matching appendix uses the saved main-run results and an independent contract. Again choose a fresh output suffix for a reproduction, changing both occurrences.

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_global_kernel/proton_kernel/DIRAC_MSBAR_CONTRACT.json \
  --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/check_dirac_msbar.py \
  --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/DIRAC_MSBAR_MATCHING.md \
  --input fine_structure_puzzle/qcd_global_kernel/proton_kernel/run_001/RESULTS.json \
  --output fine_structure_puzzle/qcd_global_kernel/proton_kernel/msbar_run_001 \
  --result fine_structure_puzzle/qcd_global_kernel/proton_kernel/msbar_run_001/RESULTS.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_global_kernel/proton_kernel/check_dirac_msbar.py \
  fine_structure_puzzle/qcd_global_kernel/proton_kernel/msbar_run_001/RESULTS.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_global_kernel/proton_kernel/msbar_run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```
