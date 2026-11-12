# Independent audit: density-portal slow-tail principal checkpoint

12 November 2026. Read-only audit of THEORY_CHECKPOINT.md and the pinned CT14 H2 action/reduction. No use of the author's matrix checks as a substitute for derivation, no new background solve and no observational fit. Finite corroboration was still pending when this review began.

## Verdict

The kernel identities, fixed-polarization scalar kinetic coefficient, sufficient eta<=50/81 bound and negative-constraint-block argument are mathematically sound for the **declared frozen leading-derivative PN block**. The Schur-complement proof genuinely retains the khronon velocity; it does not repeat CT13's static-clock sign error.

This establishes a scoped positive kinetic principal block, not full health of the parent covariant action or a finite-wavelength screened solution. The strongest 'full all-angle PN'/'every finite k' wording needs its truncation attached immediately. Lower-spatial-order lapse terms, finite mu_K, potential terms, metric/shift constraints, coefficient gradients and a solved screening background can alter the actual finite-k constraint/spatial operators. The checkpoint already leaves these obligations open; they must remain open in the final synthesis. No specific algebraic flaw was found in its claimed truncated kinetic lemma.

## 1. Action normalization and signs reconstructed

Take c=1, K=4piG and a²=xi G E with E=X+V, xi>0. In the acceleration representation L_J=a² f(g/a)/K, put x=g/a, p=f', d=f'', h=2f-xp and epsilon=xi/(8pi). At fixed g,

    L_E=epsilon h,
    L_EE=-epsilon x h'/(2E),
    L_gg=d/K,
    L_gE=a(p-xd)/(2EK),
    h'=p-xd.

