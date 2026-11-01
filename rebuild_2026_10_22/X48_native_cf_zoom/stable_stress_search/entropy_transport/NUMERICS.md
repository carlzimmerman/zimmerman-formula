# Numerical methods and finite evidence

This note records the audited numerical scope of the pinned spherical
`outward_instability_gated_heat` experiment. It separates constitutive and
semidiscrete identities from floating-point integration, finite sampled
observations, and continuum claims. A completed integrator status means that
the requested finite endpoint was reached; it does not establish settling or
a positive infinite-time entropy floor.

The physical operator is in [convective_transport.py](convective_transport.py),
with inherited conservative mechanics and heating in
[transport.py](transport.py), [collapse.py](../collapse.py), and
[material.py](../material.py). The floor observer and cold-phase integrator are
in [refinement.py](refinement.py). The separate warm continuation driver is
[bdf_continuation.py](bdf_continuation.py).

**Fixed physical experiment.** The refinement runs use equal-mass shells,
initial density 0.25, initial outer radius 1, initial velocity gradient -0.25,
and virgin K=0. The fixed scales are rho_q=G=1, a0=sqrt(8*pi), tau=0.5;
the transport parameters are diffusivity 0.1, damping strength 1, memory
activation 0.01, stratification length 0.1, and stratification scale 0.01.
Diffusivity and stratification length are physical parameters and do not scale
with shell count. The resolved populations are N=32, 64, 128, and 256; the
experiment is one spherical collapse, not a cosmological ensemble.

**Cold invariance and observed solver leakage.** When K is identically zero,
thermal pressure, memory damping, and heat flux vanish. Original shock heating
also vanishes until a cell simultaneously satisfies rho>rho_q and tau*C>1,
where C=max(-theta,0). Before that activation, the full physical equations
therefore reduce exactly to

    r_dot_i = u_i,
    u_dot_i = -G*m_i/r_i^2,
    K_i = 0.

The coupled 3N implicit solver exhibited floating-point leakage into zero K
coordinates in an unheated state whose exact K derivative vanishes. Pivoted
sparse LU is a possible numerical mechanism, but no durable diagnostic
isolates the factorization as its cause. The regression evidence establishes
the cold-state preservation issue and the replacement path's behavior, not a
complete causal diagnosis of LU. Such leakage is not physical entropy
generation. The regression case is an expanding, perturbed sphere above the
density gate in
[test_refinement.py](test_refinement.py); an independent gravity-only reference
is checked in [test_forest.py](test_forest.py).

`refinement.py` handles this by integrating only the exact 2N-dimensional
(r,u) invariant subspace while K=0 and the source is inactive. Reconstructing
the omitted K coordinate as zero is not clipping or projecting an evolved
thermal coordinate. No epsilon entropy seed, entropy floor, or additional
heating is introduced. The analytic dust Jacobian is supplied to SciPy Radau.

The activation indicator is

    max_i min(rho_i/rho_q - 1, tau*max(-theta_i,0) - 1).

At a detected upward activation crossing, the cold dense interpolant is used
to locate the root with `brentq`, `xtol=1e-13`; the full Radau system resumes
from that state with K still exactly zero. For the uniform initial sphere,
independent homologous dust quadrature gives first activation at
0.5907973398405011, with tau*C approximately 2.70729248. Recorded N128/N256
handoffs differ from this value by about 1.13e-9/1.15e-9. The root tolerance
concerns the numerical interpolant, not a certified physical-time error.

Wall time, RHS calls, and domain retries are shared across the cold and warm
phases of one `refinement.simulate` call. Negative intermediate K in the full
solver uses the documented stage extension and is counted. Negative accepted
K rejects the complete step and restarts from the unchanged accepted state;
there is no accepted-state projection. Shell ordering and minimum shell gap
are also checked. These controls do not certify positivity between all
numerical samples or validate a continuum PDE solution.

