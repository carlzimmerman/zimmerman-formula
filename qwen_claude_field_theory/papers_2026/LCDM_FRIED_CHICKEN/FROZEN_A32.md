# FROZEN A32: the joint swoop (feedback/halo knobs and dark-energy parameters tuned at once)

Frozen before any A32 number. Script `scripts/recipe34.py`, output `scripts/recipe34.out`, checkpoint `scripts/recipe34.json`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence; failing does not rule LCDM or any dark-energy model out.

Known from the record before freezing (no A32 number seen): A25 Pareto 15-knob point (`recipe27.out`, ckpt S2 k = 15; units dn, dm, dg, le, a2, a3, f0, f1, dc, sc, N2, HD, PG(2), SL; no SIDM) E1 0.0237, E2 0.0532, E3 0.0223, holdout 0.0244; knobs dg, dc, sc at bound. A26 (`recipe28.out`): R11b in LCDM has G2 slope +0.254 (C1-A), a(z)/a(0) 1.93, 2.67, 4.55 (Bz); H exponents alone reach slope +0.43 at best; a rho_DE hand term is needed.

## Question
A rival tunes the feedback/halo recipe AND the dark-energy sector at once, so that the recipe reproduces the law today and its effective a tracks sqrt(rho_DE(z)) of that same dark energy. Does any joint setting pass E1, E2, E3, holdout, G2 and GT together? If not: the trade-off curve (law rms against tracking error), knob count, knobs at bounds, whether the DE parameters land in the DESI-allowed region, and whether the tie comes from LCDM's own knobs without a rho_DE hand term.

## Recipe
- Halo/feedback: the A25 15-knob Pareto point, its own code (recipe27 `gal`, copied into recipe34 with family multipliers added; Einasto alpha 0.16, Blumenthal contraction, tanh core, DC14 shape HD, gas-rich split PG, SHMR low-mass slope SL, N2 concentration with compactness). Warm start = its recorded vector. Control, frozen: at LCDM and zero exponents the recipe34 curves equal recipe27's to < 1e-6 dex, and E1 reproduces 0.0237.
- Dark energy (4 knobs): CPL w(a) = w0 + wa (1 - a); interaction Q = xi(a) H rho_c, xi(a) = xi0 + xi1 (1 - a), xi > 0 = dark matter into dark energy (A20/A31 form). Background: d rho_c/d ln a = -(3 + xi) rho_c, d rho_DE/d ln a = -3 (1 + w) rho_DE + xi rho_c, baryons a^-3, no radiation, flat; today's densities held at the base values (h 0.674, Om0 0.315, Ob0 0.0493), so rho_DE0 is unchanged and only histories move. Perturbations: geodesic dark matter (energy transfer along the dark matter velocity, so the coupling term cancels in delta_c, as A20 Q1), dark energy smooth (no DE perturbations, stated), growth from a = 1e-3 with delta proportional to a, normalised at a = 1e-3 identically in every model (fixed primordial amplitude, the A26 C1 logic; A20 instead fixed sigma8 today, disclosed difference).
- How DE reaches the halos: (1) rho_crit(z) = rho_crit0 E^2(z) of the model sets R200; (2) c(M, z) by the A20 Ludlow-style map (constant C = 400, from memory): the colossus Diemer19 c of the matching LCDM fixes rhobar_s and the LCDM formation z_f; the model keeps the same collapse condition 1/D(z_f) - 1/D(z), and c solves the same identity in the model's rho_crit. At LCDM parameters the map is the identity (control). (3) M200 from the SHMR, as A26.
- Redshift rows (A26 Bz rebuild, frozen): base cosmology, z = 1, 1.5, 2.33, Moster et al. 2013 z-terms on the knobbed SHMR (coefficients from memory, flagged; SL term added as at z = 0), Diemer19 c(M, z) of base LCDM mapped as above, R200 at the model's rho_crit(z); SPARC baryons fixed in z (unphysical, stated).
- Cosmology rows for G2 (A26 C1-A, frozen): physical omega_m, omega_b fixed, omega_DE = f 0.685 h0^2, f in {0.5, 1, 2} (A26 used five values; three here for speed, disclosed), sigma8 set by the early-amplitude match of recipe28; fixed SHMR; the same w0, wa, xi0, xi1 applied in each; Diemer19 of each LCDM f-cosmology from colossus, then the DE map relative to it.
- Effective a of a row = lib.fit_a of pooled recipe g over all 3373 points (or the subset being tuned).
- H-exponent hand-free terms (5 knobs, primary): one exponent per knob family on X_H: SHMR N x X^p, feedback e x X^p, core size eta x X^p, contraction f -> clip(f X^p), concentration c x X^p (A26 families). X_H = H_model(z)/H0 in z rows, h/h0 in cosmology rows, 1 at base. Fitted values on a native LCDM variable; called a named process only if one is known (from memory, provisional).
- Secondary (reported separately): the same plus one rho_DE exponent per family (5 more), X_rho = rho_DE,model(z)/rho_DE0 in z rows, f in cosmology rows. Every rho_DE exponent is a hand term (A10 definition) and is counted.

