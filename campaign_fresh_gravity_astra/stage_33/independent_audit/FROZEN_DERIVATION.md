# FGF046 independent pre-exposure derivation

Actor /root/fgf046_reviewer. This document was written from the task, common
contract, and pinned FGF045 ancestry only, before reading any stage33 author
or root proof. Its companion JSON records freeze time and hashes. No literature
existence theorem, numerical result, or new-author argument is used.

## Claim and exact object

On a closed initial interval J=[x*-R,x*+R] with a collar strictly inside the
regular positive-side Q neighborhood, g=phi0_x and rho>0 are smooth and
c^2(log rho)_x=-g, c=cs>0. The unchanged data are
n0=rho, v0N(x)=V f((x-x*)/ell), V=v0 N, ell=L/N^3,
f(y)=(1-y^2)^2 on |y|<1 and zero outside. f is C1,1, not C2.
In particular ||f'||=8/(3 sqrt(3)) and Lip(f')=8. Consequently the initial
velocity gradient is O(N^4) and its Lipschitz seminorm is O(N^7).
The desired classical solution satisfies both actual fluid equations with
pressure and fixed force. Define r=v+c log(n/nref), s=v-c log(n/nref),
U=(r,s), a_+(U)=(r+s)/2+c, a_-(U)=(r+s)/2-c. Then
U_{i,t}+a_i(U)U_{i,x}=-g. Conversely this diagonal system implies both fluid
equations after setting v=(r+s)/2 and n=nref exp((r-s)/(2c)).

## Auxiliary extensions, norms, and positive time

Choose a fixed smooth cutoff supported inside the regular collar and equal
to one near J. Extend q0=log(rho/nref) by multiplying this cutoff, and extend
g the same way. Extend the compact polynomial velocity by its exact zero
extension. This never smooths either polynomial join. All extensions are
bounded C1,1 on the real line, and g is bounded C2. Denote maxima over the
two components and the whole line by
A0=||U0||infinity, M1=||U0_x||infinity, M2=Lip_x(U0_x),
G0=||g||infinity, G1=||g'||infinity, G2=Lip(g').
Fix a dimensional reference time tau>0 and speed margin u*>0. Put
P=2(M1+tau G1+1/tau), K=2(M2+tau G2),
A=A0+tau G0, S=A+c+u*,
T=min(tau,1/(16P),R/(2S)).
All summands have their correct physical units: P inverse time, K inverse
length-time, and each entry of T time. T is positive for every fixed N.
The last entry merely keeps a nonempty interior cone. Extension-cutoff norms
are fixed independently of N, so P=O(N^4), S=O(N), and this particular
formula gives T bounded below by a positive fixed multiple of N^-4 for all
sufficiently large N. This is an existence-time lower bound, not a numerical
lifespan measurement. K=O(N^7) remains explicit, although T need not shrink
with K in this construction.

## Iteration and its quantitative closure

Start U^0(t,x)=U0(x). Given U^k, construct the flow of a_i(U^k) by solving
X'=a_i(U^k(t,X)). This elementary ODE is obtained on short time pieces by
successive integration: Lipschitz constant at most P gives contraction on
pieces delta with P delta<1; concatenation covers [0,T]. Bounded speed
prevents escape on the line. Differences of two trajectories and iteration
of their integral inequality give distance at most exp(P|t-s|) times their
initial distance. The same argument applied to difference quotients gives
X_a'=a_{i,x}X_a, X_a(0)=1, so X_a=exp integral a_{i,x}>0. The flow is C1,
and its derivative is Lipschitz in the spatial label when a_{i,x} is.

