# AC17: v3s / AC2q nonspherical PN sign, UV symbol in every direction: PASS (scoped)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (5c1c453e79), frozen
before any script. Closes, at the scope below, AZ36's NO VERDICT on the full nonspherical PN-sign claim
(astra_goal_2026_11_05/AZ36_pn_sign, read only), and replaces V3X's ASSERTED line "O(GM/c^2 r) corrections
do not flip any sign" for the UV principal symbol. Script: ac17.py (sympy exact + mpmath 50 digits, one thread,
about 200 s).

## Result

Method: the khronon is written as an explicit Stueckelberg field, tau = t + sigma, on ANY static background
with conformally flat spatial metric, ds^2 = -N^2 dt^2 + Psi^4 dx^2, and arbitrary P0^i(x). This is exact,
with no PN expansion. Every static spherical background is of this form, and so is the Sun plus an external
field at the order V3X used. Fields: sigma, the polarization p^i and the lapse n. The quadratic action leads to
Euler-Lagrange equations, from which the UV symbol is read.

- **Exact closed form (v3s, on shell).**

      c^2(k) = gamma [ B_tau + x0 W'(x0) sin^2 theta_kP ] / [ (1 + gamma s)^2 + gamma mu^2/(K N^2) ]
      B_tau  = s + gamma s^2 + mu^2 (1-N)/(K N^2),    x0 = K|P|,    theta_kP = angle between k and P

  The kinetic coefficient is Psi^6 [N (1+gamma s)^2/gamma + mu^2/(K N)] > 0. Only the longitudinal p
  propagates; transverse p has no principal part (auxiliary, fixed by the W Hessian).
- **AC2q (on-region, its own clock):** B gains + 2X (1 - gamma s), the coupling becomes (1 + gamma s - 2 gamma X),
  and the kinetic coefficient gains + phidot^2 (1 - 2 gamma s)/N. All of these are positive for gamma s, gamma X << 1.
- **What this settles.** Along P (theta = 0) the result is exactly AZ36's radial theorem. Off P, the only new term
  is + x0 W'(x0) sin^2 theta, which is >= 0 because W is increasing (V3X's H >= K). The relativistic,
  direction-dependent correction therefore only raises the PN gradient weight rho_tau = s. It cannot flip the
  sign in any direction, on any such background, without a PN expansion.
- **Hypotheses the theorem rests on:** gamma > 0, s > 0 (switched-on branch), N <= 1, W' >= 0, and a background
  that solves the P equation (K Psi^2 W' Phat = a + gamma grad(N s_eff)/N, s_eff = s or s + 2X). That equation
  is used only through its contraction with P.
- **G2, the Solar background with the Galactic external field.** 873,600 points were checked, covering both
  models, both footings, g_ext of 1.9e-10 and 2.3e-10 m/s^2, 13 directions of P_ext at its unscreened bound
  g_ext/(K c^2), nodes 1-1000 AU, W' brackets M = 1, 3.2 and 10.24, and 400 directions of k.
  - 0 points have B <= 0, a kinetic coefficient <= 0, or c^2 <= 0.
  - min B/s = 1.0000000235.
  - c^2 runs from 9.8e-9 at 1 AU to 9.9e-12 at 1000 AU, i.e. gamma s = |Phi_N| (V3X's hedgehog cone).
  - The anisotropic gain is at most x0 W'/s = 1.2e-6.

## Known answers and controls

- K1: the full 4x4 symbol, with W' taken from the radial P equation, reproduces AZ36's c_rad^2 to 4.5e-48 on
  8 rows (both footings, 1-1000 AU). It is an independent numerical chain, not the closed form.
- K2: the PN limit, c^2 = gamma rho_tau (V3X W4c (c)), holds to 9.7e-9, which is O(gamma s).
- K3: with the P sector removed (P = 0, W = 0, mu = 0), the second-order Lagrangian is identically 0: sigma is
  pure gauge, as in GR.
- G1 counting: the EL equations carry at most two derivatives (no third- or fourth-derivative terms survive;
  the sigma-dot tilt terms cancel between grad.P and P.a). The lapse enters the sigma and p equations only
  below principal order. With the PN gravity term -|grad n|^2/2K, n decouples at principal order.
- MUTATE (gamma -> -gamma, separate outputs ac17_MUTATE.*): bites. All 873,600 points have c^2 <= 0, because the
  kinetic coefficient turns negative; K1 still reproduces AZ36's formula at the flipped gamma (7.7e-48).

## Failures and corrections disclosed

- First run (first_run_K3nan_killed.out): K3 printed FAIL because W was Taylor-expanded at |P| = 0, which gives
  nan. The run was killed by hand during G2, which was too slow (symbolic background derivatives at every node).
  - K3 was then evaluated with W = 0, as the criteria's "P sector removed" means.
  - The criteria's wording "P0 = 0, mu = 0, gamma = 0 => sigma sector empty" was wrong: with P0 = 0 but p kept,
    sigma still couples to p, because P is an independent field. The corrected statement is in the K3 line.
- Second run (second_run_pars_nameerror.out): a NameError from that speed-up, fixed, then rerun.
- No graded number changed between runs except by completing them.

## What it does not show

- It covers the UV principal symbol only. The finite-wavelength (non-WKB) spectrum's relativistic corrections
  are not covered; V3X's PN spectrum stays UNDECIDED on its ladder line.
- Metric perturbations beyond the lapse are argued subprincipal by derivative counting, not computed: they
  couple to the P sector at one derivative and carry their own k^2/K operator.
- Not covered: the switch interface, moving or rotating sources (AC11/AC12/AC15), nonlinear well-posedness
  (AC16 FAIL) and causality (AC18).
- The external-field background is not a solved P configuration. Its P_ext is bounded, and the on-shell form is
  used.
