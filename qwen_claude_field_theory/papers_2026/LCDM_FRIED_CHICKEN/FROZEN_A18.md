# A18: published hydro-calibrated halo responses (frozen before any number)

Research experiment in this quarantined folder only. Rival language, adopts nothing, never feeds anything outside this folder. These fitting functions stand in for real hydrodynamic runs; they are not hydro runs. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Script `scripts/recipe20.py`, output `scripts/recipe20.out`.

## Common set-up
SPARC 171 galaxies from `lib.py` (Y_disk 0.5, Y_bul 0.7). M200 (200c) from the lib Moster SHMR at M* = g.Ms, Diemer19 c200c from colossus (`cflat`). Dark mass (1 - f_b) M200 with f_b = min(M_b/M200, 0.5), as in lib's R1/R2. Total g = g_b + G M_DM(<r)/r^2. No adiabatic contraction except what a published formula itself carries. X = log10(M*/M200) throughout.

Mass-definition approximations, stated: DC14 and Lazar use M_vir and c_vir = R_vir/r_-2 (Lazar: Bryan-Norman Delta_vir, M_halo = DM mass); here 200c and Diemer19 c200c stand in for both, and M*/M200 stands in for M*/M_halo.

## Models, as published, zero free knobs
- **(a) DC14**, Di Cintio et al. 2014b (arXiv 1404.5959), formulas checked against the paper text (eqs. 1, 2, 3, 6, appendix recipe): rho = rho_s / [(r/rs)^gamma (1 + (r/rs)^alpha)^((beta-gamma)/alpha)];
  alpha = 2.94 - log10[(10^(X+2.33))^-1.08 + (10^(X+2.33))^2.29], beta = 4.23 + 1.34 X + 0.26 X^2, gamma = -0.06 + log10[(10^(X+2.56))^-0.68 + 10^(X+2.56)];
  c_SPH/c_DM = 1 + 0.00003 exp(3.4 (X + 4.5)), c = R/r_-2; r_-2 = ((2-gamma)/(beta-2))^(1/alpha) rs; rho_s from M(<R200) = dark mass.
  Validity -4.1 < X < -1.3 (paper). Choice made here: X < -4.1 is NFW (1,3,1) as the paper says; X > -1.3 is clipped to -1.3 (untested regime in the paper, AGN not modelled).
- **(b) coreNFW**, Read, Agertz & Collins 2016 (arXiv 1508.04143), checked against the paper text (eqs. 16-20): M(<r) = M_NFW(<r) f^n, f = tanh(r/r_c), n = tanh(q), q = kappa t_SF/t_dyn, t_dyn = 2 pi sqrt(rs^3/(G M_NFW(rs))), r_c = eta R_1/2 (projected stellar half-mass radius), kappa = 0.04, eta = 1.75. Inputs here: t_SF = 13.8 Gyr (continuous star formation, the age of the universe; Read et al. use the run length, about 14 Gyr); R_1/2 = 1.678 R_d (projected half-mass radius of an exponential disc; bulges ignored). Calibrated on dwarfs (M200 about 1e9 to 1e10); applied to all 171 as published, a stated extrapolation.
- **(c) Lazar et al. 2020** FIRE-2 core-Einasto (arXiv 2004.10817), checked against the paper text (eqs. 8, 12, 13, 14, Tables 1-3): rho = rho~ exp{-(2/alpha)[((r + r_c)/r~s)^alpha - 1]}, alpha = 0.16 fixed; with x = M*/M_halo:
  r_c = 10^1.21 (0.71 + x/7.2e-3)^-2.31 (x/0.011)^1.55 kpc;
  r~s/r_-2 = (1 + x/0.044)^-31.79 + 1.51 (x/0.28)^0.40;
  c_F2/c_DM = (1 + x/4.28e-3)^-1.80 + 0.374 (x/4.28e-3)^0.66;
  r_-2 = R200/c_F2; normalisation rho~ from M(<R200) = dark mass. Fit range -3.54 <= X <= -0.97; x is clipped to that range (choice made here).
No coefficient above is from memory; all three sets were read from the papers' own text. Only the input choices (t_SF, R_1/2 = 1.678 R_d, mass definitions, clipping) are mine.

