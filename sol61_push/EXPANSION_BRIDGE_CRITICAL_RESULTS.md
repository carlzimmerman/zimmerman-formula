# Critical-point family, finite slope candidates and two-sided tests

Verdict: local critical-point existence follows for every positive beta in the
specified restricted radial system. Finite two-sided integrations support a
negative-slope continuation candidate, but do not prove a smooth global
solution or select 32π. Self-review; base a92c1c1a1dee6cb676461b810c0bbabd5cfacfe3.

## Local critical-point theorem

Use C,D,R from EXPANSION_BRIDGE_RADIAL_RESULTS.md, with H>0,
B=lambda−1>0, S=3B+2, beta>0 and U/M²=3SH²/2. At a critical state fix
W=−H and put

    sigma=k r³, deltaTheta=d r³, P=p r².

For each fixed H,B,beta there is a sufficiently small positive-radius
interval on which C=D=R=0 has an analytic branch with

    k→p_star, p→p_star=S H³/(beta B),
    d→d_star=−S H⁴/(beta B²).

This is a theorem about critical *states*, not existence of a trajectory
passing through them or source/cosmology boundary matching.

Proof: use the scaled equations F=(C/r,D/r,R/r²). Their apparent poles at
r=0 are removable under the displayed substitution. For example, the
curvature term is [1−exp(−2k r³)]/r³ after scaling and has limit 2k;
the polarization term tends to −2p. The trace denominators tend to 3H
and ctheta tends to B, both nonzero. Taylor expansion therefore gives the
analytic limiting map

    F0=(2k−2p,
        2H²S/B−2beta p/H,
        −2beta p²/H+4H²S p/B+2HSd).

Its zero is the state above. The Jacobian with respect to (k,d,p) at
that zero has determinant

    det dF0/d(k,d,p)=8beta S>0.

The analytic implicit-function theorem then gives the local branch. Its
P and Theta stay positive by continuity, and the local static metric factor
is positive for sufficiently small r. The size of that interval can depend
on all parameters; no uniform radius bound is claimed.

This rules out local C=D=R compatibility alone as a beta selector. It leaves
global boundary conditions, source regularity and health as possible additional
restrictions. Seven exact symbolic identities check the limiting root,
Jacobian and normalized slope polynomial; the removable-pole argument above
supplies the analytic link that a finite root scan alone would not prove.

## Finite radial slope candidates

Write the four non-lapse derivatives as y'=b+kvec z, z=P'. Here
y=(sigma,deltaW,deltaTheta,P) and b,kvec are the affine coefficients in
the exact radial closure. At C=D=R=0, differentiating D P'+R=0 gives

    D1 z²+(D0+R1)z+R0=0,

where D0=partial_r D+grad D dot b, D1=grad D dot kvec, and similarly
R0,R1. This is necessary for a twice-differentiable crossing; it is not
by itself an existence theorem for one.

On the small-radius critical branch, the leading coefficients are

    D1=−2beta/(H r)+lower-order terms,
    D0+R1=8H²S/B+terms tending to zero,
    R0=14S²H⁵r/(beta B²)+terms smaller than r.

These follow by differentiating the leading D and R terms before substituting
the critical values; differentiating a constraint already set to zero would
erase the needed transverse information. With q=S H³r/(beta B), the
normalized polynomial is z²−4qz−7q², giving

    P'_plus/minus=q(2±sqrt(11))+terms smaller than r.

Thus one slope is negative and the other positive. The leading discriminant
is positive, so both remain real at sufficiently small radius. This square
root describes local radial slopes, not the target acceleration coefficient.
No novelty claim is made.

Six double-precision critical roots at beta=2,10,20 and r=0.001,0.002,
with H=1 and lambda=2, have maximum scaled residuals below 7e−15.
Complex-step derivatives of the original cancellation-resistant algebra give
two real finite slopes in every case, agreeing with the leading expressions
to better than 1e−6 relative. The corresponding conditional curvature ratios
are 3,75,300; no target value was inserted. These finite checks supplement
the analytic local argument and do not verify global physical admissibility.

## Two-sided finite test of the negative slope at beta=10

At critical radius 0.001 with W=−H choose the negative slope, numerically
P' approximately −0.000658312396. Start at radii rcrit(1±epsilon)
using a first-order Taylor state, then project sigma onto the exact positive
root of C=0. Test epsilon=0.001,0.0005,0.00025. Integrate inward to
r=1e−6 and outward to r=0.1 using the exact radial IVP system.

All six integrations reach their endpoints. At 128 sampled points per branch,
P,Theta and the static metric factor are positive; D stays negative on the
inner branch and positive on the outer branch. The largest normalized lapse
residual is below 1.1e−14 and shift residual below 2.3e−16. These residuals
test the necessary reduced system, not all covariant equations.

At the smallest start offset the inner P is about 5.52135605e−4 and outer
P about 1.06933389e−10. Halving the start distance reduces successive
endpoint P differences by factors about 3.956 inward and 4.000 outward,
consistent with second-order initialization error. The excluded gap around
the critical point shrinks with epsilon; no integration or proof evaluates
the singular quotient exactly at the point. Convergence of these few finite
tests is not a rigorous smooth-crossing theorem.

The outer branch decays over this interval, unlike the growing branch found
by the earlier event shooting. This is useful positive evidence for pursuing
the negative-slope manifold. But at the outer endpoint r² deltaTheta is
about −7.47e−16, rather than an independently imposed exact zero, and no
horizon or infinite-radius boundary has been matched. At the inner endpoint
deltaW is about −0.4022 despite small metric potentials: an appreciable
preferred-flow mode remains. No conserved matter interior has fixed it, and
the mass label in the original IVP diagnostic is not a calibrated material
mass for this critical-point construction. Do not call these profiles a
complete galaxy solution or use them for an observational coefficient claim.

## Evidence and next step

expansion_bridge_critical_points.py and its contract pin the seven symbolic
checks and six finite roots. expansion_bridge_critical_branches.py records
the two-sided offset integrations and convergence diagnostics. Both list
the original radial IVP code as an execution input; the reviewed definitions
are loaded without changing or rerunning its old evidence driver. The
bounded-run manifests record actual argv, hashes and outputs. Unpinned
exploratory scripts were superseded by these reproducible runs.

Next: prove local critical-manifold crossing, then vary critical W and radius
to match a conserved, regular source and the chosen outer foliation condition.
This is now a manifold/boundary problem rather than division through D=0 or
an event classification alone. The fixed-beta tests must precede any claim
that a boundary eigenvalue chooses beta. The local theorem explicitly leaves
all positive beta available. Vacuum-energy protection, the missing covariant
equations, full causal/dynamical health and the actual observed Newton/galaxy
dictionary remain unfinished. Exact 32π has not been derived.
