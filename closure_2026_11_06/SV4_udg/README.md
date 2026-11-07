# SV4: do the AGC 114905 and Malin 1 failures survive the systematics the record had not graded? Yes: NOT RESCUED, both galaxies, both footings

kappa = 1/2 FITTED; not theory closed. Adopts nothing. One galaxy excludes nothing. Footings never pooled (values
are given canonical / alt). Criteria: FROZEN_CRITERIA.md + iter_1..iter_4/FROZEN_CRITERIA.md, committed alone
(07715343da) before any script or number. Model throughout: the action's exact static field (QX4's axisymmetric
AQUAL solver, the one QX8 used, read-only), 480 x 144 grid, 240 x 72 ladder. Data and baryons are UD1/UD2's, run
read-only. No downloads; NEEDS_OWNER.md lists what is missing.

## Labels

| Systematic | AGC 114905 | Malin 1 |
|---|---|---|
| 1. Pressure support (asymmetric drift), published sigma_HI and z_d | **NOT RESCUED**: chi2 184.5 / 234.6 at the in-errors maximum (from 700 / 830); flaring (generous) 150 / 192 | **NOT EVALUABLE** (no sigma_HI on disk) |
| 2a. Disc thickness in the inclination | **NOT RESCUED**: i moves -1.6 to +1.7 deg; best in errors 395 / 481 (a-, q0 0.13, at i0 - 2 sigma) | n/a (kinematic inclination) |
| 2b. LOS through the thick layer, on the action's field | **NOT RESCUED**: C_k 0.80-0.97, chi2 614 / 732 (h x 2 generous: 520 / 624) | **NOT RESCUED**: C_k >= 0.988, chi2 55.7 / 89.5 (A2) |
| 2c. Non-circular flows | **NOT EVALUABLE** (no harmonic decomposition on disk) | **NOT EVALUABLE** |
| 2d. All of 1, 2a, 2b at once (in errors) | **NOT RESCUED**: chi2 108.8 / 143.8 (p 7e-22 / 3e-29) | - |
| 3. Large-scale field, whole local matter (ALFALFA-SDSS) | **NOT RESCUED** on the Newtonian reading (bound 0.018 / 0.015 a0 vs window edge 0.070 / 0.071); MOND reading NOT EVALUABLE (bound 0.14 / 0.13 too loose; vector estimate 0.006) | n/a: no g_e rescues it (QX4) |
| 4. Inner bulge/bar mass model, stellar vs HI distance | n/a | **NOT RESCUED**: best of 24 corners chi2 56.1 / 71.4 (baseline 56.7 / 91.3); bar bound 72.6 / 94.2 |
| **Galaxy** | **NOT RESCUED** | **NOT RESCUED** |

## AGC 114905

**iter_1, asymmetric drift.** The authors' V_circ already contains an AD term (38-178 (km/s)^2). Using the
published sigma_HI (13.9 falling to 5.0 +- 1.5 km/s), the published gas profile and z_d = 1.3 kpc, the frozen Jeans
form reproduces their term (median |ln ratio| 0.36, line ln 2). Pushing every sigma to +2 sigma and the slope to its
steepest 2-sigma pair raises the outer V_c from 26.9 to 38.7 km/s. The exact field needs 61-64 km/s. The outer ring
needs AD2 = 3129 / 3476 (km/s)^2, against 120 published: a dispersion of about 26-27 km/s, against 5. AD is the
right direction (it raises V_c); it is 25x too small.

