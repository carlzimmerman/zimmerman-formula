# FGF052 independent derivation, frozen before new author exposure

Reviewer: `/root/fgf052_reviewer`. Proof-only, zero mathematical executable computations. This derivation was written from the actual equations in hash-verified FGF048/049/051 ancestry and the FGF052 task; no new FGF052 author proof, coordinator proof or preview was read. Source hashing is metadata verification, not mathematical computation. All ten task ancestry pins matched before source use. This is an independent derivation of the critical implication, not independent rediscovery of the accepted FGF051 local existence theorem.

## Claim card and verdict

Fix all positive physical coefficients C=4 pi G_Newton, tau,sigma,J,S0,cs,nref,L,v0,a_ref independently of N. Fix a smooth compatible hydrostatic background on a fixed neighborhood of x*, with rho,g0>0. Initial n=rho, phi=phi0, chi=chi0, phi_t=chi_t=0 and v=V f((x-x*)/ell), V=v0 N, ell=L N^-3, f=(1-y^2)^2 on |y|<1 and zero outside, with its exact C1,1 joins. A positive classical whole solution means n,v,g,p,k,w,chi are C1, potentials C2, n,g,a>0, on a neighborhood of the interval and the local comparison cones for the times used. No existence through the proposed horizon is assumed as an established fact.

The normalized claim is: for every fixed B_dagger>0, fixed endpoints can be chosen just outside the initial packet with exactly hydrostatic traces through T=B_dagger ell/V for all sufficiently large N, on any such hypothetical whole solution. Exact integral balances yield a contradiction through T if its signed, time-integrated field momentum is less than P0 T minus the available first-moment capacity. For B_dagger>15/8 that capacity permits a fixed fractional budget. The actual-family verdict is **conditional on the named input: the signed matter-to-field transfer budget below**. The conditional implication and traces are derived; the actual evolution budget remains unproved.

## 1. Actual equations and protected traces

Write c=cs, g=phi_x,p=phi_t,k=chi_x,w=chi_t, a=a_ref exp chi, and

    B(g,a)=(sqrt(a^2+4g^2)-a)/2,
    W(g,a)=integral_0^g B(s,a) ds,
    Tscale=-W_chi, Us=S0(cosh(2chi)-1)/4.

The exact equations are

    n_t+(nv)_x=0,
    v_t+v v_x+c^2(log(n/nref))_x=-g,
    tau p_t=B_x-Cn, g_t=p_x,
    sigma w_t=J k_x+Tscale-Us', k_t=w_x, chi_t=w.

Hydrostatics obey B0_x=C rho, c^2 rho_x=-rho g0 and J k0_x+Tscale0-Us'=0. All scale and dynamic Q sources are retained.

Use accepted FGF051 constants R_i<R_o,S,k_edge in X=(x-x*)/L, theta=v0t/L. Its local solution is defined on |X-X_e|<=R_o N^-7/2-S theta, through k_edge N^-7/2, and includes the fixed R_i strip. Choose a fixed 0<d<R_i and r>0 with r<min(d,R_i-d)/2. Set h_e=L N^-7/2 and

    a=x*-ell-d h_e, b=x*+ell+d h_e.

At a and b take exterior subcone bases of radius r h_e, entirely outside the original support and inside the fixed edge strip. Their shrinking radii are r h_e-v0 S_h t, where S_h exceeds both the local edge speed bound S and the hydrostatic characteristic speeds. For fixed B_dagger, v0 S_h T/(r h_e)=(S_h B_dagger/r)N^-1/2 tends to zero, and T/(k_edge L N^-7/2/v0)=(B_dagger/k_edge)N^-1/2 tends to zero. Thus the endpoint vertical lines have a positive exterior subcone buffer for the entire proposed horizon.

