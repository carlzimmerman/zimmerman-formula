# Conditional spherical MOND reduction of the expansion bridge

Verdict: proved for the displayed reduced action, conditional as an
approximation to the full preferred-foliation theory. This is self-review.
Base 26426b7efec99cd38b6808d4ea4b78419fe0fef5. The original goal is not
achieved: beta and U remain free, and a complete sourced solution and its
health are unproved.

## Assumptions and the first missing implication

Start from the action and necessary equations in EXPANSION_BRIDGE_RESULTS.md.
Consider a spherical weak source in a subhorizon annulus. Write N=1+Phi,
sigma=Psi and g=Phi'>0. For this local reduction assume the matched expansion
is Theta=3H[1+small corrections], the cosmological integration constant in the
shift/trace constraint is suitably fixed, and lambda−1 is positive and not
parametrically small. The existence of a full solution with these properties
has not been demonstrated.

Use h=Hr and x=g/H. A useful proposed hierarchy is h<<x<<1,
|Phi|,|Psi|<<1, beta(P/H)^3<<1. It keeps the background radial acceleration
H²r smaller than g and places the expansion interaction in its deep-field
regime. It is not a uniform error theorem. In particular, the source-dependent
trace integration constant, clock-mode response, angular equations and
conserved matter stresses must still be checked in a coupled solution.

The formal ordering explains why retaining the cubic polarization term while
dropping other weak-metric cubic terms can be sensible. On a radial scale r,
Phi~gr=xh. The retained cubic density scales as M²g³/H, whereas a typical
weak-metric correction scales as M²Phi g², smaller by order h. Background
quadratic terms of order M²H²Phi² are smaller by order h²/x. These estimates
assume smooth profiles on scale r; they do not establish bounds on the actual
solution or justify boundary layers. At high field x>>1 this reduction cannot
be carried over without a new matching calculation.

## Spatial metric elimination, rather than an imposed flux law

The exact integrated spatial-curvature action per unit solid angle is

    M²N[exp(Psi)+exp(−Psi)]+2M²rN'exp(−Psi),

up to the boundary term already given in SPHERICAL_CLOCK_CONSTRAINTS_RESULTS.md.
Its quadratic part, after dropping the linear total derivative, is

    M²[Psi²−2rPsi Phi'].

Variation gives Psi=rPhi'. Substitution leaves −M²r²g².
At leading Theta=3H, the polarization part adds
2M²r²Pg−M²r²P²−C r²P³, with C=beta M²/(3H).
The reduced action including a leading nonrelativistic source density is

    Lred=−M²r²(g−P)²−C r²P³−r²rho Phi.

The source term comes from the leading lapse coupling. It is not a complete
relativistic material action or an exact static dust equilibrium.

Varying P and Phi gives

    g−P=3C P²/(2M²)=P²/a0,
    [r²(g−P)]'=r²rho/(2M²),
    a0=2M²/(3C)=2H/beta,  M²=1/(8πG).

Thus a regular spherical source has b=g−P=G M(<r)/r². This normalization
is derived within the reduced action; it is not borrowed from the earlier
prescribed-flux scalar BVP. An additional central integration constant would
represent an independently specified central mass and must be included when
the interior is not regular.

For an exterior mass M, the outward branch is exactly

    P=sqrt(a0 GM)/r,
    g=GM/r²+sqrt(a0 GM)/r.

In the deep limit b/a0<<1, g approaches sqrt(a0 GM)/r. If the weak
orbital dictionary v_c² approximately equals r g is valid in the stated
annulus, then

    v_c^4 approaches G M a0.

This is a positive connection between the trial action and the spherical
galaxy scaling law. The dictionary follows from the metric potential only
when the background and sourced shift terms are subleading. It is not an
observational fit, a disk/lensing solution, or an asymptotic-flatness claim at
arbitrarily large cosmological radius. The finite-radius correction inside
the reduced action is v_c^4/(GMa0)=(1+sqrt(b/a0))².

## What this says about 32π and the radius question

The same trial vacuum has Lambda=3H². The conditional force-law scale gives

    Lambda/a0²=3beta²/4.

Three illustrative beta values 2,10,20 give ratios 3,75,300, respectively,
without changing the algebraic structure of the spherical MOND law. Matching
that law therefore does not by itself select the numerical coefficient.
Nothing in this calculation sets beta²=128π/3 or fixes the vacuum energy U.

The user's radius question also has an exact dictionary. Restore units and
define r_star=c²/(2a0), the radius suggested by the Schwarzschild surface-
gravity formula. The trial scale a0=2cH/beta yields

    r_star=beta c/(4H),  r_star²Lambda=3beta²/16.

Therefore the target ratio 32π is equivalent to r_star²Lambda=8π.
It does not explain why that equality holds: it is the same unselected
beta condition. The de Sitter metric horizon itself is r_dS=c/H, giving
r_dS²Lambda=3. At the target coefficient r_star/r_dS=sqrt(8π/3)>1.
The density/acceleration radius and the actual vacuum metric horizon must
not be identified without an additional physical argument. Other preferred-
mode causal horizons have not been derived for this trial theory.

## Verification and next action

Nine exact symbolic identities pass in expansion_bridge_mond_reduction.py:
curvature expansion, spatial constraint, metric elimination, polarization,
flux variation, mass normalization, reduced force, deep circular-velocity
scaling and the coefficient ratio. Three 32-point reduced profiles use H=1,
GM=1e−16, r=1e−6 to 1e−5 and beta=2,10,20. Their maximum g/H is below
0.011 and beta(P/H)^3 below 3e−6; the background-to-field ordering proxy
Hr/(g/H) ranges up to about 0.01,0.0223,0.0315. These are illustrative
diagnostics only, not approximation errors or full-theory numerical solutions.
The validated bounded-run manifest pins the script, contract and result.

The first missing implication is a conserved-source, coupled radial solution
that realizes the assumed trace and orbital ordering. The coefficient selector
is a separate missing implication, even if that solution succeeds. This
checkpoint makes the scale dictionary less arbitrary within a controlled
formal reduction, but does not complete either obligation or solve 32π.
