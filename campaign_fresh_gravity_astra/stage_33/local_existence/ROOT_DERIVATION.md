# FGF046 root candidate: direct C1,1 construction and continuation

Frozen independent attempt before reading new author/reviewer proofs. An author
message reported a C0 iteration/C1 interpolation route after my private derivation
had reached the same route; that preview preceded this file freeze. Therefore
this is NOT a fully blinded root freeze. The proof and independent audit, not
route agreement, must carry the claim.

## Problem and local-to-global auxiliary extension

Write c=cs>0, q=log(n/nref), R=v+cq, S=v-cq. The fixed-potential equations
are equivalent for positive n to

R_t+[(R+S)/2+c]R_x=-g(x),
S_t+[(R+S)/2-c]S_x=-g(x).                                      (1)

Take a closed regular positive-side interval U in the inherited signed-Q
crossing, and a larger regular open interval containing it but not the cusp or
walls. Smoothly extend background q0=log(rho/nref) from a neighborhood of U
to a bounded smooth function q_e on the real line, constant outside a compact
interval. Such an extension is obtained by multiplying q0 minus a constant
by a smooth cutoff supported strictly inside the larger interval. Set
rho_e=nref exp(q_e)>0, phi_e=-c² q_e+mu and g_e=-c² q_e'. On U these equal
the physical background with its chosen mu. Thus the extension preserves
hydrostatics, but is an auxiliary fluid problem only: no external MOND field
solution is asserted. g_e and its first two derivatives are bounded.
Initial velocity is EXACTLY V f((x-x*)/ell), V=v0N,ell=L/N³, same zero-extended
C1,1 polynomial. R0=v+cq_e,S0=v-cq_e. The extension is fixed independently N.

Here and below C_b^{1,1} means bounded C1 functions with bounded first
derivative and globally Lipschitz first derivative. The latter allows f'' jumps.
We construct (1) on the line and prove local independence of the auxiliary
extension. No smoothing of the initial velocity is used.

## Explicit iteration bounds

