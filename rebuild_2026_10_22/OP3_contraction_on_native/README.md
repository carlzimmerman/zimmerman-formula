# OP3_contraction_on_native: BREAKS IT (Υ low). With LC1's measured contraction the native profile reads Υ 0.44 / 0.41 and the line fails, narrowly. It removes the dwarf pile-up and the high-V_flat shortfall, and over-masses L★ galaxies by +13 to +22 km/s

Criteria: `FROZEN_CRITERIA.md` (4698a8bad6), committed alone before any script or number. `op3.py`, `op3_x.py`, `op3.out`, `op3_results.json`. Not blind: CN1 and LC1 known. κ = ½ FITTED. No a₀ in this halo. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

| run | Υ (A/B) | rms (A/B) | groups Z |
|---|---|---|---|
| no contraction, frozen map (K1 = ZN2 A1) | 0.84 / 0.81 | 0.0829 / 0.0799 | +2.08 |
| **f_Q 0.872, frozen map (PRIMARY)** | **0.44 / 0.41 FAIL** | **0.0726 / 0.0710** | **+2.08** |
| f_Q 1, frozen map | 0.39 / 0.38 | 0.0731 / 0.0719 | +2.08 |
| f_Q 0.872, FC1 map | 0.39 / 0.37 | 0.0711 / 0.0701 | +1.91 |

Line: Υ 0.50–0.80, rms ≤ 0.110. Per the criteria, clusters were **not** contracted or graded, so OP2's cluster read stays uncontracted. Groups aren't contracted (as X39, CN1). My expectation was 0.45–0.55 on the frozen map: 0.44 is just below.

**By V_flat, background A, Υ / ΔV at Υ 0.50, 2–4 R_d (km/s):**
| V_flat | n | no contraction | f_Q 0.872 |
|---|---|---|---|
| 20–60 | 13 | 1.20 / −8.3 | **0.55 / −3.4** |
| 60–100 | 35 | 1.20 / −8.9 | **0.69 / −1.9** |
| 100–150 | 23 | 0.97 / −17.5 | **0.57 / −3.7** |
| 150–200 | 25 | 0.57 / −7.0 | **0.32 / +22.1** |
| 200–250 | 18 | 0.67 / −22.1 | **0.40 / +12.6** |
| 250–400 | 10 | 0.78 / −49.3 | **0.53 / −0.9** |

## How this reads
- **For it:** with no parameter, four of six bins land near Υ 0.5–0.7 and ΔV near 0, and rms improves. The 250–400 shortfall (−49), open on every rule, closes. The Υ pile-up at the cap in dwarfs goes.
- **Against it:** that median fails, and it fails where the input is measured: LC1's f_Q is from 10¹², and 150–250 km/s is where it over-masses. At 0.32 the fit is at the grid's low end. No mechanism here reduces contraction in those galaxies only. CM1 and SH1 found outflows reach only with coupling near 1 and bursts.
- **Carried assumption:** dwarfs and the largest galaxies use a number measured at one mass, from a smooth disc with steady growth; no feedback. High-mass gain may partly reflect bulges, which LC1's disc doesn't test.
- This doesn't touch the Local Group: r₁₂ in dispersion-supported dwarfs with few baryons doesn't contract (OP1 stands).

## Checks
K1 f_Q 0: Υ 0.84 / 0.81, rms 0.0829 / 0.0799 against ZN2 A1's 0.0829 / 0.0800. K2 `contract` is X39's unchanged code, already checked there and in CN1; not rerun separately here, a deviation. MUTATE M_b × 2: Υ 0.33 / 0.31, BITES.
