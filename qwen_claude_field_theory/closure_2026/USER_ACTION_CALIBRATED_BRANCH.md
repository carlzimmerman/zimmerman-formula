# Curved branch with the calibrated implicit kernel

The parametric kernel from USER_ACTION_KERNEL.md is inserted into the same
static spatial Routh equations, including finite xi and metric connections.
Its value, first derivative and second derivative are evaluated by monotone
inversion. Differentiating a local Taylor jet symbolically before replacing
its expansion point by the actual argument supplies the exact required J
derivatives; this is not a finite-polynomial replacement of the kernel.

Dimensionless parameters are g=0.35, ca=0.1, b=1, C=0.01, a0=1,
so a=4g-2ca=1.2 and the calibration A=1. Initial data have P=B=0,
P'=0.02, B'=-0.02, v=s(0.02), v'=0. The spatial constraint determines
nonzero conserved scalar flux, approximately -0.846868. This is not the
zero-flux calibration branch, nor a galactic baryonic boundary problem.

Four runs to x=0.02 complete:

| xi | rtol | maximum constraint error | maximum absolute P+B |
|---|---|---|---|
| 0.2 | 1e-8 | 6.58e-11 | 2.90689e-6 |
| 0.2 | 1e-10 | 1.13e-12 | 2.90689e-6 |
| 0.1 | 1e-8 | 7.93e-11 | 3.05060e-6 |
| 0.1 | 1e-10 | 2.34e-12 | 3.05060e-6 |

The logarithmic weak-field slip is stable against tolerance refinement,
unlike the energy residual. P and B are evolved independently. No PPN gamma
is computed from this local planar vacuum geometry, and the two potentials'
relation beyond leading weak-field order must use the actual metric.
The maximum J'(U)v-P' mismatch is 5.30e-4 or 7.12e-4 respectively; it is not
an isolated measurement of xi corrections because the flux and curved
background differ from the calibration assumptions.

Next construct boundary data with the calibrated scalar flux and physical
source conditions while satisfying the spatial constraint. Initial matching
of gradients alone does not select the desired MOND branch. No claim is
made that the displayed parameters pass full-theory or observational gates.

Command: `python3 qwen_claude_field_theory/closure_2026/user_action_calibrated_branch.py`
Exit 0. Output preserved as user_action_calibrated_branch.json. Mathbox
computation-audit scope remains bounded. Full theory OPEN.
