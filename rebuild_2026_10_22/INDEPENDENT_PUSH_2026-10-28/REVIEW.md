# Review provenance and scope

Base: `7954d48377463cafcae3e8dbb09454134aef384f` and pinned dirty inputs.

The coordinator read the actual CL3/LEE1 concentration and threshold code,
the BS1 reported-variant code, the original scorer gate, the new scripts and
their numerical outputs. A direct independent arithmetic check reproduced
eta(c_f)/eta(L)=1.788059299 at 10^12 Msun. The coordinator checked the basin
energy primitive, shell restrictions and normalization algebra separately
from the author. The exact source/table records, not agent agreement, support
the observational claims.

Fresh reviewer `synthesis_review` received the current theory and raw scorer
code without the author's desired verdict. It reconstructed the core/switch
relationship and required these corrections, now incorporated:

- distinguish CL3 own-mass thresholds, BS1's fixed-T primary, and the reported
  BS1 CL3_L3.75 variant;
- limit BS1's basin flags to the pipelines that actually change them, and
  disclose that isolated-lensing scores are carried;
- limit the 5.2715 turnaround budget to clusters and state the other mass
  assignments;
- label the exact S9 core crossings as the X43/background-A EPS diagnostic,
  rather than numerical identities of every interpolated scorer;
- preserve the asymmetric-drift limitation and no-new-grade status of the
  IC1613 inclination sensitivity.

Its final review found no further material issue within that focused scope.
It did not rerun the raw astronomical harness or validate a covariant theory.
The separate fresh basin reviewer, restrictions, independent quadrature and
audited derivation hash are in `basin_kappa/INDEPENDENT_REVIEW.md`. The root
coordinator also independently confirmed that NGC4261/KT39659 is actually
FAINT with mgas=0 in both original HG result files; the new association does
not itself specify its gas mass at the test radius.

Normal-run and deliberate-failure manifests were validated against current
input hashes. Normal execution and a valid manifest verify only their stated
finite contract; a deliberate mutation's `failed` status is expected control
evidence. Initial environment launch failures are retained, not recast as
scientific tests. Per-package reports contain commands, bounds and exact hashes.

Mathematical proofreading self-review covered the new CURRENT_THEORY.md,
README.md and HANDOFF.md, including notation, units, qualifiers and links.
Routine corrections: line wrapping and wording. Mathematical-token changes
under proofreading: none. Substantive scope corrections above came from the
scientific audit and are identified as such. Unresolved scientific issues
remain in HANDOFF.md; proofreading is not their correctness certification.

No old lane or standing rule was rewritten. No commit or publication was
performed. This checkpoint records partial research progress and the exact
remaining obligations, not achievement of the open physical theory.