Knob count: primary 15 + 4 DE + 5 H = 24. Secondary 29, of which 5 are hand terms.

## Bounds (literature from memory, FLAGGED PROVISIONAL)
- Recipe 15 knobs: A25 frozen bounds.
- w0 in [-1.5, -0.3], wa in [-3, 1.5] (wide search box; DESI DR2 combinations put w0 about -0.65 to -0.85 and wa about -0.4 to -1.1, from memory).
- xi0, xi1 in [-0.3, 0.3] (wide; Q proportional to H rho_c is usually bounded at |xi| of order 1e-3 to 1e-2 by CMB+BAO, from memory). |xi(a)| <= 0.01 over z <= 2.33 reported as "plausible coupling".
- H exponents, rho_DE exponents in [-5, 5] (A26).
- Physical guard, frozen: rho_c and rho_DE > 0 for z <= 10, and rho_DE/rho_m < 0.05 at a = 1e-3 (no early dark energy outside matter domination); a violating point gets a fixed penalty residual 10 per gate term.

## DESI-allowed region (from memory, PROVISIONAL, not looked up)
Gaussian ellipses in (w0, wa), correlation -0.9 assumed for all: DESI DR2 BAO + CMB + Pantheon+ (-0.838, -0.62; 0.055, 0.21), + Union3 (-0.667, -1.09; 0.088, 0.30), + DESY5 (-0.752, -0.86; 0.057, 0.215), DESI + CMB alone (-0.42, -1.75; 0.21, 0.58). Inside if Delta chi^2 <= 6.18 (95 %, 2 dof) for at least one. These DESI fits assume no interaction; with xi != 0 the region is only indicative (stated). LCDM (-1, 0) is reported against the same ellipses.

## Gates (frozen, as the common brief)
E1 rms to law <= 0.02 dex; E2 p95 per-galaxy <= 0.04; E3 worst bin <= 0.02; holdout: tune on GS[::2], unseen GS[1::2] rms to law <= 0.025. G1 kappa_eff = a/(c sqrt(G rho_DE0)) within 0.05 dex of 0.5 (inherited from the target, not evidence). G2 slope of ln a against ln f over f = 0.5, 1, 2 = 0.5 +- 0.05. G3 a(z)/a(0) in [0.76,1.03], [0.71,1.12], [0.33,1.21]. GT |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE0]| <= 0.05 at z 1, 1.5, 2.33, with the model's own rho_DE(z). G4 rms of log a_i over hosts log M200 11-12.5 <= 0.1. G5 halo gravity, by definition. Diagnostics, not gates: shape S at each z row (rms of recipe to law(g_b, a_fit)), H(z)/H_LCDM at z 1, 2.33, |xi| plausibility, DESI Delta chi^2.
JOINT PASS = E1, E2, E3, holdout, G2 and GT all pass at one setting.

## Objective (frozen weights)
Residual vector for least_squares: z = 0 law residuals divided by 0.02 sqrt(N) (sums to (E1/0.02)^2), plus lambda (s - 0.5)/0.05, plus lambda GT_z/0.05 for the three z. Primary lambda = 1.

