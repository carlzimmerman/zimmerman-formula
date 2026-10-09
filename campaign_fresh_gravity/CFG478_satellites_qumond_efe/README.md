# CFG478: the law as a FORCE WITH the external-field effect fails the cluster satellites. Robust with the exact QUMOND phantom, even with the host field cut to ¼

Criteria 7bccb9717 (committed before the script). Script `cfg478_qumond_efe.py` (< 1 s). Re-executes cm14b's parsing read-only. κ = ½ fitted; both footings.

The exact QUMOND enclosed phantom of a point-mass satellite in a uniform host field (a surface integral of (ν − 1) g_N,tot) replaces cm14b's 1-D shortcut.

| reading | χ² / 5 (range over kernels ν_P2, ν_mono × footings) | boost M(<r_bg)/M_b | data need |
|---|---|---|---|
| Q1: g_e as cm14b | 94.6 – 106.9 | 1.4 – 1.8 | 10.5 – 20.2 |
| Q2: g_e × ½ | 78.4 – 92.3 | 1.6 – 2.2 | same |
| Q3: g_e × ¼ (most generous) | 61.0 – 74.5 | 2.1 – 2.9 | same |

**Verdict: FORCE+EFE EXCLUDED (robust).** p < 1e-11 everywhere.

**Reading.**
- With the external-field effect, a satellite's phantom is capped near ν_e(1 + L_e/3) ≈ 1.4–1.8× its baryons. The weak-lensing masses need 10–20×, which is what the *isolated* law gives (cm14b reading A, χ² 0.7/5).
- The 1-D shortcut was not the problem: the exact solution is, if anything, smaller than the shortcut.
- Even at a quarter of the host field, which covers a factor-2 underestimate of the 3-D distance or of r_bg, the reading misses by ×4–9.
- So the "box" of council Session 9 keeps this wall. A force-with-EFE theory (AeST-class) is not reopened by this evidence. Satellites keep a phantom as if isolated, which the settling (material) reading explains and a force with an EFE cannot.

**Controls (all PASS).**
- K1: g_e → 0 gives the isolated result to 1e-6.
- K2: the uniform field alone gives zero flux.
- K3: the EFE-limit boost 1.4056 equals linear QUMOND theory ν_e(1 + L_e/3) = 1.4056, inside the analytic bracket.
- MUTATE (g_e → 0): SURVIVES (exit 1), as designed.

**Caveats (inherited from cm14b).**
- The m_bg are Sifón+18's lensing masses inside r_bg, with r_bg estimated from an isothermal match.
- The host is an NFW with M₂₀₀ = 6e14, and satellites are taken at ⟨R_sat⟩ (projected).
- The point-mass satellite is fine at r_bg = 36–149 kpc.
