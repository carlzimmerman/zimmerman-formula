# Reproduce the exact finite matching algebra

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Python 3.9.6
and SymPy 1.14.0 were used. Source/source-admission inputs were frozen before
execution. The original output directory must remain intact; choose a new
directory for reproduction and change BOTH occurrences of `run_reproduce`
below together. Do not execute commands from a manifest.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/COMPUTATION_CONTRACT_v3.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/check_matching_v3.py \
  --input fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/SOURCE_INPUT.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/SOURCES.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/DERIVATION.md \
  --input fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/INPUT_PINS.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/ADDENDUM.md \
  --input fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/BRANCH_AUDIT.md \
  --output fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/run_reproduce \
  --result fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/run_reproduce/result.json \
  --timeout 45 --max-output-bytes 1048576 --max-cpu-seconds 40 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/check_matching_v3.py \
     --output fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/run_reproduce/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_hard_vacuum/gluon_matching/run_reproduce/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The command intentionally does not request address-space or CPU-affinity
limits on macOS. It bounds wall time, CPU time, combined logs and conventional
library threads. Inspect `run.status`, exact inputs, stdout and result content.
Expected success: 16 exact checks, `L-3/4` coupling threshold, vector mass
coefficients `-3L+5/2` and `-3L+17/4`, filter moments `0` and `pi^2/6`.

`run_v1` and `run_v2` are documented failed attempts, not successful evidence.
Their source inputs and scripts must not be overwritten to make their
manifests appear successful. The failed branch behavior is explained in
BRANCH_AUDIT.md. The v3 computation is exact source-translation algebra;
it does not recalculate a Feynman integral or a physical QCD matrix element.
