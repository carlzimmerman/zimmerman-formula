# Matching the protected candidate to the repository's carrier

2026-10-11. This tests the relation to the repulsive-contact Hamiltonian in
[the microscopic carrier report](../microscopic_carrier_2026_10_10/REPORT.md).
The minimal protected action has a threshold cancellation. It is not already
the same carrier with the same contact coupling.

## Tree-level two-body matching

Expand the charged action as

\[
 V=m^2|\phi|^2+M^2|\chi|^2+
 g(\chi^*\phi^2+\chi\phi^{*2})+\lambda|\phi|^4,
 \quad M^2=4m^2+\Delta,\quad\lambda={g^2\over\Delta}.
\]

For two positive-charge phi particles scattering into two positive-charge
phi particles, the quartic vertex is -4i lambda and each conversion vertex
is -2ig. Charge flow permits the source s-channel; there is no neutral
source t/u exchange in this process. With i times the invariant amplitude
as the diagram convention,

\[
 {\cal M}(s)=-4\left(\lambda+{g^2\over s-M^2}\right).
\]

At threshold s=4m^2, the effective quartic is exactly zero at tree level:

\[
 \lambda_{\rm eff}(4m^2)={g^2\over\Delta}-{g^2\over\Delta}=0.
\]

For x=(s-4m^2)/Delta away from the pole,

\[
 {\lambda_{\rm eff}(s)\over\lambda}=-{x\over1-x}.
\]

Below resonance it is negative, vanishes at threshold, and varies strongly
near resonance. For opposite momenta of magnitude p, x=p^2/(m^2u_*^2).
The production band lies around x=1, where eliminating the source as a
constant contact interaction is invalid. The bare tree pole requires a
width/resummation and medium treatment before predicting any rate; it is
not a divergent physical cross section claim.

This matching is derived here from the stated action. The general practice
of matching scattering amplitudes, rather than merely dropping fast fields,
is illustrated by [Braaten, Mohapatra and Zhang](https://arxiv.org/abs/1806.01898).
That paper concerns real-scalar theories; no coefficient or theorem for this
two-complex-field model is imported. Search checked 2026-10-11. No novelty
claim is made for the matching method or cancellation mechanism.

A useful independent check is the source equation:
(□+M^2)chi=-g phi^2. For phi rotating near exp(-imt), the source term rotates
near exp(-2imt), so its leading denominator is M^2-4m^2=Delta. Using M^2
instead would falsely infer a nonzero threshold repulsion. The near-threshold
expansion requires |s-4m^2| much smaller than Delta, not just p much smaller
than m.

## Exact pressureless classical family

For every constant complex amplitude A in a periodic Minkowski box,

\[
 \phi=Ae^{-imt},\qquad
 \chi=-{g\over\Delta}A^2e^{-2imt}
\]

is an exact solution of both nonlinear field equations. The source equation
reduces to Delta chi+g phi^2=0. In the daughter equation, the cubic and
quartic forces cancel. Both rotating-frame derivatives vanish, as do all
gradients and the positive potential square U. Hence

\[
 E=mQ,\qquad P=0.
\]

These states contain both species and saturate the classical energy-charge
bound. In a finite periodic volume they have finite E and Q. A spatially
constant nonzero field in infinite space would have infinite total energy;
there one can only quote its densities.

This is an existence statement, not a claim that the production trajectory
settles into this family. It does not prove orbital stability, relaxation,
cosmological tracking or halo formation. In particular it cannot supply the
repulsive contact pressure assumed in the repo's separate carrier test.

## A declared extension can supply repulsion

One may add lambda_r |phi|^4 with lambda_r>0. This is new input. The threshold
quartic then becomes lambda_r. Under phi=exp(-imt) psi/sqrt(2m), the leading
nonrelativistic interaction is

\[
 {\lambda_r\over4m^2}|\psi|^4={g_{\rm NR}\over2}|\psi|^4,
 \qquad g_{\rm NR}={\lambda_r\over2m^2}.
\]

Thus a positive contact coupling is available in this extended action in
the low-energy regime sufficiently far below the source resonance. It is
not predicted by the symmetry, density or vacuum term. Near resonance the
energy-dependent source contribution must still be retained.

The classical energy-charge identity remains positive after adding this
term. In the FLRW argument its positive virial remainder cannot worsen the
lower bound R>=-u_*^2E/4; consequently the existing energy comparison theorem
survives the extension. For the absolute averaged-pressure estimate, a
conservative extra D term bounds the new quartic remainder, adding eta to
the prior bulk pressure bound. The exact pressureless rotating family no
longer solves the extended equations at nonzero A.

Production must be recalculated if lambda_r is introduced: it increases
the normal and anomalous Gaussian quartic terms. No new lambda_r is selected
here, and the reported 0.94881 fraction applies only to the minimal action.

## Verification, conclusion and remaining gap

[carrier_matching.py](carrier_matching.py) checks the threshold cancellation,
rotating field equations, charge saturation and zero pressure with exact
rational arithmetic, plus the energy-dependent amplitude identity. All 79
checks pass. [Results](carrier_matching_run/results.json) and
[manifest](carrier_matching_run/manifest.json) preserve the evidence.
The general statements follow from the displayed algebra, not the samples.
This was self-review. Radiative corrections and technical naturalness of
the parameter relation have not been analyzed; the cancellation is not
claimed as an all-orders quantum theorem.

**Decision:** the protected candidate supplies classical cold states and an
approximate production route, but the minimal version does not reproduce
the repository's repulsive-contact carrier. A positive-contact extension is
algebraically possible and preserves the energy protection, at the cost of
an extra parameter and a new production/transport calculation. Neither
version derives the repo's halo profile, acceleration scale or vacuum
connection. Those are genuine missing physical implications, not supplied
by the production percentage or the exact charge alone.
