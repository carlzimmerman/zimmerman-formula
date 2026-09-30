# Shared scale and coupling selection — 2026-09-29

**Original target remains OPEN:** derive Lambda/a0²=32pi without inserting that relation as a coupling choice. Units below have c=1. With Lambda=8pi G rho_vac, the same target is G rho_vac=4a0². These calculations do not establish exactness of the observational coefficient.

The new result is a coupled-field counterfamily: making the scale dynamical, letting it set the tensor gravitational coupling, and stabilizing its vacuum do not alone select the coefficient. An independent renormalization-flow example does select a ratio, but supplies neither the required gravitational coupling nor a MOND response. This narrows the missing implication; it does not rule out every possible theory.

## A. Include gravitational feedback before minimizing

Use the metric scalar-tensor action

    S = integral sqrt(-g) [F(chi) R/2 - (grad chi)²/2 - U(chi)]
    F = xi chi²
    U = chi⁴ [lambda + A(chi²/v² - 1)²]

with xi, lambda, A, v positive. Assigning a0=gamma chi is an explicit additional dictionary, not a force derivation.

For constant chi, the metric equation gives Lambda=U/F and R=4U/F. Substitution into the scalar equation gives exactly

    F' R/2 - U' = -4 A chi⁵ (chi²-v²)/v⁴.

The lambda term cancels. Thus chi=v is a vacuum for every positive lambda. A fixed-metric minimum of U would miss this cancellation. At that vacuum,

    G_tensor = 1/(8pi xi v²)
    rho_vac = lambda v⁴
    Lambda = lambda v²/xi
    Lambda/a0² = lambda/(xi gamma²).

The target therefore requires the extra relation lambda=32pi xi gamma². The field equations have not imposed it.

In Einstein units with reference Planck mass set to one, the scalar kinetic factor and potential are

    Z = (1+6xi)/(xi chi²) > 0
    V_E = [lambda + A(chi²/v²-1)²]/xi².

At chi=v, V_E''=8A/(xi²v²)>0. The scalar mass factor V_E''/Z=8A/[xi(1+6xi)] is independent of lambda. The conformal kinetic formula was checked against [Galtsov, EPJC 80, 443 (2020), Eq. (9)](https://link.springer.com/article/10.1140/epjc/s10052-020-8017-4).

Holding xi, gamma, A and v fixed, lambda can give 16pi, 32pi or 64pi while preserving the scalar vacuum, assigned response scale, tensor coupling and these local signs. The normalized substitutions are algebraic examples, not cosmological fits; taking gamma small and lambda proportional to gamma² can lower the curvature scale. G_tensor is not automatically the measured Newton coupling when scalar exchange contributes. No full galaxy action or perturbation analysis is claimed.

More generally, constant-scalar monomials F proportional to chi^m and U proportional to chi^n in dimension d>2 require n=dm/(d-2), but leave the height coefficient free. Dimension selects a power, not its normalization.

## B. Horizon regularity does not close this family

The Euclidean four-sphere has radius squared 3/Lambda and regular period 2pi sqrt(3/Lambda), for every positive lambda above. Its on-shell action is

    S_E = -24pi² xi²/lambda.

There is no interior stationary point as lambda varies. More fundamentally, lambda is a coupling, not a variable field, so differentiating with respect to it would require a new mechanism. Regularity supplies no relation to the independently assigned a0. A quantum probability measure has not been supplied or inferred from this action alone.

## C. Four components do not supply the missing factor four

For four free unconstrained scalars with local gradients partial_mu phi^a=q delta_mu^a, compute the full stress tensor, including variation of sqrt(-g).

With positive internal metric delta_ab and kinetic coefficient K>0:

    rho = 2Kq² + U0,   p = -U0.

This is not vacuum stress because rho+p=2Kq². With Lorentzian internal metric eta_ab:

    T_mu_nu = -(Kq²+U0) g_mu_nu.

The vacuum density is Kq²+U0, not four times Kq². Moreover, the time-derivative Hessian K eta_ab has one negative eigenvalue. The latter local ansatz contains a ghost in this free unconstrained model. Metric/lapse differentiation independently reproduces both stress results. Constraints, higher derivatives, nonlinear condensates and global de Sitter configurations are outside this test.

## D. Try genuine ratio selection

An independent candidate mechanism is flow toward a universal ratio. The input is the massless flat-space Gross-Neveu-Yukawa action with quartic term lambda4 sigma⁴/24, Yukawa coupling y, and N=4N_f. The one-loop beta functions are taken from [Fei et al., arXiv:1607.05316v3, Eq. (2.1)](https://arxiv.org/html/1607.05316v3). Set d=4, Y=y² and r=lambda4/Y. Direct differentiation gives

    dr/d(log mu) = Y [3r²+(N-6)r-12N]/(16pi²).

There is a unique positive ratio root

    r_plus = [6-N+sqrt(N²+132N+36)]/6,

and 0<r_plus<12 for every N>0: the polynomial is negative at zero, positive at twelve (exactly 360), and has roots of opposite sign. Writing u=log(Y_initial/Y), the ratio equation becomes dr/du=-[3r²+(N-6)r-12N]/(N+6); the positive root attracts positive initial ratios in the infrared. This is a fixed ratio while the couplings approach the Gaussian point, not a nonzero interacting four-dimensional fixed point.

We integrated both original coupling equations independently and compared their ratio with the analytic solution for N=4,8,40,400, initial r=0.5 and 10, Y_initial=0.05, log(mu/mu_initial) down to -100000. All eight comparisons passed; maximum absolute ratio discrepancy was below 1.7e-13. This tests the stated one-loop equations, not the accuracy of a quantum-gravity approximation.

A hypothetical identification lambda_vac=lambda4/24, gamma=y would give C=Lambda/a0²=r/(24xi). For the illustrative choice xi=1/6 this yields C<3, far below 32pi. The positive value xi=1/6 is not symmetry-selected in the induced-gravity action above. Matching 32pi requires choosing xi=r_plus/(768pi), still a free input. A Yukawa mass scale is not a derived MOND acceleration.

These beta functions are **not** those of the stabilized nonminimal action in route A. Its extra interactions, gravitational running, curvature counterterms and thresholds have not been included. The GNY model by itself supplies no selected nonzero chi vacuum, observed cosmological constant or stream-mediated galactic force. Combining the two calculations does not make a completed model.

## Evidence and next discriminator

Two bounded runs retain scripts, contracts, raw output, results and manifests:

- `runs/shared_scale`: 21/21 exact/local checks.
- `runs/rg_ratio`: 26/26 symbolic and numerical checks.

Passing these checks verifies the scoped calculations, not the desired theory. The predeclared routes and bounds are in `SHARED_SCALE_CONTRACT.md`; executable contracts are in `contracts/`.

The strongest next route is a single specified action and state from which both the response functional and renormalized vacuum stress can be calculated. The earlier exact inverse distribution reproduces P2 only under an assumed response prescription. The through-stream calculations establish a possible energy pump only in their tested sector. Neither yet identifies a0 and rho_vac from the same state.

A useful success test is to vary every independent dimensionless coupling and allowed vacuum counterterm after deriving both observables. If C changes continuously, that action does not predict it; an additional dynamical or symmetry relation is required. If a coupling flow selects a ratio, its relation to measured G and the derived MOND scale must also be fixed. The original 32pi problem is still unsolved; the missing relation is now explicit rather than hidden in a normalization.
