# Dynamical UV-normalized cutoff: no finite vacuum equilibrium, rolling instead

## Concrete changed premise and result

Promoting Claude's finite cutoff T to a canonical field u=lnT in the same UV-normalized interaction does not select T near128.915. Its vacuum potential is positive and strictly increasing, with exact logarithmic slope 1<A_u/A<3/2. The constant-modulus vacuum equation therefore has **no finite solution**. A positive canonical kinetic term permits a rolling homogeneous solution; its small-T limiting scalar or fluid-tracking states depend on the freely introduced kinetic normalization. These statements concern this explicit canonical completion and inherited UV subtraction. They are neither an all-completions obstruction nor a healthy full theory or32pi selection.

## Explicit same-action choice and both metric variations

Work in c=1, spatial n>=3, K=1/(16pi G_EH), chi_n=(n-1)/(2(n-2)). Start the exchange-symmetric projected-acceleration action already derived in the frozen parent:

    S_grav=K integral[ sqrt(-g)R_g+sqrt(-ghat)R_hat
                  +2 chi_n a0² v M(I,T)]d^(n+1)x,
    v=[(-g)(-ghat)]^(1/4),
    I=(P_g^mu nu+P_hat^mu nu)(a_g-a_hat)_mu(a_g-a_hat)_nu/(2a0²).

The shared foliation clock theta is timelike in both metrics, u_g is its normalized future normal, a_g=u_g grad u_g and P_g=g_inv+u_g u_g, similarly hatted. The acceleration-difference invariant is nonnegative; it vanishes on any shared homogeneous FRW background. The modulus u=lnT is a different scalar from theta. Choose the explicit, positive and exchange-even kinetic term

    S_u=-(f²/4) integral[ sqrt(-g)g^mu nu+sqrt(-ghat)ghat^mu nu]
                             partial_mu u partial_nu u,
    f²>0 constant.

Each metric supplies its own ordinary canonical scalar kinetic density; no mixed inverse with ambiguous signature is used. This is a minimal two-derivative diagnostic premise, not a symmetry argument fixing f². No new stabilizing W(u) is included.

At fixed T define b(y)=sqrt(1+1/y)-1, e(y,T)=b(y)/(1+(y/T)²), d=ye, q(y,T)=2 integral_0^y t e(t,T)dt. The same spherical source lift is defined parametrically by

    x=y+2d, I=x²,
    M(I,T)=q(y,T)+2d²-A(T),
    A(T)=2 integral_0^infinity y e(y,T)dy.

Then M_I=d/x, and at fixed x, M_u=T[q_T-A_T]. Thus this is the retained cutoff interaction with its own UV normalization: M(infinity,T)=0, whereas M(0,T)=-A(T). The added canonical kinetic term changes the local source modulus equation, as it must; it does not leave every source kernel exactly fixed. This same radial dictionary is not QUMOND for general shapes. For T=128.915 a global inverse is admitted by the parent; for arbitrary small T the fixed-T full source inverse can fold. The homogeneous branch I=0 and its sufficiently small-I local neighborhood remain defined for every finite T>0. The rolling calculation below is a coincident vacuum-sector calculation, **not a demonstrated full Solar/source continuation through those folds**. This is a crucial limitation of the candidate, not a silently assumed extension.

On coincident FRW metrics g=ghat, I=0 and its first variation is zero. The homogeneous foliation-clock equation is therefore satisfied. The combined action reduces to

    integral sqrt(-g)[(Mpl/2)R-(f²/2)(partial u)²-V(u)],
    Mpl=4K, V=2K chi_n a0² A(T)=(Mpl/2)chi_n a0² A(T).

Here Mpl denotes the Einstein coefficient, often denoted M_Pl² in four-dimensional hbar=c=1 notation, not its square root. All dimensions below retain classical units without setting hbar to one. The notation is retained consistently in all formulae. V and f² have dimensions [V]=energy/L^n, [f²]=[K]=energy/L^(n-2); u,T,A,chi and gamma=f²/Mpl are dimensionless. No hbar is introduced. Physical Newton normalization remains Gn=8pi(n-2)G_EH/[(n-1)Omega_(n-1)].

