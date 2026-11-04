# FROZEN A17: wave (fuzzy) dark matter soliton + NFW, recipe19

Frozen before any number was computed. Quarantined experiment, rival language, adopts nothing, never feeds anything outside this folder. kappa = 1/2 FITTED; not theory closed.

## Model
- Halo: M200 from the lib.py Moster SHMR at M_* (m200_of), Diemer19 c (cflat, 200c, z = 0), outer dark density (1 - f_b) NFW, f_b = min(M_b/M200, 0.5), as in lib.
- Soliton (Schive et al. 2014): rho_s(r) = rho_0 / [1 + 0.091 (r/r_c)^2]^8, rho_0 = 0.019 m22^-2 (r_c/kpc)^-4 Msun pc^-3 (the m^-2 r_c^-4 scaling is exact Schrodinger-Poisson scaling).
- Core-halo relation, z = 0: r_c = A x 1.6 kpc / m22 x (M200/1e9 Msun)^(-beta) x (Sigma_b/100 Msun pc^-2)^(-s), Sigma_b = M_b/R_d^2. Schive's form is A = 1, beta = 1/3, s = 0 (M_c proportional to M_h^(1/3)). M200 stands in for Schive's virial mass (difference ~0.1 dex, stated).
- Literature check: the profile form and M_c ~ a^(-1/2) M_h^(1/3) were confirmed by a web search; the coefficients 1.6 kpc and 0.019 Msun/pc^3, and the redshift factor below, are FROM MEMORY, not verified.
- Transition, primary: densities match. r_t = outermost radius (log grid 1e-3 kpc to R200) where rho_s crosses below the (1 - f_b) NFW density. Inside r_t the dark mass is the soliton's; outside, M_s(r_t) + (1 - f_b)[M_NFW(r) - M_NFW(r_t)]. If the soliton never exceeds the NFW density, the halo is pure NFW. Variant (reported for M1 only): the standard r_t = 3 r_c rule with the same assembly (density jump allowed).
- g_total = g_b + G M_dark(r)/r^2, graded by lib.grade.

## Knobs and bounds (fit in these variables)
- M1: log10 m22 in [-1.5, 2]. Scan 36 values, then a bounded 1-D fit. 1 knob.
- M2: M1 + log10 A in [-0.5, 0.5] and beta in [0, 0.7]. 3 knobs.
- M3: M2 + baryon-compactness response s in [-1, 1] (natural: baryons deepen the potential and compress the soliton). 4 knobs.
- M4: M3 + SHMR normalisation dn in [-0.3, 0.3] dex and concentration offset dc in [-0.3, 0.3] dex. 6 knobs. Disclosed as halo knobs beyond the brief's list.
- least_squares on log residuals to the law, warm start from the previous model, max 60 evaluations; for M2-M4 one extra start at Schive's values.

## Gates, every model
- lib.grade E1 rms to law <= 0.02 dex, E2 p95 per-galaxy <= 0.04, E3 worst 0.5-dex bin <= 0.02, all-data tuning.
- Holdout: tune on GS[::2], grade GS[1::2], unseen rms to law <= 0.025 dex.
- Report rms to observed (law: 0.1951), knob count, knobs at bound.
- EXACT only if E1, E2, E3 and holdout all pass.

## Acceleration scale
- The model's own scale: soliton acceleration g_c = G M_s(r_c)/r_c^2 per SPARC galaxy at the fitted knobs. kappa_eff = median g_c/(c sqrt(G rho_DE)) against 0.5 within 0.05 dex; rms of log g_c over the 171 galaxies (one constant needs <= 0.1 dex).
- Evolution at fixed M200: r_c proportional to a^(1/2) (zeta(z)/zeta(0))^(-1/6), zeta = (18 pi^2 + 82 x - 39 x^2)/Omega_m(z), x = Omega_m(z) - 1 (from memory). g_c proportional to r_c^-3 at fixed m (M_s r_c fixed by scaling). Ratio at z = 1, 1.5, 2.33 against [0.76,1.03], [0.71,1.12], [0.33,1.21].
- Dimensional: hbar/m, G alone give no acceleration. With a density, a_q = (hbar/m)^(1/2) (G rho)^(3/4). Report a_q with rho = rho_DE at the fitted m22: FDM contains no rho_DE, so any match is a hand term by definition.

