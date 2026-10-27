# Reproduction and audit boundary

The computation checks a finite assertion: nine regular radial ODE boundary
responses for ell=2,3,4, one direct quadrupole integral, a j1 root, and fixed
benchmark unit conversions. It does not compute formation, an SP ground state,
the TF quantum surface layer, nonlinear saturation, or an occupied spectrum.

Inputs and limits are declared in `inputs.json` and `contract.json` before
execution. Exact project antecedent byte hashes are in `source_pins.json`.
The first-read HEAD, assigned parent HEAD, and run-observed HEAD differ due to
concurrent work; input hashes before and after the run agree. No Git mutation
was performed by this lane.

The actual bounded command, from project root, was:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/contract.json \
  --input sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/check_virial.py \
  --input sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/inputs.json \
  --input sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/source_pins.json \
  --input sol61_push/particle_derivation_2026_10_18/micro_response/DERIVATION.md \
  --input sol61_push/particle_derivation_2026_10_18/micro_response/EXCHANGE_REVIEW.md \
  --input sol61_push/gravity_restoring_2026_10_19/internal_polarization/INTERNAL_POLARIZATION.md \
  --input sol61_push/gravity_restoring_2026_10_19/rational_completion/RATIONAL_COMPLETION.md \
  --output sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/run_001 \
  --result sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/run_001/results.json \
  --timeout 30 --max-output-bytes 65536 --max-cpu-seconds 20 --max-threads 1 \
  -- python3 sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/check_virial.py \
  --inputs sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/inputs.json \
  --result sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/run_001/results.json
```

The output directory must be fresh. For a new repetition, replace both
`run_001` result/output occurrences consistently with a new directory name.
Do not overwrite an evidence record.

The manifest validator command was:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Observed output: `valid evidence record (run status: completed); mathematical
interpretation requires review`. Runtime 1.216356 seconds, exit 0. Caps:
30 s wall, 20 s per-process CPU, 65536-byte combined log; conventional numerical
thread variables set to one. No hard memory or affinity cap requested.

Independent checks within the script: transformed regular ODE with center
series versus library Bessel formula; surface matching versus direct mass
moment integration. All use double precision, so machine agreement is not
an interval certificate. The exact analytic argument carries the formulas.
Three tolerances and a small maximum step agree; no broad parameter scan is
claimed. Translation's zero denominator is established by sin(pi)=0 in exact
mathematics, not the floating residual.

Outcome: **implementation and finite assertion verified in the stated range**,
conditional on the stated floating tolerances and library behavior. Source
checks are separately recorded in `SOURCES.md`. The physical application remains
conditional on existence and occupation of a valid coherent, dilute,
self-gravitating state in the microscopic theory.

Self-review: reconstructed mass/contact dimensions, moment sign, exterior
potential coefficient, STF contraction, filling fraction and Fourier signs.
Math proofreading covered the entire new note and equations (1)-(21); no
preexisting file was edited. Independent cross-review has been requested from
the parent lane; this file does not pre-empt its verdict.
