# A structural coefficient obstruction

Verdict: proved for the canonical-clock equations and lambda>1; observational interpretation conditional on the source transfer in CLOCK_BBN_RESULTS.md. This is a self-review, not an independent referee audit.

Let C=Lambda_geom/a0_N², R=G_cosm/G_N, and D>0. With zero additive vacuum constant, CANONICAL_CLOCK_RESULTS.md gives

    C=4D(1+D)²/[3(3lambda−1)],
    R=2D/[(1+D)(3lambda−1)].

Eliminating lambda without imposing any target coefficient gives

    C=(2/3)R(1+D)³,
    lambda>1 iff D(1−R)>R.

Hence 0<R<1 and D>R/(1−R), so

    C > (2/3) R/(1−R)³.

The lower bound increases strictly on 0<R<1, since its derivative is (2/3)(1+2R)/(1−R)^4. If R>=r>0, then C>(2/3)r/(1−r)^3. No scan or special parameter choice is needed. Equality is an excluded lambda=1 boundary.

Using only the conditional historical BBN lower endpoint r=0.92 from CLOCK_BBN_RESULTS.md gives

    C > 1197.9166667 > 11.9158974 × (32π).

Thus adjusting D, lambda, or microscopic parameters that only enter through these quantities cannot simultaneously achieve the target and the transferred BBN interval. As R approaches unity from below, the bound diverges. This is stronger than showing that a single fitted candidate fails.

## Other kinetic branch

The local principal scalar kinetic coefficient is 2(3lambda−1)/(lambda−1). Its other positive interval lambda<1/3 has negative G_cosm=2G/(3lambda−1), for positive bare G. It cannot produce the stated real homogeneous expanding solution with positive U0 and ordinary positive radiation density. The interval 1/3<lambda<1 has negative scalar kinetic coefficient. Neither is a healthy positive-density escape within the assumed action. A different action or negative additional stress would require a new analysis.

## Additive vacuum term

Adding a field-independent V leaves q0 and the static coefficients unchanged, while C_total=C_base(1+V/U0). If one retains the same expansion-coupling bound and imposes C_total=32π, then

    −V/U0 = 1−32π/C_base > 0.9160784989.

The residual U0+V stays positive. This cancellation is mathematically permitted; no protection, dynamics or quantization selecting its value has been derived. It must not be reported as an explanation of 32π. If the local Newton calibration, matter content or coupling evolution changes, rederive the observational transfer and this application rather than carrying the number over.

## Evidence and route decision

clock_coefficient_bound.py passes four symbolic identities and nine parameter-sample checks; runs/clock_coefficient_bound records provenance. The analytic inequalities, not the samples, establish the all-parameter statement. The identities are algebraic consequences of the assumed phenomenological action; they do not prove that action's microscopic origin or full dynamical health.

This closes the route of rescuing the existing standard-radiation, constant-coupling action solely by choosing different positive parameters. A useful new route must change the relation between vacuum energy, local Newton calibration and cosmological coupling, while independently fixing the coefficient. Extra radiation, coupling evolution and a protected vacuum subtraction remain possible mechanisms to investigate, not established solutions. The previously audited causality obstruction remains a separate requirement.
