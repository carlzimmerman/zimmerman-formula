# FGF056: one buffered maximal germ with fast fields and moving interior matter

Author /root/fgf056_author; fgf056_run_001. Unreviewed proof-only candidate.
All thirteen ancestry hashes were checked before source use. No new stage43
reviewer/coordinator work was read. The corrected FGF055 proof is used jointly
with its pinned scope clarification and correction audit. Numerical experiments:
zero. Hash and JSON checks are administrative, not mathematical computation.

## 1. Exact claim and inherited equations

Fix positive physical C=4 pi G,tau,sigma,J,S0,cs,nref,a_ref, a smooth compatible
positive hydrostatic H near x*, with g0>0, and finite Vmax. Fix independently of
epsilon

    (15/2)cs < V < Vmax,       15/2 < B < Bcap < V/cs.       (1)

The field speeds can be any fixed finite values. There exist epsilon0,kappa>0
such that the exact C1,1 packet v=V f((x-x*)/epsilon), f=(1-y^2)^2 on |y|<1
and zero otherwise, with all initial density and fields equal H and p=w=0,
has the single whole-packet maximal classical germ defined in Section 4. Its
maximal physical time T_epsilon satisfies

    kappa epsilon/V <= T_epsilon <= B epsilon/V.            (2)

All density and field-chart margins, and |v|<Vmax, persist on its existing
prefixes. For the full seven-coordinate first-order state U below, on the
fixed restart interval J1,

    limsup_(t upward T_epsilon) max_i ||U_i,x(t)||_(J1)
        = infinity.                                       (3)

The units in (3) may equivalently be fixed dimensionless units. Constants are
not uniform in coefficients, V/cs, or vanishing strict margins. The theorem is
conditional on (1), the stated diagnostic equations and H; it is not a claim
of an authenticated physical tuple, a particular divergent component, shock,
weak continuation, exact lifespan coefficient, or physical theory completion.

Use the same fixed units L,u as FGF055: X=(x-x*)/L, t=u t_phys/L, e=epsilon/L,
V=Vphys/u,c=cs/u,n=nphys/nref,phi=phiphys/u^2. Fields g,p,k,w have units
u^2/L,u^3/L,1/L,u/L. Suppressed dimensionless coefficients are
C_hat=C nref L^2/u^2,tau_hat=tau u^2,sigma_hat=sigma/u^2,J_hat=J/u^4,
a_hat=a_ref L/u^2,S0_hat=S0 L^2/u^4. Set q=log n,g=phi_X,p=phi_t,
k=chi_X,w=chi_t,a=a_ref exp chi and

    A(g,chi)=(sqrt(a^2+4g^2)-a)/2,
    W=int_0^g A(s,chi) ds, Tscale=-W_chi,
    Uscale=S0(cosh(2chi)-1)/4.

The COMPLETE equations are

    q_t+v q_X+v_X=0,     v_t+v v_X+c^2 q_X=-g,
    g_t=p_X,             tau p_t=A_g g_X+A_chi k-C exp q,
    k_t=w_X,             sigma w_t=J k_X+Tscale-Uscale',
    chi_t=w.                                                  (4)

H satisfies A0_X=C rho,c^2(log rho)_X=-g0 and
J chi0_XX+Tscale0-Uscale'(chi0)=0,v0=p0=w0=0.
On g>0 define b=sqrt(A_g/tau),d=sqrt(J/sigma),h_g=b, with the fixed lower
integration limit for h used by FGF055. The coordinates are

    r=v+cq, s=v-cq, R+=p+h, R-=p-h,
    Z+=w+d k, Z-=w-d k, z=(R+,R-,Z+,Z-,chi), U=(r,s,z).

