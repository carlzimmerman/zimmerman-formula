# FGF055 independent reconstruction: fast fixed fields, acoustic exterior

Reviewer `/root/fgf055_reviewer`. This proof is frozen before reading any new
FGF055 author or stage42 coordinator proof, preview, or result. All ten task
ancestry hashes were checked and matched before use. This is proof-only work;
hash/metadata operations are not mathematical experiments. No network,
literature mechanism, new calibration or physical coefficient change is used.

## Claim card and verdict

Fix positive C=4 pi G, tau,sigma,J,S0,cs,nref,a_ref and a smooth compatible
hydrostatic background H on an open interval U about x*. Fix a finite Vmax.
If Vmax>(15/2)cs, choose once

    (15/2)cs < V < Vmax,
    15/2 < B < Bcap < V/cs,
    cs < a_ext < V/Bcap.

The field speeds may be arbitrarily large but FIXED and finite. For sufficiently
small independent width epsilon, the exact C1,1 packet v=V f((x-x*)/epsilon),
f=(1-y^2)^2 on |y|<1 and zero elsewhere, with all initial density/fields equal
to H and p=w=0, has a local classical solution through kappa epsilon/V on the
contained cone specified below. No positive C1 classical solution with these
data on a neighborhood of the closed cone through B epsilon/V exists. On every
existing prefix up to the larger Bcap epsilon/V horizon, the actual field
perturbation relative to VARYING H is O(epsilon), density is positive and
uniformly bounded, and |v|<Vmax. On the exterior acoustic wedges, including
A=x*-2epsilon and D=x*+2epsilon, v and n-rho are O(epsilon^2).

This is a bounded cone-survival statement plus a legitimate local lower time,
not a claim about the old stationary-patched maximal-germ class, a classification
of its endpoint, or a global lifespan. The provisional primary verdict is
**proved as written** for this explicit conditional diagnostic cell, subject
to adversarial review. The construction input is the accepted, pinned local
characteristic start/restart construction in FGF048/FGF054; it is reused only
for each fixed datum, while all finite-V quantitative estimates are given here.

## 1. Fixed units, actual equations and compatibility

Choose L,u>0 independently of epsilon,V. Use X=(x-x*)/L, t=u t_phys/L,
n=n_phys/nref, v=v_phys/u, phi=phi_phys/u^2. Then e=epsilon/L,
V=V_phys/u, c=cs/u, and tau_hat=tau u^2, sigma_hat=sigma/u^2,
J_hat=J/u^4, C_hat=C nref L^2/u^2, a_ref_hat=a_ref L/u^2,
S0_hat=S0 L^2/u^4. Suppress hats. Fields g,p,w,k have units u^2/L,
u^3/L,u/L,1/L respectively. All constants below are fixed as e tends to zero.
They may depend on all these coefficients, V,c,Vmax, units, the background,
chart margins, B,Bcap,a_ext and field speed bounds, with no uniformity as any
fixed coefficient tends to zero/infinity or V approaches a strict gate.

Write q=log n, g=phi_X, p=phi_t, k=chi_X,w=chi_t,a=a_ref exp chi and

    Q(g,a)=(sqrt(a^2+4g^2)-a)/2,
    W(g,a)=int_0^g Q(s,a) ds, T=-W_chi,
    U(chi)=S0[cosh(2chi)-1]/4.

The FULL system is

    q_t+v q_X+v_X=0, v_t+v v_X+c^2 q_X=-g,
    g_t=p_X, tau p_t=Q_g g_X+Q_chi k-C exp(q),
    k_t=w_X, sigma w_t=J k_X+T-U', chi_t=w.            (1)

The fixed H has v=p=w=0 and

    (Q0)_X=C rho, c^2(log rho)_X=-g0,
    J chi0_XX+T0-U'(chi0)=0.                           (2)

On g>0, Q_g=2g/sqrt(a^2+4g^2)>0. Put b=sqrt(Q_g/tau),
d=sqrt(J/sigma), h_g=b with fixed positive lower integration limit, and

    r=v+cq, s=v-cq,
    R+=p+h, R-=p-h, Z+=w+d k, Z-=w-d k,
    z=(R+,R-,Z+,Z-,chi).

