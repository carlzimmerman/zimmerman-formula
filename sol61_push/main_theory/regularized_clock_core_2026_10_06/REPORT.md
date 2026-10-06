# Detuned conserved clock core: constructive finite source and exterior

Detuning the critical acceleration term admits a regular high-density, positive-pressure source and an actual same-state finite vacuum continuation. The epsilon=.01 toy below reaches its p=0 surface and r=3e-5 at two tolerances. This closes the previous regular-center density obstruction for this changed action. It does not establish a normalized cosmological match or perturbative health, and epsilon is an additional free input.

## Action, source and exact center

Keep the source_asymptotics logKGB action, Einstein coefficient M>0, fixed vacuum U(N)=M[-3H²+6 eta H² lnN], 0<eta<1, but replace its acceleration response by

    Qepsilon(a)=(1-epsilon)a²-2W(a;A), 0<epsilon<1,
    W_a=sqrt(a²+A²/4)-A/2, a=|Nprime|/(NB).

The radial stationary action (per solid angle, after boundary removal) is

    L=M[N(B+1/B)+2rNprime/B]
      -MrV²[Bprime/N+B Nprime/N²]+NBr²U
      -2M eta H Br²V Nprime/N+MNBr²Qepsilon.

Use ds²=-N²dt²+B²(dr+Vdt)²+r²dOmega² and F=N²-B²V². Matter is a static Killing perfect fluid with proper constant rest density rho0, not static dust. Its exact sources are E_Nm=-Br²[(rho+p)N²/F-p], E_Bm=Nr²[p+(rho+p)B²V²/F], E_Vm=NB³r²(rho+p)V/F. Conservation gives pprime=-(rho+p)Fprime/(2F), hence rho+p=(rho0+p0)N0/sqrtF. The unchanged sourced momentum equation is

    V[Bprime/B+Nprime/N-N²B²r(rho+p)/(2MF)]+eta H rNprime=0.

The source-current cancellation remains unchanged: response detuning is shift-independent, and conserved matter contributes the same vanishing weighted source combination as the prior derivation. No independent scalar charge is inserted.

For N=N0(1+n2r²+...), B=1+b2r²+..., V=N0xr+..., define R=rho0/M, P=p0/M, u0=-3H²+6etaH²lnN0, kappa=1-epsilon. Direct variation gives

    2b2-4n2+3x²+u0=-P,
    6b2-12kappa n2+3x²+6etaHx+u0+6etaH²=R,
    x[b2+n2-(R+P)/4]+etaH n2=0.

Consequently

    R+3P=12epsilon n2-6x²+6etaHx-2u0+6etaH²,
    (3kappa x+etaH)n2=(3/2)etaH x(x+H),
    b2=2n2-(3/2)x²-u0/2-P/2.

The physical central force uses f2=2n2-x², because F=N0²(1+f2r²+...). Thus p2=-(rho0+p0)f2/2. Positive n2 alone is insufficient.

At N0=1, y=x/H, the center branch has

    n2/H²=(3/2)eta y(y+1)/(3kappa y+eta),
    D=(R+3P)/H²=12epsilon(n2/H²)-6y²+6eta y+6(1+eta).

For kappa>eta/3, y increases from -1 to yp=-eta/(3kappa). n2 increases from zero to infinity: its derivative is (3/2)eta[3kappa y²+2eta y+eta]/(3kappa y+eta)², whose numerator is positive. D also increases, because y<0 and Dprime=12epsilon n2prime-12y+6eta>0. Thus every positive D has unique center data on this branch, and f2>0 for sufficiently high D. The cosmic vacuum endpoint y=-1,n2=b2=0 is unchanged. This is a center-data connection, not an on-shell global boundary connection.

The other epsilon range also admits formal high-density center data. If kappa<eta/3, use yp<y<-1; n2 tends to infinity at yp from above. Factor

    D=6(y+1)Q(y)/(3kappa y+eta),
    Q=-3kappa y²+(3kappa+2eta)y+eta²+eta.

On this interval Q<0: Q increases with y and Q(-1)=eta²-eta-6kappa<0. Both terms in the derivative numerator (eta-3kappa)Q+(y+1)Qprime(3kappa y+eta) are negative, so D decreases from infinity to zero. At kappa=eta/3, x=-H makes the momentum equation identically zero; the density equation sets n2=(R+3P)/(12epsilon), with high-density f2>0. This algebraic degeneracy is not proof of higher-order compatibility. The executed check and numerical construction use the nondegenerate small-epsilon branch only.

## Sourced Newton core and finite MOND window

The weak sourced equations give, with v=V+Hr, S=V²-H²r², g=a-Sprime/2,

    [r²(g-a+epsilon a+W_a+etaHv)-p r³/(2M)]prime=rho r²/(2M).

Regular center fixes the integration constant. At a p=0 uniform-fluid surface Rstar, the leading source mass is m=rho0 Rstar³/(6M). This follows from the fluid Euler equations, not a supplied scalar charge. In the controlled high-density inner core, a approximately g approximately rho0 r/(6M epsilon), agreeing with n2 approximately (rho0+3p0)/(12M epsilon).

The reduced flux b=epsilon a+W_a has the positive inverse

    a=2b(b+A)/[sqrt(epsilon²A²+4b(b+A))+epsilon(2b+A)].

