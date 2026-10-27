# FGF054 independent finite-velocity gate

Reviewer `/root/fgf054_reviewer`. Independent proof frozen before exposure to any
new FGF054 author proof, result, preview, or stage41 root proof. Ten task ancestry
pins matched before ancestry use. Old accepted proofs supply the exact system and
local C1,1 construction; this finite-V argument is newly reconstructed. No
mathematical executable computation, external theorem, literature mechanism,
coefficient retuning, or shock classification is used. Hash checks are metadata.

## Claim card and fixed units

Fix all positive physical coefficients C=4pi G, tau,sigma,J,S0,cs,nref,a_ref,
and a smooth compatible hydrostatic background on U about x*. Fix L,u>0
independently of epsilon, once and for all. Set X=(x-x*)/L, t=u t_phys/L,
n=n_phys/nref, v=v_phys/u, phi=phi_phys/u^2, g=g_phys L/u^2,
p=p_phys L/u^3, w=w_phys L/u, k=L k_phys. Coefficients become
c=cs/u, tau_hat=tau u^2, sigma_hat=sigma/u^2, J_hat=J/u^4,
C_hat=C nref L^2/u^2, a_ref_hat=a_ref L/u^2, S0_hat=S0 L^2/u^4.
Suppress hats. V=V_phys/u, e=epsilon/L; all constants below are independent of e.
They may depend on the fixed V, c, physical coefficients, background and units.

The actual equations, with q=log n and a=a_ref exp chi, are

    q_t+v q_X+v_X=0,  v_t+v v_X+c^2 q_X=-g,
    g_t=p_X, tau p_t=B_g g_X+B_chi k-C exp q,
    k_t=w_X, sigma w_t=J k_X+T-U', chi_t=w,
    B=(sqrt(a^2+4g^2)-a)/2, W=int_0^g B(s,a)ds,
    T=-W_chi, U=S0[cosh(2chi)-1]/4.

Background H has v=p=w=0, n=rho>0, g=g0>0, and
B0_X=C rho, c^2(log rho)_X=-g0, J chi0_XX+T0-U'(chi0)=0.
Initial n and fields are exactly H; v=V f(X/e), with f=(1-y^2)^2 on
|y|<1 and zero elsewhere. Its joins remain exactly C1,1.

Fix a compact background interval [-R,R] inside U. Let

    S_H=max(c, tau^(-1/2), sqrt(J/sigma))>0.

This encloses every characteristic speed of H (and the field speeds wherever
g>0). A conservative explicit conditional cell is

    Vmax > 20 S_H,       20 S_H <= V < Vmax.                (C)

For every fixed coefficient/background tuple and V in this cell there is e0>0
such that, for 0<e<e0, the same compatible classical whole-packet germ has

    kappa e/V <= T_e <= 8 e/V,

and on every existing slab below its upper horizon it has positive density,
a compact positive field chart, and |v|<Vmax. Constants and e0 may be very
poor when V/c is large. This is a nonempty conditional mathematical cell,
not a claim that supplied physical parameters or a light-speed ceiling obey (C).
Restoring time multiplies by L/u: the bounds are kappa epsilon/V_phys and
8 epsilon/V_phys. No endpoint type or physical metric conclusion is asserted.

## Exact chart and why old rescaling fails

