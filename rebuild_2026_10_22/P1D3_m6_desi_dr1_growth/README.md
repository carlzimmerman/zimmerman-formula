# P1D3_m6_desi_dr1_growth: does DESI DR1 Lyman-α P1D (z 2.2–4.4) allow X57's M6 at its bound?

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (d50412913d), committed alone before any P1D value was read.
  There are no amendments.
- **One code fix before any graded output.** The first launch was killed when NNLS overflowed on badly scaled columns.
  Column scaling was added, which does not change the χ² definition, and the run was restarted.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

**Data.**

- DESI DR1 optimal-estimator P1D: Zenodo 10.5281/zenodo.16943723, `data_points.tar`. Owner-approved download 2026-10-27;
  md5 matches the record; untracked under `_external_data/`.
- Table: `desi_y1_baseline_…_qmle_…_contcorr_v3.fits`, column PLYA with the full COVARIANCE.
- Bins: 755, using DESI's own cut 0.001 < k < 0.5π/R_z.
- The header carries `BLINDING = desi_y1`. Its status is unresolved (ledger C3).

## Verdict (frozen rule): **NOT DIAGNOSTIC (LINEAR NATIVE MODEL INADEQUATE): ROBUST on both footings**

**G0 fails everywhere.** The native linear gas proxy cannot describe per-cent-precision flux power:

| configuration | null χ² | dof |
|---|---|---|
| primary | 7017 | 719 |
| k ≤ 0.02 | 6623 | 420 |
| statistical covariance only | 7694 | 719 |
| no tilt | 9158 | 731 |
| nuisance smooth in z | 7031 | 739 |
| z ≥ 3.6 | 508 | 337 |

- The misfit is worst at z 2.2–2.6 and at large scales too, so it is not only nonlinearity. The proxy lacks the
  redshift-space and flux-bias structure of the forest.
- **G1 passes in the primary.** The Asimov Δχ² is 24.7: DESI would see M6 at the bound if the model fitted.

**Reported only, because the model fails.** The μ fits are not interpretable as M6 constraints:

| variant | μ̂ | Δχ²(μ = 1) | μ_95 |
|---|---|---|---|
| primary | 0 | 26.4 | 0.34 |
| statistical covariance only | 0 | 92.4 | 0.08 |
| nuisance smooth in z | 0 | 34.5 | 0.28 |
| **no tilt** | **3.36** | — | — |
| **z ≥ 3.6 (closest to adequate)** | 0.43 | 3.5 | 1.03 |

- In the no-tilt variant the preference reverses: Δχ²₀ is 983 in favour of M6. The direction of the "preference" depends
  on one nuisance freedom, which shows that the M6 term absorbs model misfit.
- The z ≥ 3.6 variant matches Boera's k ≤ 0.1 subset in P1D1, which gave μ̂ 0.48 and μ_95 1.26.
- Per-z μ̂ shows no 1/D² pattern: z 2.2 gives 4.85, z 2.4–3.4 give 0, and z 3.6–4.4 give 0.05, 0.33, 1.17, 0 and 1.02.
- `cov_diag_inflation.fits` was not applied, because its minimum value is 0.034 < 1 (frozen condition), so it is not a
  pure inflation.

## Checks

- **Main: 7/7 PASS, exit 0.**
  - S0: md5; 12 × 85 bins; COVARIANCE = STAT + SYST exactly; √diag = E_PK to 0.000; P1D1 M6 numbers 8/8.
  - K1, K2, K5, K6. Peak RSS is 0.50 GB.
  - K3 is **live**: a planted μ = 1 is recovered at μ̂ 1.27 with Δχ²₀ 56.5.
  - K4 is live: a planted null gives μ_95 0.57.
- **Rerun.** Identical apart from timing: 0 JSON leaf differences.
- **MUTATE (`P1D3_MUTATE=1`): exit 1.**
  - It fails S0e (m3: 7/8), as required.
  - **It does not fail K3**: the planted μ = 1 is recovered at 0.86. m1 flips the M6 sign in both injection and fit, so
    a self-consistent recovery check cannot see it. This is a twin-design flaw, disclosed, not repaired post hoc.
  - P1D1's twin failed K3 only incidentally.
  - m2 (PRAW) changes the fits (primary χ² 7540), so the column swap is live.

## What this means

- **Where M6 stands.** The forest cannot grade M6 with the framework's own linear model at DESI precision.
- **What would decide it.** A framework-native forest model adequate at the per-cent level: 3D, with redshift-space
  distortions and flux bias, in other words native 3D lognormal or hydrodynamic mocks.
- **The best available pointer.** Two independent datasets, in their most adequate regimes, give μ̂ ≈ 0.4–0.5 and
  μ_95 ≈ 1.0–1.3. M6 at X57's bound sits at the 95 % edge: neither excluded nor detected.

## Files

- `p1d3_m6_desi.py`
- `p1d3_m6_desi.out` and `p1d3_m6_desi_results.json`
- `*_MUTATE.*` (control, not physics)
