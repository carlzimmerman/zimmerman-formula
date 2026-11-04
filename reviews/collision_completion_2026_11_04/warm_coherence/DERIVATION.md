# Actual warm four-singlet statistical matrices

The physical four scalar parents have mass sqrt(.006) and warm group ID
**S1_1**, degeneracy four, actual indices [94,95,96,97]. S1_0 is the massless
two-real-state modulus. The late pole indices [60,61,62,63] and its couplings
are not transplanted. `matrix_api.actual_matrices` rebuilds the full actual-x
tree cubic and Yukawa tensors in the actual charge/Casimir-adapted basis.
The current warm common group masses determine its kinematic phase space;
the small difference from interpolated scalar widths is measured separately.

For scalar final groups j,k, define the full parent matrix Cab by summing
cubic_a,ij cubic_b,ij over their physical internal states, with both ordered
blocks for distinct groups. For fermionic groups use the corresponding
Aab=Re sum y_a,ij y_b,ij* and Bab=Re sum y_a,ij y_b,ij. The actual rest width
matrices are

    Gamma_SS=C sqrt(lambda(1,rj,rk))/(32pi M),
    Gamma_FF=M sqrt(lambda(1,rj,rk))/(16pi)
              [(1-rj-rk) A-2 sqrt(rj rk) B].

Each matrix is per physical real parent state, not averaged again by four.
Its trace divided by four is the scalar grouped width. These isotropic
spin-summed scalar-parent amplitudes can be multiplied by one common angular
occupation factor when daughters are isotropic, unpolarized and proportional
to identity inside each physical group, as assumed in the supplied warm
finite operator.

For parent momentum p, boost b=M/sqrt(M²+p²) and the exact two-body map,

    Gamma_loss,a(p)=b Gamma_vac,a <avail_j(Ej) avail_k(Ek)>,
    Gamma_gain,a(p)=b Gamma_vac,a <f_j(Ej) f_k(Ek)>.

Availability is 1+f for bosons and the separately stored 1-f hole for
fermions. Both products use the declared finite entropy projection: their
logarithms are affine on each daughter-energy stencil interval. Integrating
the exponential exactly on every interval avoids the known global GL2
angular error. Out-of-grid segments are omitted and their angular fraction
is reported. The warm002 independent hole coordinates are retained; warm001
only stores rounded numbers, so its unrecorded sub-ulp holes remain a stated
input limitation.

Let G=sum Gamma_gain,a, L=sum Gamma_loss,a, D=L-G. The declared local
bosonic Markov matrix diagnostic with bare degenerate H=M I is

    rho_dot=G-{D,rho}/2.

All tested D are positive, so the unique stationary covariance solves
D rho+rho D=2G. Channel net decay currents are

    Ja=Tr[(Gamma_loss,a-Gamma_gain,a) rho-Gamma_gain,a].

Their stationary sum vanishes. A channel to two charged carriers contributes
-2 Ja to charged depletion; positive net inverse production therefore
depletes charge. This independently matches the P-only exact scalar event
operator within 1.28e-4, consistent with the measured vertex-interpolation
error. At a common thermal bath the matrix KMS relation gives
G=exp(-EP/T)L and rho=fB(EP) I; this is recovered to 4e-15. The matrix
equation is not asserted to be the full in-medium Kadanoff-Baym evolution.

## What differs from isotropic parent kinetics

At the two saved warm midpoints, coherent stationary P-mediated charged
depletion is .64391 and .39446 times the isotropic stationary result. At
equal total parent number the corresponding ratios are .65702 and .50550.
The parent-number changes are only factors 1.00502 and 1.02823. Internal
branching anisotropy therefore supplies most of the difference. Normalized
gain/damping commutators are nonzero, and the invariant deviation of rho
from a multiple of identity is typically .4-.6 in occupied momenta.

A separate control permits four unequal diagonal populations in the stated
adapted basis, f_a=Gaa/Daa. Coherent/unequal-diagonal charged-current ratios
are .74992 and .43362. Thus allowing unequal populations alone does not
remove the effect. This intermediate diagonal comparison is basis-dependent;
it is not a physical dephasing prescription. The isotropic closure and
full matrix predictions are basis invariant.

## Whole operator and actual field phases

The large P-relative change must not multiply the whole charged history.
The independent exact-angle all25 operator shows a much larger current from
other channels. Reconstructing each actual saved eight-node GenericOrbit,
including the snapshot-matched gaugino mass source convention, gives

| Snapshot | Whole25 phase-averaged charged loss, mu^4 | P coherence triangle / whole magnitude |
|---|---:|---:|
| warm001, N=.00216902 | +5.87956444e-19 | .00017315 |
| warm002, N=.00494507 | -3.63515831e-19 | .00019829 |

