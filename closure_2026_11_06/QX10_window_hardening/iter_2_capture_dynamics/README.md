# QX10 iter_2: the sector does not leave galaxies. FAIL for all four cells (KiDS lensing shift G6)

Kappa = 1/2 FITTED; not theory closed. Criteria c1f0cadb7a, Amendment A1 168db297bd (before any iter_2 number).
Scripts: qx10_i2.py (static, graded), qx10_i2_hydro.py (heating run), qx10_i2_ka4b.py (POST-RESULT check, reported only).

## What changed from QX7 iter_4

iter_4 assumed that the captured sector sits as a self-gravitating n = 1 core of radius lambda_J(0)/2, and it ignored the
host's own pull. For window cells that core (>= 0.73 Mpc) is bigger than a galaxy's turnaround radius (0.42 Mpc for
M_b = 1e10), so iter_4 had galaxies keep no sector. Here the same fluid, p = K rho^2 with K = G lambda_J^2/(2 pi), sits in
the host's real potential with the a0 law on. The galaxy's flat-curve potential holds it. The dust no longer puffs out to
lambda_J/2; it settles into a bound halo of 150-230 kpc.

## Result (static A, both footings)

| Cell | Reference galaxy R_s (kpc) | G5 max | G6 KiDS shift (line 0.05) | G7 | Label |
|---|---|---|---|---|---|
| C1 (2.61 Mpc, p 4.25) | 232 / 224, bound | 0.004 / 0.005 | **-0.236 / -0.239** | -0.001 | FAIL |
| C2 (1.47, 3.5) | 157 / 152, bound | 0.013 / 0.014 | **-0.270 / -0.273** | -0.004 | FAIL |
| C3 (8.25, 5.625) | 416 (= r_ta), keeps 44 / 50 % | 0.000 / 0.001 | **-0.153 / -0.157** | -0.000 | FAIL |
| C4 (2.15, 3.75) | 204 / 197, bound | 0.006 / 0.007 | **-0.248 / -0.250** | -0.002 | FAIL |

- G5 (SPARC inner mass) and G7 (ellipticals) still pass. Little sector mass sits inside R_opt or a few R_e.
- **G6 fails everywhere.** The bound sector halo adds 4.2 M_b of lensing mass at 30 kpc to 1 Mpc, so KiDS lensing is over-
  predicted by 0.15-0.27 dex. The isolated-galaxy lensing pass that iter_4 kept was an artefact of ignoring the host.
- Clusters on the dynamical profile (reported): X-COP mean / rms -0.045 / 0.226 (C1 canonical; the rms still fails),
  -0.28 / 0.32 (C2), +0.32 / 0.36 (C3), -0.12 / 0.24 (C4). Groups pass in at most 4 of 20. Clusters stay FAIL.

## Time-dependent run (A1: from lambda_J/2 = 10 kpc, z_s about 1, to z = 0)

- Reference galaxy, C1: the core grows from R_s 7.6 kpc to an outer edge of 228-229 kpc (200 / 400 shells), against
  static A's 232 kpc. Nothing passes r_ta. For X-COP A644 the M_d(<0.5 R500) values agree with static A to 1e-4.
- D-consistency holds on all 8 runs. Convergence of M_d(<10 kpc) holds on 6 of 8. The two C2 reference-galaxy runs miss
  it (1.37e8 vs 8.8e7 Msun): less than one shell's mass sits inside 10 kpc. That is a resolution floor, not a dynamical
  difference. The outer edge agrees to 1 kpc.
- The run reaches the static A end state, so the heating is quasi-static and the static label stands.

## Known answers and controls

- KA1 Lane-Emden n = 1: R_s/(lambda/2) = 1.00005-1.00006 (line 1e-3). KA2 (iter_4's idealisation): reproduced to 1e-2,
  with non-trivial rows at lambda = 100 and 300 kpc (0.1069 vs 0.1069; 0.0041 vs 0.0041). KA3 (perturbed Lane-Emden):
  late mean half-mass radius 1.0067 x LE (line 5 %).
- KA4, as frozen, is vacuous: at z_s the whole core sits inside R_ref, so M_d(<R_ref) is the total mass. It is reported
  PASS, but it tests nothing. KA4b (POST-RESULT, reported only) holds K at K(z_s) for 5 sound-crossing times: r50 and r90
  move by <= 0.02 %.
- M1 (lambda_0 = 1 kpc): G5 4.23 -> FAIL, BITES. M2 (K x 1e4): G5 <= 1.5e-6, G6 <= 7.7e-4, G7 <= 4e-7 of baseline, BITES.

## Approximations

Host baryons are static at z = 0. Galaxies are sphericalised exponential discs; KiDS hosts are point masses. The collapse
phase (z = 3 to z_s) is argued, not run (A1). The sector feels and sources the algebraic a0 law, as iter_4 graded it.