## Search stages (frozen)
- S0 control: warm 15-knob point at LCDM, zero exponents; graded fully.
- S1 primary joint (24 knobs), multi-start: warm; warm with DE at the DESY5 centre; 4 starts with recipe knobs warm and the 9 DE/H knobs Latin hypercube (scipy qmc, seed 34). least_squares trf, x_scale 'jac', diff_step 0.02, max_nfev 40 per start. Best by cost.
- S2 trade-off curve: from S1 best, lambda in {0, 0.1, 0.3, 3, 10}, max_nfev 25 each, chained; plus S1 at lambda 1. Report E1 against max |GT| and |s - 0.5|.
- S3 DESI-constrained: S1 with (w0, wa) bounded to the DESY5 ellipse's 2-sigma box (w0 [-0.866, -0.638], wa [-1.29, -0.43]) and |xi0|, |xi1| <= 0.01, from S1 best clipped and from the DESY5 centre, max_nfev 40.
- S4 secondary with rho_DE hand terms (29 knobs), from S1 best, max_nfev 40.
- Holdout for S1 best and S4 best: tune on GS[::2] with the full objective (a, G2, GT computed on the tuned half) from the warm start (clean, gated) for max_nfev 30; grade z = 0 rms to law on GS[1::2]; also G2/GT read on GS[1::2].
- Time budget about 2 hours; checkpoint after every start/stage; restart resumes.