## Expected outcome (stated before running)
- M1 fails E1 (0.07 to 0.12 dex) and E2, E3: the outer halo is the plain SHMR NFW which R1 already puts 0.14 dex from the law; a soliton only changes the inner few kpc. Best m22 near 0.3 to 3, in tension with Lyman-alpha bounds (m22 > ~20, from memory).
- M2 to M4 improve to 0.05 to 0.07 dex and still fail E1, E2 and holdout. Verdict: NOT EXACT.
- g_c scales as M200^(3 beta) m22^2 (as M200 at beta = 1/3): spread > 0.3 dex over SPARC, fails one constant; rises with z (a^(-3/2)), fails the band. a_q exists only with rho_DE put in by hand.

## Results (added after the run; criteria above unchanged)
Output `scripts/recipe19.out` (13.8 s, 78 MB RSS, single thread). No bug found; the pure-NFW limit reproduces R1 base in `recipe.out` (0.1419) exactly, a cross-check.

| model | knobs | E1 rms law | E2 p95 | E3 worst bin | rms obs | holdout unseen | at bound | soliton present |
|---|---|---|---|---|---|---|---|---|
| M1 match | 1 | 0.1494 | 0.2984 | 0.1696 | 0.2491 | 0.1674 | log m22 at upper bound 2 | 171 (tiny) |
| M1 3 r_c | 1 | 0.1492 | 0.2981 | 0.1694 | 0.2489 | - | log m22 at upper bound | - |
| M2 | 3 | 0.1419 | 0.2877 | 0.1613 | 0.2424 | 0.1309 | none | 0/171 |
| M3 | 4 | 0.1419 | 0.2877 | 0.1613 | 0.2423 | 0.1309 | none | 9/171 |
| M4 | 6 | 0.0921 | 0.1811 | 0.0452 | 0.2186 | 0.0944 | none | 0/171 |

- The M1 scan has an interior cored local minimum at log m22 = -0.64 (m22 0.23), rms 0.1735, worse than the bound. The bracketed fit's best value sits at the scan bound (the script's at-bound flag does not cover M1; disclosed here). The M1 holdout used the global bounded fit and landed on the cored local minimum, so its 0.1674 is for m22 0.23.
- M2 to M4: the fit switches the soliton off (r_c large enough that rho_0 ~ r_c^-4 falls below NFW everywhere), leaving pure NFW. The best FDM recipe is no FDM core. All of M4's gain comes from the SHMR and c knobs.
- Post-result diagnostic, not frozen, `scripts/recipe19b.py`, `recipe19b.out`: M2-M4 restarted from the cored minimum converge to the same soliton-off fits (0.1419, 0.1419, 0.0921). Same verdict.
- Expectation wrong in part: I expected M1 0.07-0.12 and M2-M4 0.05-0.07; got 0.149 and 0.142, 0.142, 0.092. The soliton adds inner mass where the base halo already overshoots the law at low g_b (bins +0.10 to +0.17), so it cannot help.
- Acceleration scale g_c: at M1 median 265 a0, kappa_eff 132 (+2.42 dex), rms 0.895 dex over SPARC, slope d log g_c/d log M200 = 1.000 exactly as expected. Fitted M2-M4 values (kappa_eff 7e-4 to 0.09) describe switched-off solitons, not an operative scale. g_c(z)/g_c(0) at fixed M and m: 2.22, 3.01, 4.54 at z 1, 1.5, 2.33, all FAIL the band. a_q = (hbar/m)^(1/2)(G rho_DE)^(3/4) at m22 100: 4e-7 a0; rho_DE enters only by hand, and c sqrt(G rho_DE) contains no m.
- VERDICT: NOT EXACT. Every gate fails for every model. Fails do not rule out FDM or LCDM; this is one global recipe, not per-galaxy freedom. kappa = 1/2 FITTED; not theory closed.
