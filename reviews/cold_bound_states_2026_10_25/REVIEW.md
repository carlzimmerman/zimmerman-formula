# Self-review and focused proof audit

Claim: no nontrivial smooth, spatially localized, exactly time-periodic real
solution exists for the stated canonical flat-space field at uniform d>=8,
provided all integrations and averaged virial boundary terms are valid and
|q|<pi. Verdict: proved as written under these explicit hypotheses.

Dependencies: polynomial identity -> nonnegative potential; trigonometric
inequality -> q V_q>=2V strictly off zero; equation times q -> T=G+J;
spatial action scaling -> 3T/2-G/2-3U=0; combination -> nonnegative integral zero.
The time integrations use periodic endpoints. Spatial scaling is legitimate
only with the stated regularity/decay, not assumed from a finite numeric box.
At d=8 the positive higher powers still imply strictness. No division by q or
by d-8 is required at their zeros. Both +/-q obey the same even-potential proof.
All these obligations pass in self-review. Gravity, varying sources, broken
vacuum asymptotics and transient radiation are out of scope, not refuted.

Boundary calculation: the normalizable modes are established only for three
fixed-source planar profiles and the declared mesh/domain comparisons. The
35 penetration estimates substitute shell-average densities into homogeneous
expressions. Their extrapolation to real clumpy profiles remains conditional.
Mode norm is not called gravitational mass, nor is occupation inferred.

Gravitational surrogate: quartic truncation is diagnosed as unreliable for
most requirement rows, so its polytrope radius is not asserted to be a physical
prediction. The follow-up integrates the full potential but remains homogeneous
and fixed-source; it is not a coupled relativistic clump solution. The effective
oscillator pressure is distinguished from the full matter/scalar stress.

Proofreading scope: complete new REPORT.md. Definitions of T,G,U,J, canonical
time, energy units, squared masses and the dimensionless epsilon were checked.
No mathematical-token corrections required. Source-model and approximation
limits are retained adjacent to each inference.

Provenance: self-review at the pre-commit checkpoint continuing 3f3d00e011;
not independent certification. Normal and finite-amplitude manifests validate
with completed status; mutation validates with expected failed status from
quartic symbolic matching. The full physical goal remains unresolved.