## Expected in advance
S0: G2 slope about +0.25 to +0.4 (A26 C1-A), GT fails at all z (a rises 2 to 4x, rho_DE flat). S1: the DE knobs leave DESI and move to w well above -1 (rho_DE rising into the past, so sqrt(rho_DE(z)) can chase the halo's rising a), or xi large; GT can be approached but G2 stays below 0.45 with H exponents only; E1 stays at about 0.023 or above and E2 fails. No JOINT PASS. S3 (inside DESI): GT fails badly, since DESI-like rho_DE(z)/rho_DE0 stays near 0.6 to 1.1. S4 with hand terms: G2 and GT pass, E1/E2 still fail. So the tie needs a rho_DE hand term, and exactness is not reached.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

Runtime 731 s, single thread, small RSS. Line numbers refer to `scripts/recipe34.out`; post-result diagnostics in `scripts/recipe34_diag.py` / `recipe34_diag.out` (written after reading the run, not gates). Controls pass (l.3, 4, 11): recipe34 reproduces recipe27's curves to 0 dex; own LCDM growth matches colossus to 4e-5; the Ludlow map is the identity at LCDM to 6e-5.

Verdict line (l.161): NO joint setting passes E1-E3, holdout, G2 and GT together.

- S0 control, LCDM, no exponents (l.16-24): E1 0.0237, E2 0.0532, E3 0.0223 (all FAIL, the A25 plateau); G2 slope +0.264; a(z)/a(0) 2.20, 3.16, 5.76; GT +0.34, +0.50, +0.76: FAIL.
- Best primary point found = S3, DESI-constrained (l.126-134): E1 0.0236 FAIL, E2 0.0530 FAIL, E3 0.0226 FAIL; G1 0.497 PASS (inherited); G2 slope +0.500 PASS; GT -0.000, -0.000, -0.001 PASS; G3 FAIL (a(z)/a(0) 1.165, 1.164, 1.144 against upper bounds 1.03, 1.12, 1.21); G4 0.042 PASS. DE w0 -0.691, wa -0.595, xi0 = xi1 = -0.010 (both at the S3 bound; xi(z) reaches -0.017, outside |xi| <= 0.01). DESI: inside only the DESI+CMB-alone ellipse (dchi2 5.3); outside all three SN combinations (10.4, 26.4, 40.5). H exponents (l.130): SHMR +3.02, FB +4.25, CORE +0.12, CONTR +5.00 (at bound), CONC +1.21. Knobs at bound: dc, sc, xi0, xi1, pH_CONTR.
- S1 primary multi-start (l.47-56): best cost 2.12, E1 0.0284, E2 0.0656; G2 +0.494 and GT +0.014, -0.003, -0.002 pass, but with w0 -0.475, wa +0.05, xi(z) -0.04 to -0.07 (far outside DESI, dchi2 43 to 483); a(z)/a(0) 1.83, 2.14, 2.76 tracking rho_DE(z)/rho_DE0 3.1, 4.6, 7.7; H(z) 15-20 % above LCDM. Clean holdout from warm (l.55): unseen 0.0336 FAIL.
- S4 secondary with rho_DE exponents (l.139-148): exponents land at about 0 (|p| <= 0.01); the hand terms are not used. E1 0.0284 FAIL, E2 0.0653 FAIL; G2, GT pass; clean holdout 0.0237 PASS (l.147), but on GS[1::2] GT +0.035 at z 2.33 and slope +0.525.
- Trade-off curve (S2, l.61-119): flat, E1 0.0283-0.0286 and max|GT| 0.014-0.015 for lambda 0 to 10: the S2 chain stayed in S1's basin (see deviations). The informative pair is S0 against S3: shape at z = 0 costs nothing to track (0.0237 against 0.0236), but the cost appears in the curve shape at z (below).

What carries the tie (diag l.13-38). In S3 the H exponents do almost all of it: DE at LCDM with S3's exponents kept gives slope +0.489 and GT +0.08, +0.07, +0.06; DE kept with exponents zeroed gives slope +0.273, GT +0.29 to +0.70. Dropping any one of SHMR, FB, CONTR or CONC exponents breaks G2 or GT (slopes +0.05 to +0.87). By z 2.33 the exponents multiply star-formation efficiency x44, feedback energy x208 and contraction x536 (contraction saturated in 171 of 171 galaxies), c x4.6. The z rows stop being law-shaped: S 0.142, 0.141, 0.131 dex (S0 0.05 to 0.085; z = 0 E1 0.024). So a fitted a tracks sqrt(rho_DE) while the curves at z are 0.13-0.14 dex from the law's shape. Holdout of S3 (diagnostic, leaky start, S3 bounds): unseen E1 0.0245 but slope +0.608 and GT +0.08 to +0.10: the tracking does not carry to unseen galaxies.

Answer to the lane question. With fitted H exponents (no rho_DE written in), the fitted effective a can be made to pass G2 and GT, inside the DESI+CMB-alone region, but only through five fitted H exponents of size 1 to 5 with no named LCDM process (from memory, provisional), at the price of curves at z that are not the law's (S 0.13-0.14), a G3 failure, an interaction at the edge of its bound, and a tracking that fails on held-out galaxies. E1, E2 and E3 never pass. LCDM's own knobs, with no fitted z-scaling, do not produce the tie (S0). This differs from A26, where H exponents alone reached slope +0.43: there the exponents were tested one to three at a time on R11b; here five act jointly, with the 15-knob recipe and DE free.

Deviations and disclosures:
1. S1 did not converge: three of six starts sat on the constant guard penalty (cost 500, zero gradient), and S3, whose bounds lie inside S1's, found a lower cost (1.39 against 2.12). So S1's "best" is a local basin, and the S2 trade-off chain (started from it) only maps that basin; even lambda 0 did not return to 0.0237. The frozen clean holdouts (H1, H4) started from warm and may be similarly trapped. Not rerun.
2. Physical guard: any xi > 0 (dark matter into dark energy) of about 0.005 or more drives rho_DE negative before z 10, as A20 found for w = -1; all accepted points have xi < 0.
3. G2 uses f = 0.5, 1, 2 (A26 used five values), as frozen.
4. FOUND OUTSIDE THIS LANE, not edited: `recipe22.py` (A20) growth equation uses u' = -(1 + dlnH/dlna) u, which should be -(2 + dlnH/dlna) u; its LCDM D(z = 1) is 0.452 against colossus 0.607 (checked before this run). A20's concentration map and its K1/K2 numbers need re-checking.
Provisional: DESI ellipses (centres, widths, correlation -0.9), the |xi| plausibility scale, Moster z coefficients, Ludlow C = 400, the named-process judgement: all from memory, no web look-ups, no downloads.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
