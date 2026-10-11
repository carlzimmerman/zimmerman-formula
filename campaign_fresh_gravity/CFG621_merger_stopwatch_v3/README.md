# CFG621: merger stopwatch v3 (CFG599 rerun with a measured noise floor)

- **Status (stage B, 2026-10-11): VALID as frozen.** Every gate passed: the controls, C4(b), the calibration and MUTATE M1–M3.
  - **V-1 instant re-settling: EXCLUDED.** Z_B = +7.86 (canonical) and +8.06 (alt).
  - **V-2 pure collisionless: UNDETERMINED.** The α = 0 Bullet cell is unscorable (disclosure B-D1).
  - **V-3: INCOMPATIBLE by the literal frozen rule.** No node α ≥ 1 is allowed on both footings. But α = 1, 3 and 10 are
    UNSCORABLE, not excluded; only α = ∞ is excluded.
  - **No node is ALLOWED on either footing.**
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

## Stage B: the merger scan (criteria `FROZEN_CRITERIA_B.md`, 4dfa0833b)

Scripts:
- `cfg621_controls.py` → `cfg621_controls.out/_results.json`
- `CFG621_MUTATE=1 cfg621_main.py` → `cfg621_MUTATE.out`, `cfg621_results_MUTATE.json`
- `cfg621_main.py` → `cfg621.out`, `cfg621_results.json`
- Run cache: `runs_B/`

### Gates

| gate | result (JSON) |
|---|---|
| C1 Poisson / C2 Sod / C3 phantom | PASS: 2.83% / 1.12% / 0.13% (`cfg621_controls_results.json`) |
| C4(a), estimator R_min 75 at t = 0 (seed 599) | PASS: main galaxy 1.68, gas 0.0, lensing 2.03 kpc; sub 1.72 / 0.12 / 1.70 kpc |
| C5, C6 | PASS (unchanged code) |
| C4(b) = stage-A T-4; N_B | PASS; 0.188 (`cfg621_results.json` → `C4b`, `N_B`) |
| Calibration K1 + G1 at α = 0, canonical | PASS. v0 = 2666.7 km/s, η = 1.132 (in [0.1, 2.5]); speed 2699.4 km/s, d_SG 196.9 kpc (`calibration`). It took one round. |
| Alt footing at α = 0 | valid: speed 2686.5 km/s, d_SG 197.0 kpc (`footing_validity_alpha0`) |
| M1 α = ∞: f ≥ 0.5 | PASS, f = 1.027 (`cfg621_results_MUTATE.json`) |
| M2 α = 0: \|f\| ≤ 0.25 and β̄ ≤ 0.10 | PASS, f = 0.181, β̄ = 0.082 |
| M3 roles swapped, α = ∞: f ≤ 0.25 | PASS, f = 0.235 (a narrow pass); the swapped α = 0 run gives 0.104 |
| M4 seed 600 vs 599 at α = 0 (reported) | Δf = +0.031, Δβ̄ = +0.026; d_SG 196.8 vs 196.9 kpc |

### Per-node scores

Sub halo; f at the 720-kpc epoch; Harvey β̄ over 0.1–0.6 Gyr after pericentre (`cfg621_results.json` → `cells`). Spread is the
lensing spread at the two bracketing diagnostics; a cell is stable iff the spread is ≤ T_L = 24.90 kpc.

| α | foot | f | Z_B | spread [kpc] | n_H used | β̄ | Z_H | status |
|---|---|---|---|---|---|---|---|---|
| 0 | can | +0.181 | +1.09 | 131.0, 66.2 | 40/50 | +0.082 | +1.75 | UNSCORABLE (Bullet unstable) |
| 0.03 | can | +0.435 | +3.12 | 85.6, 55.1 | 43/50 | +0.260 | +4.29 | UNSCORABLE |
| 0.1 | can | +0.803 | +6.07 | 87.4, 87.3 | 30/50 | +0.568 | +8.69 | UNSCORABLE |
| 0.3 | can | +1.005 | +7.68 | 19.6, 19.6 | 41/50 | +0.991 | +14.73 | **EXCLUDED** |
| 1 | can | +2.073 | +16.23 | 94.7, 95.3 | 1/50 | — | — | UNSCORABLE |
| 3 | can | +1.078 | +8.27 | 287.9, 299.7 | 0/50 | — | — | UNSCORABLE |
| 10 | can | +1.056 | +8.08 | 95.8, 70.1 | 2/50 | — | — | UNSCORABLE |
| ∞ | can | +1.027 | +7.86 | 18.3, 18.4 | 34/50 | +1.015 | +15.07 | **EXCLUDED** |
| 0 | alt | +0.178 | +1.06 | 80.2, 50.3 | 39/50 | +0.061 | +1.44 | UNSCORABLE (Bullet unstable) |
| 0.03 | alt | +0.377 | +2.65 | 54.3, 54.7 | 40/50 | +0.215 | +3.64 | UNSCORABLE |
| 0.1 | alt | +0.782 | +5.90 | 11.3, 24.1 | 19/50 | — | — | UNSCORABLE (Harvey < half) |
| 0.3 | alt | +0.989 | +7.55 | 30.8, 31.4 | 37/50 | +1.000 | +14.86 | UNSCORABLE |
| 1 | alt | +2.079 | +16.27 | 33.2, 33.2 | 3/50 | — | — | UNSCORABLE |
| 3 | alt | +1.109 | +8.51 | 285.3, 297.3 | 0/50 | — | — | UNSCORABLE |
| 10 | alt | +1.125 | +8.64 | 87.8, 71.8 | 0/50 | — | — | UNSCORABLE |
| ∞ | alt | +1.052 | +8.06 | 19.0, 19.0 | 28/50 | +1.020 | +15.14 | **EXCLUDED** |

