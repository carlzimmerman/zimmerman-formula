# Candidate: no small BV clock-gradient jumps in the regular bounded class

Work in PF13's bounded weak class on the strict native on branch, with dphi in
spacetime BV, A,Pi Lipschitz, and metric C1 with locally integrable second weak
derivatives. Impose all Einstein equations with bounded native stress. Restrict
the acoustic states and frozen auxiliary/metric coefficients (in particular A)
to a sufficiently small fixed neighborhood of a D0=0
background with 0<u0=gamma r0²<=1/10. The neighborhood may depend on u0.
This theorem concerns jump parts of BV derivatives, not all BV singularities.

## Native equations have no jump-supported forcing

Write K=E h n. It is BV because dphi is BV, A is Lipschitz and the metric is
C1, with compact constitutive margins. The exact scalar equation gives

    div K=A_t Pi_x-A_x Pi_t-E(V_phi+W_phi) in L-infinity.

The auxiliary Jacobian is an ordinary bounded function, so contributes no
jump-supported measure. Compatibility of the two derivatives of phi gives
partial_t(phi_x)-partial_x(phi_t)=0. The algebraic Hilbert stress is also BV.
In the metric class stated above, the contracted Bianchi identity passes from
smooth metric approximations: connections converge uniformly, curvature in
L1 locally. Thus Einstein implies covariant div T=0 distributionally. Its
connection-times-T terms are bounded; the singular part of the coordinate
stress divergence is zero.

At almost every approximate jump point of the BV clock gradient, these three
measure identities give the Rankine–Hugoniot relations for K, clock
compatibility and full stress. This follows by the BV derivative jump part
or by rescaling to the two constant half-space traces; bounded right-hand sides
vanish under the rescaling. No smooth jump curve or one-sided derivative trace
of Pi is assumed. Continuous A,P and metric have common values at the point.

## The small jump must be an acoustic timelike jump

Freeze those common coefficients and use the invertible acoustic state
U=(m,b), m=exp(2beta)h phi_t/r, b=phi_x, with flux
F(U)=(-exp(2beta)h b/r,-phi_t). Compact positive R and subluminal c give the
local Legendre inversion already checked in PF13.

A nonzero state jump has a nonzero spatial normal component: otherwise its
Rankine–Hugoniot relation gives [U]=0. Write its speed as V. Then

    [F]=V[U],
    (integral_0^1 DF(U_minus+z[U]) dz)[U]=V[U].

For a sufficiently small neighborhood the averaged Jacobian has two separated
real eigenvalues close to the background acoustic speeds +/-c0. Hence V is
nonzero and strictly timelike, and the two outer clock-flow velocities in its
rest frame have the same nonzero sign. The common proper tangential clock
slope satisfies gamma s²<1/3, by the strict margin proved in PF12.

## Exact normal flux obstruction

In that local rest frame, common auxiliary A and common tangential clock slope
s give the common polarization conjugate B=s A>0. Scalar-base normal flux and
full normal stress continuity reduce to the previous partial Legendre corner
conditions (common potential terms cancel):

    f'(w_minus)=f'(w_plus)=j,
    w_minus j-f(w_minus)=w_plus j-f(w_plus),

with f as in PF12/SMALL_ACOUSTIC_CORNERS.md. Directly, f(w)=H(r=s sqrt(1-w²),A=B/s) up to common potential terms;
f'=-s h n_N and T_NN=f-w f'. Thus base-current and normal-stress
Rankine–Hugoniot give precisely these conditions. The topological current requires
no extra jump-product argument here: its divergence is the bounded Jacobian
already removed above. Exact strict convexity of f' for positive w, or reflection
for negative w, forbids distinct endpoints. Thus the approximate jump is zero.

Consequently the clock-gradient BV jump part vanishes in this neighborhood.
This extends the regular acoustic-corner exclusion to rectifiable BV jump sets.
It does not show that every BV function without jumps is classically smooth:
Cantor singular derivatives and continuous non-Lipschitz fields remain possible.
No entropy-process existence, uniqueness, or inevitability of a nonzero jump
from the terminal packet is proved by this result.