With As=A_chi k/tau-C exp(q)/tau and Ds=(Tscale-Uscale')/sigma,

    D_(v+c) r=-g, D_(v-c) s=-g,
    D_-b R+=As+h_chi(w-bk), D_+b R-=As-h_chi(w+bk),
    D_-d Z+=Ds, D_+d Z-=Ds, chi_t=w.                         (5)

Write (5) as U_i,t+lambda_i(U)U_i,X=F_i(U). The field sources depend on
(q,z), not v or derivatives; the density source and both h_chi terms remain.
There is no division by differences of characteristic speeds. Chi_X=k
propagates from the Z equations. The R difference gives g_t=p_X; their sum
gives p_t=b^2 g_X+As+b h_chi(chi_X-k), whose last term vanishes. Reconstruct
phi=phi0+int p dt. Then phi_X=g and A_X=Cn+tau phi_tt exactly. This verifies
compatibility initially, at comparisons and at restart.

## 2. Three spatial scales and the known-background comparison

Choose a FIXED [-R,R] in the original H patch, with a slightly larger open
neighborhood; shrink it so its field range is inside a single positive compact
chart neighborhood about z0(0). Let J=(-R,R), J1=[-R/2,R/2]. Coefficients,
background norms and R are independent of e. Choose

    S_H > max(c, sup_[-R,R] b(H), d, 0).

This is a bound on H's characteristics only. It is NOT an assumed speed bound
for an unknown solution. Define

    Theta_cap=Bcap e/V,     ell_s(t)=e+S_H t,
    R_e=(2+S_H Bcap/V)e.                                   (6)

The fixed-in-time interval I_e=[-R_e,R_e] contains the proposed support envelope
with at least e unused room through Theta_cap. It is different from the
DYNAMIC interior moment interval I=[-2e,2e]. In particular no stationarity at
+/-2e is imposed or inferred.

Here is the precise comparison identity. For a classical U and known H, put
D=U-H. Along KNOWN H characteristics,

    D_(lambda_i(H)) D_i
      =F_i(U)-F_i(H)+[lambda_i(H)-lambda_i(U)] U_i,X.       (7)

The last term contains the UNKNOWN solution gradient and is retained. On each
compact smooth prefix the two ranges lie in a compact positive chart, their
coefficient differences are Lipschitz, and sup|U_X| is finite. Extend smooth
coefficients over a slightly larger compact neighborhood if needed. Thus the
absolute RHS is at most C_T sup|D|, with C_T allowed to depend on this prefix's
gradient. No bound uniform near a breakdown is used in this comparison.

There are two versions of its domain:

(a) On J, assume U is H on the open outer strips |X|>R/2. In the right exterior
X>ell_s(t), a backward H characteristic satisfies
X(s)>e+S_H s, since |lambda_i(H)|<S_H. It reaches t=0 outside the packet,
or first reaches an outer strip, where D=0. The same holds on the left.
The integral inequality over these exteriors has zero initial/lateral data:
Dsup(t)<=C_T int_0^t Dsup(s) ds. Iterating it gives zero (the j-th bound has
factor (C_T t)^j/j!). Hence

    U(t,X)=H(X) whenever |X|>=ell_s(t).                    (8)

Equality extends to the moving edges by C1 continuity. One may restrict to
a closed interior interval ending in the zero outer strips before taking
suprema; no trace at the open endpoints of J is required.

(b) On a shrinking cone K(t)=[-K0 e+S t,K0 e-S t], with S>S_H, the backward
H paths cannot exit its outer boundaries. Intersect the same exteriors with
K(t). Their backward H paths stay in the intersection and end on the original
initial exterior. The same inequality gives (8) on that cone, without ANY
boundary data or speed cap on U. This version is essential for constructing
and identifying the germ from a local Cauchy solution.

The support assertion is therefore a consequence of classical comparison,
not a postulate about the largest instantaneous unknown speed. A nonlinear
packet trying to cross this envelope would have to lose the regularity that
makes (7) a bounded comparison inequality. This statement identifies no such
loss mechanism or individual wave.

## 3. A wider cone, actual global margins, and unchanged upper obstruction

The original parent cone has radius 3e at Theta_cap. For fast fields its radius
need NOT contain ell_s(Theta_cap). Reusing only that cone for continuation
would leave part of the germ uncontrolled. We explicitly enlarge the initial
width. Choose fixed

    S>max(S_H,Vmax+c,tau^(-1/2),d,Slo),
    K0=3+(S_H+S)Bcap/V,
    K(t)=[-K0 e+S t,K0 e-S t].                             (9)

Slo is the fixed lower-construction speed in corrected FGF055 Section 7. Then
K(t) contains I_e plus an e buffer for all t<=Theta_cap. Require K0 e<R/4,
Theta_cap<=1, and later e sufficiently small for each strict bootstrap.
All initial footprints of K lie in H's physical patch. The parent small cone
is contained in this larger cone, and both moment endpoints lie well inside.

For completeness, the parent amplitude argument works with this new K0.
On any existing positive solution on K, bootstrap |v|<Vmax and a compact field
ball |z-z*|<zeta. The choice S then contains every actual backward path.
Let Q1,Z1 bound the known derivatives of q0,z0, and Gbar bound |g|. Initial
centered acoustic invariants lie between -c Q1 K0 e and V+c Q1 K0 e. Thus

    -E e <= v+c(q-q*),v-c(q-q*) <= V+E e,
    |v|<=V+E e, |q-q*|<=V/(2c)+E e/c,
    E=c Q1 K0+Gbar Bcap/V.                                (10)

For E e<=c this gives n_-<=n<=n_+ with
n_-=exp(q*-V/(2c)-1), n_+=exp(q*+V/(2c)+1), independent of e. This controls
the ACTUAL exp q field source. Subtract the varying H field equations along
actual field paths:

    D_lambda_i(z)(z_i-z0_i)
      =H_i(q,z)-H_i(q0,z0)
         -[lambda_i(z)-lambda_i(z0)] z0_i,X.               (11)

Only known background derivatives occur here, in contrast to (7). All density,
scale and chart terms are bounded on the compact ranges. Initial difference
is zero; hence sup_K |z-z0|<=C t exp(Ct)<=C_1 t. Consequently

    |g-g0|<=C_2 t, |z-z*|<=(Z1 K0+C_1 Bcap/V)e.           (12)

For small e this is <zeta/2 and E e<(Vmax-V)/2. First exit closes both
bootstraps on every existing prefix, independently of solution gradients.
In particular g,a retain strict positive margins, and p,w,chi-chi0,k-k0=O(e)
on this ENTIRE enlarged cone.

If the solution is an admissible segment of Section 4, (8) says it equals H
outside ell_s(t). Since that envelope lies in K(t), (10)--(12) control every
nonstationary point in J. Outside K use the actual H(X) and its compact
positive bounds on [-R,R]. This yields global chart and density margins and
|v|<Vmax on J. We do NOT claim z-z0(0)=O(e) throughout fixed J. The correct
statements are central O(e) on K and exact H(X) outside the support envelope.
Also sup_J|z-z0(X)|=O(e) follows, since it is zero off the envelope; no small
interior matter displacement is asserted.

The exterior ACOUSTIC wedges X>=e+(c+eta)t and X<=-e-(c+eta)t intersected
with K, where 0<eta<V/Bcap-c, contain A=-2e,D=2e. Centered matter variables
u+=v+c(q-q0),u-=v-c(q-q0) satisfy exactly

    D_(v+c)u+=-(g-g0)-c v q0_X,
    D_(v-c)u-=-(g-g0)+c v q0_X.                           (13)

Bootstrap |u±|<eta/2. Their backward acoustic paths remain in the wedges and
reach the initial exterior. Equation (12) yields sup|u±|<=C t^2 exp(Ct),
which closes for small e. Therefore v=O(e^2),n-rho=O(e^2),j=nv=O(e^2) on
these wedges and at A,D ONLY. In the interior packet nv^2 is initially O(1).
Field stress Sf-Sf0 and mf, defined in Section 7, are O(e) throughout K.
This is the mandatory corrected parent scope.

The exact moment identity on I remains unchanged by widening the cone:
M=int_I n,P=int_I nv,I1=int_I(X-A)n,Delta=(D-A)M-I1>0 satisfy

    M'=j(A)-j(D), I1'=P-4e j(D),
    P'=-Rmom, Rmom=[nv^2+c^2(n-rho)]_A^D+int_I(ng-rho g0),
    Delta(T)=Delta0-P0 T+int_0^T(T-t)Rmom(t)dt
                                      +4e int_0^T j(A,t)dt.            (14)

The full density/field bounds give bulk O(e); endpoint pressure O(e^2),
kinetic O(e^4), and j(A)=O(e^2). At T=B e/V these remainder terms are
O(e^3),O(e^4),O(e^6),O(e^4), respectively. Taylor expansion of the fixed
smooth rho and exact int_-1^1 f=16/15 give

    Delta0=8rho*e^2+O(e^3), P0=(16/15)rho* V e+O(Ve^2),
    Delta(B e/V)<=rho*[8-(16/15)B]e^2+O(e^3)<0.            (15)

Positive density rules this out. Thus no such cone or admissible segment
survives through B e/V. The separately audited sharper O(e^4) dynamical
remainder is unnecessary here; initial Taylor error remains O(e^3). We do not
promote that refinement to threshold optimality.

## 4. Definition and construction of the SAME maximal germ

An admissible segment of length T<Theta_cap is a solution of (4) on [0,T]xJ
with positive n,g, exact initial data and initial potential gauge, spacetime C1
first-order state and C2 potentials, spatial gradients locally uniformly
Lipschitz on compact time slabs, and EXACT H on |X|>R/2. No boundary condition
is prescribed at +/-2e. Outer strips are a representation of the surrounding
known physical background, with unused room, not an artificial wall near the
packet. By (7)--(8), each admissible segment actually equals H outside
ell_s(t), a strictly stronger conclusion with large unused overlaps.

Two such segments coincide on a common prefix. Choose a closed interval
[-3R/4,3R/4]; their difference is zero in its outer strips. Subtract their
diagonal equations along the first solution's paths, stopping at time zero
or the first outer-strip contact. The difference of coefficients multiplies
the second solution's finite gradient. The resulting zero-data integral
inequality gives equality. No uniform gradient bound beyond that prefix is
needed. Potentials agree by equal p and initial gauge. This comparison also
works against a merely C1 positive competitor on the relevant footprint.

There is a genuine lower admissible segment. Use corrected FGF055 Section 7's
explicit characteristic iteration for the exact packet and compatible smooth
extension of H from a fixed patch to the auxiliary line. Its fixed-V bounds,
with Pscale=V/e, are Agrad<=a1 Pscale,Bgrad<=beta and
Hf+Hz<=C0 Pscale^2 through kappa/Pscale, with strict amplitude margins.
The exact joins have ||f'||=8/(3sqrt(3)),Lip(f')=8. The construction and
actual trace/restart in that section prove the lower time afresh, not by
substitution in FGF053's growing-amplitude theorem. Choose kappa<B and shrink
e so the enlarged K(0) lies inside the FIXED unaffected extension patch and
S>Slo. Its characteristic domain of dependence contains K through this lower
time. Thus the constructed restriction solves exactly (4) on the SAME K.