**iter_2.** The thickness correction to the optical inclination is tiny either way (q0 0.10-0.13 moves i by 0.2-0.3
deg; generous q0 0.30 by 1.6 deg). On the action's own field, V_c falls with height, so the LOS-weighted speed sits
below the midplane speed by 3-20 % (largest at the inner ring). Correcting for it raises the data 2-25 % and leaves
chi2 614 / 732. All in-errors corrections together (iter_1's maximum, thickness at i0 - 2 sigma, LOS) give chi2
108.8 / 143.8. Non-circular flows would need coherent LOS amplitudes of 3-20 km/s rising outward, 1.6-3.9x sigma_HI
in the outer three rings; no residual-field data are on disk to bound them.

**iter_3.** On the exact field the EFE window is 0.0695-0.156 / 0.071-0.156 a0 (algebraic: QX4's window reproduced,
KA3 0.3-0.4 %). From the 23,096 ALFALFA-SDSS galaxies within 200 Mpc the vector field is 3.7e-5 / 3.1e-5 a0.
The no-cancellation bound moves each galaxy as close as its 2-sigma distance allows, fills the 82 % of the sky
outside the footprint at the footprint's column, and multiplies by F_c = 10 for baryons an HI catalogue misses. It
gives 0.018 / 0.015 a0. The missing baryons would need F_c = 38 / 47. The bound grows only 1.48e-2 -> 1.81e-2 from
50 to 200 Mpc. Under QX4's MOND reading of g_e the same bound is 0.14 / 0.13 a0, above the window edge, so the
frozen rule gives NOT EVALUABLE; the vector estimate there is 6e-3 a0. QX14's census (no host) is unchanged.

## Malin 1

**iter_4, inner mass model and distances** (A2 density, 24 declared corners per footing). Corners: HSB as a sphere
(QX4) or a thin disc (h 0.3 kpc, inversion K4 0.28 %); HSB M/L 3.3, 3.7 (paper's MOND fit), 5 (paper's upper bound),
plus 1.65 (x0.5, generous); stars at (1+z)^-2, 1 or (1+z)^2 times the HI distance (the full D_A/D_L mix-up).
The best in-errors corner is disc, M/L 3.3, same distance (canonical, chi2 56.1/4) and disc, M/L 3.7, stars at
(1+z)^-2 (alt, 71.4/4). Lowering the HSB mass (x0.5, generous) is worse (122-450 / 94-352), because the 12.5 kpc
ring then falls below the data. Moving stars farther or adding stellar mass is worse (up to 598 / 831). The shape
(dip at 62.5 kpc, rise at 87.5 kpc) is set by the gas, which no inner change touches. The bar bound
(quadrupole/monopole, bar mass = all of the HSB, half-length 10 kpc) is 29-36 % in V^2 at 12.5 kpc but <= 2.8 %
at 37.5 kpc and <= 0.8 % at 62.5 kpc. Applied as frozen (V lowered at every ring), it worsens chi2 to 72.6 / 94.2.
The outer misses need -28 % / -34 % in g (QX4 iter3). A1 density (reported): baseline 54.7 / 42.9, best corner 51.2 / 80.5.
Two rows printed before amendment A1 (sph, M/L 3.3, stars at (1+z)^-2: 104.5 / 83.5) reappear unchanged.

**iter_2b.** The 1-2 kpc gas layer at 38 deg changes the LOS speed by <= 1.2 %: chi2 55.7 / 89.5 (A2), 53.7 / 42.1 (A1).

## Checks and controls

- KA0: my exact-field V equals QX4's iter1.json V_exact (0 difference) for AGC 114905 and both Malin 1 densities;
  ladders 5e-4 (AGC), 1.3e-3 (Malin A2), 4.5e-3 (A1), all below the 1 % line.
- iter_4 A1 tolerance check: cold baseline at 3e-8 vs the 400-iteration run 1-2e-10 (line 1e-3); ladder on the
  best corner 5.7e-3 / 2.8e-3; KA0 4e-11 / 1.5e-10.
- KA-AD 0.36 (line 0.69) PASS; KA3 0.3-0.4 % (line 2 %) PASS; K4 HSB thin-disc inversion 0.28 % (line 3 %) PASS.
- MUTATE, all bite on both footings: iter_1 wrong-sign AD (V_c^2 = V_rot^2 - AD2 clips four rings to 0, so chi2 is
  ~1e12: it bites, but the number only says the sign is wrong); iter_2 wrong-sign LOS (795 / 939; Malin 57.9 /
  93.0) and a+ thickness (714-990); iter_3 planted 2 x M_req host flips the label (vector 0.15 a0, in the window);
  iter_4 wrong-direction corner (sphere, M/L 5, stars at (1+z)^2, bar raising V) chi2 747 / 1001 vs 56.7 / 91.3.

## Disclosed

- Malin 1's z = 0.0826 is from memory (provisional); it sets only the (1+z)^2 distance bracket.
- iter_3: catalogue distances are the catalogue's own (cz/70 above 6000 km/s). The bound's d_eff is the exact
  closest approach over each galaxy's 2-sigma distance interval, the literal form of the criteria's "as close as its
  2 sigma distance allows". Its biggest term is a 1.4e10 Msun galaxy 17.6 Mpc away placed at 0.53 Mpc.
- After the iter_1-3 runs, sv4_common.py gained a vectorised twin of the solver's deposit (identical to 2e-16)
  and a warm start (Phi0) for iter_4's variants; iter_4 ran footings in two single-thread processes. The committed
  iter_1-3 outputs came from the original deposit.
- Malin 1 solves stop at the solver's 400-iteration cap with residual ~1.5e-8 (as QX4's A2); the ladder line is met.
- No Lean file in this lane.

## Files

FROZEN_CRITERIA.md, iter_k/FROZEN_CRITERIA.md, sv4_common.py, iter_1/iter1_asym_drift.py, iter_2/iter2_thick_projection.py,
iter_3/iter3_large_scale_field.py, iter_4/iter4_malin_inner_distance.py (run per footing: iter4_{canonical,alt}.*, iter4_MUTATE_{canonical,alt}.*),
iter_4/AMENDMENTS.md, the other .out/.json and _MUTATE twins, NEEDS_OWNER.md.
