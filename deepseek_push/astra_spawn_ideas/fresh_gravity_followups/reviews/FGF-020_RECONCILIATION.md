# FGF-020: exact positive-density moment feasibility accepted

Coordinator read the independent raw proof and verified every required result
field and listed input/output hash. Result SHA256:
`d5fe62ddef2d916ef7bfe9587bee00ee20feb203d3d84456d44a43981b9fbe18`.
This is a proof-only audit of DM1, with code inspection and provenance
validation; it did not independently rerun the synthetic binary64 force table.

For a nonatomic normalized volume, mu>0, V=nu-mu²>0, 0<epsilon<1 and L>0,
accept the exact positive measurable-profile feasibility conditions

    epsilon <= V/[V+(L-mu)²],  epsilon L < mu.

The coordinator independently verifies the complement construction: with
conditional mean m>0 and variance v>0, levels m/2 and m+2v/m weighted by
4v/(m²+4v) and m²/(m²+4v) respectively give mean m and variance v. At v=0
the complement is constant. The equality cases and zero-global-variance
exception in the raw proof remain mandatory. This extends DM1's sufficient
equal-volume example without altering its pinned derivation.

Thus any finite positive shell density can be hidden in a sufficiently small
positive volume while preserving those two idealized moments. An independent
minimum physical shell volume gives a real bound; a PSF width alone is not
that physical prior. The result is a counterexample to inference from two
integrated numbers, not a density-profile fit or a smooth hydrostatic solution.

Accept the emissivity limitation: fixed pressure with changed density changes
temperature, so conserving the unweighted density-squared moment does not
prove unchanged actual detector counts. The returned third-moment example
refutes that inference for one explicit toy response function; it is not an
assertion about a real plasma law. Both core scale footings and separate
vacuum/frozen-H Q/R examples remain correctly labeled synthetic. No full
filtered-MONO or metric claim follows.

Prefer existing FGF-019 spatial-projection work and actual thermal-response
constraints over another unchanged integrated-moment test. The main catalog's
AS1759 is related emissivity-law work; cross-link evidence before dispatching
an equivalent task.
