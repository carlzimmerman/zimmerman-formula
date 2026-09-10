# Stationary clock action: verified checkpoint, not full gravity closure

## Strongest result

An explicit logarithmic/square-root clock action now has an exactly closing Hamiltonian self-bracket, a derived stationary restoring coefficient B=A/q+2A²/U, and a reconstructed dustlike linear background history. All 1,665 tested local events pass the scalar principal kinetic/ellipticity/real-characteristic/metric-cone gates, including clock offsets and non-longitudinal directions. Seven new Lean theorems compile. The full nonlinear constraint operator and cubic interactions remain unproved; there is still no same-action MOND/lensing/CMB completion.

## Exact new scope

- `derive.py`, `repair.py`, `stationary.py`, `run_checks.py`;
- `Characteristic.lean`, `Repair.lean`, `Stationarity.lean`;
- `README.md`, `CHECKPOINT.md`, `contract.json`;
- `run_001/manifest.json`, `run_001/stdout.txt`, `run_001/stderr.txt`;
- `run_001/results.json`, `run_001/derive.json`, `run_001/repair.json`, `run_001/stationary.json`, `run_001/prior_cases.json`.

All are inside this `nonlinear_transport/` directory. No prior proof or unrelated working-tree edit was changed.

## Commands, exits and reproducibility

The manifest records the exact bounded-run argument array and source/output hashes. `run_001/results.json` records each exact test command, working directory, stdout, stderr and exit. The seven top-level cases exited 0: three research scripts, three Lean builds, and the prior-ten-case regression. All ten underlying prior cases also exited 0. Source-hash manifest validation exited 0.

These exits have different meanings: `derive.py` supplies an old-action fast-characteristic witness; `repair.py` records both passes and gradient failures of the intermediate polynomial construction; `stationary.py` records 1,665/1,665 passes for the surviving local test family. No exit is a full-theory certificate. The maximum sampled |speed| is 0.9899783991c; the two profile integrators disagree by at most 2.13×10⁻¹¹ in log coordinates. The actual Lean characteristic polynomial is checked against the one derived from the action.

## Next unavoidable calculation

Compute the variable-coefficient operator δE/δN for the logarithmic/square-root action in README §6, preserve its complete Dirac chain, and establish its kernel and invertibility with stated boundary conditions, treating k=0 separately. Then calculate cubic interaction scales, caustics and the shrinking m→0 domain. This is the current constraint bottleneck—not another free-coefficient scan. Radiation, ordinary matter and the exponential MOND operator must subsequently be included and re-varied in the same action. Full-theory status: **OPEN**.
