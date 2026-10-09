# CFG529: the f30-matched environment term. ENVIRONMENT VALID for isolated samples in both constructions (G1m and G2f pass; G3 ALL still fails, as labelled). In it, the census edge FAILS on both footings on f30

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (33969d1a7).
- **Scripts.** Both exit 0. All 8 controls pass in the main run, and 12/12 checks pass in MUTATE.
  - `cfg529_tables.py` builds the new census and sharp-edge tables for the 1,676 f30 groups. It took about 80 min under load and writes to `_external_data/cfg529_work/`, which is not committed.
  - `cfg529_score.py` runs the gates, the re-score and the verdict.
- **Settings.**
  - κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 are never pooled, and a0 is flat.
  - The cold energy's MASS is still required (no particle).
  - Data are on disk only; nothing was downloaded.
  - This is not "theory closed", and nothing here says the data favour the framework.
- **Numbers** come from `cfg529_score_results.json` and `cfg529_score_results_MUTATE.json`. Pairs are canonical / alt.

## What was built
- **Measured f30 leaked-satellite fraction.** CFG519 JSON `main.f30` gives **0.16863**. σ_stat is 0.0060; σ_tot is 0.0067, adding CFG519's stack-P σ_sys as declared.
- **Scaling.** The fraction enters CFG520 part B's rule, applied to the W30 HOD grid:
  - X = 0.13062 (Moster) / 0.13030 (Behroozi), so s = 1.291 / 1.294.
  - The same rule gives W10 0.2234 (s 1.2374, CFG520's exactly) and ALL parent 0.3134 (s 1.182).
- **Two constructions**, each with the measured fraction both in E and in the own-profile stripping mix:
  - **A** = CFG503: sharp r_ta boundary, halofit×ζ two-halo term, Jacobi stripping, SHMR as a rank-one term.
  - **B** = CFG504: smooth DK14 transition, x_t 0.910.
- **The census edge and CFG413's sharp-edge nodes** (x ≥ 0.2) were rebuilt with W30 stripping in both constructions.

## Environment validation (LCDM, SHMR propagated)
| | G1m stack P (0.2234) | G2f f30 (0.1686) | G3m ALL (0.3134), reported only |
|---|---|---|---|
| A (CFG503) | 26.13 (p 0.037) PASS | **22.47 (p 0.096) PASS** | 67.93 (p 1e-8) FAIL |
| B (CFG504) | 14.08 (p 0.52) PASS | **22.51 (p 0.095) PASS** | 59.23 (p 3e-7) FAIL |

- **The verdict is ENVIRONMENT VALID in both constructions.**
- It carries the label: **"G3 (ALL) FAILS: validated for isolated samples only; CFG504's three-gate rule not met."** This departure was declared in the criteria before any number was computed.
- G2f is stable across f30 ± 1σ_tot (p 0.089 to 0.101).

## Re-score on f30, measured f30 leakage (χ²/15; PASS if p > 0.01)
| model | A canonical | A alt | B canonical | B alt |
|---|---|---|---|---|
| (i) LCDM | 22.47 PASS | 22.47 PASS | 22.51 PASS | 22.51 PASS |
| (ii) law to r_ta | 54.40 FAIL | 44.26 FAIL | 59.67 FAIL | 46.18 FAIL |
| (iii) 5.85 r_M edge | 200.01 FAIL | 204.99 FAIL | 221.44 FAIL | 227.37 FAIL |
| (iv) V1 | 48.35 FAIL | 35.88 FAIL | 57.59 FAIL | 43.44 FAIL |
| (v) F_dd | 14.36 PASS | 14.28 PASS | 17.78 PASS | 17.93 PASS |
| **census edge** | **45.57 (p 6e-5)** | **35.84 (p 0.002)** | **54.10 (p 3e-6)** | **42.44 (p 2e-4)** |
| census Δ vs best sharp edge | +4.99 | +7.42 | +3.08 | +5.01 |
| best sharp edge x (χ²) | 0.50 (40.58) | 0.45 (28.42) | 0.45 (51.02) | 0.45 (37.43) |

## Verdict (frozen rule): census edge **FAIL on canonical and FAIL on alt** in the f30-matched environment
1. **Absolute rule.** The census edge fails p > 0.01 in every cell, on both footings and in both constructions.
2. **Placement statistic (Δ ≤ 4).**
   - Alt fails in both constructions (+7.42 / +5.01).
   - Canonical is split: it fails in A (+4.99) and passes in B (+3.08).
   - So alt fails both criteria in both constructions. Canonical's FAIL rests on the absolute rule; its placement alone is construction-dependent.
3. **Compared with CFG525's fixed stack-P environment (+19.44 / +20.53):**
   - Matching the window and the leakage to f30 shrinks the placement miss about 3-6×.
   - It does not close the miss on alt, and the absolute fit stays poor.
4. **Where the miss sits.** The census χ² excess is mostly in the inner 9 bins: 20.3 / 13.1, against F_dd's 3.9 and LCDM's 10.5. This is the same inner-bin deficit every law-type profile shows under stripping (CFG503 / 504). Even the best sharp edge fails absolutely on canonical (40.6 / 51.0).
5. **Clash.** The 5.85 r_M edge sits +186 to +209 above the best model on both footings. F_dd is best everywhere; as CFG495-504 already said, that is the halo-mass degeneracy, not a drawdown detection.

## How solid the fail is (reported variants, no verdict weight)
- **Census Δ is monotone in the leakage.** More stripping helps.
  - At f30 ± 1σ_tot: A +5.24..+4.74 / +7.80..+7.04; B +3.27..+2.89 / +5.35..+4.67.
  - Sum-of-bins convention: A +4.47 / +6.66; B +2.69 / +4.33.
  - E-only scaling: A +4.90 / +7.26; B +2.99 / +4.80.
  - HOD f, unscaled: A +6.46 / +9.65; B +4.20 / +7.01.
- **No variant gives the census p > 0.01 on either footing** (largest p 0.004).
- **Alt fails placement in every variant.** Its closest approach is +4.33.
- **Zero leakage (T4)** makes it much worse: +12.1 / +18.6 (A) and +9.1 / +14.9 (B). G2f still passes there (23.53 / 22.59), so leakage is weakly constrained by LCDM but strongly moves the edge.
- **Mismatched window (T3, construction A).** The stack-P environment (W10 + 0.2234) applied to the f30 data gives:
  - census Δ of only +0.12 / +0.24 (p 0.005 / 0.030);
  - LCDM 30.81 (p 0.009), which fails the G2-type gate.
  - So the near-pass seen there needs an environment that LCDM rejects. The matched one, which LCDM accepts, gives the fail above.

## Controls and MUTATE
- **Controls, all PASS:**
  - K1: data = CFG377.
  - K2a: E_nlz rebuilt, 1e-13.
  - K2: CFG503's 14 stack-P χ², f30 21.524 and ALL 73.994, exact.
  - K3: CFG520 part B, exact (LCDM 26.134).
  - K4: CFG525's H3 census +19.440 / +20.528 and best-x 63.145 / 44.657, exact.
  - K5: CFG504's 14 stack-P χ², f30 21.360 and ALL 50.905, exact.
  - K6: new sharp tables equal CFG525's, and the windowing path equals CFG504's EDGE|prim, both exact (0.0).
  - K7: scaled f' = f_meas to 6e-17.
- **MUTATE, all detected:**
  - T1: f_ret = 1 fails, +159 to +190.
  - T2: CFG525's fixed-environment fail is reproduced.
  - T3: the mismatched window is visible (1.66σ).
  - T4: zero leakage is visible (1.67-1.68σ).

## Dated disclosures (2026-10-09)
- **G3 departure.** G3 (ALL) is reported, not required. This was declared in the criteria before any number and is carried as a label. It fails in both constructions (67.9 / 59.2, inner and outer about equal).
- **Table build.** It took 80 min instead of the few minutes expected, because the machine was heavily loaded (a PM lane was running). Nothing changed.
- **Interpretation.** The inner-bin attribution in point 4 of the verdict, and the T3 reading, are written after the results were seen. They carry no verdict weight.

## Run
```
nice -n 10 python3 cfg529_tables.py                 # 4 workers -> _external_data/cfg529_work/cfg529_tables.npz
nice -n 10 python3 cfg529_score.py ; CFG529_MUTATE=1 nice -n 10 python3 cfg529_score.py
```
The inputs are read-only:
- `real_research/data/lensing_rar`;
- `_external_data/cfg50[234]_work`, `cfg525_work`;
- the committed JSON of CFG377, 503, 504, 519, 520 and 525.
