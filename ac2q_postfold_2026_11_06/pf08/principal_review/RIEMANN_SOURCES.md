# Exact characteristic sources and conditional localized-packet formation

**Primary verdict: conditional on local classical existence and a suitable
continuation theorem for the full constrained native system.** The source,
curvature, gradient-weight and localized variation calculations below pass
independent audit. They substantially strengthen the earlier principal-only
argument. They are not a demonstrated local-wellposedness theorem and must
not be reported as unconditional full-action formation or unique singular
selection.

## 1. Exact Riemann variables with parameter A

Use the conventions of CURVED_COERCIVITY.md and restrict to a compact
on-branch neighborhood with r>0, h=H_r>0, R=H_rr>0 and c^2=h/(rR)>0.
H_r,H_rr do not depend on P: W(P) is additive. Let

    I(r,A)=integral_(rstar)^r d rho/[rho c(rho,A)],
    z_sigma=theta+sigma I, sigma=+1 or -1,

where rstar is a fixed constant and the integration path stays in the
hyperbolic neighborhood. All r derivatives here hold A fixed. Define

    J=h+P W_P/r,
    S=-(r^2 D_r u+W_P v+2B J)/R,
    u=n(A)/r, v=n(P)/r,
    K=div_2 n=e(theta)+omega(e),
    a=e(log r), D_sigma=n+sigma c e.

Then n(r)=-r c^2 K+S, n(theta)+a=-omega(n), and exactly

    D_sigma z_sigma=-omega(n)-sigma c omega(e)+F_sigma,
    F_sigma=sigma S/(r c)+sigma r I_A u+c I_A W_P/r.

This retains both n(A)=r u and e(A)=W_P/r. It is not the frozen-A
simple-wave equation. The signs follow from I_r=1/(r c); the spatial
parameter term has the same sign for both characteristic families.

On compact field/geometry sets with bounded u,v, F_sigma is bounded.
Its spatial derivative is also controlled without differentiating stress:
F_sigma depends on r,A,P,B,u,v, and the exact equations give

    e(A)=W_P/r, e(P)=D-2P E_beta,
    e(B)=(K-B)E_beta,

while e(u),e(v) are the corrected equations in CURVED_COERCIVITY.md,
including (g-2P E_beta/r)K and +(2PB/r^2)e(r). Consequently

    |e(F_sigma)| <= C(1+||u,v||_infinity)(1+|e(r)|+|K|)

under the declared compact bounds. The coefficient C does not require a
matter-stress derivative or a supremum bound on the compressive gradient.

## 2. Spin derivatives cancel in a covariant gradient

Write a_n=-a for the acceleration. The frame identities are
[n,e]=a_n n-Ke and

    d omega(n,e)=R_base/2.

For

    W_sigma=e(z_sigma)+omega(e),

direct commutation and the Cartan curvature identity give

    D_sigma W_sigma=e(F_sigma)+a_n F_sigma+R_base/2
                    -Q_sigma W_sigma,
    Q_sigma=K+sigma e(c)+sigma c a_n.

All derivatives of omega have cancelled. Indeed Q_sigma is exactly
div_2(D_sigma), so this can be written

    div_2(D_sigma W_sigma)=e(F_sigma)+a_n F_sigma+R_base/2.

There is therefore no remaining free spin-connection derivative in this
particular gradient equation. Uniform boundedness of the connection
itself is still part of the compact geometric regime.

The transverse Einstein equation and the longitudinal constraints give

    R_base/2=B^2-E_beta^2
        +(T_ee-T_nn-2T_perp)/(2M), M=Mpl^2.

This sign agrees with a homogeneous expanding flat FRW slice:
R_base/2=Hdot+H^2. Native on-branch Hilbert stress is algebraic in the
bounded frame-clock/auxiliary variables, so this curvature is bounded
without differentiating matter stress.

## 3. Direct diagonal gradients and exact quadratic coefficients

An equivalent route avoids the spin form altogether. Clock compatibility,
the commutator, and the base curvature give

    n(a)+c^2 e(K)=a(c^2-1)K-e(c^2)K+e(S)/r-2aS/r,
    n(K)+e(a)=a^2-K^2+R_base/2.

Set w_sigma=K+sigma a/c. Expansion yields exactly

    D_sigma w_sigma=-Aq w_sigma^2-Bq w_sigma w_-sigma+R_sigma,
    Aq=(1-c^2+r c c_r)/2=G/4,
    Bq=(1+c^2-r c c_r)/2,
    G=3(1-c^2)-h H_rrr/R^2.

