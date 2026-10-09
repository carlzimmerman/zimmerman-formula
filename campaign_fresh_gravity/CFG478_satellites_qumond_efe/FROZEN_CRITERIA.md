# CFG478: does the law as a FORCE WITH the external-field effect really fail the cluster satellites? cm14b re-done with the exact QUMOND phantom in a uniform host field. FROZEN before any script exists

Owner chat 10-08 ("swing both"). κ = ½ fitted; both footings. No DM particle; the retained cold mass is included exactly as cm14b did.

**Why.** cm14b (sonnet55_push/cold_mass/cm14b_sifon_table.py) excluded the host-EFE reading at χ² 99.7/5 using a 1-D shortcut, M = ν((g_N + g_e)/a₀) M_b. Council Session 12 named this the weakest wall of the "box". If force-with-EFE survives, AeST-class relativistic MOND with a₀ ∝ √ρ_DE is a complete-theory candidate again.

**Exact QUMOND enclosed phantom.** For a point-mass satellite (M_b) in a uniform host field g_e:

M_ph(<r) = (1/4πG) ∮_{|x|=r} (ν(|g_N + g_e|/a₀) − 1)(g_N + g_e)·n dA

This is exact in QUMOND, because ρ_ph = ∇·[(ν − 1) g_N,tot]/4πG and the uniform background alone has zero divergence. The satellite is axisymmetric about g_e, so it reduces to a 1-D θ integral at each r. M(<r) = M_b + M_ph(<r) + retained cold (0.13 × 5.364 × M_b, as cm14b).

**Inputs.** cm14b's own parsed Sifón+18 table (5 M★ bins; m_bg with errors; ⟨R_sat⟩), its baryons (M_b = 1.2 M★), its r_bg estimate, and its host (NFW, M₂₀₀ = 6e14, c = 4), with g_e = G M_host(<R_sat)/R_sat². These are imported by re-executing cm14b's parsing block, never editing it.

**Readings.**
- **Q1 (primary):** the exact QUMOND with g_e as cm14b; kernels ν_P2 (cm14b's) and ν_mono; both footings.
- **Q2 (generous bracket, declared):** g_e × 0.5 (host field halved).
- **Q3 (most generous, reported):** g_e × 0.25.

**Verdict** (cm14b's rule; χ² over the 5 bins, 5 dof).
- **FORCE+EFE EXCLUDED (robust)** if p < 0.01 in Q1 and Q2, for both kernels and both footings.
- **SURVIVES** if p > 0.01 in Q1 for any kernel or footing.
- **FRAGILE** if it is excluded in Q1 but survives in Q2.
- Also reported: the boost M(<r_bg)/M_b per bin against what the data need.

**Controls.**
- K1: g_e → 0 reproduces the isolated spherical result M_ph = (ν(g_N/a₀) − 1) M_b to 1e-6.
- K2: the surface integral of the uniform field alone (M_b → 0) is 0 to 1e-10 relative.
- K3: the exact Q1 boost lies between ν_e(1 + L_e) and ν_e as r → large, where L_e = d ln ν / d ln y at y_e (the EFE-dominated limit).

**MUTATE (`--mutate`).** g_e → 0 everywhere (isolated satellites, cm14b's reading A, which fits). The verdict must flip to SURVIVES; exit 1 when it does.
