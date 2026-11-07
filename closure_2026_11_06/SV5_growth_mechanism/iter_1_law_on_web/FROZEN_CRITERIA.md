# SV5 iter_1: class W. Any sector that supplies the target source, with the a0 law ON on the linear web. FROZEN CRITERIA

Kappa = 1/2 FITTED; not theory closed. Committed with ../FROZEN_CRITERIA.md, before any script or number.

## Class

W = every sector (any equation of state, switch or coupling) that delivers T0.1's Newtonian source on the linear web, while
the a0 law acts there as the action's static equation does: QUMOND on the peculiar field, simple nu(y) = 1/2 + sqrt(1/4 + 1/y)
(the inverse of law S, EQUATIONS 4.1), as WG2 R1 ran it. Members differ only in how they reach the target web field, so in the
linear-Gaussian approximation they share its law-on response.

## Method

- Field: Gaussian realisation of the dust reference's CLASS P_lin(k, z) (QX3 corner model M, A_s = 2e-9) times A_X0, the PR4
  amplitude fit of X0 (so the Newtonian target matches PR4). N = 128^3, L = 2000 Mpc comoving, seed 5. Same phases at every z:
  delta_k(z) = delta_k(z_ref) sqrt(P(k, z)/P(k, z_ref)).
- z grid: 0.25, 0.5, 1, 2, 3, 5, 8, 12, 20, 50.
- Newtonian: Phi_k = -(3/2) H0^2 Omega_m delta_k / (a k^2) (comoving), g_N = -grad Phi / a (physical, m/s^2). Corner H0, Omega_m.
- Law on: g = P_L[nu(|g_N|/a0) g_N] (longitudinal projection); B(k, z) = <|Phi_law,k|^2> / <|Phi_N,k|^2> in 16 log shells from
  k_f to k_Ny.
- Projection: Rr = sqrt(B) on the solver's (k, z) grid, linear in ln k and ln(1+z), held constant outside the box shells and
  outside [0.25, 50]. S = I2.limber_ratio(M, H0, kgrid, zgrid, Rr).
- Statistics: A_S from I2.best_amp_chi2(X0 S); amplitude ratio r = A_X0 / A_S (model/data lensing amplitude);
  shape Delta chi^2 = chi2(X0 S) - c0.

## Gates (per footing; a0 enters through nu)

- W1 amplitude: |r - 1| <= 3 sigma_A,rel (T0.4). FAIL otherwise.
- W2 shape: Delta chi^2 <= 4.
- Rigorous bound (reported with W1): y_max = max over the grid of |g_N|/a0 at each z; nu_min = nu(y_max). The box-integrated
  gradient power obeys sum |g|^2 >= nu_min^2 sum |g_N|^2 (Lean: Cauchy-Schwarz with <g, g_N> = <nu g_N, g_N>).

## Label

NO-GO FOR CLASS W if W1 fails on both footings (with the Lean bound > 1 + 3 sigma_A,rel at every graded z, the integrated
statement holds for every field whose |g_N| <= y_max a0). FAIL if only W2 fails. PASS if both pass.

## Checks and MUTATE

- K1: Newtonian realisation power / (A_X0 P_lin) per shell, median within 15 % at z = 1.
- K2: a0 x 1e-8 gives B within 1e-2 of 1 in every shell (nu -> 1 limit of the solver).
- K3 (reported): seed 6, z = 1, B per shell.
- MUTATE (separate outputs *_MUTATE): nu == 1 (law off on the web). Must give r = 1 and Delta chi^2 = 0 to 1e-6, so W1 and W2
  pass; it bites iff the main run fails W1.
