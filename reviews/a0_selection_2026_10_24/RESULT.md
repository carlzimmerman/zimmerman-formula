# Dark-energy selection: vacuum tracking versus operational response

Status: **no mechanism selecting a0 found**. Three frozen routes tested; none supplies a parameter-free acceleration. This is a structural result for specified models, not a no-go theorem for all completions. Kappa=1/2 remains FITTED. The repository's CFG493 measurements are kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078; neither entered the calculation. Only the dark-energy footing is considered.

Criteria were committed alone as 87e0c60793 before check.py existed. Continuous symbolic couplings were tested, not a menu of numerical coefficients. This work follows the user's request to select the scale dynamically rather than solve an equilibrium with it as an input.

## 1. Can quantum running select the curvature-tracker ratio?

The existing tracker (sol61_push/puzzle_32pi_curvature_tracking_2026_10_15/RESULT.txt) has, in natural units,

    F = M^2 + xi phi^2,    V = E + lambda phi^4/4,
    phi_v^2 = 4 xi E/(lambda M^2),    Lambda = E/M^2.

Thus Lambda/phi_v^2=lambda/(4xi). Positive E, lambda and xi support the previously checked stable local branch. These equations track the vacuum but leave a dimensionless ratio. They do not establish that phi_v is an operational acceleration.

For a minimal massless matter-loop truncation, the primary-source dictionary gives

    beta_lambda = 18 lambda^2/(16 pi^2),
    beta_xi = 6 lambda (xi+1/6)/(16 pi^2).

See SOURCE.md for the source, sign and normalization conventions. Exact integration yields

    I = (xi+1/6)/lambda^(1/3) = constant,
    lambda(t) = lambda_i/[1-18 lambda_i t/(16 pi^2)],
    xi(t)+1/6 = (xi_i+1/6)[lambda(t)/lambda_i]^(1/3).

The arbitrary invariant I carries initial-condition information. There is no nonzero-lambda fixed point in this truncation. The instantaneous zero of beta[lambda/(4xi)] at xi=1/12 is not a fixed trajectory: beta_xi is nonzero there. At lambda=0 the beta functions vanish for all xi, but the finite positive-lambda tracker solution is lost.

Formally extrapolating to the infrared sends xi to -1/6, outside the positive-xi tracker branch; xi crosses zero when [lambda/lambda_i]^(1/3)=1/(1+6xi_i). This is NOT a prediction that the physical massive vacuum must cross: mass thresholds invalidate the massless extrapolation. Decoupling requires the massive flow and does not supply a selection argument here.

**Verdict:** minimal running does not determine the free ratio. Full gravity, extra interacting fields and a nonperturbative fixed point were not tested. Even a fixed ratio would still need a force/transport derivation identifying a0.

## 2. Does exact classical scale symmetry fix the amplitude?

Remove explicit M and E and take two scalars:

    F = xi phi^2 + zeta chi^2,
    V = (lambda phi^4 + 2g phi^2 chi^2 + h chi^4)/4.

For x=chi^2/phi^2, the dimensionless Einstein-frame potential is

    U(x) = (lambda+2gx+hx^2)/[4(xi+zeta x)^2].

An interior stationary point, when its denominator is nonzero and x_star>0, obeys

    x_star = (zeta lambda-g xi)/(h xi-zeta g),
    U_star = (lambda h-g^2)/[4(h xi^2-2g xi zeta+lambda zeta^2)],
    U''(x_star) = (h xi-zeta g)/[2(xi+zeta x_star)^3].

These formulas alone do not guarantee a healthy vacuum; require F>0, positive scalar kinetic metric, positive U_star and positive angular curvature. The radial scale direction remains flat classically. On any allowed interior branch, rescaling all quartics by the same positive s preserves x_star, positivity and scale symmetry, while U_star becomes s U_star. Thus the symmetry permits continuously different vacuum normalizations. Endpoint minima likewise retain the quartic amplitude freedom. Degenerate stationary families do not restore uniqueness.

In general spacetime dimension d>2 the scale-invariant potential has degree 2d/(d-2); the quartic expression above is the d=4 specialization. The canonical conformal coefficient in the plus-F convention is -(d-2)/[4(d-1)], or -1/6 at d=4; it does not force the positive tracker ratio.

**Verdict:** exact classical scale symmetry alone does not select the vacuum amplitude or its coupling to the nonlinear response. This does not exclude an additional quantum principle fixing all relevant dimensionless couplings.

## 3. Can curvature identify dark energy and set the force scale?

In four-dimensional Einstein gravity, with mass densities and c restored,

    R = 8 pi G (rho_m+4rho_v)/c^2.

Consequently a scalar trigger proportional to sqrt(R) also responds to dust. For conserved dust and constant vacuum density its squared trigger varies as rho_m,0(1+z)^3+4rho_v, not as rho_v alone.

