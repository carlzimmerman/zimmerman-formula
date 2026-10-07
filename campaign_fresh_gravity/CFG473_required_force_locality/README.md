# CFG473: the force needed to hold an isothermal cold fluid at the law's target is NONLOCAL in y = g_N/a₀ (it flips sign between compact and diffuse baryons)

Criteria committed before the script. Script `cfg473_locality.py` (< 1 s). Units G = a₀ = M_b = 1; κ = ½ fitted. No DM particle; the cold mass is still required.

The fluid sits exactly at the target with σ² = V_f²/2 (the BTFR-fixed value that makes the deep regime an exact isothermal sphere, CFG472). The extra radial acceleration needed for balance is f = σ² d ln ρ_ph/dr + ν g_N (positive = outward).

| y = g_N/a₀ | a = 0.1 | a = 0.3 | a = 1 | a = 3 | spread |
|---|---|---|---|---|---|
| 0.10 | +0.048 | +0.032 | −0.037 | −2.91 | 1.84 dex, **sign flip** |
| 0.32 | +0.169 | +0.125 | −0.191 | — | 0.13 dex, **sign flip** |
| 1.0 | +0.621 | +0.487 | — | — | 0.056 dex |
| 3.2 | +2.70 | +1.86 | — | — | 0.089 dex |
| 10 | +8.24 | −20.3 | — | — | **sign flip** |

(— means the diffuse profiles never reach that y.)

**Verdict: NONLOCAL** (frozen rule: a sign flip across compactness at fixed y).
- The holding force is not a function of the local baryon acceleration alone. It depends on the baryons' global structure: outward for compact (HSB) discs, inward for diffuse (LSB) ones at the same y.
- Read with CFG472: no pressure gives the target, and the extra force a settling mechanism would need is not a local coupling either. That reproduces from a new direction the record's Gap 1 finding: the object the law needs is nonlocal, keyed to the enclosed baryon mass (C(r) = (a₀/4π) M_b(<r)).
- Only for compact discs in the transition (y ≈ 0.3–3) is the force roughly universal (0.06–0.13 dex).

**Controls.**
- **K1 FAILED as frozen:** the deep-regime f/(ν g_N) at r ≥ 30 r_M is 0.0166 against the 1% tolerance. The residual is ν_mono's subleading term (ν ≈ y^−½ + ½), so f → 0 only asymptotically. The tolerance was mis-specified and the physics is unaffected. The main run exits 1 because of K1.
- K2 PASS (d ln ρ_ph/dr = −2/r to 3e-4).
- **MUTATE** (σ² ×2): the deep-regime f becomes ~100% of ν g_N, so K1 fails as designed (exit 1).
