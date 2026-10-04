# CFG324: candidate B's large-scale growth, from B's declared rule, scored on CMB lensing and peculiar velocities

The frozen criteria are in `FROZEN_CRITERIA.md`. They were committed alone first, in 197ee7c08 (sha256 `ca5860da…a0d7`).
κ = ½ is fitted and held fixed. Both footings are used, with the ν_mono kernel. The cold component (Ω_c h² = 0.1200) is kept in
every reading: the mass is still required, and it is not a particle species. Nothing here closes the theory.

## Why this lane

AUDIT_SIGMA8 (dd14eb3d3) left candidate B's growth untested, because gate 3.03 was "met by allowance". This lane derives the
linear growth from each reading of B's declared rule, then scores it against Planck 2018 lensing and against the 6dFGSv × 2M++
velocities, both of which are on disk.

## Readings (scored separately, never pooled; citations in FROZEN_CRITERIA §1)

| | reading | lensing 8–400 (linear / halofit base) | velocities fσ₈(z = 0.039), obs 0.249 ± 0.110 | verdict |
|---|---|---|---|---|
| **R1**, B as declared | bound-only switch T3 + identity T5 + FG001. The web is unbound (f_ta = 1.2e-3 at 20 h⁻¹Mpc, 2e-16 at 50), so growth is exactly ΛCDM | 1.000 / 1.000 (−0.39σ), χ² 10.15 | 0.437, z = +1.70 | **PASS** |
| **R2-est** | the bound regions' phantom is ADDED (Ω_ph/Ω_m = 0.73 / 0.84 at z = 0) | 1.575 / 1.589 (+20σ) can; 1.687 / 1.705 (+24σ) alt | 0.618 / 0.648, z = +3.3 / +3.6 | FAIL |
| **R2-min** | the same, with the phantom only at z ≤ 0.25 (a hard lower bound) | 1.038 / 1.047 (+1.0 / +1.3σ) can; 1.045 / 1.056 alt | 0.486 / 0.493, z = +2.15 / +2.22 | ND |
| **R2** overall | the two variants disagree on both observables | ND | ND | **NOT DETERMINED** (it already fails X-COP: CFG4_target H2) |
| **R3** | acceleration door: y_b = 5e-3 to 7e-2, far above y_th ≤ 2.1e-5, so the whole web is ON; baryon-sourced ν_mono boost from z = 100 | 26.0 (can) / 32.5 (alt), +900 to +1100σ; σ₈ 7.3 / 8.2 | 7.15 / 8.22, z > 60 | **FAIL** |

**Overall.** B's growth is now TESTED under its declared reading (R1), and it passes. The reason is simple: under the bound-only
switch with identity bookkeeping, linear growth is ΛCDM's, derived rather than assumed. The passing growth is therefore ΛCDM's,
and the pass discriminates nothing between B and ΛCDM.

The two other readings the record names behave differently. The additive bookkeeping is not determined: it fails in its estimate
variant and survives only if its phantom vanishes above z = 0.25. The acceleration-door switch fails by more than an order of
magnitude, in the same way as the chassis.

## Controls

- **C1, ΛCDM.** CLASS reproduces XR26's χ² of 10.14561 exactly, with a pull of −0.39σ. The Limber/CLASS ratio is 1.0015. The
  growth ODE matches CLASS's D(z) to 2e-5.
- **C2, chassis.** The audit's σ₈ of 23.32 / 27.48 is reproduced. Its lensing amplitude of 223 / 306 is excluded, and its
  velocities sit at z = +224 / +266.
- **C3, velocity pipeline.** R_e is reproduced to 0.0012 dex. The FFT and the direct sum agree to 0.9° at the origin. The FP
  scatter is 0.094 dex. The shuffled-u null gives β = +0.03 (0.3σ).
- **C5.** The harness's ν_mono equals FP1's exactly.
- **C4 (R3 premise) FAILED, and it is kept.** In CLASS at z = 100, δ_b/δ_cdm is 0.64 at k = 0.1 h/Mpc, and 0.64–0.86 across
  k = 0.02–1. R3's single-fluid boost therefore over-counts between z = 100 and z ~ 20. This was not re-run. R3's verdict rests
  on its margin: ×26–32 in lensing amplitude. Separately, the audit's D5 shows a boost switched on only at z = 3 still fails by
  ×8 in σ₈. The C4 failure is why part 1 returns rc = 1.
- **MUTATE (CFG324_MUTATE=1, R1 growth ×2).** Lensing reaches 3.81 (+100σ) and the velocities z = +5.7. Both rows FAIL, and both
  scripts return rc = 1.

## Caveats on the velocity measurement (none changes a frozen verdict)

- **The error is large: 44% on fσ₈.** It is dominated by the declared σ₈,g systematic, which is the full size of the corrections:
  presmoothing ×1.388 and nonlinear ×0.890. The presmoothing correction assumes the cube's 4 h⁻¹Mpc Gaussian, a value quoted from
  memory of Carrick+2015 and not checked against the paper. The raw cube σ₈ of 0.708 × 1.388 = 0.98 is close to that paper's
  quoted σ₈,g* (also from memory). R1's +1.70 is therefore a weak pass, not support.
- **The frozen mock bias correction is large: +0.139 on β = 0.424.** Without it (reported only, not scored), fσ₈ = 0.371. R1 and
  R2-min would then pass at about 1σ, and R2-est would move from FAIL to ND. The mock re-applies the magnitude limit to an
  already-selected sample, so the correction may over-count.
- **Flag: the fitted external flow is |V_ext| = 1076 km/s.** That is implausibly large, and it is likely degenerate with the FP
  zero point on a southern-sky sample. The forward FP slope a = 0.72 shows regression dilution, as expected for a fit in log R_e.
- **R1 in-halo redistribution envelope (reported).** A fully linear C_L^φφ moves the amplitude by 0.0075 (0.27σ).
- **Reported, not load-bearing.** Against the eight typed RSD points (gate 3.03), Δχ² vs ΛCDM is 0 for R1, +1.1 / +1.3 for
  R2-min, and +50 / +66 for R2-est.

## Files and runs

From the repository root, run part 1 first:

    python3 campaign_fresh_gravity/CFG324_candidate_B_growth/cfg324_growth_lensing.py      # ~6 min; 11/14, rc 1 (C4)
    python3 campaign_fresh_gravity/CFG324_candidate_B_growth/cfg324_velocities.py          # ~15 s; 6/9, rc 0
    CFG324_MUTATE=1 python3 .../cfg324_growth_lensing.py                                   # 9/14, rc 1
    CFG324_MUTATE=1 python3 .../cfg324_velocities.py   # reads the MAIN part-1 JSON; 5/9, rc 1

`cfg324_common.py` holds the harness. Outputs are the `.out` and `_results.json` files, with the `_MUTATE` versions separate. The
lane has no downloads. Its inputs are XR26's typed Planck bands, the CFG4_switch / CFG4_target results JSONs, the audit's L341
copy (sha-checked), `fp_6dfgs_campbell2014.tsv` and `twompp_density.npy`.
