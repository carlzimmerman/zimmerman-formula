# NBC1_neutral_baryon_contact: FROZEN CRITERIA

Frozen 2026-11-10, committed alone before any script of this lane exists. kappa = 1/2 FITTED; not theory closed.
Footings canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), computed and graded separately, never pooled.
Cold dark energy is a gravitating component, never a particle. Nothing here says the data favour the framework.
One thread, analytic plus one small ODE; nothing downloaded.

## Question

Can a0 be a contact strength? Hypothesis H: cold dark energy is a conserved, cold, normally self-gravitating component
(form B, counted once) that exchanges momentum with NEUTRAL baryons only (atoms and molecules in gas; not ionised
plasma, not stars), with drag force per unit volume

    f = kappa_c * rho_c * rho_n * |dv| * dv,      kappa_c constant (no speed dependence),

and kappa_c of order G / a0. Three values are graded, each on each footing:

    k = kappa_c * a0 / G  in  {1, pi, 2 pi}     (G/a0 = 7.13 / 5.90 cm^2/g; pi G/a0 is MEDIUM_DESIGN's value).

H is a microphysical version of PAPER49's rule T (tether only to condensed baryons at low relative speed), which TM1
scored as a postulate. It differs from the contact medium of `closure_2026_11_10/MEDIUM_DESIGN_2026-11-10.md` section 3
only by the word NEUTRAL, which was put in to remove that note's two kills (recombination, the Bullet).

## Disclosed before freezing

- MEDIUM_DESIGN section 3 and its check output were read (all-baryon contact dies at recombination and in the Bullet).
- Hand estimates made in the coordinating chat before this file: gas drag time at the solar circle about 0.4 Gyr;
  about 2 scatterings of an inner-halo element off the Milky Way's gas layer in 10 Gyr; a settled layer of about
  74 Msun/pc^2 against a budget of about 20; drag over expansion about 1 at z 1000 and about 5e-3 at z 100.
  The thresholds below are round numbers set far from those estimates.

## Setup (closed forms, EQ1)

Point-mass baryons M_b, r_M = sqrt(G M_b / a0), x = r / r_M, u = g / a0.
g_N = a0 / x^2, X(x) = [sqrt(1 + 4 x^2) - 1] / 2, g_c = a0 X / x^2, g = g_N + g_c, v_c^2 = g r.
rho_c r = a0 / (2 pi G sqrt(1 + 4 x^2)).  J = (a0^2 / (4 pi G)) [u - ln(1 + u)], with dJ/dr = -rho_c g.
Halo: not rotating, isotropic, sigma^2 = J / rho_c (Jeans; primary). Reported beside it: the halo cut at
x_t = sqrt(5.41 * 6.41), sigma^2 = (J(x) - J(x_t)) / rho_c.
Drag on gas moving at v through a Maxwellian medium of one-dimensional dispersion sigma: the exact average
D(v, sigma) = < |v - w| (v - w).vhat >, done by quadrature. Momentum loss rate of the gas nu = kappa_c rho_c D / v.

## Tests

**K1 gas-disc survival (graded; closed form, no outside data).** Optically thin neutral gas on a circular orbit in the
law's own halo. N_orb(x) = 1 / (nu T_orb), T_orb = 2 pi r / v_c: the number of orbits in which the gas loses its
angular momentum to a non-rotating halo. Grid x in [0.1, 3], 30 log-spaced points.
- FAIL if N_orb < 10 at any grid point.
- PASS if N_orb >= 50 at every grid point (50 orbits is 10 Gyr at the solar circle).
- otherwise NO VERDICT.
Reported: the largest k that gives N_orb >= 10, and >= 50, on the whole grid; the gas layer's own optical depth
k (G/a0) Sigma_gas for Sigma_gas 5, 10, 13 Msun/pc^2 (it must be below 1 for "optically thin" to hold; if it is not,
K1 is NO VERDICT at that k).

**K2 the co-rotation escape (graded; inputs PROVISIONAL, from memory).** K1's drag vanishes only if the cold component
moves with the gas. Then it is supported by rotation, and each crossing of the gas layer damps its vertical motion.
- Count: N_sc = kappa_c Sigma_gas * 2 * (10 Gyr) / T_orb at the solar circle, with R0 = 8.2 kpc, v0 = 233 km/s,
  Sigma_gas = 13 Msun/pc^2 (all three PROVISIONAL). Settled fraction s = 1 - exp(-N_sc).
- Column of a rotation-supported layer that gives the law's own in-plane g_c at the Sun: Sigma_flat = g_c / (2 pi G),
  with g = v0^2 / R0 and g_c = a0 g / (g + a0) (no baryon model needed).
- Round-halo column inside |z| < 1.1 kpc: Sigma_round = rho_c * 2.2 kpc, rho_c = g_c (2 - a0/(g + a0)) / (4 pi G R0).
- Predicted dark column: Sigma_H = s Sigma_flat + (1 - s) Sigma_round.
- Budget (PROVISIONAL): total dynamical 68 +- 4 minus baryons 47 +- 3.4 inside 1.1 kpc = 21 +- 5.2 Msun/pc^2.
- FAIL if Sigma_H > budget + 3 errors (36.6). PASS if Sigma_H <= budget + 1 error (26.2). Else NO VERDICT.
The label of K2 carries the word PROVISIONAL.

**K3 recombination (reported; graded only at the extremes).** Neutral fractions: helium by Saha (He I only; an upper
bound on neutral helium above z 1800, stated), hydrogen by Saha down to x_e 0.99 then the Peebles three-level equation.
omega_b = 0.02237, cold share 5.41 omega_b, h = 0.674, omega_r = 4.18e-5, T0 = 2.7255 K, Y = 0.245 (PROVISIONAL
standard values). Relative speed: sqrt(v_bc^2 + 8 k_B T / (pi m)), v_bc = 30 km/s at z >= 1100 and
30 km/s * (1 + z)/1101 below (MEDIUM_DESIGN's number). Rates over the expansion rate, z = 2500 ... 30:
- G_c = kappa_c rho_n v / H (the cold component's momentum, against neutral baryons),
- G_b = kappa_c rho_c f_n v / H (the baryons' momentum; the neutrals are collisionally tied to the rest).
- PASS (by hand) if max G_c at z >= 900 is below 1e-3. FAIL (by hand) if it is above 1. Otherwise
  NOT DECIDED BY HAND (a Boltzmann run with this coupling would be needed; none is run here).

**K4 the Bullet (reported; NOT A TEST).** H was built to pass it: the gas is ionised. Reported: the neutral fraction
needed for one optical depth at the gas columns of MEDIUM_DESIGN (0.006 to 0.03 g/cm^2).

**K5 heating of the neutral gas (reported; PROVISIONAL input).** Dissipation per hydrogen nucleus at the solar circle,
kappa_c rho_c D(v0, sigma) * v0 * 1.4 m_H, non-rotating halo, against the measured [C II] cooling of the diffuse gas,
2.65e-26 erg/s per H (PROVISIONAL, from memory). Reported as a ratio; the share that goes to the gas is not specified
by H (between a half and all), so K5 is not graded.

**K7 the curve.** Whether H has the law's X(x) as its fixed point for every M_b is NOT EVALUATED here. It is moot
unless K1 or K2 passes.

## Known answers (any failure makes every label NO VERDICT)

- KA1: D(v, sigma) -> (4/3) sqrt(8/pi) sigma v for v = 0.01 sigma, and -> v^2 for v = 100 sigma, each to 1 %.
- KA2: from the definitions, N_orb = (v_c^2 / D) sqrt(1 + 4 x^2) / k. With c0 = v_c^2 / D evaluated at
  sigma^2 = v_c^2 / 2: N_orb k at x = 1e-3 equals c0 to 1 %, and N_orb k / (2 x) at x = 300 equals c0 to 1 %.
- KA3: with all baryons, k = pi, 30 km/s, z = 1100: drag over expansion 0.73 (canonical) and 0.61 (alt) to 3 %
  (MEDIUM_DESIGN_check.out).
- KA4: Saha hydrogen half-ionised at z in [1340, 1410]; Peebles x_e(1100) in [0.08, 0.22]; x_e(200) in [1e-4, 1e-3].
- KA5: dJ/dr = -rho_c g by finite difference at x = 0.1, 1, 3 to 1e-5.
- KA6: Sigma_round at the Sun in [10, 30] Msun/pc^2 on both footings (the round halo is consistent with the budget).

## MUTATE (separate outputs, `*_MUT_*`)

- M1: k -> k / 100. K1 must turn to PASS at k = 1 (the test can pass).
- M2: Sigma_gas -> 0 in K2. N_sc = 0 and K2 must turn to PASS (the round halo fits the budget).
- M3: drop the neutral restriction in K3 (all baryons). G_c at z 1100 must rise above the neutral value.

## Verdict rule (per footing, per k; then the lane label per footing)

- KILLED if K1 FAILS and K2 FAILS at that k (the non-rotating halo destroys gas discs; the co-rotating one settles
  into a layer the vertical force does not allow), or if K3 FAILS by hand.
- SURVIVES THE HAND TESTS if K1 PASSES, or K2 PASSES with K1's premise void, and K3 does not FAIL.
- NO VERDICT otherwise.
- Lane label per footing: KILLED if H is KILLED at all three k; SURVIVES if it survives at any k; else NO VERDICT.
  Because K2's inputs are PROVISIONAL, a KILLED label that needs K2 is written KILLED (K2 PROVISIONAL).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
