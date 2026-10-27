# Focused independent audit of the current duality note

Reviewer: `micro_exchange`, separate from the derivation's `density_duality`
author. Shared repository/model context limits independence; the decisive
algebra below was recomputed from the displayed definitions, not inferred
from the author's reported finite checks. No manuscript or other lane file
was edited. This is a focused proof audit, not a whole-manuscript referee
report or an external-literature audit.

Target: `../density_duality/DENSITY_DUALITY.md`, initial reviewed SHA-256
`79dabea29fadc953f8bf90d37ec93f0068b4fd90d708437f7854242421c55b64`.

Normalized claim: on a smooth nonzero-amplitude common-phase chart of the
specified charge-one/charge-two model, the conserved total current has a
first-order two-form dual. This represents signed reference-charge density,
not arbitrary positive rest density. A bare rational `W(|P|)` of the dual
potential is not a gauge-invariant local energy. A separate physical
polarization is a different degree-of-freedom assignment.

Primary verdict for the initial text: **correct only after a stated
restriction**. The only required restriction found is local and explicit:
in equation (1), the omitted terms must be separately invariant under the
two species phase rotations if the cubic-only species divergences in (3)
are claimed exactly. Common weighted U(1) invariance alone permits, for
example, `(X* Phi^2)^2+h.c.`, which adds a relative-phase source. The total
current remains conserved in that broader theory. The author was informed
and acknowledged this restriction. All other audited displayed statements
below pass within their stated chart, boundary, and approximation domains.

Dependency/obligation audit:

| Obligation | Independent reconstruction | Status |
|---|---|---|
| Exact current sources | EOM give `div jPhi=-4g Im(X*Phi^2)`, `div jX=+2g Im(X*Phi^2)` | Passed for selected cubic-only relative-phase coupling; dots restriction required |
| Common phase completion | `f^2 dtheta^2+h^2(2dtheta+ddelta)^2=A(dtheta+a)^2+f^2h^2 ddelta^2/A`, `A=f^2+4h^2`, `a=2h^2 ddelta/A` | Passed for stated positive-amplitude phase chart |
| First-order coefficient | Eliminating J from `-J^2/(4A)+J dot(dtheta+a)` returns the exact completed square | Passed |
| Dual component signs | Direct epsilon expansion gives `J0=div Q` and `Ji=-dot Q_i+(curl C)_i` | Passed with epsilon0123=+1 and the displayed component definitions |
| Gauge action | `delta Q=curl Lambda`, `delta C=dot Lambda-grad Lambda0` makes both current components unchanged | Passed; these transverse P changes are redundancy |
| Compact normalization | `b=2pi B` gives `N=(1/2pi) integral db`; one charge-one phase winding couples to integral b | Passed for stated charge-one compactness convention; charge-two-only sector separately flagged |
| Charge versus mass | Subtracting mJ0 gives exactly `2m nPhi-+(M-2m)nX++(M+2m)nX-` | Passed in leading NR population dictionary |
| Neutral counterexample | Equal positive and negative populations give J0=0 with positive rest density | Passed; no positive-density conclusion from this Noether current |
| NR flux dual inertia | Eliminating j from (17) returns (16); substituting `rho=mn`, `m j=-dot P+curl calA` gives inertia `1/(2rho)` | Passed on n>0 chart, with irrotationality and boundary restrictions retained |
| Newtonian coupling | `-rho U=P dot grad U-div(UP)` and varying U yields `Delta U=K(rhob+rho)` | Passed; physical density is counted once |
| Bare W obstruction | Compact curl change can create nonzero P at fixed zero div P; W>0 below saturation, so its integrated energy changes | Passed; local gauge invariance fails, including at fixed stock |
| Longitudinal completion | `P_L=grad Delta^-1 rho` gives positive quadratic kernel `K|rho_k|^2/(2k^2)` | Passed; this is nonlocal in density, not a local EOS |
| W Legendre partner | Inverting `E=W'(p)` gives `p=a0 E/[K(a0+E)]`; subtraction yields displayed F | Passed below saturation; not a propagation-health proof |
| Finite stock/global sectors | Divergence theorem requires 1/r^2 flux tail for nonzero compact stock; global exact B on a closed slice has zero integrated dB | Passed with smoothness/topology qualifications stated |

Decisive scope point: the W obstruction concerns *the dual potential of the
conserved microscopic current*. It cannot be promoted to a claim that a
new, independent material polarization or a nonlinear mediator displacement
is impossible. Conversely, merely declaring such a physical polarization
does not prove that it is the microscopic dual B. The note correctly keeps
those assignments separate and identifies the needed new kernel/source
matching.

The pure-gauge counterexample uses no extra physical transverse mode. At
P=0 the linear variation of W vanishes, but a finite small pure-gauge curl
has strictly positive quadratic energy. A smooth compact cutoff and an
overall amplitude rescaling keep it globally below saturation and leave
boundary flux fixed. Thus the finite variation, rather than a nonzero first
derivative at the origin, is the appropriate contradiction.

The common-phase duality's vacuum chart limitation is appropriately stated:
it cannot be extended through amplitude zeros by simply setting A=0 in
the denominator, and a neutral incoherent bath has no stipulated common
classical phase. These limitations do not weaken the independent population
counterexample.

Computation audit: read `../density_duality/check_exact.py` and its finite
assertions. The phase-current algebra, gauge components and Legendre checks
match the displayed objects; their finite symbolic checks do not certify
global topology, boundary falloffs or physical population identification.
Executed the documented manifest validator on `../density_duality/run_002/`
with the repository root; it returned `valid evidence record (run status:
completed)`. No new numerical experiment was necessary for this review.
The author's external-source extraction was read but not independently
re-authenticated here; all conclusions above use the internal displayed
algebra and ordinary local current duality.

Strongest safe statement: for the selected action and stated smooth chart,
the exact common Noether current has the normalized local dual, while both
positive-rest-density identification for the neutral produced population and
an undifferentiated local rational W of that dual potential fail. A separate
physical polarization remains an unmatched model extension. The cheapest
remaining check is the author's proposed occupied-state static kernel and
source assignment, not another dual gauge rewriting.

## Addendum: final restricted version checked

Re-read the changed equation-(1) paragraph at final note SHA-256
`bb45b6bddef696c689f9e60ca3f4bb608a8ce8914cab694e6027383d675f2fff`.
It now explicitly restricts the omitted terms to the selected masses,
modulus potentials and portals, each separately species-phase invariant,
and makes the cubic the only relative-phase transfer. The exact restriction
required above is present. The final normalized claim's primary verdict is
therefore **proved as written**, within the chart, boundary and NR domains
already stated in the note. This does not promote the original proposed
positive-mass/W derivation to a theorem; the valid result is precisely its
restricted dual construction and the two explicit obstruction arguments.
No remaining actionable correctness issue was found in the assigned scope.
