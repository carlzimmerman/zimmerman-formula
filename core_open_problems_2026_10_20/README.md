# Four independent investigations of the theory's core

20 October 2026. **All four original physical-origin problems remain open.**
This package records four independent investigations, explicit conditional
constructions and obstructions, reproducible computations, and a coordinator
review. It does not promote an analogy, a fitted coefficient, or a partial
relativistic action into a completed theory.

| Question | Result of this checkpoint | What remains missing |
|---|---|---|
| [Horizon normalization](01_horizon/report.md) | Separates the two meanings of a₀/2; derives an analytic-readout obstruction; independently checks detector rates and information thresholds. | A physical force coupling and a rule fixing κ = ½. |
| [Microscopic medium and n](02_medium/report.md) | Explicit dielectric, Born–Infeld/two-level and lattice models miss the required response. A kinetic model gives the stationary law conditionally. The maximum circular-speed difference is 7.46% at fixed a₀ and baryonic source. | A microscopic source and state producing the full potential and selecting n. |
| [Relativistic completion](03_relativity/report.md) | A specified clock/polarization action recovers static S2, derives leading lensing equality and a luminal tensor principal symbol, and exposes a polarized scalar constraint bound. | S3's conserved mass interpretation, physical-vacuum and general-background stability, strong coupling, and full Solar-System tests. |
| [Stiffness origin](04_stiffness/report.md) | Distinguishes L* from a background-dependent response length; tests finite-range exchange, contact-fluid pressure, and quantum-pressure mechanisms. | Independently fixed microscopic range/couplings and the correct full polarization operator. |

## Important corrections to the starting description

- With κ = ½, **a₀/(cHΛ) = 1/√(32π/3) ≈ 1/5.79**. The 1/11.58 factor
  refers either to the simple law's baryonic field at g = a₀ or to an assigned
  ambient scale in the quadratic temperature-excess law. A smooth response does
  not itself define a sharp vacuum switch.
- **n = 1 and n = 2 are different effective theories.** Their capacities are
  a₀ and a₀/2. Their shared deep limit does not make their full laws identical.
- **The 1 kpc value was a scan edge.** The later approximate SPARC calculation
  reports a soft upper edge near 2.04/2.14 kpc. The approximately 24 pc lower
  limit is conditional on the globular sample and screening model. The dwarf
  mass deficit cannot be treated as a clean independent stiffness measurement.
- **An enclosed spherical mass/area bound is not a projected lensing bound.**
  The sheet and spherical projection formulas differ.
- The relativistic candidate's exact flat-vacuum calculation uses independent
  Λ = 0 and finite a₀. Enforcing S1's relation between them requires a separate
  de Sitter/clock calculation. The candidate also gives P a new dynamical
  interpretation; it has not derived the original cold-mass sector S3.

The circular-speed result assumes an isolated, spherical, unscreened system and
the same a₀ and baryonic mass. Finite stiffness and baryonic calibration must be
controlled before using it as an observational test. No data preference for
either theory is established here.

## Evidence and review

- [Target contract and worker scopes](CONTRACT.md).
- [Coordinator's derivations and scope audit](REVIEW.md).
- [Independent review of the raw relativistic action](05_independent_review/independent_audit.md).
- [Pinned baseline source map](BASELINE_INPUTS.json), with exact source snapshots.
- [Additional documentary source map](SUPPORTING_SOURCES.json), including
  snapshots of sources absent or different at the publication parent.
- Each numbered report links its executable checks, source checks, successful
  run records, failed attempts where applicable, and precise continuation.

The four initial investigations used isolated contexts and disjoint write
scopes. Afterward, the horizon worker independently rederived the relativity
candidate's scalar and tensor checks from the raw action before comparing the
author's calculation. The coordinator also rederived shared law identities and
the polarized shift elimination. This is independent checking within an AI
workflow, not a formal proof certificate or external peer review.

## Reproduce

The scripts use Python and the scientific packages in `requirements.txt`.
That file pins the coordinator's environment; original run environments are
recorded separately. Each lane's report gives a direct, portable command and
its exact scope. No observational dataset or network access is needed for the
new computations. Historical source paths are provenance, not a new data fit.

```bash
python3 core_open_problems_2026_10_20/verify_bundle.py
```

All seven commands passed and reproduced their mathematical outputs; the
[verification receipt](verification.json) records hashes and environments.
For the shared conventions alone, `review_checks.py` uses only Python's
standard library. Original provenance manifests describe the original checkout;
the portable scripts do not require restoring its untracked source paths.
Counts of passing checks describe the computations; they do not close the
four physical-origin questions.

## Next discriminating work

1. Specify a microscopic force observable and its coupling before assigning a
   thermal activation threshold; then test whether permitted vacuum offsets
   leave κ free.
2. Derive a proposed medium's source-dependent partition function or reaction
   affinity, including zero source, before selecting n from a curve fit.
3. Reduce the candidate's complete constrained perturbations on an actual
   polarized solution and the S1-linked de Sitter vacuum, with arbitrary wave
   direction; then test the S3 embedding and preferred-frame limits.
4. Fix microscopic parameters independently, establish both longitudinal and
   transverse stiffness, and test whether the derived operator remains valid
   over the scales where screening is used.

These continuations remain open. The packet closes this requested research and
publication checkpoint, not the research program or the theory's open claims.
