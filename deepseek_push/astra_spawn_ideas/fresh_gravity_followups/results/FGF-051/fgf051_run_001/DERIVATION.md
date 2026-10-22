# FGF051: bounded-speed edge evolution of the unchanged coupled data

Author candidate by `/root/fgf051_author`, run `fgf051_run_001`. Proof-only;
zero mathematical executable computations. All ten task ancestry hashes and
the task hash were verified before source-text use. No new stage38 root or
reviewer derivation or preview has been read. This is an author proof with
self-review, not independent acceptance.

## 1. Precise claim and scope

Fix positive C=4 pi G_Newton, tau,sigma,J,S0, sound speed cs,nref,L,v0 and
one positive fixed a_ref, independently of N. Fix the inherited smooth
hydrostatic background on a neighborhood of K0=[x*-R,x*+R], with
rho>0 and g0=phi0_x>0. Its equations and the actual evolved equations are
written below. For all sufficiently large integer N, keep EXACTLY

    n(0)=rho, phi(0)=phi0, chi(0)=chi0, phi_t(0)=chi_t(0)=0,
    v(0,x)=v0 N f((x-x*)/(L N^-3)),
    f(y)=(1-y^2)^2 for |y|<1, and f=0 for |y|>=1.          (1.1)

There are fixed radii 0<r_*<R_i<R_o and constants k_edge,S>0,
independent of N, giving compatible classical local solutions on BOTH
shrinking domains

    D_e(t)={|x-x_e| <= L[R_o N^-7/2-S v0 t/L]},
    x_e=x* +/- L N^-3,
    0<=t<=k_edge (L/v0)N^-7/2.                           (1.2)

All seven characteristic speeds, and material speed, have magnitude less
than v0 S there. The fixed inner intervals |x-x_e|<=L R_i N^-7/2 persist
throughout that time. Solutions have matter and first field derivatives C1
in spacetime, first spatial derivatives Lipschitz for each fixed N, and
potentials C2. Density, scale and g have positive N-independent margins.
The initial v=b0 and v=b0+cs intersections on both halves, and every
positive-velocity initial material/Q or acoustic/Q intersection inside the
packet, lie in |x-x_e|<=L r_* N^-7/2. Their material, fluid acoustic and Q
characteristics stay in the protected inner intervals on the asserted time.

This does NOT assert that every later speed-intersection point stays there.
If b0=cs occurs in the zero-velocity exterior, it is also an acoustic/Q
coincidence; no claim places arbitrary such background points in edge strips.
That exceptional class was not excluded by the supplied hypotheses. The
specific v=b0 and v=b0+cs crossings requested by the task are all covered.
No new nonsonicity assumption is introduced to hide this distinction.

The local solution equals any existing positive whole-packet classical branch
on the common closed local cone (or its compact interior if a branch is only
open-domain defined). No existence of the whole branch through (1.2) follows.
For every fixed prescribed B_*>0, (1.2) contains the full comparison time
T_N=B_*(L/v0)N^-4 when N^(1/2)>=B_*/k_edge. Local force, density-gradient
and adverse-gradient bounds on these domains are proved in Section 8.
They do not bound a supremum over the full FGF049 cone.

## 2. Equations, units and full diagonal chart

In physical units let

    g=phi_x, p=phi_t, k=chi_x, w=chi_t, a=a_ref exp chi,
    B(g,a)=(sqrt(a^2+4g^2)-a)/2,
    W(g,a)=integral_0^g B(s,a) ds, T=-W_chi,
    U_s(chi)=S0[cosh(2chi)-1]/4.

The four equations are

    n_t+(nv)_x=0,
    v_t+v v_x+cs^2(log(n/nref))_x=-g,
    tau phi_tt=B_x-Cn,
    sigma chi_tt=J chi_xx+T-U_s'.                         (2.1)

The hydrostatic data obey

    B(g0,a_ref exp chi0)_x=C rho,
    cs^2(log rho)_x=-g0,
    J chi0_xx+T(g0,a_ref exp chi0)-U_s'(chi0)=0.           (2.2)