This reduction is not obtained by discarding the second metric equation. Independent variations give, on coincidence,

    2K G_mu nu=T_mu nu(each),
    T_mu nu(each)=(f²/2)[partial_mu u partial_nu u
                        -(1/2)g_mu nu(partial u)²]-(V/2)g_mu nu.

The determinant-volume variation is one quarter per metric, so its vacuum stress is exactly -Vg/2 per sector. The two equations agree in vacuum. For a fluid extension, take identical mirrored minimally coupled fluids, each with half the displayed total density; an ordinary-only homogeneous fluid generally cannot keep the metrics coincident. Summing the two equations gives Mpl G=T_total. The canonical modulus equation is

    f² Box u-V_u=0,
    uddot+nH udot+V_u/f²=0.

For a constant modulus the metric equations would give Lambda=chi_n a0² A/2 and H²=chi_n a0² A/[n(n-1)], but the modulus equation additionally requires A_u=0. Importing the constant-T Lambda dictionary while omitting this new equation would be inconsistent.

## Exact positive slope and endpoint asymptotics

Set y=T tan(theta), theta in(0,pi/2), h(y)=yb(y)=1/[sqrt(1+1/y)+1]. Then

    A(T)=2T integral_0^(pi/2) h(T tan(theta))dtheta,
    dln h/dln y=(1-1/sqrt(1+1/y))/2 in(0,1/2),
    A_u/A=1+[integral h (dlnh/dlny)]/[integral h] in(1,3/2).

All integrals converge. Differentiation is controlled by the bounded logarithmic derivative times h, so no unverified differentiation of a divergent moment is used. In particular A_T>0 and no finite positive T constant-modulus solution exists, regardless of f² or H. Adding an independent constant offset does not change this equation. A new W would have to supply W_u=-V_u at a proposed equilibrium; the equilibrium would depend on that new physics, not follow from this retained kernel.

Dominated convergence gives

    A(T)~sqrt(2)pi T^(3/2) as T->0,
    A(T)~(pi/2)T as T->infinity.

For the first limit h(Ttan(theta))/sqrt(T)<=sqrt(tan(theta)), whose integral is pi/sqrt(2). For the second h<=1/2. The derivative slope tends to3/2 and1 respectively by the same weighted estimates. The small-T correction is slow enough that an initial too-demanding finite-T asymptotic check failed; the accepted test uses T=1e-15 and records its finite residual, not exact equality.

## Actual homogeneous equations and runaway

For the mirrored fluid with -1<w_b<1, or empty vacuum with rho_b=0,

    n(n-1)H²/2=[f²udot²/2+V+rho_b]/Mpl,
    Hdot=-[f²udot²+(1+w_b)rho_b]/[(n-1)Mpl],
    rhobdot=-nH(1+w_b)rho_b.

These contain scalar kinetic energy; the old vacuum moment is not the entire rolling gravitational source. Total energy is decreasing on the expanding flat branch, so H<=H_initial and |udot| is bounded. The unbounded increasing potential forbids u going to+infinity. An initially positive velocity must turn: a bounded upper limiting u would retain a positive force and cannot sustain asymptotically nonnegative velocity. Once udot=0, uddot<0, so velocity cannot cross back to positive. If decreasing u had a finite lower limit, V_u would be bounded below by c>0; v=-udot would obey vdot+nH_initial v>=c/f², giving a strictly positive eventual speed and a contradiction. Therefore u->-infinity on any future-complete expanding homogeneous solution: T->0, not a finite cutoff. This is a homogeneous-sector statement; full source admission can fail before that limit.

## Limiting scalar and density-tracking predictions

Write gamma=f²/Mpl, N=ln a,

    x=f udot/[sqrt(Mpl n(n-1))H],
    z=sqrt[2V/(Mpl n(n-1))]/H,
    E=2x²+(1+w_b)(1-x²-z²),
    r=sqrt[n(n-1)/gamma], s=(A_u/A)r/2,
    x_N=-nx-sz²+(n/2)Ex,
    z_N=sxz+(n/2)Ez, u_N=rx.

