# QX8 frozen criteria: the flagship SPARC grade on the action's exact field

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings never pooled.
Shared rules: closure_2026_11_06/SWARM_BRIEF.md.

## Why

The flagship SPARC/RAR pass (PAPER67 v1.2, the FG1 row "S SPARC", from EM1/P4's grader) applies the algebraic law
g = nu(g_N/a0) g_N point by point to the in-plane Newtonian field. QX4 (beabff85b5) solved the action's static
equation exactly (AQUAL, div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho, mu(x) = x/(1+x), the inverse of the law's
nu; QX4 Lean) and found the exact in-plane field up to 0.097 dex below the law near R_d in low-surface-density
discs. That is above the 0.057 dex line. v3s's static sector is this AQUAL equation up to terms <= 4e-4 (QX4 3a,
AC8). So what the action predicts on SPARC is the exact field. This lane regrades SPARC on it.

## The grade reused, unchanged (EM1 em1_emergent.py, P4's loader, mask and weights)

- Data: real_research/data/sparc_data/*_rotmod.dat (175 galaxies) and SPARC_Lelli2016c.mrt. Not the RC100 CSV:
  the flagship grade never used it.
- V_bar^2 = sign(Vgas) Vgas^2 + U Vdisk^2 + 1.4 U Vbul^2. Per-galaxy U on the grid 0.30-1.20 in steps of 0.01,
  chosen by the minimum weighted mse. Weights W = 1/(max(eV,1)/max(Vobs,1))^2. Mask GB > 0, GO > 0, Vobs > 0.
- Pooled rms = sqrt(sum wr2 / sum ws); median U.
- **LINE (PAPER67's own): rms <= 0.110 and 0.50 <= median U <= 0.80.** The algebraic law reads canonical
  0.0541 @ 0.52 PASS and alt 0.0537 @ 0.44 FAIL (U).

## The exact field

For each galaxy and footing, the solver is QX4's aqual.py, imported read-only.
- Grid: (ln r, theta), 160 x 48, p = 2. r_min = 0.02 x R_1, r_max = 300 x R_last.
- Picard iteration, tolerance 1e-7, at most 400 iterations; the residual is recorded per solve.

Baryons, in solar masses with kpc throughout:
- **Stellar disc.** Sigma = U x SBdisk(R), using rotmod's SBdisk. Interpolated in log SB between data radii and
  held at the first value inside R_1. Beyond R_last it falls off as exp(-(R - R_last)/R_d), with R_d the catalogue
  Rdisk, and is cut at R_last + 6 R_d. Vertical profile exp(-|z|/z_d)/(2 z_d), with z_d = 0.196 R_d^0.633 kpc (the
  SPARC convention).
- **Gas.** Non-negative least squares on thin annuli. Each annulus is sech^2 with z_g = 0.15 kpc. Edges sit at the
  geometric midpoints of the data radii, and the outermost edge is at 1.1 R_last. The Newtonian basis comes from the
  solver itself in Newton mode, using one factorisation. The fit is to sign(Vgas) Vgas^2 at the data radii.
- **Bulge, at U = 1.** M(<r) = Vbul^2 r/G at the data radii, made monotone by a running maximum. rho = dM/dr/(4 pi r^2).
  Inside R_1 it is a uniform sphere matching M(R_1). Beyond R_last, rho = 0.

The correction is taken against the solver's own Newtonian field, so that inversion error is second order:

    T(R, U) = log10[ g_R,exact(R) / (nu(g_N,solver(R)/a0) g_N,solver(R)) ]

Here g_N,solver comes from the same grid and the same mass, by linear superposition of the components. Then
**log10 g_pred = log10[nu(GB/a0) GB] + T** on the data's own GB. T is computed at U nodes {0.30, 0.42, 0.60, 0.85,
1.20} and interpolated linearly in log U on the fine grid. Where g_N,solver <= 0, T = 0, and those points are counted.

## Graded and reported

- **GRADED: the frozen line on the exact field, per footing.** EXACT FIELD PASSES / FAILS PAPER67's line.
- Reported: rms and median U for the law and for the exact field; the median refit shift in U; T statistics binned
  in g_bar/a0 and in Sigma_0 (SBdisk at R_1); fixed U = 0.50 rms for the law and for the exact field (EM1 A1's
  convention); and the same grade without the galaxies tagged by K4.
- Reported, with a 2 sigma reporting line: the surface-brightness trend at fixed speed. Per galaxy, take the weighted
  mean residual at its best U, then regress on log10 SBeff and log10 Vflat (OLS; galaxies with Vflat > 0). Bootstrap
  over galaxies, 2000 draws, seed 20261106. "No trend" means |slope_SB| < 2 sigma. Done for the law and for the exact
  field.
- Sensitivity, reported only: z_d x 2 and z_g x 2 on the K5 subset (median and max change in T).

## Known answers (they can fail)

- KA1: the algebraic mode of this code reproduces P4/EM1. Canonical 0.054087447879939264 @ 0.52 and alt
  0.05371798965550355 @ 0.44, rms within 1e-4 and U equal.
- KA2 Plummer: the exact radial g against the exact spherical solution nu(g_N/a0) g_N, max relative 1e-3 (QX4 K1's
  code, grid 160 x 48).
- KA3 Kuzmin, h/a = 0.02: the midplane V against Brada-Milgrom's form nu(|g_N|/a0) g_N, max relative 0.02 (QX4 K2's code).
- K4 baryon reconstruction: the solver's Newtonian V_bar^2 at U = 0.5 against rotmod's, as a weighted rms fractional
  difference. The median over galaxies must be <= 5 %. Galaxies above 10 % are tagged and the grade is also reported
  without them.
- K5 ladder: 12 galaxies (every 15th by name), 160 x 48 against 240 x 72, max |dT| at data points <= 0.005 dex.
- K6 interpolation in U: held-out U = 0.50 and 0.72 on the K5 subset, direct against interpolated, max <= 0.005 dex.
- K7: every Picard solve reaches residual <= 1e-7. Solves that stop at the cap are tagged; their T must still pass
  K5-type agreement against a 240 x 72 rerun.

## MUTATE (separate outputs)

- M1: mu = 1, so the exact field is Newton and log10 g_pred = log10 g_N,data. The line must FAIL on both footings.
- M2: a planted T - 0.100 on every point. The fixed-U mean residual must move by +0.100 +- 0.005, and the refit
  median U must rise. Both must happen, or the grader is not sensitive.

## Label rules

- Per footing: **EXACT FIELD PASSES** if the line is met and KA1-KA3, K4 (median), K5 and K6 pass and the MUTATEs
  bite. **EXACT FIELD FAILS** if the line is missed with those checks passing. **NO VERDICT** if any of those checks
  fail.
- If the exact field passes only because U refits upward, the label says so and gives both the fixed-U and the
  refit numbers.
- Scope: isolated discs (no external field), catalogue distances and inclinations, AQUAL static sector only, one
  disc thickness convention plus the reported sensitivity. If the grade fails, it is the flagship that fails, and the
  label says so plainly.