**Methods, tolerances, and provenance.** The main runs use SciPy sparse Radau,
`rtol=2e-7`, `atol=1e-9`, and `max_step=0.05`. The tight N256 chain uses Radau
with `rtol=2e-8`, `atol=1e-10`, and the same maximum step. The BDF expansion
segments use `rtol=2e-7`, `atol=1e-9`, and `max_step=0.05`. Each recorded run
has an internal 45-second wall cap, 300,000 RHS-call cap, 80 domain-retry cap,
and minimum retry step 1e-12. Manifest commands, software versions, source and
restart hashes, result hashes, process status, and outer runner limits are
stored alongside each result; the cited audited manifests match their current
inputs and outputs. A manifest process failure must be interpreted together
with the result status: the historical cases below exited with `wall_limit`,
not a demonstrated physical singularity or negative-memory counterexample.

**Energy references and restart lineage.** The reported error of an ordinary
continuation is relative to that continuation's initial total energy. It must
not be presented as the error accumulated since virgin collapse. For exact
state handoffs, segment bounds e_j combine relative to the original reference
energy E_0 as

    max |E(t)-E_0|/|E_0| <= sum_j e_j*|E_j,start|/|E_0|.

The cold-to-warm wrapper implements the corresponding triangle bound with the
original initial energy, explicitly marking it as an upper bound. These are
accepted-state numerical diagnostics, not rigorous rounding-error bounds.
The N32/N64 floor files continue their matching
[N32 t8](conv_n32_t8/result.json) and [N64 t8](conv_n64_t8/result.json)
ancestors. Their continuation-only errors are about 8e-15 and 6e-15, whereas
the combined original-energy bounds through t32 are about 8.995e-10 and
8.949e-10. Fresh N128/N256 cold-to-warm bounds through t32 are about 1.0004e-8
and 1.0205e-8. The completed tight N256 chain gives approximately 2.448642e-9
relative to its original virgin state.

Prepared radius perturbations are applied once before evolution, preserve K
and mass, and report the full internal, kinetic, and gravitational preparation
work. Radius factors 0.99 and 1.01 add total energies 0.0005298719930 and
0.0005148967877 respectively. Subsequent conservation is measured relative to
the prepared state; exact return to the unperturbed equilibrium is not
required because conserved energy changed. The separately prepared
[entropy mode](entropy_mode_n64_t64/result.json) is energy neutral and records
its entropy preparation decrease explicitly; that preparation is not counted
as entropy production by the simulated law.

**Absolute sample windows and floor diagnostics.** The automatic
`settling_metrics` summary uses the last quarter of each file's own history.
Consequently the N32/N64 t8-to-t32 files have stored cutoffs at 26, while fresh
N128/N256 t0-to-t32 files have cutoffs at 24. Those summaries cannot be
compared as though they used the same absolute interval. The following values
were recomputed from raw histories restricted to 24<=t<=32:

| N | Actual retained sample range | Count | Minimum central-5% K | Minimum outside guard K | Relative density-5% span |
| ---: | --- | ---: | ---: | ---: | ---: |
| [32](floor_n32_t32/result.json) | 24 to 32 | 65 | 0.3493312591 | 0.3493309959 | 1.22609e-4 |
| [64](floor_n64_t32/result.json) | 24 to 32 | 65 | 0.3495330395 | 0.3495329104 | 1.21227e-4 |
| [128](floor_n128_t32/result.json) | 24.02305964157824 to 32 | 65 | 0.3495986336 | 0.3495985641 | 1.19069e-4 |
| [256](floor_n256_t32/result.json) | 24.023059641573333 to 32 | 65 | 0.3496197548 | 0.3496197186 | 1.18470e-4 |

These sample grids are close, but not identical. The cold-to-warm handoff
restarts the diagnostic grid. No exact t24 observation is claimed for the
higher resolutions. Maximum hydrostatic residuals over these retained samples
are below 4.53e-5; full-force residuals are below 2.03e-7. Original shock
heating is zero there, while heat transport and damping continue at decreasing
rates. These source-coupled diagnostics distinguish the observed relaxation
from a claim based only on small kinetic energy.

For a fixed mass fraction f, every constant-K cell intersecting the prefix is
included, even when the last cell is only partially intersected. Its outside
guard is the next cell: zero-based index `ceil(f*N)`. Central-5% included
counts/guard indices are 2, 4, 7, and 13 on these grids. The observer uses exact
decimal mass fractions for this mapping. The guard is not a point measurement
exactly at mass fraction f. Raw per-cell arrays, prefix minima, guards, and
geometry were cross-checked. `min_positive_K` excludes zero cells and cannot
by itself establish a floor; the prefix minima and `min_all_K` include zeros.
All audited late arrays here are positive.