Apply comparison version (b) to it. It equals H on K outside ell_s(t).
At X=+/-R_e the comparison leaves a stationary open collar of width at least
e on its inner side and e on its outer side within K. Restrict to I_e and
patch to H on J\I_e. Equality holds on OPEN overlaps, so no derivative jump
or interface source is introduced. The potentials also agree there: these
collars are exterior to ell_s(s) at every earlier s, so p=w=0 there throughout
the history and phi=phi0,chi=chi0. We now have an admissible segment through
kappa e/V, independent of auxiliary extension.

More generally any positive classical solution defined on a neighborhood of
this closed K prefix with the exact initial data has (8) there by version (b),
and so patches by this same argument to an admissible segment (if its regularity
is C1,1, it belongs to the specified class). Conversely any admissible segment
restricts to such a cone solution. This explicit footprint equivalence is what
allows the parent's cone obstruction to concern the SAME whole-packet germ.
It does not assert continuation at a single point while discarding the rest
of the packet.

Let T_e be the supremum of lengths of admissible segments. Uniqueness identifies
all overlaps, so their union defines one solution on [0,T_e)xJ. Every compact
prefix belongs to an admissible segment. The preceding lower construction and
(15) give

    kappa e/V <= T_e <= B e/V < Theta_cap.                 (16)

