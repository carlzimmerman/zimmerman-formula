# FGF044 independent exact-continuity flow audit, frozen

Before new author/root proof or previews. One prescribed C1 profile, no smoothing, no numerical scan. Keep the fixed-reference Q central crossing, physical coefficients, fixed time slab [0,T], mass and walls. Choose x*>0 on its positive regular side, away from center/walls; this allowed side choice is explicit because rho'<0 there will decide the exact energy-inequality sign. Let w=L/N³, U=v0 N, f(y)=(1-y²)² for |y|<1 and0 otherwise. v_N(x)=U f((x-x*)/w), N dimensionless. Unlike previous smooth bumps, f is C1 globally and piecewise smooth with bounded piecewise second derivative; f'' jumps at endpoints. This regularity is adequate below; no C-infinity assertion.

## Exact finite-time map and density

Define theta=Ut/w=(v0/L)N4 t and the dimensionless flow Y_theta(y0). Outside [-1,1] it is the identity; inside solve dY/dtheta=f(Y). The explicit increasing time coordinate

 F(y)=y/[2(1-y²)]+atanh(y)/2,
 F'(y)=1/(1-y²)²=1/f(y)

maps (-1,1) onto R. Thus Y_theta(y0)=F^-1(F(y0)+theta), remains strictly inside for every finite theta, and increases toward1 without arriving in finite time. Physical flow is X_t(q)=x*+w Y_theta((q-x*)/w) within the support and q outside. Its positive Jacobian is

 J_t(q)=f(Y_theta(y0))/f(y0).

The endpoint extension has J=1: the C1 velocity has v'=0 at the endpoints, and its finite-time flow derivative is exp(integral v'(X_s)ds), tending to1 as q approaches an endpoint at fixed N,t. Consequently the global map is C1, increasing and onto, with fixed exterior and no mass crossing endpoints. Define

 n_N(t,X_t(q))=rho(q)/J_t(q).

This is positive for finite N,t, conserves mass exactly, and solves continuity in the distributional sense, classically inside smooth pieces. Conservative flux traces match at support endpoints; no delta boundary source is introduced. Density is continuous and piecewise regular; first derivatives can jump, which is allowed in the stated weak equations. Initial n=rho, original fields held at phi0,chi0 with zero field velocities. Field walls unchanged. Only the initial support mass m_N=integral_(x*-w)^(x*+w)rho=O(w) can move; exterior initial mass stays fixed forever.

## Polynomial compression and entropy

Write g(y)=1-y² inside. Along a trajectory d(1/g)/dtheta=2Y, hence its absolute derivative is <=2. Applying this forward and backward yields

 (1+2theta)^-1 <= g(Y)/g(y0) <=1+2theta,
 (1+2theta)^-2 <= J <=(1+2theta)^2.

The inequalities also extend continuously at endpoints. Therefore |log J|<=2log(1+2theta). For finite N and fixed slab every state has finite positive density; no uniform density cap or no-vacuum limit is inferred. Since log rho is Lipschitz on this regular support and |X_t(q)-q|<=2w,

 D(n_N|rho)
 =integral_support rho(q)[log rho(q)-log rho(X_t(q))-log J_t(q)]dq
 <=m_N[2log(1+2theta)+2w ||(log rho)'||infinity].

The -n+rho entropy terms integrate to zero by exact support mass conservation. Thus sup_(0<=t<=T)D=O(N^-3 log N), and ||n-rho||1<=2m_N=O(N^-3). K=integral n v²/2<=U²m_N/2=O(N^-1), uniformly in time. The fields are unchanged, so the FULL relative energy is exactly

 Erel_N(t)=K_N(t)+cs² D(n_N(t)|rho).

This uses actual hydrostatic cancellation of internal/interaction first variations, not deletion of interaction. Hence sup_t Erel=O(N^-1)+O(N^-3log N)->0. Full energy-density difference is small in L1 too: e(n)-e(rho)=cs² h(n|rho)+e'(rho)(n-rho), interaction is bounded by ||phi0||infinity||n-rho||1, and kinetic is nonnegative. No field energy changes.

## Exact global inequality FAILS on the chosen positive side

A small uniform energy bound is not an exact energy inequality. At t=0, entropy's first derivative vanishes because n=rho and mass is fixed. Stationary prescribed v gives

 Erel_N'(0)=K_N'(0)=integral rho v² v' dx
                         =-(1/3)integral rho' v³ dx>0,

since f>=0 is nonzero and rho'<0 on the chosen positive-side support. Thus for every sufficiently large N there are arbitrarily small positive times at which Erel_N(t)>Erel_N(0). This does NOT satisfy the stipulated exact inequality. The initial derivative tends to -(rho'(x*)v0³L/3)integral f³>0, despite uniform excess tending to zero; the initial time layer is nonuniform. A quantified weaker statement holds: Erel_N(t)<=Erel_N(0)+epsilon_N with epsilon_N bounded by U²m_N/2+cs²m_N[2log(1+2UT/w)+2wLip(logrho)]->0. Side choice matters; no unproved strict-sign statement is asserted for x*<0.

## Finite supply and cubic spacetime flux

The material change of variables gives the exact accounting identity

 integral_0^T integral n v³/2 dxdt
 = (1/2)integral_support rho(q) integral_q^(X_T(q)) v(x)² dx dq
 <=(1/2)m_N U² w integral_-1^1 f(y)²dy =O(N^-4).

It uses dx/dt=v along a positive trajectory. No exterior mass source enters. Likewise

 integral_0^T integral n v dxdt=integral rho(q)(X_T(q)-q)dq<=2w m_N=O(N^-6),
 integral_0^T integral n v² dxdt<=2U w m_N=O(N^-5).

