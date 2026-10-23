# T1_efe_strength AMENDMENT A2 (POST-HOC, after a development smoke test; append-only; no verdict line changed)

**What had been seen.** A development run in a scratch directory (not committed): the satellites on 3 systems only, Coma at
ε = 0, 0.5, 1 (S1's committed values, reproduced), F2's Track A at x_e ≤ 0.003 (F2's committed values, reproduced), the
globulars on a 4 × 4 sub-grid, the wide-binary curve, and the full LENS-P2 curve (it is read from P2's JSON, so its
per-dataset numbers were seen: canonical ε̂ at the 1.5 edge, 95 % [0.67, 1.5] of the catalogue field). No production SAT,
GC or full-grid LENS-F2 number existed. Nothing in `FROZEN_CRITERIA.md` or `AMENDMENT_A1.md` is changed.

1. **K3b stays as written and fails on its third clause.** A1 asked for a *GLS* (full-covariance) amplitude from P2's
   profile to reproduce P2's A_out(a) to 1e-6. P2's estimator is not GLS: it weights by m/var with the diagonal
   jackknife variance and takes σ from the jackknife of the ratio (`p2_spec_isolated_lensing.py`, `amps()`). The GLS value
   is 0.127 ± 0.261 against P2's 0.195 ± 0.269 (canonical). My A1 text was mis-specified; the frozen K3b FAIL is kept and
   the run exits 1 because of it. The GLS values are reported as a robustness line.
2. **K3c (new, post-hoc):** P2's own estimator recomputed from P2's committed profile and covariance reproduces A_out for
   (a), (b), (b_lo) to 1e-6, and the covariance-propagated σ is within 1 % of P2's jackknife σ, on both footings.
   This is the check that the LENS-P2 likelihood is read correctly.
3. **Implementation fixes (no frozen line touched):** the F2-vs-P2 absolute-x_e block evaluates each curve on its own
   full scan range (the smoke test had truncated P2 to F2's grid); the verdict header names LENS-P2 per A1; the
   non-overlapping pairs of the primary set are printed on the verdict line; the "bary"-reference restatement promised in
   A1 §1/§4 is implemented as reported combinations C9b, C10b and Vb.
