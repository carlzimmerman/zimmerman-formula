# A finite assembly reservoir: reciprocal mechanics, not yet a halo selector

2026-10-11. Base checkpoint `0e3b9616a35724da12b48b0c655cd936c906fdd6`.
The previous goal turn made progress by computing captured profiles and a
bounded-phase-density obstruction. This continuation removes the prescribed
source-radius history in a finite variational prototype. The full theory
remains OPEN; no cold carrier, cosmic abundance or vacuum normalization is
identified here.

**Result:** source recoil, source contraction and cold self-gravity can be
evolved with reciprocal forces and a finite, explicitly accounted energy
supply. The computation passes conservation checks. It does not establish a
stationary halo or a universal density. In particular, negative individual
energies in a self-gravitating population are not a sufficient host-retention
diagnostic.

## Why the source profile changed

A Plummer density falls as `r^-5`. Under exact global homologous contraction,
internal velocity is `(dot b/b)r`; its kinetic energy involves
`integral r^2 rho d^3x`, which diverges logarithmically for an untruncated
Plummer profile. The earlier externally prescribed potential was a valid
test-field calculation, but cannot simply acquire a finite breathing inertia
under that same global flow ansatz.

Use instead the positive Gaussian source

\[
 \rho_b(x)=\frac{M}{(2\pi)^{3/2}b^3}
 e^{-|x-R|^2/(2b^2)},\qquad
 \Phi_b(r,b)=-\frac{GM}{r}\operatorname{erf}\!\left(\frac r{\sqrt2b}\right).
\]

Its second moment is `3 M b^2`, giving breathing kinetic energy
`3 M dot b^2/2`. To compute its self-energy, the difference of two Gaussian
positions has variance `2 b^2` per coordinate and
`<1/|x-y|>=1/(sqrt(pi)b)`. Thus
`U_self=-A/b`, `A=GM^2/(2sqrt(pi))`. Include support energy `C/b^2`, with
fixed positive C, as in an adiabatically compressed nonrelativistic gas under
the homologous ansatz. C is an input. This collective-coordinate model is
not a solution of the complete gas Euler equations.

## Hamiltonian and reciprocal equations

For cold parcels of masses m_i and pair softening epsilon,

\[
 H=\frac M2V^2+\frac{3M}{2}\dot b^2+\frac C{b^2}-\frac Ab
 +\sum_i m_i\left[\frac{v_i^2}{2}+\Phi_b(r_i-R,b)\right]
 -\sum_{i<j}\frac{Gm_im_j}{\sqrt{|r_i-r_j|^2+\epsilon^2}}.
\]

Let `a_b=-grad Phi_b` and

\[
 \partial_b\Phi_b=\frac{GM}{b^2}\sqrt{\frac2\pi}
 e^{-r^2/(2b^2)}.
\]

Then the reciprocal source equations, with an optional phenomenological
damping coefficient gamma, are

\[
 M\ddot R=-\sum_i m_i a_b(r_i-R,b),\qquad
 3M\ddot b=\frac{2C}{b^3}-\frac A{b^2}
 -\sum_i m_i\partial_b\Phi_b-3M\gamma\dot b.
\]

Cold accelerations are the source force plus softened pair forces. Record
the exported energy through `dot Q=3 M gamma dot b^2`. Direct differentiation
gives `d(H+Q)/dt=0`; total linear and angular momenta are conserved. At
gamma=0 the retained mechanics is Hamiltonian. At gamma>0, Q accounts for
the prescribed loss of coherent source motion; it does not derive radiation
microphysics or constitute a full action for a cooling field.

The available energy is finite. Since
`Phi_b >= -GM sqrt(2/pi)/b`, putting `eta=sum m_i` and
`D=A+GM eta sqrt(2/pi)` yields

\[
 H\ge-\frac{D^2}{4C}
 -\frac{G}{\epsilon}\sum_{i<j}m_im_j.
\]

For equal masses this pair sum is `eta^2(1-1/N)/2`. Therefore Q cannot exceed
initial H minus that lower bound. This follows from the model's positive
support energy and finite softening, not from a separately supplied infinite
reservoir. The coefficients C, gamma and epsilon are still chosen inputs.

## Executed finite experiment