The time cap is strictly inactive. The perturbation is in I_e, which lies
inside [-R/4,R/4]; fixed outer strips are never approached. Different auxiliary
extensions or wider physical patches yield the same restriction and potential
gauge on the common whole-packet footprint. Their maximal times agree when
their own bookkeeping caps are inactive, because continuation on the common
cone can be patched to either representation. No selected arbitrary maximal
chain or assumed future existence is involved.

## 5. Bounded first gradients force bounded full higher seminorms

Suppose contrary to (3) that limsup_(t up T_e) D(t)<infinity, where
D(t)=max_i||U_i,X||_(J1). Compact earlier prefixes then bound D by a finite M1
on all [0,T_e). Outside I_e the state is H; thus all first gradients on J are
bounded too. Section 3 provides compact state ranges, positive density/chart
margins and finite speeds on the ENTIRE required domain, uniformly in time.
For this fixed e choose finite first/second coefficient derivative bounds on
a slightly larger smooth cutoff neighborhood of those ranges. The cutoffs
will never alter the actual equation there.

Choose S1 above every actual speed furnished by these amplitude bounds and
above H's speeds. It can be chosen independent of e; require additionally
S1 Theta_cap<R/4. The inward cones

    L(t)=[-3R/4+S1 t,3R/4-S1 t]

