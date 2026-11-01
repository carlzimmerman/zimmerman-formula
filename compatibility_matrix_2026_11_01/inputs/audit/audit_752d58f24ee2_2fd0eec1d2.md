# Polarization link: a current can be derived, but the response switch cannot

20 October 2026. [Target and conventions](TARGET.md). Parent checkpoint:
`reviews/conversion_dynamics_2026_10_20/CHECKPOINT.json`.

**The existing fields do not yet yield the required tether-on/released-off
response or close the memory gap.** This phase derives the candidate link
explicitly, substitutes it into the action, and tests binding, condensation,
support and common gravitational backreaction. No fitted switch, portal,
response coefficient or rate is introduced.

## 1. The conversion current can be constructed exactly

For a specified selected population with
`dot rho_t+div j_t=S_t`, the existing equations give the nonlocal
longitudinal representative

\[
 P_t=\nabla\Delta^{-1}(\rho_t-\bar\rho_t),\qquad
 \boxed{\dot P_t=-j_t^L+
       \nabla\Delta^{-1}(S_t-\dot{\bar\rho}_t).}
\]

The actual original cubic reaction supplies one such source, and the
previous capture calculation supplies others in its admitted kinetic
limits. Boundary flux, background and zero modes must be included.
This improves the kinematic accounting without selecting a new coupling.

But substituting this representation into the original scalar action
does not generate the required canonical matter energy

\[
 {K|P_t|^2\over2}+W_{\rm rem}(K|P_t|)
       +{\gamma\over2}|\nabla P_t|^2.
\]

For example, the actual scalar contact gives
`g2(div P_t)^2/(2m^2)`, a derivative restoring term. A current partition
does not change physical observables. Installing the desired `W` after
choosing a bound-state projector would change the action. The projector
also has nonlocal currents, local interference, and closing-gap problems
at the proposed unbinding threshold. [Exact selector and action comparison](selector/RESULT.md).

## 2. Binding creates tidal response, not the missing local dipole

A live daughter-host system has no internal uniform gravitational
mass dipole: both masses accelerate, and the complete dipole is their
center of mass. In an exact existing-gravity Coulomb control the first
nonzero internal density response is

\[
 \chi_{\rm int}(k,0)
   ={83\over24}{\mu^3a^6\over\hbar^2}k^4+O(k^6).
\]

The coefficient includes all breathing and quadrupole states, including
the continuum. It is a calculated tidal/finite-wavelength response.
The bound-state expansion becomes singular as the gap closes; it does
not approach an exactly inert released state. The full-energy stress
identity also prevents using nonconserved source/daughter rest masses
to manufacture an internal uniform dipole. [Derivation and exact scope](multipoles/RESULT.md).

Granting a supported baryonic reference does not fix release either.
A conditional two-coordinate supported model has
`chi(0)=(m+M)^2/k_a+m^2/k_b`. Removing binding gives a free-motion pole,
rather than zero response. Completing the anchor as a live universally
gravitating body restores center-of-mass-only uniform response. No actual
anchor is supplied by this calculation; the old spherical breathing
curvature cannot be used as a Cartesian anchor. [Support-loophole check](support/RESULT.md).

## 3. The actual scalar phase still gives the wrong restoring kernel

The original homogeneous zero-temperature retained-source mean-field
model has one stable occupied amplitude branch at each allowed chemical
potential or positive charge density. A direct fixed-charge convexity
check excludes a hidden second local amplitude minimum there. The
unbounded high-chemical-potential grand functional is not a second
physical phase.

Keeping the actual gapless phase gives a positive density susceptibility
and a displacement action with kinetic `dot P_L^2/(2m^2 C_theta)` and
restoring `(div P_L)^2/(2m^2 q_mu)`. It does not supply the critical local
polarization energy. Loss of condensation does not remove finite-density
gas response. A local-charge spectral moment confirms the latter within
its stated continuum/lattice regimes; it does not by itself prohibit
an independently defined extra-force switch. [Phase, gapless response and spectral check](phases/RESULT.md).

## 4. Common gravity was tested as an existing bridge

Integrating out a positive-susceptibility ordinary density in the already
specified reciprocal energy gives a mixed source coefficient

\[
 -{v\over1-v\chi},\qquad v={K\over k^2},\quad0<v\chi<1.
\]

It strengthens static gravitational feedback and cannot vanish in that
stable responder domain. Its induced curvature is attractive, not the
missing positive critical tether. The phase-dependent susceptibility
changes the feedback; it supplies no binary response gate. Taking the
Jeans denominator to zero invalidates passive elimination. This is a
linear static mode result, not a claim about all dynamic or nonlinear
states. [Common-gravity calculation](GRAVITY_BRIDGE.md).

## 5. The unchanged canonical field does not store a static off state

The canonical equation is

\[
 \nabla\Phi-KP-R(K|P|)\widehat P+\gamma\Delta P=0.
\]

An exactly zero `P` on an open region forces `grad Phi=0` there whenever
ordinary small local material variations remain admissible. At fixed
baryon sources and one fixed convex material domain, eliminating `Phi`
gives the strictly convex energy

\[
 \mathcal E[P]={K\over2}\|P_T\|^2+\int W_{\rm rem}(K|P|)
   +{\gamma\over2}\|\nabla P\|^2-\int\nabla\Phi_b\cdot P.
\]

It has at most one static minimum in that class, rather than responding
and nonresponding memory minima at the same controls. Existence, live-host
relaxation, constrained empty-medium regions and different microscopic
phases are separate questions. [Fixed-environment memory test](CANONICAL_MEMORY.md).

## Consequence for the requested memory

The field/source ledger can be repaired algebraically, but the inspected
existing actions still do not provide the physical constitutive selector.
The remaining task is to derive a material state or support law whose
actual action has the required response and whose released state retains
ordinary mass without that tether response. Its transition and retention
must then be calculated together. A mask multiplying `P`, the scalar
condensate fraction, or the nodal determinant would assume this step.

These are scoped obstructions and exact conditional responses, not a
global impossibility theorem for every finite-temperature, nonlinear or
nonuniform many-body state. [Open routes and resumption conditions](NEXT.md).
All new deductions are analytic. The six proof notes received separate
raw reconstruction in [the audit](audit/RESULT.md), with exact hashes in
`audit/provenance.json`. No new lifetime or full-theory closure is claimed.
