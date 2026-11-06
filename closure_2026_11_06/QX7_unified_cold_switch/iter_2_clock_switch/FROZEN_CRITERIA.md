# QX7 iter_2 frozen criteria: stiffness switched by the cosmic clock (a late-heating cold dark energy)

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Runs whatever iter_1's outcome.

## Mechanism, in covariant form

p = A(tau) (Q - 1)^2, with an explicit dependence on the khronon (or AC2q clock) value. tau is a scalar, so this is covariant.
The khronon's normalisation is already fixed by K(Q), so no reparametrisation symmetry is broken beyond what K(Q) breaks;
this is stated, not graded. The Jeans length is uniform on each leaf: lambda_J(a) = lambda_3 (a/a_3)^m, physical, with
a_3 = 1/4 (z = 3). Superhorizon modes see a leaf-uniform switch, which is consistent by construction. Two constants:
(lambda_3, m). In the linear growth ODE this is QX3 iter3's solver with k_J = mu0 a^(3 beta), where beta = -m/3 and
mu0 = 2 pi a_3^m / lambda_3. That map is the known answer K1: at m = 0, the code must reproduce iter3/iter2's G2 at the same
mu, Delta chi^2 to 1e-2.

## Grid

m in [0, 8] in steps of 0.25 (33 values); lambda_3 log-spaced from 1e-4 to 0.2 Mpc physical (41 values). G2' is evaluated only
where the analytic gates pass.

## Non-cluster gates (fix the window)

- G2' (CMB-lensing growth): QX3 iter3's G2' ODE, Limber ratio, amplitude refit. Pass if Delta chi^2 <= 4.
- G4' (forest): physical lambda_J(z=3) <= (0.42/h)/4 Mpc, i.e. 0.42/h comoving (X22, as QX3).
- G3' (reference galaxy, as QX3): lambda_J(z_c = 2) >= r_ta(10^11.5 Msun, z_c = 2), with r_ta from
  rho_ta = 5.55 rho_m0 (1+z_c)^3.
- G3b (law-obeying massive systems): no capture for each Humphrey elliptical (M_b = ups_krou L_K) and the 5 highest-M_b SPARC
  quality galaxies (M_b = 0.5 L[3.6] + 1.33 M_HI). The perturbation mass is M_t = M_b (1 + omega_d/omega_b): the dust is cold
  on large scales before the capture decision. The test: lambda_J(z_c) >= r_ta(M_t, z_c) at z_c = 2. Sensitivity at z_c = 1
  and 3, and with M_t = M_b, is reported and carries no label.

## Cluster predictions (no cluster input)

For every window member, a system is captured if lambda_J(z_c) < r_ta(M_t, z_c), with z_c = 0.5 for X-COP and z_c = 1 for groups
(conventional assembly epochs, stated now). If it is captured, the dust inside r is M_d(<r) = f_cap (omega_d/omega_b) M_b(<r),
with f_cap = 0.76 (X22): the dust traces the baryons, which is a stated assumption. The prediction is then
M_pred(r) = M_law(G (M_b + M_d)/r^2), the law applied to the total Newtonian field, both footings. If not captured,
M_pred = M_law(M_b) (QX2 iter 1 for X-COP, QX5 F = 1 for groups).
- X-COP: HO1 line |mean Delta| <= 0.05, rms <= 0.10 (Delta = log M_obs - log M_pred).
- Groups: the QX5 group rule (both groups' points inside their stated mass errors x2, i.e. |Delta| <= 2 sigma_log, for at least
  16 of 20 groups); the median Delta is reported.
- The window passes clusters if X-COP AND groups pass for at least one member; every member's result is reported (no
  cherry-picking: the label states whether the pass holds over the whole window or only part of it).

## Galaxy-side rechecks

If no galaxy or elliptical is captured (G3', G3b), SPARC/RAR, ellipticals, KiDS isolated-galaxy lensing (to 300 kpc) and
Cassini/PPN are unchanged from the record: the hot dust's mean density rho_d0 adds g_d(1 AU) = (4 pi/3) G rho_d0 r. That is
computed and must be <= 1e-15 g_N. Stated, not otherwise regraded.

## Label

- PASS: non-empty window AND the cluster predictions pass, as above.
- FAIL (no window) if no member passes G2', G3', G3b and G4'. FAIL (clusters) if a window exists but the predictions fail.
- MUTATE 1: flip G3b (require capture of the ellipticals); members must then appear, so the analytic gates have power.
- MUTATE 2: no capture anywhere (f_cap = 0) must reproduce QX2 iter 1's X-COP mean (+0.468 canonical / +0.435 alt) to 1e-3.
- MUTATE 3: f_cap x 3 must move the X-COP mean by more than 0.1 dex (the predictor is sensitive).