The invertible characteristic chart obeys EXACTLY

    D_(v+c) r=-g, D_(v-c) s=-g,
    D_-b R+=Q_chi k/tau-Cn/tau+h_chi(w-bk),
    D_+b R-=Q_chi k/tau-Cn/tau-h_chi(w+bk),
    D_-d Z+=D_+d Z-=(T-U')/sigma, chi_t=w.             (3)

Write the last five equations as D_lambda_i(z) z_i=H_i(n,z).
No density, pressure, h_chi term or scale restoring response is omitted.
The scale pair gives k_t=w_X; with chi_t=w, the constraint chi_X=k propagates.
Subtracting the R pair gives g_t=p_X; addition gives
p_t=b^2g_X+Q_chi k/tau-Cn/tau+b h_chi(chi_X-k), whose last term vanishes.
Reconstructing phi=phi0+int p dt gives phi_X=g and preserves the potential
gauge. This also holds at compatible C1 restart traces. No characteristic
speed difference occurs in a denominator.

## 2. Explicit common contained cone and whole-cone amplitude closure

Choose [-R,R] compactly in U in fixed units. On this interval bound the
background derivatives by Q1=sup|q0_X| and Z1=sup|max_i z0_i,X|.
Let z*=z0(0),q*=log rho(0). Choose a closed chart ball of radius 2zeta about
z* strictly inside g>0, with positive a and finite primitive bounds. Its smaller
radius-zeta ball is the bootstrap range. Let Gbar bound |g| on the larger ball.
Choose one constant

    S > max(Vmax+c, sup_chart b, d, 1),
    K = 3+S Bcap/V, Theta_cap=Bcap e/V,
    C_e(t)=[-K e+S t, K e-S t].                       (4)

Take e so K e<R and Theta_cap<=1. At Theta_cap this cone has radius 3e;
it contains the whole fixed interval [-2e,2e] with an e buffer. Its initial
slice covers incoming density sources and both field families, however fast
their fixed speeds are. No wall data are specified. Under the field chart
and |v|<Vmax bootstrap, every backward characteristic stays in earlier cone
sections because its absolute speed is strictly smaller than S.

The acoustic invariants centered on the CONSTANT q* have initial values in
[-c Q1 K e,V+c Q1 K e]. They give on every existing bootstrap prefix

    -D_e <= v+c(q-q*), v-c(q-q*) <= V+D_e,
    D_e=(c Q1 K+Gbar Bcap/V)e=:D0 e,
    -D_e <= v <= V+D_e,
    |q-q*| <= V/(2c)+D_e/c.                            (5)

For D_e<=c the density therefore lies in the fixed interval

    Nmin=exp(q*-V/(2c)-1) <= n <= Nmax=exp(q*+V/(2c)+1). (6)

This includes all incoming field source locations. The exponential V/c
constant is finite because V,c are fixed. It is not a gradient or variation
estimate and does not assume survival beyond the prefix in question.

Now subtract the VARYING background in the field equations, putting
u_i=z_i-z0_i(X). Since H_i(rho,z0)=lambda_i(z0)z0_i,X,

    D_lambda_i(z) u_i
      =H_i(n,z)-H_i(rho,z0)
       +[lambda_i(z0)-lambda_i(z)]z0_i,X.             (7)

Only background derivatives occur here. On a fixed larger compact neighborhood
choose Lz finite bounding the z-Lipschitz constants in (7), including Z1 times
the speed Lipschitz constant, and Ln bounding the n coefficient in H. Here
Ln may be C/tau, with an enlarged norm constant, since only the Q equations
contain n. All scale terms are in Lz. Smooth cutoffs off this neighborhood
can be used for coefficient bounds; they equal one on the actual chart.
Writing rho_max=sup_Ulocal rho, one obtains

    A_z(t):=sup_C_e(t)|z-z0|
      <= int_0^t [Lz A_z(s)+Ln(Nmax+rho_max)] ds,
    A_z(t) <= Dn t exp(Lz t), Dn=Ln(Nmax+rho_max),
    A_z(t) <= Cf e, Cf=Dn(Bcap/V)exp(Lz).              (8)

The initial relative field is exactly zero. This uses the actual complete
source, not a frozen force or a first-gradient estimate. Inverting the chart
with Lipschitz constant Lg gives |g-g0|<=Lg Cf e=:Cg e throughout the cone.
Similarly p,w and differences in k,chi are O(e). Since z0 differs from z* by
at most Z1 K e, (8) gives |z-z*|<zeta/2 when

    (Cf+Z1 K)e < zeta/2.                              (9)

Choose also D0 e<(Vmax-V)/2. Then (5) strictly improves the speed bootstrap.
Initially both bootstrap inequalities are strict for small e. A first-exit
argument on any existing compact prefix proves (5)-(9) throughout that prefix.
This removes any circular use of S or of the density source bound. Constants
never use the unknown solution's gradients near a possible endpoint.

## 3. Exterior acoustic wedges with permitted field arrivals

Let eta=a_ext-c>0 and define

    E_+(t)=C_e(t) intersect {X>=e+a_ext t},
    E_-(t)=C_e(t) intersect {X<=-e-a_ext t}.           (10)

The intervals are nonempty: at Theta_cap the inner endpoint is less than 2e
in magnitude, whereas the outer endpoint is 3e. At t=0 they are entirely
outside the packet. Set the VARYING-background acoustic differences

    Rf=v+c(q-q0(X)), Sf=v-c(q-q0(X)).

Using (2) gives, including the advective derivative of q0,

    D_(v+c) Rf=-(g-g0)+(g0/c)v,
    D_(v-c) Sf=-(g-g0)-(g0/c)v.                       (11)

On the wedges bootstrap |v|<eta/2. Their inner moving boundaries have speeds
+a_ext and -a_ext. On the right, v +/- c<a_ext; a backward acoustic path
therefore cannot leave through the inner boundary. On the left, v +/- c>
-a_ext gives the analogous fact. Outer containment follows from S. Thus
both invariant paths start on the initial outside-packet data Rf=Sf=0.
Taking L0=sup|g0|/c, (8) and (11) imply

    A_f(t)=sup_(E_+ union E_-) max(|Rf|,|Sf|)
      <= int_0^t[Cg e+L0 A_f(s)]ds,
    A_f(t)<=Cg e t exp(L0 t)<=Ca e^2,
    Ca=Cg(Bcap/V)exp(L0).                             (12)

Since |v|<=A_f, choosing Ca e^2<eta/4 strictly improves the exterior bootstrap.
Moving-domain first exit is legitimate: points entering a wedge through its
moving outer edge are not needed, since that edge recedes faster than every
acoustic characteristic; each backward path has already stayed in earlier
sections. The inner edge also has strict characteristic separation. No fluid
wall or global derivative control is assumed. In particular

    |v|<=Ca e^2,
    |q-q0|<=Ca e^2/c,
    |n-rho|<=Cn e^2, Cn=rho_max exp(1)Ca/c             (13)

when Ca e^2/c<=1. The fixed A=-2e,D=2e lie strictly in these wedges through
Theta_cap because a_ext Bcap/V<1. Fields there need not be stationary; their
actual perturbations can be O(e), with nonzero p,w and flux. This is precisely
the distinction from FGF054's exact full-field collars.

## 4. Exact variable mass, pressure, momentum and capacity

On [A,D], let ell=D-A=4e, j=nv, M=int n, P=int nv and I=int(X-A)n.
Direct integration, retaining both endpoint terms, gives

    M'=j(A)-j(D),
    P'=-[nv^2+c^2 n]_A^D-int ng,
    I'=P-ell j(D).                                   (14)

Hydrostatics gives c^2[rho]_A^D=-int rho g0. Hence with

    Rm=[nv^2+c^2(n-rho)]_A^D+int(ng-rho g0),

one has P'=-Rm. The positive capacity Delta=ell M-I=int(D-X)n satisfies
Delta'=ell j(A)-P, and therefore EXACTLY

    Delta(T)=Delta0-P0 T+int_0^T(T-t)Rm(t)dt
                            +ell int_0^T j(A,t)dt.   (15)

The plus sign in the left mass influx term is essential. M is not conserved.
Let Jb=Nmax Ca. By (6),(13), |j(A)|,|j(D)|<=Jb e^2, and

    |M(t)-M0|<=2 Jb e^2 t,
    |[nv^2+c^2(n-rho)]|<=2Nmax Ca^2 e^4+2c^2 Cn e^2,
    |int(ng-rho g0)|<=4e(Nmax Gbar+rho_max G0),        (16)

where G0=sup|g0|. Thus |Rm|<=Cr e for e<=1, with one fixed finite Cr.
Consequently the weighted Rm integral is at most Cr e T^2/2=O(e^3),
and the last term of (15) has absolute value at most 4 Jb e^3 T=O(e^4).
These are strictly smaller than the O(e^2) initial moment margin. No sign of
field transfer or pressure error has been assumed, and n-rho need not be
small in the interior.

With rho*=rho(0)>0, exact integration int_-1^1 f=16/15 and smooth background
Taylor bounds yield

    Delta0=8rho* e^2+O(e^3),
    P0=(16/15)rho* V e+O(V e^2).

At Theta=B e/V, (15)-(16) give

    Delta(Theta)/e^2
      =rho*[8-(16/15)B]+O(e).                         (17)

All constants are independent of e. Since B>15/2, the leading term is negative;
for small e this contradicts Delta(Theta)>0. This excludes a positive classical
solution through the closed cone horizon. Equality or low-Mach cells are not
decided. The sufficient cell is Vmax>(15/2)c, with no field-speed-to-V gate.
The field speeds enter K,chart/source constants and the admissible e threshold.

## 5. Full field momentum and energy on nonstationary boundaries

Define

    mf=-(tau p g+sigma w k)/C,
    Sf=[gQ-W+tau p^2/2+sigma w^2/2+Jk^2/2-U]/C.

Direct differentiation of (1) gives

    (nv)_t+(nv^2+c^2n)_X=-ng,
    (mf)_t+(Sf)_X=ng.                                (18)

For example (gQ-W)_X=g Q_X+T k, cancelling the scale source in mf_t.
Writing Fm=int mf and dSf=Sf-Sf0, the varying-boundary-trace laws are

    Fm'=int(ng-rho g0)-[dSf]_A^D,
    (P+Fm)'=-[nv^2+c^2(n-rho)+dSf]_A^D.             (19)

Here Sf0_X=rho g0, c^2rho+Sf0 is constant, and Fm(0)=0. Equations (19)
retain the field momentum boundary stress. In particular P+Fm is generally
NOT constant and Fm' is not just the bulk transfer used in FGF054. From (8),
|mf|,|dSf|=O(e), so Fm=O(e^2); each term in (19) is controlled, but no
cancellation of the endpoint field stress is imposed or needed for (15).

With e_int=c^2n(log n-1), the full autonomous energy and flux are

    E=nv^2/2+e_int+n phi
       +[tau p^2/2+W+sigma w^2/2+Jk^2/2+U]/C,
    F=nv[v^2/2+c^2 log n+phi]-(pQ+Jwk)/C.            (20)

Matter plus interaction has exchange +np, Q gives -np-Tw/C, scale gives
+Tw/C; hence E_t+F_X=0. At A,D, j=O(e^2), bounded q,phi and O(e)
field p,w give F=O(e), generally nonzero. Thus

    d_t int_A^D E=F(A)-F(D),

with BOTH field fluxes included. For moving endpoints alpha,beta any balance
h_t+f_X=s gives

    d_t int_alpha^beta h=int s+f(alpha)-f(beta)
                         +beta' h(beta)-alpha' h(alpha). (21)

In particular the cone integral of E has the additional term
-S[E(beta)+E(alpha)] and is not called conserved. No energy coercivity or
unsigned interaction-energy assumption is used in the amplitude or capacity
argument. phi-phi0=int p dt=O(e^2) on the vertical segments of this cone.

## 6. Lower construction and restart on the SAME cone

We do not use or redefine FGF054's exact-H exterior maximal class. For a local
start, take one compatible smooth bounded extension of H from a fixed patch
containing [-R,R] to the auxiliary line, with g0 bounded below, k0=chi0_X,
and phi0 a compatible antiderivative. No auxiliary exterior hydrostatics is
asserted. The velocity is exactly V f(X/e), including its unsmoothed joins:
||f'||=8/(3sqrt(3)), Lip(f')=8. For each fixed e the pinned characteristic
construction freezes speeds/sources, integrates, contracts in C0, and uses
uniform Lipschitz gradients plus interpolation to pass to a C1 solution.
Compatibility follows from Section 1. This is the only inherited local input.