Compare the stationary hydrostatic diagonal state U0 to the constructed edge state U on each exterior subcone. Their initial data agree identically. Along characteristics of the bounded comparison state, the difference solves a homogeneous Lipschitz system with coefficient-difference times the other solution's finite first derivative. Its sup D(t) is bounded by K integral_0^t D(s)ds; iterating gives D(t)<=Dmax(Kt)^j/j! for every j and hence D=0. This is local uniqueness, not a smallness approximation. FGF051's one-sided comparison with any whole classical branch identifies the edge state with that branch on the common cone, without imposing an a priori O(1) whole-branch speed. Therefore n=rho,v=0,g=g0,p=0,chi=chi0,k=k0,w=0 at both endpoints and in neighborhoods. Integrating phi_t=0 with the original phi0 fixes phi itself there. Bounded edge traces alone would not prove this.

## 2. Momentum densities, stresses and signs

Let brackets mean [H]=H(b)-H(a). Multiplying fluid momentum by n and using continuity gives

    (nv)_t+(nv^2+c^2 n)_x=-ng.

Define Q and scale momentum densities and their stresses by

    mQ=-tau p g/C,
    SQ=(tau p^2/2+gB-W)/C,
    mS=-sigma w k/C,
    SS=(sigma w^2/2+J k^2/2-Us)/C.

Since W_x=B g_x-Tscale k,

    (mQ)_t+(SQ)_x=ng+Tscale k/C,
    (mS)_t+(SS)_x=-Tscale k/C.

For example (gB-W)_x=g B_x+Tscale k, so the sign of the Q-scale exchange is positive in the Q equation. The scale potential enters its stress with a minus sign. Thus

    (nv+mQ+mS)_t+(nv^2+c^2n+SQ+SS)_x=0.

No n phi momentum term is needed: interaction is n phi in energy and -ng in matter momentum; the actual Q equation transfers exactly the opposite ng to the combined fields. Omitting scale exchange or pressure breaks the control.

On a fixed interval define mass M=int n, centered first moment I=int(x-x*)n, matter momentum P=int nv and field momentum F=int(mQ+mS). Before applying traces the exact balances are

    M'=-[nv],
    I'=P-[(x-x*)nv],
    P'=-[nv^2+c^2n]-int ng,
    (P+F)'=-[nv^2+c^2n+SQ+SS].

With the proved traces M is constant and I'=P. In hydrostatics (SQ0+SS0)_x=rho g0 and (c^2rho)_x=-rho g0, so the total stationary stress is constant. Consequently

    P+F=P0, F(0)=0,
    P'= -D(t), F'=D(t),
    D(t)=int_a^b (ng-rho g0)dx.

The pressure difference need not vanish: -c^2[rho]=int rho g0. It cancels the background force only. The two field boundary stresses need not individually cancel; their sum plus pressure does. In particular matter momentum is not conserved.

## 3. Explicit initial integrals and errors

Set rho*=rho(x*), delta=d h_e and H=ell+delta, so width b-a=2H=2ell(1+d N^-1/2). Smoothness gives uniform background derivative constants on the fixed patch. Direct polynomial integration gives

    int_-1^1 f=2(1-2/3+1/5)=16/15,
    int_-1^1 y f=0,
    int_-1^1 y^2 f=2(1/3-2/5+1/7)=16/105,
    int_-1^1 f^2=2(1-4/3+6/5-4/7+1/9)=256/315.

Taylor expansion and odd-integrand cancellation therefore give

    M=2rho*H+O(H^3),
    I0=(2/3)rho'_*(H^3)+O(H^4),
    P0=(16/15)rho* V ell+O(V ell^3),
    Kpacket=(1/2)int rho v^2=(128/315)rho* V^2 ell+O(V^2 ell^3).

For a merely C2 bound on rho the displayed I0 leading remainder is still bounded by O(H^4); the smooth inherited background more than suffices. All O constants are fixed in N with physical units inherited from derivatives of rho. In particular P0/(MV) tends to 8/15, P0 is O(N^-2), Kpacket O(N^-1), and the initial capacity

    A_N=(b-x*)M-I0=2rho*ell^2[1+O(N^-1/2)]

