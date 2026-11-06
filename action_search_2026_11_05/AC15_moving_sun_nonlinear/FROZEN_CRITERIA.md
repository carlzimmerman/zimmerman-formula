# AC15 frozen criteria: the moving Sun, nonlinear (v3s and AC2q side by side)

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. Astra's AZ37 files are read only, never edited.

## Why

AC11 (44192e0129) and AC12 (946cf79e1a) left the moving Sun NO VERDICT. AC12 held the Sun's static
charge q_sun = Phi_N/gamma fixed and solved only continuity, div(q w) = 0. It found that the flow's
Bernoulli term is not small (B 0.09-0.38 at 1 AU, 6-23 at 9.58 AU), so the charge cannot be held fixed.
AC15 solves the coupled problem: the charge is set by the flow, and the flow by the charge.

## S1: the equations (sympy, exact)

PN Lagrangian at mu_K = 0 (AC7 / H4; AC12 H0), with the P mass term written out:
L = P.grad Xi - (gamma/2)(div P)^2 - (K M_theta/2) P^2,  Xi = phi - sigma_t + |grad sigma|^2/2,  v = -grad sigma.

- S1a. The P equation is grad(Xi + gamma q) = K M_theta P, with q = div P. The right side is the
  screening term. Its size relative to gamma grad q is at most 2 M_theta (r/Lstar)^2. This is reported at
  10 AU and must be <= 1e-9, in which case it is dropped.
- S1b. For a pattern stationary in the Sun's frame (sigma(x - V t)), Xi = phi + (w^2 - V^2)/2 exactly, with
  w = v - V. With the Galactic khronon at rest far away (q -> rho0, v -> 0) this gives global Bernoulli:
      gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2,   c_gal^2 = gamma rho0,   Phi_N = GM/r.
  It holds everywhere the P equation holds, across any kink in sigma included, because Xi + gamma q is
  continuous. There is one constant, not one per streamline.
- S1c. The gradient of the Hamilton-Jacobi form, together with charge continuity, is barotropic Euler with
  h = gamma q (p = gamma q^2/2, sound speed^2 = gamma q c^2) for smooth irrotational flow. That is the
  system evolved in S2.
- KA1 (static limit = C6P hedgehog). At V = 0 and w = 0, S1b gives gamma q = c_gal^2 + Phi_N: the hedgehog
  q_sun = Phi_N/gamma (AC11 B2e) on the Galactic background. Its enclosed charge M r^2/Lstar^2 gives
  C6P's anomaly GM/Lstar^2.
- KA2 (Bernoulli off = AC12). With q held fixed, the stationary continuity operator is AC12's
  div(q w) = 0 (sympy identity).

## S2: the solve (axisymmetric 2D, time-dependent to steady)

Units: accretion radius R_A = 2GM/V^2 and V (so GM = 1/2), density in rho0. The only parameters are
M_inf = V/c_gal and the inner radius. Every cell of both footings (Lstar canonical 21.68/24/27, alt
22.85/24/24.60 pc; V = 220, 369 km/s) has M_inf in [234, 490]. Runs use M_inf = 234 and 490, which bracket
the grid. Each cell is graded with both runs, rescaled as below; the two must give the same label.

- Finite volume in (ln r, theta), r in [2, 2000] R_A, HLL fluxes, MUSCL minmod, RK2, CFL 0.4,
  well-balanced geometric pressure sources. Reflecting axes. Uniform wind w = -V z at outer inflow faces,
  zero-gradient at outer outflow faces.
- Inner boundary bracket at r_in = 2 R_A: ABSORB (zero-gradient, no outflow from the core) and REFLECT
  (wall). The excised core's charge is bounded by the Bernoulli cap q <= rho0 + (Phi_N + V^2/2)/gamma
  (q >= 0), integrated inside r_in, and added as a centred point charge to the graded field.
  Planets sit at 27-735 R_A.
- Starts: UNIFORM (q = rho0, w = -V everywhere) and HEDGEHOG (q = static hedgehog, w = -V: S1b-consistent
  at t = 0). Both are run at M_inf = 234 with ABSORB, coarse. UNIFORM runs every bracket.
- Ladder: coarse (dln r = 0.05, 80 theta cells) and medium (0.025, 160). Medium is run for UNIFORM-ABSORB at
  both M_inf and for UNIFORM-REFLECT at 234.