Fresh fixed-V lower-time estimates are as follows. Set Pscale=V/e>=1.
On a fixed extended background chart and q in [q_- -1,q_+ +1], bound field
speed/source and derivatives by Lambda,F,G,G2,L1,L2,P1,P2 as in pinned
FGF048, with all scale and exp(q) contributions retained. Put

    A=max(||r_X||,||s_X||), Bf=max_i||z_i,X||,
    a0=8/(3sqrt(3))+c||q0_X||, a1=2(a0+1),
    beta=2(Bf(0)+1+P1 a1/c).

The exact differentiated equations imply

    A<=a0 Pscale+int(A^2+G Bf),
    Bf<=Bf(0)+int[L1 Bf^2+P1(Bf+A/c)],
    D_v q=-v_X, ||z(t)-z0||<=int(Lambda Bf+F).         (22)

A fixed sufficiently small kappa>0, chosen below B, strictly closes
A<a1 Pscale,Bf<beta, |q-q0 along material paths|<1/2 and a half-chart
state margin for t<=kappa/Pscale. For explicit positive choices require

    kappa <= min(1,1/(2a1),
      (a1-a0)/(2(a1^2+G beta+1)),
      (beta-Bf(0))/(2(L1 beta^2+P1 beta+P1 a1/c+1)),
      zeta_lo/(2(Lambda beta+F+1)), B/2).