There is a more selective construction. In natural units, let u be the normalized dust rest-frame velocity, use signature (-,+,+,+), and include vacuum in the Einstein source. In d spacetime dimensions,

    Lambda_read = [(d-3)R/2 - R_mu_nu u^mu u^nu]/(d-1).

For exactly pressureless dust plus vacuum this equals Lambda. In d=4 it is (R/2-R_uu)/3. With isotropic material pressure P, it becomes Lambda-8piG P; more generally it reads the spatial mean pressure. It needs the matter rest frame and the Einstein equation. It is not a universal vacuum detector for an arbitrary modified-gravity or multistream stress tensor.

**This measures the source; it does not determine the response coefficient.** To exhibit the distinction, conditionally take a preferred-clock effective theory with acceleration b_mu=u^nu nabla_nu u_mu. In homogeneous FLRW the comoving clock has b_mu=0. A covariant term proportional to (b_mu b^mu)^(3/2) therefore has zero background value, first variation and quadratic variation about that clock. In a static aligned weak-field configuration b is the gradient of the physical potential. Such a term can change the nonlinear force response without changing the classical homogeneous vacuum or its linear perturbations.

More explicitly, with fixed baryon coupling and physical potential Phi, write the static deep-MOND action as

    L_static = -F(y)/(8piG) - rho_b Phi,    y=|grad Phi|^2,
    F(y) = 2 y^(3/2)/(3a_star).

Its equation is div[(|grad Phi|/a_star) grad Phi]=4piG rho_b. Now add the symmetry-allowed response term

    delta F(y) = 2 eta y^(3/2)/(3a_Lambda),
    a_Lambda = sqrt(Lambda/3)   (c=1).

The resulting operational scale is

    1/a_eff = 1/a_star + eta/a_Lambda,
    d a_eff/d eta = -a_eff^2/a_Lambda.

Restoring units gives a_Lambda=c^2 sqrt(Lambda/3). The factor 2/3 merely normalizes the derivative of y^(3/2); it is not a prediction for kappa. Eta is an independently allowed Wilson coefficient. At the classical static level a sufficiently small shift preserves positive cubic response, while changing the acceleration scale and preserving the homogeneous vacuum. This demonstrates freedom under covariance and clock symmetries, conditional on this EFT class. It does NOT establish full covariant nonlinear health, quantum radiative stability, or an escape from the repository's failed clock models.

**Verdict:** even an exact dust-vacuum projector does not select a0. A further microscopic constraint must fix the nonlinear response coefficient. An arbitrary choice of eta would reinsert the answer.

## What a successful next mechanism must actually calculate

The open target is a shared microscopic theory that calculates both the vacuum stress and the nonlinear acceleration response, with their relative normalization protected against the deformation above. A mere common dimensionful scale, stable vacuum, fixed background curvature or attractive halo equilibrium is insufficient. Possible additional principles include a demonstrable symmetry identity relating the vacuum and response operators, or a fully specified interacting fixed point with no remaining relevant parameter controlling their ratio. Neither has been exhibited here; naming either is not a mechanism.

A concrete falsification test for any proposed completion is to add the cubic response deformation: if the proposed principle allows it, the principle has not selected a0. If it forbids it, the reason must follow from the microscopic equations and survive the approximations used to obtain the galaxy law. The same equations must then predict another observable. No universal impossibility result or uniqueness of the suggested research directions is claimed.

## Evidence and self-review

- check.py: 14/14 exact symbolic identities pass in run/.
- run_MUTATE/: reversing the conformal offset and rescaling only one quartic makes 6 checks fail; exit status 1 as intended. These are sensitivity controls, not new physical solutions.
- response_check_v2.py: 7/7 exact identities pass in response_run_v2/.
- response_check.py and response_run/ preserve an initial failed derivation: the vacuum sign in R_uu was wrong, and a four-dimensional projector numerator was incorrectly used in general d. Both are corrected in v2. The failed output is not evidence for a physical claim.
- All four manifests validate against their recorded artifacts. Scripts are bounded single-thread symbolic computations; no scans or numerical acceleration inputs. Manifest validation verifies provenance, not theoretical correctness.
- Self-audit: separated massless RG from massive vacuum flow; checked curvature sign and general-d trace; restricted the projector to its matter/frame premises; separated an allowed static response deformation from proof of full model stability. No independent audit was performed.
- Campaign identity checks: no target numerical inputs in executable scripts; no kappa output exists to scale, rename or assign a pi weight. Those numerical-hit checks are inapplicable, not passed. No horizon entropy or uncancelled hbar factor enters. The source beta functions use conventional natural units; their loop factor cancels from the trajectory invariant. This lane makes no EXACT CANDIDATE claim and is registered as free/structural rather than a determinate numerical trial.
