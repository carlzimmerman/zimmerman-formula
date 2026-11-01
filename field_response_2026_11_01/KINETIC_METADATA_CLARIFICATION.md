# Clarification of inherited kinetic-run metadata

The numerical kinetic contracts inherited two descriptive fields from the
radial-run template: `conventions` mentions the isotropic fluid completion,
and the BVP tolerance list contains both 2e-6 and 3e-7. The actual kinetic
calculation, its assertion, pinned CONTRACT_KINETIC.md and reviewed code use
canonical anisotropic perturbations and only the refined 3e-7 scalar solves.
The material-fluid inertia matrix is used solely as a positive normalization
of energy Rayleigh quotients, not as a derived kinetic-mode operator.

No frozen manifest or numerical output is rewritten. This is a documentary
clarification of those inherited labels; the code, six-case population, energy
coefficients, results and source hashes are unchanged. It does not promote
positive tests to a stability theorem or negative energy to a kinetic growing
mode theorem.

The endpoint-stability contract also inherited the generic [4,8,12] basis
list and two scalar tolerances. Its actual code evaluates the full12-mode
space at3e-7 and both quadratures. No explicit nested endpoint solves are
claimed; a positive full-space form has positive restrictions, but that
algebraic implication is distinct from running separate nested cases.