Thus the former persistent cubic spacetime measure disappears under exact continuity; it cannot be sustained by the O(N^-3) initial participating mass. This is an exact finite-slab bound, not a freely exchanged long-time limit.

At t=0 the cubic spatial flux still tends to F_*=rho(x*)v0³L integral f³/2>0. At fast times t=s w/U with fixed finite s, its spatial integral tends to (rho(x*)v0³L/2)integral f(Y_s(y0))³dy0, positive. At each fixed t>0 it tends to zero, as follows from a uniform dimensionless flow bound. The explicit F formula gives f(F^-1(s))<=16/(1+|s|)²: for y>=0, F(y)<=1/(1-y) by bounding its rational and logarithmic pieces, and f<=4(1-y)²; symmetry covers negative s. Split final locations into F(y)<=theta/2 and F(y)>theta/2. On the first, f(y0)<=64/theta² and dy0=f(y0)dy/f(y), so integral f(Y)^3dy0<=64 theta^-2 integral f(y)²dy. On the second, f(Y)<=64/theta², so contribution is <=2(64/theta²)^3. Bounded rho0 supplies the same O(theta^-2) bound for the weighted cubic integral for theta>=2. Since U³w is constant, fixed-t cubic flux is O(N^-8 t^-2). Uniform disappearance on [0,T] is FALSE because t=0 and t=O(N^-4) retain order-one flux; on [t0,T] with t0>0 it is uniform. The initial layer has total spacetime mass O(N^-4), so no time-delta energy-flux defect survives.

## Complete energy current and local residual

For general transported n, the enthalpy cannot be replaced by the old constant mu. The actual current is

 S_N=n v³/2+cs² n v log(n/rho_ref)+n v phi0,

with zero field parts. Along the flow log n=log rho(q)-log J, so on the fixed slab |log(n/rho_ref)|<=C+2log(1+2UT/w). The exact displacement accounting therefore bounds the spacetime enthalpy flux in L1 by O(N^-6 log N), and potential flux by O(N^-6). Together with the cubic O(N^-4), ||S_N||_(L1 spacetime)->0. Every term is finite for each N. The full energy-density difference tends uniformly-in-time to zero in spatial L1. Consequently RE_N=partial_t e_total,N+partial_x S_N tends to zero against compact spacetime C1 tests. Initial full energy trace is O(N^-1) and walls have zero energy current, so there is no hidden initial/boundary defect. Local energy balance is NOT exact at finite N; with exact continuity and stationary fields the off-shell identity is RE_N=v_N Rm_N wherever smooth, but the direct current bounds justify the weak limit without multiplying weak residuals.

## All remaining actual residuals and nonuniformity

Continuity is EXACTLY zero. Scale residual stays zero. Dynamic Q source is now Rphi=C(n_N-rho), O(N^-3) in L-infinity_t L1_x, because the original fields still source rho. It is not an exact field solution. Put r=n-rho. Hydrostatic background cancellation gives

 Rm=partial_t(nv)+partial_x(nv²+cs²r)+r g0,
 Rcomb=partial_t(nv)+partial_x(nv²+cs²r),
 Rm-Rcomb=r g0.

The latter follows directly from FULL combined currents P=nv, Pi=Pi0+nv²+cs²r; field stresses are unchanged. Using compact spacetime C1 tests, integrated ||nv||1=O(N^-6), ||nv²||1=O(N^-5), and integral||r||1=O(N^-3), so both residuals are O(N^-3) in the corresponding first-derivative spacetime test norm. Initial momentum is O(N^-2), so tests reaching t=0 add only a vanishing term. Primitive momentum equals conservative momentum since continuity is exact; density is positive at finite N. All claims are spacetime weak statements; the old uniform-time spatial residual estimates must NOT be inherited.

In fact a rapid uniform-time momentum obstruction can be detected. Let G(s)=integral_-1^1 f(Y_s(y0))dy0. Then G'(0)=integral f'f=0 and

 G''(0)=integral [f(f')²+f² f'']dy0=-integral f(f')²dy0<0,

using vanishing endpoint terms. The specified piecewise smooth C1 profile has bounded f'', sufficient for these integral derivatives. Thus G'(s)<0 at some fixed small s>0. At t=s w/U, the derivative of spatial momentum is U² integral rho(x*+wy0)f'(Y_s)f(Y_s)dy0, asymptotic rho(x*)U² G'(s), of order N². A smooth spatial test equal1 on the support detects this in Rcomb because spatial flux derivatives then integrate to zero. Therefore no uniform-in-time spatial Lip* residual convergence is asserted; it generally fails in this initial layer. This does not contradict spacetime weak convergence or small total momentum.

## Zero control, traces, scope

For v0=0 use the direct identity flow X_t(q)=q, n=rho, zero current, zero full excess and EVERY residual zero. Do not use the singular theta rescaling formula to infer this limit. The mass identity n(X)J=rho and the exact path integrals independently check accounting. Finite-N maps preserve support, regularity and wall traces; no smoothing or unrecorded profile variation occurs.

Outcome: exact continuity extinguishes the persistent cubic spacetime flux, entropy and full energy remain uniformly small, but the original fields have density residuals and the exact global energy inequality FAILS on the chosen right-side background. Only a quantified vanishing energy error and spacetime weak residual convergence hold. This is a prescribed-velocity transport family, not an exact coupled trajectory. Fixed-time initial-layer limits and exact versus approximate energy inequalities remain separate. The next missing implication is a same-action construction satisfying the actual energy inequality and required local/residual topology simultaneously, not another moment/profile sweep.

Both positive a0 hypotheses, actual signed MOND Q source, distinct vacuum/frozen-H/evolving-H histories and fixed inertias remain. No RAR/M, filtered-MONO, metric/photon/DOF, physical reservoir, instrument evidence, novelty or theory closure follows.
