# AC12 frozen criteria: is the Sun's own charged halo carried with the Sun? (AC2q and v3s side by side)

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. Astra's AZ37 files are read only, never edited.

## Why

AC11 (44192e0129, B2e): the Sun's own static khronon charge q_sun = Phi_N/gamma exceeds the Galactic
rho0 (0.0447 / 0.0514 Msun/pc^3) by 1.0-1.6e3 at 1 AU and equals it at r_eq = 1,007-1,562 AU. So AZ37's and
AC11's AU-scale tests froze the wrong background. AC12 asks what the khronon flow does inside the Sun's halo.

## Derivation to be checked (sympy), then solved

The sigma Euler-Lagrange equation of the PN Lagrangian (AC7/H4 at mu_K = 0) is charge continuity,
d_t q + div(q v) = 0, with v = -grad sigma (Hamilton-Jacobi form of Xi = phi - sigma_t + |grad sigma|^2/2).
H0 (sympy) re-derives this from the sigma-dependent part P.grad Xi.

Suppose the charge pattern is stationary in the Sun's frame, q(x - V t). In that frame the flow relative to
the Sun is w = v - V, and continuity becomes div(q w) = 0. Take w -> -V far away (the Galactic khronon is at
rest while the Sun moves) and q = rho0 (1 + r_eq/r) (+ s^2 for AC2q). Writing w = V grad(u(r) cos theta), u
solves

    q (u'' + 2u'/r - 2u/r^2) + q' u' = 0,   u -> -r (r -> inf),   u regular at r = 0.

Inside the 1/r halo the regular solution is u ~ r^sqrt(2). In units x = r/r_eq the problem is universal.
For AC2q, the clock's s^2 = 2 rho_DE (bound) is added to q. The O(s^2 v/c) parts of the time-derivative
term are dropped; they are bounded and reported, not graded.

## Tests

- H1 (co-motion). Integrate outward from x0 with the Frobenius start, fit u = alpha x + beta/x^2 on
  x in [50, 200] (where q is uniform to 2 %), and rescale to alpha = -1. Report
  f(x) = max over theta of |w|/V = max(|u'|, |u/x|) at 1 AU, 9.58 AU and r_eq, for every Lstar set and
  both footings, for v3s (s = 0) and AC2q.
  - Convergence: two x0 (1e-7, 1e-8) and two rtol pairs (1e-10/1e-12, 1e-12/1e-13). f must agree to
    <= 1e-6 relative.
  - Fit check: the residual of the two-term fit on [50, 200] must be <= 1e-4 relative.
- H2 (local Mach number). Phase speed c_ph(r) = Omega'(k = 1/r)/k from AC11's on-region system (its
  `system()`, reimplemented here verbatim), evaluated with the local charge q(r) in place of rho0.
  M(r) = f V / c_ph at 1 AU, 9.58 AU and r_eq, for V = 220 and 369 km/s.
- H3 (self-consistency of the kinematic halo). In the Sun's frame the flow's Bernoulli term is
  Xi_kin = |w|^2/2 - V^2/2. B(r) = max over theta of |grad(|w|^2/2)| / |grad Phi_N|.
  - The kinematic halo (the Sun's static charge carried by the flow) is self-consistent at r only if
    B(r) < 0.1. Otherwise the flow reshapes the charge, and a nonlinear solve is required.
- H4 (what the matching region can do at the planets; reported). Assume the response near r_eq is at most
  the local charge itself (|dq| <= q, a nonlinear cap). The relative tidal acceleration at r is then at most
  (4 pi/3) * 2 rho0 r^3 / M_sun. Also report the screened metric effect of a flow-induced charge
  dq ~ max(B, 1) q_sun at 1 AU, relative to g_N: max(B, 1) * 2 r^2 / Lstar^2.

## Known answers and control (separate outputs)

- KA1: halo off (q = rho0 uniform) gives u = -x exactly, f = 1 (relative flow = V, as AZ37/AC11 assume).
  The H2 phase speeds at 1 AU and 9.58 AU must equal AC11's stored ac11.json values to <= 1e-9 relative.
- KA2: the inner log-slope of f over x in [1e-6, 1e-5] equals sqrt(2) - 1 to <= 1e-3.
- MUTATE (AC12_MUTATE=1): flip the sign of the q' u' term, i.e. transport against the gradient. The inner
  exponent then becomes p = sqrt(3) - 1, so the slope of f is sqrt(3) - 2, not sqrt(2) - 1. KA2 must FAIL in the mutate.
  If it does not, the slope check has no power.

## Lines (per footing and Lstar set; v3s and AC2q graded separately)

- CO-MOVING SUBSONIC CORE at 1 AU if f(1 AU) V < c_ph(1 AU) for both V, and B(1 AU) < 0.1. AZ37's
  AU-scale resonance is then absent in the kinematic picture.
- SUPERSONIC at radius r if M(r) > 1. The resonance is present there, with pole cosine 1/M.
- KINEMATICS NOT SELF-CONSISTENT at r if B(r) >= 0.1.
- The complete moving-Sun label stays AZ37's: PASS needs the full nonlinear moving branch and its metric
  response, which AC12 does not solve. AC12 can therefore only sharpen NO VERDICT, unless H1-H3 expose a
  physical inconsistency (an imaginary c_ph with q > 0, or no regular solution), which would be a FAIL
  candidate. No alpha_1 or alpha_2 is claimed; no static potential is divided into a gravitomagnetic
  coefficient.
