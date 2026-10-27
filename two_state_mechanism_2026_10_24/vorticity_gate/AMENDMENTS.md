# Execution disclosures

The initial scan stopped in its gradient check before any phase trajectory.
At the innermost mass cell dE/dx is 6.77e-9 while total energy is order unity.
Subtracting total energies at dx=1e-5 lost precision. A step study confirmed
cancellation: the apparent relative error grew as the step shrank, while
outer derivatives agreed. The check now uses a fourth-order centered formula
with dx=.01 for derivatives below 1e-6 and .001 otherwise, retaining the
original 2e-5 tolerance. No energy, gradient, physical parameter or ODE changed.
The old source and failed run are retained as historical evidence.

The first gradient-damped uniform-grid probes stopped on the concentrated
massive profile: assigning half a cell's mass inside its geometric midpoint
made u exceed a0, despite the underlying continuum profile being admissible.
The step study found approximate maxima 1.12–1.54 versus exact values below
0.83. The within-cell enclosed fraction is now calculated from the initial
positive mass profile, and used consistently in u, the adjoint gradient,
Hessian and F-mass diagnostics. This fixes the quadrature representation;
no physical mass or saturation threshold changes. A regression check on all
four uniform-grid profiles requires their initial enclosed fields to agree
with the continuum expression to 1e-12. Earlier results are superseded.
