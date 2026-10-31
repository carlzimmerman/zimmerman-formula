# ZN1_zooms_to_z0: KEYS ONLY [GAS-SCALE-DEPENDENT] [MASS-DEFINITION-DEPENDENT] [NOISE-LIMITED]. One native z = 0 profile with no fitted parameter passes all 15 shear keys on one gas scale; X-COP misses in its inner points, and passes in 38 % of seed draws

Criteria: `FROZEN_CRITERIA.md` (22d690ccf2), `AMENDMENT_A1.md` (b5df0a0a1c), `AMENDMENT_A2.md` (9d7a0e5573, item 7 added before any graded number). `zn1_continue.py`, `zn1_measure.py`, `zn1_def.py`, `zn1_grade.py`, `zn1_boot_tail.py`, `zn1_score.py`. Outputs `zn1.out`, `zn1_results.json`, `zn1_shapes.json`, `zn1_readouts.out`, `zn1_boot.out`, `zn1_score.out`, `zn1_MUTATE.out`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## Frozen grade
Rule: M₂₀₀ from fair share inside R₂₀₀, shape from the zooms at z_obs, cold mass f_c M₂₀₀ m(r/R₂₀₀). No S, η, r₀ or a₀.

| Job | keys | worst key | joint χ²/15, p (BA1, reported) | X-COP mean, rms |
|---|---|---|---|---|
| **f★ 0.034, X-COP's gas** | **15 of 15** | **G-IN-Mall −1.73** | **10.5, 0.79** | −0.070, 0.116 FAIL |
| **f★ 0.0615, X-COP's gas** | **15 of 15** | **G-IN-Mall −1.83** | **9.3, 0.86** | −0.078, 0.121 FAIL |
| f★ 0.034, eRASS1's own gas | 11 of 15 | G-OUT-M3 +4.53 | 38.9, 7e-4 | as above |
| f★ 0.0615, eRASS1's own gas | 12 of 15 | G-OUT-M3 +4.25 | 34.9, 3e-3 | as above |
| f★ 0.034, MA1's budget M₂₀₀ | 7 of 15 | G-OUT-all −3.17 | 37.2, 1e-3 | −0.151, 0.173 FAIL |
| f★ 0.0615, MA1's budget M₂₀₀ | 6 of 15 | G-OUT-all −3.38 | 43.4, 1e-4 | −0.158, 0.178 FAIL |
| f★ 0.034, z = 0 shape for all | 15 of 15 | G-IN-Mall −1.92 | 11.2, 0.74 | −0.070, 0.116 FAIL |
| f★ 0.0615, z = 0 shape for all | 14 of 15 | G-IN-Mall −2.02 | 10.4, 0.79 | −0.078, 0.121 FAIL |

All 15 keys at f★ 0.034, h 0.672: G-IN-all −1.22; G-MID-T1 −0.47, T2 +0.30, T3 −0.04, b +0.25; G-OUT-all −0.68, T1 −0.52, T2 −0.43, T3 −0.20, b +0.48; G-OUT-Mall +1.22, M1 +0.43, M2 +0.54, M3 +1.51; G-IN-Mall −1.73.

X-COP by x (0.1, 0.2, 0.3, 0.5, 0.7 R₅₀₀): **−0.164, −0.104, −0.055, −0.010, −0.016.** The model is too heavy only inside about 0.3 R₅₀₀. By cluster: A1795 −0.029, A2029 −0.040, A2142 −0.147, A2319 −0.131, A644 +0.049, A85 −0.113, ZW1215 −0.077.

**Bootstrap (A2 item 3), 200 draws of the seeds:** KEYS ONLY 124, **Z0 PROFILE PASSES BOTH 75**, F★-DEPENDENT 1. The headline class holds in 62 %, below the 68 % line: **[NOISE-LIMITED].** X-COP mean −0.070 [−0.082, −0.034], rms 0.116 [0.082, 0.131], passing in 38 % of draws. All 15 keys pass in 100 % at f★ 0.034, 98 % at 0.0615. So nine seeds don't decide X-COP. They do decide the keys.

