# Planar lapse-preservation follow-up

`REPORT.md` derives the general planar action and initial evolution, exact lapse-time ODE and complete forcing. `checks.py` independently varies the action and constructs a short spatial interval of first-time-consistent negative-response jets. `runs/main_a` is the bounded positive record; isotropy/drop_lapse_spatial/wrong_momentum controls must fail. All manifests use `contract.json` and actual hashes in `provenance.json`.

The analytic formal recursion argument is separate from the bounded computation: no convergence, full on-shell existence, global lapse boundary problem or well-posedness is claimed. Constraint preservation removes an immediate algebraic veto but leaves actual background realization open.

Reproduce with computation-audit run_experiment.py, this contract, every execution_artifact as --input, a fresh output directory and /usr/bin/python3 checks.py --output <newrun>/results.json. Caps: wall60s, CPU45s, threads1. Controls: --control isotropy, drop_lapse_spatial, wrong_momentum. Validate generated manifests. Prior action/source provenance is reused without new downloads; no external PDE theorem is asserted.
