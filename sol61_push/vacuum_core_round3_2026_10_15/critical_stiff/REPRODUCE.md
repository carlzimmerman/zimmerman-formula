# Reproduction and interpretation

`PROOF.md` supplies the exact Maxwell equilibrium, coupled radial congruence, positive all-radial bound, positive-part finite-D0 Newtonian continuation and its RTM/interface obstruction. `run_v1` is the current bounded evidence; the same-team independent `AUDIT.md`, when present, is separate from the author proof.

The result includes 24 exact symbolic checks. Its finite non-interval integrations use f=1341/250 as an assigned **central** density ratio and eta=0,10^-4,10^-3,10^-2. They test the implementation and illustrate the analytic branch; no interval ODE certification or universal quantitative neighborhood is claimed. At finite eta the integrated mass ratio exceeds the central input f and is recorded without resetting it. This is not a derived cosmic abundance.

From the repository root, rerun into a fresh output directory, replacing RUN_NEW consistently:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula \
 --contract sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/computation_contract.json \
 --input sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/PROOF.md \
 --input sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/check_critical_stiff.py \
 --input sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/inputs/source_manifest.json \
 --input sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/inputs/MC_BOUNDARY_PROOF.md \
 --input sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/inputs/SOURCE_FORCE_DICTIONARY.md \
 --input sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/inputs/S2_CANONICAL.md \
 --output sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/RUN_NEW \
 --result sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/RUN_NEW/results.json \
 --timeout 45 --max-output-bytes 65536 --max-cpu-seconds 35 --max-threads 1 \
 -- python3 sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/check_critical_stiff.py \
 sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/RUN_NEW/results.json
```

Validate the current hashes with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py \
 sol61_push/vacuum_core_round3_2026_10_15/critical_stiff/run_v1/manifest.json \
 --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The global nonlinear spatial Hamiltonian is a declared Newtonian field model, including its exterior. It is not a completion of the relativistic RTM vacuum action, and the unchanged finite-density RTM gate fails near this compact branch's cold edge. These restrictions apply even though the Newtonian equilibrium and radial energy are well behaved.
