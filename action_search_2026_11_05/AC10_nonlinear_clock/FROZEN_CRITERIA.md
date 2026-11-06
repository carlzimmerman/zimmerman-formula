# AC10 frozen criteria: AC2q nonlinear planar evolution, does it fold like v3s (X14)?

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. Footings 9.3603e-11 / 1.1312e-10 m/s^2, never pooled.

## Question

CLOSURE.md section 3 says AC2q "inherits X14's caustics generic" by inference (X14:
rebuild_2026_10_22/X14_caustic_completion, criteria 68bf6e379d). AC10 tests it directly. AC2q's PN system
(AC7, ac7.py q2) in 1D planar symmetry is evolved nonlinearly, like for like with X14's F2 setup (a cold
khronon stream crossing a baryon sheet). Two questions: does it fold, and does either AC2q-specific piece
(the clock's s^2 charge, or the stiffness switched on the charge) regularize it?

## Planar reduction used (stated, then checked symbolically)

From AC7's Lagrangian: the charge Pi = D.P + C2, C2 = s^2[(1+sigma_t)^2/(1+phi)^2 - sigma'^2] ~= s^2 at PN order.
- P' = Pi - s^2, so P sees only the excess over the clock background.
- Poisson sees Pi; the uniform clock background s^2 is the cosmic background (swindled). Gravity therefore also
  sees the excess Pi - s^2.
- Velocity v = -sigma'; the label acceleration is a = K(M-1) S_ex(<x) - K Sigma_b(<x) - gamma d_x max(Pi, 0)
  (planar Green's function: symmetric halves). Pi is carried by the labels (continuity).
- v3s (X14 known answer) is s = 0 with the switch on D.P = Pi.

Corrections dropped: O(gamma s^2) <= 4e-17 (AC9), O(v^2/c^2, phi) <= 1e-6, and the Helmholtz screening term
K M s^2 l^2 <= 1e-6 for l <= 1 Mpc. S1 (sympy) must confirm that the 1D Euler-Lagrange equations of AC7's
Lagrangian reduce to this system at s^2 -> PN order, with residual 0 at the stated order.

Per-label J equation (pressure-free): J'' = -K rho_b J + K(M-1)(Pi_0 - s^2 J).
Analytic predictions frozen here:
- A1 (v3s, X14 F2): Pi_0 = rho_ph, s = 0 gives J = 1 - K Sigma tau/w + omega_p^2 tau^2/2. It folds iff
  omega_p tau_f <= 1/sqrt(2).
- A2 (AC2q, clock-only stream: Pi_0 = s^2, no phantom) gives J = 1 - (K Sigma/(w Omega)) sin(Omega tau), with
  Omega^2 = K s^2 (M-1). It folds iff Omega tau_f <= 1. The threshold is 1, not 1/sqrt(2).
- A3 (soft, Pi_0 < 0, switch off): folds for every datum.

## Numerics

Lagrangian labels (N cells), positions and velocities, DOP853 (rtol 1e-10, atol 1e-12). Cell J = dx/dq;
cell charge Pi_0/J. A smooth sheet Sigma_b erf(x/(sqrt 2 w_b)), w_b = 1e-3, in units w = 1, K Sigma_b = 1.
The stream occupies labels x0 in [-3, -0.05] at velocity 1. A fold is the first time the minimum interior J
(excluding the 5 % of cells at each stream edge) reaches J_thr = 1e-3, before t_max = 6. Regular means the
interior J stays >= 0.05 to t_max. Anything else is UNDECIDED.
- Convergence ladder: N = 2000, 4000, 8000. The fold time must change by <= 1e-3 (relative) between 4000 and
  8000, and the fold/regular label must not change between rungs.
- J_thr sensitivity (reported, not graded): 1e-4.

## Rows

Physical rows, read at run time from X14's results json (F5 numbers): 5 radii (11, 33, 73, 91, 156 kpc),
w = 68.75 and 74.8 km/s, M-1 at both ends of X14's bracket, both footings. Planar map: K Sigma_b = 2 g, so
tau_f = w/(2g). Charge Pi_0 = rho_ph + s^2, with s^2 = 2 rho_DE (bound, framework-native:
K s^2 = 32 pi a0^2/c^2). Stiffness c_s^2 = gamma Pi c^2, gamma = 2 pi Lstar^2 (geometric), Lstar 21.7/22.9 pc
and 90 pc. The same rows are also run as a clock-only stream (rho_ph = 0) and as a soft stream (Pi_0 = -rho_ph).
v3s twin: s = 0, switch on Pi.

Stress rows (dimensionless, reported, and graded only as checks on A1/A2):
- clock-only Omega^2 tau_f^2 in {0.8, 1.2}: A2 predicts fold, no fold;
- phantom omega_p^2 tau_f^2 in {0.4, 0.6}: A1 predicts fold, no fold.

## Checks

- S1: the symbolic reduction (above).
- K1: zero charge and no pressure. The coupled label code equals independent per-label integration
  (J from finite differences), with fold-time difference <= 1e-6. The thin-sheet delay after crossing must equal
  v_cross/(K Sigma_b) within 2 %.
- K2: the v3s twin reproduces A1's threshold on the stress pair. K3: AC2q reproduces A2's threshold on its pair.
- MUTATE-A (separate outputs): Sigma_b -> -Sigma_b (repulsive) on the zero-charge stream must be REGULAR.
- MUTATE-B (power gate): an AC2q stress row with Mach 0.3 (stiffness raised by hand, clock-only charge
  Pi_0 = 0.1) must be REGULAR. If it folds, the method cannot see pressure regularization and no verdict stands.

## Verdict lines

- CAUSTIC-GENERIC (inference confirmed) if every physical AC2q row, on both footings, folds converged; the
  soft rows fold; and every AC2q fold time is within 1e-2 (relative) of its v3s twin.
- REGULAR (inference refuted) if any converged physical AC2q row is REGULAR.
- NO VERDICT if convergence fails on a physical row, if S1 or K1-K3 fail, or if a MUTATE does not bite.

Scope: planar, frozen M per row (linearized W about the background, as in AC7), pressure-free shock handling
(inviscid), no 3D, no moving Sun (AC11), no post-fold continuation. X > 0: at PN order X = s^2[(1+sigma_t)^2
/(1+phi)^2 - v^2]/2. The script reports the minimum X/X_bg up to the fold. A fold makes v' diverge with v
finite, so X > 0 is not what fails there. That statement is checked (min X/X_bg > 0.99), not assumed.
