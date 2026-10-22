# FGF055: fluid boundary control despite fast Q and scale arrivals

Author /root/fgf055_author, run fgf055_run_001. Proof-only author candidate;
not independently accepted evidence. All ten task ancestry pins matched before
source use. No stage42 root/reviewer files, external literature, services,
numerical experiments, parameter fitting, or additional agents were used.

## 1. Claim card and domain

Fix positive physical C=4 pi G, tau,sigma,J,S0,cs,nref,a_ref, a smooth compatible
hydrostatic background H about x*, and a finite matter ceiling Vmax. Suppose

    Vmax > (15/2) cs.

Choose once, independently of epsilon,

    (15/2)cs < V < Vmax,
    15/2 < B < Bcap < V/cs.

No restriction compares either field speed to V. For every such fixed tuple
there are epsilon0>0, kappa>0 and a finite cone speed S such that for every
0<epsilon<epsilon0 the exact initial data

    v=V f((x-x*)/epsilon), f(y)=(1-y^2)^2 on |y|<1, zero otherwise,
    n=rho, phi=phi0, chi=chi0, p=phi_t=0, w=chi_t=0

have a positive compatible C1/C1,1 local solution through kappa epsilon/V
on the explicitly contained cone defined below. But no positive compatible
classical solution with these initial data on that SAME cone survives through
B epsilon/V. On every existing prefix below Bcap epsilon/V, the actual
solution on the cone has uniform positive density and field margins,
|v|<=V+O(epsilon)<Vmax, g-g0=O(epsilon), and at x* +/-2epsilon,
v=O(epsilon^2), n-rho=O(epsilon^2). All constants may depend on the FIXED
coefficients, background, V/cs, Vmax-V, and strict time margins. Uniformity is
only in epsilon. Fast field propagation enlarges the cone and worsens constants;
it does not impose a field-speed ceiling relative to V.

Regularity means the seven first-order state variables are spacetime C1,
with spatial gradients locally uniformly Lipschitz on compact time prefixes;
potentials are C2. The upper a priori argument needs only positive C1 states
on a neighborhood of each closed cone prefix. This is a bounded existence/
non-survival implication, not an identified maximal-domain germ, a divergence
classification, weak evolution, or an authenticated physical parameter tuple.

## 2. Fixed units, complete source, chart, compatibility

Choose L,u>0 independently of epsilon,V. Let X=(x-x*)/L, t=u t_phys/L,
e=epsilon/L, V=V_phys/u, c=cs/u, n=n_phys/nref, v=v_phys/u,
phi=phi_phys/u^2. Units of g,p,w,k are u^2/L,u^3/L,u/L,1/L.
Coefficients become tau_hat=tau u^2, sigma_hat=sigma/u^2,
J_hat=J/u^4, C_hat=C nref L^2/u^2, a_ref_hat=a_ref L/u^2,
S0_hat=S0 L^2/u^4. Suppress hats in Sections 2--8; Vmax and speeds are
also divided by u. All are fixed as e decreases.

Set q=log n, g=phi_X, p=phi_t, k=chi_X, w=chi_t, a=a_ref exp chi,

    A(g,chi)=(sqrt(a^2+4g^2)-a)/2,
    W(g,chi)=integral_0^g A(s,chi) ds,
    Tscale=-W_chi, U(chi)=S0[cosh(2chi)-1]/4.

The unchanged equations are

    q_t+v q_X+v_X=0,          v_t+v v_X+c^2 q_X=-g,
    g_t=p_X,                 tau p_t=A_X-C exp q,
    k_t=w_X,                 sigma w_t=J k_X+Tscale-U',
    chi_t=w.                                                   (2.1)

The background satisfies, writing q0=log rho,

    A0_X=C rho, c^2 q0_X=-g0,
    J chi0_XX+Tscale(g0,chi0)-U'(chi0)=0, v0=p0=w0=0. (2.2)

