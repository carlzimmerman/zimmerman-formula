# Scalar gravitational susceptibility and critical host continuation

Start with `DERIVATION.md`. It distinguishes the actual charge-1/charge-2 carrier from the separate canonical charged host and gives explicit density, mediator, phase and gravity formulas. `LITERATURE.md` contains the narrow primary-source comparison for the constructive three-body continuation.

New bounded calculation: 78 exact/finite checks passed in `run_002`; the runner-v2 manifest validates with status `completed`. The checks support precisely the declared formulas/range, not a full gravitational law or physical `a0`. The critical `lambda=2` branch is a declared change from the original host `lambda=2−1/M`.

`source_pins.json` pins the working bytes and records the initial requested Git base plus the later concurrently changed HEAD. No source/current/frozen/manuscript file was edited by this lane.

To regenerate into a fresh directory, use the argument list in `run_002/manifest.json` (change both output directory occurrences and the declared result path). The exact original invocation is recorded there. To validate the existing evidence:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/particle_derivation_2026_10_18/micro_response/run_002/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The run’s input hashes cover the script and action/normalization sources. The prose notes were completed after that run; they are analytic reports, not additional machine-verified assertions. No heavy simulation or queue was launched.

`EXCHANGE_REVIEW.md` independently reconstructs the adjacent exchange note’s threshold matching, pair factors, signs, detailed balance, energy moments and explicit delta-host overlap. No algebraic defect was found in that narrow scope; its full numerical implementation was not independently audited.

`HARD_NUMBER_LOSS.md` derives the original-action X+X−→Phi+Phi− channel, exact threshold flux and decay comparison, and a restricted integrated weighted-current defect. Its separate authoritative `hard_loss_run_002` has 34 checks and a validated runner-v2 manifest. `HISTORICAL_INPUTS.json` records exact hash-verified v1 script snapshots; historical 001 manifests retain their original paths/hashes and are not current-root freshness evidence.

`REVIEW_CORRECTION.json` and `DERIVATION_PRE_REVIEW.md` preserve the independent review correction: exact S positivity is distinct from leading NR X positivity close to cancellations. The final response derivation is independently reviewed in the adjacent `micro_exchange/RESPONSE_REVIEW.md`; the earlier `self_review.json` pins the preserved pre-review bytes.
