# CFG810 FROZEN CRITERIA: rule H-EX at GALAXY scale on KiDS-1000 isolated lensing (committed before any script)

**Question.** CFG804 put the catchment supply into the law (edge at 5.364 N M_b). CFG805 added the framework's two-halo term
(all-radii Δχ² edge − no-edge narrowed +149 to +11; heavy bins carry the misfit: inner over-predicted, 0.2–1.4 Mpc under-predicted).
Rule H-EX (CFG809) says something different about the same baryons. Retained baryons tether only their own cold share through
the law, and the EXPELLED share is free collisionless mass. Does H-EX, applied to galaxies, fit KiDS better than the CFG804/805 edge model?

**Model (per mass bin, trial log M_b,gal).**
1. Law profile of the galaxy's own baryons truncated at the retained-share edge, s = r/r_M = 5.84 (N = 1 case of CFG804
   edge_of; this is the CFG801 settled edge). Same `profile()` as CFG804.
2. Free expelled share, in units of M_b,gal: m_f = 5.364 (N − 1), with N = 1/f_ret from the CFG804 census fixed point
   (CFG416 fret_of, N is a function of M_b, not a parameter).
3. Placement of the free share: **DECLARED BRACKET, not Method A.** CFG637 Method A (cfg637_lib.derive with an InfallEX cap)
   needs per-system placed cluster profiles (CFG652 machinery) and a multi-minute run per trial mass; with the mass profiled on a
   250-point grid per bin it is not feasible. Primary placement: an isothermal sphere rho ∝ r^-2 from 0 to the catchment r_ta,
   with r_ta = CFG637 single-shell `r_ta_single(M_ta, a_obs = 1/(1+0.2562))`, M_ta = M_b/(f_ret f_b) from the same fixed point.
   MUTATE placement: uniform sphere to r_ta. These bracket concentrated and flat; Method A at galaxy scale remains undone and any
   PASS/BETTER is therefore conditional on the placement.
4. Two-halo term: CFG805's T1x P_grav template, b profiled per bin (4 free b, same freedom as the comparators). Exclusion radius
   of the template = the bin's r_ta (the free mass extends to r_ta, so the matter inside it is already counted), evaluated at the
   CFG805 starting masses (10.14/10.46/10.70/10.89) and fixed during the fit.
5. Mass profiled per bin exactly as in CFG804/805 (grid 9.5–12.0 step 0.01, 4 sweeps). Full covariance; primary R ≤ 0.31 Mpc;
   all radii (to 2.6 Mpc) is the headline for classes, as in CFG805.

**Comparators.** B+2h and D_der+2h are recomputed here with CFG805's own template/solver and must match cfg805_results.json (K1).

**Classes (all radii; χ² difference vs B+2h = Δ; D_der+2h reference Δ_D = +11.1).**
- **BETTER**: Δ ≤ 4 AND χ²(H-EX+2h) ≤ χ²(D_der+2h) − 4.
- **PARTIAL (added, stated before running)**: χ²(H-EX+2h) ≤ χ²(D_der+2h) − 4 but Δ > 4.
- **SAME**: |χ²(H-EX+2h) − χ²(D_der+2h)| < 4.
- **WORSE**: χ²(H-EX+2h) ≥ χ²(D_der+2h) + 4.
The absolute χ² is also reported with its p-value. The poor absolute fit of every model (χ² ≈ 160 on 52 dof) is not the
object here; a BETTER class does not close it.

**Controls.**
- K1: B+2h and D_der+2h χ² within 0.5 of cfg805_results.json (all radii).
- K2: free share set to 0, no two-halo term, reproduces the CFG801 edge model: χ²(D, N=1) within 0.5 of cfg804_results_MUTATE.json
  (all radii and primary).
- MUTATE: uniform placement (separate outputs). If MUTATE gives the same class as primary the placement does not matter; if it
  differs the class is placement-conditional, and that is reported.

**Both footings are not run here:** canonical a0 = 9.3603e-11 only (CFG804 convention). Alt footing is a separate flag `alt`.

kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed.
