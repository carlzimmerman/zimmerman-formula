# Self-audit

No independent agent review was requested or used. Scope: new scalar mode proof, declared initial-value benchmarks, source/phase normalization and interpretation. No predecessor files changed.

Primary run:833 cold mode cases,20 two-fluid matrix cases and56 expanding mass/epoch cases. Six numerical checks pass: characteristic residual<=1.73e-16; finite inertia does not exceed quasistatic growing rates; growth repeat<=9.50e-9 relative; zero-k dust reference within3.67e-12; positive cold growth respects the dust comparator. Polynomial and matrix agreement support finite cases; monotonicity and inequalities are separately derived in DERIVATION.md.

Phase and phase_v2 each completed with14 masses,3001 output times and two ODE tolerances. Maximum phase-response tolerance difference is2.19e-9 relative to each history's maximum response. Phase_v2 adds polarization-history validity accounting; original output remains unmodified. Both mean and cos2kx forcing coefficients are h_amp²/4. Normalized delta_i=1 runs compute perturbative coefficients and must not be interpreted as physical unit-contrast solutions.

Interpretation gate fails: no sampled phase shift of .1 occurs with both prior |P|<.1 and density contrasts<1. Minimum normalized validity violation is18.229. This is a finite single-mode result with assumed FRW scalar damping and quasistatic P, not a universal bound on broadband or nonlinear production. Numerical tolerances certify the ODE solution, not the assumed cosmology.

Additional limitations:
- The cold onset table extrapolates linear evolution to delta_c=1; baryons can cross their nonlinear threshold earlier. It is not a derived spherical collapse barrier.
- Frozen-background growth bounds cannot simply be promoted to a full finite-inertia expanding comparison theorem.
- The real logarithmic W has |P|<1; values beyond it in quadratic extrapolations signal invalid approximation, not admissible field values.
- Scalar FRW damping, zero initial phase perturbation and adiabatic quasistatic P are explicit additional choices; their parent-action consistency is unresolved.
- Maxima/minima use3001 time samples with tolerance repeats, not formal continuous-time bounds. The large factor18 failure margin is decisive for the sampled histories but not a general no-go.
- Pressureless baryons at z1100 are an intentionally simplified inherited benchmark, not a recombination-era treatment. No primordial transfer spectrum, gas pressure, radiation, non-Gaussianity, nonlinear backreaction or population transport is calculated.
- Mass labels use k=1/R_L at reference total mean matter density; an alternative window changes the mapping. They are not measured remnant masses.
- Coefficient positivity and homogeneous stability are not a full constraint/hyperbolicity proof.

Prose/equation self-review: checked sign of mismatch force, eta root, derivative wrt q², symmetric two-fluid matrix, units, phase source factor1/4, N-time friction1.5, the separation of density/field nonlinearity, and conditional rather than observational meaning of the growth table. Core selection, population closure and simultaneous observational preservation remain unestablished.
