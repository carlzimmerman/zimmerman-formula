# Reproduce FSP-S

Read REPORT.md for the result and its restricted scope. No measured alpha is an input.

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula` with Python 3.9.6 and mpmath 1.3.0. Use a **new** output directory if the existing run is retained:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract fine_structure_puzzle/spectral_route/contract.json \
  --input fine_structure_puzzle/spectral_route/spectral_check.py \
  --output fine_structure_puzzle/spectral_route/runs/reproduce_001 \
  --result fine_structure_puzzle/spectral_route/runs/reproduce_001/results.json \
  --timeout 30 --max-output-bytes 1048576 --max-cpu-seconds 25 --max-threads 1 \
  -- python3 fine_structure_puzzle/spectral_route/spectral_check.py \
  --output fine_structure_puzzle/spectral_route/runs/reproduce_001/results.json
```

For the sign control, substitute `contract_control.json`, a fresh directory, and append `--mutate-spectral-sign` to the child command. The expected runner status is `failed`, exit 1, with 11 failed mathematical checks at each precision. It deliberately reverses the spectral response sign; it is not a positive-evidence run.

Validate either manifest:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  fine_structure_puzzle/spectral_route/runs/main_003/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The initial launch and finite-precision failures are retained and explained in REPORT.md. Their original code is `archive_inputs/spectral_check_initial.py`; its hash equals the historical manifest input hash. Old manifests are historical records and will not validate against the revised current script path without reconstructing their original inputs.

Source records pin seven exact PDF versions and extracted-text hashes. They were acquired to `/private/tmp/fsp_spectral_sources/` and read there. No full source text/PDF is placed in tracked files or assumed available on another clone. The project cache was queried read-only before acquisition; no cache write was made outside this agent's ownership. Reacquisition URLs and extraction command are in `source_records.json`. A PDF hash authenticates bytes, not the scientific implication.

`LIFTING_REVIEW.md` is a separately requested focused review of the archive route's displayed hypothetical potential. Its authoritative record is `runs/lifting_review_001/manifest.json`; the script reads/hashes the report as a declared input and independently derives seven symbolic checks without importing archive code. Reproduce by using `contract_lifting.json`, both `lifting_check.py` and `archive_audit/REPORT.md` as runner `--input` arguments, a fresh output directory/result path, and child command `python3 fine_structure_puzzle/spectral_route/lifting_check.py --output .../results.json` with the same runner limits. No whole archive rerun is needed.
