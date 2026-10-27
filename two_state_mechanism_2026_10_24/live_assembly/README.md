# Assembly work now closes; the proposed separation fails

**The requested physical goal was not reached.** We built an energy-conserving
assembly coupling and evolved it with live spherical self-gravity. It can
create some tethered matter from an exactly free initial state. It does not
create predominantly tethered rotating systems while keeping the acceleration
relation. Free matter remains abundant in the rotating cases too.

This is a constructed effective interaction and a reduced dynamical experiment,
not a microscopic theory, a 3D disk-formation simulation or an observational fit.

## What was built

Contraction and internal conversion share a reciprocal dissipative coupling.
Infall can pay the positive energy cost of forming T, while the reciprocal
force changes the infall. An explicit positive receiver takes dissipated
energy. Mechanical, gravitational, internal-state and receiver energies close
analytically; all radial forces come from the same energy functional.

Both baryon and medium shells now move, cross, contract and expand under live
gravity. Their angular momenta are conserved. Every mass/size profile receives
the same equations and parameter scan, crossed with the same initial angular-
momentum coherence values. No object name selects a phase or force law.

The collective phase and circulation approximation is different from the
previous fixed-density local-vorticity model. It restricts spatial conversion
and uses a collective barrier over the polarization field. T and F share
each medium shell's velocity: separate transport is not modeled. These are
substantial limitations, especially for any claim about a mixed-state halo.

## Numerical outcome

The supported-assembly scan completed all 60 cases: four profiles, three
coherences and five coupling strengths including the zero-pump control.
At 30 initial dynamical times, the largest tethered fraction in the entire
scan was **2.79%**, compared with the declared 95% formation target.
Low-coherence cases kept **98.46–100%** of the initial medium as snapshot-bound
free matter. They pass that illustrative mass-reservoir test, but the strongly
rotating cases also remain mostly free and fail the joint target.

Refined runs at one common coupling alpha=.3 doubled shell and field-grid
resolution and tightened the time tolerance tenfold. Results at 30 times:

| Baryon mass (solar masses) | Scale (kpc) | Strong-coherence T fraction | Weak-coherence bound F / initial medium | Strong-coherence maximum RAR residual |
|---|---:|---:|---:|---:|
| 300,000 | 0.3 | 0.784% | 99.620% | 1.582 dex |
| 100 million | 1 | 0.318% | 99.830% | 0.763 dex |
| 60 billion | 3 | 0.659% | 99.967% | 0.286 dex |
| 100 trillion | 300 | 1.502% | 99.695% | 0.345 dex |

The comparison uses the actual evolving monopole acceleration against the
parent baryon-only relation, over .5–5 current baryon half-mass radii. The
illustrative tolerance was .05 dex. It is not a comparison with observed data.
Precise endpoint fractions are not converged: shell refinement changes some
small fractions appreciably. The large shortfall from 95% survives refinement.

Colder assembly was also tested: 32 cases with less centrifugal support.
Thirty hit the inner radial boundary before the requested stopping time;
their endpoints are **not completed formation/retention tests**. One early
trajectory also slightly exceeded the energy-error threshold. The two full
cold trajectories had small final T fractions, 0.060% and 0.213%.

A targeted cold case (100 million solar masses, strong coherence, alpha=3)
was then extended inward by a factor of 2000. It completed five initial
dynamical times at two field resolutions, with **4.15% and 4.79% T**, about
95% snapshot-bound F and a roughly .92-dex maximum RAR mismatch. This resolves
that case's earlier boundary obstruction, but is not a 30-time or general
cold-collapse result. The other truncated cold cases remain unresolved.

## What the checks establish

- Maximum relative total-energy error: 3.45e-6 in the supported scan,
  2.46e-7 in its refinement and 1.05e-5 in the extended cold test.
- Independent instantaneous energy and signed work identities hold to
  better than 6e-13 in the tested states.
- Initial force quadrature changes by at most 3.68e-5 from 512 to 2048 cells;
  energy derivatives and gravitational homogeneity were also checked.
- Five completed evidence manifests validate against current input hashes;
  all stderr files are empty. A completed batch record does not turn an
  individual boundary-terminated trajectory into a complete physical test.

The zero-pump control stays exactly free, even under live collapse. This
agrees with the analytic obstruction in the original phase-gradient dynamics.
The new coupling removes that obstruction, but rotation-dependent metastability
does not by itself guarantee assembly into the tethered basin.

## Scientific limits and next obligation

The reservoir test only asks whether at least 90% of the initial free medium
is instantaneously bound. It does not establish enough mass for measured
dwarf or cluster profiles. Binding is a snapshot diagnostic in a changing
potential; the available mass was assumed to be 5.364 initial baryon masses.

The tested global pumping prescription is unsuccessful in the declared scan.
This does not refute all two-state interactions. A viable continuation needs
a local assembly/capture process, independent T/F transport and an explicit
source for its interaction and dissipation coefficients. A successful radial
model would still need 3D disk geometry and observational tests. Increasing
rotation or relabeling an object cannot substitute for those obligations.

[Derivation](DERIVATION.md) · [Self-audit](AUDIT.md) · [Research handoff](HANDOFF.md)
· [Figure](results.png)

## Reproduction

From this directory, using Python, NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 python3 assembly.py --output /tmp/live-scan.json
OPENBLAS_NUM_THREADS=1 python3 cold_probe.py --output /tmp/live-cold.json
OPENBLAS_NUM_THREADS=1 python3 cold_probe.py --support .7 --n 24 --nq 1024 --rtol 2e-8 --alphas .3 --output /tmp/live-refine.json
OPENBLAS_NUM_THREADS=1 python3 wide_infall.py /tmp/live-wide.json
OPENBLAS_NUM_THREADS=1 python3 invariants.py /tmp/live-invariants.json
```

Exact commands, environment versions, pre/post input hashes and result hashes
are in the corresponding `run_*/manifest.json`. Contracts preceded these
recorded runs. Exploratory five-time pilots in /tmp were repeated or superseded
and are not the evidence for the results above.
