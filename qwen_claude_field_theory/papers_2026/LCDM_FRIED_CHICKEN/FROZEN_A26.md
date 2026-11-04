# FROZEN A26: tie gates on the full tuned recipe R11b

Frozen before any A26 number. Script `scripts/recipe28.py`, output `scripts/recipe28.out`, checkpoint `scripts/recipe28.json`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Only number seen before freezing: a timing test (one R11b evaluation over 171 galaxies takes about 0.02 s). Known from the record: R11b at K11B has E1 0.0275 (A4, `recipe5.out`; A16 start line, `recipe18.out`).

## Question

So far the tie gates G1 to G5 (A13) were applied to analytic halo scales. Here they are applied to the complete 14-knob recipe R11b (A3, `recipe18.py` gal3 with no N blocks), knobs frozen at K11B = [-.512, .363, -.142, -.6, -.988, -.44, .051, -.139, .8, .6, 1., -.416, -.33, .15]. Does the tuned recipe, rebuilt in another cosmology or at another redshift, move its effective acceleration scale as a = kappa c sqrt(G rho_DE)? If not, what is the least added dependence that makes it?

## The recipe and what cosmology touches

Base cosmology = lib.py: flat, H0 67.4, Om0 0.315, Ob0 0.0493, sigma8 0.811, ns 0.965, no radiation; OL = 0.685, rho_DE0 = OL rho_crit0. Baryons, radii, Upsilon (0.5/0.7), M_*, M_b, R_d, gas fraction and surface density are the SPARC ones and never change. The recipe's halo depends on cosmology and z only through three places, and nothing else is changed:
1. R200 from rho_crit(z) of that cosmology (Einasto alpha 0.16, the ein2 of recipe18).
2. c(M, z) from colossus Diemer19 in that cosmology (masses passed in Msun/h of its own h), times the frozen cnorm and cslope terms of cflat.
3. M200 from the SHMR: footing A holds the K11B SHMR (m200k) fixed; footing B re-matches by abundance matching (below).
f_b = M_b/M200 (capped 0.5) as in R11b, so the cosmic baryon fraction does not enter. All feedback, core and contraction forms and knobs are frozen.

Effective a of a recipe row = lib.fit_a(all g_b, all recipe g) pooled over the 3373 points (bounded log a in [-12, -8]). Shape fidelity of a row, S = rms of log g_recipe - log law(g_b, a_fit) over all points (reported every row).

## (a) Cosmology rows, G2

rho_DE scaled by f in {0.5, 0.71, 1, 1.41, 2} on two cosmology footings:
- C1 physical (primary): physical omega_m = 0.315 h0^2 and omega_b = 0.0493 h0^2 (h0 = 0.674) held fixed, omega_DE = f 0.685 h0^2, flat, so h = sqrt(omega_m + omega_DE), Om0 = omega_m/h^2, Ob0 = omega_b/h^2. Primordial amplitude held fixed: sigma8 of each cosmology is chosen so that sigma(R, z = 30) at the same physical radius R = 8/h0 Mpc equals the base value (colossus Eisenstein-Hu transfer depends on omega_m, omega_b, so the early spectrum is the same; only late growth and h differ). ns fixed.
- C2 fractions (disclosed second footing): flat, Om0 0.315, Ob0 0.0493, sigma8 0.811 held fixed, H0 = 67.4 sqrt(f). So rho_m and rho_b scale with rho_DE by the same f; physical rho_m is not held.
SHMR footings: A fixed SHMR; B abundance matching at a fixed stellar mass function in physical units: cumulative n(>M200) from colossus Tinker08 (mdef 200c, z 0) on log M 8 to 16.5 Msun in physical Mpc^-3 for each cosmology; a galaxy's base halo M_base = m200k(M_*, K11B) maps to M_new with n_new(>M_new) = n_base(>M_base). Masses clipped to the grid are counted and reported.
G2: least-squares slope of ln a_fit against ln(rho_DE/rho_DE0) over the five rows, 0.50 +- 0.05. Reported on all four footings C1-A (primary), C1-B, C2-A, C2-B, with pairwise slopes.
G1: kappa_eff = a_fit(base)/(c sqrt(G rho_DE0)) within 0.05 dex of 0.5. Stated in advance: this passes by construction, because R11b was tuned to the law with A0 = 0.5 c sqrt(G rho_DE0) in this cosmology; it is not evidence.

