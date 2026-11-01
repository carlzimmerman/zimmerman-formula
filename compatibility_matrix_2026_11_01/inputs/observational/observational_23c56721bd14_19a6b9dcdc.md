# LS1_lstar_analogs: SYSTEMATIC L★ DEFICIT at c_f 4 (both footings). The Milky Way's shortfall is not unique; native converged η largely removes it in SPARC analogs

Criteria: `FROZEN_CRITERIA.md` (7c800267d0), committed before any script or number. Script `ls1_analogs.py`, outputs `ls1.out`,
`ls1_results.json`, MUTATE `ls1_MUTATE.out`. Idea relayed from an external model; its thresholds were frozen unchanged.

## Frozen grade (c_f 4, X73 PRIMARY; 18 analogs, V_flat 200–250, Q ≤ 2, Inc ≥ 30°)
| footing | median Υ | ΔV at Υ 0.50, 2–4 R_d (median, 68 %) | verdict |
|---|---|---|---|
| canonical | 0.71 | −34.7 [−52.2, −7.1] km/s | **SYSTEMATIC L★ DEFICIT** |
| alt | 0.65 | −25.7 [−42.4, −0.6] km/s | **SYSTEMATIC L★ DEFICIT** (SPARC line already fails, X78) |

Control V_flat 100–150: ΔV −6.4 canonical, −0.8 alt.

**Checks.** K2 PASS. MUTATE PASS (halo × 0.5: ΔV −50.3 / −46.2). **K1 as coded (d == 0) prints FAIL: max |d| 1.4e-17**, floating-point
noise, not a physics difference; recorded rather than re-coded.

## Reported, post-result, not graded: `ls1_posthoc.py` → `ls1_posthoc.json`
Median Υ / ΔV (km/s) by V_flat, canonical. Converged = CE1's η(M) interpolated (25.94 / 17.67 / 16.91). Law = simple ν, reported kernel only.
| V_flat | n | c_f 4 | converged η | a₀ law |
|---|---|---|---|---|
| 20–60 | 13 | 0.30 / +3.7 | 0.30 / +3.7 | 0.33 / +2.4 |
| 60–100 | 35 | 0.48 / +2.9 | 0.48 / +2.9 | 0.62 / −2.0 |
| 100–150 | 23 | 0.74 / −6.4 | 0.71 / −5.6 | 0.65 / −6.8 |
| 150–200 | 25 | 0.58 / −12.6 | 0.49 / +1.3 | 0.44 / +5.2 |
| 200–250 | 18 | 0.71 / −34.7 | 0.57 / −7.8 | 0.54 / −12.5 |
| 250–400 | 10 | 0.82 / −65.5 | 0.73 / −51.0 | 0.70 / −40.0 |

Alt: law ΔV −5.0 at 200–250, −34.4 at 250–400; converged as canonical above the floor.

**Reading.**
- c_f 4, the only configuration passing the full grader, is short at L★ by about 20–25 km/s relative to the law. That is the Milky Way's size of miss, at KiDS's mass scale.
- Converged native η removes most of it in the analogs (ΔV −7.8, Υ 0.57), and in the 150–250 bins its Υ is at or above the law's.
- ΔV at 250–400 is large for every model, the law included, so a fixed Υ 0.50 is itself too low or those baryon models are incomplete there. Bulges are not separated.
- The floor-branch bins (V_flat < 100) do not change with η, so CE1's SPARC Υ 0.48 is a sample-median statement set by how many galaxies lie in low-Υ bins. The Υ 0.50 line was not moved here.
- Clusters are unchanged by this: CE1's G-MID-T3 and G-IN-Mall still fail OVER at converged η.

## Milky Way at converged η (`x79_mw.py`, X79_ETAMULT 1.245 → `x79_mw_nativex1.245.out`, reported)
Canonical: best in-prior V_c 216.0 km/s (X79 at ε-cut η: 209.1), K_z 67.3, χ²_Ou 99; McMillan 207.3 (200.1). Still V+K ONLY, no all-four cell; Z ≈ −2.8 in prior. Improved, not a pass. The multiplier also scales 10¹³–10¹⁴, unused for this mass.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
