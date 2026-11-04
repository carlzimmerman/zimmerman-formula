# FROZEN A25: the deepest single-recipe knob search (every LCDM block on record, stacked)

Frozen before any A25 number. Script `scripts/recipe27.py`, output `scripts/recipe27.out`, checkpoint `scripts/recipe27_ckpt.json`, SIDM response cache `scripts/recipe27_sidm_table.npz` (regenerable cache, not a result). Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence; failing does not rule LCDM out.

Timing known before freezing (no graded number seen): R11b+N2 evaluation 0.022 s on all 171 galaxies; one A19 SIDM core solve 3.5 ms.

## Question
(i) Does ANY global (one recipe for all galaxies) combination of the LCDM blocks on record reach EXACT: E1 rms to law <= 0.02 dex, E2 p95 per-galaxy <= 0.04, E3 worst 0.5-dex g_b bin (>= 50 points) <= 0.02, holdout (tune GS[::2], unseen GS[1::2]) <= 0.025? (ii) The Pareto curve: best rms to law against number of fitted knobs, and the minimal knob count that is EXACT, if any.

## Recipe (one function of the knobs, applied to every galaxy)
SPARC from lib.load() (171 galaxies, 3373 points, Y 0.5/0.7), target the law's curve, residual log10 g_model - log10 g_law. Base = R11b (A3, `recipe4.py`/`recipe18.py` gal3): SHMR m200k (4), feedback energy e = 10^le (M*/M200/0.01)^a1 Sigma_b^a2 (f_gas/0.5)^a4, n = tanh(e) (4), core size eta = 10^le0 (M*/1e9)^a3 (2), contraction fraction f = f0 + f1 (log M_b - 9.5) clipped to [-1,1] (2), c = Diemer19 x 10^dc (M/1e12)^sc (2). Einasto dark profile, Blumenthal contraction (gal3's iteration), core M -> M tanh(r/(eta 1.75 R_d))^n. Dark mass (1 - f_b), f_b = min(M_b/M200, 0.5). Blocks added (each switchable; "off" value in brackets):
- N1 Einasto alpha = 0.16 + alpha1 log(M200/1e12) [0] (A16).
- N2 c x Sigma_b^s_c, Sigma_b = M_b/R_d^2 in 100 Msun/pc^2 [0] (A16).
- N4 f + f2 log Sigma_b [0] (A16).  N5 eta x Sigma_b^a5 [0] (A16).
- HC coreNFW term (Read, Agertz & Collins 2016, A18 inputs): e -> e + k_q 0.04 t_SF/t_dyn, t_dyn = 2 pi sqrt(r_s^3/(G M_NFW(r_s))), t_SF = 13.8 Gyr [k_q 0].
- HD DC14 shape (Di Cintio et al. 2014, A18 code, strength s interpolating NFW (0) to published (1)): dark mass multiplied by M_DC14(s)/M_NFW at the same M200, c, both normalised at R200 [s 0].
- SI constant-cross-section SIDM isothermal core (A19 solver `core()`, Kaplinghat et al. 2014 style, t = 10 Gyr): dark mass multiplied by M_SIDM/M_NFW at the same M200, c, f_b; knob log10 sigma/m [off]. For speed the fits use a per-galaxy table of ln(M_SIDM/M_NFW) at the measured radii on nodes log M200 = base SHMR value + (-1.0 to +1.6, step 0.2), log c/c_Diemer19 (-1 to +1, step 0.25), log sigma/m (-2 to 2, step 0.5), trilinear, clipped at the table edge (clipped fraction printed). Every graded number of a point with SI on is recomputed with the direct solver (not the table). Control, frozen: table against direct on that point, rms difference <= 0.003 dex, else the table is refined and disclosed.
- AC Gnedin et al. 2004 modified contraction: the Blumenthal condition evaluated at orbit-averaged radii rbar = A_g R200 (r/R200)^w for both dark and baryon mass [off = Blumenthal] (2 knobs).
- PG gas-rich split (f_gas >= 0.5): f0 + Df0_g, le0 + Dle0_g [0, 0] (2).  PB bulge split (any V_bul > 0 in the rotmod file): f0 + Df0_b, le0 + Dle0_b [0, 0] (2).
- SL low-mass SHMR slope break: log M200 + s_low min(log M* - 9, 0) [0] (1).
- SS SHMR scatter sigma (dex in M* at fixed M200), as the Eddington shift of the mean log M200 at fixed M*: Delta = alpha_hmf ln10 sigma^2 / s^2, alpha_hmf = d log(dn/dlnM)/d log M (colossus Tinker08, 200c, z = 0), s = local d log M*/d log M200 of the knobbed SHMR, Delta clipped to [-0.6, 0] [sigma 0] (1). Mean curve at the mean halo, not the mean of curves (stated).
Response blocks HD and SI are applied as multiplicative ratios on top of the Einasto, contraction and tanh core, an approximation (stated); the fit can switch the others off. Full stack: 14 + 14 = 28 knobs.

