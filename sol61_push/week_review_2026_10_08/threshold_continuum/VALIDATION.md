# Validation and research status

October 8, 2026. The proof in REPORT.md is a self-contained, self-reviewed conditional theorem. No independent referee or subagent audited it. These computations check finite examples and implementation invariants, not its universal quantifiers.

## Results

- Baseline: 64/64 checks pass.
- Remove the continuum coupling: four checks fail, detecting the lost critical coefficient shift.
- Remove the spectral filter: three checks fail, detecting violations of the noncommuting form bound.
- All three provenance manifests validate with repository-relative input and output hashes.
- All experiment stderr files are empty.

For C=L=b=1, the unperturbed asymptotic coefficient is A=2.6285390342484543. At alpha=1/2 and D=1e-10 the paired-continuum result epsilon/D^{3/2}=2.6285173676212996, a ratio 0.9999917572. At alpha=1 it is 2.628516534280554, ratio 0.9999914401.

At alpha=1/3, an independent infinite-interval quadrature gives 2.690290120442926. Finite cutoff at D=1e-10 gives 2.6902683244120493. The limiting coefficient ratio is 1.02349255057, and its square (the corresponding toy a0 ratio at unchanged conversion eta) is 1.04753700108. This is a mathematical comparison, not a change in a measured acceleration.

For alpha=1/5, the exact continuum lower-bound ratios m(D)/D^{3/2} grow from 1.691794 at D=.01 to 53.499224 at D=1e-8. This is an analytic trial-energy bound, not a computed bound-state energy.

The 6-dimensional noncommuting matrix example verifies preservation of the transition vector, nonzero continuum coupling, both signed form inequalities and the relative matrix norm bound. Its discrete spectrum is only a check of the operator construction, not a substitute for the required continuous E^{-1/3} measure.

The log quadrature cuts off u below exp(-40). For the tested roots e>=2 and alpha>=1/3, the omitted positive integrand is O(u^2) in log coordinates and negligible relative to the stated 2e-8 residual tolerance. The independent incomplete-beta baseline and the critical direct-u quadrature test the change of variables. No randomized trials were used.

## Reproduction

Use Python 3.9.6, NumPy 1.26.2 and SciPy 1.11.4. The checked contract is contract.json. The actual command, input hashes, repository revision and dirty-state record, resource limits, elapsed time, logs and results are in each runs/*/manifest.json. Paths are relative to the repository root.

For a fresh output directory, run the installed mathbox computation-audit scripts/run_experiment.py with --root pointing to this repository, --contract to contract.json, --input to checks.py, --output and --result to a new run location, --timeout 60 --max-output-bytes 100000 --max-threads 1, followed by:

    -- python3 sol61_push/week_review_2026_10_08/threshold_continuum/checks.py --output NEW_RESULTS_PATH --mutate none

Replace none by omit_continuum or omit_filter for the negative controls; their expected scientific exit status is 1. Do not overwrite these recorded runs.

## Status and next discriminating test

Established under stated hypotheses: alpha>1/3 protects the leading coefficient, explicit examples show the boundary is sharp for this criterion, and the spectral source construction enforces a safe nonzero continuum coupling.

Conditional: applying any of this to BFSS. The actual source transition measure is unknown. The local bounded source may fail through a linear continuum shift; the matrix-ray limit is exact, but its physical packet realization has not been proved. The modified source avoids that form-bound problem by construction, while introducing an unselected energy scale and a generally nonlocal operator.

Next test: derive the operator-weighted threshold measure for a specified physical source, or first construct the escaping packets that decide the local source's linear-response obstruction. Neither total density of states nor an assumed exponent answers this. There is no selected k=1/2, exact filtered-MONO completion, or theory-of-everything result.

A metadata inspection initially looked for stdout.log/stderr.log; the runner uses stdout.txt/stderr.txt. That read-only filename mismatch did not affect any experiment.