contain J1 and all perturbations through Theta_cap. Every backward actual
characteristic and intermediate spatial segment used below lies in earlier
L(s); no unknown lateral data enter the higher estimates.

Set Agrad=max(||r_X||,||s_X||),Bgrad=max_i||z_i,X|| on L(t),
Hf=max(Lip r_X,Lip s_X),Hz=max_i Lip z_i,X. All first gradients are bounded
by M1 enlarged by the fixed H bounds. Differentiating (5) once gives

    D_(v+c) r_X=-v_X r_X-g_X,
    D_(v-c) s_X=-v_X s_X-g_X,
    D_i z_i,X=-(D_z lambda_i.z_X)z_i,X
                              +H_i,q q_X+D_z H_i.z_X.      (17)

In particular H_i,q contains -C exp(q)/tau in the Q equations. It is retained.
Let G,G2 bound the first/second derivatives of g, L1,L2 those of field speeds,
and P1,P2 those of complete field sources. Sup norms include component sums.
Subtract (17) along two paths of the same family and divide by their positive
separation. Its logarithmic derivative is bounded by the corresponding speed
gradient. Using |v_X|<=Agrad,|q_X|<=Agrad/c gives

    Hf(t)<=Hf(0)+int_0^t[3Agrad Hf+G Hz+G2 Bgrad^2]ds,
    Hz(t)<=Hz(0)+int_0^t[(3L1 Bgrad+P1)Hz+(P1/c)Hf
                              +L2 Bgrad^3+P2(Bgrad+Agrad/c)^2]ds.       (18)

The three transport factors include the separation derivative and the two
speed-gradient products. For each compact prefix the C1,1 regularity already
makes these difference quotients legitimate. Continuous first derivatives
at the original packet joins are used exactly; no classical f'' is assigned
at a join and no smoothed packet is substituted. These are the same elementary
full coupled estimates reconstructed in FGF053, now on the domain L with
actual amplitude bounds derived for this fast-field problem.

Bounded first gradients reduce (18) to H(t)<=H(0)+int(E1 H+E2), hence

    Hf(t)+Hz(t) <= [Hf(0)+Hz(0)+E2 t] exp(E1 t) <= Hbar_e<infinity. (19)

For fixed e the initial seminorm is finite and contains 8V/e^2, not a bound
uniform in e. Neither E1,E2 nor Hbar_e is claimed uniform as the assumed M1
varies. This suffices for continuation at the single fixed-e endpoint.

## 6. Actual endpoint traces, constraints, outer gluing and restart

On fixed J1, (19) bounds U_XX a.e.; all coefficients and first gradients are
bounded. The equation bounds U_t. Distributionally,

    (U_i,X)_t=-lambda_i(U) U_i,XX
                -(Dlambda_i(U).U_X)U_i,X+DF_i(U).U_X.      (20)

Its right side is uniformly bounded for this fixed e. Integrating in time
and then taking continuous spatial representatives yields uniform Lipschitz
time bounds for both U and U_X on J1. They therefore have actual uniform
limits U*,V* as t approaches T_e. Integrating in X identifies V*=(U*)_X.
The spatial Lipschitz bound (19) passes to this trace. Moreover the equation
shows U_t tends uniformly to F(U*)-lambda(U*)V*. Thus the limiting trace
contains the time-C1 matching data, not just an a.e. limit of amplitudes.

