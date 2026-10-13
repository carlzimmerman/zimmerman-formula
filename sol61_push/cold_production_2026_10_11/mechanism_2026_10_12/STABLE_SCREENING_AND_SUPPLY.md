# Stable screening and a supply-limited alternative

12 October 2026. Base workspace HEAD when this continuation started: 1667f7ee58936103d14ae03bc36a44c9fb02cf70. This is a continuation of MECHANISM.md, not a claim that the halo mechanism has been found.

## A genuine repair: homogeneous scalar stability

Add a positive mediator mass term to the trial extension:

    E(n,chi) = k n² + b chi²/2 + a |chi|³/3 + g n chi,
    a,b,g,k > 0, b = bare mediator mass squared.

Writing z=-chi>=0, stationarity gives b z+a z²=g n. Therefore

    z=2gn/[b+sqrt(b²+4agn)],
    M_eff²=b+2az=sqrt(b²+4agn),
    d²E_eff/dn²=2k-g²/sqrt(b²+4agn).

The homogeneous Hessian is positive semidefinite for every n>=0 if 2k>=g²/b. A strict inequality gives a strictly positive compressibility contribution everywhere. This fixes the earlier zero-temperature instability within this trial mean-field model. It is not a relativistic quantum stability proof; gravity, gradients, baryon response, and finite-temperature dynamics are separate. The density coupling can preserve the carrier's number symmetry, but the previous Hamiltonian bound must be rederived for the extended action.

## Why that repair still fails the requested heating law

For distinguishable particles of reduced mass mu with fixed-strength Yukawa potential alpha exp(-M_eff r)/r, the weak-coupling Born differential cross section is

    d sigma/d Omega = 4 mu² alpha²/[M_eff²+2mu²v²(1-cos theta)]².

Integrating with momentum-transfer weight 1-cos(theta) gives

    sigma_T = [2 pi alpha²/(mu² v⁴)] F(x),
    x=4mu²v²/M_eff²,
    F(x)=ln(1+x)-x/(1+x).

The standard equal-mass version appears in [Tulin, Yu and Zurek, arXiv:1302.3898](https://arxiv.org/pdf/1302.3898). Here the angular integral is independently checked, and the use of reduced mass explicitly states the distinguishable baryon/carrier convention. This expression applies only in the Born regime; it must not be extended through strong-coupling resonances.

Define local logarithmic slopes A=d ln(sigma_T)/d ln(n), B=d ln(sigma_T)/d ln(v), with the other independent variable fixed. Let p=d ln(M_eff²)/d ln(n) and q=d ln(F)/d ln(x). Then exactly

    p=2agn/(b²+4agn), 0<p<1/2,
    q=x²/[(1+x)²F(x)]>0,
    A=-p q,
    B=-4+2q.

The simple heating route requires sigma_T proportional to n^-1 v^-2 under the energy-per-collision assumptions in MECHANISM.md. That means A=-1 and B=-2. But B=-2 forces q=1 and hence A=-p>-1/2. In the asymptotic density-dominated limit the best possible value is -1/2. Conversely, A approaching -1 requires p approaching 1/2 and q approaching 2, which gives B approaching 0. **No choice of positive constants in this fixed-coupling Born model gives the desired pair of local slopes.**

At x=2.162581587, B=-2; the high-density A is -1/2. At x=0.01, A=-0.9934 in that limit but B=-0.0264. Eleven symbolic/numerical checks pass in screening_run/. The analytic slope identity, rather than the finite grid, supplies the class-specific obstruction. This is a self-review, not an independent-agent audit. It does not exclude different energy-per-collision laws, density-dependent vertices, nonlinear screening responses, inelastic channels, or nonperturbative scattering.

Even positive incoherent sums of these fixed-coupling Born channels retain the obstruction: each A_i>=-(B_i+4)/4, and the slopes of their sum are cross-section-weighted averages. Thus B_total=-2 implies A_total>=-1/2. Interference is outside this extension.

## Different route: energy supply limits the heating

A density cancellation can arise without a 1/n microscopic cross section. Introduce an explicitly modelled energy-carrying bath, with local energy density U, source j_b=epsilon(v) rho_b, absorption rate Gamma_abs=c kappa_abs rho_c, and escape time t_esc:

    dU/dt = j_b - Gamma_abs U - U/t_esc,
    Q_c = Gamma_abs U.

This is a proposed local transport approximation, not a derived new interaction. For fixed coefficients its stable stationary solution is

    U_eq=j_b/(Gamma_abs+1/t_esc),
    Q_c=j_b tau/(1+tau), tau=Gamma_abs t_esc,
    relaxation rate=Gamma_abs+1/t_esc>0.

When tau>>1, Q_c approaches epsilon(v) rho_b regardless of rho_c; the heating per cold mass is then proportional to rho_b/rho_c. For tau<<1 it goes to zero with rho_c, avoiding an unphysical finite heating rate with no absorber. Its logarithmic density slope for Q_c is 1/(1+tau), ranging from one to zero. The radiation/bath energy equation accounts for stored and escaped energy. If baryons power j_b, their energy equation must include -j_b; the energy-budget obstacle does not disappear. If another sector powers it, that sector must be included instead.

This supplies a physical *type* of density saturation, not the complete mechanism. It needs an actual emissivity, absorption vertex, optical depth, and spatial transfer solution. It also exposes a second requirement: the desired heating is epsilon(v)=C a0 v. A constant emissivity per baryon mass does not provide it. Under the earlier conditional crossing-time transport estimate L proportional to V^5/G, constant epsilon produces V^5 proportional to M_b, whereas epsilon proportional to V gives V^4 proportional to M_b. An emissivity chosen proportional to V simply to match the answer would be an assumption, not a derivation.

## Current decision

The mass-floor scalar is stable in its stated homogeneous model but fails the joint density/velocity heating requirement in the Born class. Adding more positive incoherent channels of the same kind cannot repair that particular failure. Do not spend further runs retuning those constants.

The supply-limited bath is an open, distinct route: it naturally saturates density dependence and regulates the empty-density limit. Its first unresolved implication is a derived source/absorption process that supplies epsilon proportional to a0 v, with a conserved energy budget and viable transport. It does not derive the vacuum value of a0 or the halo attractor. A full spatial calculation is premature until that source is specified. Strong-coupling scattering remains another open route, but would require a fresh phase-shift calculation and environmental averaging, not extrapolation of the Born formula.
