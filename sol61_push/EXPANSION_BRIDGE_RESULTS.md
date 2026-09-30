# Source matching for the expansion-based scale bridge

Status: exact necessary reduced equations and an excluded source ansatz.
Self-review; the full theory and 32π selection remain unproved. Base checkpoint
e1354bea98a9b9a2cfc0965b29572cb28676708f. This tests the candidate proposed in
DERIVATIVE_BRIDGE_RESULTS.md rather than repeating its free-beta argument.

## A concrete interacting preferred-foliation branch

Use the stationary areal metric and definitions of
SPHERICAL_CLOCK_CONSTRAINTS_RESULTS.md, with constant lambda and no extra
scalar or R3² term in this restricted calculation:

    E=exp(sigma), Fkin=V'+V sigma', W=V/r, T=Fkin+2W,
    Theta=−T/N>0, Q=Fkin²+2W²−lambda T².

The trial action per unit solid angle is

    Lr=M²r²E Q/(2N)+M²r²N E R3/2+2M²r²P N'
       −r²N E[M²P²+U+beta M²P³/Theta],

where M²,beta,U are positive constants and P>=0. This is a defined branch
with a preferred foliation. It is not claimed to implement the tadpole
self-tuning mechanism or to fix U; the vacuum-offset problem remains.
Its pole at Theta=0 limits the domain of this action.

Because Theta contains N and V', its coefficient changes the metric
equations as well as the polarization response. Define

    B=beta N³P³/T²=beta N P³/Theta²,
    J=Fkin−lambda T−B.

Direct reduced variation gives the necessary vacuum equations

    J'+(2/r−N'/N)J−2(W−lambda T−B)/r=0,

    −M²Q/(2N²)+M²R3/2−2M² exp(−sigma)(P'+2P/r)
       −M²P²−U−2beta M²P³/Theta=0,

    a_clock=exp(−sigma)N'/N=P+3beta P²/(2Theta).

The lapse contribution has a factor of two multiplying the cubic term.
Treating Theta as a constant during lapse variation misses this term:
at fixed T the interaction is beta M²r²N²E P³/T. The shift current B
is also absent if a vacuum coefficient is inserted after variation.

A mass-free control N=1, sigma=0, V=−Hr, P=0 yields Theta=3H,
R3=0, Q=−3(3lambda−1)H² and U=3M²(3lambda−1)H²/2.
Its curvature is Lambda=3H². The earlier conditional bare dictionary gives
a0bare=2H/beta, Cbare=3beta²/4. These equations do not select beta.
Angular equations, foliation variation before symmetry reduction, conserved
matter stresses and full characteristic/constraint analysis are not completed.
The displayed equations are necessary, not a sufficient solution certificate.

## Two distinct foliations of the same source geometry

For a geometric control, take the static metric

    ds²=−Fdt²+dr²/F+r²dOmega², F=1−2m/r−H²r².

Here m is the mass length GM in the GR control. Restrict initially to F>0.
A unit timelike radial normal can have u^r=s(r),
u^t=sqrt(F+s²)/F. Since sqrt(−g)=r² sin(theta),

    Theta=(r²s)'/r².

Choosing s=Hr+C/r² gives constant Theta=3H. It is hypersurface orthogonal:
with A=sqrt(F+s²),

    u_mu dx^mu=−A[d t−s/(F A)dr],
    tau=t−integral s/(F A)dr.

The tau slices have radial metric 1/A². In ADM form N=A,
exp(sigma)=1/A and V=−A s. At C=0, A²=1−2m/r,
the slices have R3=0, and their clock acceleration is

    a_clock=m/[r² sqrt(1−2m/r)].

Thus a mass does not *kinematically* force the expansion invariant to become
mass dependent: constant-expansion slices exist. This construction is local
to its real timelike domain, not a complete foliation through both horizons
or a compact-source interior.

By contrast, unit-lapse, flat-spatial free-fall slices have
V=−sqrt(H²r²+2m/r) and

    Theta=3(H²r³+m)/[r^(3/2)sqrt(H²r³+2m)].

Writing y=m/(H²r³)>0 gives Theta/(3H)=(1+y)/sqrt(1+2y)>1.
For y>>1, Theta approximately scales as 3sqrt(m/2)/r^(3/2).
Using that normal would therefore make the trial bare acceleration coefficient
mass/radius dependent. A physical preferred foliation must be selected by
the theory; these different choices are not interchangeable calibrations.

## The constant-expansion GR shortcut fails its interacting shift equation

The constant-expansion geometry alone is not an interacting source solution.
Insert its C=0 functions N=A, sigma=−ln A, V=−A Hr into the necessary
shift equation above. Fkin=W=−AH and T=−3AH, so

    J=A[H(3lambda−1)−beta P³/(9H²)].

The exact shift residual reduces to

    −beta A P²P'/(3H²).

In a vacuum mass exterior, beta>0 requires P=0 or P'=0 wherever P is
positive. But the polarization equation is

    a_clock=P+beta P²/(2H).

For m>0 and r>2m its left side is positive and strictly decreasing with r.
The right side is a strictly increasing function of P>=0, forcing a positive,
nonconstant P(r). Therefore this frozen GR constant-expansion mass ansatz
cannot satisfy both necessary equations. This excludes that shortcut; it
does not exclude deformed constant-expansion solutions or general sourced
solutions of the trial action. Additional Horndeski/scalar terms would also
change the momentum equation and require a new derivation.

## Repo review and next decision

I read the current puzzle_32pi README and the N1/N2/N3 lane summaries under
sonnet55_push at the base checkpoint. They report respectively a geometric
radius-choice problem, a free polynomial coupling at nonlinear folds, and
inserted closure parameters in cosmological shell fixed points. I did not
independently rerun those lanes or adopt their observational numbers as new
evidence. Their summaries provide no already-derived coefficient selector
to import into this action. Their scoped no-go claims do not exclude every
physical theory.

The source test adds a specific obstacle: choosing constant expansion is
insufficient; polarization backreaction changes the shift constraint. The
next executable continuation of this route is a coupled radial solve for
N,sigma,V,P with conserved source and vacuum boundary conditions, including
the pole-domain condition Theta>0. It cannot solve selection by itself:
beta and U still require independent physical determination. A genuinely
different selector must enter the dynamics, microscopic normalization or
global boundary data, rather than equating the target to a free coupling.

Eleven symbolic identities pass in expansion_bridge_constraints_v2.py,
including the full reduced shift residual on the C=0 geometry. The original
ten-identity run is preserved; v2 adds that decisive check without modifying
its pinned predecessor. Both bounded-run manifests record inputs and outputs.
No interacting numerical source solution, stability proof or 32π derivation
was obtained in this checkpoint.
