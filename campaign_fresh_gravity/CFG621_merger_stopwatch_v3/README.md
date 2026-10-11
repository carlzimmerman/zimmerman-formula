# CFG621: merger stopwatch v3 (CFG599 rerun with a measured noise floor)

- **Criteria:** two-stage freeze.
  - `FROZEN_CRITERIA_A.md` was committed alone first (3dcb3a075). It covers the isolated-halo noise floor.
  - `FROZEN_CRITERIA_B.md` (the merger criteria) is committed alone after the stage-A results and before any merger run.
  - Frozen text is never edited. Later changes are dated disclosures below.
- Settings as CFG599:
  - κ = ½ is FITTED. Both footings are kept and never pooled in physics.
  - Kernel ν(y) = 1/(1 − e^(−√y)). Candidate B, G9, no EFE.
  - The cold energy's mass is required (an input). No particle species.
  - Yardsticks are raw data only. This is not "theory closed", and nothing here says the data favour the framework.

## Stage A: estimator noise on isolated halos (no merger run)

Script: `cfg621_stageA.py` → `cfg621_stageA.out`, `cfg621_stageA_results.json`. Per-run series are in `runs_A/`.

Setup:
- 48 runs: main and sub × α 0 and 1 × both footings × seeds {599, 621–625}.
- CFG599 model and particle numbers, 0.6 Gyr per run, 61 epochs each.
- Estimator E-1: shrinking circle, R0 300 / R_min 75 kpc, for galaxy, gas and lensing.

| quantity (JSON key) | value |
|---|---|
| P95 of lensing–galaxy distance, pooled over 2928 epochs (`P95_L`) | 8.30 kpc |
| **C4 lensing tolerance T_L = 3 × P95_L = merger lensing-stability rule** (`T_L`) | **24.90 kpc** |
| P95 of gas–galaxy distance (`P95_G`) → T_G = 3 × P95_G (`T_G`) | 4.90 → **14.70 kpc** |
| T-4 (stage-B C4(b)) on all 48 runs (`C4b_T4`) | PASS. Max d_L 16.03, max d_G 12.67 kpc, max \|M(<300) drift\| 4.8% |
| per-config P95 d_L: main / sub (`per_config`) | 9.1–9.8 / 4.5–4.7 kpc |
| α 1 minus α 0 median d_L (`alpha1_minus_alpha0_median_dL`) | −0.14 to −0.30 kpc. Settling adds no drift |
| P95 of the lensing spread; isolated epochs unstable under s ≤ T_L (`P95_spread`, `R2_unstable_fraction_isolated`) | 7.66 kpc; 0.0000 |
| sub-only P95_L; N_B = P95_L,sub / (194 × 0.125) (`P95_L_sub`, `N_B`) | 4.56 kpc; **0.188 (≤ 1: Bullet score diagnostic)** |
| CFG599's failing realisation with E-1 (`R4_cfg599_realisation`) | max d_L 8.66 kpc (was 18.17 with R_min 50) |

Reading:
- The main cluster's estimator noise is a slow per-seed wander, not white noise. The P95 of a single run is close to its maximum.
- That wander is the same at α = 0 and α = 1, so it is particle noise on a cored centre, not settling.
- The sub, which is the scored halo, is about half as noisy as the main.

### Dated disclosure (2026-10-10, stage A)

- **A-1 t = 0 offsets.** The largest t = 0 offset over the 48 starts is 4.67 kpc (`t0_max_offset`). This is the galaxy peak of
  the main at seed 622. CFG599's C4(a) checks its single seed-599 realisation against 3 kpc. With E-1, the seed-599 main has
  a galaxy offset of 1.68 kpc and a lensing offset of 2.03 kpc at t = 0.
  - So the 3 kpc C4(a) tolerance is also near the R_min 75 estimator's realisation noise: seed 622 would fail it.
  - Stage A froze C4(a) as "re-run in stage B with E-1" (CFG599's check, seed 599, 3 kpc). It is kept as frozen. The seed-622
    fact is reported here, before stage B is frozen.
