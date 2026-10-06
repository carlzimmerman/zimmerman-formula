# A stable adiabatic auxiliary sector has the wrong response slope for direct scalar MOND

Base: 85251b027ede0ec3a57bec52da9548b290fe4829. This tests a microscopic action premise beyond an arbitrary positive acceleration spectrum. It is a scoped obstruction, not a global impossibility of MOND or an explanation of 32pi. The original goal remains open.

## Declared action and source dictionary

In any spacetime dimension d>=3, use signature (-,+,...,+), a shift-symmetric phase phi and finitely many amplitudes R^A:

    L=-K_AB(R) partial R^A partial R^B/2+F(R)X-V(R),
    X=-partial phi partial phi/2, K>0, F>0.

The auxiliary amplitudes have a positive field-space kinetic metric. We examine a local adiabatic stationary branch: their derivative terms are negligible compared with their gap, and they respond by stationary minimization. This reduction must be valid at the tested source scales. It is not automatically valid near a caustic, at a massless gap, or for a time-dependent condensate.

For the proposed direct scalar force, matter has a weak linear coupling of one fixed sign and normalization to phi. Equivalently its leading scalar equation is div[P_X grad phi]=a positive fixed source coefficient times density, with a static fixed local clock q=phi_dot. The measured scalar force is proportional to g=|grad phi| by a positive constant; in a scalar-dominated deep-MOND regime the required effective mu is proportional to P_X and increases linearly with g. A different physical matter metric, derivative source coupling, simultaneous dynamical gravity or nonlocal response changes this dictionary and is not covered.

## Fixed-clock theorem

At fixed X the stationary amplitudes satisfy

    V_A-X F_A=0,
    H_AB=V_AB-X F_AB>0.

Positive H is the declared stable auxiliary-energy gap, not an assertion that every algebraic stationary branch is stable. The implicit-function theorem gives

    H_AB R_X^B=F_A,
    P(X)=F(R(X))X-V(R(X)),
    P_X=F,
    P_XX=F_A(H^-1)^AB F_B>=0.

Since X=(q²-g²)/2 on the fixed-clock branch,

    dP_X/dg=-g P_XX<=0.

Consequently this class cannot produce the increasing deep-MOND mu(g) on any open gradient interval under the stated source map. This is an exact sign argument, independent of the number of amplitudes, their curvature metric, or the value of a0. Curved positive K changes gap normalization and the range of validity; it does not change the algebraic sign. H is a coordinate-invariant bilinear form at a stationary point, so the test does not depend on amplitude coordinates.

## Fixed-charge control

Fix a local phase charge J=Fq instead. The appropriate amplitude energy is

    E_J(R;g)=V(R)+J²/[2F(R)]+F(R)g²/2.

Its stationarity condition is again V_A-X F_A=0 with q=J/F. Its Hessian at that stationary point is

    H_J=H+q² F_A F_B/F.

When the charge-ensemble gap H_J is positive, differentiating at fixed J gives

    (H_J)_AB R_g^B=-g F_A,
    dF/dg=-g F_A(H_J^-1)^AB F_B<=0.

Thus changing from fixed clock to a stable local fixed-charge minimization is not itself an escape. This is a local ensemble control; it does not construct a globally stationary phase with spatially varying q, or solve charge transport in a galaxy. Dynamic charge/phase evolution remains a different problem.

## Sharp finite-band and radial consequences

Let the target mu be g/a0 on [g1,g2], 0<g1<g2. Any nonincreasing model mu with a uniform relative error at most epsilon must satisfy

    (1+epsilon)g1/a0 >= (1-epsilon)g2/a0,
    epsilon >= (g2-g1)/(g2+g1).

The bound is sharp in this class of monotone responses: constant mu=2g1g2/[a0(g1+g2)] attains it, and a decoupled stable amplitude sector realizes a constant F. On a one-decade band the minimum error is 9/11, about 81.8 percent. Ten-percent fidelity would restrict g2/g1 to at most 11/9. These are exact conditional response bounds, not an observational error assessment.

There is also a geometric consequence if the static equation remains elliptic, mu+g mu'>0. In spatial dimension n=d-1, a spherical source outside its body has r^(n-1)mu(g)g=constant source flux. Therefore

    d ln g/d ln r=-(n-1)/(1+d ln mu/d ln g)<=-(n-1).

The force falls at least as steeply as the Newtonian radial power within this branch. Deep MOND instead has mu proportional to g and slope -(n-1)/2, giving 1/r in three dimensions. Ellipticity is an additional assumption for this radial inequality; the response-sign theorem does not require it. No GR coupling normalization in arbitrary dimension is inferred from the flux constant.

## Explicit complex-field failure and an important countercontrol

For a canonical complex amplitude F=R² and a desired P_X=k sqrt(-2X), k>0, on a spacelike branch, eliminating R would require

    X=-R⁴/(2k²),
    P=-k(-2X)^(3/2)/3,
    V=F X-P=-R⁶/(6k²),
    H=V_RR-X F_RR=-4R⁴/k²<0.

This algebraic embedding does reproduce the desired constitutive law but fails the positive-gap premise. At q=0 its homogeneous radial perturbation is tachyonic, since the phase-amplitude derivative mixing is spatial and vanishes at zero momentum. Stabilizing the potential elsewhere does not make H positive on the same target band. A dynamical completion retaining extra degrees of freedom must be tested rather than replaced by this unstable algebraic branch.

Negative P_XX is not a generic ghost theorem. The spacelike single-field control above has positive temporal quadratic coefficient P_X and positive longitudinal coefficient P_X+2X P_XX=2P_X. It is locally hyperbolic with radial speed squared 2 in the fixed Minkowski metric; that is not a causal UV completion certificate. The present obstruction is to the positive-gap adiabatic auxiliary model, not to every mathematically hyperbolic P(X).

## Primary source and missing physics

The action premise is motivated by Mukohyama and Namba, *Partial UV Completion of P(X) from a Curved Field Space*, arXiv:2010.09184, section II.A, equations (2), (4)-(11). The primary PDF was directly read. It describes a linear two-field kinetic completion and its Legendre relation, and explicitly allows convex **or concave** P(X) algebraic completions. It does not say that a concave branch has the positive-gap premise imposed here. Our arbitrary-amplitude sign theorem, fixed-charge extension, finite-band bound and radial application are independently derived above; no literature novelty is claimed. Source note and exact local evidence hashes are separate from PDF-byte authentication.

The simpler scalar source/acceleration premise differs from the actual logKGB accelerated clock and from the curvature-linked zero-stress carrier. Their successful checks cannot be pooled into this action. This test shows why requiring a stable microscopic amplitude response is not a selector for the desired coefficient in this class: it fails the MOND response before reaching a vacuum integral. Curvature couplings, additional invariants, finite-temperature/phase-space variables, nonadiabatic amplitudes and another physical matter metric remain possible changed premises. Each needs its own force and vacuum dictionary, abundance, propagation and source solution. No hbar is introduced; all equations are classical and dimensionally stated through the action in general d.