Use max component norms. Define U0=||R0,S0||inf, P0=||(R0',S0')||inf,
Q0=max Lip(R0'),Lip(S0'), F0=||g_e||inf, F1=||g_e'||inf,
F2=Lip(g_e'). Choose any fixed physical tau>0 and put

P*=P0+tau F1+1/tau, Pbar=2P*,
Q*=Q0+tau F2, Qbar=4Q*,
T=min(tau,1/(16P*)).                                           (2)

P* has inverse-time units; Q* has inverse-length inverse-time units. No
unitless constant has been added to a dimensional norm. If Q*=0, all second
spatial derivatives below vanish and that special case is immediate.

Start U^0(t,x)=(R0,S0)(x). Given U^m=(R^m,S^m), solve the TWO linear
transport equations with velocities lambda±^m=(R^m+S^m)/2±c, source -g_e,
and the same initial data, by integrating along their characteristic flows;
call the result U^{m+1}. For a bounded velocity continuous in t and globally
Lipschitz in x, that flow exists by direct successive approximation of its
integral ODE on short intervals, continued to T with the uniform speed bound.
The ODE successive differences are bounded by factorial time powers of the
Lipschitz constant; uniqueness follows from the same integral inequality.
Its label derivative solves J_t=lambda_x J, J(0)=1, so it is positive and
bounded above/below at finite time. Inverse maps exist since the displacement
is bounded. Differentiating this explicit formula yields the transport solution.

Inductively, ||U^m||inf<=U0+T F0, ||U_x^m||inf<=Pbar,
Lip_x U_x^m<=Qbar on [0,T]. The base satisfies these bounds. For the first
derivative of the next transport solution, the label-Jacobian formula gives

P_{m+1}(t)<=(P0+tF1) exp(Pbar t)<=P* exp(1/8)<Pbar.              (3)

For the Lipschitz derivative, differentiate once more a.e., or take difference
quotients of the first-derivative transport formula. The second-derivative
transport equation is

D_m U^{m+1}_{xx}=-2 lambda_x^m U^{m+1}_{xx}
                 -lambda_{xx}^m U^{m+1}_x-g_e''.

Here |lambda_x^m|<=Pbar, |lambda_{xx}^m|<=Qbar a.e. It yields

Q_{m+1}(t)<=(Q0+tF2+t Qbar Pbar) exp(2Pbar t)
 <=Qbar(1/4+1/8)exp(1/4)<Qbar.                                (4)

The a.e. derivative/difference quotient bound is legitimate for C1,1
coefficients and data: their first derivatives are Lipschitz, their flows are
C1 with Lipschitz spatial Jacobian, and the first-derivative formula has those
same properties. Integrating the bounded difference quotients gives the
Lipschitz estimate without a pointwise f'' value at a join. Formula (4) also
shows why Q0's large N7 value does not enter the time smallness gate.
The amplitude estimate follows directly from the characteristic source integral.

## Contraction and actual C1 limit

Subtract consecutive transport equations, using the velocity of U^m:

D_m (U^{m+1}-U^m)=-(lambda^m-lambda^{m-1}) U_x^m.

The initial difference is zero. Since the average defining lambda has
component max-norm Lipschitz constant one, the sup norm on the whole slab gives

||U^{m+1}-U^m||inf <=T Pbar ||U^m-U^{m-1}||inf
                    <=(1/8)||U^m-U^{m-1}||inf.                 (5)

The first difference is finite; therefore the series converges uniformly.
To see that a C0 limit has not been mistaken for a classical solution, for any
scalar difference d with Lip(d_x)<=2Qbar one has, for h>0,

|d_x(x)|<=2||d||inf/h+Qbar h.

Minimizing in h bounds ||d_x||inf by 2 sqrt(2Qbar ||d||inf). Thus the
geometric series of consecutive FIRST derivatives also converges uniformly,
with ratio at most sqrt(1/8), for each fixed finite N. If Qbar=0 the bounded
affine difference has zero derivative. The limiting U_x is continuous, remains
Lipschitz in x, and is the derivative of U by the integral identity in x.
The equations give U_t^{m+1}=-lambda^m U_x^{m+1}-g_e, also uniformly convergent
to a continuous function. Integrate in t to identify it as U_t. Consequently
U is genuinely C1 in spacetime, uniformly C1,1 in x, satisfies (1) pointwise
and has the exact initial trace. n=nref exp[(R-S)/(2c)] is strictly positive
and v=(R+S)/2 satisfies both fluid equations. All these statements are for
finite N; density positivity does not assert a uniform upper density bound.

The initial norms obey U0=O(N),P0=O(N4),Q0=O(N7), with fixed background
contributions. Formula (2) therefore gives T>=k0 N^-4 for sufficiently large
N with k0>0 fixed by this background/extension, not a numerical shock constant.
The high Q0 affects the magnitude of derivative bounds, not the lower-time
exponent. The argument has not imported a general PDE existence theorem.

## Uniqueness, domain independence, and stationary control

For two C1 solutions, their component difference along the first solution's
characteristics obeys D deltaU=-(lambda(U)-lambda(V)) V_x when the forces
coincide. Hence the sup norm satisfies delta(t)<=delta(0)+integral P_V delta.
Iteration of that inequality gives uniqueness for bounded-gradient solutions
on any common compact time interval, without assuming a small contraction time.
The same estimate holds on a backward characteristic cone contained in the
common initial/force region; no unknown lateral data enter if the cone sides
move inward faster than both solutions' characteristic speeds. Thus the
restriction to such a cone is independent of the chosen exterior extension.

Global invariants yield |R|,|S|<=U0+tF0, so for a fixed comparison horizon H
one can use C_N=U0+HF0+c+epsilon_v as a strict characteristic speed bound.
For times O(N^-4), C_N=O(N) and the relevant footprints have O(N^-3)
additional radius. They remain in U for all sufficiently large N. The lower
existence interval and the FGF045 upper interval can therefore be interpreted
in the original regular patch, not as an assertion about the central cusp.

The globally extended stationary pair v=0,n=rho_e solves (1). The constructed
solution agrees with it outside the forward cone of the initial compact
velocity support, by the preceding local uniqueness inequality on backward
cones. Thus any disturbance through an O(N^-4) time horizon is confined to
[x*-ell-C_Nt,x*+ell+C_Nt], which is contained in U for large N. No later
invariant support of the ORIGINAL ell interval is claimed. This also supplies
the exact hydrostatic zero-velocity control by uniqueness.

## Continuation gate and its precise consequence

A conservative sufficient continuation gate for the constructed auxiliary
C1,1 branch on [0,t*) is bounded amplitude, bounded first derivative and bounded
Lip_x U_x, with fixed g_e in C_b^{1,1}, and t* finite. Then the PDE and its
first-derivative equation bound |U_t| and |(U_x)_t| a.e.; the latter by
(speed)Q+P²+F1. The corresponding time-Lipschitz estimate gives a uniform C1
trace at t*, with the same spatial Lipschitz derivative bound. Apply (2)-(5)
to that trace to restart, and use uniqueness on overlap. This constructs an
extension; it does not assume a continuation theorem.

In this auxiliary global C1,1 class one can also DERIVE the higher-norm gate
from a uniform bound on P=||U_x||inf. Indeed differentiating the actual first-
derivative transport equation once in the a.e./difference-quotient sense used
in (4) gives

Q(t)<=Q(0)+integral_0^t [3P(u)Q(u)+F2]du.                       (6)

The coefficients are 2 lambda_x U_xx plus lambda_xx U_x; each is controlled
by P Q, with the first carrying factor two. Iteration gives
Q(t)<=[Q(0)+F2 t] exp(3 integral_0^t P(u)du). Initial C1,1 is retained on
every local construction interval; this estimate is valid throughout their
unique overlaps. The invariant source formula bounds amplitude on every finite
horizon. Therefore finite uniform first-derivative bound implies continuation
of THIS constructed global branch. This is stronger than merely postulating
its higher norm, and must be audited separately before use.

Taking the union of unique successive local intervals gives a maximal
C1-in-time/C1,1-in-space branch; the union has a well-defined finite-time
restriction because of uniqueness. FGF045 excludes its continuation through
Tupper=B L/(v0 N4) once N meets that theorem's localization thresholds.
The construction above supplies Tlower>=k0 N^-4. Consequently

k0 N^-4 <= tmax <= B L/(v0 N4).                                 (7)

If the first-derivative norm were uniformly bounded as t approaches tmax,
(6) and the restart argument would extend this branch, a contradiction.
Thus limsup_{t up to tmax} ||U_x(t)||inf=infinity for this auxiliary realization.
By finite propagation any divergence on this short horizon is in U, where
extensions coincide on their common domains. Density remains finite and
positive for each fixed N through the invariant bounds. No jump shock profile,
post-breakdown entropy solution, or unique continuation beyond tmax is inferred.
If the higher-norm propagation step (6) cannot be independently justified,
retain only the conservative three-norm continuation gate and withdraw (7)'s
first-gradient classification; the existence and conditional upper bound remain.
This last sentence is an audit instruction/limitation, not a substitute for proof.

## Energy and physical scope

The constructed C1 solution obeys H_t+Q_x=0, with
H=nv²/2+c²n[log(n/nref)-1]+n phi_e,
Q=nv[v²/2+c²log(n/nref)+phi_e]. Direct substitution cancels pressure work
and the fixed-force work with interaction transport. This is local and remains
valid for restrictions. Integrate only with actual boundary fluxes; moving
cone boundaries retain Reynolds terms. Relative to hydrostatic background,
subtract mu times mass balance. The disturbance is compact before tmax on the
short horizon, so global RELATIVE mass and energy are integrable and conserved;
no infinite background-energy integral is used. Initially relative energy is
integral rho_e v0² N² f²/2=O(N^-1). This energy conservation is now attached
to a constructed fluid solution, not just a hypothetical one.

Frozen original Q fields still have Rphi=4pi G_Newton(n-rho), Rchi=0 on U.
The auxiliary exterior is not promoted to a Q solution. Both a0=9.3619e-11 and
1.1279e-10 m/s² retain their distinct backgrounds. Constant-vacuum, frozen-H
and evolving-H branches are separate; no evolving reference or reservoir is
constructed. No transfer to RAR/M/filtered MONO, metric/photon/DOF, criterion B,
observational/source-mass inference, historical novelty or physical closure.
All norms/estimates here are analytic; zero mathematical executable runs.
