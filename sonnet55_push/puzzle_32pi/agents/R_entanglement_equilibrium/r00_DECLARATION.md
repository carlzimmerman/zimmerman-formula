# r00: pre-declaration (written BEFORE any scale-computation script was run)

Lane R: Jacobson's entanglement equilibrium (arXiv:1505.04753v4, opened and read in full), applied to a ball that is NOT small compared with
the de Sitter radius L, and to a ball around a point mass in the Newtonian regime.
c = G = 1 for geometry; hbar = 1 for the modular energy; L = de Sitter radius, H = 1/L, Lambda = 3/L^2 (d = 4), rho_Lambda = Lambda/(8 pi G).

## What I already knew or believed before running anything (disclosure)
- The small-ball chain of the paper (eqs 3-8, 19, 22-27): delta A|_V = -Omega_{d-2} l^d G_00/(d^2-1), delta<H_zeta> = Omega_{d-2} l^d/(d^2-1) delta<T_00>,
  so G_00 = 8 pi G T_00 with Lambda an INTEGRATION CONSTANT (paper eq 25-26). I expected to reproduce it.
- By hand (not scripted at declaration time) I believed: for a spherically symmetric perturbation of the S^{d-1} slice, the exact fixed-volume area shift equals
  -8 pi G * integral of (conformal Killing weight) * delta rho, for EVERY ball radius (so the leading Einstein equation would not fail at O(1) at first order),
  and that the exact de Sitter ball volume is V = 2 pi L^3 (x - sin(2x)/2), x = R/L (the task text has a factor 2 missing: V(pi) must be 2 pi^2 L^3).
  Decisions below are made by the scripts, not by these beliefs.

## The two constructions
C-dS: geodesic ball of geodesic radius R = x L on the time-symmetric slice S^{d-1}(L) of dS_d (K = 0), exact A(x), V(x); equilibrium condition =
      delta S = delta A|_V/(4G) + 2 pi delta<X> = 0, with delta<X> the modular energy with the exact conformal-Killing weight of the ball.
C-N : geodesic ball centred on a spherically symmetric mass distribution in the weak-field (Newtonian) regime, with and without Lambda.

## Candidate radii x* (declared)
X1  x = pi/2       (equator: A extremal, boundary mean curvature 0, the conformal Killing vector becomes a Killing vector, modular T = T_dS)
X2  x = pi/4       (boundary area = half the dS horizon area, i.e. S_ball = S_dS/2)
X3  F(x) = 1/2     (the exact fixed-V area response to a uniform energy density equals half of the small-ball formula -Omega l^d G_00/(d^2-1)), d = 4
X4  |next term| = |leading term| in the series of F(x) in x^2 (d = 4)
X5  x = 1          (R = L)
X6  x = R*/L = sqrt(8 pi/3)  (R* = c/sqrt(G rho_Lambda): a target-related radius; included only to see what it is, flagged as target-aware)

## Candidate accelerations (declared; each has an explicit meaning)
Q1  a_mod(x) = 1/(L tan(x/2)) : 2 pi T_c, with T_c the modular temperature at the ball centre (unit-surface-gravity conformal Killing vector, xi_c = L tan(x/2))
Q2  k1(x) = cot(x)/L          : principal extrinsic curvature of the ball boundary in the slice (mean curvature = (d-2) k1)
Q3  a_st(x) = tan(x)/L        : proper acceleration of the static observer at the ball boundary (static patch centred on the ball)
Q5  g_eq(x): Newtonian acceleration G M/R^2 of a point mass M at the centre whose exact modular-energy area deficit 8 pi G M xi_c equals the exact
      Lambda area deficit A_flat(V) - A_dS(V) of the same ball (a mass-equals-vacuum-energy crossover; NOT expected to be a fixed acceleration)
Q6  (structural, not a number): the acceleration at which the exact nonlinear equilibrium relation deviates from first order by O(1) in the Newtonian regime
Also: sign of dA_V/dL (does the fixed-V area have an extremum in L for any x?).

## Bookkeeping to be reported for each candidate
value in units of H; value in units of sqrt(G rho_Lambda) (H = sqrt(8 pi/3) sqrt(G rho_Lambda), c = 1; variable held fixed: L, i.e. Lambda);
exact form / pi-content (algebraic or transcendental). Comparison with a0 = H/Z, Z = sqrt(32 pi/3), i.e. a0/H = 0.172747, a0/sqrt(G rho_Lambda) = 1/2,
is done ONLY at the end of r04, and against six decoy targets (Z' = 5, 5.5, 6, 2 pi, 6.5, 1.05 Z) for calibration.

## Pre-declared success / failure criteria
- SUCCESS (derivation type): a candidate defined without reference to a0 whose value equals 1/Z (in H units) or 1/2 (in sqrt(G rho_Lambda) units) by an exact
  identity (symbolic, or numerically to 1e-10), and not reproduced equally often by the decoys.
- SUCCESS (test type): a computed finite radius/acceleration at which the exact equilibrium condition departs from 8 pi G at O(1), mapping to a definite acceleration.
- Otherwise: the verdict is SHARP NO-GO or NOTHING NEW, stated plainly.