## Knobbed versions, 3 global knobs per model, then grade again
- k1 SHMR normalisation dn (lib meaning, M* at fixed M200 times 10^dn), bounds [-0.5, 0.5].
- k2 concentration normalisation dc (dex on Diemer19 c_DM), bounds [-0.3, 0.3].
- k3 one response strength: DC14 s interpolates (alpha, beta, gamma) and log(c_SPH/c_DM) linearly between NFW (s = 0) and published (s = 1), bounds [0, 2]; coreNFW log10 of a multiplier on q (kappa), bounds [-1, 1.5]; Lazar log10 of a multiplier on r_c, bounds [-1, 1].
- Guards in the DC14 s interpolation (s > 1 can push the published exponents past sense): beta >= 2.05 and gamma >= 0 (no hollow centre), alpha >= 0.3. At s <= 1 these never bind on the published fit.
- Tuned by least_squares on log g to the law (as lib.fit), start at published (0, 0, published s), bounded.

## Gates (every model, zero-knob and knobbed)
- lib.grade on all-data tuning: E1 rms to law <= 0.02 dex, E2 p95 per-galaxy <= 0.04, E3 worst 0.5-dex g_b bin <= 0.02; rms to observed reported.
- Holdout: tune on GS[::2], grade GS[1::2]; unseen rms to law <= 0.025 dex. For zero-knob rows the holdout is just the rms on GS[1::2] (nothing tuned).
- Knob count and knobs at bound reported.
- EXACT only if E1, E2, E3 and holdout all pass.
- kappa_eff: these models carry no acceleration scale of their own. Reported for information only: a fitted to the model's g(g_b) by lib.fit_a, kappa_eff = a/(c sqrt(G rho_DE)) against 0.5 within 0.05 dex. That is a read-off, not a native scale, and the z-evolution band (E5) is not applicable: no z-dependence of these fitting functions is used. Stated as N/A, not graded.

## Expected outcome, written in advance
All three zero-knob rows FAIL E1 (rms to law 0.06 to 0.15 dex, the territory of R1/R2); coreNFW probably worst at high mass (it cores massive discs too). With 3 knobs each improves but stays above 0.04 dex, fails E1 and E2; no row is EXACT. The record's R1/R2 (3 to 7 knobs, 0.072 dex) is the comparison.

## RESULT, written after the numbers (scripts/recipe20.out, 13 s, single thread). No bug found; no _before_fix file.
Controls: DC14 at s = 0 reproduces lib NFW to 2e-4 dex; DC14 exponents at X = -2.5 (alpha 2.65, beta 2.51, gamma 0.25) and Lazar r_c 2.2 kpc at x = 5e-3 match the papers' stated behaviour. SPARC log M*/M200 spans -2.78 to -1.45 (p5 to p95), no galaxy outside either fit range, so the clipping never acted.

| row | knobs | E1 rms to law | E2 p95 | E3 worst bin | holdout unseen | rms to obs | kappa_eff (read-off) | verdict |
|---|---|---|---|---|---|---|---|---|
| DC14 published | 0 | 0.1325 | 0.2498 | 0.0618 | 0.1270 | 0.2166 | 0.573 | NOT EXACT |
| DC14 + 3 | 3 (0 at bound) | 0.0748 | 0.1459 | 0.0233 | 0.0746 | 0.2020 | 0.467 | NOT EXACT |
| coreNFW published | 0 | 0.1159 | 0.2104 | 0.0232 | 0.1071 | 0.2061 | 0.512 | NOT EXACT |
| coreNFW + 3 | 3 (0 at bound) | 0.0729 | 0.1368 | 0.0382 | 0.0762 | 0.2034 | 0.457 | NOT EXACT |
| Lazar20 published | 0 | 0.1767 | 0.3747 | 0.1001 | 0.1659 | 0.2378 | 0.621 | NOT EXACT |
| Lazar20 + 3 | 3 (0 at bound) | 0.0835 | 0.1563 | 0.0432 | 0.0842 | 0.2053 | 0.452 | NOT EXACT |

Tuned knobs (dn, dc, strength): DC14 (+0.20, -0.08, s 0.29); coreNFW (+0.35, +0.07, log q-mult -0.31); Lazar20 (+0.38, -0.21, log r_c-mult -0.61). All three want a lighter halo at fixed M* (dn +0.2 to +0.4) and a weaker response than published. Convergence check after the run (not a gate): 4 random restarts at 200 evaluations each land on the same minima (one coreNFW restart stuck at a worse 0.0989).
Verdict as expected in advance: every row fails E1 and E2, none is EXACT; knobbed rows sit at 0.073 to 0.084 dex, the same territory as R1/R2 (0.072). The kappa_eff column is a fitted read-off, not a native scale; E5 not applicable. Stand-ins for hydro, not hydro runs. Passing would show freedom, not evidence; failing here does not rule out LCDM. kappa = 1/2 FITTED; not theory closed.