Smooth inverse coordinates give positive n*,g*, finite chi*, and the propagated
constraint chi*_X=k*. Define phi*=phi0+int_0^T_e p(s)ds. The integral and its
spatial derivative converge; g_t=p_X yields phi*_X=g*. Its spatial regularity
is C2,1, and p* is its time velocity. Potentials and their required derivatives
are compatible with the full original (4). By (8) the endpoint trace equals H
on |X|>ell_s(T_e), not merely beyond I_e. Choose, for example, an open collar
of half-width e/4 about each +/-R_e. It and a substantially larger surrounding
interval remain exterior to ell_s(t) for every t<=T_e. There p=w=0 throughout,
so both phi*=phi0 and chi*=chi0 hold on BOTH sides. This verifies potential
constants, not merely equality of g and k.

Extend the actual trace from J1 to the auxiliary line using H in the adjacent
physical patch, since it already equals H on open overlaps. Farther away use
a bounded smooth compatible extension of q0,g0,chi0, with g0 kept positive and
k0=chi0_X; set p=w=v=0 there. Choose the antiderivative of g to match phi* on
J1. Equality with phi0 on both stationary collars ensures the same potential
constant matches on both neighboring sides. The trace and exact packet joins
are untouched. This is a C1,1 compatible positive auxiliary datum.

For precision about existence, the source-pinned construction in FGF051
Section 4 freezes speeds/sources at each iterate and solves transport along
that iterate's paths. With finite initial gradient K and derivative-Lipschitz
bound H, a short time preserves doubled bounds by the differentiated transport
and difference-quotient inequalities. Successive differences obey
||U^(j+1)-U^j||<=C delta_t(1+K)||U^j-U^(j-1)|| with factor <1/2.
Uniform C0 convergence plus |f_X-g_X|<=2||f-g||/h+Hh gives uniform C1
convergence; the PDE supplies continuous time derivatives. This constructs an
actual C1,1 restart from THIS trace with strict chart margins. Equations (5)
propagate the constraints and reconstruct (4), as checked in Section 1.
It does not presume an already existing continuation or a smoother trace.

Choose the positive restart duration small enough that (i) it is less than
Theta_cap-T_e, (ii) the restart physical Cauchy cone contains I_e and its open
collars, and (iii) the known H characteristics cannot consume the unused e/4
collar widths. Comparison identity (7), now with zero difference on these
initial collars, preserves smaller stationary open collars about +/-R_e.
Patch the restarted restriction to H outside I_e exactly as in Section 4.
It has the outer-strip condition, solves the same equations, and is classical
across T_e: U,U_X and U_t agree there by (20), and potentials agree with their
second derivatives by compatibility. C1,1 bounds are finite on the new compact
slab. Reapplying the original initial-time exterior comparison to the glued
solution recovers (8); it need not be assumed during the restart construction.

The new solution is an admissible extension of the SAME germ. Uniqueness
identifies any overlap; no exterior extension choice changes it. This contradicts
the definition of T_e. Thus a bounded combined-gradient limsup is impossible,
and (3) follows. Artificial cone tips, outer boundaries, compact-chart exit,
density zero/infinity, or the inactive time cap are not alternative explanations
for this endpoint under the established bounds. The conclusion is still only
an obstruction in the combined first-gradient norm.

## 7. Full balances: the internal endpoints remain nonstationary

Let j=nv and define

    mf=-(tau p g+sigma w k)/C,
    Sf=[gA-W+tau p^2/2+sigma w^2/2+J k^2/2-Uscale]/C.

Using (4), including A_X-Cn and the entire scale equation,

    n_t+j_X=0,
    j_t+(nv^2+c^2 n)_X=-ng,
    mf_t+Sf_X=ng.                                          (21)

Indeed (gA-W)_X=g A_X+Tscale k; its scale term cancels the corresponding
term from mf_t. The background satisfies Sf0_X=rho g0 and
(c^2 rho+Sf0)_X=0. On I=[A,D]=[-2e,2e] we have exactly

    P'=-[nv^2+c^2 n]-int_I ng,
    Fm'=-[Sf-Sf0]+int_I(ng-rho g0),
    (P+Fm)'=-[nv^2+c^2(n-rho)+(Sf-Sf0)].                   (22)

