# Density and collar continuation provenance

Base checkpoint: **X48-NLC-2026-11-01-B**. The exact target and observed
coordinator revision are in [TARGET.md](TARGET.md). The shared checkout moves
concurrently; the unchanged physical files are identified by the existing
[22-source inventory](../../verification/source_hashes.json), not a later
shared HEAD. No physical source, initial datum, coefficient, prior proof
note, or previous run artifact was changed by this continuation.

## New proof records

- [gradient_symmetrizer.md](gradient_symmetrizer.md) proves the exact
  midpoint density-gradient cancellation, its explicit small singular
  exponent, complete mechanical collar, and the composed conditional
  first-energy theorem.
- [relative_entropy.md](relative_entropy.md) proves the full weighted
  relative-entropy balance, heat collar, time-dependent drop-threshold
  conversion, negative-gradient propagation, and sufficient activation
  trace. Together these two notes give uniform conditional inner energy
  `O(s^5)`.
- [flux_potential.md](flux_potential.md) preserves the earlier flux-potential
  defects as well as the successful one-sided nonlinear gradient closure.
  Its independently reviewed scope is Sections 4–7, rather than all of its
  proposed flux-potential constructions.
- [local_work.md](local_work.md) gives the finite Hardy shear and local/collar
  estimates, a regular reaction-flow chart, and the restricted local-metric
  obstruction. The later gradient energy resolves the chart-only route's
  singular-start limitation by adding a different energy mechanism.
- [boundary_transfer.md](boundary_transfer.md) gives the actual total-volume
  variation and fixed-cut lemma. Its prescribed-coefficient counterexample
  lies outside the specified momentum/energy IVP and does not refute (UC).
- [pointwise_continuation.md](pointwise_continuation.md) derives the actual
  sufficient normalized-stress bound and the exact all-p stress equation.
  It retains the mixed heat flux and coefficient remainder; their iteration
  estimate is not proved. Its instantaneous one-cell state distinguishes a
  false static energy-to-maximum implication from the unrefuted cold IVP.

The independent reviewer reconstructed the conditional claims from the raw
proofs and exact physical sources. The coordinator separately reconstructed
the positive actual volume-variation and fixed-cut claims. Exact review
scopes, byte hashes, and the unreviewed portion of the auxiliary boundary
counterexample are recorded in [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md).
Independent agreement is not itself a mathematical certificate.

The previous live floor-status bytes are preserved before updating its
handoff:

| Snapshot | SHA-256 |
| --- | --- |
| [base_floor_status.txt](base_floor_status.txt) | `7a7b3ddf8df5b685416d2e9dc190ef5acd0c22cd56cb719b0eb566ab914fd1d0` |

This is a verbatim context snapshot. Its relative links keep the original
floor_theorem namespace; it is not a second live status. The prior phase's
status and all audited proof inputs retain their bytes.

## Verification scope

The mathematical checks are direct source reconstruction, exact shared-flux
summation, finite-edge product identities, rational inequalities, and fixed-N
activation analysis followed by an N-independent scalar inequality. No
external regularity theorem, continuum limit, grid extrapolation, or numerical
trajectory is a load-bearing proof leaf.

No new collapse experiment or physical test run was performed. Existing
conservation and quiet-gate proofs remain applicable because all 22 inventoried
physical/test source files are checked byte-for-byte against the prior
inventory. This check verifies unchanged inputs, rather than re-running the
earlier test suite. Current source and proof hashes, audit pins, local links,
delimiters, whitespace, and scoped diff validation are recorded in
[checks.json](checks.json).

Focused mathematical self-proofreading covers the new coordinator target,
overview, status, and provenance. Author and reviewer proofreading scopes are
specified in their individual notes. The original actual pointwise bound and
propagation of the common prefix/collar hypotheses remain unproved; the
all-time entropy-floor theorem is still conditional on uniform seeding.
