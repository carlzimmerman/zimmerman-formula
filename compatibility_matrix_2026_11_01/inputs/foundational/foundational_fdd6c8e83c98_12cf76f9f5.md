# DR01 — dynamical response of the dilute PN28 field

**Result: the specified field has a computed, conserving kinetic response to
rotating baryonic forcing. This has not yet produced a core-regulation
mechanism.** The calculation includes the field's own gravity, reciprocal
scalar response and canonical-current feedback. It goes beyond FR01's static
compression test. It does not show that a core expands, that contraction is
prevented, or that the galaxy acceleration and cluster laws follow.

The user authorized this calculation and publication on 2026-11-01. Source
snapshots, contracts, implementations, raw results, independent review,
failed reference checks and reproduction commands are included here.

## What was calculated

We linearized the actual PN28 canonical waterbag Hamiltonian around the FR01
dilute `psi_c=.2, epsilon=.01` halo, its compact-baryon endpoint, and its
diffuse-baryon control. The calculation follows the occupied phase-space
boundary with orbital Fourier modes; it does not impose a fluid EOS during
the evolution. The current-feedback term omitted by a frozen-background
tracer calculation is retained.

The unresolved scalar timescale is handled through an explicit controlled
model limit: `F²→0` at fixed spatial stiffness `Cs=F² c_chi²` and finite
forcing frequency. The scalar responds elliptically, without scalar
radiation or inserted dissipation. This is not a selected finite propagation
speed or a nonlinear vacuum-crossing completion.

A prescribed `l=m=2` quadrupole has a smooth sin-squared envelope of duration
`20/omega_dyn`. Five pattern speeds are fixed in advance. The source is a
finite-duration external potential, not a live stellar bar with a solved
energy/angular-momentum reservoir. No acceleration target or fitted response
multiplier is inserted.

## Finite-pulse result

The table gives total external work divided by squared forcing amplitude in
FR01's dimensionless units. The forcing amplitude is `A=0.0002`; it is a
linear normalization, not a calibrated galactic bar strength. Frequencies
are divided by **each background's own** dynamical frequency. Comparing
columns therefore does not hold the absolute physical forcing history fixed.

| Pattern speed / omega_dyn | Baseline, full | Baseline, bare | Compact, full | Compact, bare | Diffuse, full |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.26996 | 0.12411 | 2.55781 | 1.24245 | 0.32658 |
| 0.5 | 0.002865 | 0.001690 | 4.44069 | 3.87764 | 0.004123 |
| 1 | 6.78277 | 1.36546 | 2.30146 | 0.98510 | 6.74969 |
| 2 | 0.017796 | 0.035006 | 9.77968 | 54.13862 | 0.018643 |
| 4 | 187.53469 | 166.77374 | 6.43724 | 5.04147 | 185.42997 |

Primary records: [baseline](baseline_basis12_001/result.json),
[compact](compact_final_k1536_001/result.json), and
[diffuse](diffuse_l2_001/result.json). Bare controls retain the same background
orbits while removing induced gravitational, scalar and current feedback
together. They do not isolate the scalar's individual contribution.

![Finite-pulse work](summary_001/response.png)

Collective feedback strengthens some frequencies and suppresses others. At
pattern ratio one, the baseline work is about five times its bare value;
at ratio two, compact-state feedback reduces the bare work to about 18%.
There is no supported universal drag or enhancement factor. Nonnegative
pulse work also follows structurally from a positive finite Hamiltonian and
a zero initial perturbation; its sign alone is not a new physical discovery.
The calculated magnitudes, frequency dependence and feedback are the result.

## Validation and its limits

- The finite Hamiltonians are positive in the tested spaces: minimum
  eigenvalues about `0.64329`, `0.72288` and `0.65509` for baseline, compact
  and diffuse. This is finite-model stability, not a continuum theorem.
- Final spatial changes in work are below 0.2% for the baseline and below
  0.08% for the compact state. The diffuse refinement changes are below
  0.6%. All meet the frozen 1% work target. Separate orbital, Fourier and
  Krylov checks are in [the comparison record](summary_001/summary.json).
- At the final compact grid, increasing Krylov dimension from 1152 to 1536
  changes integrated work by at most `3.5e-10` relatively. The energy and
  angular-momentum ledgers are much tighter than spatial truncation errors.
- Independent dense-matrix and direct time-integration controls pass. Exact
  orbital-harmonic bare responses agree with the Krylov results to roughly
  `2.2e-12`. The current-feedback force-sum rule agrees within `4e-5` at the
  primary grids.
- High-order radial matrices are ill-conditioned in their original
  polynomial coordinates. At the final compact grid the worst complete
  feature-Gram discrepancy is about 0.104%, although the forcing sum rule
  is much more accurate. Results are floating-point convergence evidence,
  not rigorous error enclosures.

The [independent review](INDEPENDENT_REVIEW.md) checks signs, conjugations,
phase-space measure, angular factors, scalar exterior, and work/torque
normalizations. The first independent reference run remains recorded as
failed: it lacked absolute accuracy for tiny, nearly cancelling reference
work. A separately normalized and tightened integration passes the unchanged
gates. The original zero-feedback implementation defect and residual-label
correction are also preserved, rather than rewriting prior evidence.

## Longer forcing does not give a universal absorption law

For the baseline, doubling pulse duration changes work by factors roughly
`2.07, 0.027, 0.94, 0.044, 2.18` across the five frequencies. Some responses
grow, while others are suppressed by a longer and spectrally narrower
forcing pulse. The baseline comparison is stable under the stated Krylov
refinement. It does not prove an infinite-time damping rate.

The corresponding longer compact-state run remains numerically inconclusive:
its work changes substantially with Krylov dimension. Its raw outputs are
included but excluded from physical duration-scaling conclusions. Late-time
quadrupole amplitudes are likewise not established damping curves.

![Baseline duration comparison](summary_001/duration.png)

## What this does not establish

The first-order density response is a quadrupole and has zero spherical
average. Computing positive second-order total work does not determine the
second-order spherical redistribution. No result here reverses FR01's
31.4% contraction of the radius enclosing the original core mass.

Work performed inside that core radius is a separately recorded observable;
it excludes transport across the boundary and is not retained core heat.
Positive work can remain in coherent motion. Neither permanent heating,
core expansion, a finite stellar energy budget, population selection nor
formation has been demonstrated. The microscopic potential, `B/V`, universal
acceleration and cluster behavior remain unresolved.

The useful new building block is an implemented and reviewed kinetic
response with an explicit energy/angular-momentum account. The missing
implication is still **that exchange produces the required sustained radial
mass redistribution under a physically available baryonic source**.

See [reproduction commands](REPRODUCE.md), [the frozen contract](CONTRACT.md),
[analytic equations](THEORY.md), [numerical normalization derivation](DERIVATION_NUMERICS.md),
[validation](VERIFICATION.json), and [handoff](HANDOFF.md).
