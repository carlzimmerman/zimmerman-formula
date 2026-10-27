# Action-first test: a coefficient identity without normalization selection

> **Continuation:** [Additional-principle screen](ADDITIONAL_PRINCIPLES.md) finds that coefficient restrictions cannot create the missing cubic. At D=0, the nonexceptional constraint forces a degenerate Einstein metric; exceptional rank-loss sectors remain unanalysed. Retire this action from the active normalization search absent explicit new physical structure.

**Failed candidate. No new microscopic MOND mechanism found.** The explicit
scale-invariant two-measure action has a real relation among vacuum and kinetic
coefficients, but a symmetry-preserving coupling deformation changes the
canonically normalized nonlinear response at fixed vacuum and Einstein coupling.
It also has no static cubic. We stop this candidate at the action gate.

Kappa=1/2 remains FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=
0.345 +/- 0.078 are separate and unused. No observational calibration enters.

## What was and was not already tried

DBI/local SUSY: W4-04 and W4-08 symmetry_protection; local Weyl:
reviews/explicit_weyl_source_2026_10_24; de Sitter gauge: K080 and K195.
These were screened out as repeats. The two-measure FAMILY was already flagged
in fable_independent_2026/L32_NECESSARY_CONDITIONS.md, S7, for integration-constant
freedom. This work does not claim to discover or newly exclude that family.
The narrower addition is an explicit original-action deformation at FIXED
integration constant, including canonical response normalization. A bounded
repository text search found the broad screen but not this particular test.

## Source action and symmetry

Primary source: [gr-qc/0607111v5](https://arxiv.org/pdf/gr-qc/0607111v5),
header 10 April 2007 (the body carries a different later template date),
*Fine Tuning Free Paradigm of Two Measures Theory*, Eqs.(8),(9),(16)-(21).
The scalar-gravity action uses independent connection Gamma, metric, scalar
phi and measure density Phi. With q=alpha phi/Mp and k_g the source's
GR coupling (NOT the acceleration-law kappa), it is

    S=integral e^q [-(Phi+bg sqrt(-g)) R(Gamma,g)/k_g
                   +(Phi+bphi sqrt(-g)) g^(mu nu)phi_,mu phi_,nu/2
                   -e^q(Phi V1+sqrt(-g)V2)].

Under constant theta: g->e^theta g, Gamma fixed, phi->phi-Mp theta/alpha,
Phi->e^(2theta)Phi. Each displayed term is invariant for arbitrary bg,bphi,V1,V2.
The source's regular Einstein-frame reduction gives

    P(X,phi)=X-(A+Delta X)^2/(4D),
    A=V1+M^4 exp(-2q), D=bg A-V2, Delta=bg-bphi,
    X=g_E^(mu nu)phi_,mu phi_,nu/2,  signature +---.

The reduction assumes the regular measure/Einstein-frame branch. This source
is an interacting classical scalar-gravity model, not an established quantum
UV completion or a sourced MOND theory. Its claims about general cosmology
are not needed here.

## Deformation test (our calculation)

General-dimensional weight check: if the measure transforms with weight d/2,
a kinetic prefactor exp[(d-2)q/2] and potential prefactor exp[dq/2] give zero
net scale weights in d dimensions. The cited action is the d=4 specialization.
There is no dimensional argument selecting its relative kinetic couplings.

Hold bg,V1,V2,k_g,alpha and the integration constant fixed. Make the change

    bphi -> bphi + eta.

In the original action this adds only

    delta S = eta/2 integral sqrt(-g) e^q g^(mu nu)phi_,mu phi_,nu.

Its scale weights are 2-1-1=0. Diffeomorphism invariance is preserved too.
It changes no measure-dependent L1 term, so the measure-sector symmetry
associated with L1 is unaltered. This is not a separately appended vacuum
counterterm and not merely a field redefinition.

Expand P=-U+ZX+BX^2:

    U=A^2/(4D),  Z=1-A Delta/(2D),  B=-Delta^2/(4D).

There really is an identity

    4 U B + (1-Z)^2 = 0.

It survives the deformation. What fails is interpreting that identity as a
fixed physical ratio. For Z>0, canonical scalar normalization gives nonlinear
coefficient B/Z^2. The dimensionless invariant

    J=U B/Z^2=-A^2 Delta^2/[4(2D-A Delta)^2]

is unchanged by constant field rescaling, but

    dJ/dDelta=-A^2 D Delta/(2D-A Delta)^3,

which is nonzero for 0<Delta<2D/A. Thus changing bphi changes physical scalar
self-response while U and the Einstein coupling remain fixed. This tests
scalar response, not an already established baryonic gravitational force.

To avoid comparing off-shell field values, take the zero-integration-constant
branch M^4=0. Then A=V1, U is constant and a constant phi solves its reduced
field equation. This branch is allowed for the counterexample, not dynamically
selected. Choose V1>0, bg>0, V2<bg V1/2 and
0<Delta<min(bg,2D/V1). At X=0 the original measure ratio is
zeta=bg-2V2/V1>0, zeta+bg=2D/V1>0, bphi>0 and Z>0.
Small variations of bphi stay on this regular branch with the same positive
vacuum and Einstein-frame geometry. Local linear scalar kinetic health holds;
no all-background, quantum or UV health theorem is asserted.

For a static gradient h, E=-P(X=-h^2/2) is

    E=U+Z h^2/2-B h^4/4.

There is no h^3. Even forcing Z=0 would leave a quartic rather than MOND and
remove the assumed positive zero-gradient quadratic kinetic term. Introducing
a baryonic portal or identifying this scalar with gravitational acceleration
would be additional physics, not justified by this action.

## Disposition

The test answers the requested symmetry question for this action: an allowed
coupling changes the invariant response at fixed positive vacuum, without
breaking its stated classical symmetry. The shared-origin identity remains
true but does not select normalization. The absence of a MOND cubic is a
separate entry failure. No kappa value, protected quantum cancellation or
observational force prediction is claimed.

Frozen 4aea352e6b before executable. check.py verifies the displayed algebra
and scale weights; these are implementation checks, not physical validation.
The sign-reversal mutation breaks the coefficient identity as expected.
Self-review checked canonical normalization, actual invariant deformation,
regular measure branch and the fixed-state qualification. No independent review.
No downloads, numerical parameter search, new particle weights, or heavy run.
The source reduction is externally supplied; its entire derivation was not
independently reproduced. I1-I8: no measured inputs, no Friedmann substitution,
rho_DE footing only, classical hbar absent and no pi matching claim.

This refines an old negative screen; it is not a newly opened door. Further
work on this action requires an additional principle that forbids the displayed
kinetic deformation AND supplies the missing sourced cubic. None was found.
Do not proceed to spectrum engineering or loop calculations for it on the
strength of the shared denominator alone. The broader search remains unresolved.
