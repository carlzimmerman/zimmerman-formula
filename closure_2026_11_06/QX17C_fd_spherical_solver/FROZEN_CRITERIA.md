# QX17C FROZEN CRITERIA: a convergent solver for the static spherical v3s equations (2026-11-06)

Frozen before any script. Adopts nothing. kappa = 1/2 FITTED. Not theory closed.

**Why this lane exists.** QX17B S-sph is FAIL as frozen (c3cebe6cd6). scipy solve_bvp hit its mesh-node limit on the
KNOWN case and on the Sun's full solve. That verdict stays on the record. This lane re-solves the *same* problem with a
different method and grades the *same* gates.

## Problem (identical to QX17B)

- Equations: QX17B RESULT §3 and sph_solve.py, i.e. the weak (B = 1, eps -> 0) and full (areal-gauge GR) systems.
- Body: uniform ball with the same tanh edge (width 2e-3 R).
- Footings: canonical (a0 9.3603e-11, Lstar 21.7 pc) and alt (a0 1.1312e-10, Lstar 22.9 pc). Never pooled.
- Bodies: Sun (M_sun, R_sun) and galaxy (1e10 Msun, R = 0.5 kpc).

## Method

Unknown: Y(s) on a grid from the exact centre s = 0, where Y(0) = 0 (no artificial inner radius). The grid is geometric
from min(1e-3 R/Lstar, 1e-3) out to s_out, plus a uniform cluster around the ball edge.

Equation (scaled, as sph_solve.py):

    (1/H) [ Z_{i+1/2} - Z_{i-1/2} ] = 2 ( B fW(Y/B) - (1 + eps Z/2) G )
    Z_{i+1/2} = Delta(s^2 Y / B) / (h s_m^2 B_m)

- **Mass:** m(s) comes from the same discrete Z (it telescopes). Weak G equals gN + Y exactly.
- **Full mode:** B, m and the TOV pressure come by quadrature from the current Y. Solved by damped Newton (weak
  tridiagonal Jacobian, defect correction).
- **Outer boundary:** the decaying modified-spherical-Bessel mode k_1 about law S, with k^2 = 2(1/(1 - Y_S)^2 - 1).

## Convergence rules (a row with no convergence gets NO VERDICT, never PASS)

- **C1 Newton:** max scaled residual <= 1e-9.
- **C2 grid:** each graded number changes by <= 10 % of its gate tolerance when the grid density doubles.
- **C3 outer edge:** each graded number changes by <= 10 % of its gate tolerance when s_out goes up 10x.

## Gates (same tolerances as QX17B)

| gate | what | tolerance |
|---|---|---|
| G1 KNOWN | galaxy, weak, Lstar = 1e-3 pc: law S at 1-30 kpc | <= 1e-3 |
| G2 | Sun full: y / g* over 10 AU to 1e-3 Lstar | within 1 % |
| G3 | Sun: full vs weak y, 2 R_sun to 1e3 Lstar | <= 10 U_max (U_max = M/R) |
| G4 | galaxy full: law S at 1-30 kpc | <= 1e-2 |
| G5 | galaxy: full vs weak y, 2 R to 1e5 pc | <= 10 U_max |
| X1 cross-method | weak exterior y vs QX17B's converged solve_bvp runs (Sun weak, galaxy weak), on their common range | <= 1e-3 relative |

## Twin and label

**MUTATE:** drop the phantom-mass feedback (G = gN instead of the total). The solver must still converge, and G1 and G4
must FAIL.

**Label:** CERTIFIED (solver) iff G1-G5 and X1 PASS, C1-C3 hold, and MUTATE fails G1 and G4.

**Not gated, recorded:** the Sun's g/g_lawS at 1, 3, 10, 30, 100, 1000 Lstar (isolated point Sun, no Galactic field).

Small job: one thread, < 1 GB.
