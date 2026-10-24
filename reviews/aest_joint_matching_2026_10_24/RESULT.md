# Scalar-vector mixing: a real source mechanism, not joint amplitude selection

The baryonic source subproblem has a concrete escape from the preceding one-field test: metric-vector-scalar mixing can source the scalar while preserving its shift symmetry. This does not yet fix the vacuum, protect the low-gradient quadratic cancellation, or select a0. The requested microscopic mechanism remains unresolved. Kappa=1/2 remains FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate and unused.

## Authenticated sources

[2007.00082v3](https://arxiv.org/html/2007.00082v3), equations 2-6: AeST separates temporal Q and spatial Y using a unit timelike vector. Matter couples to the metric; scalar sourcing comes from gravitational mixing. The cosmological constant is explicitly free, and the MOND normalization is a chosen small-Y coefficient. The quasistatic reduction has an additional mass scale limiting its MOND domain. The homogeneous dust contribution contains an integration constant.

[2109.13287v2](https://arxiv.org/html/2109.13287v2), sections III-V and appendix B: constrained Minkowski perturbations have healthy propagating modes in appropriate parameter regimes, but the nonpropagating sector needs care at low momentum. The nonlinear MOND term is analyzed separately, with boundedness results restricted by the mass scale. The paper leaves de Sitter stability for further investigation. It is not a proof of all-mode stability about every baryon-sourced positive-vacuum halo. The page body carries a later rendered date; identification follows its arXiv version header.

[2304.05134v1](https://arxiv.org/html/2304.05134v1), abstract and sections 2-4: actual quasistatic spherical solutions have Newtonian, MOND and oscillatory regimes; transitions depend on parameters and boundary conditions. These establish more than a guessed source term, but static existence is not a dynamical stability theorem. This audit does not reproduce the numerical solutions or Hamiltonian analysis.

## Explicit source mechanism

Define Q=u^mu partial_mu phi and Y=(g^mu nu+u^mu u^nu)partial_mu phi partial_nu phi, with u^mu u_mu=-1. These are independent invariants. Unlike P(X), their coefficients do not force the timelike kinetic and spatial MOND response onto the failed single-function relation of the previous review.

The vector acceleration J^mu=u^nu nabla_nu u^mu couples through J^mu partial_mu phi. In the quasistatic limit the corresponding mixed spatial action has the structure

    S_stat=-integral {[|grad Phi|^2-2 grad Phi.grad varphi
                      +|grad varphi|^2+J(Y)]/(8 pi Ghat)+rho_b Phi}.

This expression neglects the published mass term only in its stated mass-negligible regime. Set Phi=Phi_hat+varphi. The square becomes |grad Phi_hat|^2 and the matter term becomes rho_b(Phi_hat+varphi). Variation gives

    laplacian Phi_hat=4 pi Ghat rho_b,
    div[J_Y grad varphi]=4 pi Ghat rho_b.

Thus a scalar source emerges after diagonalization even though the underlying matter action has no explicit scalar coupling. This genuinely escapes the previous direct-portal objection. A constant scalar shift changes the reduced source expression only by a field-independent quantity; the original covariant action is shift symmetric.

No claim that the vector is a fixed nondynamical clock is needed. Its own constraints and propagating modes must be included in any health analysis; the cited constrained analysis provides partial evidence, not a complete halo/vacuum certificate.

## Operational normalization and quadratic discriminator

Write the local small-Y expansion

    J(Y)=bY+(2gamma/3)Y^(3/2), b>=0, gamma>0.

For n spatial dimensions, with the displayed action normalization, radial flux is

    S_(n-1) r^(n-1)(b y+gamma y^2)=4 pi Ghat m_b,
    y=varphi'>=0.

In n=3 this gives b y+gamma y^2=Ghat m_b/r^2. For b=0,

    y=sqrt(Ghat m_b/gamma)/r,
    a0=Ghat/(gamma G_N).

G_N is the separately calibrated high-acceleration gravitational constant. The physical total acceleration is Ghat m_b/r^2+y; the latter dominates in the deep regime. The pure cubic field contribution has radial power r^(-(n-1)/2), yielding 1/r only for n=3. No universal dimensional selection of n is inferred.

For b>0,

    y=[sqrt(b^2+4gamma Ghat m_b/r^2)-b]/(2gamma),

so at the smallest gradients y approaches Ghat m_b/(b r^2). The quadratic term therefore spoils a strict deep-MOND limit, though sufficiently small b can leave a finite useful interval. This is a physical force discriminator rather than a field-normalization label.

Analytic mutation: gamma->2gamma at fixed vacuum, Ghat and high-gradient G_N halves a0 and divides the deep scalar force by sqrt(2). This is direct substitution in the exact expression, not a numerical experiment or a fitted selection.

## What the symmetries do not protect

The action's free covariant function F(Y,Q) permits independent operators proportional to

    1, Y, Y^(3/2).

Each preserves diffeomorphism invariance, the scalar shift, and the unit-vector constraint. A constant changes vacuum energy; a Y term restores linear spatial response; a Y^(3/2) term changes the MOND amplitude. For the spatial terms, Y=0 on homogeneous FLRW, so their value and first background variation vanish: they need not alter the homogeneous vacuum. The Y term does alter perturbations, which is precisely the cancellation test. Around an aligned zero-spatial-gradient background, the cubic term begins at third order in gradients and does not fix the quadratic time kinetic coefficient.

To hold high-gradient calibration fixed, multiply the spatial deformations by a smooth function equal to one near Y=0 and zero above a chosen transition interval. This demonstrates allowed functional freedom; it is not proposed as a microscopic mechanism or another fitted parameter. Full constraints, radiative effects and health of any such deformed theory require their own analysis. The point is narrower: the stated symmetries alone do not forbid these operators or compute their coefficients.

Neither requiring positivity of an allowed kinetic matrix nor selecting a minimum of the temporal function equates these three independent coefficients. A new microscopic Ward identity or flow could in principle remove the freedom, but it is absent from the action and the audited sources. Setting gamma proportional to the inverse square root of vacuum energy by hand would simply restate the requested law.

## Exact status

This route genuinely solves a structural sub-obligation: retaining baryonic scalar sourcing without an explicit shift-breaking scalar-matter portal. It provides an established setting in which to study healthier extra-field dynamics. It does not establish a fully stable sourced positive vacuum, radiative protection of b=0, or a parameter-free joint amplitude. No claim of a new theory or universal no-go is made.

Criteria committed before the analytic audit: 0d491d43b2. The derivation and mutation are short analytic substitutions; no executable, numerical scan, simulation or independent review was performed. No fitted a0 or cosmological measurement was used. A successful continuation requires an explicit microscopic restriction on F and its vacuum term, not another freely chosen interpolation function. Goal remains open.