## Bounds, frozen (literature basis from memory, FLAGGED; my judgement where stated)
Base 14 as R11b (A3, my judgement): dn +-0.54, dm +-0.9, db +-1.2, dg +-0.6, le [-2, 1.48], a1, a2, a4 +-3, le0 +-1, a3 +-1, f0 +-1, f1 +-1, dc +-0.33, sc +-0.15. N1 +-0.1 (Einasto alpha rises about 0.03 per dex, Gao 2008, Dutton & Maccio 2014); N2 +-0.5, N4 +-1, N5 +-1 (A16, judgement); HC k_q [0, 2] (published 1); HD s [0, 1.5] (published 1); SI log sigma/m [-1, 1] cm^2/g (0.1 to 10; galaxy-scale SIDM fits 0.5 to 5, Kaplinghat et al. 2016, Ren et al. 2019); AC w [0.6, 1.0], A_g [0.85, 1.6] (Gnedin 2004: 0.85, 0.8; Gnedin 2011: 1.6, 0.8); PG, PB Df0 +-1, Dle0 +-1 (judgement); SL +-0.3 (low-mass SHMR slopes dlog M*/dlog M 1.4 to 3, Moster, Behroozi, Brook, Garrison-Kimmel); SS sigma [0, 0.3] (0.15 to 0.2 dex at Milky Way mass, larger at dwarf masses).
Widened variant (plausibility cost): A16's W for gamma (+-0.9), cnorm (+-0.5), cslope (+-0.3); every other half-width x1.5 about the frozen centre, keeping physical floors (k_q, s, sigma >= 0; w <= 1.2; A_g >= 0.5); SI [-2, 2]. Plausibility cost = for each knob, distance outside its frozen range in units of the frozen range width; reported as sum, max and the list. Median log M200 shift against the base SHMR reported for every graded point.
"Removed" values (a knob fixed, not counted): the off values above; for base knobs dn, dm, db, dg, a1, a2, a4, a3, f0, f1, dc, sc, le0 = 0 and le = -6 (feedback core off).

