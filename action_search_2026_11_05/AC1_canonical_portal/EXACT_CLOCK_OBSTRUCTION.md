# The canonical portal preserves a caustic-prone exact clock branch

**Claim:** for the specified v3s clock/polarization action plus the canonical
potential-only scalar portal, there exist smooth unit, hypersurface-orthogonal
clock initial data on its exact scalar/dust FRW metric whose smooth clock
foliation ends in finite cosmic time, while that metric and the scalar/dust
background remain regular. This does not prove a curvature singularity, a
negative-energy mode, or failure of every selected charged solution. It does
refute unconditional global smooth-clock regularity for this candidate class.
Kappa=1/2 FITTED; no complete healthy action established.

## Why this is a full exact branch, not a principal-part extrapolation

Use the action skeleton in AZC1 ACTION.md, replacing its independent cuscuton
sector by canonical X-V(phi) and a²=xi G V(phi). Keep tau and phi independent.
Choose P=0, Q=sqrt(-grad tau.grad tau)=1, multiplier lambda_P=0.
A normalized gradient with Q constant is geodesic, so A_mu=0.

- W starts at K P_mu P^mu/2, so W and its first derivatives in P,phi and
  the metric vanish at P=0. The norm p=K sqrt(P²) need not be differentiated
  alone at zero: the complete W is differentiable there by its expansion.
- The P.A term's P variation is A=0; all its other first variations carry P.
- The switched term is F(s)=[max(s,0)]², s=D.P=0. F(0)=F'(0)=0, so all
  first variations vanish. This argument does not assume F''(0) exists.
- The clock norm penalty is proportional to (Q-1)². It and its first
  variation vanish, including the metric variation.
- The multiplier equation n.P=0 holds and lambda_P=0 removes its other terms.

The remaining equations are exactly Einstein plus canonical scalar plus dust.
Thus the AZ40 homogeneous solution remains a solution for any locally regular
unit gradient clock on it, even if that clock is not comoving with the dust.
This reasoning works for any independent scalar sector with W(0,a)=0 and
vanishing first derivatives; changing only that sector does not remove this
clock branch. It does not apply to added terms that directly constrain the
clock's expansion/shear or align it with the independent scalar.

## Smooth initial data and focusing

In flat FRW ds²=-dt²+a(t)² dvec(x)², label planar geodesics by x(t0)=q.
Conserved covariant spatial momentum p=a² dx/dproper_time gives

    dx/dt = p/[a² sqrt(1+p²/a²)],
    x(q,t)=q+integral[t0,t] p(q)/[a² sqrt(1+p(q)²/a²)] dt.

Choose p(q)=-lambda*q*exp(-q²/L²), with lambda>0,L>0.
At a(t0)=1, initial eikonal data can be chosen as

    tau(t0,x)=lambda*L²*(1-exp(-x²/L²))/2,
    tau_t(t0,x)=sqrt(1+p(x)²).

Then -tau_x=p and Q=1. The data are smooth and timelike at every finite x,
and n=-grad tau is hypersurface orthogonal. In particular tau need NOT be
constant on the initial cosmic-time slice. Before crossing, the Hamilton-Jacobi
characteristics produce the required unit gradient clock. Proper time and
cosmic time have not been equated for moving trajectories.

At q=0, p=0 and p'=-lambda, so differentiation gives exactly

    J(0,t)=partial x/partial q=1-lambda*integral[t0,t] dt/a(t)².

For any chosen finite t1>t0 with a smooth positive scale factor, the integral
is strictly positive. Taking lambda larger than its reciprocal forces J to
reach zero before t1. Thus this existence statement does not depend on a
numerical scan or on expansion continuing forever. At the center,
partial p/partial x=-lambda/J diverges. Either another characteristic crossed
earlier or this one does; either establishes finite loss of the smooth clock
foliation. The FRW curvature, density and independent scalar need not diverge.
A weak continuation or branch-selection rule is an additional obligation.

## Concrete exact cosmological witnesses

At y0=1, a(t0)=1, the AZ40 branch gives

 H(N)²/H0² = Ob0 exp(-3N)+(1-Ob0)exp[-3(1-beta)N],
 Ob0=sech(1)²,
 I(N)=integral[0,N] exp(-2n)/(H(n)/H0) dn,
 J=1-(lambda/H0) I.

The six frozen witnesses use beta=1/3,2/3,.9 and lambda/H0=10,100. All have
roots in 0<N<1, with 40/80-digit agreement. Reversing the momentum slope gives
J=1+(lambda/H0)I>0 for N>=0 and J=2 at the original crossing.

The original centered-difference step pair (1e-4,5e-5) fails its 1e-5 agreement
line at lambda/H0=100. Those failed outputs remain in evidence/clock_original/ and
the retained local clock_initial/. The separately frozen pair (1e-5,5e-6) tests the same map and
threshold, also requiring the differences to scale by approximately .01.
The original failed label is not overwritten. Numerical derivatives corroborate
the exact expression, not supply the existence proof.

## Self-audit

Primary verdict: **proved as written** for the scoped existence claim above,
by explicit branch substitution and the characteristic Jacobian. Author
self-review only; no independent review is claimed.

Passed: first variations including the switched term; independent phi/tau;
initial timelike normalization; spatial momentum conservation; distinction of
proper/cosmic time; smooth expanding FRW during the finite witness interval;
quantifiers (some admissible clocks, not every solution).
Not addressed: physical branch selection; weak continuation; charged background
observables; full causal response; added clock-regularization action.
Out of scope: global exclusion of all healthy modified-gravity theories.

This narrows the next action calculation. The canonical portal improves the
scalar density-tie route but does not, by itself, remove the existing clock
regularity gap. X14's previously studied K² completion is a separate action
with its own unresolved nonlinear and health questions; its passes cannot be
transferred here. No new literature claim is made from that inherited report.