- t_end = 3000 R_A/V. Checkpointed, resumable on SIGTERM, nice 10, at most 4 processes, one thread each.

## Graded observables (per footing, per Lstar, per V; v3s and AC2q)

The anomalous charge is dq = q - rho0 on the grid, plus the core point charge. Its potential solves
del^2 phi = 4 pi G dq (Legendre expansion, l <= 24). In SI the acceleration is G rho0 R_A times the code
value. Per cell, the code field is rescaled by the run's (M_inf_cell / M_inf_run)^2 when that is larger
than 1 (column charge scales as M^2), and by 1 otherwise.

- G1, planets. |a_anom(planet) - a_anom(Sun)|, maximised over theta, at Earth (1 AU), Mars (1.524 AU)
  and Saturn (9.58 AU), against C6P's per-planet bounds 8.7e-15 / 1.4e-15 / 7.0e-15 m/s^2.
- G2, annual (time-varying) part. A planet orbits through a pattern that is fixed in the Sun's frame. The
  amplitude is max over theta minus min over theta of the same quantity, against the same bounds.
- G3, Cassini. Q_eff = |a_anom, l = 2 part| / r at 9.58 AU, maximised over theta, against KT16's
  5.2e-27 s^-2. The Hees line 9.0e-27 is reported beside it.
- The static C6P hedgehog's own G1 numbers (GM/Lstar^2) are printed beside these for comparison.

## Known answers and controls (separate outputs)

- KA3 (gravity off). The uniform wind stays uniform: max |q - 1| and |w + z| <= 1e-10 at t = 50.
- KA4 (hydrostatic). With no wind (outer boundary held at the hedgehog), the static hedgehog stays within
  2e-2 of q at r <= 100 at t = 50.
- KA5 (hypersonic, ballistic). UNIFORM-ABSORB at M_inf = 490, medium. q at r = 20-100 and psi =
  10-80 deg from the upstream axis must match the pressureless point-mass focusing density within 5 %.
  That density sums the streams whose periapsis exceeds r_in, n/n0 = sum |db/dr|_psi / sin psi.
- MUTATE (AC15_MUTATE=1). Flip the sign of gravity on the charge (repulsive Sun). Charge is then swept
  out, and dq < 0 near the Sun must be detected: G1 at Earth must exceed 0.1 of the bound with the opposite
  sign of the UNMUTATED radial anomaly, or KA5's density must fail by more than 50 %. If neither happens,
  the grader has no power and no verdict stands.
- S1 sympy checks: residual 0.

## Steadiness, convergence, shock proxy

- Steady: every graded number changes by <= 5 % over the last 20 % of t_end. Otherwise the run is
  NOT STEADY. Its time-varying envelope (max over the last 20 %) is graded instead, and NOT STEADY is
  reported.
- Converged: every graded ratio changes by <= 30 % between coarse and medium, and no label flips.
- Shock proxy. The evolution uses Euler shock conditions, while the khronon conserves global Bernoulli
  (S1b). Each graded number is recomputed from the Bernoulli charge q_B = rho0 + (Phi_N + (V^2 - w^2)/2)/gamma
  (clipped at 0), using the simulated w. Grading with q and with q_B must give the same label.

## Lines

- PASS (moving Sun, scoped). G1, G2 and G3 are under their lines on both footings, every Lstar and V, in
  every bracket (both inner BCs, both starts, both M_inf runs, q and q_B), with KA1-KA5, S1 and MUTATE
  passing, steady or NOT STEADY-envelope graded, and converged.
- FAIL. Some cell is over a line in every bracket, on converged runs with all known answers passing.
- UNDECIDED. Over in some brackets and under in others (branch- or proxy-dependent). The splitting
  bracket is named.
- NO VERDICT. A known answer, S1, MUTATE or convergence fails.
- No steady solution. If neither start becomes steady, the label is decided on the envelopes as above,
  and "no steady state reached" is reported with it. Non-existence of a steady transonic solution is then
  a reported result, not a failure.
- Scope: PN order, mu_K = 0, screening term dropped (S1a), axisymmetric (Sun's velocity along the axis),
  Sun as a point mass outside r_in, Euler shock proxy checked by q_B. No PPN alpha_1 or alpha_2 is claimed,
  and no static potential is divided into a gravitomagnetic coefficient. AC2q differs from v3s only by
  s^2/rho0 ~ 4e-6 in the charge. This is reported, not run separately.
