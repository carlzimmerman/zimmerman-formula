# C-H exact nonlinear clock-focusing gate

2026-09-05. Continue the same C-H action, on its original smooth compact
clock-leaf domain. No new action, no commit/push. Initial HEAD 129311b8e;
HEAD advanced to 8e9d8c601 during this study. Other contributors' dirty
changes are out of scope; the manifest hashes the actual dependencies.

Test the exact branch with vacuum de Sitter physical metric, U and heat
field W constant, multipliers zero and unit-gradient geodesic clock X=1.
Derive rather than assume vanishing acceleration, all auxiliary first
variations, the metric equations and their preservation before any caustic.
Do not assign a finite q'(0): use the continuous first variation of q(|p|²).

Construct a periodic family P(q)=-p0 sin(kq) of initially tilted clock
geodesics and obtain their exact characteristic map, reconstructed clock,
Jacobian and invariant expansion. Determine whether the first caustic is
finite, treating the threshold/equality and Minkowski limits separately.
Verify compact clock-level caps rather than pretending t=0 is a clock leaf.

Exact SymPy geometry and characteristic identities; independent solve_ivp
integration of geodesics/Jacobi equations, no randomness; float64 comparisons
before crossing. Finite run grids and tolerances are written in the manifest.
The exact proof, not a plot or finite scan, supports any universal statement.

An invariant clock/leaf singularity on an exact solution is a restricted
nonlinear obstruction, not a proof of ghost, acausality, failure of local
existence/uniqueness, or nonexistence of all relativistic MOND. A primordial
origin and abundance are not derived by declaring the field a clock.
Default exit0 means diagnostics verified; failures exit1; --require-closed
exits2 because the full theory remains OPEN.
