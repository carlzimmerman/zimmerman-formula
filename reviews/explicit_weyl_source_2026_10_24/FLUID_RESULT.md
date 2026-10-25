# Independent continuation: volume-preserving medium symmetry

## Exact target and status

Frozen criteria e5333eab45. This is a distinct physical-medium symmetry, not another compensator rewrite. It supplies an apparent cubic invariant in three dimensions, but that invariant's static variation gives no MOND restoring force. Its covariant linear-density completion is dust plus a vacuum constant. Neither the symmetry nor this completion relates the two amplitudes. The original joint-selection goal remains open. Campaign standing facts and no-target conventions are those in FROZEN_CRITERIA.md; kappa=1/2 remains FITTED.

This is distinct from the earlier n+1-field spacetime determinant medium: here there are n comoving fields in n+1 spacetime dimensions and ordinary fluid dynamics. No claim is made that all fluid extensions fail.

## Symmetry and arbitrary invariant function

Let X^I, I=1,...,n, be comoving scalars. The symmetry group includes spacetime diffeomorphisms acting on the metric, baryonic matter and X, and internal relabelings

    X^I -> F^I(X),       det(partial F/partial X)=1.

Baryons can couple minimally to the spacetime metric; they are inert under the internal relabeling. This is not an additional nontrivial internal transformation of baryons. Define

    B^IJ=g^mu nu partial_mu X^I partial_nu X^J,
    b=sqrt(det B)>0.

Under relabeling B -> J B J^T, so det B and every function F(b) are invariant. The leading effective action is integral sqrt(-g) F(b). In particular the symmetry by itself does not forbid b^(1/3) or b^(2/3). On a uniform isotropic static map X^I=s x^I in n=3 these scale as |s| and s^2, while b scales as |s|^3. Therefore even the apparent suppression of the lower powers requires an extra analyticity assumption in b, not the symmetry alone. Analyticity at b=0 is especially nontrivial because the invertible-fluid description itself assumes b>0.

## Test the most favorable analytic truncation

Grant an expansion beginning with F(b)=-V-m b, with m>0, V>0. For a static orientation-preserving invertible spatial map, set J_i^I=partial_i X^I. In flat space b=det J. Its static energy contribution is

    E_m=m integral det J d^n x.

The determinant derivative is its cofactor C_I^i. Commuting partial derivatives in the antisymmetric cofactor formula gives the Piola identity

    partial_i C_I^i=0.

For compactly supported variations,

    delta E_m=m integral C_I^i partial_i delta X^I d^n x=0.

Equivalently det J=(1/n)partial_i(X^I C_I^i). Thus the cubic scaling in n=3 is a boundary density for this static branch; it is not the scalar energy |grad chi|^3 whose Euler derivative is a nonzero divergence. An isotropic amplitude scaling is not a functional equivalence of actions. A varying ansatz J_i^I=s(x)delta_i^I is also generically incompatible with J being a gradient, so it cannot be substituted to manufacture a scalar MOND equation.

## Gravity does not make it inert: it makes it dust

With zero shift and a static metric ds^2=-N(x)^2 dt^2+h_ij dx^i dx^j,

    b=det J/sqrt(h),      sqrt(-g) b=N det J.

Its variation is proportional to

    partial_i(N C_I^i)=C_I^i partial_i N.

For an invertible map, a strictly static fluid configuration of this linear-b model therefore requires partial_i N=0. It cannot remain at rest against an arbitrary baryonic gravitational potential; a dust flow can move under gravity. This avoids incorrectly declaring the covariant density topological or gravitationally invisible.

The standard stress tensor, or direct metric variation, gives for F(b)

    rho=-F,       p=F-b F_b.

For F=-V-m b this becomes

    rho=V+m b,       p=-V.

The m b piece is pressureless matter; V is a vacuum contribution. In homogeneous FLRW, b=b_initial/a^n from comoving-volume conservation. The fluid abundance remains state/initial-data dependent. No baryon-determined MOND amplitude is obtained. The absence of pressure supports gravitational motion, but no halo profile, caustic treatment or universal clumping history is derived here.

## Controls, source, and limits

Constant N gives the static bulk cancellation; nonconstant N restores the gravitational force condition rather than a MOND stiffness. Changing V leaves the relabeling symmetry and fluid rest-mass coefficient intact. Changing m changes the dust energy while leaving V independent. Adding nonlinear F terms gives pressure and real bulk response, but their coefficients are freely allowed by this symmetry and require a new source/force derivation. Higher derivatives, nontrivial charges, nonminimal baryon couplings and other field content are outside this pure linear-b test.

Primary foundation: [Ballesteros and Bellazzini, Effective perfect fluids in cosmology, 1210.1561v3](https://arxiv.org/html/1210.1561v3), version 2013-03-31, section 2, equations (2.4)-(2.14), inspected 2026-10-24. The source supplies the relabeling symmetry, F(b) action and perfect-fluid stress. The static determinant/lapse test above is derived here. No paper was downloaded and no numerical experiment was used. Review is same-agent analytic self-review; no universal no-go, microscopic protection or full positive-vacuum stability is claimed.
