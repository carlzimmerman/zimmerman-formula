# Reproduce or inspect this round

Run from the repository root. Input copies are committed inside each route;
there is no live data download or production simulation. Existing output
directories must not be overwritten.

First run `python3 sol61_push/ambitious_round4_2026_10_15/verify_round.py`.
It validates all 25 manifests with the Mathbox validator, permits exactly
the two documented stale historical Einstein inputs, checks their recovered
preimages, and verifies pinned source snapshots and current proof hashes.
Its success means artifact integrity and correct failure classification,
not mathematical truth. The validator path is in the script; change that
tool-location argument if the same Mathbox version is installed elsewhere.

For fresh scientific execution, read each manifest's actual argv and
contract, use the pinned software versions and select a new output name.
The bounded runner refuses an existing output directory. Route instructions:

- [Angular exact checks](angular/REPRODUCE.txt).
- [Einstein computation, bounds and interpretation](einstein/COMPUTATION.md).
- [Inventory exact checks and high-precision energy quadratures](inventory_energy/REPRODUCE.md).
- [Lensing report and replay instructions](lensing/RESULT.md), with
  `lensing/run_bounded.py` and each saved `*_contract.json`.

Lensing's final aggregate is `summary_verified_001`; use the actual
`native_all_verified_001` fit and supplemental `refinement_001` controls.
The extended-source diagnostics have their own declared contracts and do
not alter the original point-source criteria. The runner's CPU limits are
per process and numerical thread limits cooperative; no memory/affinity
cap was claimed. Every command records its actual revision and dirty state.

The historical failed Einstein manifests continue to refer to superseded
code at the original path. Inspect their recovered exact bytes via
`HISTORICAL_INPUT_RECOVERY.json`; do not replace current code or edit an
old manifest merely to make a present-root validation return zero.
