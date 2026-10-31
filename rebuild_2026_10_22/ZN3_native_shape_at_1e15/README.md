# ZN3_native_shape_at_1e15: Z0 PROFILE PASSES BOTH [GAS-SCALE-DEPENDENT] [MASS-DEFINITION-DEPENDENT]. With native shapes up to the clusters' own mass and no fitted parameter, X-COP and all 15 shear keys pass at both f★ on one gas scale

Criteria: `FROZEN_CRITERIA.md` (02aa9f4c97), `AMENDMENT_A1.md` (8dda1c4d63). Chosen after seeing ZN1, disclosed there. `zn3_def.py`, `zn3_grade.py`, `zn3_measure.py`, `zn3.out`, `zn3_results.json`, `zn3_shapes.json`, `zn3_boot.out`, `zn3_MUTATE.out`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework. Clusters only.

| Job | keys | worst | X-COP mean, rms | joint χ²/15, p (jackknife p), worse h |
|---|---|---|---|---|
| **f★ 0.034, X-COP's gas** | **15 of 15** | **G-OUT-M3 +1.46** | **−0.004, 0.076 PASS** | **9.8, 0.83 (0.57)** |
| **f★ 0.0615, X-COP's gas** | **15 of 15** | **G-IN-Mall −1.33** | **−0.011, 0.076 PASS** | **8.5, 0.90 (0.72)** |
| f★ 0.034, eRASS1's own gas | 11 of 15 | G-OUT-M3 +4.47 | as above | 38.6, 0.001 |
| f★ 0.0615, eRASS1's own gas | 12 of 15 | G-OUT-M3 +4.19 | as above | 34.7, 0.003 |
| f★ 0.034, MA1's budget M₂₀₀ | 7 of 15 | G-OUT-all −3.22 | −0.079, 0.106 FAIL | |
| f★ 0.0615, MA1's budget M₂₀₀ | 6 of 15 | G-OUT-all −3.42 | −0.085, 0.110 FAIL | |
| z = 0 shape for all | 15 of 15 at both f★ | G-OUT-M3 +1.54, G-IN-Mall −1.48 | same | |

X-COP by x, f★ 0.034: −0.057, −0.013, +0.020, +0.028, +0.005 (ZN1 had −0.164 at x 0.1). In its band, model/data 0.993; G-IN-Mall's pred/meas stays above 1, at Z −1.25.

**Bootstrap, 200 draws of seeds at all three masses:** PASSES BOTH 199, F★-DEPENDENT 1. Not noise-limited, so A1's extra seeds aren't triggered.

**Native at 10¹⁵, z = 0:** lg M₂₀₀ 14.75, M₂₀₀/M nominal 0.558, c₂₀₀ 4.43, c_nfw 8.20, slope past R₂₀₀ 2.54.

## Limits, all still open
1. **Everything rests on SM1's +0.111 dex.** On eRASS1's own gas the keys fail, G-OUT-M3 +4.47. Five clusters, none in the lensing sample. The tilt test on ZN1 moved no class; the overall size is the lever.
2. **M₂₀₀ must be fair share inside R₂₀₀.** The budget M₂₀₀ fails. And the grader's M_fair at r_ta exceeds what the zooms hold, closed by a thin shell (γ about −44) that the keys don't feel (ZN1 tested removal, |ΔZ| ≤ 0.01) but which isn't physical.
3. **Chosen after ZN1's miss.** The rule didn't change, but this isn't a blind pass.
4. **Resolution and power:** ng 64 only, isolated spheres. η moved × 1.3 from ng 48 to ng 64. UV1 tests missing power; ng 80 at these masses hasn't run.
5. **Collisionless, gas assigned separately, no feedback or BCG response.** G-IN-Mall's cross-shear null fails.
6. **Clusters only.** Galaxies are a different story: ZN2, HS1, AM1, ND1, KN1.

## Checks
K1 two tags reproduce ZN1 |d| 0 (`zn3_k1.out`). K2 as ZN1. ZK1's K3 stands. MUTATE r × 1.5: X-COP rms +0.148, G-IN-Mall +1.49, BITES. Bootstrap identity draw |d| 0. Footing-free: no a₀ in this rule.