On g>0, A_g=2g/sqrt(a^2+4g^2)>0. Define b=sqrt(A_g/tau),
d=sqrt(J/sigma), h(g,chi)=integral_gstar^g b(s,chi) ds, gstar>0 fixed,

    r=v+cq, s=v-cq,
    R+=p+h, R-=p-h, Z+=w+d k, Z-=w-d k,
    z=(R+,R-,Z+,Z-,chi).

This is a smooth invertible chart. With As=A_chi k/tau-C exp(q)/tau,
Ds=(Tscale-U')/sigma, the exact diagonal equations are

    D_(v+c) r=-g, D_(v-c) s=-g,
    D_-b R+=As+h_chi(w-bk),
    D_+b R-=As-h_chi(w+bk),
    D_-d Z+=Ds, D_+d Z-=Ds, chi_t=w.                    (2.3)

Write the field part z_i,t+lambda_i(z)z_i,X=H_i(q,z). It includes the actual
incoming density source, both h_chi terms, scale response and restoring force.
It contains neither fluid velocity nor any state derivative in H. Coincident
speeds cause no division or chart singularity. The Z equations propagate
chi_X=k; the R difference then gives g_t=p_X, and their sum gives
p_t=b^2 g_X+As+b h_chi(chi_X-k). Thus reconstructing phi=phi0+integral p dt
preserves phi_X=g and the original dynamic source A_X=Cn+tau phi_tt.
Compatibility also passes to the lower construction's exact C1 traces.

## 3. Wide actual cone and uniform amplitude bootstrap

Choose a fixed compact background interval [-R,R] in the original patch,
center z*=z0(0), q*=q0(0), and a convex chart ball |z-z*|<=2zeta lying
strictly in g>0. Shrink R so the background lies in its inner part. On this
ball let Gbar bound |g| and Lg bound the inverse chart derivative of g.
Let Kq,Kz bound |q0_X|,|z0_X| on [-R,R]. Norms below are max norms and
operator bounds include component sums.

Choose S strictly greater than Vmax+c, tau^(-1/2), d and the finite lower-
construction speed Slo from Section 7. The global inequality 0<A_g<1 on
g>0 ensures b<tau^(-1/2); there is no assumption S<V. Put

    Hrad=3+S Bcap/V,
    Theta=B e/V, Theta_cap=Bcap e/V,
    K_e(t)=[-Hrad e+S t, Hrad e-S t].                  (3.1)

For t<=Theta_cap it contains [-3e,3e]. Require Hrad e<R. Every backward
field, fluid, material, and zero-speed path stays in earlier sections of this
cone as long as the actual speeds are below S. All initial footprints lie in
the original background patch, however large but fixed S is. The entire
initial packet is included, with room for incoming density/field responses.

On any existing solution prefix bootstrap |z-z*|<zeta, |v|<Vmax. These
hold strictly initially for small e. Under them the path containment is
valid. Integrating centered acoustic invariants r-cq*,s+cq* along their
ACTUAL paths to t=0 gives

    -E e <= r-cq*, s+cq* <= V+E e,
    -E e <= v <= V+E e,
    |q-q*| <= V/(2c)+E e/c,
    E=c Kq Hrad+Gbar Bcap/V.                           (3.2)

No boundary values enter: all paths reach the original initial slice. For
E e<=c and Kq Hrad e<=1, this gives

    n_- = exp(q*-V/(2c)-1) <= n <= exp(q*+V/(2c)+1)=n_+,
    |q-q0(X)| <= Q:=V/(2c)+2.                          (3.3)

Thus the full density source is bounded uniformly in e even if gradients
become large. The initial spatial variation contributes O(e), since the
cone width is Hrad e, not a fixed order-one width.

For the varying background, set dz=z-z0(X), dq=q-q0(X). Subtract the exact
stationary field equations along the ACTUAL field characteristics:

    D_lambda_i(z) dz_i
      =H_i(q,z)-H_i(q0,z0)
                       -[lambda_i(z)-lambda_i(z0)] z0_i,X.   (3.4)

Only the KNOWN background derivative occurs. Let K>=1 bound the Lipschitz
constant of H in (q,z), plus Kz times the Lipschitz constant of lambda, on
the compact q interval in (3.3), its background range, and the chart ball.
The segment between q and q0 lies in a fixed compact interval; all exp(q),
scale and chart terms are included. Initial dz=0 exactly. Containment and
(3.4) imply, with Z(t)=sup_{K_e(t)}|dz|,

    Z(t)<=K integral_0^t[Q+Z(s)]ds
         <=K Q t exp(Kt)<=Af t, Af=K Q exp(K), t<=1.    (3.5)

In particular

    |g-g0|<=Cg t, Cg=Lg Af,
    |z-z*|<=Kz Hrad e+Af Bcap e/V.                     (3.6)

Take e so Theta_cap<=1, (3.6)<zeta/2 and E e<(Vmax-V)/2. Then both
bootstraps improve strictly, giving (3.2)--(3.6) on every existing prefix
below Theta_cap by first exit. Constants use no actual solution gradient,
variation norm, crossing count, or endpoint regularity. In particular the
bound survives arbitrarily close to any earlier classical endpoint.
The scale chart gives positive finite a and g margins and p,w=O(e);
chi-chi0,k-k0=O(e) too. It is an actual response, not a frozen force.

## 4. Exterior fluid wedges permit field arrivals

Choose eta>0 with c+eta<V/Bcap, and put h_a=c+eta. For example
eta=(V/Bcap-c)/2 works. Inside K_e define the right and left exterior wedges

    E_R(t)=K_e(t) intersect [e+h_a t,infinity),
    E_L(t)=K_e(t) intersect (-infinity,-e-h_a t].       (4.1)

These have nonempty interiors through Theta_cap. The fixed endpoints
A=-2e,D=2e remain inside them with distance at least
[1-h_a Bcap/V]e from their inner edges and at least e from K_e's outer
edges. These margins are strictly positive. Fields cross the inner edges
freely; they are NOT stationary comparison cones for the full system.

Use spatially centered fluid invariants

    u+=v+c(q-q0(X)), u-=v-c(q-q0(X)).

The exact equations, including the advective background derivatives, are

    D_(v+c) u+=-(g-g0)-c v q0_X,
    D_(v-c) u-=-(g-g0)+c v q0_X.                       (4.2)

Initially u+=u-=0 throughout both wedges, including the exact packet joins.
Bootstrap max(|u+|,|u-|)<eta/2 on their union. Then |v|<eta/2, so both
acoustic speeds have magnitude <c+eta/2<h_a. At the right inner edge they
are strictly slower than the edge's rightward speed h_a; backward paths
move into the exterior wedge. At the left inner edge the reversed inequality
has the same effect. At outer edges they remain contained by S. Therefore
every backward acoustic path reaches the initial exterior, without any
assumed trace on a wall or the moving inner boundary.

Let Uext(t) be the supremum of these two deviations on both wedges and
Kext=c Kq. From (3.6),(4.2),

    Uext(t)<=integral_0^t[Cg s+Kext Uext(s)]ds
             <=(Cg/2)t^2 exp(Kext t).                 (4.3)

Choose e so this is <eta/4 through Theta_cap and also <=c. The first-exit
argument closes the exterior speed bootstrap. In particular on both wedges,

    |v|<=Cv e^2,
    |q-q0|<=Cv e^2/c,
    |n-rho|<=Cn e^2,
    |j|=|nv|<=n_+ Cv e^2,                              (4.4)

where Cv=(Cg/2)(Bcap/V)^2 exp(Kext),
Cn=rhobar exp(1) Cv/c, and rhobar bounds rho on [-R,R]. The field time
bound is evaluated on the full wide cone; no assumption suppresses fast
incoming field signals. A large Cg merely lowers epsilon0. Formula (4.2)
shows why centering on a constant density or dropping v q0_X would be wrong.

## 5. Exact capacity identity with every boundary contribution

Use [F]_A^D=F(D)-F(A), j=nv, ell=D-A=4e,
M=int_A^D n, P=int_A^D nv, I=int_A^D(X-A)n. Direct integration gives

    M'=j(A)-j(D),
    P'=-[nv^2+c^2 n]_A^D-int_A^D ng,
    I'=P-ell j(D).                                    (5.1)

For example integration by parts of -(X-A)j_X gives -ell j(D)+int j;
the left endpoint term vanishes because its weight is zero. Hydrostatics
gives c^2[rho]_A^D=-int rho g0. Hence, EXACTLY,

    P'=-R(t),
    R=[nv^2+c^2(n-rho)]_A^D+int_A^D(ng-rho g0).

Define Delta=ell M-I=int_A^D(D-X)n>0. Equations (5.1) yield
Delta'=ell j(A)-P, and double integration gives

    Delta(T)=Delta0-P0 T+int_0^T(T-t)R(t)dt
                                      +ell int_0^T j(A,t)dt. (5.2)

In particular M is not treated as constant, and pressure is not discarded.
The appearance of j(A), not j(D), is checked independently by differentiating
the alternate expression int(D-X)n directly.

Let G0 bound |g0| on the fixed patch. The uniform density/field bounds and
(4.4) imply, at all existing times below Theta_cap,

    |int(ng-rho g0)|<=Qb e, Qb=4(n_+ Gbar+rhobar G0),
    |c^2[n-rho]_A^D|<=Qp e^2, Qp=2c^2 Cn,
    |[nv^2]_A^D|<=Qk e^4, Qk=2n_+ Cv^2.               (5.3)

These are estimates on the actual density; no smallness of n-rho in the
core is assumed. One may split ng-rho g0 into (n-rho)g0+n(g-g0), but the
coarse bound suffices. The four absolute remainder contributions to (5.2),
at T=Theta, are respectively bounded by

    Qb B^2 e^3/(2V^2),
    Qp B^2 e^4/(2V^2),
    Qk B^2 e^6/(2V^2),
    4n_+ Cv B e^4/V.                                  (5.4)

Also |M(t)-M(0)|<=2n_+ Cv e^2 t=O(e^3), as a consequence rather than a
conservation assumption. All signs in (5.2) allow either flux direction.

The exact profile integral is int_-1^1 f=16/15. If Lrho bounds |rho_X|,

    |P0-(16/15)rho* V e|<=(16/15)Lrho V e^2,
    |Delta0-8rho* e^2|<=16Lrho e^3, rho*=rho(0)>0.

Consequently, for e<=1, (5.2)--(5.4) imply

    Delta(Theta)<=-mu e^2+Ccap e^3,
    mu=rho*[(16/15)B-8]>0,
    Ccap=[16+(16/15)B]Lrho
          +(Qb+Qp+Qk)B^2/(2V^2)+4n_+ Cv B/V.          (5.5)

Take e<mu/[2(Ccap+1)]. Then Delta(Theta)<0, contradicting strictly positive
density. Therefore no positive classical solution on the contained cone can
survive through Theta. The bound is not conditioned on a field speed<V;
only the acoustic wedge inequality Bcap<V/c is used. Failure of this
sufficient acoustic cell does not prove a PDE counterexample or sharpness.

## 6. Field momentum and full nonstationary energy fluxes

Define field momentum and stress

    mf=-(tau p g+sigma w k)/C,
    Sf=[gA-W+tau p^2/2+sigma w^2/2+J k^2/2-U]/C.

Direct differentiation using ALL of (2.1) gives

    (nv)_t+(nv^2+c^2 n)_X=-ng,
    (mf)_t+(Sf)_X=ng.                                  (6.1)

For the sign check, (gA-W)_X=g A_X+Tscale k. This cancels the scale
Tscale k term in the time derivative of mf. Let Fm=int_A^D mf. Then

    Fm'=-[Sf]_A^D+int_A^D ng,
    (P+Fm)'=-[nv^2+c^2n+Sf]_A^D.                       (6.2)

The hydrostatic total stress c^2 rho+Sf0 is constant, since
Sf0_X=rho g0. Thus (6.2) can equally be written

    Fm'=-[Sf-Sf0]+int(ng-rho g0),
    (P+Fm)'=-[nv^2+c^2(n-rho)+(Sf-Sf0)].               (6.3)

Neither [Sf-Sf0] nor Fm is set to zero. By the smooth chart, throughout I
(and hence at A,D) one has Sf-Sf0=O(e), mf=O(e), whereas nv^2=O(e^4) and c^2(n-rho)=O(e^2).
Thus Fm=O(e^2), and time-integrated field stress may be O(e^2). The weaker
absolute O(e) stress bound cannot be mistaken for a stationary exterior.
It is fully retained by (6.3), and the capacity proof uses the equivalent
fluid equation (5.1), avoiding any unsupported separate cancellation estimate.

Let eint=c^2 n(log n-1). With the actual potential gauge reconstructed above,

    Etotal=nv^2/2+eint+n phi
         +[tau p^2/2+W+sigma w^2/2+J k^2/2+U]/C,
    FE=nv[v^2/2+c^2 log n+phi]-(p A+J w k)/C.          (6.4)

Kinetic plus internal energy has source -nvg. Adding n phi changes that to
+np. The Q energy has source -np-Tscale w/C and flux -pA/C; the scale energy
has source +Tscale w/C and flux -Jwk/C. Consequently

    (Etotal)_t+(FE)_X=0,
    d/dt int_A^D Etotal=FE(A)-FE(D).                   (6.5)

Both field fluxes are generally nonzero here. At A,D p,w=O(e), phi-phi0=O(e^2)
from vertical reconstruction, so FE=O(e) while the matter flux is O(e^2).
No endpoint energy flux is deleted and no coercivity is used. For ANY moving
contained endpoints alpha,beta and any h_t+Jflux_X=s the exact rule is

    d/dt int_alpha^beta h=int s+Jflux(alpha)-Jflux(beta)
                               +beta' h(beta)-alpha' h(alpha). (6.6)

This applies to mass, fluid momentum, field momentum, total momentum and
energy. On K_e the last terms are -S[h(beta)+h(alpha)]. We never call an
integral on that shrinking cone conserved or omit its advective terms.

## 7. Fresh lower construction on this same cone

The source-pinned local iteration is FGF051 Section 4 (hash in input pins).
Its construction, not its old N-dependent horizon or old stationary gluing,
is reused as follows. Extend q0,chi0 smoothly outside a fixed interval to
bounded functions, g0 to a bounded positive function, k0=chi0_X, and phi0
as an antiderivative. On the fixed patch these are exactly H. Keep the exact
velocity V f(X/e), including both original joins. Only auxiliary data outside
the fixed patch change. Cut off the state coefficients outside a larger
compact range to make their C2 bounds finite; prove below that cutoffs remain
inactive. All extension and coefficient constants are fixed in e.

For each fixed e, set Ustate=(r,s,z). The iteration freezes speeds/sources
at Ustate^j and integrates the linear equations along their characteristics.
With initial gradient K0 and gradient-Lipschitz seminorm H0 finite, a short
positive time preserves doubled bounds K,H and amplitudes: the next gradient
is bounded by (K0+C K t)exp(C K t), and the next seminorm by
[H0+C t(H K+K^3+H+K^2)]exp(2C K t). The difference of successive iterates
is <=C t(1+K) times the previous sup difference, chosen <1/2. Uniform C0
convergence plus |du-dv|<=2||u-v||/h+Hh gives C1 convergence. This proves
an exact C1,1 start without smoothing joins or merely citing hyperbolicity.
The same construction starts any compatible endpoint trace inside the chart.

Here are fresh fixed-V quantitative continuation estimates. Write Pscale=V/e
and require Pscale>=1. Use compact coefficient bounds Lambda,F,G,G2,L1,L2,
P1,P2 for field speeds/sources, first/second derivatives of g,lambda,H,
including exp(q) and all scale terms. Let B0=max||z0_X||, q_-,q_+ initial
extrema, and a fixed positive displacement margin zeta0. Define

    a0=8/(3sqrt(3))+c||q0_X||, a1=2(a0+1),
    beta=2(B0+1+P1 a1/c),
    Agrad=max(||r_X||,||s_X||), Bgrad=max_i||z_i,X||.

The initial inequalities are Agrad(0)<=a0 Pscale, Bgrad(0)=B0. Differentiating
(2.3) on its actual characteristics and using exact material transport gives

    Agrad<=a0 Pscale+int(Agrad^2+G Bgrad),
    Bgrad<=B0+int[L1 Bgrad^2+P1(Bgrad+Agrad/c)],
    D_v q=-v_X, ||z(t)-z0||<=int(Lambda Bgrad+F).       (7.1)

Choose a new kappa>0 less than B and at most

    1, 1/(2a1),
    (a1-a0)/[2(a1^2+G beta+1)],
    (beta-B0)/[2(L1 beta^2+P1 beta+P1 a1/c+1)],
    zeta0/[2(Lambda beta+F+1)].                        (7.2)

Through t<=kappa/Pscale, the bootstrap Agrad<a1 Pscale, Bgrad<beta improves
strictly by (7.1). Density lies in [q_- -1/2,q_+ +1/2] in log units and
field displacement is <=zeta0/2. Initial invariants and bounded g give a
finite speed bound Slo independent of e, e.g. strictly above
V+c||q0||+gbar+c+Lambda+1 for t<=1. This is the Slo used in Section 3.

For exact joins ||f'||=8/(3sqrt(3)), Lip(f')=8. Let Hf=max(Lip r_X,Lip s_X),
Hz=max_i Lip z_i,X. Difference quotients of the gradient equations give

    Hf<=Hf0+int[3Agrad Hf+G Hz+G2 Bgrad^2],
    Hz<=Hz0+int[(3L1 Bgrad+P1)Hz+(P1/c)Hf
                              +L2 Bgrad^3+P2(Bgrad+Agrad/c)^2]. (7.3)

