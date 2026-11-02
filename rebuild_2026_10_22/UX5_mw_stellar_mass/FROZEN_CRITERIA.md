# UX5_mw_stellar_mass: frozen criteria

Committed alone, before any script or number of this lane. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, both reported, never pooled. Reinstates nothing; the cold sector stays retired. No cold-sector term anywhere here.

**Not blind.** Read before this freeze: LW1 README and lw1_mw.py, lw1_mw.out; X5 README and x5_lib.py; P4 solver and T4 block; OD1 README; UL1 README, ul1.out in part, ul1_est.out, ul1_core.py, ul1_grade.py; SP3 and UR3 READMEs. So I know: form A gate results on the 175 cells, K(R0) 76.7+ for passing cells, the law's UL1 bins and Z's, the estimator tables. From those Z's I estimated by hand that a constant offset near +0.21 dex nearly passes GSWLC's level gate. I have not computed QUMOND, the widened box, or any D/i refit.

**Premise correction, on record before running:** LW1's MW form A is already a full 2D axisymmetric AQUAL solve with thin disc, thick disc, bulge, HI and H2. It isn't one-zone; DiskMass is. What hasn't been done: (a) a real QUMOND solve, since the law's nu gives two different modified Poisson equations and has no action to choose; (b) varying the vertical structure, which X5 held at McMillan17's; (c) grid convergence of K at 1.1 kpc.

## Part 1. Vertical force
nu(y) = 1/2 + sqrt(1/4 + 1/y); mu = x/(1+x), its inverse.
- **Form A:** div[mu(|grad Phi|) grad Phi] = 4 pi rho. P4's solver, L* = 0.
- **Form Q:** lap Phi = div[nu(|grad Phi_N|) grad Phi_N], lap Phi_N = 4 pi rho, same grid and face fluxes.
- **Form R:** LW1's round rule, carried for comparison, on Newton. No field equation.

Boxes. **B175:** X5's 175 cells. **BV:** B175 crossed with h_thin {0.25, 0.30, 0.35}, h_thick {0.72, 0.90, 1.08} kpc, thick share of the stellar column at R0 {0.12, 0.26, 0.35}, thick and thin R_d tied. Ranges: Bland-Hawthorn & Gerhard about +-1 sigma on heights (PROVISIONAL, from memory); the 0.12 and 0.35 shares bracket their 12 % and McMillan's value. Sigma_b(R0) is held per cell. **BV2:** thick R_d fixed 2.0 kpc, same heights and shares, R_d grid {2.27, 2.60, 2.93}. Form A on BV may be run on the subset Sigma_b {40.3, 43.7, 47.1}, M_bb {1.64, 1.88, 2.12}, R_d {1.93, 2.27, 2.60, 2.93}; stated as a subset if so. Form Q and R on all. Gas held at McMillan17's.

Gate, unchanged: UR3's and LW1's classify: L1 v_c, L2a chi2_Kz <= 67.459, L2b |K(R0) - 66.4| <= 4.4, L3 Ou chi2 <= 59.89; classes FEASIBLE IN PRIORS (R_d and M* tags), FEASIBLE (WIDE PRIORS ONLY), V+K ONLY, INFEASIBLE. Line never moved. Reported beside it, no class change: **strict** count, additionally |h - 2.72| <= 0.30.

**Part 1 labels, per form, per footing, per box:** the class itself. **K_z FAILURE SURVIVES** for a form if B175 and BV both have no cell passing L1 + L2a + L2b in priors. **K_z FAILURE REMOVED BY FORM** if Q passes in priors on B175. **REMOVED ONLY BY STRUCTURE** if in priors only on BV or BV2. Any pass gets the same stress as a fail: convergence, a0 x 1.5, count, box-corner position, strict.

Checks: Q1 spherical Plummer, form Q and A against g = nu(gN) gN, <= 1 % at 1-30 scale radii. Q2 Kuzmin disc, thin sheet: both forms have exact field nu(gN) gN off the plane (Brada and Milgrom); K at z 1.1, R 4-12 kpc within 2 %. Q3 form A reproduces LW1's stored K, v_c for all cells, relative 1e-6. Q4 Newton McMillan 177.092, 61.889. Q5 convergence: doubled r and theta resolution on McMillan and the best cell per form; K, v_c moves stated, and if |dK| > 1 the class is tagged [GRID-DEPENDENT].
MUTATE: Q with nu = 1 must return Newton and fail Q1, Q2; a0 x 1.5 must move K. Twin outputs separate.

## Part 2. Upsilon at 60-150 km/s
Gate unchanged: UL1's level and shape, 5 bins, its h including 0.04 pad. Law rows from UL1, reproduced by own code against stored bins (P1, tolerance 1e-6; a difference is reported, not patched).

**(a) Constant offset delta in estimator mass, all bins.** Find the range of delta passing level, per estimator, per footing, and whether shape passes. Declared IMF scale, PROVISIONAL from memory: Chabrier to Kroupa +0.03, diet Salpeter +0.09, Salpeter +0.24 dex.
**(b) Differential.** Required: d(60-150) minus d(150-250), dex, per estimator. On-disk budget: variation across bins of GSWLC - Taylor, with its sign; dependence of the estimators on axis ratio and distance at fixed V. Web literature may be read for SPS terms, tagged PROVISIONAL, with direction stated.
**(c) Denominator.** L_W1/L_3.6 on the SPARC matches: what ratio would be needed, what's measured. M_X / L[3.6] directly on the matches.
**(d) Bin mapping.** Could a V shift do it; largest estimator value in the table.
**(e) D and i.** Refit the law with per-galaxy D and i free under SPARC's published Gaussian errors (MAP, UL1's statistic plus priors; scaling V_gas, V_disk, V_bul by sqrt(D'/D), R by D'/D, V_obs by sin i / sin i'; L and M_HI move with D^2 as the fit's mass). Note M_X/L_W1 doesn't depend on D. Also the uniform shift in log D, then in i, needed per bin to reach GSWLC, in units of the bin's median published error. i held under 90.
**(f) Gas, reported, no label:** the factor on M_gas that would close the gap.

**Part 2 labels, per footing:**
- **CARRIED BY IMF OFFSET:** level and shape pass on both estimators with one delta <= 0.24 in each.
- **LEVEL ONLY BY OFFSET:** level passes on a delta <= 0.24 for that estimator, shape fails. Stated per estimator.
- **CARRIED BY DIFFERENTIAL SPS:** required differential <= an on-disk or PROVISIONAL literature term of the right sign.
- **CARRIED BY D, i:** MAP refit reaches level at 60-100 and 100-150 against GSWLC within published errors; or uniform shift <= 2 median errors.
- **NOT CARRIED:** none of these. Any label holding only against one estimator says so.
MUTATE: set the law's low bins to the estimator's values, gate must pass level there; double them, must fail. Prior on D, i removed must move U.

## Part 3
For each question, one measurement that would decide it, with what each outcome means. Judgment, labelled as such.

## Reporting
Byte-identical rerun of the read. Every failed check reported. Failures published under these labels. Expectation on record: form Q K_z within a few per cent of form A, failure survives on B175, 65 %; BV reaches in priors for A or Q, 25 %. Part 2: LEVEL ONLY BY OFFSET on GSWLC near Salpeter, not Taylor; shape fails; D, i not carrying, 75 %.
