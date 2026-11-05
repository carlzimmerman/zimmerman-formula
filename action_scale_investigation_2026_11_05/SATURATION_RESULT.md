# Near-saturation obstruction for the single-clock density candidate

The candidate is not radially hyperbolic across its entire formal classical
state domain. For every b>0, with the other positive parameters fixed,
there are regular local static initial data with positive radial kinetic
coefficient but negative constrained radial squared speed. This is a
statement about the action in SINGLE_CLOCK_RESULT.md, not the adopted v3s
action, and not a demonstrated instability of a physical galaxy.

## Exact sign obstruction

Use the constrained radial symbol in RADIAL_RESULT.md at a point where
d=p'+2p/r=0. All of X,rho=X+V,b,K,gamma,N,B,r are positive. Let
s=p/(a-p)>0 and h=s+s/(1+s)-2log(1+s). Then

    Num=2X+(bX/K)h > 0,
    D0=2X+1/gamma+(bX/K)h-(bX^2/(K rho))s^3/(1+s),
    c_radial^2=Num/D0.

The static metric equations imply

    B'+B N'/N=B^3 r Num/(2M^2),
    Mt=4(M^2)^2/(N B^3 Num)>0.

Thus a negative D0 here gives a gradient sign problem, not a negative
radial time-kinetic coefficient. Its large-s behavior is exact:

    D0/s^2 -> -bX^2/(K rho),
    Num/s -> bX/K,
    s c_radial^2 -> -rho/X.

In particular no positive choice of b removes this region. A smaller b
moves its location; it does not select one healthy positive coefficient
on the whole unrestricted domain. This includes, but does not single out,
the proposed coefficient.

There is an explicit finite sufficient threshold. Set

    A=2X+1/gamma, E=bX^2/(K rho).

Since h(0)=0, h'>0 and (s-h)'=(1+2s)/(1+s)^2>0, one has0<h<s.
For s>=1, s^3/(1+s)>=s^2/2. Hence

    D0 < A+(bX/K)s-E s^2/2.

If

    s >= max[1, 4rho/X, 2sqrt(K rho A/(bX^2))],

the positive constant and linear terms are each at most E s^2/4.
Consequently D0<0, strictly, at finite s within0<p<a.

## The state is compatible with the local static equations

At any r0>0 choose finite N0,B0>0, q>0, V>0 and a finite s above the
threshold, with p0=a(N0)s/(1+s) and d0=0. The four first-order static
equations in STATIC_RESULT.md determine N',B',p',d'. Their right-hand
sides are smooth near these data: N,B,r,gamma are nonzero and p<a by a
strict finite margin. The local ODE solution therefore exists and retains
these strict inequalities on a sufficiently small interval. Num>0 and
D0<0 also persist on a smaller interval by continuity.

This is not an off-shell choice of a lapse Hessian with the static
constraints ignored. It is a local static ODE branch. Reconstruction of
the omitted covariant equations uses the symmetry/constraint argument in
RADIAL_RESULT.md; no new independent stress-tensor implementation is
claimed. No regular center, asymptotic cosmology, positive-mass galaxy,
or complete exterior boundary condition has been imposed.

## Additional analytic structure of the d=0 slice

Direct differentiation, without a numerical root search, gives

    D0'=(bX/K) s^2/(1+s)^2 [1-(X/rho)(3+2s)].

It is either decreasing for all positive s, or increases to one maximum
and then decreases. Since D0(0)>0 and D0 tends to minus infinity, there is
exactly one positive zero on this slice. Also

    D0-Num=1/gamma-E s^3/(1+s)

is strictly decreasing from positive to negative and has one positive
zero. At that zero D0=Num>0, so it occurs before the D0 zero. Thus the
frozen radial symbol passes through a region with speed greater than the
metric light speed before its negative-speed-squared region. This is a
local characteristic comparison, not a proof of a retarded-causality
violation in a completed EFT. The derivation of this paragraph is analytic;
the recorded12 computation checks cover the preceding sign certificates
and limiting formulas, not a separate root-counting computation.

## Numerical diagnostic and boundaries of the conclusion

The predeclared arbitrary-unit fixture X=V=1,b=0.1,K=0.5,gamma=0.25,s=100
gives Num=20.3519716, D0=-965.7470383 and c_radial^2=-0.0210738121.
The40/80-digit arithmetic agrees within the declared1e-30 normalized bound.
This illustrates the sign; the exact asymptotic and finite-threshold proof
establish the all-positive-b statement. The fixture is not an observation
or an independently calibrated physical state.

As a formal continuum classical system, the negative constrained principal
speed prevents a uniformly healthy interpretation over the full stated
domain. To infer an instability in an effective theory requires wavelengths
short compared with the background variation scale yet below its unknown
ultraviolet cutoff. That additional window has not been established here.
Neither have physical initial conditions been shown to reach the bad region.

Possible escapes must change or justify something concrete: a dynamically
preserved restricted state domain, an appropriate cutoff, additional
operators, or a portal whose derivative structure differs. Finite constant
stiffness and adjusting b alone cannot remove this asymptotic obstruction.
A potential-only portal avoids this particular X-dependent term but does
not equal the full canonical energy density on general histories. None
of these escapes by itself fixes the MOND coefficient.

The four earlier shell examples and their converged radial box modes are
not retracted: they inhabit a different region. They must not be promoted
to a global health claim. Further refinement of those same examples would
not answer this new obstruction.

## Evidence and proof audit

saturation_v2.py passes12 checks. Omitting the negative portal term fails
exactly the asymptotic-denominator and fixture-sign checks. The original
expression-tree comparison error and its failed run are preserved in
SATURATION_ERRATUM.md and evidence/saturation. Corrected and mutation runs
have separate hash manifests. Self-review only.

Audit obligations: fixed finite positive parameters before taking s large;
strict p<a rather than evaluation at the singular endpoint; positive time
kinetic term; local on-shell ODE compatibility; conditional reconstruction
of covariant equations; asymptotic versus cutoff-valid inference; no claim
that observed sources occupy this branch. Verdict: proved for the formal
classical radial symbol and local static class as stated.