Set b=sqrt(B_g/tau), d=sqrt(J/sigma), h_g=b with fixed lower integration
limit g*>0, r=v+cq, s=v-cq, R+=p+h, R-=p-h, Z+=w+d k,
Z-=w-d k, z=(R+,R-,Z+,Z-,chi). For g>0 this is a smooth invertible chart.
The exact characteristic equations are

    D_(v+c) r=-g, D_(v-c) s=-g,
    D_-b R+=B_chi k/tau+h_chi(w-bk)-Cn/tau,
    D_+b R-=B_chi k/tau-h_chi(w+bk)-Cn/tau,
    D_-d Z+=D_+d Z-=(T-U')/sigma, chi_t=w.             (1)

Thus z_i,t+lambda_i(z)z_i,X=H_i(q,z), with no v or derivatives in field
sources. Every scale and density term remains. The constraints chi_X=k,
g_t=p_X and phi_X=g propagate from compatible data; addition of the Q pair
gives p_t=b^2g_X+B_chi k/tau-Cn/tau+b h_chi(chi_X-k).

Replacing v0 by V_phys/N in old FGF053 changes c=cs/v0 and every dimensionless
coefficient and chart constant. Its old fixed constants and N thresholds are
not uniform under that substitution. More geometrically, e=N^-3 would give
a time O(e/V)=O(N^-3), while the old collar N^-7/2 is now smaller than the
O(N^-3) acoustic/field travel. Neither its collar margin nor its threshold
survives. Here e and V are independent physical inputs in fixed units.

## Genuine stationary collars and physical germ

Take I=[A,D]=[-2e,2e]. About each endpoint take the hydrostatic comparison cone
with initial half-width 3e/4 and inward speed S_H. Initially these cones lie
strictly outside [-e,e]. At t<=Theta=8e/V, (C) gives

    S_H t <= 2e/5,
    3e/4-S_H t >= 7e/20 > e/4.                       (2)

Therefore each cone contains an open fixed collar of radius e/4 throughout
the comparison interval. They and I lie inside [-R,R] when 3e<R.

These collars are forced by uniqueness, not by a wall. For any existing
positive C1 candidate U on the cones, compare it to known H along H's
characteristics, all contained in earlier cones. Subtracting diagonal equations
gives a sup difference bounded by its time integral times a finite constant
on each existing compact slab. The constant uses U's actual bounded gradient;
it need not be uniform as an endpoint is approached. Zero initial difference
and iterated integration give U=H. This requires no assumed global bound on
U's propagation speed. Potentials agree too: p=w=0 and the initial gauges agree.

Restrict any physical solution to I plus those open collars and glue to H on
the remainder of (-R,R). Equality on open overlaps makes an exact classical
solution, with no artificial wall equation. Define admissible segments this way,
with the original C1/C1,1 regularity and initial data, initially allowing times
less than Theta0=9e/V. The same collar calculation at Theta0 gives
3e/4-9e/20=3e/10>e/4, so its bookkeeping cap also has positive margin.
Uniqueness follows by stopping characteristics at their first initial or
lateral contact, where both admissible solutions have equal data. The union
of all such segments is a unique intrinsic germ. Comparison above means an
actual whole-packet continuation on the same cones patches into this germ;
its lifespan is not the lifespan of an arbitrary distant extension.

All amplitude estimates below may use Theta0, replacing 8 by 9 in constants.
The moment upper bound uses Theta=8e/V, leaving the artificial cap inactive.

## Actual lower interval, not an imported high-N constant

Choose one compatible smooth extension of the background, equal to H near
[-R,R], with g bounded below. Set P=V/e>=1. In a fixed field chart and
q-neighborhood q_- -1<=q<=q_+ +1, use FGF048's coefficient bounds
Lambda,F,G,G2,L1,L2,K1,K2 for field speeds, sources and their first/second
state derivatives. They are fixed in e. Let B0=max_i||z0_i,X||,
a0=8/(3sqrt(3))+c||q0_X||, a=2(a0+1),
beta=2(B0+1+K1 a/c). Differentiating the actual equations gives

    A(t)<=a0 P+int_0^t(A^2+G Bf),
    Bf(t)<=B0+int_0^t[L1 Bf^2+K1(Bf+A/c)],             (3)

where A=max(||r_X||,||s_X||), Bf=max_i||z_i,X||. Also D_v q=-v_X and
||z(t)-z0||<=int(Lambda Bf+F). Choose kappa positive and at most

    1, 1/(2a),
    (a-a0)/(2(a^2+G beta+1)),
    (beta-B0)/(2(L1 beta^2+K1 beta+K1 a/c+1)),
    delta/(2(Lambda beta+F+1)), R/(4 S), 1/2,

where delta is a fixed chart margin and S is a fixed speed bound exceeding
V+c||q0||+gbar+c+Lambda+1. At t<=kappa/P, bootstrap A<aP,Bf<beta,
|q-q0 along material paths|<1 and ||z-z0||<delta strictly improves to
A<aP,Bf<beta, q_- -1/2<=q<=q_+ +1/2, ||z-z0||<=delta/2.
The acoustic invariants bound all speeds by S. The fixed physical backward
cone [-R+St,R-St] contains [-3R/4,3R/4]; for small e it contains I and its
comparison collars.

For precision the local construction is the inherited characteristic iteration,
not merely an invocation of hyperbolicity. Its endpoint extension applies here
because the actual difference-quotient inequalities are

    Hf<=Hf0+int[3A Hf+G Hz+G2 Bf^2],
    Hz<=Hz0+int[(3L1 Bf+K1)Hz+(K1/c)Hf
                         +L2 Bf^3+K2(Bf+A/c)^2].       (4)

The exact joins give Hf0+Hz0<=h0 P^2 with fixed h0 depending on V through
8/V. Under (3), (4) gives Hf+Hz<=const P^2 through kappa/P. For each
fixed e these are finite; the PDE and its weak spatial derivative give actual
uniform C1 time traces. Their gradients stay Lipschitz, positive margins are
strict, and compatibility passes to the trace. The same characteristic
iteration restarts it, so no endpoint before kappa/P can stop the branch.
Open stationary collars allow patching into precisely the germ above. Hence
the lower bound is derived with fresh fixed-V constants.

## Full-horizon source, positivity, and evolved speed ceiling

The following is an a priori estimate on EVERY existing truncated segment,
not an assumption of survival to the upper horizon. Put z*=z0(0), q*=q0(0),
and choose a fixed compact chart ball |z-z*|<=2delta in g>0. Bootstrap
|z-z*|<delta. Let Gbar bound |g| there; let Q1 bound |q0_X| and Z1
bound max_i|z0_i,X| on the background interval. Choose

    Delta=min(1,(Vmax-V)/2)>0,
    D_e=2c Q1 e+Gbar (9e/V),
    e <= Delta/(2c Q1+9 Gbar/V).                        (5)

Initial or lateral data on I obey |q0-q*|<=2Q1 e. Stop every acoustic
characteristic at its first initial or lateral contact. In (1) this gives,
with rtilde=r-cq*, stilde=s+cq*,

    -D_e <= rtilde,stilde <= V+D_e,
    -D_e <= v <= V+D_e,
    |q-q*| <= V/(2c)+D_e/c.                            (6)

Thus |v|<=V+Delta<Vmax (if Delta uses the half margin, strictness follows
from V+Delta<Vmax), and

    exp(q*-V/(2c)-Delta/c) <= n
                 <= exp(q*+V/(2c)+Delta/c).             (7)

These positive finite bounds are UNIFORM in e, although exponential in V/c.
They control the actual density source -Cn/tau. Let Fbar bound every complete
H_i(q,z) on this q interval and the doubled chart, including chi_t=w.
Integrating each field characteristic from its first initial/lateral contact
(or vertically for chi) gives

    max_I |z(t)-z*| <= 2Z1 e+Fbar t
                    <= (2Z1+9Fbar/V)e.                 (8)

Choose e<delta/[2(2Z1+9Fbar/V)] (omit an irrelevant zero denominator).
This strictly improves the chart bootstrap. By first-exit reasoning, (6)-(8)
hold on the full proposed comparison interval for every candidate continuation
and hence up to the actual earlier maximal time. They give positive g,a,
bounded p,w,k,chi, and the evolved matter speed margin. Density gradients
are not asserted bounded at the maximal time. No force is frozen and no
field gradient/source derivative cancellation is claimed.

Outside I the admissible germ is exactly H. The comparison plus gluing
argument makes these whole-germ amplitude bounds physical on the local patch.
The only speed ceiling certified is the stated matter ceiling in this scalar
fluid model; neither c nor S_H is identified with light speed.

## Moment contradiction with all pressure and transfer terms

At fixed A,D the forced hydrostatic collars imply v=p=w=0, n=rho,
phi=phi0, chi=chi0. Thus M=int_I n=int_I rho is conserved. Let
P=int_I n v and I1=int_I Xn. Actual continuity and momentum give

    I1'=P,
    P'=-[nv^2+c^2 n]_A^D-int_I ng
      =int_I(rho g0-ng),                               (9)

where c^2 rho_X=-rho g0 was used. Pressure stress is retained, not zeroed.
Therefore |P(t)-P0|<=M(Gbar+G0)t, where G0 bounds |g0|. Positivity requires
I1(t)<D M, whereas (9) gives

    I1(Theta)>=I1(0)+P0 Theta
                         -M(Gbar+G0)Theta^2/2.          (10)

For an explicit finite-e margin, choose e so |rho(X)/rho*-1|<=eta=1/100
on I, rho*=rho(0)>0. Exact integral int_-1^1 f=16/15 implies

    P0 >= (1-eta)rho* V e (16/15),
    D M-I1(0)=int_I(2e-X)rho <= 8(1+eta)rho* e^2.

At Theta=8e/V their difference is at least

    [(128/15)(99/100)-8(101/100)]rho*e^2
                           =(46/125)rho*e^2.           (11)

Since M<=4(1+eta)rho*e, the error term in (10) is at most
128(1+eta)rho*(Gbar+G0)e^3/V^2. Taking additionally

    e < V^2/[1280(1+eta)(Gbar+G0)]                       (12)

makes that error less than rho*e^2/10, strictly below (11). This is the
contradiction: no positive classical whole-packet continuation reaches
Theta. The lower construction and this upper contradiction concern the SAME
germ and original data. Conditions (2),(5),(8),(11),(12), P>=1 and the
fixed outer buffer give a nonzero e0 in every fixed cell (C).

For explicit field momentum accounting set
Fmom=-int_I(tau p g+sigma w k)/C. Direct differentiation gives

    d_t[-(tau p g+sigma w k)/C]
       =ng-(1/C) d_X[gB-W+tau p^2/2+Jk^2/2+sigma w^2/2-U].

Together with matter momentum this is a local total momentum conservation
law. Hydrostatic total stress is spatially constant, so its endpoint values
cancel and P+Fmom=P0, Fmom(0)=0. Consequently (10) is precisely the
integrated ACTUAL field-transfer estimate, not a fixed-force approximation.
No moving boundary is used. If one were used, mass and momentum would gain
beta' n(beta)-alpha' n(alpha) and beta' nv(beta)-alpha' nv(alpha), respectively;
the proof does not silently discard these terms.

## Energy, controls, scope and smallest remaining implication

With e_internal=c^2 n(log n-1), the complete autonomous local energy is

    E=nv^2/2+e_internal+n phi
                  +[tau p^2/2+W+sigma w^2/2+Jk^2/2+U]/C,
    F_E=nv[v^2/2+c^2 log n+phi]-(pB+Jwk)/C.

Matter plus interaction supplies +np, Q supplies -np-Tw/C, scale supplies
+Tw/C. Thus E_t+(F_E)_X=0 with both field fluxes. Fixed hydrostatic endpoint
fluxes vanish. A moving integral has the additional exact contribution
beta' E(beta)-alpha' E(alpha); no shrinking-cone energy is called conserved.
No coercive global energy estimate is used. At V=0, H is the exact solution,
P0=P=Fmom=0 and F_E=0. The contradiction depends on positive P0 and does
not apply; formulas with 1/V are explicitly excluded from that negative
control. The original C1,1 joins, pressure and scale coupling are unchanged.

Repeat separately for a_ref=9.3619e-11 and 1.1279e-10 m/s^2 with their own
compatible backgrounds and constants. Constant vacuum and each individually
frozen a0 E(z), E^2=.315(1+z)^3+.685, are separate autonomous choices.
Evolving reference is excluded. The adopted a_ref=kappa_vac c_light sqrt(G
rho_Lambda) is not derived; the dynamic diagnostic chi does not prove physical
vacuum closure. Q, RAR, registered M and operative filtered MONO remain
distinct, and all actual source formulas retain the Q/MOND scaling.

The sufficient cell is deliberately conservative. Failure of Vmax>20S_H
means this particular parameter gate has not been certified, not failure of
the PDE or core framework. A sharper collar/moment optimization or a separate
mechanism could cover other cells, but is unnecessary to this bounded result.
No full shock classification, physical metric/photon/two-DOF completion,
criterion B, cluster calibration, cosmology or historical novelty follows.
The next physical implication would be checking whether an independently
justified coefficient/background tuple and matter ceiling intersect this
conditional cell; no such physical justification is supplied here.

Dependency graph: pinned FGF048 exact equations, characteristic local
construction and difference-quotient restart -> fresh fixed-V lower bound;
pinned FGF051 known-solution cone uniqueness -> fresh O(e) collars;
(1) plus bounded finite V -> (6)-(8) actual sources and evolved ceiling;
pressure-retaining (9), finite-e estimates (11)-(12) -> upper horizon.
No external theorem or executable computation leaf is present.

Provisional independent verdict: proved as written within the explicit
conditional cell (C), subject to subsequent adversarial audit. This frozen
reconstruction is not a review of the still-unseen FGF054 author artifacts.
