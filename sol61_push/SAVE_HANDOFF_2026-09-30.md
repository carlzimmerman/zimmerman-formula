# Saved research handoff

The exact 32π coefficient remains unresolved. The completed derivations, audit contracts, scripts, and recorded computations are in this folder. The latest completed result is `CLOCK_CONE_RESULTS.md`, committed as 04ea72785: the exact extrapolated retarded clock response fails the finite-cone analyticity test. This does not establish an instability at real spatial momentum or exclude a bounded effective theory with additional high-frequency physics.

The canonical-clock construction in `CANONICAL_CLOCK_RESULTS.md` links the vacuum and galaxy scales, but leaves a free dimensionless combination. It does not derive 32π without imposing it.

## Unfinished next test

Under that construction's stated assumptions, imposing the target gives

    D(1+D)^2 = 24π(3λ−1),  λ>1,
    G_cosm/G_N = 48π/(1+D)^3.

Consequently D exceeds the positive root of D(1+D)^2=48π, and the cosmological-to-local gravitational coupling ratio is below approximately 0.824. This conditional prediction suggests a primordial-nucleosynthesis test.

An observational exclusion has NOT been completed. Before claiming one, verify the BBN-only interval in Alvey et al., arXiv:1910.10730, and its transfer assumptions: constant couplings during BBN, unchanged particle and nuclear physics, negligible extra clock or surface radiation, and the stated local Newton calibration. A CMB-derived bound cannot be imported automatically into preferred-foliation gravity. Additional radiation or evolving couplings require a separate calculation.

Next priority: finish that conditional observational test, then investigate a causal completion that also fixes the remaining coefficient. Do not describe either task as solved or claim global novelty from repository searches.

## Subsequent completed check

The previously unfinished source transfer is now documented in CLOCK_BBN_RESULTS.md. Equation (9) of the checked primary source gives the BBN-only interval [0.92,1.04] at 95.4% confidence. Under the explicit standard-radiation, constant-coupling transfer assumptions, the candidate's entire R<0.8238741 range is outside it. Twelve computation checks and execution provenance are saved. This closes that restricted observational branch; evolving couplings or additional radiation are separate, unverified modifications. Exact 32π remains unresolved.

The subsequent CLOCK_COEFFICIENT_BOUND.md proves the all-parameter obstruction C>(2/3)R/(1−R)^3. With the same conditional R>=0.92 lower endpoint, C>1197.9167, nearly twelve times 32π. An additive constant would have to cancel more than 91.6% of U0. Changing existing parameters alone cannot rescue this branch. Thirteen symbolic/sample checks and provenance are saved; no independent likelihood was computed.

VARIABLE_CLOCK_RESULTS.md changes the constant-coupling premise via lambda(q). It derives the coupled homogeneous equations and a stable vacuum criterion (S U)''>0 with S=3lambda−1. A linear trial lambda=1+ell q has a unique homogeneously stable vacuum and early instantaneous force-balance roots near lambda=1. Sixteen checks pass. This does not prove an evolving solution, local galaxy matching, full stability or coefficient selection. The next executable test is a constrained radiation-plus-scalar trajectory including kinetic energy.

That trajectory test is now completed for five toy initial conditions in VARIABLE_CLOCK_TRAJECTORY_RESULTS.md. All reach the vacuum over 12 e-folds, including ±10% initial-q offsets at ell=10. The independently evolved H² formulation passes 19 checks with maximum relative constraint residual 2.274e−8; failed/sensitive log-H diagnostics are retained. The radiation-only toy has no observational fit or matter era. Next: inhomogeneous scalar health and cosmological-to-galaxy matching for lambda(q); coefficient selection remains unresolved.

VARIABLE_CLOCK_MODES_RESULTS.md now derives the full quadratic scalar action on the constant-q de Sitter vacuum of the local phenomenological model. An exact mode transformation proves fixed-wavevector future boundedness, scalar decay and metric freezing for the positive linear-coupling family; both scalar kinetic coefficients are positive for nonzero momentum. Fifty symbolic/finite checks pass, including twelve mode evolutions and six direct-equation comparisons. This does not establish radiation-era perturbative health, nonlinear strong coupling, causal completion, galaxy matching or 32π selection. Next: match the cosmological q* boundary to local galaxy gravity rather than assuming the flat-static q0 calibration.

GALAXY_SCALAR_MATCHING_RESULTS.md now tests a frozen-curvature weak-static scalar/flux truncation. Eight finite BVPs show a near-vacuum gradient-retaining branch that differs from pointwise relaxation at high local field, and a small-Z case that tracks the local root. Fifty BVP checks, four coefficient identities and eleven comparison-bound checks pass; two failed mesh attempts are preserved. The matched bare ratio is D³(3x⁴−1)/3, x=q*/q0; the previous Newton rescaling is conditional on local relaxation and changes this by (G_N/G)². No full metric/foliation matching or observed Newton dictionary is established. Next: coupled weak-source ADM matching; do not fit free D and ell and call that a derivation of 32π.
