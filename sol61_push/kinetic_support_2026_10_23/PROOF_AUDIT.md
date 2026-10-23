# Self-audit: fixed-occupancy mass-slope identity

Claim: every nontrivial isolated differentiable stationary branch specified in DERIVATION.md, at fixed K and couplings and with vanishing boundary terms, has d(E/M)/dM<0. Verdict: **proved as written under those explicit hypotheses**, by an internal scaling identity. This is self-review, not an independent proof certificate. The claim does not assert existence at all masses, dynamical attainability, or a general ban on population selection.

Dependency graph: waterbag velocity integral -> T=(3/2)K int rho^(5/3); mass-preserving canonical dilation -> virial identity; independent amplitude variation -> muM identity; phase Euler-Lagrange equation -> V=2J+2Z+H/2; algebra and sign of2W-pW' -> strict mass-slope sign. All leaves are explicit internal calculus or stated boundary/differentiability hypotheses. No Newtonian stability theorem is imported.

Checks:
- Velocity-ball normalization, pressure coefficient and mass exponent5/3: passed by direct integration.
- Dilation preserves mass and f0 by inverse velocity scaling; T has exponent2, mismatch exponent3, phase potential-3, phase gradient-1, gravitational energy1: passed.
- Polarization amplitude changes by t^2; W term derivative2D-3B: passed.
- int rho h=2V+D follows from integration by parts and grad h=-W'(p)P/p: passed.
- Phase multiplication by chi-1 gives V-H/2=2Z+2J: passed.
- Subtraction gives -4T/3-4J-2Z-H+2B-D: passed.
- Derivative of2W-pW' is -p^2/(1-p)^2; at p0 it is zero: passed. Nontrivial waterbag T>0 makes strict inequality.
- Differentiability/existence/vanishing surface terms are assumptions, not established for every mass. Finite-box numerics approximate the identity; they do not prove its general boundary hypotheses.
- Numerical comparison across16 solutions: independent Jeans virial, energy virial and mass-slope residuals recorded in virial/result.json. This is a consistency check, not the proof.

Separate stability claim: the radial and nonspherical density Hessian and 3D evolution provide **computational verification only in the stated finite range**. The small negative l1 eigenvalue is identified as a translation-discretization error by analytic symmetry, overlap>0.999997 and refinement toward zero; it is not falsely reported as a wholly positive unprojected finite matrix. High-l positivity uses the written variational bound. Full kinetic nonlinear stability, cosmological formation and baryon-coupled preservation remain unproved.
