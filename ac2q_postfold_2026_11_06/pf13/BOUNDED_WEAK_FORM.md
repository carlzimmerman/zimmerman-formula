# A direct bounded weak formulation, without expanded derivative products

This defines and checks a candidate native variational weak class. It does not
prove existence from PF12 terminal data or uniqueness. It does not describe
arbitrary concentration measures.

Work in a regular conformal planar chart, E=exp(2alpha+2beta), Pi=exp(2beta)P,
r=exp(-alpha)sqrt(phi_t²-phi_x²)>0. Take phi,A,Pi locally W1,infinity, dphi
locally BV, bounded multiplier mu>=0, compact clock/cap margins, and regular
metric coefficients. Impose Ar>=1 and mu(Ar-1)=0 almost everywhere. Define

    H=r²/2-V-W+(Ar-1-gamma r²)²/(2gamma), h=H_r,
    Deff=(Ar-1)/gamma-r², D=Deff-mu,
    L=E[H-mu(Ar-1)]-A(phi_t Pi_x-phi_x Pi_t).

The density is locally integrable; first variation with smooth compact test
functions is meaningful in the strict timelike/cap domain. The equations are

    phi_t A_x-phi_x A_t=exp(2alpha) W_P,
    phi_t Pi_x-phi_x Pi_t=E r D,
    div J=-E(V_phi+W_phi),
    J^t=E(h-mu A)n^t-A Pi_x,
    J^x=E(h-mu A)n^x+A Pi_t,
    n^a=-g^{ab}phi_b/r.

The first two identities hold almost everywhere. The scalar equation is weak:
for every compact smooth eta,

    integral J^a partial_a eta = integral E(V_phi+W_phi) eta.

All displayed products are ordinary bounded measurable products. No product
of a discontinuous coefficient with a derivative measure is required. In
particular one must not substitute an unproved meaning for R n(r), D_r n(r),
or frame commutators from the expanded smooth equations.

Require ALL Einstein equations in addition, not just the two conformal wave
equations. The on-shell native stress to impose is

    T_ab=H g_ab+(rh-mu Ar)n_a n_b (longitudinal base),
    T_perp=H+P W_P.

A sufficient concrete metric class is C1 with distributional second derivatives
locally integrable and with the full Einstein tensor equal to this bounded
stress. One can enlarge this separately to junction metrics, retaining their
junction conditions. The bounded class above carries no matter surface stress.

## What is native, and what is being defined

The displayed action is the exactly equivalent auxiliary action on smooth
native fields, before its topological integration by parts. Its weak first
variation gives the equations above directly. Thus this is a concrete extension
of the native smooth equations and variational principle, with no new bulk term
or physical regulator. Equivalence to every possible distributional reading of
the original higher-derivative P.acceleration action is not asserted; such a
reading must specify its own singular products and boundary terms.

The original unexpanded Noether/Hilbert equations remain essential. Weak scalar
and polarization equations alone do not justify applying the smooth Noether
chain rule to infer weak stress conservation. Ordinary scalar shock examples
already show why an extra energy equation can fail at a jump. Here the full
Einstein equations retain that condition and exclude the reviewed regular
acoustic corners. A finite-current bound is automatic in this bounded class,
but it does not establish existence or uniqueness of its solutions.

For piecewise regular members with a regular interface and common continuous
phi,A,Pi, bounded explicit sources give the usual normal scalar-current jump
zero; the auxiliary identities and their variational forms supply the normal
polarization conditions. Full Einstein and bounded stress provide the ordinary
geometric and stress flux conditions. This recovers, rather than evades, the
previous regular-corner obstruction.
