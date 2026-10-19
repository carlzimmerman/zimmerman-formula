# Reproduce this independent review's finite checks

Use the existing Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0. No installation or measured alpha is needed. Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. The first calculation was frozen before author inspection. The scalar follow-up was independently encoded after comparison; it imports no author file.

Keep the original runs. Choose new output directories and change both occurrences of each new directory together.

```
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/independent_contract.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/independent_check.py \
  --input fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/independent_inputs.json \
  --output fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/reproduce_source \
  --result fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/reproduce_source/results.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/independent_check.py \
     fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/reproduce_source/results.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/trace_contract_v2.json \
  --input fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/trace_check_v2.py \
  --output fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/reproduce_trace \
  --result fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/reproduce_trace/results.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/trace_check_v2.py \
     fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/reproduce_trace/results.json
```

For each run, validate the new manifest using

```
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_hard_vacuum/reviews/gluon/reproduce_source/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Repeat with `reproduce_trace/manifest.json`. Expected successful counts: 23 and 10. The original `trace_run_v1` is a retained failed reviewer diagnostic, caused by an incorrect expected sign for the arbitrary next coupling increment; do not overwrite it or characterize it as completed. It contains no final result file. The original successful `run_v1` and `trace_run_v2` have unchanged code/input hashes and valid result files.

These runs check exact rational identities and three real numerical filter quadratures, with two additional filter moments fixed by exact symmetry. The 60-digit quadrature tolerance is absolute 1e-50; it is not a proof by interval arithmetic. The rational source identities are uniform algebraic equalities for r!=0, while their physical interpretation requires the hierarchy and current assumptions in SOURCE_CRITICAL.md and REVIEW.md.

The commands request wall, CPU, log and conventional thread bounds, with no address-space or affinity request on macOS. Exit zero and a valid manifest do not establish the source's two-loop integral calculation, a QCD OPE remainder bound, a nonperturbative proton matrix element, or physical R/alpha.