## What the zooms did (reported)
| | M₂₀₀/M nominal | R₂₀₀/r_f | c₂₀₀ (NFW fit to m(x), x 0.05–1) | c_nfw (X48's, over r_vir) | η | slope past R₂₀₀ | M(<r)/M(<r, z_f) at r/r_f 0.1, 0.2, 0.5, 1, 1.5 |
|---|---|---|---|---|---|---|---|
| 10¹⁴, z 0 | 0.683 | 1.120 | 5.94 | 10.35 | 34.1 | 2.65 | 0.975, 1.053, 1.152, 1.185, 1.229 |
| 10¹³, z 0 | 0.718 | 1.277 | 6.47 | 12.20 | 40.3 | 2.68 | 1.040, 1.069, 1.196, 1.196, 1.196 |

- **Late mass mostly lands outside r_f.** The inner profile barely changes after z_f: within scatter at 0.1 r_f, 15–20 % up by r_f. So the core rule's assumption that the inner halo freezes roughly holds.
- **η isn't a constant of the halo.** It's a fit over [r_conv, r_vir], and it rises from 19–25 at z_f to 34–40 at z = 0 only because r_vir grows.
- **The native slope past R₂₀₀ is 2.65–2.68,** steeper than 2.25 (GX1) or NZ1's solved 1.87.

## Scored
**My expectation on record** (X-COP probably passes, G-OUT-M3 most at risk): wrong on both.

**Argon's predictions:** class X-COP ONLY: MISS, it's the reverse. X-COP +0.022, 0.082: MISS (−0.070, 0.116), though 38 % of draws pass. G-OUT-M3 +2.85 [2.35, 3.40]: MISS at +1.51, better than it said. G-OUT-Mall +1.75 [1.35, 2.15]: MISS at +1.22. G-IN-Mall −1.65 [−2.05, −1.35]: HIT at −1.73. c₂₀₀ about 7.25: 5.94 and 6.47. [MASS-DEFINITION-DEPENDENT]: right. Its drop condition is not met.

## The limits, which are large
1. **The whole keys pass depends on SM1's +0.111 dex.** On eRASS1's own gas the same rule fails, G-OUT-M3 +4.53. The offset comes from five clusters that aren't in the lensing sample, median of −0.055 to −0.116, and its use across the sample is an extrapolation. Fair share makes the prediction proportional to the gas mass, so this is the rule's main lever.
2. **The mass definition matters.** MA1's budget M₂₀₀ fails everything, OVER. The native rule works only with M₂₀₀ fair share inside R₂₀₀, which gives M₂₀₀/M_ta 0.29.
3. **That leaves a tail problem.** The zooms hold about 2.2 M₂₀₀ at x_edge, but the grader's M_fair at r_ta is about 3.4 M₂₀₀. The frozen tail closes the gap with γ about −39 (68 % −58, −19) in a narrow shell just inside r_ta. So ρ rises outward there, which isn't physical. Removing the tail altogether (`zn1_notail.py`, post-result) moves no key by more than 0.01, so the keys don't depend on it, but the budget and the native profile don't agree. Either the extrapolated gas to r_ta is too much, or r_ta's closure isn't right. 204 of 1318 cells needed γ outside −40 to 60.
4. **Clamped mass.** Lensing clusters have median lg M₂₀₀ near 14.4 and X-COP's near 14.6–15; the top tag is 13.83. ZN3 runs the 10¹⁵ shape.
5. **Isolated spheres.** No large-scale structure beyond the sphere, so mass stops arriving at the sphere's edge. The zooms evolve all of Ω_m as one fluid; the gas is assigned separately, and f_c is FC1's.
6. **Newtonian, collisionless, no feedback.** No contraction from the BCG, no gas physics.
7. **G-IN-Mall** is the key with a failing cross-shear null, and it's the worst key.
8. **This is clusters only.** ZN2 grades the same profile on SPARC and groups. HS1 and AM1 are galaxy-scale problems this doesn't touch.

## SM1's offset tilted (`zn1_tilt.py`, post-result)
Offset +0.111 ± 0.0625 (13.38 − lg Mgas500) per dex, about ±0.04 dex between M3 and M1, X-COP's gas. Both signs stay 15 of 15 at both f★: G-OUT-M3 +1.16 and +1.84 at f★ 0.034, worst key −1.70 and +1.84. Argon said ±0.35 on that key, and it's ±0.34. A flat offset isn't the weak point; its overall size is.

## Checks
K1 engine |d| 0 (`zn1_k1.out`). K2 sampled NFW: 0.0076 (limit 0.01), R₂₀₀ 0.0041. K3 harness against MA1 |d| 0 (`zn1_k3.out`). K4 N unchanged, R₂₀₀ equation 3.2e-6 on the grader's interpolated profile (the frozen 1e-6 was for the zoom measurement, which is exact). ZK1's K3 stands. MUTATE r × 1.5: X-COP rms +0.038, G-IN-Mall +1.66, BITES. Bootstrap identity draw |d| 0.