The flow separation has logarithmic derivative bounded by the speed gradient;
this supplies the transport factors in (7.3). The argument applies to the
continuous first derivatives across the joins; no classical f'' is assigned
there. Initially Hf0+Hz0<=h0 Pscale^2 with finite h0 including 8/V. Under
(7.1), for fixed E0,D0 the sum satisfies H<=h0 Pscale^2+int(E0 Pscale H+
D0 Pscale^2), hence H<=C0 Pscale^2 through kappa/Pscale. These constants
are fixed in e, although they can depend on V.

For each fixed e these bounds are finite. The weak spatial derivative of
the PDE reads

    (Ustate_i,X)_t=-lambda_i Ustate_i,XX
      -(Dlambda_i.Ustate_X)Ustate_i,X+DF_i.Ustate_X.

Its RHS is uniformly bounded through a putative endpoint <=kappa/Pscale.
States and gradients have actual uniform C1 traces; their spatial Lipschitz
seminorms and strict margins persist. The characteristic construction restarts
this precise trace, with compatibility from Section 2. Thus no such endpoint
prevents existence through kappa e/V. This is a fresh lower time with fixed
coefficients, not the old theorem with V substituted for a growing amplitude.

Restrict this solution to K_e for that time. Hrad e<R, S>Slo, and (3.1)
ensure it solves the exact original data on the SAME domain used for the upper
argument, with no interface and no stationary patch. Local uniqueness there
follows by subtracting two diagonal systems along the first solution's contained
characteristics: the difference is bounded by its time integral times finite
coefficients and the other solution's first gradient on each compact slab.
Zero initial difference implies zero by iterating this inequality. Consequently
auxiliary exterior choices do not affect their common cone restriction.