There is no opposite-family square. The remainder can be written

    R_sigma=R_base/2+sigma e(S)/(r c)-2sigma aS/(r c)
        -2sigma c_A e(A)K
        -sigma a[c_r S+c_A n(A)]/c^2-a c_A e(A)/c.

The previously proved identities imply
|R_sigma|<=C(1+|w_plus|+|w_minus|) whenever the compact bounds and u,v
bounds hold. In particular S and e(S) obey the same bounded/linear-
gradient structure as F_sigma. This is an exact remainder statement
conditional on those bounds, not a high-frequency truncation.

Choose a positive local weight f(r,A) satisfying

    f_r/f=-Bq/(r c^2).

Since D_sigma r=-r c^2 w_-sigma+S, y_sigma=f w_sigma satisfies

    D_sigma y_sigma=-(Aq/f)y_sigma^2+remainder,
    |remainder|<=C(1+|y_plus|+|y_minus|).

The mixed quadratic term cancels exactly. The extra factor
(f_A/f)D_sigma A is bounded because D_sigma A=r u+sigma c W_P/r.
On a fixed compact hyperbolic neighborhood, f and its inverse/derivatives
are bounded. Near a D=0 state with 0<gamma r0^2<1, Aq has a uniform
positive lower bound. No formation theorem is imported in this algebra.

## 4. Localized packets and a variation bootstrap

A localized packet has amplitude delta and width epsilon on a fixed
periodic clock slice, hence gradient delta/epsilon but total variation
O(delta). This is more economical than a high-frequency wave repeated
across the whole domain. Background geometric expansion may contribute
an additional O(1) to the variation functional below; it is independent
of epsilon.

Let Z be the sum of the proper-slice L1 norms of W_plus,W_minus.
Their definitions control TV(r) and TV(theta), up to bounded connection
and e(A) terms. The curved coercive L1-to-Linfinity estimate therefore
gives

    ||u,v||_infinity<=C(1+Z).

Apply the absolute-value inequality to the conservative equation in
section 2 and integrate between clock slices phi=tau. The flux of
D_sigma through a clock slice has unit normal component. The spacetime
volume is d tau d ell/r. With r bounded away from zero,

    upper Dini derivative of Z <= C(1+Z)^2.

The source estimate uses only the linear-gradient bounds established
above. Proper slice length also stays controlled for a uniform short
time: its variation is bounded by integral |K|/r, itself controlled by Z.

Thus bounded initial Z gives a positive variation-control interval
independent of the pointwise packet compression. This removes the
previous large-global-TV bootstrap obstacle. Uniform compactness of
field values follows on a short interval from bounded characteristic
sources and bounded auxiliary temporal rates, provided the classical
equations and the geometric bounds are available.

For the metric part, in a regular conformal planar gauge the Einstein
equations have wave principal parts with algebraic matter stress and
quadratic first-metric-derivative terms. Bounded on-branch stress allows
short-time first-derivative estimates from uniformly bounded initial
metric derivatives, without a matter-gradient bound. This must be part
of the actual coupled continuation argument; it is not a replacement
for proving local existence of that constrained system.

## 5. Explicit gradient comparison

Convert the characteristic equations to clock time tau. Since
D_sigma(phi)=r, this divides their coefficients by bounded positive r.
Under the preceding compact bounds they have the form

    (partial_tau+lambda_sigma partial_x)y_sigma
        =-a_sigma y_sigma^2+R_sigma,
    0<a0<=a_sigma<=a1,
    |R_sigma|<=C(1+|y_plus|+|y_minus|).

Let q be the largest negative magnitude of either family and p the
largest positive value, taking zero if absent. The characteristic maximum
comparison gives the corresponding one-sided Dini inequalities

    q' >= a0 q^2-C(1+p+q),
    p' <= -a0 p^2+C(1+p+q).

Choose fixed L>=1 with p(0)<=Lq(0), and q(0) above a threshold depending
on L,C,a0. At p=Lq, the upper derivative of p-Lq is bounded by

    -a0(L^2+L)q^2+(1+L)C[1+(L+1)q],

which is negative above that threshold. Thus p<=Lq remains invariant,
q cannot decrease below the threshold, and

    q'>=a0 q^2/2.

