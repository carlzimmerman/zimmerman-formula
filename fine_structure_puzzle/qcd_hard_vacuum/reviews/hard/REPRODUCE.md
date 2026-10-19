# Reproduce the independent bounded controls

Run from the repository root. This does not execute or modify author code.
Use a new output directory and update the final result argv to that same path.
The full primary PDFs remain in the ignored shared cache; SOURCE_NODES.json
contains only the required numeric subset and its primary TeX hash.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root . \
  --contract fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/COMPUTATION_CONTRACT.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/independent_check.py \
  --input fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/SOURCE_NODES.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/PRETARGET.md \
  --input fine_structure_puzzle/qcd_hard_vacuum/hard_proton/run_001/result.json \
  --output fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/run_002 \
  --result fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/run_002/result.json \
  --timeout 45 --max-output-bytes 1048576 --max-cpu-seconds 40 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/independent_check.py \
     fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/run_002/result.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_hard_vacuum/reviews/hard/run_002/manifest.json --root .
```

Actual initial run: run_001, 2026-10-19T17:54:49Z, CPython 3.9.6, mpmath
1.3.0, macOS arm64. Contract limits and all input hashes are in its real v2
manifest. No memory address-space cap was requested. It checks 35 finite-a
source rows, the common-mass node functional, linearized marginal-error
ceilings and fresh Dirac n=2,4 cases; it does not reproduce full source
correlator fits, mass-control tables, QCD matching or a curved vacuum.
