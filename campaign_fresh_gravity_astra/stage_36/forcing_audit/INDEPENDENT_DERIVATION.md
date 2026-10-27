# FGF049 independently frozen narrow evolving-force audit

Role: /root/fgf049_forcing. Scope: exact identities, sufficient force gate,
FGF048 coverage, and endpoint caveats. This is not a second existence proof.
Primary verdict: **conditional on a named input**: adverse evolving-force
control on the complete comparison cone through the compression time.

## Inputs and chronology

The FGF049 task hash matched 18f24abe89549ea2d380772afe5b6ffbce3c8ce69a9e9dd70d99afa3dccdc8fd.
All nine ancestry hashes matched. The OLD FGF045 and FGF048 derivation text
and FGF048 reconciliation were read before their hash checks; hashes then
matched before this new derivation. No new stage36 author, root, or other
reviewer proof/preview has been read before this freeze. Common framework,
result contract, campaign contract, and pinned FGF046/047 reviews were read.
All writes are confined to this review directory. No mathematical executable
computation, literature service, external theorem, or observation is used.

## Claim card and unchanged system

Fix C=4pi G, tau,sigma,J,S0,c=cs,nref,a_ref>0 independently of N, and the
same smooth hydrostatic positive-g patch K0=[x*-R,x*+R] compactly inside U.
Set ell=L/N^3, V=v0 N, omega=V/ell, and keep exactly
v(0,x)=V f((x-x*)/ell), f=(1-y^2)^2 for |y|<1 and zero otherwise.
Then d=max|f'|=8/(3sqrt(3)), Lip(f')=8; f is C1,1, not C2 at joins.
n(0)=rho, phi(0)=phi0, chi(0)=chi0, phi_t(0)=chi_t(0)=0.

On g=phi_x>0 use the actual Q inverse and scale sector:

    a=a_ref exp chi, B=(sqrt(a^2+4g^2)-a)/2,
    W_g=B, T=-W_chi, U_s=S0[cosh(2chi)-1]/4,
    n_t+(nv)_x=0,
    v_t+v v_x+c^2(log(n/nref))_x=-g,
    tau phi_tt=B_x-Cn,
    sigma chi_tt=J chi_xx+T-U_s'(chi).

Hydrostatic data obey B0_x=C rho, c^2(log rho)_x=-g0, and
J chi0_xx+T0-U_s'(chi0)=0. No frozen inversion B_x=Cn is used in evolution.
The conditional assertion below rules out a positive classical solution
covering the whole stipulated comparison cone through T_N=Btime/omega,
provided that same solution obeys the stated evolving-force gate. Without
proving that gate for all relevant branches, it is not an unconditional
upper-lifespan theorem.

## Exact weighted identities and the one-sided force

Let q=log(n/nref), r=v+cq, s=v-cq, alpha=r_x, beta=s_x,
Dplus=partial_t+(v+c)partial_x, Dminus=partial_t+(v-c)partial_x.
Then, with pressure retained,

    Dplus r=-g, Dminus s=-g,
    Dplus alpha=-(alpha+beta)alpha/2-g_x,
    Dminus beta=-(alpha+beta)beta/2-g_x,
    Dplus q=-beta, Dminus q=-alpha.

For h=n^(-1/2), y=h alpha, z=h beta these give exactly

    Dplus y=-y^2/(2h)-h g_x,
    Dminus z=-z^2/(2h)-h g_x,
    Dv h=(y+z)/4.

The C1 flow-label/Jacobian differentiation of the integrated r,s equations
justifies this without pointwise second derivatives of the C1,1 initial
profile. Only spatial differentiability of the actual g is used. The mixed
alpha beta term cancels; no g_t term appears in this spatial differentiation.
For upper positive-gradient envelopes and for w=-y on a compressive ray, the
harmful forcing is K(t)=sup_{K_t}(-g_x(t,x))_+, not the favorable positive g_x.
Using sup|g_x| is sufficient but stronger than necessary.

## An explicit sufficient evolving-force gate

Let h0=max_K0 rho^(-1/2), hmin=min_K0 rho^(-1/2),
Q0=max_K0 |log(rho/nref)|, Ginit=max_K0 |g0|, and set

    A=2d h0, b0=d hmin,
    Btime=(h0/A)[exp(8A/b0)-1],
    T_N=Btime/omega, Hstar=h0+A Btime.