## (b) Redshift rows, G3

Base cosmology, same SPARC baryons in halos at z = 1, 1.5, 2.33: R200 at rho_crit(z), Diemer19 c(M, z), K11B knobs frozen.
- Bz (primary): Moster et al. 2013 SHMR z-terms added on top of the K11B offsets, with zeta = z/(1+z): log M1 = 11.59 + dm + 1.195 zeta; N = (0.0351 - 0.0247 zeta) 10^dn; beta = 1.376 + db - 0.826 zeta; gamma = 0.608 + dg + 0.329 zeta. Coefficients from memory, flagged; mass definition taken as 200c as in lib.py.
- Az (disclosed): SHMR held at z = 0, only R200(z) and c(M, z) move.
G3: a(z)/a(0) inside [0.76, 1.03], [0.71, 1.12], [0.33, 1.21] at z 1, 1.5, 2.33.

## G4, G5

G4: per-galaxy effective a_i = fit_a on each galaxy's own R11b curve (base cosmology, z = 0); rms of log a_i over galaxies with log M200 (K11B SHMR) in [11, 12.5] <= 0.1 dex. Also reported over all 171, the median, and how many a_i sit at a fit bound.
G5: the recipe's scale is halo gravity at the measured radii, so it is operative by definition (as A13 T3, T4).

## (c) Reverse engineering: least added dependence

Five knob families, each given one multiplicative power of X = V/V0, V in {rho_DE, H}:
- SHMR: N -> N X^p (star-formation efficiency).
- FB: core strength epsilon (e of R11b) -> e X^p.
- CORE: core size eta -> eta X^p.
- CONTR: contraction f -> clip(f X^p, -1, 1).
- CONC: c -> c X^p.
Lambda is rho_DE up to constants, so it is not a separate variable. In the z rows rho_DE is constant (Lambda), X_rhoDE = 1; X_H = H(z)/H0_base. In the cosmology rows X_rhoDE = f, X_H = H0/H0_base. At the base (f = 1, z = 0) every X = 1, so E1 to E3, G1 and G4 are unchanged by construction: "keeping E1 near 0.0275" holds automatically and is not a test. The shape tolerance that is a test: S of every row <= S_base + 0.005 dex.
Fit on the primary footings (C1-A cosmology rows, Bz redshift rows), objective J = ((s - 0.5)/0.05)^2 + sum_z (log10 r_z/0.05)^2, r_z = a(z)/a(0) (target 1, the tie for constant rho_DE). Exponents bounded [-5, 5]; at-bound reported.
- c1: each of the 10 single options (5 families x 2 variables), one exponent.
- c2: if no single passes G2, G3 and S, every pair of options from distinct families (40 pairs), Nelder-Mead from 0, max 200 evaluations.
- c3: only if no pair passes, the five best pairs extended by each remaining distinct-family option (3 exponents).
A solution passes if G2 (primary), G3 (primary) and S hold. The minimal solution is the passing one with fewest exponents (ties broken by J). For it: exponents counted; G2 reported on the three untuned footings; holdout: exponents refitted with a from GS[::2] only, then G2 and G3 read from GS[1::2] (same tolerances).
Classification, fixed now: any exponent on rho_DE (or Lambda) is a hand term by the A10 definition. An exponent on H uses a native LCDM variable, but the value is fitted; it is called a named LCDM process only if a known process scales that knob with H at that sign and roughly that size (named from memory, provisional); otherwise it is a fitted H term with no named process.

## Expected in advance

G1 passes (by construction). G2 fails on C1 (slope below 0.5: the halo at fixed M only tightens through h and late growth) and likely on C2 too, other side (all densities move together, slope near or above 1); A and B differ. G3 fails on Bz, a rising past 1.21 by z 2.33 (denser, more massive halos at fixed M_*, as A15 U1 1.49); Az also rises. G4 lean fail (0.1 to 0.2 dex). (c): no single exponent passes both G2 and G3; the minimal solution needs two exponents, at least one on rho_DE (a hand term); an H exponent alone cannot fix C1's slope and z together.

