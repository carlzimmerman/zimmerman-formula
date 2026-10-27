# Finite-radius pinning and its matter force

Scope: self-derived Newtonian spherical effective model, prescribed baryon
moments and fixed cold density during phase tests. This is a conditional
construction, not a microscopic discovery or an observed galaxy fit.

## Connection to prior results

The common constant-gap selector failed in the two-state research; the
vorticity barrier protects prepared uniform T but cannot supply formation
energy. Local_inside_out showed that a free exterior destroys its localized
fronts. Positive response-weighted stiffness can hold a mostly converted
reservoir, but did not select a free exterior. The new question is spatial
selection, with all energy derivatives retained.

The kinematic field is the existing C=omega²/(omega²+sigma²/Lrho²), now
computed with f(r)=.95/[1+(r/Rj)^8]^(1/2). Curl includes f'(r), and Jeans
pressure includes the same centrifugal support. No phase is assigned by
radius. Rj is a prescribed rotation scale, not a predicted galaxy parameter.
The turnover can make curl pass through zero and then change sign. Squaring
curl does not erase the intervening low-C region; its consequences remain.

## A bounded auxiliary interaction

Per unit T mass introduce

    e_z = (k/2)(1+C²/c²) z² - g C z,  k>0, c>0.

Completing the square gives z*=g C/[k(1+C²/c²)] and

    min e_z = -epsilon B(C),
    epsilon=g² c²/(2k),  B(C)=C²/(C²+c²).

This derives the reduced energy from the stated auxiliary interaction. It
does not derive that interaction from known particles or determine epsilon,c.
At finite cold mass the binding energy is bounded below by -epsilon Mc.
The mode's response time, inertia, noise and actual energy receiver remain
unspecified. The experiments assume instantaneous minimization.

Add -epsilon integral B(C) dM_T to the response-weighted energy. Epsilon is
1e5 (km/s)² in the declared test, common across both templates; c is a common
dimensionless feasibility input, not an independently measured quantity.
The full finite-grid phase gradient and Hessian acquire respectively

    -epsilon m_i B_i h'(x_i),
    -epsilon diag(m_i B_i h''(x_i)).

These derivatives allow spatially selective binding and a finite interface.
They do not eliminate the binding force on matter or on the baryons.

## Actual interface restoring force

For any differentiable front family x(R), its generalized force is exactly

    F_R = -grad_x E . dx/dR,
    k_R = (dx/dR)^T H (dx/dR) + grad_x E . d²x/dR².

At a stationary state the second term vanishes. For the locally linear
translation mode x=x*+v deltaR it vanishes identically. We use
v=-x*'(r) exp[-((r-R*)/(.15 Rreservoir))^4], centered on the outer q=.5
crossing. This moves the interface without translating the entire core.

For FI-2 Rj=5b,c=.03, n256, R*=28.44968 kpc, k_R=1.919763 in units
Eunit=Mb a0 rM and Runit=rM. The residual generalized force is2.52e-7.
Thus F_R(deltaR)=F_R(0)-1.919763 deltaR to first order. The physical
stiffness is (Mb a0/rM) k_R. Energy second differences give1.920522
(relative difference3.95e-4). The corresponding n128 result is1.916833.
The lowest full phase Hessian eigenvalue is positive (.21645 at n256).
This demonstrates local energetic phase stability for this discretization,
not stability to moving mass, live baryons, 3D deformations or noise.

Finite shifts of +/-.2 kpc in this mode relax back within phase-vector
distance3.39e-6 of the stored minimum; the initial distance is .04396.
The positive fixed metric satisfies M xdot=-grad E and Qdot=grad E^T
M^-1 grad E, with relative E+Q error below1.08e-9 over100 internal units.
No Gyr interpretation is attached to that time.

## Derive the matter force rather than infer it from phase stability

Let n=dMc/dr, q=h(x), and u=M_T(<r)/r² in dimensionless units. Write
mu_u for the variation of W, barrier and response-weighted stiffness with
respect to added T mass through u. In the interior continuum,

    mu_u(r) = integral_r^infinity [w'(u)+beta C s(x) F'(u)
                                  + .5 ell² F'(u) x'²] ds,

with the appropriate exterior matching contribution. The code uses the
actual discretized W tail and minimized gradient tail, including gamma'(M).
At fixed Eulerian phase, the cold mass potential is

    mu_c = q[mu_u-epsilon B].

Let mu_q=(1/n) deltaE/deltaq, including the interface Euler derivative.
Independent T and F mass variations give exactly

    mu_T = mu_c + (1-q) mu_q,
    mu_F = mu_c - q mu_q.

In the finite grid mu_q=E_x/(m h'). At a stationary mixed phase mu_q=0;
the two potentials coincide. At pure T the correction to mu_T vanishes.
For the tested interior use (1-q)/h'=cos(pi x/2)/[pi sin(pi x/2)] to
avoid catastrophic cancellation near x=1. The F endpoint requires its own
one-sided interpretation; we do not use an undefined T chemical potential
where T is absent to claim an interior force result.

The actual additional T acceleration is -d mu_T/dr, and total T acceleration
is -g_total-d mu_T/dr. The finite-difference T mass variation (adding T while
holding F fixed) verifies the potential to2.38e-9 relative in its test.
The total mass profile has been granted the parent law, so its initial
g_total=law(gb). It remains a law-following static configuration only if
the additional acceleration equals g_total. This is a force-balance test,
not an inferred scatter or a prediction of the later live mass distribution.

As a check, uniform T, no binding and no phase gradient give mu_u'=-u/(1-u),
so a_T=-(gb+gF)+u²/(1-u), reproducing the prior relation. With binding alone,

    a_T=-(gb+gF)+u²/(1-u)+epsilon B'(r).

Consequently the source in that restricted equilibrium is gb+gF-epsilon B'.
It is incorrect to discard this term just because q is nearly1. The full
force calculation also keeps the barrier and interface contributions.

## Reciprocity on baryons

The binding contribution to the variation in the prescribed kinematic field
is -epsilon n q B_C deltaC, where B_C=2 C c²/(C²+c²)². The barrier contributes
beta r² s F deltaC. With A=omega² and D=sigma²/Lrho²,

    deltaC = [D deltaA-A deltaD]/(A+D)²,
    deltaA=2 omega . curl(delta v_b).

Thus the same functional supplies a baryon momentum/stress term after
integration by parts, plus variations of dispersion and density derivatives
in D. Setting these to zero in an evolving system would violate reciprocity.
Here baryons are fixed as an explicit necessary-test approximation. Their
live backreaction and kinetic completion have not been simulated. This is
an additional reason a phase minimum alone cannot close the physical target.
