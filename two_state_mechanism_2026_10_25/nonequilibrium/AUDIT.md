# Computation audit and interpretation

Outcome: **finite numerical assertions verified in the stated range, conditional
on BO physics, floating precision and the restricted reaction network**. The
broader galaxy mechanism is not established. No new mathematical novelty claim.

## Evidence

| Run | Status / purpose |
|---|---|
| run_electronic | Completed: nested prolate bases and two full Coulomb/dipole curves |
| run_spectrum | Completed: radial h=.02, scattering match800,640 log energies |
| run_refine | Completed: h=.01,1280 energies, same match800 |
| run_tail | Completed: smaller electronic basis, tail join32, match400 |
| run_kinetics | Failed before computation: Python3.9 rejects starred unpacking in subscript |
| run_kinetics_v2 | Failed at JSON serialization: NumPy bool_ gates |
| run_kinetics_v3 | Completed: explicit concatenate and native bool gate serialization;39 points |
| run_extend | Completed:18 larger-mass points to reach optically thin applicability |
| run_audit | Completed: independent normalization, domains, coverage, time refinement |
| run_bound | Completed: continuous-interval bound for the implemented rate interpolant |

Failed scripts, errors and immutable manifests remain archived. They provide
no physical evidence. Fixes are in new source files; no pinned input was edited.
The electronic contract inherited the phrase 'explicit two-orbital basis' in its
coefficient-domain description. That metadata phrase is stale: ELECTRONIC.md,
source, basis-order bounds and outputs specify the actual multi-function prolate
basis. The contract is retained unchanged for provenance.

All exact regeneration argv, input/output hashes, versions and execution statuses
are in the run manifests. Run with Python3.9.6, NumPy1.26.2, SciPy1.11.4,
PYTHONDONTWRITEBYTECODE=1 and OPENBLAS_NUM_THREADS=1. The mathbox bounded runner
created the manifests. VALIDATION.json contains fresh validator outputs for all10.
Validation checks provenance, not physical truth. Re-executions require new output
directories and unchanged pinned inputs.

## Independent checks and limitations

The scattering normalization sqrt(2mu/(pi k)) matches a finite-box eigenstate /
local-level-spacing calculation to .077% at four energies. This is independent
of merely evaluating detailed balance with the same arrays. Thermal Milne
reciprocity errors <=4.22e-15 are algebraic convention checks, not independent
certification of a cross section.

Nuclear eigenstates have integral |u|² dR=1, continuum states are delta(E-E')
normalized, and the dipole strength includes rotational absorption factors.
Bound degeneracy is 2J+1 without nuclear-spin exchange projection. Atomic radiative
rates use a leading BO mass convention; finite-mass corrections are not hidden
as free formation parameters.

The potential tail coefficient follows directly from hydrogen perturbation theory.
For unit-field perturbation z, the first-order wavefunction is
psi1=-(r+r²/2)cos(theta)psi_1s. Substitution into
(H0+1/2)psi1=-z psi_1s verifies it. The energy shift is
<z psi1>=-(<r²>+<r³>/2)/3=-(3+15/4)/3=-9/4.
Thus alpha_pol=9/2 and the distant charge gives -9/(4R^4).
The matched R^-6 term and asymptotic dipole correction are approximations checked
by varying the join; they are not exact long-range coefficients.

At the coldest checked T=6.4e-8, the first retained continuum decade contributes
.1415% of the rate. It is a diagnostic, not a rigorous error bound for E<1e-10.
No arbitrary subthreshold extrapolation enters the integrations. At T=.03 the
contribution above E=1 is1.06e-15; the retained domain extends to2. Narrow
resonances could evade a log-grid test. The rates' numerical refinements are
therefore not a claim of uniform accuracy at every continuum energy.

run_audit also records a sampled rate-ratio cap of4.313%; this is NOT the uniform
cap and must not be used as one. run_bound supersedes it by maximizing each cubic
log-ratio interval, including the upper endpoint T=.05, giving4.41415%.
The bound is conservative for that interpolant, using double precision; it is
not validated interval arithmetic for the exact continuum problem.

## Conservation and scope

Each event conserves both constituent counts and net charge. Kinetic energy,
negative atomic/molecular binding energy and escaped radiation form one ledger.
The tiny numerical drift verifies that ledger. It does not prove the omitted
physical processes negligible. No external blackbody spectrum is inserted into
an isolated parcel and no matter-only energy conservation is claimed during
radiative cooling. Temperatures can rise despite radiation loss because reactions
reduce the number of freely translating particles.

Opacity is the maximum over a finite photon-frequency grid and161 recorded times,
not a spatial radiative-transfer calculation. The conservative cut tau<.1 is a
necessary screen for this outgoing-radiation approximation. Initial39 cases have
zero common applicability-passing points; extension18 has12. Raw opaque results
are not included in the quoted best physically screened point. Other reactions,
spatial gradients and nonthermal distributions remain uncontrolled even there.

The inherited80%/20% threshold is an operational screen, not an observationally
derived abundance target. No galaxy types enter the differential equations, but
four selected mass/radius profiles do not constitute actual morphology formation.
No live gravity, countercharge spatial transport or RAR comparison is present
in this stage. Earlier3D field experiments are not silently counted as coupled
to this new kinetic solver.
