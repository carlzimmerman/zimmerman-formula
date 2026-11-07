# EW2 iter_4 frozen criteria: SPARC, Cassini, c_T, galaxy lensing on v4's own equations

Kappa = 1/2 FITTED; not theory closed. Committed with ../FROZEN_CRITERIA.md before any script or number. Both footings,
never pooled. Members: iter_2's declared list, plus iter_2's mu_w and mu_h once they exist (the members the web and the
hosts need).

## Gates (per member, per footing)

- SPARC: QX5's sparc() loader (Q <= 2, i >= 30, eV/V <= 0.1, Upsilon disc 0.5, bulge 0.7), sphericalised M_b(r) = vb2 r/G
  interpolated in r, flat beyond the last point; static spherical v4 solve, Delta = 0. shift_i = log10(g_AeST/g_law) at
  every point. PASS iff rms shift <= 0.096 dex (the room left under QX8's flagship line 0.110 by the law's own P4 rms
  0.054, in quadrature) and |mean shift| <= 0.05 dex (the G6 line).
- Cassini / Solar System: v4's static sector inside L* is v3s's (C1 + C3); its Q2 and planetary grades are read from
  C6P (clean PASS both footings) and AX1/v3s, not recomputed. Computed here: the mass term's own contribution. (i) The
  static dust around the Sun, delta rho = mu^2 G M_sun/(4 pi G r), gives the radial anomaly dg = mu^2 G M_sun/2 at every
  r (exact for Phi = -G M/r); (ii) a uniform zero-point offset |Phi_0| <= (600 km/s)^2 (generous: Galactic depth plus the
  zero point) gives dg = mu^2 |Phi_0| r/3 at Saturn and a tidal Q2 <= mu^2 |Phi_0|/3 (upper bound). PASS iff
  dg(Saturn) <= 7.0e-15 m/s^2 (Saturn bound, AX1) and Q2 <= 9.0e-27 s^-2 (Hees), with C6P's PASS carried.
- c_T: PASS iff the tensor modes of iter_1's action couple only through R (structural reading of the stated action: the
  F^2, J.D phi, Y, F(Y, Q) and gamma_L terms carry no h_ij kinetic term), so c_T = c. Graded by reading the action, not
  computed; I1's ill-posedness where the aether twists is reported as a separate health row (read).
- Galaxy lensing: Psi = Phi in the static limit (iter_1 KA1, C1 K1 replay) gives lensing = dynamics: PASS iff iter_1 KA1
  passes. The KiDS amplitude is iter_2's G6 at the same member.

## Label

Per member and footing; the summary row is at the members that pass iter_2's G6 (host-compatible) and at mu_w.

## Known-answer checks

- KA1: mu = 1e-6: SPARC rms shift <= 1e-4.
- KA2: Cassini (i) checked against the closed form on the solver for the Sun out to 50 AU (relative 1e-3).

## MUTATE (separate outputs *_MUTATE)

Drop gamma_L (plain AeST, L* -> 0): the AX1 engine's AeST class, run read-only from a scratch copy (no write into
rebuild_2026_10_22/), must FAIL Cassini Q2 in every cell (AX1 recorded 2.44-5.15x). Bites iff it fails.
