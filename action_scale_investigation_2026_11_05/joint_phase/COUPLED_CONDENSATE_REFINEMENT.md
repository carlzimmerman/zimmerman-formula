# Derivative refinement and symmetry extension — 2026-11-07

The first recorded run passed 117/120 checks, including all eight Lean
certificates. Three centered logarithmic finite differences at x=3.1 failed
the 1e-7 comparison. The exact mass formula has a pole at pi, so the leading
O(step^2) difference error needs testing. Keep the original run and inputs.

New checker: evaluate centered steps 1e-5 and 0.5e-5, use Richardson
(4*D_half-D_full)/3, and record both relative errors. Do not relax the tolerance.
All other physical assumptions, fixtures and checks remain unchanged. Add a
symbolic identity for the exact logarithmic mass derivative. If the refinement
does not pass, diagnose further rather than interpreting it as physics.

After this test, inspect a symmetry-based coupling identification analytically:
O(3) potential lambda*(phi^2+2|chi|^2-v^2)^2/4. Test whether its continuous
vacuum manifold admits the necessary nonzero minimal wall tension. This is
an additional analytic route, not a new adopted action or numerical halo solve.