Here A,b0,Hstar have inverse-square-root-density units, Btime is dimensionless.
Take omega>=Ginit/(c d), so max(0,sup y0,sup z0)<=A omega.
The characteristic starting at a_N=x*+ell/sqrt(3) has
w0=rho(a_N)^(-1/2)[d omega+g0(a_N)/c]>=b0 omega.

Assume the actual force on the comparison cone has nonnegative time majorants
F_N(t), K_N(t), with |g|<=F_N and (-g_x)_+<=K_N, such that

    I_N=integral_0^T_N F_N(u) du <= C_v V,
    Hstar integral_0^T_N K_N(u) du < A omega,
    K_N(t) Hstar^2 <= b0^2 omega^2/4 for a.e. t<=T_N.       (G)

C_v is a fixed dimensionless constant independent of N. Choose a fixed positive
velocity epsilon_v, and

    S_N=V+c Q0+I_N+c+epsilon_v+1/sqrt(tau)+sqrt(J/sigma),
    K_t=[x*-R+S_N t,x*+R-S_N t].

All terms in S_N have velocity units (B_g is dimensionless). The two extra
field speed bounds hold because 0<B_g=2g/sqrt(a^2+4g^2)<1 on g>0; scale
speed is sqrt(J/sigma). They make this cone compatible with all field and
fluid characteristic speeds while the solution stays in its positive chart.
Choose N large enough that ell+2S_N T_N<R. Since S_N=O(N), this is eventually
satisfied and the selected compressive ray stays inside K_t. The force
majorants and cone are understood as a priori conditions on this same domain;
no exterior static solution is presumed.

A first-contact speed bootstrap integrates r,s to obtain
|v|+c<=V+c Q0+I_N+c<S_N. Thus backward fluid/material rays stay in K_t and
the selected ray displaces by at most S_N T_N=O(N^-3). The upper envelope
M=max(0,sup_Kt y,sup_Kt z), H=sup_Kt h satisfies

    M(t)<=A omega+integral_0^t K_N(u)H(u) du,
    H(t)<=h0+(1/2)integral_0^t M(u) du.

The middle gate in (G) proves M<2A omega and H<=h0+A omega t<=Hstar.
Consequently density is bounded below by Hstar^(-2). Along the chosen ray,

    w'=w^2/(2h)+h g_x >= w^2/(2h)-h K_N
       >= w^2/(4h) >= w^2/[4(h0+A omega t)]

whenever w>=b0 omega, using the last gate in (G). The derivative is positive,
so the lower threshold persists. Hence

    1/w(t)<=1/(b0 omega)
             -log(1+A omega t/h0)/(4A omega).

At T_N the right side is -1/(b0 omega), impossible for a finite positive w.
This is the precise conditional O(N^-4) nonexistence-through-time statement.
For a simpler sufficient gate, a uniform bound
sup_{[0,T_N]xK_t}(-g_x)_+=o(omega^2) gives both derivative gates for large N.
An O(omega^2) bound is also enough if its coefficient is below both displayed
thresholds. Uniform O(1) evolving g_x is much stronger than required.
The two-sided bound on g is used for speed/amplitude, not the Riccati sign.

## Where the actual feedback estimate is missing