**Capped runs and completed continuation chains.** The original status records
remain unchanged:

| Recorded segment | Method | Start | Reached | Status |
| --- | --- | ---: | ---: | --- |
| [Compression](compress_n64_t64/result.json) | Radau | 32 | 43.65472851883699 | wall_limit |
| [Compression finish](compress_n64_finish/result.json) | Radau | 43.65472851883699 | 64 | completed |
| [Expansion](expand_n64_t64/result.json) | Radau | 32 | 46.05664445808807 | wall_limit |
| [Expansion Radau continuation](expand_n64_finish/result.json) | Radau | 46.05664445808807 | 46.47356943523749 | wall_limit |
| [Expansion BDF switch check](bdf_switch_check/result.json) | BDF | 46.47356943523749 | 46.6 | completed |
| [Expansion BDF finish](bdf_expand_t64/result.json) | BDF | 46.6 | 64 | completed |
| [Tight N256](tight_n256_t32/result.json) | Radau | 0 | 28.12673158196404 | wall_limit |
| [Tight N256 finish](tight_n256_finish/result.json) | Radau | 28.12673158196404 | 32 | completed |

The BDF driver imports actual `scipy.integrate.BDF` and calls the same
`model.rhs` and `model.jacobian_sparsity`; it does not relabel Radau, alter the
law, reset K, or add energy. It requires strictly positive initial K and uses
the same accepted-state rejection policy. The Radau-to-BDF handoffs preserve
time, state, energy, mass, closure, and parameters. The expansion's completed
chain has about 90.598 seconds cumulative integration time and 454,634 RHS
calls across four separately capped segments. It did not finish inside the
original run's 45-second cap. Its combined energy-error bound relative to the
prepared expansion state is approximately 4.45533e-13.

The unperturbed, compressed, expanded, and entropy-mode N64 chains all reach
64. Their raw late windows are distinct:

| Case | Actual samples retained within 56<=t<=64 | Count | Relative density-5% span | Maximum hydrostatic residual |
| --- | --- | ---: | ---: | ---: |
| [Unperturbed](steady_n64_t64/result.json) | 56 to 64 | 65 | 1.03723e-7 | 3.26329e-8 |
| [Compressed](compress_n64_finish/result.json) | 56.0526283276707 to 64 | 101 | 3.99714e-8 | 1.31305e-7 |
| [Expanded, BDF](bdf_expand_t64/result.json) | 56.115625 to 64 | 59 | 5.66048e-8 | 1.59752e-7 |
| [Entropy mode](entropy_mode_n64_t64/result.json) | 56 to 64 | 65 | 1.07903e-7 | 3.40174e-8 |

The tight N256 chain has 290 retained samples from
24.02305964180807 to 32 on a mixed restart grid. At the common endpoint t32,
maximum cellwise relative differences from baseline N256 are approximately
7.614e-9 in K, 7.548e-9 in density, and 2.516e-9 in radius. This supplies a
completed tolerance check at t32, without claiming identical sampling grids.

**Interpretation and checks.** The finite observations support radial
relaxation and positive sampled central entropy in this specified experiment.
Four finite resolutions do not prove a positive lower limit as N tends to
infinity, and finite windows do not prove persistence as t tends to infinity.
A minimum principle propagates an established lower bound under its boundary
hypotheses; it does not create entropy from virgin zero data. Uniform seeding,
guard control, geometry, convergence, and intervening-time bounds require
additional arguments.

The [refinement tests](test_refinement.py), [quiet-domain tests](test_forest.py),
[perturbation tests](test_stability.py), and
[warm BDF tests](test_bdf_continuation.py) address numerical and constitutive
contracts. The quiet-domain tests include independent gravity-only evolution
and retained dilute heat with zero stress. They are not observed forest
likelihood tests. Semidiscrete energy cancellation and source/flux checks
remain distinct from integration accuracy, and none of these checks proves
well-posedness, convergence, global stability, or halo formation for the full
PDE, or tests nonradial/three-dimensional dynamics.
