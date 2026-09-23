# Nonlinear external-field tail investigation

Checkpoint NEFT-01, 2026-09-21. Base Git revision:
`44f1694720574d9f5a2d46ce6b5e1d215d142627` (dirty shared checkout).
Scope: this new directory only. No existing research claims are changed.

User target: find and substantiate a useful result not already in the repository.
Selected obligation: extend the existing linear field–orbit reciprocity into
the first nonlinear external-field correction, with explicit source-multipole
and asymptotic qualifications. No empirical discovery or derivation of kappa
is part of this claim.

Three executed/active mathematical routes:

1. Expand the AQUAL constitutive flux to quadratic order and invert the
   anisotropic exterior operator. Test whether the axial coefficient still
   depends on the second derivative of the response. Candidate: it cancels.
2. Try to infer that coefficient from the raw opposite-side force difference.
   Obstruction: a matching-dependent dipole falls more slowly than the desired
   nonlinear term. Do not set the dipole to zero by assumption.
3. Remove the dipole by combining measurements at r and 2r; compare AQUAL with
   QUMOND having exactly the same isolated spherical relation. Candidate:
   different nonlinear coefficients, despite identical isolated curves.

Proof success requires the full quadratic PDE identity, axial reduction,
multipole classification, source normalization, and radial-filter algebra.
Numerical success alone is not a proof of an asymptotic expansion for all
nonlinear solutions. The general-source claim will explicitly assume a
differentiable multipole expansion. A separate compact smooth weak-source
calculation must test the matching contribution, rather than ignore it.

Validation planned: exact symbolic differentiation; full nonlinear-operator
residual scaling for several response functions; independently integrated
second-order radial Green functions for compact sources; Newtonian and QUMOND
controls; self-audit and bounded literature/repository overlap search.

## NEFT-02: substantive checkpoint

All three routes reached discriminating outcomes. Route 1 produced the exact
quadratic potential and cancellation of mu'' on the axis. Route 2 failed as a
universal raw statistic: a source-dependent induced dipole dominates it and
can reverse its sign. Route 3 removes that dipole and yields distinct normalized
coefficients, L in AQUAL and -k_nu in QUMOND. For identical deep isolated curves
these are 1 and 1/2. An optional third radius also removes the next odd power.

The exact calculation and conditional asymptotic proof are in PROOF.md. The
source-matching issue is tested by global second-order AQUAL Green calculations
and a nonlinear QUMOND Green calculation with angular/radial convergence checks.
The primary audit verdict remains conditional on the explicit far-field
expansion; empirical validation and global literature priority are not claimed.

The deliverable is a new scoped research package. Next independent task, if
pursued: full nonlinear AQUAL validation with correctly matched dipole boundary
data, followed by a rigorous asymptotic expansion theorem. No legacy source or
status file has been edited by this package.