Set `G=M=1`, `C=.05 A`, initial `b=1`, `dot b=0`. Without streams the supported
minimum is `b_eq=2C/A=.1`. Use 24 antipodally paired parcels at radius 2,
angular momenta `.2` and `.6` with paired signs, and mass ratios
`eta=.05,1`. Opposite tangential beams are separated by angular offsets
`+/-.15`; initial positions are not coincident. Initial instantaneous parcel
energy relative to the source plus other parcels is `.05`.

Compare gamma=0,.5,2 from identical physical states at each eta. A separate
no-self-gravity control uses the same initial states as eta=1,gamma=.5;
its Hamiltonian and initial total energy differ. These mass ratios are
prototype inputs, not the theory's cosmic abundance 5.364.

| eta | gamma | Final b at t=30 | Exported Q | Sampled mean cold mass inside .4, t=20--30 |
|---:|---:|---:|---:|---:|
| .05 | 0 | .64335 | 0 | .0021124 |
| .05 | .5 | .09985 | 1.15134 | 0 |
| .05 | 2 | .10000 | 1.14609 | 0 |
| 1 | 0 | 8.29171 | 0 | 0 |
| 1 | .5 | .10005 | 1.42840 | 0 |
| 1 | 2 | .10000 | 1.28795 | 0 |

These finite-window zeros are not exclusions of later core returns. For
example, the eta=.05,gamma=.5 parcels are at radii about 7.6--9.7 at the end,
with negative instantaneous energies. Their orbital times can exceed the
integration window. Source convergence toward its supported radius is not
cold-population convergence toward the required halo density.

At eta=1 without damping, the body has expanded to b=8.29 and is still changing;
coupling to incoming cold material does not automatically yield a settled
compact source. No stationary or permanent-retention verdict is assigned to
any of these finite trajectories.

## Binding is not ownership

In eta=1,gamma=.5, sixteen parcels have negative final instantaneous energies
including other cold matter. That does not establish capture by the baryonic
host. As a concrete ambiguity, parcels 20 and 9 have negative softened
two-body relative energy about `-.07117`, while their pair centre at radius
17.07 is outward moving with positive **host-only** energy about `.03947`.
Those pair diagnostics do not prove permanent internal binding or final
escape in the full evolving system either. They show why a sign test alone
does not supply the theory's host-assignment rule.

[diagnostic_run](diagnostic_run/manifest.json) records these quantities.
Candidate pairs can overlap and must not be added as independent captures.
With only 24 softened parcels, clumping may reflect discreteness; it is not
evidence that physical cold energy fragments that way. This is a numerical
warning against interpreting coarse self-gravitating parcels as a converged
collisionless distribution.

## Verification and surviving obstruction

[run_v2](run_v2/manifest.json) passes 45/45 checks. The source force and radius
derivative agree with independent potential differences. A directional
finite difference of the complete H verifies the damping-power identity.
The largest main-run energy-plus-Q error is below `4.8e-8`. Momentum, angular
momentum, monotonic Q and the finite Q ceiling pass. Deliberately reversing
the source reaction sign produces energy error `.133` and is rejected.
A tighter eta=1,gamma=.5 integration preserves the source evolution closely;
individual cold trajectories are not asserted to have converged statistically.

The initial [run](run/manifest.json) passed its conservation tests but placed
opposite tangential beams at identical positions. The corrected run separates
them before interpreting self-gravity. Original source and contract snapshots
remain under `run/`; its historical hashes differ from current code. Neither
successful conservation nor this separation establishes a Vlasov limit.

This turn used explicit analytic self-review and numerical controls; no fresh
agent review was performed. Numerical checks verify this finite mechanical
model, not the full theory.

There is also an exact limit on what this extension can fix. In the
collisionless mean-field limit, cold trajectories still obey Hamiltonian
transport, even when baryons radiate and the potential depends on time or on
the cold density itself. The phase-space flow has zero divergence. Thus
baryon cooling and cold self-gravity alone do not raise a bounded initial
cold f_max. The preceding [core constraint](../captured_profile_2026_10_11/CORE_CONSTRAINT.md)
still applies when escape depth is finite. Finite-N clumps are not a valid
way to evade that continuum constraint.

**Next live numerical step:** replace the coarse point parcels with a checked
spherical collisionless mean-field representation, retaining reciprocal
source-radius work. Establish host retention and orbit residence before
comparing a stationary density. The exact-to-origin branch separately needs
a singular cold initial state, different cold dynamics, or a physical
regularization of the law. The carrier, abundance, a0, kappa and vacuum
coupling remain unresolved. No frozen criterion or other lane was changed.