The scalar fraction is x²+z², and the fluid fraction 1-x²-z². These are derived directly from the equations above. No external tracking theorem is borrowed. At small T use p=3/2 in place of A_u/A. The limiting scalar fixed point is

    x_s=-(p/2)sqrt[(n-1)/(n gamma)], z_s²=1-x_s²,
    w_s=-1+(n-1)p²/(2n gamma),
    a~t^h, h=4gamma/[(n-1)p²], T~t^(-2/p).

It exists with V>0 when x_s²<1. Its two autonomous eigenvalues are n(x_s²-1) and n(2x_s²-1-w_b), so it is locally stable against the fluid for gamma>(n-1)p²/[2n(1+w_b)]. Acceleration requires gamma>(n-1)p²/4. For any finite gamma this is power-law expansion, not future constant-H de Sitter.

For gamma<(n-1)p²/[2n(1+w_b)], the limiting tracking state is

    x_t=-sqrt[n gamma/(n-1)](1+w_b)/p,
    z_t²=n gamma(1-w_b²)/[(n-1)p²],
    Omega_scalar=2n gamma(1+w_b)/[(n-1)p²], w_scalar=w_b.

Its Jacobian trace is n(w_b-1)/2<0 and determinant n²(1-w_b²)(1-Omega_scalar)/2>0. Both conditions are explicit and checked. Tracking therefore predicts a constant fraction **set by gamma and the fluid**, not a vacuum coefficient fixed by symmetry. Its scale factor is a~t^[2/(n(1+w_b))], while T~t^(-4/3) for p=3/2. These are limiting fixed-point and local-stability statements; a broad global attractor theorem for the full two-metric/source system is not claimed.

The exact homogeneous dictionary along any such state is H²/a0²=chi_n A(T)/[n(n-1)z²]. Because T evolves and z depends on gamma/branch, it does not identify a universal a0/H. Changing the positive canonical normalization changes the tracking fraction or power-law equation of state. No finite value128, no32pi and no density-versus-vacuum preference is selected.

## Bounded computation and remaining implication

checks.py independently evaluates the original y integral and the transformed positive integral at declared cutoffs, verifies endpoint coefficients and the exact autonomous fixedpoints/Jacobians, and integrates the full varying-slope homogeneous equations for n3, gamma=.1,.5,2 with dust and gamma=.1 with radiation. Initial x0=0,z0=.1,T0=128.915 defines positive fluid data through Friedmann; the number is a declared test initial condition, never an equilibrium or target fit. Forty-five e-fold runs approach the stated limiting points. Their endpoint scalar fractions are approximately .133333,.666667,1 and .177778 respectively; the scalar-dominated gamma2 state is accelerated and still has rolling T. Each integration has an explicit12000-RHS guard.

The numerical logarithmic-slope table has350 nodes on u=-55..10 and independent midpoint tests. Below u=-55 its endpoint slope is used; this is an explicitly bounded asymptotic approximation, not an exact value at all u. For T<1/2, a crude bound on 3/2-A_u/A is (15/4)sqrt(T)[ln((1+T²)/T²)+1], from h>=sqrt(T)/3 on y in[T,2T], h/s<=y on y<=1 and h/s<=1/2 beyond. At exp(-55) this is below5e-10 and decreases thereafter, negligible compared with the declared2e-4 fixed-point comparison tolerance. The ODE evidence is nevertheless bounded numerical corroboration, not a global stability proof.

Preflight a and b preserve endpoint quadrature warnings/failures, c preserves the valid integral's finite-T asymptotic mismatch; none is successful evidence. The final cotangent-based endpoint reconstruction avoids cancellation of pi/2-theta, and the scalar run extends35 to45 e-folds to test its named slow convergence. Standard run manifests and three intended false controls are authoritative; RUNS.json is a separate frozen summary. No source paper theorem or new data are imported; sources.json pins authenticated action/source records and their exact local input hashes.

The first remaining full-theory implication is an admissible global interaction/source extension with the evolving T, including the common-clock and relative-metric constraints. Even conditional on that extension, positive canonical kinetic energy does not change the exact finite-vacuum obstruction. A stabilizing interaction or a different dynamical principle would be genuinely new input and must be derived independently.