An upper bound for the classical lifespan within this regime is
2/[a0 q(0)]. No ratio a1/a0 is needed for this particular positive/negative
maximum comparison: both damping of p and growth of q use the lower
bound a0. A localized packet can have q(0)~delta/epsilon and a uniformly
bounded ratio p(0)/q(0), including a symmetric packet after accounting
for the bounded weight f. Taking epsilon/delta sufficiently small makes
this time shorter than the uniform compactness/variation interval.

## 6. Constraint-compatible initial-family lemma

There is a constructive initial constraint route that does not require
small r_x. On a fixed flat proper clock slice prescribe positive
r(x) close to r0 in the supremum norm and solve

    A_x=W_P(P)/r, P_x=(rA-1-gamma r^2)/gamma.

At r0 the constant solution is A0=1/r0+gamma r0, P0=0. The linearized
periodic operator for (delta A,delta P) is invertible by the same positive-
mass/coercive argument. As a map from periodic C1 unknowns to C0
residuals with C0 parameter r, its coefficients involve r but not r_x.
The local Banach implicit-function argument therefore gives a unique
nearby C1 solution with norm O(||r-r0||_infinity), independently of the
packet slope. The native W_P is C1 at P=0, sufficient for this local
argument; it does not justify calling the resulting family C-infinity.

Concretely the constant first-order matrix is

    M0=[[0,Khold/r0],[r0/gamma,0]],

with eigenvalues +/-sqrt(Khold/gamma). The periodic operator
partial_x-M0 has a bounded L-infinity-to-W1,infinity inverse on the fixed
slice. After subtracting this linear part, the local nonlinear Lipschitz
constant tends to zero with ||r-r0||_infinity and the solution radius.
A contraction therefore yields the same width-independent small solution
bound. This supplies a direct version of the local IFT argument that
does not conceal any r_x-dependent constant.

Equivalently, with P=(W_P)^(-1)(r A_x), the stationary equation is the
Euler equation of

    integral [W*(r A_x)/r+r A^2/(2gamma)-(1/gamma+r^2)A] dx.

The linear scalar operator and forcing are

    [-(r0/Khold)partial_x^2+r0/gamma]delta A=-D_r delta r.

The sign is negative on the right. Local strict convexity/positive mass
supports uniqueness; this is not a global large-data/cap existence claim.
Small amplitude retains Q>1, the clock/cap/denominator margins and
hyperbolicity. Higher finite regularity follows only to the extent allowed
by the hold law and prescribed r.

Take beta constant, E_beta=0, and a constant nonzero transverse expansion
B. The momentum constraint e(B)=E_beta(K-B)=0 is then satisfied. With
rho=T_nn computed from the native auxiliary data, the Hamiltonian
constraint is satisfied by

    K=(rho/M-B^2)/(2B).

K stays uniformly bounded while e(log r) can be arbitrarily steep.
This provides ordinary ADM constraint data with bounded geometry. In an
initial conformal chart one may take theta=0, constant alpha,beta, and
bounded alpha_t,beta_t giving these two extrinsic curvatures. Completing
the constraints is therefore not the same as assuming bounded matter
gradients. The initial-family construction must still be placed in the
regularity class of the actual local-existence theorem.

## 7. Exact remaining conditional input

What is not proved here is local classical wellposedness and a continuation
criterion for the full native Einstein/scalar/polarization system in this
finite-regularity, elliptically constrained formulation. The needed theorem
must preserve all Einstein constraints and the auxiliary reconstruction,
and ensure continuation while the indicated domains, geometry and relevant
first derivatives remain controlled. It must be applied to the constructed
packet family rather than assumed from the frozen k-essence subsystem.

Subject to that theorem and the stated compact on-branch solution regime,
the reviewed identities give a conditional finite-gradient-breakdown
argument for sufficiently narrow admissible packets. If that existence/
continuation theorem is unavailable, the conclusion remains conditional.
Its absence is not itself evidence of illposedness, avoidance, or a
predictivity failure. Nor does conditional breakdown identify any unique
postbreak weak limit or force an added physical term.

## Audit summary

Exact characteristic sources, spin cancellation, curvature identity,
quadratic coefficients, r-dependent integrating factor, covariant variation
inequality, gradient comparison, and local small-amplitude auxiliary initial
solve pass this independent audit under their stated hypotheses. The full
local-wellposedness/continuation input and singular selection remain open.

Independent delegated analytic review, 2026-11-06. No numerical result or
external shock theorem was used as a substitute for the missing local
evolution theorem. Earlier audit files are retained as chronological records.
