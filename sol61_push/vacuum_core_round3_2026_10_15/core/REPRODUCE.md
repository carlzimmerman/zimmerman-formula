# Reproduction and run history

The authoritative bounded result is `run_v3/manifest.json`, `run_v3/results.json`, and its raw logs. Its claim-supporting inputs are the frozen `PROOF.md`, `check_core_v3.py`, and the source snapshots listed in `computation_contract_v3.json`. `AMENDMENT.md` clarifies the EOS endpoint after that run without changing its constants or pinned files. `AUDIT.md`, when present, is the independent same-team mathematical audit.

From the repository root, rerun into a **new** output directory, replacing RUN_NEW below consistently:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract sol61_push/vacuum_core_round3_2026_10_15/core/computation_contract_v3.json \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/PROOF.md \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/check_core_v3.py \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/source_manifest.json \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/PRIOR_CORE_PROOF.md \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/PRIOR_ACTION_PROOF.md \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/PRIOR_JOINT_AUDIT.md \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/MODES_PROOF.md \
  --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/SOURCE_FORCE_DICTIONARY.md \
  --output sol61_push/vacuum_core_round3_2026_10_15/core/RUN_NEW \
  --result sol61_push/vacuum_core_round3_2026_10_15/core/RUN_NEW/results.json \
  --timeout 45 --max-output-bytes 65536 --max-cpu-seconds 35 --max-threads 1 \
  -- python3 sol61_push/vacuum_core_round3_2026_10_15/core/check_core_v3.py \
  sol61_push/vacuum_core_round3_2026_10_15/core/RUN_NEW/results.json
```

`run_v1` failed in an implementation-only maximum-substitution assertion, before testing the integral and interval claims. `check_core.py` and `DRAFT_PROOF_V1.md` retain its exact draft versions. `run_v2` passed but is an archived draft because its proof had the wrong displacement tail power; its exact proof bytes are `DRAFT_PROOF_V2.md`, and its code remains `check_core_v2.py`. Historical manifests referencing the live `PROOF.md` are expected to detect this proof revision; neither is authoritative evidence for the final text. No historical output is deleted or promoted to a current pass.

The final runner reports actual software, argv, input/output hashes, effective caps, runtime and logs. Validate the current record with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/vacuum_core_round3_2026_10_15/core/run_v3/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```
