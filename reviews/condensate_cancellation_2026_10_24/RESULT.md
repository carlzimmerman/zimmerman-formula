# Condensate cancellation with a retained baryonic source

The microscopic joint-selection goal remains open. A condensate is a genuine way to remove spatial quadratic stiffness while retaining a time kinetic term. It is not automatically a MOND mediator. The new diagnostic below distinguishes the stable homogeneous condensate from its proposed sourced static response.

Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 remain separate and unused. No numerical target or observed normalization enters this calculation.

## Primary sources and the viable part of the idea

[Ghost Condensation, hep-th/0312099v1](https://arxiv.org/abs/hep-th/0312099v1), abstract only: a rolling scalar can have vacuum-like stress and a low-energy k^4 dispersion. Its reported direct spin-dependent force is not the desired baryonic MOND law. The full HTML failed, so no detailed equation attribution is made to this source.

[Ghost Condensate in N=1 Supergravity, 1212.2185v2](https://arxiv.org/html/1212.2185v2), II.1-II.9: cosmological shift-charge dilution admits P_X=0 with positive time kinetic if P_XX>0. Section IV constructs a de Sitter condensate and stabilization. Its displayed small-parameter dispersion, IV.59, is omega^2 approximately -kappa_paper(3 k^2/2+k^4), requiring negative kappa_paper for the stated stabilization. Thus this example has a restored k^2 term; its coefficient has a permitted range, not a unique amplitude prediction. This is not the campaign's kappa. The result is not a microscopic MOND/vacuum matching calculation.

Neither source is refuted by the following different, explicitly sourced P(X) test. Existing clock_flux/RESULT.md supplied the P_X=0 caveat but did not carry out this static branch and source audit.

## Explicit retained-source test

Use signature -+++, c=hbar=1, fixed local weak metric, and

    L=P(X)-q rho_b phi, X=-(partial phi)^2/2, q>0.

The linear source is a local EFT test of the required force, not a completed supersymmetric baryon portal. On phi=v t+psi(r), let y=psi'>0, X0=v^2/2 and X=X0-y^2/2. The baryonic acceleration is -q grad psi. In n spatial dimensions the exterior equation gives

    S_(n-1) r^(n-1) P_X y=q m_b.

For a smooth healthy condensate,

    P=-V+A(X-X0)^2/2+..., A>0,
    P_X y=-A y^3/2+O(y^5).

This has the wrong sign for the attractive outward-gradient branch. Its formal magnitude scales as r^(-(n-1)/3), hence r^(-2/3) in three dimensions, rather than the MOND r^(-1) force. Taking y<0 solves the opposite-sign branch but makes this specified direct scalar force repulsive. The static Lagrangian starts at +A y^4/8 rather than the desired negative cubic. This fixed-metric diagnostic omits gravitational lapse shifts of X and does not exclude a different self-consistent scalar-metric profile.

Now impose the required attractive MOND current P_X y=C y^2 with C>0, rather than guessing P. Since dX/dy=-y, it requires

    P_X=C y, P_XX=-C/y.

The quadratic perturbation action about the local background is

    L2=P_X[(dot pi)^2-(grad pi)^2]/2
       +P_XX[v dot pi-grad psi dot grad pi]^2/2.

The matter-coordinate time coefficient is K_t=C(y^2-v^2)/y. More decisively, for timelike scalar gradient the scalar-rest-frame kinetic coefficient is

    K_rest=P_X+2X P_XX=C(2y^2-v^2)/y.

It is negative for y^2<v^2/2, including the small-gradient condensate regime. This is a genuine wrong-sign time kinetic in that restricted P(X) model, not merely a slow spatial instability. A small higher-spatial-derivative correction does not reverse the leading time-kinetic sign. If additional operators become leading, the P(X) approximation and this conclusion must be reevaluated together. A spacelike branch, extra fields, or a materially different background is outside the calculation.

## Cancellation is not preserved by simply adding the source

For homogeneous fields in n-dimensional expanding space, the stated action gives

    dot J+n H J=-q rho_b, J=P_X dot phi.

Without the source, a^n J is conserved; expansion can drive J toward zero in an appropriate basin. With a persistent source, J=0 is not an exact solution. For fixed H and rho_b the steady value is -q rho_b/(nH), not zero. This fixed-source example is not a conserved-dust cosmology; dilution and energy exchange require their coupled equations. Source removal can recover the vacuum attractor but does not demonstrate cancellation within a baryonic halo.

The simplest shift-preserving alternative also fails to source a static force: integral sqrt(-g) partial_mu phi J_b^mu is a boundary term if nabla_mu J_b^mu=0 and its coefficient is constant. This statement does not cover general derivative, disformal, nonconserved-current or curvature portals.

## Positive vacuum still has an unfixed amplitude

At the homogeneous root, rho=2XP_X-P=-P(X0). A constant P->P-Delta leaves the root, local current and kinetic derivatives unchanged but shifts rho by Delta. Thus the shift symmetry and root condition alone neither fix vacuum energy nor relate it to C and q. In dynamical gravity H changes, so the entire cosmological trajectory is not unchanged. A specific ultraviolet completion could constrain the shift; none has been supplied by this EFT construction.

The mechanism therefore addresses one subproblem, homogeneous quadratic cancellation, but does not jointly supply the healthy sourced MOND branch and selected positive vacuum amplitude. This is not a universal no-go for condensates or supergravity. It does show why combining separately valid claims of a stable condensate and a MOND-shaped action is insufficient: they must describe the same physical branch and the same source coupling.

## Evidence and remaining boundary

Frozen before scripts: ceec4e5b4b. Thirteen symbolic identities pass; these include simple bookkeeping identities and are not thirteen independent physical tests. Reversing the sign of dX/dy produces five expected failures and exit 1. No full cosmological simulation, halo boundary-value solution, source-complete supersymmetric action, radiative-protection proof or independent review is claimed.

A viable continuation must explicitly alter the failed branch/portal assumptions, compute the full physical kinetic matrix and force on that branch, and derive vacuum plus source normalization from the same microscopic data. Adding an arbitrary stabilizer or selecting a favorable initial condition does not meet the original goal. No parameter-free a0 has been obtained.