## Search, frozen
- S1 full stack, frozen bounds: 9 starts, the warm start (R11b's recorded K11B, blocks at off or small: SI log sigma/m -1, AC at Gnedin 2004) and 8 Latin-hypercube starts (scipy qmc, seed 27); least_squares trf, x_scale 'jac', diff_step 0.02, max_nfev 150 per start. Spread of the best starts reported.
- S2 backward elimination from S1's best down to 0 knobs, removal units = each base knob singly and each added block whole: each candidate removal is re-fitted for 4 evaluations from the current knobs, the 2 best re-fitted for 60, the best kept.
- S3 forward one round from R11b: each block added alone to R11b, re-fitted for 60 (extends A16).
- Pareto set = lowest rms to law at each knob count over S1 to S3.
- S4 widened bounds on the full stack: warm start from S1's best plus 3 Latin-hypercube starts, max_nfev 150.
- S5 equal-galaxy-weight objective on the full stack (each galaxy's residuals weighted 1/sqrt(n_points)), aimed at E2, from S1's best, max_nfev 150; graded with the same pooled gates.
- Fits use the SIDM table; grades use the direct solver.

## Grade for every Pareto point and for S1, S4, S5
- lib.grade E1, E2, E3 and rms to observed; knobs at bound (within 1e-3 of the range); median log M200 shift.
- Holdout, gated (clean): tune on GS[::2] from the frozen-centre vector (removed knobs fixed) for 80 evaluations and from one Latin-hypercube start for 60, keep the lower tuned-set cost, grade GS[1::2] <= 0.025. Reported, not gated: the same tuned from the all-data knobs (leaks all-data information, as A4 noted for A16-style holdouts).
- EXACT only if E1, E2, E3 and the gated holdout all pass.
- Tie gates for the recipe's effective a, a = lib.fit_a of the recipe curve on all points (A13/A15 machinery):
 G1 kappa_eff = a/(c sqrt(G rho_DE)), lib cosmology, within 0.05 dex of 0.5. Known in advance: the target is the law with A0 = 0.49995 c sqrt(G rho_DE), so any recipe close to the law passes G1 by inheritance; G1 is not evidence of a tie.
 G2 knobs fixed, recipe recomputed at the three J cosmologies (OL, H0) = (0.70, 67.4), (0.685, 73), (0.65, 73) (Om0 = 1 - OL, Ob0 0.0493, A13's setc): Diemer19 c, rho_crit, R200 and t_SF from that cosmology, SHMR (in Msun) and baryons fixed; slopes d ln a/d ln rho_DE from the first to each of the other two, both 0.50 +- 0.05.
 G3 knobs fixed, lib cosmology at z = 1, 1.5, 2.33: Diemer19 c(M, z), rho_crit(z), t_SF = age(z), SIDM t = min(10 Gyr, age(z)), M200 fixed per galaxy (halo routes at fixed M, A13/A15), baryons fixed (unphysical, stated); a(z)/a(0) inside [0.76,1.03], [0.71,1.12], [0.33,1.21]. SHMR scatter shift held at z = 0.
 G4 per-galaxy a_i = fit_a(g_b, recipe curve) for galaxies with recipe log M200 in [11, 12.5]: rms of log a_i <= 0.1 dex.
 G5 operative at galaxy radii: halo gravity, passes by definition (A13 convention), stated not graded.
 The recipe ties a to rho_DE natively only if G1 to G4 all pass with no hand term. Each knob is a constant of the recipe and carries no rho_DE, so a G2 pass would itself need checking for coincidence.

## Expected in advance
The full stack improves on A16's 0.0263 to about 0.021 to 0.024; E2 stays above 0.04 (about 0.045 to 0.05) on the same outlier galaxies; NOT EXACT at any knob count. The Pareto curve flattens by about 12 to 16 knobs; most added blocks buy under 0.001 dex each. Widened bounds gain under 0.002 dex at a plausibility cost. The equal-galaxy-weight objective lowers E2 a little and raises E1. G1 and G4 pass by inheritance where the curve is near the law; G2 fails (slope well below 0.5, set by R200 and c moving with rho_crit, not with rho_DE); G3 fails at z 2.33 (halo central accelerations rise at fixed M, as A13 T3). So exactness, if reached, would not bring the tie.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## Run status and disclosures, written during the run (no graded number read yet)
- Control passed: with only the base knobs at K11B this code matches recipe18 gal3 to 0.00e+00 dex (rms to law 0.0275, as A16 records).
- SIDM table built in 1220 s. 46,488 of 193,914 node solves (24 %) are unmatched or failed cores by the A19 criterion (|log mismatch| > 0.03). Their ratios are kept unless non-finite, in which case the ratio is set to 1. Graded points with SI on are recomputed with the direct solver, and that solver's unmatched count is printed.
- Timing: full-stack evaluation 0.034 s in table mode and 1.09 s with the direct solver.
- The run (`recipe27.py`, PID 63978) was still in S1 when this lane handed back. Results go here once it finishes; the checkpoint `recipe27_ckpt.json` lets a restart resume. `recipe27_sidm_table.npz` is a regenerable cache and should not be committed.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
