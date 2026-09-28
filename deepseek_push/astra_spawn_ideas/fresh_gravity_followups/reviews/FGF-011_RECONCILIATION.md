# FGF-011 reconciliation: accepted in exact boundary scope

2026-09-27. Coordinator read the independent derivation, verified all returned
input/output hashes and required fields, and validated numeric_run_001's
manifest. Result SHA256:
`225fc95535c363a778ff5dd4e430651917df58eb7d8e5aed1f86dfa4ebf2c8a7`.
The audit's independent operator calculation, 34 controls, 672 grid cases and
96 growth checks support the stated finite evidence; no new coordinator rerun
of that same grid was needed.

Accept the exact supported/subtracted-model dispersion, growth maximum and
hydrostatic-slab scale identity with their specified premises. The coordinator
also independently verified the new factorization: expanding
cs²[(rho xi)']²/rho and integrating the cross term gives
cs²rho xi'²+[cs²rho'²/rho-cs²rho'']xi². Hydrostatic balance makes the bracket
rho g'=C rho²/A, where C=4piG and A=b'(g)>0. The density-potential cross term
integrates to 2rho xi psi'. Completing the square gives

    2V=integral[cs²rho xi'²+(A/C)(psi'+C rho xi/A)²]dx
       +[cs²rho' xi²-2rho xi psi]_left^right.

For positive smooth rho,A, cs²>0 and xi=psi=0 at both walls, V is strictly
positive for nonzero longitudinal perturbations. Together with positive
kinetic energy this settles the sign for this finite, externally supported,
one-dimensional linear boundary problem. It does not settle free boundaries,
3D modes, non-isothermal matter, zero-field degeneracy, nonlinear evolution,
cosmology or the operative filtered-MONO metric theory.

FGF-015 must therefore be revised from an open sign search into a conforming
positive-spectrum/convergence test, with deliberately wrong boundary terms
as controls. Numerical negativity under exactly these hypotheses is first an
implementation/audit failure. FGF-016 can be released as conditional inference
work. FGF-014 is released only as the explicitly supported/subtracted toy
combination; a physical two-field matter background is a distinct open gate.