For an aligned scalar with q=n.partial phi, eta=q²/E, the bare canonical kinetic coefficient plus this interaction gives

    G_phi=1+epsilon h,
    K_free=1+epsilon[h-eta x h'/2].

The Legendre transformation to the independent polarization gives

    W_EE=-L_EE+L_gE²/L_gg,
    K_lock=K_free-q² L_gE²/L_gg
          =1+epsilon[h-eta(p²/d-xp)/2].

The subtraction and factor 1/2 are correct. E is a local bare canonical energy function here; its identification with a total interacting-sector stress density away from FRW is not automatic. eta=1+w is the bare aligned canonical ratio. A cosmological w in the desired interval does not prove a local screened solution remains in that interval.

The static total Lagrangian -g²/(2K)+a² f/K indeed gives mu=1-f'/x. For the simple-mu f=x-ln(1+x), d=(1+x)^-2 and p=x/(1+x), so p²/d-xp=x³/(1+x). This reproduces CT14 H2's failure coefficient with the same normalization. The source script explicitly retains delta A=grad(deltaPhi-delta sigma_dot), and the checkpoint's use of the fixed-polarization coefficient is the appropriate kinetic one.

Notation hygiene: the checkpoint sometimes calls the dimensional polarization magnitude p=a f'(x) and later the dimensionless p(x)=f'(x). The formulas are consistent when those are distinguished; rename them Pmag=a p(x) in publication to avoid a normalization ambiguity.

## 2. Slow-tail formulas and bound reconstructed

Let u=sqrt(1+2x), x>=0. Direct differentiation of

    f=(u³-3u+2)/6

gives p=x/u and d=(1+x)/u³. Thus 0<d<1 for x>0, p>0 there, and mu=1-1/u has the required mu~x deep limit. The Legendre inverse x=r²+r sqrt(1+r²) for r=Pmag/a>=0 is correct. At r=0 take the continuous endpoint; the transverse Hessian formula is interpreted by its limit.

The stated

    h=(u-1)³(u+3)/(12u),
    D=p²/d-xp=x³/[(1+x)u]

are correct. For x>0,

    2h/D=(2/3)[1-2(u-1)/(u+1)³].

The derivative of (u-1)/(u+1)³ is (4-2u)/(u+1)^4. Its maximum on u>=1 is 1/27 at u=2, hence 2h/D>=50/81. Therefore eta<=50/81 implies h-eta D/2>=0 and K_lock>=1 for all finite x>0. At x=0, h=D=0 and K_lock=1 by continuity, but the clock constraint inversion is singular there, so this scalar coefficient does not supply a uniform two-mode health bound including x=0.

The bound is sufficient, not shown necessary or optimal. It covers the stated canonical w interval only on the aligned bare-scalar branch. At eta=2/3 the leading large-x terms cancel and subleading terms can drive K_lock negative; there is no contradiction with the more restrictive sufficient bound.

Convexity obstruction to a tail with p->0 is also correct in this unscreened class: if p>0 somewhere and p tends to zero, p'=d must be negative somewhere. For mu=1-exp(-x), d=(1-x)exp(-x) has precisely that failure. The clock coefficient d/(1-d) of the unscreened gamma=mu_K=0 PN reduction is negative for x>1. This does not exclude additional screened operators or every rapid-tail parent action.

## 3. All-angle kinetic block: reconstructed proof

In the given PN truncation and units a=K=1, the Legendre Hessian is

    H=diag(x/p,x/p,1/d).

For the slow kernel H_T=u>1 and H_L=u³/(1+x)>1 at x>0. Adding the active nonnegative stiffness gives Dmat=H+gamma k² n n^T>I for gamma>=0. For unit n, Qc=n^T Dmat^-1 n lies strictly between zero and one. The constraint block

    C=[[-k²,k n^T],[k n,-Dmat]]

has negative polarization block and negative lapse Schur complement -k²(1-Qc). It is therefore negative definite for finite x>0,k>0.

For physical velocities v=(delta phi_dot,zeta_dot), the proposed reduction is

    K_red=diag(K_lock,0)-B^dagger C^-1 B.

Since -C^-1 is positive definite, the second term is positive semidefinite. If a vector v could have zero quadratic form, its scalar component must vanish because K_lock>0. Its remaining clock component then couples through the nonzero clock column B_clock=(0,-n), so it too must vanish. Hence K_red is strictly positive definite for every angle in this truncated block. Adding the stated lapse/scalar velocity coupling to B cannot defeat this argument; it changes neither the positive baseline scalar entry nor the nonzero clock column.

For the simplified polarization/scalar mixing alone, direct inversion yields the checkpoint's 2x2 matrix. Its determinant is

    [Qc(K_lock+C0)-B0²]/(1-Qc),
    C0=bvec^T Dmat^-1 bvec,
    B0=n^T Dmat^-1 bvec.

Cauchy-Schwarz gives Qc C0>=B0², leaving strictly positive Qc K_lock/(1-Qc). This is a genuine coupled proof, not a test of just one diagonal element. No lower uniform eigenvalue over x->0/infinity, k->0/infinity or gamma->infinity has been established by it.

## 4. Spatial/no-growing-root and metric scope

If the truncated conservative reduced system has exactly U=diag(G_phi k²,rho_tau), rho_tau>0 and no omitted leading gyroscopic/spatial cross terms, then U and K_red positive definite imply positive generalized omega² and no growing roots in that system. This conclusion is conditional on that U actually being the retained operator. Positive kinetic energy alone does not establish gradient stability of every term in the parent action.

CT14's complete finite PN matrix includes potential slopes, lapse/scalar zero-frequency couplings, finite mu_K and a background density. The checkpoint drops these in declaring a principal block. In a full reduction the scalar kinetic background can also supply lapse² terms, and nonlinear n.P constraints/background geometry can contribute lower-PN/spatial terms. Such contributions cannot be inferred from the C displayed here. Reinstating them need not preserve negative definiteness at arbitrary finite k. Full metric/shift/tensor constraints have also not been derived anew for the changed action. Thus phrase the result as 'all-angle positivity of the specified leading PN kinetic block', not 'the covariant action is healthy at all wavelengths'.

At gamma=0 parallel to g, the simplified block gives c_fast²=G_phi/K_lock in its high-k limit, consistent with the report. Its slow-tail large-x ratio tends to 2/(2-3eta)>1 for eta>0 inside the sufficient interval. Thus this construction already has a real preferred-foliation/metric-cone issue; kinetic positivity does not establish luminal or subluminal propagation. For gamma=0 the slow high-k root tends to rho_tau/K_zeta_zeta. At negative rho_tau that is a finite-rate negative branch; positive stiffness can make the inherited UV failure stronger. The report correctly does not declare a universal negative-density or sign-interface pass.

## 5. Background density tracking and screening mismatch

f=x²/2-x³/3+... gives L_J=g²/(2K)-g³/(3Ka)+..., so homogeneous g=0 has no interaction energy and the a-dependent portal enters beyond the quadratic acceleration term. Exact FRW can therefore retain the stated canonical homogeneous E and a²=xiGE in this architecture. This does not establish perturbation health, phantom crossing, cold abundance, kappa or the old growth/CMB gates for the new parent.

The unscreened slow tail is phenomenologically expensive: 1-mu~1/sqrt(2x) gives delta g~sqrt(a gN/2), approximately 5x10^-7 m/s² at 1AU for the quoted a. This estimate is a warning about the unscreened branch, not a solved screened prediction. Physical acceleration and khronon acceleration can differ after stiffness/screening, so old simple-mu local tests cannot be inherited and neither can old local constancy: h now grows as x^(3/2). A screened solution must determine its own g/a, eta, polarization, active switch, density sign and scalar variation before using the kinetic lemma.

The bound covers an exponential scalar-dominated lambda=1 canonical attractor's w=-2/3 algebraically. It does not prove that the coupled local scalar solution around matter inherits that attractor ratio. The checkpoint properly lists this as the first unresolved physical implication.

## Publication status

Accept as a useful analytic principal checkpoint with a genuinely changed interpolation function. Do not adopt or publish it as a complete healthy theory, a local-gravity success, an empirical improvement, a first-principles normalization or a resurrection of a retired route. The next load-bearing computation is a consistent screened background plus its full constrained perturbation operator; the all-angle matrix sweep only corroborates the declared algebraic truncation.
