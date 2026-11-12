# Focused audit of the angular-acceleration / BAO construction

Primary verdict: **conditional on a named input** — observational identification of T=D_Aa₀ under constrained radial baryonic shape and geometry. The restricted algebra is correct; an unrestricted nuisance-free or all-theory claim is refuted by the counterexamples below.

## Claim card

For positive distance D, global stellar multiplier U, acceleration a₀ and fixed angular baryonic template b, consider independently measured circular speeds with the specified pointwise simple-μ or quadratic law. If the data contain distinguishable responses to A=DU and T=Da₀, the stated coefficient ratios identify T independently of a global b calibration. With independent BAO distances and a Friedmann background with constant gravitational coupling ratio g_G, the joint coefficient is 8πg_G/(3κ²).

Domain: positive scales, finite nonzero redshifts for the BAO distance ratio, known force-law convention, identifiable angular geometry, common sound horizon, distance duality where surface brightness is converted into the mass template, separately conserved specified background components. For the two-radius inverses, the relevant denominator and positive coefficients must exist. The photometry-only, single-speed, exact deep-limit, exact Newtonian-limit, arbitrary-gradient and unrestricted modified-background cases are not covered.

The claim is a measurement construction. No observed T, κ, dark-energy evolution or model likelihood is measured by this audit. κ=1/2 is not derived.

## Dependency graph

1. Independently measured angular light and resolved circular speeds + geometry/population/gas assumptions → a restricted b(θ), w(θ) inverse problem. **Empirical input, presently incomplete for the proposed Euclid sample.**
2. Specified pointwise law → linear coefficient identities → T cancellation. **Internal algebra, independently reconstructed.**
3. Different radial response directions → locally full-rank information matrix. **Internal algebra, not a guarantee after nuisance projection.**
4. Independent BAO d_M,d_H + inferred T → q=a₀r_d/c² and h=Hr_d/c. **Definitions and distance convention.**
5. Friedmann closure + conserved components + constant g_G and κ + density portal → coefficient C_DE=8πg_G/(3κ²). **Conditional physical assumptions and algebra.**
6. Full-rank redshift columns + joint correlated likelihood → a testable coefficient. **Statistical/empirical obligation, not yet executed.**

No step may infer T by first imposing the relation that step 5 is intended to test. That would make the observational argument circular.

## Obligation matrix

| Obligation | Status | Decisive evidence |
|---|---|---|
| Units, positive branches and two linear estimators | Passed under stated laws | Independent reconstruction in route_joint_upstream_review.md |
| Global light/M/L normalization cancellation | Passed under one-template scaling | Explicit transformation of both coefficients |
| General disk AQUAL inherits linear identities | Failed as a general inference | Angular covariance survives, but the nonspherical field equation need not equal the pointwise algebraic rule |
| Radial information condition | Passed for the specified independent-error toy model | Cauchy–Binet determinant; exact deep/Newtonian rank loss |
| Arbitrary inclination/velocity-scale cancellation | Failed | T scales with velocity squared; unknown inclination gives an amplitude degeneracy |
| Arbitrary radial M/L or gas cancellation | Failed | Positive-density flat-curve family produces the same velocities for every positive a₀ |
| Sound-horizon cancellation in the normalized redshift ratio | Passed | Both distances contain the same r_d |
| Joint coefficient identifies local κ without coupling convention | Failed | It identifies κ/√g_G; the September scales audit already establishes this |
| Full Friedmann/modified-gravity generality | Conditional | A specified background equation and species inventory are necessary |
| No hidden redshift rank degeneracy | Conditional | q² proportional to the matter column is an exact counterexample |
| Real-data precision and coverage | Not addressed by the algebra | Requires nuisance-projected realistic profiles, selection and full likelihood |
| New fundamental theory or literature novelty | Not established | Prior inverse-cosmology and shape-estimator work overlaps; no action constructed |

## Review and computation provenance

The upstream and joint reviews independently derive the key steps from the definitions, rather than importing the author's checking implementation. The reviewer had earlier participated in the release audit, so this is independent derivation within the same research session, not blind external peer review. Its source hash records the route revision read; later addenda are separately identified. Root then checked the normalization, coupling correction, boundary cases and claim restrictions.

The redshift synthetic computation covers 54 deterministic cases and the declared symbolic identities; the spectral computation covers 225 exact rational centroid cases plus specified counterexamples. The catalogue run independently reproduces the quality-selection output from pinned ZIPs. None is an astronomical likelihood run. Completed manifests and validators establish file/run provenance, not a theorem or theory verdict. Failed implementation runs are retained and excluded from mathematical evidence.

## Strongest safe statement and next check

The proposed T observable removes a global mass normalization within the restricted inverse problem, and the subsequent BAO construction can avoid an absolute ruler and early matter-density prior. It retains radial-shape, dynamics, inclination, coupling and cosmological-closure assumptions. The cheapest decisive continuation is to project the T sensitivity against realistic nuisance directions and independent constraints, then hold out resolved radial information. If the remaining direction is rank deficient or prior dominated, the route needs new measurements rather than more claims of cancellation.