There is no union-of-stationary-germs or claim of intrinsic maximal endpoint.
The exact statement is the lower solution on K_e through kappa e/V together
with impossibility of ANY positive classical solution on K_e through B e/V.
The artificial cone tip is inactive: K_e has radius >=3e even at Bcap e/V.
Compatible local restart on the controlled lower interval is proved; a global
maximal-domain/restart equivalence after that interval is outside this claim.

## 8. Width choices, control, and scope

All imposed upper bounds on e are finitely many positive strict constants:
Hrad e<R, e<=min(1,V), Theta_cap<=1, E e<=c, Kq Hrad e<=1,
(Kz Hrad+Af Bcap/V)e<zeta/2, E e<(Vmax-V)/2,
Cv e^2<eta/4, Cv e^2<=c, and e<mu/[2(Ccap+1)]. Zero denominators in a
vacuous bound are omitted. The lower construction uses its own fixed compact
margins and (7.2). Choose the minimum after slightly tightening all inequalities.
This yields e0>0 for every fixed coefficient/background tuple in the stated
acoustic cell, including arbitrarily fast finite field speeds. Restore physical
epsilon0=L e0, time bounds kappa epsilon/V_phys and B epsilon/V_phys,
density bounds by multiplying by nref, and field/velocity errors by their
fixed units. Field-bound constants may be huge; no uniformity in coefficients,
V/cs, chart degeneration, or the vanishing strict acoustic margin is claimed.