## RESULTS (written after the run; criteria above unchanged)

Runtime 1257 s, peak 53 MB, single thread. Line numbers refer to `scripts/recipe28.out`.

Deviations: (1) the first launch stopped with a NameError (recipe18's BL table was not loaded) before any gate number was printed; only the environment lines (h, Om0, sigma8 per cosmology) had appeared. The exec slice was widened and the run restarted; no wrong output exists to keep. (2) No bug found after the run. Control (l.13): the rebuilt recipe reproduces recipe18 gal3 at K11B to 0 dex, and the C1 f = 1 cosmology reproduces the base c grid exactly; base E1 0.0275 (l.16).

- G1 PASS by construction (l.19): a_fit 9.306e-11 = 0.994 A0, kappa_eff 0.497.
- G2 FAIL on all four footings (l.22-25): slope +0.254 C1-A (primary), +0.187 C1-B, +0.869 C2-A, +1.453 C2-B. Physical-density footing gives about half the tie's slope, fixed-fractions footing about 1.7 to 2.9 times it. Abundance matching moves the slope away from 0.5 on both. Shape S stays near base on C1 (0.029) but degrades on C2-B (0.059).
- G3 FAIL (l.28-29): Bz a(z)/a(0) 1.93, 2.67, 4.55 at z 1, 1.5, 2.33; Az (SHMR held at z 0) 1.48, 1.93, 3.02. Larger than A15 U1's 1.49 for the central acceleration because in the deep regime the fitted a goes roughly as the square of the halo acceleration. Curves also stop being law-shaped: S 0.051 to 0.084 (Bz).
- G4 PASS (l.31), against the expectation: per-galaxy a_i over log M200 11-12.5 (120 galaxies) rms 0.047 dex, median 0.988 A0; all 171 rms 0.053; none at a fit bound. This is the tuning showing through (R11b was fitted to the law with one A0), not a native constant.
- G5 PASS by definition.
- Verdict on (a, b): the tuned recipe does NOT carry the tie. Its scale is a0 today in this cosmology because it was tuned there; moved in rho_DE it follows the halo, not sqrt(rho_DE), and moved in z it rises 3 to 4.5 times.

(c) Reverse engineering (l.33-120). No solution passes G2, G3 and S together within the frozen search (1, 2 and 3 exponents; l.120). S is the blocker: every z-row solution leaves the high-z curves 0.05 to 0.17 dex off the law's shape (base 0.0275, tolerance 0.0325), so the scale can be dialled but the curve is not the law's curve at z.
- Singles (c1): any one rho_DE exponent sets the slope to 0.5 (e.g. CONC x rho_DE^+0.248, FB x rho_DE^-0.517) but cannot touch z (rho_DE is constant for Lambda); no H exponent alone reaches the slope (best +0.10) or the band.
- On G2 and G3 alone (S ignored, a read, not the frozen pass), two exponents suffice: one on rho_DE plus concentration x H^-1.509 (l.54: e.g. SHMR x rho_DE^-2.649, slope 0.500, a(z)/a(0) 0.90, 0.94, 1.13). Three exponents bring a(z)/a(0) to 1.01, 0.98, 1.01 (l.94). In every passing-on-G2 solution, at least one exponent is on rho_DE: a hand term by the A10 definition. No H-only combination reaches slope 0.5 (best +0.43 with CONTR at bound).
- The H exponents are fitted values: core size x H^+3.3 and concentration x H^-1.5. Diemer19 c(M, z) already carries the LCDM z dependence, so an extra H^-1.5 on c is not a named process; a core growing as H^3.3 has no named LCDM process (from memory, provisional). Count: 2 to 3 added exponents on top of 14 knobs, at least 1 hand term, and still failing S.

Expected outcomes confirmed: G2 fails (C1 below, C2 above), G3 fails, the minimal G2+G3 fix needs a rho_DE hand term. Not expected: G4 passes; S fails every solution.

Provisional: Moster et al. 2013 z coefficients and its mass definition (from memory); the named-process judgement (from memory). No web look-ups, no downloads.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