Define U^{k+1} along that flow by
U_i^{k+1}(t,X_i^k(t,a))=U0_i(a)-integral_0^t g(X_i^k(u,a))du.
This gives the exact initial trace and the linear equation with velocity
frozen only at the preceding iterate. It is C1 with first spatial derivative
Lipschitz; no C2 endpoint of U0 is invoked. The amplitude estimate is
||U^{k+1}(t)||<=A0+tG0<=A. Set W_i^{k+1}=partial_x U_i^{k+1}.
Differentiating the displayed flow formula proves, along the flow,
D_i^k W_i^{k+1}=-a_{i,x}(U^k)W_i^{k+1}-g'.
If ||U_x^k||<=P then
||W^{k+1}||<=exp(PT)(M1+TG1)<=exp(1/16)P/2<P.
For the spatial Lipschitz seminorm, compare this linear derivative equation
along neighboring flows and their Jacobians (or take its a.e. spatial
derivative, justified by Lipschitz functions). The resulting bound is
Lip(W^{k+1}) <= exp(2PT)[M2+T(P Lip(U_x^k)+G2)].
Indeed the differentiated equation contains 2 a_x W_x+a_xx W+g'', with
|a_x|<=P, |a_xx|<=Lip(U_x^k) a.e., and |W|<=P. No pointwise second
derivative at the polynomial joins is asserted. Since T<=tau and PT<=1/16,
this is at most exp(1/8)(K/2+K/16)<K. The seed satisfies all these bounds.
If K=0, the same recursion is exactly zero. Thus every iterate has uniform
amplitude, gradient, and gradient-Lipschitz bounds A,P,K.

For k>=1 the difference d^{k+1}=U^{k+1}-U^k obeys
D_i^k d_i^{k+1}=-(a_i(U^k)-a_i(U^{k-1}))U_{i,x}^k,
with zero initial data. Because |a_i(U)-a_i(V)|<=||U-V||max,
||d^{k+1}||infinity <= PT ||d^k||infinity <= ||d^k||infinity/16.
The first difference is bounded, so summing this geometric series proves a
uniform Cauchy limit U, without invoking a named PDE existence result.

## The classical derivative is retained

C0 convergence alone is inadequate; that would leave the task unproved.
Here K repairs the issue. For any two iterates, their difference F has
Lip(F_x)<=2K. Comparing F_x(x) with the forward quotient of step h>0 gives
|F_x(x)|<=2||F||infinity/h+K h, uniformly in t and x. Taking h to zero after
||F|| goes to zero (or optimizing h) proves uniform convergence of U_x^k.
The limit derivative is U_x by the integral formula on every spatial segment.
Moreover derivatives have a uniform space-time modulus: on a frozen flow,
|dW/dt|<=P^2+G1; tracing from (t,x) back to time s moves at most S|t-s|,
so
|W_i^k(t,x)-W_i^k(s,y)|<=K|x-y|+(KS+P^2+G1)|t-s|
for k>=1. Therefore U_x is continuous jointly in (t,x), with the stated
spatial Lipschitz bound. The equations give uniform convergence of
U_t^{k+1}=-a_i(U^k)U_{i,x}^{k+1}-g to -a_i(U)U_{i,x}-g.
The time integral identity proves this is U_t. Hence U is genuinely C1,
U_x is spatially Lipschitz, the initial traces are exact, and the diagonal
system holds pointwise. The inversion to (n,v) is C1, with strictly positive
n between nref exp(-A/c) and nref exp(A/c). Both actual equations follow
pointwise, including the pressure term c^2(log(n/nref))_x.

## Uniqueness and physical-domain independence

Two C1 diagonal solutions with bounded first spatial derivatives and the same
force obey, along the first solution's characteristics,
D_i(U_i-V_i)=-(a_i(U)-a_i(V)) V_{i,x}.
On the full line the sup difference is bounded by L integral of itself,
where L bounds the second solution's derivatives. Repeated integral
substitution gives D(t)<=Dmax (Lt)^m/m! for every m; taking m to infinity
gives uniqueness. This does not require a Lipschitz derivative on the second
solution, only C1 and bounded gradient in the comparison region.

For local independence, restrict to J_t=[x*-R+Sbar t,x*+R-Sbar t], with
Sbar larger than both solutions' speeds on the slab. Every backward
characteristic from J_t stays in J_u, as the two inward boundaries outrun
it. The same difference inequality and factorial argument on these nested
intervals gives equality. If two extensions have different global bounds,
take their common time and the larger speed; the conclusion applies on the
common cone, not automatically on a larger one. For a local competitor use
its finite compact C1 bounds and shrink the time/cone. Thus germ uniqueness
and extension independence hold before any backward path exits the regular
initial patch. No cusp, wall, or exterior physical boundary data enter.
The cone above using S from one construction is a valid constructed physical
patch; comparison with another construction is always made on a common
admissible cone.