Use X=(x-x*)/L, theta=v0 t/L, velocity v0, potential v0^2,
density nref, g unit v0^2/L, p unit v0^3/L, w unit v0/L,
k unit 1/L. Suppress hats and use q=log(n_physical/nref). The fixed
coefficients in the following equations are

    c=cs/v0, tau_hat=tau v0^2, sigma_hat=sigma/v0^2,
    J_hat=J/v0^4, C_hat=C nref L^2/v0^2,
    a_ref_hat=a_ref L/v0^2, S0_hat=S0 L^2/v0^4.             (2.3)

All remaining sections through Section 8 use these dimensionless coefficients
and variables unless explicitly restored. In particular N is the initial
velocity amplitude, X_e=+/-N^-3, and P=N^(7/2). P is an inverse edge length,
not a physical coefficient or pressure. Denote coefficient derivative bounds
by K1,K2 below to avoid confusing them with P.

On g>0 define d=sqrt(J/sigma), b=sqrt(B_g/tau), and
h(g,chi)=integral_gstar^g b(s,chi) ds for fixed gstar>0. Since
B_g=2g/sqrt(a^2+4g^2)>0, (g,p,w,k,chi) has a smooth invertible chart

    r=v+cq, s=v-cq,
    R_+=p+h, R_-=p-h, Z_+=w+d k, Z_-=w-d k,
    z=(R_+,R_-,Z_+,Z_-,chi).

