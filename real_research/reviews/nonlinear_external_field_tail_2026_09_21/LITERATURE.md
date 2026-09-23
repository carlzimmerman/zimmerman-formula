# Attribution and bounded overlap check

Checked 2026-09-21. This is an English-language, scoped repository and web search.
The same investigator did discovery and verification. There was no independent
reviewer, exhaustive ADS/MathSciNet citation census, or authenticated source
archive created for this package.

## Exact scope of the proposed addition

The object of the search was not the existence of MOND external-field effects,
lopsidedness, anisotropic Green functions, or differences between AQUAL and
QUMOND. All are known. The candidate addition is the combination of:

1. the explicit quadratic exterior potential for arbitrary smooth response;
2. cancellation of the second response derivative from its odd axial degree -3
   coefficient;
3. removal of an arbitrary degree -2 source dipole by the r, 2r force filter;
4. the resulting coefficient's relation to isolated orbital slope, with distinct
   AQUAL and QUMOND expressions at matched physical acceleration.

**Classification:** apparently new within the stated search scope as a combined
asymptotic extraction relation; the exact global literature priority of the
quadratic potential or the combined relation remains unestablished. This is a
calculation within known theories. It does not introduce a new fundamental law.

## Primary sources inspected

**Indranil Banik and Hongsheng Zhao, _The External Field Dominated Solution In
QUMOND & AQUAL: Application To Tidal Streams_, arXiv:1509.08457v3, 2020-04-04.**
[Primary HTML](https://arxiv.org/html/1509.08457v3).
Sections 2–3 give the linearized operators, stretched AQUAL Green function and
QUMOND angular potential. Their n is a potential gradient, as it is here;
their L0 is our L, and their K0 is our k_nu. Their first-order calculation
authenticates the starting equations and normalization. It does not supply this
package's quadratic calculation or its two-radius filter. The paper credits the
older AQUAL result to Bekenstein–Milgrom (1984) and Milgrom (1986); these were not
fully re-audited here. The nonlinear identities in PROOF are derived directly
from the stated PDE and do not rely on an unverified theorem in those papers.

**G. F. Thomas, B. Famaey, R. Ibata, F. Renaud, N. F. Martin and P. Kroupa,
_Stellar streams as gravitational experiments II. Asymmetric tails of globular
cluster streams_, arXiv:1709.01934v1, 2017-09-06.**
[Primary PDF](https://arxiv.org/pdf/1709.01934v1).
Sections 2–3, equations (1)–(6), explicitly use QUMOND and investigate lopsided
potentials, including a point-mass host and satellite, numerically computed
physical potentials and the established linear boundary condition. This is
prior art for nonlinear external-field lopsidedness and its possible stream
consequences, not an observational validation of our statistic. The inspected
copy carries a 2018 manuscript date but an arXiv v1 footer dated 2017-09-06;
the arXiv version identifier is the source pin used here.

Discovery also found Wu et al., arXiv:1706.07825 (galaxy lopsidedness), and
Chae–Milgrom, arXiv:2201.02109 (numerical AQUAL/QUMOND external-field solutions).
Their full texts were not used as theorem evidence in this package; their
existence limits any broad claim that nonlinear EFE or theory discrimination
is newly proposed here.

## Repository overlap

The reviewed recent packages were the unit-response action, orbital-shape law,
linear field–orbit reciprocity, and particle-free validation roadmap dated
2026-09-20. The nearest earlier numerical work found was:

- `real_research/reviews/directional_efe_2026/laneA_predictions.py`: directional
  lopsidedness from a QUMOND Legendre/Green calculation, plus a proposed
  observational mapping. Its free-fall/reference convention must be reconciled
  before reusing its force arrays; it was inspected, not imported or modified.
- `real_research/reviews/mi_route_a_efe_dipole_resolve_2026.py`: kernel-specific
  directional predictions, including a deep-EFE sign change. A sign change in
  the raw asymmetry is therefore not new to this repository.
- `qwen_claude_field_theory/IDEAS_101_200.md`, I191: a proposed second-order EFE
  saturation calculation. It does not present this arbitrary-response exterior
  potential and dipole-eliminated orbital relation.

No matching combined theorem was located. This is bounded search evidence,
not an exhaustive proof that no equivalent formula exists among all files.

## Search record and blind spots

Repository searches used `rg` over Markdown, LaTeX and Python, first in
`real_research`, `qwen_claude_field_theory`, `fable_independent_2026`, and
`deepseek_push`, then across the repo. Queries included second-order/external
field, nonlinear/dipole/far-field, odd tail, dipole cancellation/subtraction,
antipodal, orbital slope/curvature, and filenames combining EFE with asymmetry
or nonlinear corrections. Bulk data and dependency directories were excluded.

Two web search strategies were used: exact/synonym theorem terms, and older
phenomenological terms followed to primary references. Representative queries:

- `AQUAL external field second order perturbation potential dipole nonlinear`
- `MOND external field quadrupole rotation curve slope finite perturbation antipodal`
- `"MOND" "second order" "external field" potential`
- `"AQUAL" "dipole" external nonlinear`
- `"MOND" "asymptotic" "dipole" potential external field`
- `"MOND" "r^{-3}" "external"`
- `"MOND" "lopsidedness" "external field" arxiv`
- `AQUAL QUMOND nonlinear external field asymptotic expansion odd potential second order dipole coefficient`
- `"MOND" "asymmetry" "rotation curve slope"`

The search included publicly indexed material available on the check date,
with older work reached through the inspected papers' references. Forward
citation coverage was incomplete. Adjacent nonlinear electrostatics was surfaced
but not exhaustively reviewed. Search snippets and failed HTML retrievals were
not used as proof. The two primary sources were read through arXiv HTML/PDF;
local cache lookups were performed, but no source bytes were retained here.
