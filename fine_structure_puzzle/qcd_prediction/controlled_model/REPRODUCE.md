# Reproduce QCD-C

No dependencies were installed. Observed runtime: Python 3.9.6, mpmath 1.3.0.
Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`.
The original output directory must remain immutable; choose a new directory
and make the same change in `--output`, `--result` and the child's `--output`.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/qcd_prediction/controlled_model/contract.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/check_maxwell.py \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/inputs.json \
  --input fine_structure_puzzle/qcd_prediction/controlled_model/source_records.json \
  --output fine_structure_puzzle/qcd_prediction/controlled_model/run_003 \
  --result fine_structure_puzzle/qcd_prediction/controlled_model/run_003/results.json \
  --timeout 90 --max-output-bytes 1048576 --max-cpu-seconds 80 --max-threads 1 \
  -- python3 fine_structure_puzzle/qcd_prediction/controlled_model/check_maxwell.py \
  --inputs fine_structure_puzzle/qcd_prediction/controlled_model/inputs.json \
  --output fine_structure_puzzle/qcd_prediction/controlled_model/run_003/results.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/qcd_prediction/controlled_model/run_002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

`run_002/results.json` contains the grid and all checks; the runner records
input hashes before/after, code revision/dirty state, argv, resources, exit
status and result hashes. A zero exit is only execution evidence; the analytic
asymptotic reduction and interpretation are in `REPORT.md`.

The source can be reacquired, without assuming a retained cache:

```bash
curl -L --fail --silent --show-error https://arxiv.org/pdf/1301.1706v2 \
  -o /private/tmp/fsp003_1301.1706v2.pdf
shasum -a 256 /private/tmp/fsp003_1301.1706v2.pdf
pdftotext -layout /private/tmp/fsp003_1301.1706v2.pdf /private/tmp/fsp003_1301.1706v2.txt
```

The PDF hash observed here was
`833d06861858d30708e857310b049fe28a7a88f6b9c3d69265d90e0ecd609a3e`.
Check the metadata/version separately; do not silently treat a different
download as the same byte-pinned source. Its regenerated title-page date
differs from the arXiv version date, as documented in `source_records.json`.

`run_001/manifest.json` records an unsuccessful audit before the numerical
zero-normalization fix. Its original main-script input is now stale by design;
the identical old bytes are retained in `run_001/check_maxwell_at_failure.py`.
Do not count that run among completed numerical evidence.