Here zeta_lo is a fixed lower-construction chart displacement margin. All
constants may depend on V but not e. Actual speeds on this short interval
are bounded by a fixed Slo using the acoustic invariants and chart. Choose
e so Slo kappa e/V<R/4 and K e<R/2; the local construction's physical fixed
cone then includes every C_e(t) for t<=kappa e/V.

For exact join regularity, the difference-quotient equations give

    Hf<=Hf(0)+int[3A Hf+G Hz+G2 Bf^2],
    Hz<=Hz(0)+int[(3L1 Bf+P1)Hz+(P1/c)Hf
                            +L2 Bf^3+P2(Bf+A/c)^2]. (23)

Here Hf=max(Lip r_X,Lip s_X), Hz=max_i Lip z_i,X. The joins contribute
8V/e^2=(8/V)Pscale^2, so Hf(0)+Hz(0)<=h0 Pscale^2 for fixed h0.
Equations (22)-(23) yield Hf+Hz<=Clo Pscale^2 through kappa/Pscale.
For each fixed e, this is finite. The PDE and its weak spatial derivative
bound U_t and (U_X)_t, producing uniform C1 endpoint traces retaining the
C1,1 seminorm and strict states. Restart the exact trace by the pinned local
iteration; the compatibility constraints and potential antiderivative pass
to the trace, and uniqueness identifies overlaps. No exact-H patching is
used anywhere. This proves existence through the stated lower time.