Here the plus R mode travels at -b; the minus R mode travels at +b.
Set A_s=B_chi k/tau-C exp(q)/tau and D_s=(T-U_s')/sigma. Direct chain
rule from the compatible equations gives the diagonal system

    r_theta+(v+c)r_X=-g,
    s_theta+(v-c)s_X=-g,
    R_+,theta-b R_+,X=A_s+h_chi(w-b k),
    R_-,theta+b R_-,X=A_s-h_chi(w+b k),
    Z_+,theta-d Z_+,X=D_s,
    Z_-,theta+d Z_-,X=D_s,
    chi_theta=w.                                         (2.4)

Every h_chi term and the actual exp(q) source is retained. Thus field speeds
lambda_i(z)=(-b,+b,-d,+d,0) and sources H_i(q,z) depend on no fluid velocity
and no state derivative. The fluid inverse is v=(r+s)/2,q=(r-s)/(2c), with
fixed c>0. Coincident field/fluid speeds cause no singular chart or division.
Section 7 derives the constraints from (2.4), closing the converse direction.

## 3. Exact edge profile, intersections and auxiliary data

Choose a fixed background neighborhood containing every packet for large N.
Let b_bar be an upper bound for its dimensionless b0; set
r_*=sqrt(b_bar+c), R_i=r_*+1 and R_o=R_i+2. Other fixed positive margins
would work. At the right edge write u=P(X_e-X); at the left write
u=P(X-X_e). On the interior half, 0<=u<=sqrt(N), the exact identity is

    v_N=u^2(2-u/sqrt(N))^2.                               (3.1)

It is zero on the exterior side. For 0<=u<=D with sqrt(N)>=D,

    0<=v_N<=4D^2,
    |(v_N)_X|<=8D P,
    Lip((v_N)_X)<=8 P^2.                                 (3.2)

The derivative estimate follows by differentiating (3.1): its u derivative
is 4u(2-u/sqrt(N))(1-u/sqrt(N)), of magnitude at most 8u.
The second derivative is the original N^7 f''; |f''|<=8 on [-1,1].
f' is continuous and vanishes at each join, so the a.e. second-derivative
bound implies the Lipschitz bound across the join too. No join is smoothed.

On each half (3.1) also gives v_N>=u^2. Every strictly positive initial
speed-intersection value belongs to

    v_N=b0, b0+c, b0-c, or c-b0,                          (3.3)

with only positive RHS retained. These come respectively from v=+b and
v+/-c=+/-b; v=-b is impossible for v>=0 and b>0. Every positive RHS
in (3.3) is <=b_bar+c, so every such point has u<=r_*.
For v=b0 and v=b0+c, the difference is negative at the support edge and
positive at the center for N>b_bar+c, so at least one root lies in each half.
There is no root outside the support for these two positive targets. This
proves inclusion for ALL their roots, without treating b0 as constant.
Values v=0,b0=c give the exterior exception stated in Section 1. The joins
when b0=c are included since u=0. No finite-crossing-count premise is needed.

For construction, fix a C-infinity cutoff eta(ξ), equal to one for
|ξ|<=R_o, zero for |ξ|>=R_o+1, and 0<=eta<=1. For each edge separately
extend the velocity by

    v_e^ext(X)=eta(P(X-X_e)) v_N(X).                       (3.4)

Choose N so sqrt(N)>=R_o+1 and the support of (3.4) lies in the original
background patch and does not reach the packet center. If E1=||eta'||,
E2=||eta''||, D=R_o+1, the extended velocity satisfies

    ||v_e^ext||<=V_e=4D^2,
    ||(v_e^ext)_X||<=C_v P, C_v=8D+4D^2 E1,
    Lip((v_e^ext)_X)<=C_h P^2,
    C_h=8+16D E1+4D^2 E2.                                (3.5)

These constants are independent of N and of the choice of edge. This changes
only auxiliary data outside the physical outer strip, not the requested
initial data on it. It is not a smoothing of either original join.

Extend q0 and chi0 smoothly to bounded constants outside a fixed neighborhood,
and extend g0 by a smooth positive convex cutoff to a positive constant.
All background derivatives through the needed order are bounded independently
of N, with 0<m<=g0<=M. Put k0=chi0_X, p0=w0=0 and take phi0 as a compatible
antiderivative. This agrees with (2.2) on the original patch; hydrostatics
outside it is not needed. Section 9 proves that no imposed exterior data
or deletion of incoming high-speed core data changes the physical germ.

## 4. Starting the actual C1,1 system without an imported existence gate

Here is a local construction for each fixed N and for every compatible
C1,1 restart state staying in the chart. It applies on the auxiliary line.
Use smooth coefficient cutoffs in state space, equal to one on a compact
neighborhood of the initial q,z range, and a velocity cutoff outside a finite
range larger than the initial r,s amplitudes. The cutoffs give globally bounded
C2 speeds/sources and derivatives. They do not alter (2.4) in the neighborhood
ultimately proved to contain the solution. Convex segments between two states
can then be estimated without leaving the domain of coefficient definition.

For U=(r,s,z), write the cut-off equation as U_i,theta+lambda_i(U)U_i,X=F_i(U).
Start U^0(theta,X)=U0(X). Recursively solve the linear characteristic problem

    U_i^{j+1}(theta,X)=U0_i(Y_i^j(0;theta,X))
       +integral_0^theta F_i(U^j)(s,Y_i^j(s;theta,X)) ds,
    d_s Y_i^j=lambda_i(U^j)(s,Y_i^j), Y_i^j(theta)=X.      (4.1)

C1 coefficients with spatially Lipschitz derivatives give C1 flows with
Lipschitz spatial derivatives: their first Jacobian obeys
J'=lambda_X J, J(theta)=1, and differences of this ODE bound its Lipschitz
seminorm. Thus (4.1) preserves C1,1, including the original joins.

For completeness, fix bounds K>=2(||U0_X||+1), H>=2(Lip(U0_X)+1)
and an amplitude bound larger than ||U0||+1. With C a finite coefficient
bound, differentiation of the transport equation yields

    (partial_theta+lambda(U^j)partial_X)U_i,X^{j+1}
       =-(Dlambda_i(U^j) U_X^j) U_i,X^{j+1}+DF_i(U^j) U_X^j.

This bounds the next gradient by (||U0_X||+C K t)exp(C K t).
Differentiating once more a.e., or taking difference quotients along the flow,
bounds the next derivative-Lipschitz seminorm by

    [Lip(U0_X)+C t(H K+K^3+H+K^2)] exp(2 C K t).          (4.2)

Here terms containing the next seminorm have been absorbed in the exponential;
previous seminorms are <=H. Choose a positive t small enough to preserve K,H
and amplitude. This is only a finite-N starting time, so dependence on H is
allowed. It also preserves a prescribed small state displacement because
||U_theta||<=bounded_speed*K+bounded_source.

Subtract successive linear equations along the j-th flow. The forcing is
F(U^j)-F(U^{j-1})-[lambda(U^j)-lambda(U^{j-1})]U_X^j.
Consequently ||U^{j+1}-U^j||_{C0([0,t])}<=C t(1+K)
||U^j-U^{j-1}||_{C0([0,t])}. Further decrease t to make this factor <1/2.
Uniform convergence follows by summing a geometric series. If two functions
have gradient Lipschitz seminorm <=H, a finite difference of length h gives
|u_X-v_X|<=2||u-v||/h+Hh. Optimizing h shows derivative convergence.
Thus U^j converges in spatial C1, uniformly in theta; (4.1) and the PDE give
continuous time derivatives and the equation for the limit. The bound H
passes to its spatial gradients. This constructs spacetime C1/C1,1 U.

For two solutions, subtract along characteristics of the first. The difference
is bounded by a constant times the time integral of its sup, with the constant
depending on finite coefficients and the second solution's first gradient.
Iteration gives D(t)<=Dmax(Ct)^j/j! for every j, hence uniqueness. This proof
also works on the contained cones of Section 9. These steps derive a genuine
start and restart construction; real characteristic speeds alone would not.

## 5. Uniform block estimates and bounded local speed

Let K be the compact extended initial field range, and choose delta>0 such
that its closed 2delta neighborhood stays in g>0 and the chart, with
m/2<=g<=2M and chi in [chi_min-1,chi_max+1]. Also use
q_- -1<=q<=q_+ +1, where q_-,q_+ are initial extrema. On a slightly larger
cutoff neighborhood define finite dimensionless bounds

    Lambda>=max_i|lambda_i|, F>=max_i|H_i|,
    G>=||D_z g||, G2>=||D_z^2 g||, g_bar>=|g|,
    L1>=max_i||D_z lambda_i||, L2>=max_i||D_z^2 lambda_i||,
    K1>=max_i||D_(q,z)H_i||, K2>=max_i||D_(q,z)^2 H_i||.

Use induced max norms so vector sums below are covered by these constants.
These bounds are independent of N because the initial field extension is
fixed, q is controlled by transport, and field sources do not depend on v.
The amplitude cutoff of Section 4 can be chosen outside the fixed invariant
bound below. Define

    A=max(||r_X||,||s_X||), Bf=max_i||z_i,X||,
    A0<=a0 P, a0=C_v+c||q0_X||,
    B0=max_i||z0_i,X||,
    a1=2(a0+1), beta=2(B0+1+K1 a1/c).

Differentiating (2.4) along its ACTUAL characteristics gives

    A(theta)<=A0+integral_0^theta [A^2+G Bf] du,
    Bf(theta)<=B0+integral_0^theta
                    [L1 Bf^2+K1(Bf+A/c)] du.             (5.1)

In particular |v_X|<=A and |q_X|<=A/c. Each field derivative obeys
D_i z_i,X=-(Dlambda_i.z_X)z_i,X+H_i,q q_X+D_zH_i.z_X.
Pressure has already been retained in r,s, with fixed c, and no comparison
of characteristic speeds has been divided out. Also exactly

    (partial_theta+v partial_X)q=-v_X,
    ||z(theta)-z0||<=integral_0^theta (Lambda Bf+F)du.      (5.2)

Let Q0=||q0|| and set S=V_e+c Q0+g_bar+c+Lambda+1. Choose k=k_edge>0
no larger than

    1, 1/(2a1),
    (a1-a0)/[2(a1^2+G beta+1)],
    (beta-B0)/[2(L1 beta^2+K1 beta+K1 a1/c+1)],
    delta/[2(Lambda beta+F+1)],
    (R_o-R_i)/(2S), (R_i-r_*)/(2S).                       (5.3)

All constants are fixed, positive and finite. Bootstrap A<a1 P, Bf<beta,
q in (q_- -1,q_+ +1), and ||z-z0||<delta on a local solution. At theta<=k/P,
(5.1), using P>=1, strictly improves the first two bounds to

    A <= [a0+k(a1^2+G beta)]P < a1 P,
    Bf <= B0+k[L1 beta^2+K1 beta+K1 a1/c] < beta.          (5.4)

Material transport in (5.2) gives q_- -1/2<=q<=q_+ +1/2, and its field
line gives ||z-z0||<=delta/2. The auxiliary line has no spatial boundary.
The r,s source equations separately yield

    |r|,|s|<=V_e+c Q0+g_bar theta,
    |v|<=V_e+c Q0+g_bar for theta<=1.                    (5.5)

Every fluid, field and material speed is consequently strictly less than S.
This derives the speed gate from the actual momentum equations and field
bounds; it is not a local-speed assumption imposed on a full fast packet.
The state cutoffs stay inactive. Section 6 closes the endpoint in this
bootstrap, so these are estimates on actual constructed solutions.

## 6. Exact joins, higher derivatives, trace and restart

Set Hf=max(Lip(r_X),Lip(s_X)), Hz=max_i Lip(z_i,X). The twice-differentiated
fluid transport has terms -2v_X r_XX-v_XX r_X-g_XX, and similarly for s.
The field equation has -2lambda_i,X z_i,XX-lambda_i,XX z_i,X+H_i,XX.
Taking a.e. derivative bounds, or spatial differences of first-gradient flow
ODEs, gives

    Hf <= Hf0+integral [3A Hf+G Hz+G2 Bf^2],
    Hz <= Hz0+integral [(3L1 Bf+K1)Hz+(K1/c)Hf
                            +L2 Bf^3+K2(Bf+A/c)^2].      (6.1)

To justify these at a join, the flow separation solves
(X1-X2)'=lambda(X1)-lambda(X2). Divide the difference of first-gradient
ODEs by this separation; its logarithmic derivative supplies one of the
transport-gradient terms. Its coefficient is bounded by ||lambda_X||.
Integrating the resulting difference-quotient inequalities gives (6.1) for
the continuous first gradients and their Lipschitz seminorm, without assigning
any classical f'' at the join. The a.e. formulas have the same bounds.

From (3.5), Hf0+Hz0<=h0 P^2 with fixed h0. On (5.4) choose constants E,D0
so the sum inequality is

    Hf+Hz <= h0 P^2+integral [E P(Hf+Hz)+D0 P^2].

For example E=3a1+G+3L1 beta+K1+K1/c and
D0=G2 beta^2+L2 beta^3+K2(beta+a1/c)^2, enlarged if needed, work.
Iteration of the scalar integral inequality gives

    Hf+Hz <= [h0 P^2+D0 P^2 theta]exp(E P theta)
           <= C_H P^2, C_H=(h0+D0 k)exp(E k).             (6.2)

This retains the exact initial O(N^7) seminorm while allowing k N^-7/2.
For each fixed N, all quantities in

    (U_i,X)_theta=-lambda_i U_i,XX
                   -(Dlambda_i.U_X)U_i,X+DF_i.U_X        (6.3)

are bounded a.e. by finite constants, uniformly up to any putative endpoint
<=k/P; speeds are bounded by S. Hence both U and U_X are uniformly Lipschitz
in time in the sup norm. Integrate (6.3) distributionally, then use continuous
spatial representatives. U and U_X have uniform endpoint limits; integration
in X identifies the limit derivative, and the Lipschitz bound (6.2) passes
to it. The strict q/chart margins and finite amplitudes persist.

Apply the construction of Section 4 to that precise C1,1 endpoint trace,
with its compatible potentials as verified in Section 7. Uniqueness glues
the restart. The restart time may depend on N; this does not matter since
no finite endpoint <=k/P can obstruct extension. The union of the locally
unique intervals and the strict improvements proves existence through k/P
(and briefly beyond for each N). No unproved high-norm restart criterion,
no smoothing, and no imported FGF048 time coefficient is used here.

## 7. Constraints, matter compatibility and the source

Taking sum/difference of the Z equations gives k_theta=w_X and
w_theta=d^2 k_X+D_s. With chi_theta=w, initial chi_X=k propagates exactly.
Before imposing that constraint, subtraction of the R equations gives

    2b(g_theta-p_X)+2h_chi chi_theta=2h_chi w,

so g_theta=p_X because chi_theta=w and b>0. Their sum gives

    p_theta=b^2 g_X+A_s+b h_chi(chi_X-k).                  (7.1)

The last term vanishes by the already propagated scale constraint.
Define phi=phi0+integral_0^theta p du. Then phi_X=g and phi_theta=p.
Thus (7.1) says exactly

    B_X=C exp(q)+tau phi_thetatheta.                      (7.2)

Adding/subtracting the fluid pair yields
v_theta+v v_X+c^2 q_X=-g and q_theta+v q_X=-v_X, hence continuity with
n=exp(q)>0. These are all actual equations (2.1). Chart smoothness and the
C1 solution give C2 potentials. At an endpoint the constraints pass by C1
convergence, and phi has its own compatible continuous trace, so every
restart satisfies the same constraints. No fixed-field source substitution
or replacement of the dynamic MOND density by a Newtonian missing mass occurs.

## 8. Quantitative density, field and adverse-gradient estimates

On the auxiliary branch and hence on its physical cone,

    exp(q_- -1/2)<=n<=exp(q_+ +1/2),
    a_ref exp(chi_min-1)<=a<=a_ref exp(chi_max+1),
    m/2<=g<=2M, Bf<=beta, |v_X|<=a1 P.                   (8.1)

Here n is normalized; multiply by nref for physical density. We have
|q_X|<=a1 P/c and a sharper time-dependent bound: differentiating the exact
q equation yields D_v q_X=-v_X q_X-v_XX. Consequently

    ||q_X(theta)|| <= [Q1+C_H P^2 theta]exp(a1 P theta),
    Q1=||q0_X||,
    ||n_X(theta)||<=n_bar [Q1+C_H P^2 theta]exp(a1 k),
    n_bar=exp(q_+ +1/2).                                 (8.2)

Also |q_theta|<=|v||q_X|+|v_X|<=C_qt P for fixed C_qt, so at a fixed X
|q(theta,X)-q0(X)|<=C_qt P theta. This supplies an actual same-point density
change O(N^-1/2) on theta=B_* N^-4, with fixed B_*.

Since g_theta=p_X and p=(R_++R_-)/2,

    ||g(theta)-g0||<=beta theta.                          (8.3)

For a derivative refinement insert Hf<=C_H P^2, Bf<=beta and
|q_X|<=a1 P/c in the second line of (6.1). With

    E_z=3L1 beta+K1,
    D_z=(K1/c)C_H+L2 beta^3+K2(beta+a1/c)^2,

it follows that

    Hz(theta)<=[Hz0+D_z P^2 theta] exp(E_z theta).

Differentiate g-g0=integral p_X in the weak spatial sense and use continuity
of g_X-g0_X. Since Lip(p_X)<=Hz,

    ||g_X(theta)-g0_X||
       <=exp(E_z k)[Hz0 theta+(D_z/2)P^2 theta^2].        (8.4)

On the full edge horizon the RHS is O(1); on the fixed comparison horizon
Theta_N=B_* N^-4 it is

    <=exp(E_z k)[Hz0 B_* N^-4+(D_z/2)B_*^2 N^-1].        (8.5)

This is NOT inferred by extending an FGF048 estimate beyond its old kappa;
(8.4) holds on the newly constructed, smaller-spatial-domain interval.
At the comparison horizon (8.2) gives ||n_X||=O(N^3) since P^2=N^7.
Field chart Jacobians satisfy exp(-L1 beta theta)<=j_i<=exp(L1 beta theta)
for terminal-label Jacobians; both Q paths and their scale terms are controlled.
No resonance denominator is present anywhere in these estimates.

Let M_-=sup(-g0_X)_+ on the fixed original background neighborhood. On D_e(theta)
or on either protected inner interval, (8.4) yields the actual local budget

    integral_0^Theta sup(-g_X)_+ dtheta
       <= M_- Theta+exp(E_z k)[Hz0 Theta^2/2
                                         +D_z P^2 Theta^3/6]              (8.6)

for every 0<=Theta<=k/P. At Theta_N this is

    <= M_- B_* N^-4
       +exp(E_z k)[Hz0 B_*^2 N^-8/2+D_z B_*^3 N^-5/6].    (8.7)

The local force impulse is <=2M Theta, or the sharper integral of |g0|+beta theta.
The sign convention is deliberate: an actually favorable g_X>=0 contributes
zero; bounding by (8.6) is sufficient but can overestimate a positive gradient.

Restore g units v0^2/L, g_x units v0^2/L^2, and time L/v0. Thus multiply
(8.3) by v0^2/L, (8.4)-(8.5) by v0^2/L^2, (8.6)-(8.7) by v0/L, and the
force-impulse bound by v0. Physical density gradients multiply (8.2) by nref/L.
In particular the edge adverse integral through T_N is O((v0/L)N^-4),
and force impulse is O(v0 N^-4). These are far smaller than the FGF049 budgets
eta*(v0/L)N^4 and Gamma*v0 N for fixed positive eta,Gamma, BUT ONLY on the
edge domains. Supremum on the whole cone cannot be replaced by either local
supremum or their union.

## 9. Buffer, exterior independence and matching to a whole branch

In dimensionless variables put

    D_e(theta)=[X_e-R_o/P+S theta, X_e+R_o/P-S theta].     (9.1)

Every backward characteristic of the constructed branch from D_e(theta)
stays in D_e(u) at earlier u: its displacement is at most S(theta-u), and
its endpoints recede at precisely that enclosing speed. The strict speed
bound leaves a strict characteristic margin. Vertical reconstruction paths
are also contained. By (5.3), S theta<=(R_o-R_i)/(2P), so (9.1) contains
the full fixed inner interval [X_e-R_i/P,X_e+R_i/P]. Any characteristic
of speed at most S issued from an initial root |X-X_e|<=r_*/P obeys
|X(theta)-X_e|<=[r_*+S k]/P<R_i/P; continuation of that path inside the
cone is therefore legitimate for the full local time. This proves persistence
of the initial labeled paths, not confinement of the future zero set of a
relative-speed function.

The apparent danger is high-speed core data outside D_e(0). The following
uniqueness argument addresses it without assuming that a global branch already
has speed S. Let U be the constructed branch and V any other positive C1
solution of the same equations on a neighborhood of the closed cone, agreeing
with its original initial data on D_e(0). Chart V is valid on this compact
cone, with finite gradient and compact positive state range, possibly with
N-dependent bounds. Extend coefficient functions smoothly over a compact
set containing both ranges. Along U's i-th characteristics,

    D_i^U(U_i-V_i)=F_i(U)-F_i(V)
                         -[lambda_i(U)-lambda_i(V)] V_i,X.              (9.2)

Those U paths remain in the cone regardless of V's putative exterior speed.
The sup difference D(theta) over D_e(theta) therefore satisfies
D(theta)<=C_V integral_0^theta D(u)du, where C_V is finite for this fixed N
and comparison interval. Its zero initial value and the iterated factorial
bound of Section 4 force D=0. In particular V's speeds inside the cone
become the bounded U speeds as a consequence. This is why fast incoming core
data cannot penetrate this particular region while V remains classical on it.
No unproved bounded speed for V was needed; no lateral boundary values were
specified. If V exists only to t'<k/P, apply this on each compact common
subcone up to t'. This matches to the existing whole-packet germ without
asserting its later existence.

The same proof compares any two auxiliary extensions on a common contained
cone. One convenient fixed cutoff supplies uniform constants; arbitrarily
large unrelated extension norms are not claimed to share those constants.
The local physical restriction solves exactly the unchanged data (1.1).
The two edge constructions are disjoint for large N and require no artificial
interface; merging them with a future core solution is a separate problem.
For fixed B_*, the gate N>=(B_*/k)^2 ensures Theta_N<=k/P. The larger buffer
survives even at the full edge time; at Theta_N its loss S B_* N^-4 is only
O(N^-1/2) of its original N^-7/2 width.

## 10. Energy, moving boundaries and exact zero-velocity control

Return to physical notation in this section. With

    e(n)=cs^2 n[log(n/nref)-1],
    E=nv^2/2+e+n phi
       +[tau p^2/2+W+sigma w^2/2+J k^2/2+U_s]/C,
    F_E=nv[v^2/2+cs^2 log(n/nref)+phi]-(pB+Jwk)/C,       (10.1)

the fluid momentum/continuity equations give the kinetic-plus-internal
balance with source -nvg. Adding interaction n phi gives +np.
For the Q part use W_t=B g_t-Tw=B p_x-Tw and tau p_t=B_x-Cn;
its balance has flux -pB/C and source -np-Tw/C. The scale equation multiplied
by w, with k_t=w_x, gives flux -Jwk/C and source +Tw/C. Thus

    E_t+(F_E)_x=0.                                      (10.2)

Both field fluxes and both interaction cancellations are required. The C1
state/C2 potential regularity already proved suffices for these pointwise
identities. For moving endpoints alpha(t),beta(t) in a physical edge cone,

    d/dt integral_alpha^beta E dx
       =F_E(alpha)-F_E(beta)+beta' E(beta)-alpha' E(alpha).              (10.3)

For (1.2), alpha'=v0 S, beta'=-v0 S, so the boundary energy term is
-v0 S[E(beta)+E(alpha)]. No conserved shrinking-cone energy, global energy
coercivity or removal of pressure work is asserted. The edge initial kinetic
excess is O(N^-7/2) because v is bounded there; the full packet's different
O(N^-1) kinetic excess is not used to bound gradients.

For the exact control replace (1.1)'s velocity by zero while keeping the same
hydrostatic data. The stationary tuple solves continuity trivially, momentum
by cs^2(log rho)_x=-g0, the Q equation by B0_x=C rho, and the scale equation
by its full third relation in (2.2), including chi0_xx and T. It has p=w=0,
zero full flux and exact stationary energy. The diagonal R equations still
contain nonzero h_chi k terms when chi0_x!=0; those are accounted for by the
chain rule in (2.4). Local uniqueness identifies the constructed restriction
with this exact stationary tuple. Auxiliary nonhydrostatic extensions cannot
affect the control on the common domain. Pressure is essential to this check.

## 11. Framework branches and limitations

Repeat this argument separately for a_ref=9.3619e-11 and 1.1279e-10 m/s^2,
with each one's compatible background and constants; both are positive, so
each gives k>0. Taking a minimum is permitted for this finite pair if a common
lower coefficient is wanted, but equality of their backgrounds is not assumed.
The adopted relation a_ref=kappa_vac c_light sqrt(G_Newton rho_Lambda,ref)
is an input, not derived here. Its pressure form a_ref^2=kappa_vac^2 G(-p_vac)
equals it only for p_vac=-rho_Lambda,ref c_light^2. The dynamic diagnostic
chi field does not by itself prove any physical pointwise vacuum relation.

Constant vacuum and a separately frozen a_ref=a0 E(z), with
E(z)^2=.315(1+z)^3+.685, are distinct histories. Every individually fixed
positive reference fits the proof with its own compatible background.
An evolving reference is outside this autonomous theorem: if
alpha_ref=d(log a_ref)/dt, W_t acquires -T alpha_ref in addition to -Tw,
so (10.2) becomes E_t+(F_E)_x=-T alpha_ref/C for the otherwise same equations.
The chart also acquires explicit reference-time terms. No conservation or
uniform-time result for that evolving protocol is silently asserted.

The full dynamic MOND source (7.2) and all source scaling remain intact.
The Q law F=sqrt(B^2+aB) is distinct from RAR
F=B/[1-exp(-sqrt(B/a))], registered M and filtered MONO. Nothing here proves
physical vacuum/metric/photon/two-gravitational-DOF completion, criterion B,
calibrated observations, cosmology, stability, historical novelty or closure.
No literature mechanism has been imported.

The bounded local target is supported by an actual construction. Still open:
control in the fast core, bounds for future resonance creation/migration,
interface/matching estimates on a complete domain, the full-cone feedback
supremum and any actual compression upper lifespan or endpoint classification.
A local lifespan exceeding B_* N^-4 does not settle any of those claims.
