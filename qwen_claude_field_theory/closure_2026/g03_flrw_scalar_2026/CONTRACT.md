# C-H on an allowed expanding compact background

Continue the same action defined in ../g03_covariant_action_2026/ACTION.md.
Do not add f32, change q, remove the clock, or claim strict AQUAL matching.
No commit or push is part of this study.

Background: flat three-torus, scale factor A(t), positive Lambda, empty
particle and Maxwell fields, tau=t, spatially constant U. Work in c=1 units;
restore c in dimensional claims. Derive background equations by varying the
Einstein-Hilbert minisuperspace action. The auxiliary first variation vanishes
at DU=a=0 because q(|p|^2) is C1, not C2, there.

The next gate is the *reduced* quadratic action at this singular point.
Eliminate U by its stationary spatial functional before expanding in a fixed
smooth perturbation direction. Supply a continuum directional argument and
finite spectral minimizations of the exact nonlinear q. Never substitute a
finite guessed constitutive Hessian at zero field. Numerical checks use
alpha=A=1, two positive Gaussian widths, 4/8 cosine modes, 192/384 nodes,
and lapse amplitudes .02,.01,.005,.0025. They are not continuum certification.

Derive the scalar ADM action retaining lapse and shift. Restore the scalar
spatial-coordinate variable before Legendre transformation; calculate all
primary/secondary constraints, their brackets, and multiplier preservation.
Count only after this quadratic-sector chain closes. Treat k=0 afresh;
do not substitute it into a nonzero-mode inverse. Compare this count with
the independent reduced kinetic Hessian. Derive the tensor kinetic and
gradient terms separately. Do not transfer these results to other backgrounds
or to the full nonlinear Dirac chain.

Pass means consistency of this bounded calculation, not a closed theory.
Record any additional scalar explicitly, including zero spatial sound speed.
A clock counted separately is not automatically healthy at nonlinear order.
Nonuniform zero-field/high-frequency limits, interactions, generic constraint
closure, causality, ordinary-matter cosmology and PPN remain separate gates.

Implementation: tests first; then flrw_gate.py (symbolic actions/constraints,
nonlinear variational check, portable results/manifest); then REPORT.md.
Do not edit the earlier G03 evidence while performing this independent study.