At a<<epsilon A the response is Newtonian with slope epsilon. The finite interval epsilon A<<a<<A has a²/A approximately b. This detuned action has no exact deep-MOND asymptotic at a->0. Equality of the two flux terms occurs at

    a_cross=epsilon A/(1-epsilon²),
    r_cross=12M epsilon² A/[(1-epsilon²)rho0]

for the same uniform source. A linear-core extrapolation beyond this radius is invalid. In the toy r_cross≈2.0002e-10, far below the source surface; extrapolating the center slope to that surface falsely predicts a≈88 instead of the integrated a≈1.27.

For the same reduced high-acceleration flux, slope=1+epsilon gives G_N=G_E/(1+epsilon), G_E=1/(8piM), and operational finite-window a0=(1+epsilon)A. These are a weak-branch dictionary, conditional on admitted background and suppressed clock-flow corrections, not a universal Cavendish result. Vacuum Lambda=3H² is unchanged, so Lambda/a0²=3H²/[(1+epsilon)²A²] remains free. The normalized-clock rescaling symmetry is unchanged because Qepsilon depends on the normalized acceleration. No 32pi selector results.

## Actual bounded conserved source and continuation

Inputs: M=H=A=N0=1, eta=.5, epsilon=.01, rho0=6e6, p0=4. These are dimensionless mathematical controls, not astronomical data. Center data are x=-.16835016905728112, n2=50000030.625843205, b2=100000060.70917374, f2=100000061.22334462. The high-density root approaches the finite pole x=-.16835016835016836 rather than requiring large clock flow.

Radau integration uses t=lnr, exact fluid stress and conservation, a scaled numerical Jacobian, and controlled r³/r² higher center terms at r0=1e-13. Those terms are required for accurate initialization of the small center mode; the action contains |a|³ and does not require a complete analytic series. Their equations are 3epsilon n3+(eta-3x)y2=-4n2²/A and 3(4x+eta)n3+[-12x²+2C]y2=0, C=b2+n2-(rho0+p0)/4; b3=3n3-4xy2. These initialization coefficients are not independently symbolically certified in this package. Two tolerance agreement and finite samples support this bounded computation, not a numerical existence certificate.

Both tolerances reach p=0 at Rstar≈8.77305424e-7, with relative surface difference≈2e-9. The leading m≈6.752311e-13. Full Killing-force samples are positive, pressure nonnegative through the surface (within rounding), and weak lnN,lnB remain below1e-4. The same N,B,V,Nprime state is then continued with rho=p=0 to r=3e-5: no exterior clock charge or independent matching constants are added. Surface density jumps but pressure vanishes, so no pressure surface shell is introduced.

At rtol1e-7/3e-8, the exterior takes141747/185021 rhs calls and approximately1.87/2.37 seconds in recorded phase timers. Final lnN≈3.583348861e-6,lnB≈6.755141447e-7,w=-V/(rN)≈.637443395,k=rNprime/N≈6.748227548e-7. Flow endpoints differ by≈5.3e-9; other endpoints agree much more closely. The 41 sampled exterior points have a/A from1.269708 down to.022494, Qaa between.119089 and1.890115, and weak massflux within≈2.2e-6 relative range of the source m. The physical-force/matched-MOND ratio varies .822–1.356; this is not an exact MOND fit. It includes detuning, finite P2 amplitude, flow and boundary-layer corrections.

Qaa>0 here is only an acceleration Hessian diagnostic. The main finite-symbol audit independently shows negative physical high-k directions after Qaa changes sign; its epsilon=.01 threshold a/A≈3.50896 is not reached in this segment. Positive Qaa alone is not full health. Sampled physical F ranges from approximately1 to1.00000717; for each case r_cos=(m/H²)^(1/3)≈8.77305e-5, so the source and final radius are approximately.01 and.342 times r_cos. The latter is not an asymptotically negligible cosmic scale. The budget is per integration phase: exterior calls total326768 across the two cases, fluid calls29186, aggregate355954 (the exact recorded counts are authoritative). This is an aggregate resource statement, not a200k total-run limit. No finite-matrix rank diagnostic or complete time-dependent perturbation test is claimed by this integration.

The original 20k evaluations capped shortly outside the surface. Those exploratory records and historical_20k/core.py are retained. The higher budget demonstrates that those caps were resource failures, not evidence of a matching obstruction. The fresh outer run declares200k evaluations and30s per phase, with aggregate runner wall60s/CPU30s, one numerical-library thread and1MiB logs. No arbitrary initial-step overflow or default-Jacobian failure is promoted to physics.

## Evidence and remaining implication

Authoritative results: exact_a10/10; exact_control_a rejects the actual lapse and density identities when detuning is deleted; critical_control_a rejects the same high-density regular-center target at epsilon0. core_200k_b5/5 includes separately required exterior completion. All inputs and outputs are retained with outer manifest hashes and logs. Check counts are evidence bookkeeping; the center arguments above are the proof.

The first missing implication is a globally normalized on-shell solution joining this conserved source to the chosen cosmological clock/vacuum, with physical finite-gradient perturbative health throughout. The toy fixes central N0=1 but does not impose N->1 at a cosmological outer boundary; finite matching is not that boundary-value theorem. The high-density source has sharp density surface and high-frequency exterior modes; a different pressure/density profile or boundary shooting may change them and requires new recorded hypotheses. This constructive changed-premise route repairs the critical regular-center obstruction at the cost of a Newtonian infrared core, changed measured-force dictionary and free epsilon. It does not supply cold matter identity or select the vacuum ratio.
