# QX7 iter_2: cold sector heated by the cosmic clock, lambda_J = lambda_3 (a/a_3)^m. FAIL (no window)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria d9d76d87a2. Script: qx7_iter2.py (one thread, about 1 min).
It reuses QX3 iter3's G2' solver: beta = -m/3, mu0 = 2 pi a_3^m / lambda_3. Outputs: qx7_iter2.json/.out and qx7_iter2_MUTATE.*.

## Result

- Analytic gates pass in 56 of 1,353 cells: forest G4' (lambda_J(z=3) <= 0.42/h comoving), reference galaxy G3', and G3b
  (7 Humphrey ellipticals and the 5 most massive SPARC galaxies, M_b up to 3.4e11, perturbation mass M_b(1 + R), R = 5.56).
  All 56 have m >= 4.25. The sector has to heat steeply between z = 3 and z = 2.
- **G2' (CMB-lensing growth): no cell passes.** Closest Delta chi^2 = 9.47 (m 8, lambda_3 0.137 Mpc) against a line of 4. A
  power-law heating fast enough to keep the dust out of massive ellipticals by z = 2 keeps heating, so the dust stops
  clustering at z < 1-2, inside the lensing kernel.
- Label: **FAIL (no window)**. The cluster predictions are not reached.
- Sensitivity (no label): with G3b at z_c = 1 there are 129 analytic cells; at z_c = 3 there are 0. With M_t = M_b there are 128. The
  massive ellipticals' assembly epoch is the hinge.

## Known answers and controls

- K1: m = 0 reproduces QX3 iter2's G2 at mu = 1e3, Delta chi^2 1252.7496 = 1252.7496. **PASS.**
- MUTATE 2 (f_cap = 0) reproduces QX2 iteration 1's X-COP mean, +0.4675 / +0.4345. **BITES.**
- MUTATE 3 (f_cap x 3) moves the X-COP mean by +0.318 / +0.311. **BITES**: the cluster predictor is sensitive.
- MUTATE 1 (G3b flipped): as coded it asks for a full window member, and none passes G2' (closest 14.7), so **NO BITE as coded**.
  The frozen purpose, "the analytic gates have power", is met: the flipped G3b admits 75 analytic cells against 56. Disclosed;
  the FAIL rests on G2', which K1 validates.
- Solar recheck: hot dust at the cosmic mean gives g_d(1 AU)/g_N = 1.6e-23.

## Next (pre-planned mutation, iter_3)

The failure is a shape problem: the heating has to stop. In this framework the natural saturating clock is the dark-energy
fraction Omega_DE(a), the quantity a0 tracks. So iter_3 is lambda_J = lambda_* Omega_DE(a)^p. It is frozen before it runs.
