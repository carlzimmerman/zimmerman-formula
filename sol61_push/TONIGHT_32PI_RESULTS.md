# 32pi tonight: exact inverse response, still no coefficient selection

**32pi remains OPEN.** A substantive mathematical result is an explicit, regular fluctuation distribution that reproduces the entire P2 inverse law under a declared mean-magnitude response prescription. Its vacuum normalization does not give 32pi. The prescription and state are reconstructed from the desired force law; they are not derived physical dynamics. This distinction is essential.

Base and scope: `TONIGHT_32PI_CONTRACT.md`. New bounded evidence: `runs/tonight/` (34 checks), `runs/inverse_response/` (14 checks), `runs/action_bridge/` (6 checks). All three runs completed successfully. The original theory and coefficient success criteria remain unchanged. This is self-review, with independent symbolic identities and direct quadratures; no independent-agent referee was used. No claim of literature novelty is made.

## 1. A published route requires a missing response map

Primary sources checked online: [Kanatchikov and Kholodnyi, arXiv:2311.05525v1](https://arxiv.org/html/2311.05525v1), and the corrected later account [arXiv:2608.12404v1](https://arxiv.org/html/2608.12404v1). For the later account, HTML and PDF text agree on the equations used below. Its existence was already noted by the repository's September 23 sweep. Earlier `agentT4_Zeff.py` calculated its scale ratio; the present audit tests the observable and inversion.

The later source uses zero-mean isotropic spin-connection fluctuations, variance h²=a_star²/2, and Lambda=lambda a_star². Its Eq. (35) gives A=sqrt(b²+h²), with b=GM/r². Section 5 sets g=A-h but subsequently gives b=sqrt(g²+h²)-h in Eq. (44). The scale identification is a0=2h, with lambda=3 quoted for the ordering prescription. These are the limited source inputs used here; the full quantum formalism is not audited.

Independently invert the first equation, without an expansion:

    g = sqrt(b²+h²)-h
    implies b² = g²+2hg.

The stated Eq. (44) instead implies

    g² = b²+2hb.

These are different maps. At b=h=1, the first gives g=sqrt(2)-1, while the second gives g=sqrt(3). In the weak-source limit, the first suppresses response, g~b²/(2h); P2 requires g~sqrt(2hb). Relabeling variables can posit another constitutive relation, but cannot derive that relation by this substitution. This is a gap in the specified argument, not a disproof of every precanonical-gravity construction.

Also, for a fixed source and zero-mean additive vector noise xi,

    E[b e+xi] = b e,
    E[|b e+xi|²] = b²+E[|xi|²].

The first is a mean vector acceleration; the second is an RMS. Only the first directly supplies the ensemble mean equation in this additive model. A fluctuation variance is not automatically an attractive mean orbital force. To mimic P2 in the second moment would require E[|xi|² | b]=a0 b, a source-dependent state rather than constant vacuum noise. Likewise a source-independent homogeneous relative-noise structure function cannot equal a0 GM/r² for every baryon mass at the same radius. Source-conditioned correlations and their dynamical effect must be derived.

Even accepting the stated scale identification gives Lambda/a0²=lambda/2=3/2. Obtaining 32pi requires lambda=64pi, which is not the cited ordering value. Elimination of the UV scale alone does not close the coefficient.

## 2. A specific attempted rescue exposes state dependence

Consider a different **hypothetical modified-inertia prescription**, treating g as imposed acceleration and b as response:

    b(g) := E[|g e+xi|]-E[|xi|].

This is an extra constitutive assumption, not the mean geodesic equation above. For an isotropic radial probability density p(R), direct angular integration gives

    E_angle[|g e+xi|] = R+g²/(3R),  R>=g;
                              = g+R²/(3g),  R<=g.

If E[1/R] is finite, then b(g)=g² E[1/R]/3+o(g²). Hence its putative MOND scale is a0=3/E[1/R]. A variance alone does not determine that inverse-radius moment.

For the cited Yukawa amplitude, the normalized radial density is p(R)=(2/a_star) exp(-2R/a_star). The rescue has a logarithmic susceptibility:

    b(g)/g² = (2/(3a_star)) log(a_star/g)
              + [11/9-(2/3)(EulerGamma+log(2))]/a_star + o(1/a_star).

There is no constant deep-MOND a0 in this limit. Three independent quadratures verify the expansion. The Yukawa function also satisfies a modified Helmholtz equation with a delta source at R=0 and has divergent ordinary gradient norm. A point-interaction domain or a different quantum measure may address that issue; neither is supplied by this scalar-function calculation. The finite-gradient criterion here is ordinary Euclidean H1, not a claimed universal quantum-gravity health condition.

As a controlled regularization, take a gamma radial family with shape k and choose its scale so E[R²]=a_star²/2. The same rescue yields

    Lambda/a0² = 2lambda k(k+1)/(9(k-1)²),  k>1.

In this family ordinary gradient norm is finite for k>2; its ratio is then below 4lambda/3. With lambda=3, solving for 32pi requires k=1.125995..., outside that finite-gradient subfamily. This is a restriction on that family, not a bound on all probability states. The shape was not dynamically selected.

## 3. Exact inverse construction: the whole P2 law can be represented

Instead of guessing a distribution, demand the exact response b(g)=sqrt(g²+h²)-h. In three-dimensional acceleration configuration space,

    Delta² |g-vector - xi| = -8pi delta³(g-vector-xi).

Applying this identity to the convolution fixes the isotropic vector probability density uniquely:

    P_h(xi) = 15 h⁴/[8pi (|xi|²+h²)^(7/2)].

It is positive, smooth, normalized and has finite ordinary gradient norm for its square-root amplitude. Its exact moments are

    E[R] = h,
    E[1/R] = 3/(2h),
    E[R²] = 3h²/2,
    integral |grad sqrt(P_h)|² d³xi = 7/(3h²).

For completeness, the convolution of this density with the norm and the desired function sqrt(g²+h²) have the same bi-Laplacian. Their difference is a smooth radial biharmonic function. The radial biharmonic basis is 1, g, g², 1/g: smoothness excludes g and 1/g, and the shared asymptotic U(g)-g->0 excludes the constant and g² terms. The latter limit follows by dominated convergence from the finite first moment and zero vector mean. Hence the convolution is exactly sqrt(g²+h²), and E[R]=h supplies the subtraction at zero. Direct angular/radial quadrature verifies the response at g/h=0.01, 0.1, 1 and 10, independently of that argument. This construction realizes a0=2h across the full interpolation, not just its leading power.

This is an **inverse representation theorem under the proposed response rule**. It was obtained by using P2 as input. It neither selects the state nor converts mean magnitude into a force derived from an action. The corresponding scalar operator can likewise be reconstructed:

    psi=sqrt(P_h),
    H=-Delta+V,
    V(R)=(35R²-42h²)/[4(R²+h²)²],
    H psi=0.

R here is fluctuation acceleration magnitude, not galaxy radius. V was derived from the chosen psi; presenting it as an independently discovered physical Hamiltonian would be circular.

There is a valid static variational bridge, which avoids confusing a mean magnitude with a mean geodesic acceleration. Define

    W(g) = [g sqrt(g²+h²)+h² asinh(g/h)]/2-hg,
    L_static = -W(|grad Phi|)/(4piG)-rho_b Phi.

Then W'(g)=b(g), and variation gives div[(b(g)/g) grad Phi]=4piG rho_b. In spherical symmetry this realizes P2 with a0=2h. It has the same calibrated Newtonian G, since W~g²/2 at large g, and W~g³/(3a0) near zero. It is precisely the earlier reconstructed P2 AQUAL primitive, now given an inverse probability representation. A microscopic derivation of this averaging functional is still absent. Adding C h² to W leaves the static force unchanged; interpreting that term as a covariant vacuum energy would require C=64pi under the declared normalization. That is a selected height, not a result of the variation.

The state also shows why the vacuum dictionary must be derived again. If one **additionally** retains Lambda=lambda a_star² and matches a_star² to twice the variance, then

    Lambda/a0² = 3lambda/4.

At lambda=3 this is 9/4, not 32pi. The target would require lambda=128pi/3. If one instead defines the scale by a_star² integral|grad psi|²=1, the ratio is 3lambda/28. That alternative is a diagnostic, not a derivation of the source's full metric condition. The two scale dictionaries differ by seven. Transferring the Yukawa state's variance/operator relationship to a different state is unjustified.

## 4. Locking vacuum pressure does not fix response normalization

The repository's pressure route removes an additive freedom by setting a0²=kappa² G[-K(Q)]. Test it with a fixed DBI pressure minimum:

    K(Q)=-T+T[1-sqrt(1-Q²/L²)],
    K(0)=-T,  K''(0)=T/L²>0.

The height and Hessian are independent of kappa. At the minimum, a0²=kappa² GT and Lambda=8piGT, giving Lambda/a0²=8pi/kappa². The same vacuum admits kappa=0.4, 0.5 or 0.6 in this family. They give coefficients 157.080, 100.531 or 69.813.

For each positive scale the spherical P2 AQUAL inverse has mu(x)>0 and

    mu(x)+x mu'(x)=2x/sqrt(1+4x²)>0.

Thus background regularity and static ellipticity do not select 1/2, even after vacuum height is locked. This reproduces the normalization freedom in a setting that already ties the two scales; it is not a new generic vacuum-offset result. No full covariant health certificate is asserted for this separated diagnostic family.

## Decision and remaining executable obligation

The original goal is not reached. The exact inverse distribution is a concrete target for a physical state-selection mechanism; it is stronger than choosing a favorable phase or matching one coefficient. Any proposed completion of this rescue must derive (i) the response functional as an equation of motion, (ii) the state and its correlations conditioned on the baryon source, and (iii) its absolute vacuum stress from the same operator/action. Only then can the ratio be evaluated. None of the dictionaries tested here gives 32pi without an added condition.

The open continuation is to test a specified source-coupled field/kinetic operator against this inverse target and its vacuum stress, or to find a different mechanism that selects the multiplicative pressure coefficient. Constructing an operator from the target above does not satisfy that obligation. The full two-point precanonical equation and its physical observable map remain unexecuted; a ground-state/measure/domain specification is needed before a coefficient can be extracted. These routes remain open, not exhausted or proved impossible.

Initial exploratory evidence is retained as `initial_tonight_*`: 31/34 passed. Two failures were unresolved positive square-root simplifications, repaired by checking the squared identities with positive branches. One was an actual factor-two error in the expected static ellipticity expression; it was corrected to the independently differentiated value above. Corrected bounded evidence is 34/34, 14/14 inverse-construction and 6/6 static-action checks. Counts verify the scoped calculations, not the physical theory or 32pi.
