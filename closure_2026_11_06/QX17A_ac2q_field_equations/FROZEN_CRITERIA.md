# QX17A_ac2q_field_equations: FROZEN CRITERIA (committed alone, before any script)

Owner 11-06 "keep grinding on it", after QX17 (full covariant equations of v3s, CERTIFIED). This lane does the same for the
**AC2q candidate** (AC7 b0d44a6952; not adopted). Adopts nothing. kappa = 1/2 FITTED. Not theory closed.
Lane id: first committed as QX18 (1b39bcb871), which collided with the parallel QX18_elliptical_gate lane; renamed to QX17A before any script (`ls`, `git log --all | grep QX17A`: empty). Criteria text otherwise unchanged.

## Action (AC7; c = 1, K = 4 pi G, Mpl^2 = 1/(8 pi G))

    L/sqrt(-g) = R/(4K) + X - V(phi) + P.A - W(K|P|) - gamma { F(Pi + 2X) - (2X)^2/2 } + lambda n.P

The clock is phi (tau = phi), Q = |d phi|, X = Q^2/2, n = -d phi/Q, A = -h.d ln Q, Pi = D.P, F = [max(.,0)]^2/2.
There is no K(Q) sector. QX17's definitions otherwise.

## Checks (PASS = relative residual <= 1e-10 at every test point; same method as QX17: jet variation, 2+1, 3 seeds,
n.P = 0 by P = h.V, Sigma = Pi + Q^2 > 0 branch, generic test polynomials for W and V)

- **K1** P equation, **K2** phi (khronon) equation including -V'(phi), **K3** metric equation: closed forms in RESULT.md
  against the direct variation.
- **K4** FRW (P = 0): the stiffness stress tensor vanishes identically and the phi equation is box phi = V'
  (sympy, from the closed forms).
- **K5** n.n T of the P + stiffness sector = Pi (1 - gamma Q^2) + gamma Pi^2/2. In unitary gauge that is the record's on-region
  T_on = -2 gamma X D.P (LEAN QX1.ac2q_on), plus v3s's gamma F.
- **MUTATE**: drop the -2 gamma Q^2 Sigma_+ n n term from the metric equation and the -2 gamma (Sigma_+ - Q^2) piece from the phi
  current. K2 and K3 must FAIL.

Labels: CERTIFIED / FAIL as in QX17.