Neither j(A),j(D),pressure nor field stress is zero there. Throughout I the
field bounds yield mf,Sf-Sf0=O(e); the matter endpoint orders O(e^4),O(e^2)
hold only on the acoustic wedges. This reproduces the corrected scope.

With eint=c^2 n(log n-1) and the reconstructed actual potential, put

    E=nv^2/2+eint+n phi
             +[tau p^2/2+W+sigma w^2/2+J k^2/2+Uscale]/C,
    FE=nv[v^2/2+c^2 log n+phi]-(pA+Jwk)/C.                 (23)

Fluid kinetic/internal energy contributes -nvg; n phi changes this to np.
The Q field contributes -np-Tscale w/C, the scale field +Tscale w/C.
Both field fluxes are present, and E_t+FE_X=0. Thus on any fixed [a,b]
contained in the physical solution, int E has derivative FE(a)-FE(b).
For arbitrary contained moving endpoints alpha,beta and balance h_t+F_X=s,

    d/dt int_alpha^beta h=int_alpha^beta s+F(alpha)-F(beta)
                                +beta' h(beta)-alpha' h(alpha).        (24)

Apply this to each equation (21), their sum and (23). On shrinking K the last
term is -S[h(beta)+h(alpha)]; on L it is -S1[h(beta)+h(alpha)]. Those terms
are not omitted. On the expanding support envelope they have the opposite
outward signs; subtraction of stationary background is possible but must use
the corresponding background terms as well.

At the REMOTE fixed +/-R_e, (8) does imply j=mf=FE=0 and total stress equal
the same constant background total stress on both sides. Consequently mass,
total momentum and energy integrated over I_e have zero boundary derivative
(the separate fluid momentum still exchanges with fields). These are derived
outer facts, never transferred to +/-2e. No energy coercivity or separate
field-momentum conservation is invoked in the continuation proof.

## 8. Controls, branch bookkeeping, and stop

For V=0 use H itself, without epsilon/V: all equations hold, pressure balances
gravity, p=w=v=0, j=mf=FE=0. The packet momentum margin in (15) vanishes.
This control does not have the finite upper endpoint conclusion.

Every smallness condition on e is a finite strict positive bound once the
physical tuple, H, V,B,Bcap and speed margins are fixed. In particular they
include K0 e<R/4, S1 Theta_cap<R/4, the parent bootstrap and acoustic-wedge
inequalities, and the strict negative moment margin in (15). Arbitrarily large
but fixed field speeds only worsen constants; no coefficient-uniform limit is
claimed. Restore (16) to physical time using L/u to obtain (2).

Repeat separately for a0=9.3619e-11 and 1.1279e-10 m/s^2, with each one's
compatible H. The adopted a_ref=kappa_vac c_light sqrt(G rho_Lambda) is not
newly derived; a_ref^2=kappa_vac^2 G(-p_vac) is equivalent only when
p_vac=-rho_Lambda c_light^2. The chi sector remains an added diagnostic
assumption, not a derived physical vacuum identification. Constant-vacuum and
each separately frozen a_ref=a0 E(zcos), E(zcos)^2=.315(1+zcos)^3+.685, are
different autonomous cases. An evolving reference changes chart/work terms
and needs a reservoir equation; no such theorem is asserted here.

Q is A=(sqrt(a^2+4g^2)-a)/2, equivalently F=sqrt(B_N^2+a B_N) on the
positive radial branch. RAR F=B_N/[1-exp(-sqrt(B_N/a))], registered M and
operative filteredMONO remain distinct and unused. Dynamic MOND source
A_X=Cn+tau phi_tt is retained; there is no Newtonian missing-mass substitution
or source/discrepancy fit. No metric/photon, two-DOF, criterion-B, cosmological,
cluster, calibration, observational likelihood or historical novelty claim.

The author candidate settles only the named same-germ continuation implication,
subject to independent raw-proof audit. STOP this finite-V diagnostic endpoint
chain if accepted. The physical priorities remain the independently checked,
owned AS228 variational repair and both metric equations, and authenticated
instrument response/covariance/outer constraints for cluster inference. No new
child refinement, uncalibrated sweep or ownership change is proposed.
