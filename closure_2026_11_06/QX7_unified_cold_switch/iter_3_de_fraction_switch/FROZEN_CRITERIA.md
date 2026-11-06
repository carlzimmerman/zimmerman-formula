# QX7 iter_3 frozen criteria: cold dark energy heated by the dark-energy fraction, lambda_J = lambda_* Omega_DE(a)^p

Frozen before any iter_3 number. Kappa = 1/2 FITTED; not theory closed. This is the pre-planned mutation of iter_2 (76a0c3e0b7),
whose power law failed CMB-lensing growth because the heating never stops.

## Mechanism

p = A(tau) (Q - 1)^2 with A(tau) such that the physical Jeans length is lambda_J = lambda_* Omega_DE(a(tau))^p.
Omega_DE(a) = rho_DE / rho_tot(a) on the background: the vacuum term over the total, from the same CLASS background
as QX3 G1. It is a function of the khronon value tau only, so it is covariant and uniform on each leaf. It saturates
at late times. In this framework a0 tracks rho_DE, which makes Omega_DE the natural switch variable; this is stated, not derived.
Two constants (lambda_*, p).
- Reading 3b, stated now and graded analytically only: with Omega_DE read LOCALLY through the khronon expansion,
  Omega_DE = 8 pi G rho_DE / (theta^2/3), every virialised region (theta about 0) would be hot. Then no bound system captures
  dust, so clusters get M_law(M_b), which is QX2 iteration 1's FAIL. Reading 3b is labelled FAIL (clusters) by that argument.

## Grid and gates

p in [0, 6] in steps of 0.125 (49 values); lambda_* log-spaced from 1e-3 to 1e3 Mpc (61 values). The gates are iter_2's,
unchanged:
- G4' (forest): lambda_J(z=3) <= (0.42/h)/4 Mpc.
- G3' (reference galaxy): lambda_J(z=2) >= r_ta(10^11.5, 2).
- G3b (12 massive systems, M_t = M_b(1 + R)): lambda_J(z=2) >= r_ta(M_t, 2).
- G2': the QX3 iter3 growth ODE with this k_J(a), Delta chi^2 <= 4. The solver is generalised to any k_J(a).
  Known answer K1: k_J(a) = mu0 a^(3 beta) through the generalised solver must reproduce iter3's g2 at (beta, mu0) =
  (-1, 1e3) to 1e-6 in Delta chi^2.

## Cluster predictions and label

iter_2's predictor, unchanged: X-COP captured at z_c = 0.5, groups at z_c = 1, f_cap 0.76, the dust tracing the baryons,
the law on the total field. X-COP gets the HO1 line. Groups: at least 16 of 20 with both points within 2 sigma_log, required
for BOTH stellar allowances (strict); the result with either allowance is reported.
- PASS if the window is non-empty and at least one member passes X-COP and groups on both footings. Report the fraction of
  window members that pass; a pass on part of the window is labelled as such.
- FAIL (no window) / FAIL (clusters) otherwise. Sensitivity at z_c = 1 and 3 for G3b and the X-COP/group epochs is reported
  with no label.
- MUTATE 1: the 12 massive systems' M_b x 10 must strictly shrink the analytic-gate cell set (G3b has power).
  MUTATE 2: f_cap = 0 must reproduce QX2 iteration 1's X-COP mean to 1e-3. MUTATE 3: f_cap x 3 must move it by > 0.1 dex.