Negative loss means net charged return in that frozen-state operator; it is
not a newly integrated history. For phasewise local stationary responses,
sum w |Pcoh-Piso| is 1.00994e-22 and 7.20801e-23 mu^4, or .017177% and
.019829% of the whole phase-averaged current magnitude. The triangle bound
applies to this tested local-stationary closure only.

The actual parent projector is constant to below 1e-15 at both turning
points and every saved phase. Its overlaps therefore align the actual-x
matrices to one common physical frame without a fabricated Berry connection.
In that frame a second, separately labeled orbit-averaged matrix steady
diagnostic gives P coherence/isotropy ratios .64682 and .39447. The absolute
per-phase triangle is 1.01804e-22 and 7.20809e-23 mu^4, or .017315% and
.019829% of the whole current magnitude. Every actual phase has no open
channel with P as a daughter, so the tested P one-to-two/inverse sector is
complete within the frozen tree channel model.

Minimum damping/H is 6.80e4 and 6.98e4, whereas minimum damping/omega is only
.01122 and .01140 across represented parent momenta. Cosmological changes
are slow relative to this damping gap, but prompt within-orbit elimination
is not established. Neither phasewise steady nor averaged-matrix steady
is silently identified with the exact periodic density response. Given the
small absolute current budget, the coordinator requested this bound in lieu
of an expensive many-momentum periodic solve for these two warm snapshots.

## Exact first remaining implication

For a full coherent history one must evolve the parent matrix in the common
frame with its phase-dependent gain/loss, couple its channel currents to the
actual daughter distributions and forces, and match the dispersive medium
selfenergy. The bare degeneracy H=M I is a diagnostic input; an unknown
Hermitian thermal splitting is not assumed absent in the physical theory.
Broken-vector channels are outside this FFS/SSS operator. In the warm region
their thresholds can be open, so the constructed matrices are not called
fully inclusive physical widths. A matched physical history must address
that sector separately.
The first matrix-transport bridge is therefore still conditional. The present
evidence bounds the tested warm local/current correction budget, not every
later state, periodic history or additional degenerate multiplet.

## Rigorous periodic trace envelope without solving forty momentum ODEs

For the declared eight-phase frozen-bath coefficient model, define separately
at every represented parent momentum

    Smax=max_phase Tr Gamma_gain,
    gamma_min=min_phase lambda_min(D)>0,
    Nmax=Smax/gamma_min.

For any PSD density, including an arbitrary Hermitian commutator within the
fixed four-state coefficient model,

    d Tr(rho)/dt=Tr G-Tr(D rho)<=Smax-gamma_min Tr(rho).

Every PSD periodic response therefore has Tr(rho)<=Nmax pointwise. A frozen
finite evolution with initial trace N0 instead has the uniform bound
Tr(rho)<=max(N0,Nmax). For an isotropic periodic trace equation, the sharper
scalar damping is min_phase Tr(D)/4, giving its own bound Niso_max.

Set Acharged=sum_a charged_carriers(a) (Gamma_loss,a-Gamma_gain,a).
At the same bath the affine gain current cancels in a comparison. Since rho
and rho_ref are PSD,

    |Tr Acharged (rho-rho_ref)|
       <=||Acharged||op [Tr rho+Tr rho_ref].

Using rho_ref=f_actual I and summing positive momentum measures and actual
phase weights gives an absolute current envelope independent of the unknown
periodic density and of its Hermitian Hamiltonian. The declared eight-phase
matrices, or their positive convex interpolants, supply the uniform source
and damping bounds. This does not assert that arbitrary uncomputed continuous
thermal matching is bounded by those sampled coefficients.

`run_trace001` gives:

| Snapshot | Any PSD periodic response vs stored isotropic current | Fraction of saved whole25 magnitude |
|---|---:|---:|
| warm001 | 3.17794e-21 mu^4 | .54051% |
| warm002 | 2.32487e-21 mu^4 | .63955% |

Replacing the phase-weighted operator norm by its phase maximum yields
3.18782e-21 and 2.32516e-21 mu^4, or .54219% and .63963% of the same saved
whole-current reference. Comparing coherent and isotropic periodic responses,
both with their trace envelopes, gives .58076% and .63995%. The finite
frozen-bath evolution initialized at the stored parent trace has the same
.54051%/.63955% bound here. Thus a genuine periodic-current envelope is
available without instantaneous-steady elimination or a many-momentum ODE.

The directly measured averaged-matrix correction uses only about 3% of this
envelope. These rigorous bounds establish a small correction budget for this
specific frozen warm operator, even though its internal singlet branching
effect is large. A changing bath, changed selfenergy/rates, new channels or
a different historical parent trace remain outside the periodic model.
