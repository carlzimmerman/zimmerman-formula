# RG1_native_n_regrade: FROZEN CRITERIA

Written before any script or number from this regrade. Owner's go, 10-31: regrade on the working rule (`OWNER_DECISION_2026-10-31_NO_FLOOR.md`).

**Disclosed first.**
- I have read each source lane's result, and ND1's native LITTLE THINGS and ceiling tables. ZN1's X-COP on its native profile is −0.070 / 0.116. None of these rows has been computed on this rule.
- **A correction to the owner decision file.** I listed HO1 and HO2's SLUGGS as floor-dependent. They are not: all those systems sit on the η branch. What changes there is c_f S9 → native η, Burkert → smooth core, and no switch. Reported as such, not as an effect of removing the floor.
- GD1–GD3 use OS1's Σ ∝ σ^q, not the floor, so they too are rule changes rather than floor removal.

**Rule.** S_cold(M200) = f_c η(M_t) ρ(M_t) Σ_coll(M_t), M_t = M200/f_c, by ND1's `RULE_NAT`: CE1's A4 η, X80's ρ₁₀ 1.128, ρ₁₁ 0.938. Below 1e10 ρ stays at ρ₁₀ and Σ_coll is held below M_t 2e7, as ND1. Clusters: M_t = M_fair + M_b,t, as FC1. Smooth core; r₀ from M(<R200) = M200 (M(<r_ta) = M_fair in clusters), compact root. No switch: route E everywhere. No a₀, so the footings coincide in the halo; where a lane reports both, both are shown.
One table, built once from ND1's code, is read by every part. **K0:** it reproduces ND1's rule S at M_t 1e10…1e14 (51.8, 78.4, 149, 236, 380) within 1 %, and 29.4 at lg M200 9.

## Parts, each on its source lane's own frozen line
- **P1 Local Group (X49):** X49's script, five classes, EM1's M200. REPRODUCED iff |Z| < 2. Primary smooth core; Burkert reported. **K1:** floor + Burkert reproduces X49's class medians within 0.001.
- **P2 Milky Way (GD1, GD2, GD3):** GD3's X5 box, same cells, same lines L1, L2a, L2b, L3, same classes: FEASIBLE IN PRIORS, FEASIBLE (WIDE PRIORS ONLY), V+K ONLY, INFEASIBLE. Background A graded, B reported. McMillan 2017 row reported against Eilers, as GD1. **K2:** OS1's law with q_fS reproduces GD3's class and best D on canonical PRIMARY.
- **P3 SLUGGS (HO2 a):** HO2's source run unmodified up to the grade, with its Step 0 kept. Same classes: PASS, IMPROVES ON X38, FAILS. **K3:** HO2's own Step 0 passes and the CL2 row reproduces HO2's mean.
- **P4 X-COP (HO1 a):** PASS iff |mean Δ| ≤ 0.05 and rms ≤ 0.10, 35 points. **K4:** HO1's Step 0 passes and the CL2 row reproduces.
- **P5 HG2 groups (HO1 b):** PASS iff D_pred lies in measured 95 % [−0.511, −0.076].

**Carried, not rerun:** SPARC, groups, LITTLE THINGS, ceilings, clusters from NF1, X80, ND1, ZN1.

**MUTATE:** S × 0.5 in the table; P1, P2's K check-lines must move. Exit nonzero if unmoved. Jobs: one thread, nice 15, under 1 GB, minutes.

**Word rule.** Each part's own label, plus one line: RG1 ALL HOLD if P1–P5 all pass, otherwise list failures. A failure is a failure of this rule, not a closure. Native inputs carry the source lanes' ledgers; McMillan and Portail baryons stay labelled ΛCDM-PROCESSED per the 10-31 summary, so P2 is not a clean framework verdict. Core-law board tiles get updated from these and the carried rows; the main board stays as is. κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.
