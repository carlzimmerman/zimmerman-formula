# QX7 iter_1 frozen criteria: stiffness switched by potential depth (lapse)

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed.

## Mechanism, in covariant form

Which scalar reads potential depth?
- (R1) The K(Q) sector's own Q. In the dilute (cold) regime Q - 1 = rho_d/(2A) (QX3 D1). A sound speed c_s^2(Q) is therefore
  barotropic: it reads the sector's own density, not the depth. That is QX3 iter3's class (no-go there for power laws). This is
  stated and Lean-checked (c_s^2 = p'(Q)/rho'(Q) is a function of Q alone). It is not regraded.
- (R2) AC2q's dark-energy clock, X = s^2/(2 N^2). With N = 1 + Phi, delta X / X = -2 Phi + O(Phi^2) (Lean). For subhorizon
  modes in the quasi-static limit, where the clock (c_s = 1) has a negligible delta phi', it is the Newtonian-gauge potential,
  including every long-wavelength mode inside the horizon. The sector becomes cold (lambda_J below the QX3 G2 bound) wherever
  the depth key Phi_key >= t, and hot (lambda_J >= the galaxy's turnaround radius) below t. Two switch shapes: two-sided
  |Phi| >= t, and one-sided (wells only) -Phi >= t.

## Gates

- C1 (clusters cold): t <= the smallest X-COP depth key (QX5 key a: 4.5e-5 canonical, 4.7e-5 alt; read from qx5.json).
- C2 (galaxies hot): the expected fraction of SPARC galaxies sitting at a cold site is <= 0.05. For galaxy i, the depth key is
  Phi_loc,i (QX5 key a, per-galaxy maximum) plus Phi_LSS. Phi_LSS is Gaussian with variance
  sigma_Phi^2 = Int_{k_min}^{10/Mpc} Delta^2_Phi(k, z=0) dln k, from the CLASS linear P(k) of the background above, with
  Phi = (3/2) Omega_m H0^2 delta_m/(a k^2 c^2). k_min = H0/c (graded) and 10 H0/c (conservative, reported, label-bearing:
  both must pass). Galaxies are taken as unbiased tracers (generous: real galaxies sit preferentially in wells).
  The 0.05 line: captured galaxies carry about 4 M_b of dust (QX3 G3) and would sit about 0.6 dex off the RAR. SPARC's quality
  sample has no such population, so 5 % is generous.
- Window: some t satisfies C1 and C2, for each footing, each k_min, and each switch shape (one-sided is the generous one).

## Label

- FAIL if no t satisfies C1 and C2 together (for the generous one-sided switch with k_min = 10 H0/c). The depth key is then
  dominated by the large-scale potential, which no threshold can separate from cluster depths.
- If a window exists, iter_1 passes this stage only. It then needs iter_2-style growth/forest/cluster grading, done here
  under the same gates as iter_2 with the switch read as the window.
- MUTATE A: t = 1e-7 must fail C2 (cold fraction > 0.5). MUTATE B: the flipped switch (cold where |Phi| < t) must fail C1 for
  every t in [1e-7, 1e-3] (X-COP hot). If either does not bite, NO VERDICT.
- Superhorizon note (stated now): modes with k < H0/c are excluded from the key, because an adiabatic superhorizon mode is a
  local time shift and gives delta X/X of about (dot X/X) delta t, which is about 0. That is why k_min is a cut and not a free
  choice.
- White dwarfs and neutron stars (|Phi| 1e-4 to 0.2) are cold sites. The captured mass is bounded by rho_d0 times the
  star's Jeans volume and reported; it is not graded.
