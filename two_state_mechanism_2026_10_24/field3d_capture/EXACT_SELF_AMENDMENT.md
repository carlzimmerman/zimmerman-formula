# Exact self-energy amendment

The initial live suites spend most of their field time recomputing the energy
of isolated individual packets. That energy is exactly translation-invariant
in the continuum; fixed-box quadrature needlessly introduces a small self-force.
The revised evaluator computes every isolated Gaussian nonlinear self-energy by
an all-space radial integral, cached by mass and field parameters. It subtracts
those same self integrands from the 3D nonlinear mesh sum. Thus only nonlinear
interference between distinct packets needs 3D quadrature. This is the same
continuum functional, with a better quadrature decomposition. The analytic
quadratic terms remain unchanged. The force differentiates the revised discrete
energy, and state changes use its full finite difference.

A single T packet now has identically zero self-force and exact isolated energy
(up to scalar integration tolerance). This is not a return to spherical averaging:
every multi-packet interaction uses the complete vector sum at all 3D mesh points.
The exact isolated maximum also detects single-packet saturation independently
of mesh placement. Multi-packet saturation remains sampled, and the nonlinear
interference exterior remains truncated. The original suites are preserved as
quadrature/performance history; use the exact-self suites as final evidence.
