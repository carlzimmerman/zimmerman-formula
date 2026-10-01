# Independent fixed-offset identifiability audit

2026-09-30. Reviewer: /root/coupled_dynamics, separate from the root author.
Primary verdict: **proved as written**, for the exact finite stored-operator
claim and strict positive-monotone baseline specified in DERIVATION.md.

## Normalized claim

Let C be the inherited 12-by-16 H augmented by the row fixing coordinate 15,
the additive map offset. On a nonempty affine observation fiber C theta=d,
the linear target L theta is constant iff L lies in row(C). At a baseline
whose 15 free pressures strictly decrease to the fixed zero outer endpoint,
failure of the row-space condition also implies local nonidentification
within the positive-monotone finite family. The provided exact-rational
witness establishes that failure for the stored operator with fixed offset.

The interior hypothesis is essential for this constrained conclusion. At a
boundary baseline, inequalities could remove otherwise target-changing null
directions. No such boundary exception occurs for the supplied strict baseline.

## Dependency graph and independent reconstruction

Inherited FGF-019 finite geometry/operator -> stored binary64 H,L,baseline ->
exact rational interpretation -> C null vector -> strict feasible perturbations
-> same observations/offset and distinct targets. No literature mechanism or
physical gravity theorem is a dependency.

If L=w C, equal C theta gives equal L theta. Conversely, if L annihilates
ker(C), it defines a functional on im(C), via C theta -> L theta; extending
that finite-dimensional functional yields L=w C. Thus L outside row(C)
provides v in ker(C) with Lv nonzero. For each positive adjacent-pressure
margin m_i and perturbation difference d_i, epsilon <= m_i/(2|d_i|) preserves
both signed perturbations whenever d_i is nonzero; zero d_i needs no bound.
Including the last pressure against zero proves positivity of every node.
The nonzero target difference is 2 epsilon Lv. This independently recovers
the claimed implication and the implemented certificate construction.

## Obligations and checks

* Passed: NPZ dimensions H=(12,16), A=(12,15), baseline and L length 16.
  L has only the two relevant pressure-slope coordinates nonzero and zero
  offset coordinate, consistent with the inherited interval target.
* Passed: exact Fraction arithmetic in the author code treats stored floats
  as rational numbers; RREF uses nonzero pivots without a floating cutoff.
  Its finite rank 13/nullity 3 calculation is correctly implemented on C.
  The audit inspected this computation; it did not rerun rank elimination.
* Passed independently: parsed returned v and both returned witnesses as exact
  rationals and evaluated them against the NPZ coefficients. Every Hv=0,
  v_offset=0 and Lv!=0 condition held exactly.
* Passed independently: both returned witnesses equal theta0 +/- epsilon v,
  preserve H theta and offset exactly, and satisfy every strict adjacent
  decrease and positive last-free-pressure inequality.
* Passed independently: both displayed gradient floats equal conversion of
  the exact target values. Displayed width/baseline ratio reproduces
  0.004305185699537076. It is one feasible separation, not the sharp width.
* Passed: wrong-offset control is a valid negative control; adding one to
  the offset component violates the explicitly appended row.
* Passed: current author-manifest inputs and outputs match their hashes;
  manifest validation reports a valid evidence record. The NPZ hash also
  matches its original FGF-019 output record, establishing ancestry.
* Out of scope: recalibrating the inherited beam/map response, recomputing
  the original image reduction, or certifying its astronomical assumptions.

The author code enumerates free columns through a set. Which witness is
selected is not a portable ordering guarantee; the recorded witness itself
is sufficient, fully pinned and independently checked. This does not affect
existence or the accepted claim. No edit to author inputs was made.

## Evidence identity and execution scope

Reviewed root result SHA256:
`5f34637ae2d32de310ab66d2b03e74eaebc82a8e93dfc6cd173e74016dd7aa2b`.
Reviewed derivation SHA256:
`eeba650f3bffa1b74eb2315af367b71184a4ea61e819bc491018721ad38bf1ff`.
Inherited NPZ SHA256:
`f27b6da0437825255d71462f6cb7e91d2becfb6152b99b74cf7f6ac4f013c96c`.

The existing bounded computation is the evidence run. This review did not
launch a fresh seed or rerun its witness search; it performed read-only hash,
implementation and exact returned-certificate checks in an inline Python
process and ran validate_manifest.py with the repository root. It did not
claim new experimental resource limits for those audit operations.

## Strongest safe conclusion and remaining gap

Fixing this model's constant map offset alone does not identify this finite
pressure-gradient target, even locally at the supplied positive decreasing
synthetic baseline. The witnesses differ by about 0.4305% of the absolute
baseline gradient while producing identical compressed observations. This
lower bound on ambiguity is not a sharp extremum, an observational error bar,
a fit to the actual map or a statement about all available map pixels.

No MOND force, source requirement or missing mass is computed, so no Q/R/M
branch or a0 normalization is selected by this result. A physical force bridge
still needs calibrated pressure/density/composition, both reference scales,
and distinct vacuum versus H-scaling assumptions. FGF-022 separately addresses
constrained extrema; this audit supplies neither its result nor a duplicate run.
