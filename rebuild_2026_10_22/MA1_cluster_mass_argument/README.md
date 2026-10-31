# MA1_cluster_mass_argument: passing the same collapsed mass on all paths moves clusters from the edge to room to spare, frozen label MASS ARGUMENT PASS, but a cluster's own z_obs takes it back

Criteria: `FROZEN_CRITERIA.md` (b22583d196), committed alone before any script or number. Scripts `ma1_grade.py`, `ma1_def.py`, `ma1_tail.py`. Numbers: `ma1.out`, `ma1_results.json`. Stress test: `ma1_zobs.py`, `ma1_zobs.out`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## The bookkeeping point
Σ_coll(M) is defined for the object whose **collapsed** mass today is M (X43's Lacey–Cole half-mass formula; X48's zooms put M/2 at z_f). SPARC and groups pass M200. Since GS1 extended the cluster budget to r_ta, the cluster path has passed M_fair + M_b,t, the mass out to turnaround. Here M₂₀₀ is the model's own total mass inside R₂₀₀, as a fixed point: M₂₀₀/M_ta = 0.50 [0.47, 0.55], so S falls by × 0.857 [0.842, 1.000]. (The criteria say "about 3×". On this profile it's 2×.)

## Frozen verdict, canonical: MASS ARGUMENT PASS, both f★
| Rule | f★ | SPARC Υ (A/B) | groups Z | worst key | G-IN-Mall (h 0.672/0.686) | G-MID-T3 | result |
|---|---|---|---|---|---|---|---|
| **MA1** | 0.034 | 0.51 / 0.50 | +1.62 | G-IN-Mall −1.45 | −1.45 / −1.23 | −1.15 / −0.61 | **PASS** |
| **MA1** | 0.0615 | 0.51 / 0.50 | +1.62 | G-OUT-all −1.55 | −1.50 / −1.26 | −1.35 / −0.80 | **PASS** |
| FC1 | 0.034 | 0.51 / 0.50 | +1.62 | G-IN-Mall −1.95 | −1.95 / −1.64 | −1.71 / −1.13 | PASS |
| FC1 | 0.0615 | 0.51 / 0.50 | +1.62 | G-IN-Mall −2.004 | −2.004 / −1.69 | −1.93 / −1.34 | FAIL |

Alt: FAIL on the SPARC line (Υ 0.44), X78's known failure; its cluster numbers equal canonical's.

## Reported
| Run | f★ 0.034 | f★ 0.0615 |
|---|---|---|
| p16 | PASS, worst −1.32 | PASS, worst −1.48 |
| p84 | FAIL on the SPARC line (0.49), clusters pass, worst −1.72 | same, worst −1.77 |
| **η(10¹³, 10¹⁴) × 1.1144 (A4's guide)** | **PASS, worst −1.80** | **PASS, worst −1.85** |
| η(10¹³, 10¹⁴) × 1.206 (its 68 % upper end) | FAIL, G-IN-Mall −2.07 | FAIL, G-IN-Mall −2.13, G-MID-T3 −2.04 |
| M at 18π² ρ_m, not 200 ρ_c | PASS, worst −1.65 | PASS, worst −1.70 |

The label does not depend on the mass definition. The room is now about × 1.17 where it was × 1.016 (`../FC1_cold_share_native_eta/fc1_a4_expect.out`).

## 🛑 The stress test that takes it back (POST-RESULT, reported only; the frozen verdict stands as frozen)
MA1, like FC1, still treats every cluster as seen at z = 0. Its proper formation epoch follows from its own z_obs: D_f = δ_c / (δ_c/D(z_obs) + ω√ΔS), with R₂₀₀ at 200 ρ_c(z_obs). The clusters have z_obs median 0.22 [0.11, 0.39]. At fixed M that raises S by × 1.26 (median), × 1.51 (p84), × 1.75 (max).

| Run | f★ | result | worst keys |
|---|---|---|---|
| z_obs | 0.034 | **FAIL** | G-IN-Mall −2.33 / −2.00; G-MID-T3 −1.96 |
| z_obs | 0.0615 | **FAIL** | G-IN-Mall −2.40 / −2.05; G-MID-T3 −2.19 |
| z_obs, × 1.1144 | 0.034 | FAIL | G-IN-Mall −2.76 / −2.36; G-MID-T3 −2.35 |
| z_obs, × 1.1144 | 0.0615 | FAIL | G-IN-Mall −2.83 / −2.43; G-MID-T3 −2.59 |

SPARC is at z = 0, so it's unchanged. This omission was in FC1 and every lane before it, so it isn't MA1's alone. **So MA1 fixes one bookkeeping error, and the next one along undoes the gain.** With both applied the rule misses mainly on G-IN-Mall, the shear band with the failing null (IC1 D2), whose excess is out of line with X-COP (XH1). I'm not dropping that key after the fact. η itself may depend on z_obs through peak height, and that isn't measured here.

I went looking for errors that help. This one hurts, and I only found it by attacking the pass. Others could remain in either direction.

## X-COP (reported)
Still FAIL on rms: mean −0.014, rms 0.136 (f★ 0.034); by x +0.205, +0.013, −0.057, −0.102, −0.128. The mean now passes. In the disputed band X-COP has the model at × 1.05. Model M₂₀₀ runs × 1.4–1.6 over X-COP's hydrostatic M₂₀₀ in five of seven clusters. See `../NZ1_zoom_core_radius/` for the shape.

## Checks
K0 switch off reproduces FC1 and XH1, |d| 0. K1 SPARC rms and groups Z unchanged, |d| 0. K2 1304 cells, all converged within 7 iterations, R₂₀₀ equation 6.4e-13. K3 pass. MUTATE argument × 2 moves G-IN-Mall by −0.52 (and lands near FC1's −1.95): bites. RSS 0.71 GB.

## Limits
Post hoc, disclosed. No parameter, but also no derivation of S, η or κ. Cluster η still ng 48; `ma1_grade.py --A4` reruns this once CE1's A4 tables exist. M₂₀₀ comes from the single-tail profile, which is itself too heavy on X-COP.