## A sufficient continuation gate, deliberately not a classification

Let a constructed branch exist on [0,t*) times an open regular spatial
interval containing closed J1, and let J2 lie strictly inside the interior
of J1. Require t* finite, fixed smooth force on a collar, uniform bounds
0<m<=n<=M, |v|<=Vbar, |n_x|+|v_x|<=D, and
Lip_x(n_x)+Lip_x(v_x)<=H on J1 for all t<t*. These imply uniform bounds
for U,U_x,Lip(U_x) on J1. The flow argument used above gives a uniform
time-Lipschitz bound for U_x on smaller intervals as t approaches t*: trace
only time increments smaller than the spatial collar divided by a speed
bound. The PDE gives a uniform time-Lipschitz bound for U. Consequently U
and U_x have uniform limits on any intermediate closed interval J3 strictly
between J2 and J1; integrate U_x to verify the terminal trace is C1,1.
It remains positive after inversion. Extend this terminal trace by a fixed
cutoff from J3, preserving it near J2, and run the same construction with
its bounded norms. The extension is auxiliary; local uniqueness patches the
new solution to the old one on a cone from J3 and extends beyond t* near
J2. The C1 time derivative matches at t* by the PDE. This is a sufficient
interior continuation criterion, fully adequate for the exact C1,1 data.

This argument intentionally retains H. A separate estimate might propagate
H from bounded first gradients using differentiated characteristic equations,
but that implication is not needed or claimed here. Failure of this sufficient
gate does not prove gradient blowup. Nor does applying FGF045's upper-time
obstruction classify an earlier endpoint of an extension-dependent global
solution. All conclusions concern the original regular causal patch.

## Control, energy, old obstruction, and exclusions

Hydrostatic n=rho,v=0 obeys both equations since c^2(log rho)_x=-g.
For any constructed solution define e=c^2 n(log(n/nref)-1),
E=nv^2/2+e+n phi0 and F=nv[v^2/2+c^2 log(n/nref)+phi0].
The product rule for C1 functions gives
K_t+(vK)_x=-v(c^2 n)_x-nvg,
e_t+(ve)_x=-c^2n v_x,
(n phi0)_t+(nv phi0)_x=nvg,
so E_t+F_x=0. On [a(t),b(t)],
d/dt integral E dx=F(a)-F(b)+b' E(b)-a' E(a).
Thus a moving cone is not assigned conserved energy. Fixed zero-flux
boundaries give the conditional integrated conservation statement only.

FGF045 now has a nonempty constructed C1 germ to which its obstruction may
be applied whenever that germ is continued over its stipulated cone. No
positive C1 continuation covering that cone through its proved upper time
exists. This does not construct a shock or identify which local continuation
hypothesis fails first. The retained H gate is sufficient, not a necessary
and sufficient characterization.

Frozen fields retain C(n-rho), C=4pi G_Newton, as the source residual. Both
a0=9.3619e-11 and 1.1279e-10 m/s^2 are separate fixed backgrounds with their
own constants. Signed Q is unchanged. Constant-vacuum, frozen-H, and evolving-H
branches are not identified. No coupled-field existence, physical reservoir,
RAR/M/filtered-MONO, metric/photon/DOF, instrument, empirical or theory closure
follows. There were no mathematical executable runs or external sources.

## Failed or deliberately unproved routes

A mere C0 contraction cannot certify C1; the uniform K estimate and finite
quotient argument above are indispensable. The unjustified shortcut of treating
M2 as O(N^4) is rejected: its actual order is N^7. Bounded first gradients
alone are not used as the continuation gate in this frozen proof, so an
assertion of forced first-gradient blowup at a maximal endpoint remains
unproved here. Smooth replacement of f is neither used nor authorized.
