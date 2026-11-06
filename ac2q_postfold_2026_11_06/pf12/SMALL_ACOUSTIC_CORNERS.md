# Small acoustic corners near the packet backgrounds

Candidate local necessary-condition result; not a theorem that a shock forms
or a complete classification of BV continuations.

At a D0=0 homogeneous state set u=gamma r0², A0=1/r0+gamma r0. The exact
native scalar speed in the clock rest frame is

    c0²=u/(1-u+u²).

For 0<u<=1/10 this is strictly between zero and one. A weak acoustic interface
has speed tending to +c0 or -c0 relative to that frame. Its proper tangential
clock slope s0 is r0/sqrt(1-c0²), so the corner-frame parameter is

    epsilon0=gamma s0²=u(1-u+u²)/(1-u)² < 1/3.

For example, the crude bounds u<=1/10, 1-u+u²<=1 and (1-u)²>=81/100
give epsilon0<=10/81<1/3. This avoids extending the statement to an unproved
larger range. The u=.001 fixture is inside this range.

In the interface rest frame, clock flow speed tends to the nonzero value
opposite the interface speed. Thus sufficiently small perturbations of both
outer states and interface speed retain same-sign nonzero flow, positive
on-branch charge, and epsilon<1/3. The size of this neighborhood may depend
on the fixed u; no uniform neighborhood as u->0 is asserted.

In this neighborhood the exact PF02 partial normal Legendre transform is

    f(w) = ([B sqrt(1-w²)-1-epsilon(1-w²)]²
             +epsilon(1-w²))/(2gamma),

where w is interface-rest flow velocity and B>0 is the common polarization
normal conjugate (B=s A in PF11 notation, not the transverse expansion).
Common regular tangential P derivatives add only an affine term in w, leaving
the following corner argument unchanged. The full coupled dynamic extension
was audited in coupled/time_layer_review/MATCHING_BRIDGE.md.

With no surface current/stress and regular common traces, the scalar and
normal stress conditions require

    f'(wL)=f'(wR)=j,
    wL j-f(wL)=wR j-f(wR).

For 0<w<1 the exact third derivative is

    f'''(w)=(3w/gamma)[4epsilon²+
       B/(1-w²)^(5/2)*(1-epsilon(3-2w²)(1-w²))]>0.

Consequently f' lies strictly below its equal-endpoint chord between distinct
positive wL,wR; integrating j-f' gives a strictly nonzero normal stress defect.
Reflection treats negative endpoints. No nontrivial such corner satisfies
all native flux equations. Equal velocities with common B force equal normal
polarization derivatives as in the prior corner derivation.

This excludes an ordinary small acoustic shock continuation in this regular
class. It does not establish that every postbreak BV solution has such a shock,
that its side current traces are regular, or that its Einstein equations admit
no diffuse/oscillatory defect. In particular no general entropy-solution theorem
for the constrained nonlocal AC2q system has been imported. A solution of a
chosen two-equation shock model is not a solution of the full stress equations
unless this additional condition is verified.