- Allowed set: none on either footing.
- Excluded: canonical {0.3, ∞}, alt {∞}.

### Verdicts (frozen V-1 to V-4, `cfg621_results.json` → `verdicts`)

- **V-1 instant re-settling (α = ∞): EXCLUDED.** Z_B = +7.86 and +8.06, at least 3 on both footings. The lensing peak is stable
  there (spread 18–19 kpc) and sits on the stripped gas (f ≈ 1.03–1.05). Z_H = +15.1 on both footings. M1 confirms the
  machinery puts the lensing on the gas at α = ∞, and M3 confirms it follows the collisionless baryons when the roles are swapped.
- **V-2 pure collisionless (α = 0): UNDETERMINED.** The Harvey side is scorable and within 2σ on both footings (Z_H +1.75 / +1.44).
  The Bullet cell is unscorable, because one convergence variant leaves the sub (B-D1).
- **V-3 galaxy-side compatibility: INCOMPATIBLE under the literal frozen rule** (no node α ≥ 1 is allowed on both footings).
  - Read honestly, it is driven by unscorability at α = 1, 3 and 10, plus the exclusion of α = ∞.
  - The unscored as-run Bullet values at α = 1, 3 and 10 are Z_B = +8 to +16 on both footings. None of them is near the data.
  - At α = 1 the sub's primary lensing peak lies about 440 kpc from its galaxies on the gas side, past the gas.
  - So no reading of this lane supports compatibility with the galaxy-side α ≳ 0.5.
- **V-4: "mixed".** α = ∞ is excluded; α = 0 is not determined. Every node with α ≥ 0.03 that has a Bullet value (scored or not)
  has Z_B ≥ 2.65.
  - The unscored as-run readings rise steadily from α = 0 (Z_B ≈ +1.1, Z_H ≈ +1.4 to +1.8) to α = 0.3 (Z_B ≈ +7.6).
  - Unscored reading only: the merger side, as modelled here (case L, rule 2S, no EFE, CFG599 cool core), leans to α ≲ 0.03.
    That is in tension with the galaxy-side α ≳ 0.5. The α = 0 node is the one that would need a scorable Bullet cell to settle V-2.

### Dated disclosures (2026-10-11, stage B)

- **B-D1 Merger-side spread is set by the environment, not by isolated noise.** Source: `cfg621_spread_diag.py` →
  `.out`, `_results.json`; post-run, no verdict changed.
  - Of the 32 bracketing epochs of the grid, 18 have the (R0, R_min) = (400, 75) variant above T_L. That variant's 400-kpc
    starting circle around the sub reaches toward the main cluster about 700 kpc away and lands elsewhere.
  - At α = 0 that variant alone makes the Bullet cell unstable: the other three variants agree within 11.7 kpc.
  - At α = 1 and α = 3 the disagreement is among the remaining variants; at α = 3 the (300, 90) variant is also off by about 285 kpc.
  - Stage A measured the estimator on isolated halos, as frozen, so it could not see this. The stage-B stability rule
    (spread ≤ T_L) therefore makes most merger cells unscorable.
  - This is a design limitation of the two-stage freeze, stated as such. The frozen verdicts stand as computed.
- **B-D2 Order.** MUTATE (with the calibration) ran before the grid, as §3 of criteria B requires. The grid then re-used the
  calibration and the identical α = 0 and α = ∞ canonical runs from the cache. The verdict pass read the MUTATE gate (all pass)
  in the same invocation.
- **Not claimed:** any allowed α; that collisionless is allowed; compatibility with the galaxy side. Instant re-settling is
  excluded only within this model (case L only, no EFE, a declared cool-core drag model, σ_f = 0.125 PROVISIONAL).

### What a v4 would need (new frozen criteria first)

1. A merger-calibrated stability rule, for example the spread across a seed ensemble at α = 0 in the merger. Or convergence
   variants whose starting circle cannot reach the other cluster (R0 ≤ d_sub-main / 3), frozen before any run.
2. Then α = 0, 0.03 and 0.1 rescored. Those are the cells that decide V-2 and whether any α is allowed.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA_A.md` | stage A, the noise floor (3dcb3a075) |
| `FROZEN_CRITERIA_B.md` | stage B, the merger scan (4dfa0833b) |
| `cfg621_sim.py` | CFG599 simulator + estimator E-1/E-2 |
| `cfg621_stageA.py` → `.out`, `_results.json`, `runs_A/` | stage A |
| `cfg621_controls.py` → `.out`, `_results.json` | C1–C3, C4(a), C5, C6 |
| `cfg621_main.py` → `cfg621.out`, `cfg621_results.json`; `_MUTATE` variants | calibration, MUTATE, grid, verdicts |
| `cfg621_spread_diag.py` → `.out`, `_results.json` | B-D1 |
| `runs_B/` | calibration, MUTATE and grid time series |

Compute: nice -n 10, ≤ 4 processes of 1 thread, about 1.5 GB each.
