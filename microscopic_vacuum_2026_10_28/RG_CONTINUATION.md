# MV28 second route: a microscopic steep term and a conditional RG ratio

This route follows the spectrum result; it does not change its frozen
model or computation. It supplies a microscopic building block and an
exact conditional ratio. A complete microscopic realization of both terms
has **not** been constructed here.

## A steep potential from gauge dynamics

Consider supersymmetric SU(N_c) gauge theory with N_f massive vectorlike
quark pairs, with masses m_i=lambda_X X, all nonzero. The checked primary
meson expectation values integrate to the holomorphic superpotential

    W_dyn=N_c[Lambda^(3N_c-N_f) det m]^(1/N_c),

up to the discrete branch and an X-independent superpotential term.
That term is irrelevant to this rigid derivative but not to gravity.
For canonical X metric, at large enough |lambda_X X| to decouple the
quarks, the F_X energy is

    U_np=N_f^2 |Lambda|^(6-2N_f/N_c)
                  |lambda_X|^(2N_f/N_c) |X|^(2N_f/N_c-2).     (R1)

Thus N_f/N_c=5/2 gives a cubic radial energy. The smallest integer example
is SU(2) with five vectorlike pairs; it is asymptotically free since
3N_c-N_f=1. In that example

    W_dyn=2 Lambda^(1/2)(lambda_X X)^(5/2),
    U_np=25 |Lambda| |lambda_X|^5 |X|^3.                     (R2)

This derives the *holomorphic contribution*, not a protected full scalar
potential. Its use requires nonzero heavy quark masses, small SUSY-breaking
splitting compared with their masses, adiabatic confinement dynamics, and
control of the nonholomorphic Kahler metric. For example the quark-splitting
ratio in (R2) scales as 5|lambda_X|^(3/2)sqrt(|Lambda|/|X|).
No claim extends this expression to X=0 or strong threshold corrections.
The source does not provide a cosmological vacuum or the PN28 portal.

Put s=ln(|X|/v) and retain the explicit trial portal Z_motion=exp(2s).
Then a cubic term is proportional to exp(3s). Scalar wavefunction running
can change its local slope, so exact log-pressure behavior is not protected
by the holomorphic exponent alone.

## The conditional stiffness/energy formula

Suppose an independent supersymmetry-breaking F direction contributes
U_F=|f|^2/Z_T(X)>0, without an interfering F_X cross term. Let the *actual*
positive contributions be U_np and U_F and define their local slopes

    b=dln U_np/ds,       a=dln Z_T/ds=-dln U_F/ds.

At a stationary vacuum with a,b>0 and no additional constant/sector,

    b U_np=a U_F,
    V=U_np+U_F,
    B_curv=U_ss/9.

Direct differentiation, retaining running a_s and b_s, gives

    B_curv/V = ab/9+(a b_s-b a_s)/[9(a+b)].                  (R3)

For approximately constant slopes, B_curv/V=ab/9. With b=3 this is a/3,
and U is exactly the two-exponential branch of VR28 with delta=a/3.
Here the requested microscopic calculation is a wavefunction response,
rather than a freely assigned scalar-potential stiffness.

In the Wilsonian metric convention calibrated to the explicit chiral-loop
threshold in the checked source, a=-2gamma_T when the relevant threshold
scale is proportional to |X| and no other threshold/state dependence
contributes. The sign convention is also checked by the positive Yukawa
gamma producing the familiar increasing F-term energy. Consequently

    B_curv/V approximately -2gamma_T/3                     (R4)

when b approximately 3, gamma is slowly running, and all hypotheses above
hold. This is a conditional matching relation, not a computed value for
the model in SPECTRUM_RESULT.md and not a universal constant. A full
threshold calculation is required to identify the relevant gamma in any
new model. Canonical X metric corrections and running supply corrections
already exposed in (R3).

## Two obstructions to the naive assembly

First, a gauge-invariant linear term fT with a constant f requires T to be
a gauge singlet. Its one-loop anomalous-dimension matrix contains a positive
semidefinite Yukawa term and no negative gauge-Casimir term:

    gamma_i^j=[(1/2)Y_ipq Y^jpq-2g^2 C(i)delta_i^j]/(16pi^2).

For a single singlet T, gamma_T>=0 at this order, so a<=0. Its F energy
increases rather than decreases. Adding it to the increasing cubic term
does not produce the proposed positive-radius stationary point. One cannot
assign a negative gauge contribution to that singlet by hand. Collective
gauge-breaking F directions, strong dynamics or other threshold structures
would be new models needing an explicit calculation.

Second, placing the two superpotential terms on the *same* F direction
does not add the two energies independently. If
W=fX+A X^(5/2), then

    U=|f+(5/2)A X^(3/2)|^2,

with an interference term and possible supersymmetric zeros. Treating this
as f^2+|(5/2)A X^(3/2)|^2 would give a false vacuum and a false ratio.
An orthogonal F sector must be demonstrated, including its stabilization,
backreaction, gauge invariance and gravity coupling.

## Relation to matter stability and full gravity

For constant slopes, U_ss-3U_s=b(b-3)U_np+a(a+3)U_F. The trial matter
closure therefore has positive compressibility for all s on its stable
positive-source branch when a>0 and b>=3. This supplies a concrete repair
target for the shallow-loop-potential obstruction found in the first route.
For b=3 its pressure becomes logarithmic only in the finite window already
described in VR28. At b>3 the eventual EOS is a power law instead.

If an additional constant C or other sector survives the supergravity
matching, V in (R3) must be replaced by V_total=U_np+U_F+C, while U_ss is
unchanged in that scalar description. An exact symmetry/matching condition
forbidding or calculating C is still needed. The source's integration
constant in W also becomes gravitationally relevant. No full gravitational
UV theory, exact R protection, complete orthogonal breaking sector, phase
stability, relative-only portal, or observational map is supplied by (R1).

The new exact result is (R3), and a gauge theory supplies the desired steep
building block. Equations (R4) and the two-term vacuum are conditional.
The next actual microscopic target is an explicit gauge-invariant collective
breaking sector with decreasing energy and controlled full gravitational
matching, rather than selecting gamma to reproduce an acceleration number.
