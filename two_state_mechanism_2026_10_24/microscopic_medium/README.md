# Microscopic spectrum with gravitating, transported countercharges

**Outcome: the tested microscopic candidates do not derive the required critical
response. Live transport is implemented in a conservative 3D electrostatic
model, but disk/dwarf/cluster separation and a preserved acceleration relation
are not established.** This is a negative research result, not a completed model.

## What changed

[Derivation](DERIVATION.md) computes the Coulomb ground-state excitation gaps
and oscillator strengths instead of assigning a continuous critical spectrum.
The first dipole gap is **3B/4**. The gapless acoustic mode in a simple diatomic
medium is electrically dark at zero wave number; its charged optical mode is
gapped. Counting acoustic modes alone would have given a misleading argument.
Neither candidate supplies the predecessor's required n(s)d proportional to s.

[The causal parent and parameter ledger](COMPLETION_AND_LIMITS.md) give the
Maxwell/moving-charge action, continuity and energy accounting. The numerical
solver uses its nonrelativistic electrostatic limit plus Newtonian gravity.
All baryons and both charged constituents move and gravitate; nothing is hidden
in a fixed compensating background. The neutral medium is represented by its
constituents, never counted twice. Radiation and relativistic gravitational
stress-energy are not evolved.

Charge matching reduces one coupling conditionally. Microscopic masses remain
free; formation energy and atomic oscillator strengths are then determined.
The previous fitted susceptibility is not inserted into this different model.
The harmonic collective example has an assumed spring constant and therefore
is not a first-principles closure.

## Tests actually completed

The principal run has 12 distinct configurations: 36 particles, two seeds,
spin fractions 0/.5/.9, two common preparation endpoints (independent positions
or close neutral pairs), duration two units sqrt(b³/(GM_b)). Six additional
integrations check three softenings at two tolerances. A separate follow-up
has 12 tighter short/long integrations. These are small numerical diagnostics,
not converged galaxy simulations or quantum atoms represented individually.

- Force versus independent finite difference: relative discrepancy 6.24e-10.
- Independent circular-orbit return discrepancy: 2.98e-11.
- Worst sampled relative energy drift in the 12-configuration scan: 5.84e-8.
- Worst momentum drift: 9.58e-15; angular momentum drift: 2.13e-9
  (dimensionless absolute units).
- Tight long-run energy drift at h=.04/.08/.16:
  1.04e-11 / 1.68e-12 / 7.65e-13.
- Tight short-time trajectory refinement errors: at most 7.81e-10.
- Tight long-time trajectory refinement errors: **.889 / .000237 / 3.46e-7**.
  The smallest-softening trajectory is unresolved. Long-run endpoint population
  comparisons have not been shown statistically or continuum converged.

Energy is analytically conserved by the Hamiltonian and approximately conserved
by the adaptive integrator; there is no energy rescaling or discarded receiver.
All error figures sample 81 output times, not every internal integrator stage.

Illustrative endpoint neutral-pair fractions from the principal run:

| Initial preparation | Spin | Seed 17 | Seed 29 |
|---|---:|---:|---:|
| Independent positions | 0 | .417 | .333 |
| Independent positions | .5 | .333 | .500 |
| Independent positions | .9 | .250 | .333 |
| Close pairs | 0 | .583 | .750 |
| Close pairs | .5 | 1.000 | .833 |
| Close pairs | .9 | .750 | .833 |

Even the independent-position starts already have accidental negative-energy
pairs (.333 and .417); these endpoints must not be called formation fractions.
Pairs require mutual nearest opposite neighbors and negative two-body relative
energy. A neutral pair is **not positively charged tethered matter**. Its
complement is not automatically gravitationally bound free matter. Inner dark
mass, positive and negative counts, and baryon shape are recorded separately in
the raw results. No sufficient retained-free-mass or disk-formation claim follows.

## Structural result stronger than the small runs

The tested classical equations are exactly homologous under mass/size scaling
when the dimensionless initial conditions and h/b are held fixed. Consequently
the four historical dwarf/disk/cluster mass-size mappings share the same
trajectories at equal dimensionless age. They are not four independent tests.
Rotation can affect shape and transport, but this model cannot distinguish a
rotating dwarf from a larger homologous rotating system. It contains no a0 and
cannot derive a fixed acceleration transition. A fixed physical age, quantum
length, radiative cooling or collective phase could break homology; these are
not ruled out and have not been implemented here.

The narrow conclusion is that this candidate cannot deliver the requested
combination. This does not prove that every interacting quantum medium fails.
A valid next candidate must derive the **dipole-weighted retarded response**,
its state and equation of state, and its gravitating mass together. Assigning
an attractive spectrum or a separate capture efficiency would undo the desired
parameter reduction.

## Reproducibility and status

- Main valid evidence: [run_transport_v2/manifest.json](run_transport_v2/manifest.json)
  and [results](run_transport_v2/results.json).
- Follow-up valid evidence: [run_refinement/manifest.json](run_refinement/manifest.json)
  and [results](run_refinement/results.json).
- Both statuses are completed; both manifests validate against current sources.
- Initial run_transport failed at parsing (missing parenthesis), before any
  scientific result. Its manifest is historical and stale against the corrected
  source; its original source is retained as failed_source.py. It is excluded.
- The predecessor causal_collective evidence still validates unchanged.

Exact runner argv, hashes, software versions and random seeds/bounds are retained
in the contracts and manifests. Use the installed mathbox validate_manifest.py
with `--root` pointing to the repository to check either successful manifest.
Scripts can also be rerun with `python3 experiment.py --output <new.json>` or
`python3 refinement.py --output <new.json>` from this folder; use the bounded
runner for provenance-bearing evidence. No manuscript, published claim or older
implementation was changed.
