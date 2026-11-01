# Independent stress reviews

All delegated reviews were read-only and checked exact artifacts rather than
the author's proposed verdict. Agent agreement is supporting review provenance,
not an independent mathematical certificate or an observational validation.

## Constitutive law and static cores

Reviewer `review_memory_stress` independently reconstructed the energy identity,
latent-energy gate, entropy-volume convexity, active principal symbol, finite
core estimate, physical free-surface condition, radial quadratic identity and
dense/point-mass limits. No substantive algebraic error was found under the
written hypotheses. Positive sound speed does not imply strong hyperbolicity
of the pressureless dormant phase; that limit is explicit in `DERIVATION.md`.

The reviewer reproduced the 10-row static report and checked the later 32
inner-shell comparisons. Direct density quadrature recovered requested mass
fractions to maximum absolute discrepancy 1.12e-10. All comparisons were within
their stated finite range. The smallest paired radius margin over the dust
reference was 0.0527. Only one loading case has the tighter same-implementation
refinement, which does not independently refine all inner-shell radii.

Current reviewed equilibrium source hash:
`11ce9331fa42b9ac97544d80d8e38829fc15de674ab734854c911b4a2c7fab5c`.
Current static result hash:
`532500d5304979819b17d7c603a144442489e1490781e3514b0027463f0a2e49`.
The current static manifest validated against these inputs and outputs.

## Conservative cold-collapse pilot

Reviewer `review_collapse` independently derived semidiscrete energy cancellation
from the interface pressure force, shell-volume derivative, source and node
gravity. This validates the declared discretization, not exact continuum
gravity or conservation by arbitrary time steps. The reviewer checked all
three Radau manifests and the actual inner result statuses.

At 78 exact common samples through t=3.85, the maximum N64/N128 relative
differences were 0.06145% in 5%-mass mean density, 0.07312% in 10%-mass mean
density, 0.01218% in half-mass radius and 0.01450% in outer radius. Maximum K
differed by up to 1.86%. The time-refined N64 run agrees in 5%-mass density to
2.84e-8 relatively on its common interval through t=1.2. These are early
refinement observations, not a continuum theorem or late-time convergence.

No stored state has a half-density crossing. The reported core-radius field
therefore uses a fallback outer radius and is not a resolved core measurement.
The late N64 state still breathes: its final velocities are inward, viscosity
is active in 18 cells, and acceleration RMS is 0.624. From t=0.65 onward every
stored state has outward-decreasing K. The pilot consequently supplies no
settled-core or convective-stability result.

The reviewer also exercised the short explicit rejection path. It recovered
from two invalid shell stages without changing accepted states. Intermediate
negative-memory extensions can be large in rejected explicit attempts; the
preserved Radau evaluations have only tiny such excursions and no domain
rejections. Accepted negative K is an error, not a projected state. The logged
`attempted_step` is a pre-call bound and need not equal an internal SciPy trial
after adaptive shrinkage. These implementation limits do not change the
finite Radau result interpretation above.

The collapse and material hashes match the preserved Radau snapshot. Current
tests differ from the copied test source only by removal of an import guard.
All nine collapse tests passed in the independent review. The reviewer did
not inspect the subsequent entropy-endpoint construction.

## Exact entropy endpoint

Reviewer `review_endpoint` identified the continuous proxy's parcelwise
entropy counterexample, actual RK45 method, and the difference between
shooting residuals and numerical error. The exact mass-parcel repair was then
independently audited. Every original parcel coefficient is constant on its
full mass interval and scaled by alpha>=1, removing the counterexample.
No substantive equation or implementation defect was found in the declared
finite domain.

The reviewer reconstructed the mass-coordinate equations, central expansion,
contact restarts, pressure continuity, density ordering, energy terms, source
lineage, same-entropy loading and residual acceptance. All 13 endpoint tests
passed independently. An orthogonal radius-coordinate enthalpy integration
used independent bracketed EOS inversion and contact restarts. It agreed to
7.07e-7 relatively in mass, 3.53e-7 in radius, and 8.61e-7 absolutely in energy,
supporting the declared 2e-6 acceptance scale. Smaller internal shooting
residuals are not substituted for these independent checks.

A separate analytic reviewer checked cancellation of radial contact terms
under continuous xi, P, and Delta P, and the restoring buoyancy sign of downward
density jumps. The energy-envelope identity uses actual W including the latent
constant. Neither review proves full nonradial/global stability or dynamical
access to the endpoint. Current exact endpoint source hash:
`d52a0840f601ceb89389b0b6b7b01fd48a498d40bca3f481917e177f0e97df29`.
