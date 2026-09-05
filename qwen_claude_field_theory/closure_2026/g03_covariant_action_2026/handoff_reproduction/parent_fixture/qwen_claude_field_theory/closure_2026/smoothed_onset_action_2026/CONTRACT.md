# Smoothed onset action gate — 2026-09-04

Approved scope: test whether the suggested unsmoothed-Newtonian plus
once-filtered phantom response is variational, and compute the onset curve
of a variational correction. This is a static research calculation, not a
relativistic completion or an empirical fit.

Conventions: positive outward potential gradient; acceleration is minus that
gradient. `S` is translation-invariant self-adjoint smoothing, `xi` its
Gaussian standard deviation (or Helmholtz length). `mu(y)=1-exp(-y)`;
`s=y*mu(y)` defines the inverse partner, not the RAR fitting function.
Dimensionless spherical variables: `x=r/xi`, `epsilon=GM/(a0*xi**2)`.
Onset means additional acceleration equals unsmoothed Newtonian acceleration.

Plan: (1) differentiate the action and test its discrete first variations;
(2) test source-response reciprocity with the actual exponential kernel;
(3) solve both proposed and action-corrected spherical onset curves;
(4) check small-mass asymptotes, convergence, ordinary MOND recovery and
known limits; (5) run the nearby existing regression tests and record results.

Arithmetic: SymPy exact identities, NumPy/SciPy float64 integration/root
finding; deterministic inputs, no fitted data. Periodic nonzero modes are
used only for the finite reciprocity test, with zero mode projected out.
Spherical calculations use isolated space and a point source. The Gaussian
radial integrals extend to at least ten smoothing lengths beyond the
evaluation radius; compare independent quadratures and a twelve-length cut.
Test mass range is epsilon=1e-12 through 1e-4 for central asymptotes, plus
separate large-radius and high-acceleration checks. No external field.

A detected nonsymmetric response rules out a C2 reduced energy producing
that response with matter coupled linearly to the physical potential,
under the specified stationary-elimination and boundary assumptions.
It is not a theorem excluding all relativistic MOND or all nonlocal actions.
The Gaussian variational correction must be evaluated even if the original
one-filter prescription fails. A test exit 0 verifies stated finite
assertions, not the full fried-chicken requirements. A nonconverged quadrature
or inconsistent normalization leaves the corresponding assertion OPEN.

Explicit non-claims: novelty priority, data agreement, relativistic action,
PPN, slip, gravitational DOF, FLRW, causal propagation, ghost freedom, and
controlled cosmological zero mode. A0 and xi remain phenomenological inputs.
Finite source size must be much smaller than onset; a dominating external
field can remove the isolated mass exponent.
