# NZ1_zoom_core_radius: r₀ from the zooms passes X-COP's hydrostatic masses with no fitted parameter, and keeps the SPARC line, but under-predicts the shear beyond about 1 Mpc. Frozen label X-COP PASSES, KEYS BREAK

Criteria: `FROZEN_CRITERIA.md` (7b6807445e), committed alone before any script or graded number. Scripts `nz1_grade.py`, `nz1_def.py`, `nz1_bins.py`. Numbers: `nz1.out`, `nz1_results.json`, `nz1_bins.out`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## The rule
S comes from the zooms, and so does r₀: r₀ = r_f/a, with η = (4/3) a²/B(a), so a ≈ 13.3, 10.4, 10.1 at 10¹², 10¹³, 10¹⁴. Budget r₀ runs about × 1.6 larger than that on clusters (`../MA1_cluster_mass_argument/`). Beyond r_f, the fair share to r_ta fills a tail whose slope γ is solved per cluster. Nothing is fitted. M is MA1's M₂₀₀, a hybrid, as the criteria say.

## Frozen verdict: X-COP PASSES, KEYS BREAK
| Run, f★ | X-COP mean | rms | x 0.1 | 0.2 | 0.3 | 0.5 | 0.7 | keys over 2 | groups Z | SPARC Υ |
|---|---|---|---|---|---|---|---|---|---|---|
| **ALL, 0.034** | **+0.047** | **0.087** | +0.100 | +0.006 | +0.012 | +0.052 | +0.064 | G-MID-T2, G-MID-T3, G-OUT-Mall, G-OUT-M3 | +3.98 | 0.52 / 0.52 |
| **ALL, 0.0615** | **+0.042** | **0.085** | +0.100 | +0.002 | +0.007 | +0.044 | +0.056 | G-MID-T3, G-OUT-Mall, G-OUT-M3 | +3.98 | 0.52 / 0.52 |
| CLUSTERS, 0.034 | +0.047 | 0.087 | | | | | | same four | +1.62 | 0.51 / 0.50 |
| CLUSTERS, 0.0615 | +0.042 | 0.085 | | | | | | same three | +1.62 | 0.51 / 0.50 |

Pass line for X-COP: |mean| ≤ 0.05, rms ≤ 0.10. FC1's rms was 0.139, MA1's 0.136, HO1's 0.126.

- **This is the first zero-parameter rule in the record to pass X-COP's line.** CS2's alt OS1 passes it (0.092), but OS1 is normalised to X-COP's own hydrostatic mass. Here no hydrostatic mass enters.
- **It keeps the SPARC line on ALL paths** (rms 0.0691, against 0.0687). L★ is not fixed: ΔV by V_flat at Υ 0.50 is +3.7, +2.9, −10.2, −2.3, −17.1, −53.1, against FC1's +3.7, +2.9, −6.4, −3.8, −16.2, −56.7.
- **The shear beyond about 1 Mpc goes under.** At f★ 0.034, h 0.672: G-OUT-M3 +5.10, G-OUT-Mall +3.06, G-MID-T3 +2.40, G-MID-T2 +1.64 (+2.03 at h 0.686). G-IN-Mall improves to −0.80. This is IB1's trade again, with the same G-OUT-M3 +5.
- **Groups fail under ALL:** Z +3.98, against +1.62.
- Solved γ: median 1.87 [1.73, 2.00] over 1314 cells. Every cell has a tail.

## A4's guide makes X-COP better here
With η at 10¹³ and 10¹⁴ × 1.1144: X-COP mean +0.017, rms 0.076 (f★ 0.034); +0.012, rms 0.075 (f★ 0.0615). The same keys stay over 2, with G-OUT-M3 +5.02 and +4.93. On the single-tail rules a higher η hurts. On this rule it helps.

## How this reads
1. **X-COP and the shear aren't graded at the same radii.** X-COP's line stops at 0.7 R500, under about 1 Mpc. The failing keys are at 0.46–3 Mpc. So this isn't proof that the two data sets contradict each other. It says that the mass beyond r_f isn't where this tail puts it.
2. **What's physically missing.** The zooms stop at z_f with M/2 inside r_f. The mass that arrives after z_f has to end up inside R₂₀₀, only about 1.12 r_f. A single power law out to r_ta can't hold it. That's why this rule can't be self-consistent in M, as the criteria disclosed.
3. **The mutation brackets it.** r₀ × 1.5 gives γ 2.90, keys all pass, SPARC line just fails (0.49), X-COP rms 0.125. r₀ × 1 gives γ 1.87, X-COP passes, keys fail. So the real profile lies between, with γ somewhere between 1.87 and 2.90. Choosing a multiplier in there would be a knob.

## Limits
Hybrid M. Cluster η at ng 48. S at z = 0 on every path, the omission `../MA1_cluster_mass_argument/ma1_zobs.out` exposes. Below 10¹², η and a clamped until X80. Post hoc, disclosed.

## Checks
K0 rule off reproduces MA1, |d| 0. K1 a(η) 7.1e-15, M_c(r_f) = f_c M/2 8.0e-15. K2 M_c(r_ta) 2.1e-13, ρ(r_f) 6.7e-16. K3 CLUSTERS leaves SPARC and groups, |d| 0. Table check: budget r₀ reproduces FC1's 250–400 ΔV, |d| 0. MUTATE r₀ × 1.5 moves X-COP rms by +0.038: bites. RSS 0.72 GB.