Write p=phi_t, k=chi_x, u=chi_t. Compatibility and the field equations give

    g_t=p_x,
    p_t=(B_g g_x+B_chi k-Cn)/tau,
    k_t=u_x,
    u_t=(J k_x+T-U_s')/sigma, chi_t=u.

In the weak spatial sense appropriate to C1,1 derivatives,

    g_tt=(B_xx-C n_x)/tau,
    B_xx=B_g g_xx+B_gg g_x^2+2B_gchi g_x k
             +B_chichi k^2+B_chi k_x,
    n_x=n q_x,
    (g_x)_tt=(B_xxx-C n_xx)/tau,
    n_xx=n(q_xx+q_x^2).

The last identity is distributional where third derivatives of B do not exist
classically. It is a diagnostic of the missing source control, not an extra
regularity assumption for the weighted argument. Scale feedback remains in
all B_chi derivatives and in

    u_tx=[J k_xx+T_g g_x+(T_chi-U_s'')k]/sigma.

Equivalently, in FGF048's characteristic field coordinates, differentiating
the -C exp(q)/tau source produces exactly -C exp(q) q_x/tau in both potential
modes. This term is not controlled by finite total mass or initial field jets.
As compression changes density and its derivatives, its magnitude need not
remain its initial magnitude.

FGF048 proves, only for 0<=t<=kappa/omega in physical compression units,
positive bounded density and fields, fluid first derivatives O(N^4), field
first derivatives O(1), total spatial gradient Lipschitz norm O(N^7),
q_x=O(N^3), |g-g0|=O(N^-4), and |g_x-g0_x|=O(N^-1).
These imply (G)'s force estimates on THAT short interval with far more margin
than necessary. They do not give them on [0,Btime/omega]. Its bootstrap
requires a sufficiently small kappa, and neither the N^-4 exponent nor the
vanishing initial response extends its constant to Btime. In particular the
bounds on q, n q_x, q_xx, and the coupled field derivative norms are available
only while that short-time bootstrap closes. The minimal missing implication
for this frozen route is (G) on every putative classical interval up to T_N,
with chart/domain gates if the claim is attached to a maximal coupled branch.
Failure to derive it does not exhibit a stable branch.

Preserved unsuccessful inequalities: (1) replacing kappa by Btime in
A(t)<=A0+integral[A^2+G Bf] loses the smallness required for A<=a N^4;
(2) q transport requires integral |v_x|, uncontrolled toward compression;
(3) a formal initial g_tt or p_t cancellation supplies no interval remainder;
(4) energy O(N^-1) supplies no pointwise bound on n q_x or negative g_x;
(5) B_x=Cn would delete tau phi_tt and incorrectly substitute static inversion.

## Energy and hydrostatic control

For e(n)=c^2 n[log(n/nref)-1], the full exact energy and flux are

    E=nv^2/2+e(n)+n phi
      +[tau p^2/2+W+sigma u^2/2+J k^2/2+U_s]/C,
    F=nv[v^2/2+c^2 log(n/nref)+phi]-(pB+Juk)/C.

Fluid plus interaction exchange is +np, potential-field exchange is
-np-Tu/C, and scale exchange is +Tu/C, so E_t+F_x=0. On [a(t),b(t)]

    d/dt integral_a^b E=F(a)-F(b)+b' E(b)-a' E(a).

Inward cone endpoints contribute -S_N[E(a)+E(b)]. The shrinking-cone
integral is not conserved. Initial excess is kinetic O(V^2 ell)=O(N^-1)
and gives no gradient estimate. The exact zero-velocity hydrostatic tuple
satisfies every equation, p=u=0, zero flux, alpha=-g0/c,beta=g0/c. It has
no order-omega compressive trigger and is consistent with the identities.

## Scope and obligation matrix

Passed: unchanged profile/pressure; exact moving-force weighted identities;
one-sided sufficient gate; force-dependent fluid containment and field speed
bounds; explicit reciprocal contradiction conditional on (G); full local
energy and moving boundaries; hydrostatic negative control; old input pins.
Conditional: (G) on the full upper comparison interval, actual coupled chart
margins there, and any requested maximal-branch continuation interpretation.
Not addressed: a second full construction/restart theorem or classification.

A positive-C1 branch can terminate before comparison time because a first
derivative diverges, a positive coefficient margin is lost, restart regularity
fails, or its domain no longer contains the physical footprint. The force
contradiction alone does not select which. To infer a first-gradient endpoint,
one must separately retain positive compact state margins and the buffered
physical domain, propagate the C1,1 gradient norm from bounded first gradients,
construct traces, and restart the actual coupled system. FGF046's fixed-field
classification cannot supply those coupled premises by substitution.

Run this claim separately for a0=9.3619e-11 and 1.1279e-10 m/s^2 with their
own backgrounds/constants. The adopted vacuum scale a0=kappa_vac c_light
sqrt(G rho_Lambda) is not derived; the pressure-law equality requires vacuum
p=-rho_Lambda c_light^2. Constant-vacuum and each frozen a0 E(z), with
E(z)^2=.315(1+z)^3+.685, are separate fixed-reference families. An evolving
reference adds protocol work and is outside the displayed conservation law.
No physical coefficient is retuned with N. Q is distinct from RAR, registered
M and filtered MONO. The diagnostic scale adds a degree of freedom; no physical
vacuum relation, metric/photon/two-DOF completion, criterion B, calibrated
cluster evidence, cosmology, global stability or historical novelty follows.

Proofreading self-review: notation and display consistency checked; no external
manuscript edited, no smoothing or mathematical-token repair of old sources.
Zero mathematical executable computations; administrative hashes only.
