# X55 ASSUMPTION LEDGER (committed with the criteria, before any script or number)

| # | assumption | source | direction / risk |
|---|---|---|---|
| A1 | Relation log M200 = a + b (log M_b − 10.5), one global line, no intrinsic scatter term | question | a scatter term would widen both regions; EM1 R2 found 0.5 dex per-galaxy scatter is allowed by SPARC |
| A2 | SPARC M_b = 0.5 L[3.6] + 1.33 M_HI (fixed Υ 0.5, helium 1.33) | EM1 | the fitted per-galaxy Υ does not enter the relation variable |
| A3 | Lens M_b = M★ (LePhare + 0.15 dex) + M_cold (B21 relation); hot CGM in the lensing mass, not in the relation | X53 A3/A6, F2 | ±0.15 dex variant reported; the definitions are not identical (SPARC cold gas = 1.33 M_HI; B21 cold gas relation) |
| A4 | M200 w.r.t. 200 ρ_crit,0 with background A's h for both data sets | X38, X53 | lenses at z ≈ 0.2–0.3 (X53 variant: ~10 in Δχ², no class change) |
| A5 | SPARC: pure a₀/(2πG) floor (X38); KiDS: X43 rule max(floor, η Σ_coll), c_f 4 (X53) | X38, X43, X53 | the rules differ only above 10^12.09 (canonical) / 10^12.43 (alt); SPARC X43-rule variant reported |
| A6 | Sharp truncation at R200 on the KiDS side | X53 | untruncated variant reported (A1: the edge costs ~60 in χ²) |
| A7 | Two-halo term = CFG805 template (T1x P_grav, **ΛCDM-inherited initial conditions**, σ8 low by 3.2 %), b_eff ≥ 0 per bin | CFG805 via X53 | inherited from ΛCDM-based ICs; amplitude absorbed by b_eff; disclosed |
| A8 | **EM1's (a, b) = (11.18, 0.90) was fitted with NFW halos and the Bullock+01 c(M) relation (a ΛCDM concentration–mass relation)** | EM1 | used here only as step 0 and as the reference point; X55's own SPARC fit is Burkert at the floor and uses no c(M) |
| A9 | SPARC uncertainty by galaxy bootstrap (B 1000, seed 55); Gaussian (Mahalanobis) region | this lane | non-Gaussian / edge-hitting bootstraps reported |
| A10 | KiDS regions Birge-scaled by max(1, χ²_min / dof) | this lane | widens KiDS regions (generous to finding one relation); unscaled reported |
| A11 | Graded separation only over nodes passing X38's SPARC line | question ("sensible Υ") | unrestricted n_sep reported |
| A12 | Halo tables on log M200 (0.01 dex) with linear interpolation | this lane | checked by K_TAB (KiDS) and step 0 item 4 (SPARC) |
| A13 | Saturated halos held at M_max (X38 A1) | X38 | counts reported (coordinator) |
| A14 | Isolation leakage proxy: outer data × 0.64 (F2 GAMA/KiDS isolated, g_bar < 3e-14) | F2 committed | crude, reported only |
| A15 | Nothing ΛCDM-derived enters the halo masses: no abundance matching, no SHMR, no c(M) in X55's fits | owner rule | A7 is the only ΛCDM-inherited ingredient in the graded path |