is O(N^-6). Endpoint choices with unequal fixed d_-,d_+ have width 2ell+(d_-+d_+)h_e and add an O(rho*ell h_e) term to I0; the leading threshold below is unchanged. Our symmetric choice removes that unnecessary asymmetry.

## 4. Exact moment gate and constants

Positivity on the interval implies I(t)<(b-x*)M, strictly, since int(b-x)n>0. Integrating I'=P0-F yields

    I(T)=I0+P0 T-int_0^T F(t)dt
        =I0+P0 T-int_0^T (T-s)D(s)ds.

Thus the weakest scalar signed transfer condition sufficient through this identity is

    int_0^T F(t)dt <= P0 T-A_N,                       (G)

including equality because the spatial moment bound is strict. Equivalently use the weighted force discrepancy integral. No absolute value or pointwise-in-time smallness is necessary. A robust stronger sufficient condition is int F<=eta P0 T with fixed eta<1 and

    (1-eta)B_dagger>15/8.

Indeed P0 T/A_N tends to (8/15)B_dagger, since T=B_dagger ell/V. This conclusion is uniform for all sufficiently large N at fixed strict margin. For example eta=1/2 and B_dagger=4 satisfy it. An absolute force bound int_0^T(T-s)|D(s)|ds<=eta P0T is stronger still. These are conditional sufficient estimates, not estimates proved for the actual family. No identification with old FGF049 B_* or FGF048 kappa is made.

Units: P and F have units density*length*velocity, A_N and the weighted integral have density*length^2, and P0T has the same units. The required weighted budget is O(rho*L^2 N^-6); its average field momentum allowance is O(rho*L v0 N^-2). The weighted force discrepancy has kernel with one time factor, so int(T-s)D(s)ds has the required two powers of time relative to force. No lost C factor: F=-C^-1 int(tau pg+sigma wk).

## 5. Actual energy estimate and its precise failure to close the budget

The complete autonomous energy density and flux are

    E=nv^2/2+c^2 n[log(n/nref)-1]+n phi
      +(tau p^2/2+W+sigma w^2/2+J k^2/2+Us)/C,
    Jenergy=nv[v^2/2+c^2 log(n/nref)+phi]-(pB+Jwk)/C.

Matter plus interaction exchanges +np, Q exchanges -np-Tscale w/C, and scale exchanges +Tscale w/C, hence E_t+(Jenergy)_x=0. Exact traces give zero flux at both fixed endpoints, so int E is conserved; moving boundaries instead require their Reynolds terms. Initial excess over the hydrostatic energy is Kpacket exactly.

A concrete energy-to-field-momentum bound is available but insufficient. Write

    Hf=int (tau p^2/2+W+sigma w^2/2+J k^2/2+Us)/C >=0.

The g>0 chart and fixed endpoint phi imply phi(a)<=phi(x)<=phi(b); fix the harmless time-independent potential gauge phi0(x*)=0, so the endpoint magnitudes are O(ell). Since e(n)=c^2 n[log(n/nref)-1]>=-c^2 nref, positivity and mass conservation imply

    Hf <= Etotal(0)+c^2 nref(b-a)-phi0(a)M = O(N^-1).

The bound retains interaction rather than treating the full energy as positive. Also B(s,a)>=s-a/2 for s>=0, so W>=g^2/2-ag/2>=g^2/4-a^2/4. Since a^2<= (8a_ref^2/S0)Us+2a_ref^2,

    int g^2 <= K_g C Hf+2a_ref^2(b-a),
    K_g=max(4,8a_ref^2/S0).

Cauchy-Schwarz and the nonnegative field terms then give the explicit inequality

    |F| <= sqrt(2tau Hf)*sqrt(K_g Hf+2a_ref^2(b-a)/C)
           +2sqrt(sigma/J) Hf.                       (E-bound)

All coefficients are fixed physical coefficients; factors tau,C,sigma,J remain explicit. This proves only |F|=O(N^-1), hence int_0^T|F|=O(N^-5). Gate (G) needs signed transfer of order N^-6 with a suitably small coefficient. The energy estimate loses one power of N. This is a failure of this sufficient estimate, not a counterexample to (G) or to the coupled PDE. A sharper signed cancellation, field-specific transfer estimate or time accumulation estimate could still succeed.