For later traces, if a positive classical branch on a neighborhood of a compact
part of the cone has compatible C1,1 trace and finite chart margins, the same
local restart works after compatible extension of that trace on a slightly
larger interval; retain the existing phi,chi there, set k=chi_X, and extend
g positively with its antiderivative matching phi on the inner interval.
There is no condition of matching phi0 at either exterior end. This observation
asserts only local restart under its trace hypotheses, not that gradients or
C1,1 norms stay bounded near the upper-survival obstruction. Common-cone
uniqueness follows by subtracting the diagonal equations along one solution's
actual paths with finite gradient coefficients on each existing compact slab.
This connects the lower branch to any candidate continuation on this SAME
cone without importing the old stationary maximal class.

## 7. Controls, evidence and limitations

At V=0, do not use formulas dividing by V. H itself solves the complete
system, Rf=Sf=0, p=w=v=0, F=0, and all balances reduce to their stationary
values. There is no positive initial momentum and no capacity contradiction.
The fixed C1,1 joins, positive n and positive g chart, full scale and pressure
terms, and evolved |v|<Vmax are preserved where claimed.

Restore physical time as t_phys=(L/u)t: the two horizons are
kappa epsilon/V_phys and B epsilon/V_phys. Treat both a_ref=9.3619e-11 and
1.1279e-10 m/s^2 separately with compatible backgrounds and constants.
The adopted reference vacuum relation a_ref=kappa_vac c_light sqrt(G rho_Lambda)
is not derived. Constant vacuum and each individually frozen a0 E(z), with
E(z)^2=.315(1+z)^3+.685, are distinct autonomous choices; an evolving reference
is excluded. Diagnostic chi dynamics does not establish pointwise physical
vacuum closure. Q, RAR, registered M and operative filtered MONO remain distinct;
the nonlinear Q/MOND source relation (1), not Newtonian missing mass, is retained.
No physical metric/photon/two-DOF, criterion B, cluster, cosmology, calibration,
novelty, component divergence, weak continuation, or sharp-threshold conclusion.

Dependency graph: pinned equations/chart and local start/restart construction
-> fresh fixed-V lower bound; whole-cone acoustic amplitudes -> bounded actual
density source -> varying-background O(e) fields -> exterior acoustic O(e^2)
traces -> exact variable-mass/pressure balances -> negative capacity at B>15/2.
The wider cone is essential; estimates solely on the mass interval would
silently miss incoming density sources. No external theorem leaf is invoked.

Obligation matrix: exact equations/compatibility, full cone containment, field
source bound, exterior characteristic closure, flux signs, positive moment
margin, same-domain lower construction, exact joins, density/chart/speed margins,
energy and V=0 are passed in this derivation. A new intrinsic maximal-domain
and endpoint theorem is not addressed and not needed for this bounded claim.
Physical realization is out of scope. No numerical experiment was performed.

The cheapest next check is an adversarial comparison of frozen independent,
author and coordinator proofs, particularly the moving exterior first-exit
geometry and the absence of unknown first-gradient assumptions in (7)-(12).
