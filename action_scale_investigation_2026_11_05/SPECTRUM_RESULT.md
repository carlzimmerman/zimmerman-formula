# Restricted radial box: refined low modes are positive

This is a finite variational calculation about four stipulated finite-shell
backgrounds. It is NOT a full action-health verdict or a coefficient
derivation. Both b values were prescribed before the first shell solve.

## What was actually discretized

The exact static action was integrated by parts so the lapse has no spatial
derivative. Its Hessian was differentiated symbolically in B,N,p,B',p'.
Linear elements for B,p and cellwise-constant lapse were assembled with
midpoint action quadrature. The lapse and polarization constraints were
eliminated together, avoiding a spurious local inversion where the lapse
diagonal changes sign. Radial kinetic mass comes from the independently
derived shift-elimination formula in RADIAL_RESULT.md.

delta B=delta p=0 at both ends defines the perturbation box. This differs
from the natural polarization conditions used to construct the background;
no spectrum for the actual cosmological exterior is implied. Frequencies
are generalized eigenvalues of -H_static versus the positive kinetic mass.

## The failed initial run is retained

The40/80/160-cell ladder failed the frozen2% criterion in every case, with
19-30% last-rung changes. Two40-cell cases had negative modes absent on
the next rungs. We did not declare these physical instabilities or erase
them. evidence/spectrum remains status failed with its original criteria.
The independent Dirichlet Laplacian control converged to pi^2, and its sign
reversal produced a negative eigenvalue. Constraint and eigen backward
residuals were small, so resolution was tested first without changing the
equations or boundary conditions.

## Refinement outcomes

Separate160/320/640-cell runs reproduce the original160-cell values exactly
and meet the same2% criterion at the last pair. All reported low5 values
are positive on these three refined rungs. At640 cells:

| b | Lstar | lowest omega^2 | low3 maximum320-to640 change |
|---|---|---|---|
| .1 | 1 | 1.75155e-8 | .879% |
| .1 | 3 | 3.67636e-8 | 1.024% |
| .3 | 1 | 1.16449e-8 | .714% |
| .3 | 3 | 2.63213e-8 | 1.452% |

Units are the arbitrary diagnostic units in SHELL_CONTRACT.md. No conversion
to galaxy, solar or cosmological time is justified. The largest scaled
constraint condition estimates remain of order3e10; small backward residuals
and mesh convergence are evidence, not exact arithmetic certification.
Background discrete action-gradient residuals decrease with refinement;
they are recorded rather than assumed zero.

## Safe interpretation and next checks

The specified radial-box low modes pass the numerical convergence/sign gate.
This strengthens the candidate's restricted radial evidence beyond its
short-wave test. It does not prove angular stability, weak coupling,
nonlinear regularity, global causality, or matching to an actual source.
The background is a fixed201-sample cubic interpolant; a denser independent
background representation remains an important error discriminator before
using these eigenvalues in any physical claim. No continuum enclosure or
independent eigensolver has been used.

The finite diagnostics pass at two b values. They therefore do not select
b, even within their limited scope. The action remains a family with an
imposed portal rather than a derivation of kappa=1/2.

Self-review only. Evidence: spectrum.py, spectrum_refine.py,
spectrum_second.py and their separate manifests/contracts. Initial failed
results and every refinement are preserved. No change to the adopted v3s
action or project-wide verdict has been made.