The exact uncontrolled term is -C^-1 int_0^T int_a^b(tau p g+sigma w k)dx dt, equivalently int_0^T(T-s)int(ng-rho g0)dx ds. Mass alone does not control int ng, nor n_x, nor a force supremum. Positivity of n is not a sign bound for D because rho g0 is subtracted and g is dynamic. Total momentum conservation is an identity relating P to F, not a bound on F. Edge control leaves the core products in this exact term uncontrolled. FGF048's short-kappa estimate cannot be extended to B_dagger by renaming its coefficient.

## 6. Zero-velocity control and branch restrictions

For v0 packet replaced by zero initial velocity, stationary hydrostatics solves all equations exactly: P=F=D=0, M,I fixed, Jenergy=0 and total stress constant. Pressure cancellation is essential to D=0. Its P0=0 makes (G) read 0<=-A_N, which is false since A_N>0; the moment contradiction is not triggered.

Carry both a_ref=9.3619e-11 and 1.1279e-10 m/s^2 separately with each compatible background and constants. The adopted relation a_ref=kappa_vac c_light sqrt(G_Newton rho_Lambda,ref) is not newly derived. Constant-vacuum reference, each separately frozen a0 E(z) with E^2=.315(1+z)^3+.685, and evolving reference are different protocols. For time-varying a_ref, the energy balance acquires explicit W_reference work -(Tscale/C)d(log a_ref)/dt in this convention, and stationary exterior data are generally not solutions; the autonomous result cannot simply be reused.

The diagnostic Q branch F_accel=sqrt(B^2+aB) is distinct from RAR F_accel=B/[1-exp(-sqrt(B/a))], registered M and filtered MONO. Dynamic B_x=Cn+tau p_t remains intact. No physical metric/photon/vacuum/two-DOF completion, criterion B, calibration, cosmology, historical novelty, endpoint shock classification, continuation beyond breakdown, global cone theorem or theory closure follows.

## 7. Dependency graph and obligation matrix

Task/data + accepted FGF051 local cone -> exterior subcone uniqueness -> exact hydrostatic endpoint traces -> zero matter flux and constant total boundary stress -> M constant, P+F=P0, I'=P -> explicit initial integrals + n>0 -> conditional moment contradiction. Actual PDE + autonomous fixed reference + traces -> complete energy conservation -> (E-bound), insufficient for (G). No circular use of the desired lifespan bound appears.

| Obligation | Evidence kind | Status |
|---|---|---|
| Actual full Q/scale/fluid objects and exact joins | pinned internal definitions | passed |
| N^-7/2 edge existence and whole-branch matching | accepted pinned internal theorem FGF051 | passed as dependency |
| Exterior buffer and exact hydrostatic traces | internal derivation above | passed |
| Pressure, both field momenta/stresses, exchange signs | direct algebra | passed |
| Explicit polynomial integrals, width and varying-rho errors | exact integration and Taylor remainder | passed |
| Signed weighted moment gate and 15/8 threshold | internal proof | passed |
| Full energy including interaction and both fluxes | direct algebra | passed |
| Energy-to-momentum inequality | internal proof | passed, insufficient scale |
| Actual weighted transfer bound (G) through T | presently unsupplied estimate | conditional |
| Zero-velocity hydrostatic control | exact substitution | passed |
| Both reference normalizations and history/model separation | explicit conventions | passed |
| Physical completion and endpoint type | none | out of scope |

There are no external-theorem or computation leaves and no literature used. The smallest missing implication is a non-circular bound on the signed integrated field momentum satisfying (G), or its strict-margin fractional version, for actual whole classical candidate continuations. Cheapest next check: exploit the actual zero initial p,w and opposite Q/scale exchange signs to estimate the time-integrated core products; do not repeat the already insufficient unsigned total-energy bound.
