# IC32 execution review and next calculation

Base: ea437f3de53a57bc5fd141c6887bd9fec6e33134. Self-review, not independent or formal certification.
The original full-theory target remains **OPEN**.

## Terminal execution evidence

| Job | Child exit | Runner exit | Runtime seconds | Meaning |
|---|---:|---:|---:|---|
| tests | 0 | 0 | 244.425914 | 406 tests, unittest reports 243.773 seconds |
| preservation | 2 | 1 | 39.568553 | Nine scoped checks true; strict mode refuses full closure |
| legacy | 1 | 1 | 41.973042 | Old coefficient representation exceeded the BVP mesh allowance |
| basis | 0 | 0 | 0.551829 | Six exact arbitrary-endpoint jet identities vanish |

All four manifests validated with the installed Mathbox validator and repository root.
Validation establishes pinned-input/output provenance, not the mathematical interpretation.
Each run had 300 seconds wall time, 2 MiB logs, and one cooperative numerical-library thread.
There was no hard memory or affinity cap. Exact child and runner commands are in run_index.json.

## Mathematical progress

The same radial action supplies the first time derivatives of the constrained IC31
pinned exterior, including the matter spatial momentum generated from initially
zero fluid gradients. No gravitational constraint is re-solved after a finite
Euler kick. Halving the kick twice gives approximately fourfold reductions in
all five tested constraint defects for nonzero amplitudes; the frozen-auxiliary
negative control is substantially worse.

All five selected repaired-coefficient cases solved: amplitudes 0, 1, 2;
amplitude 1 spatial refinement; amplitude 2 aligned mesh.
Maximum lapse-preservation defects at nodes and midpoints range from
6.52e-15 to 1.18e-9. Other equations have different errors:
the largest tested off-node q Euler defect is 1.4763847384573303e-6.
It must not be quoted as a 1e-9 all-equation solution.

For amplitude 2 the unprojected lapse errors at dt=.001,.0005,.00025 are
6.977938868017852e-6, 1.7543805447668412e-6, 4.4075780541976816e-7.
The frozen-auxiliary lapse error at dt=.001 is .012051651365209776.
This supports first-order tangency in the tested domain, not many-step evolution,
a continuum existence theorem, or a nonlinear functional Dirac count.

## Repairs and adverse evidence retained

1. Node-only evaluation initially hid a midpoint lapse defect .0003010700688290167.
   Direct source evaluation and integration by parts of represented momentum jets
   removed the source re-interpolation defect. The output field
   source_reinterpolation_error is a deliberately unused bad-method diagnostic,
   not the corrected solver's residual.
2. The old literal expanded floating coefficient polynomials have D'' jumps up to
   2.943677015957001e-5, evaluated at 80 digits. Calling those literal polynomials
   exactly C2 was unjustified. The intended interpolation construction and the
   underlying implicit D(S) are distinct from its rounded expanded representation.
3. Increasing the old solver's node allowance from 18000 to 60000 did not repair
   it. The final reproducible legacy run failed at 29420 nodes, with worst
   residual 2.1703581259617673e-5; further refinement would exceed its allowance.
   This is a numerical failure, not proof of a physical instability.
4. The new endpoint-defined quintic Hermite approximation uses shared fixed
   endpoint jets, with six exact C2 matching identities. It is a different
   numerical approximation, not literally the old rounded function. All selected
   IC32 repaired cases use this same function without source refitting.
5. Near-duplicate mesh nodes caused a developmental zero-width-cell failure.
   A regression now tests merging roundoff-equivalent abscissas. The merge changes
   only the mesh, not the coefficient action.
6. TDD included missing functionality, independent radiation Legendre tests,
   the off-node residual failure, and the duplicate-node failure before repair.

## Next indispensable calculation

Derive general inhomogeneous evolution retaining Q', q', and each fluid gradient.
Do not reuse IC32's initial-slice simplifications at a second step. Evolve many
steps with convergence and constraint audits, then investigate the transition
from the active pin to the unpinned exponential-MOND branch with derived matching
data. Global coefficient regularity, functional constraint closure including
zero modes, physical stability/causality/strong coupling, full PPN, and actual
cosmological/galactic observations remain separate unsatisfied obligations.

Carl Zimmerman's exponential law, vacuum-scale relation, and primordial-clock
direction are credited in IC32_CONSTRAINT_PRESERVATION.md. Neither the factor 1/2
nor an empirical prediction or a global novelty claim has been derived here.
