# Reproduction and scope

`PROOF.md` supplies the analytic sufficiently-small-parameter existence and radial coercivity argument. `AMENDMENT.md` fixes the interpretation of parameter choice, the auxiliary vacuum-free ODE limit, the charged chemical constant, and run provenance. `STIFFNESS_DICTIONARY.md` is optional and is not an assumption needed for the theorem. None supplies full angular, Einstein, nonlinear or empirical closure.

The current bounded evidence is `run_v2`, using `computation_contract_v2.json`, which correctly records Python 3.9.6, SymPy 1.14.0, NumPy 1.26.2 and SciPy 1.11.4. `run_v1` is preserved as a successful draft with inaccurate NumPy metadata, not authoritative provenance. Proof/code bytes did not change between runs.

To reproduce, run from the repository root into a fresh output directory, replacing RUN_NEW consistently:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula \
 --contract sol61_push/vacuum_core_round3_2026_10_15/stiff_core/computation_contract_v2.json \
 --input sol61_push/vacuum_core_round3_2026_10_15/stiff_core/PROOF.md \
 --input sol61_push/vacuum_core_round3_2026_10_15/stiff_core/check_stiff_core.py \
 --input sol61_push/vacuum_core_round3_2026_10_15/core/PROOF.md \
 --input sol61_push/vacuum_core_round3_2026_10_15/core/AMENDMENT.md \
 --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/MODES_PROOF.md \
 --input sol61_push/vacuum_core_round3_2026_10_15/core/inputs/PRIOR_ACTION_PROOF.md \
 --output sol61_push/vacuum_core_round3_2026_10_15/stiff_core/RUN_NEW \
 --result sol61_push/vacuum_core_round3_2026_10_15/stiff_core/RUN_NEW/results.json \
 --timeout 45 --max-output-bytes 65536 --max-cpu-seconds 35 --max-threads 1 \
 -- python3 sol61_push/vacuum_core_round3_2026_10_15/stiff_core/check_stiff_core.py \
 sol61_push/vacuum_core_round3_2026_10_15/stiff_core/RUN_NEW/results.json
```

The 15 exact symbolic checks verify the specified reduction, base solution, matching derivative, and constants. The three finite non-interval shooting runs use outer radii 100, 200 and 400, with a first-Picard neutral tail match and its analytic contraction remainder conditional on the integrated endpoint. They are floating implementation diagnostics. They do not certify the selected numerical point by interval ODE integration or quantify the existence theorem's open neighborhood.

Validate the pinned record with the Mathbox validator, supplying `--root` to check all current file hashes:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py \
 sol61_push/vacuum_core_round3_2026_10_15/stiff_core/run_v2/manifest.json \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula
```