For V=0 treat the data separately, without using epsilon/V. H solves the
complete fluid, Q and scale equations exactly, with v=p=w=0, j=0, mf=0,
zero total energy flux, and Delta constant. Pressure balances gravity.
There is no positive P0 margin and no contradiction for this negative control.

Repeat separately for a_ref=9.3619e-11 and 1.1279e-10 m/s^2 with each
compatible background. If cs and Vmax are common, the same acoustic cell
works for this finite pair by taking larger fixed constants and the smaller
epsilon0,kappa, without assuming the backgrounds equal. Constant-vacuum
and each INDIVIDUALLY FROZEN a_ref=a0 E(zcos), E(zcos)^2=.315(1+zcos)^3+.685,
are separate autonomous cases; no evolving-reference or uniform-in-redshift
statement follows. Here zcos is redshift, distinct from the field chart z.

The adopted a_ref=kappa_vac c_light sqrt(G rho_Lambda) is not derived;
a_ref^2=kappa_vac^2 G(-p_vac) is equivalent only for p_vac=-rho_Lambda c_light^2.
The diagnostic chi field is an added assumption, not physical vacuum closure.
Q is A=(sqrt(a^2+4g^2)-a)/2, equivalently F=sqrt(B_N^2+a B_N) for positive
baryonic acceleration B_N. RAR F=B_N/[1-exp(-sqrt(B_N/a))], registered M,
and operative filtered MONO remain distinct and unused here. The full source
A_X=Cn+tau phi_tt retains MOND scaling; no Newtonian missing mass is substituted.
No metric/photon, two-DOF, criterion B, cosmological, cluster/empirical,
calibration, historical novelty, or physical closure conclusion is made.
AS228 ownership and its missing variational-repair dependency are unchanged.

Author's bounded verdict: supports_scoped_claim, subject to independent raw-
proof review. No internal missing implication was identified for this precise
contained-cone claim. The remaining gate is independent audit of Sections
3--7, not authentication of a numerical model or a maximal-endpoint theorem.
Outside Vmax>(15/2)cs this argument gives no upper survival bound; that is a
limitation of this certificate, not a counterexample to the equations.
