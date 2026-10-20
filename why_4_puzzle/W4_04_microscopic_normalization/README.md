# W4-04: direct microscopic normalization attempt

The requested selection of **xi=1/4 was not achieved**. The three tested
microscopic routes produce genuine normalization relations, but none
supplies an operational MOND coefficient. Kappa=1/2 remains FITTED.

The main advance is to replace an unspecified portal with a concrete
calculation target. If one mediator supplies both Newtonian and deep-MOND
forces, with static energy coefficients C2 at high gradient and C3 at low
gradient, then spherical flux fixes

    xi=32pi C2^3/(9 epsilon C3^2),
    xi=1/4  iff  epsilon C3^2/C2^3=128pi/9.

This dictionary uses actual physical source normalization and force-law G.
Common species multiplicities and hbar factors can cancel from the ratio.
It is not necessary to reject a mechanism just because its coefficients
arise from a quantum loop. The equation is a conditional reduction, not
a new principle fixing the ratio. For tensor-plus-mediator theories the
measured G dictionary must be derived again.

## What the physics actually fixed

**Local supersymmetry:** an explicit locally supersymmetric Born-Infeld/FI
action has vacuum V=2T-3Mp^2m32^2. On its restricted m32=0 branch,
T=V/2 and the pure-electric expansion contains `E^4/(4V)`. This is an
actual quarter in a vacuum/response coefficient. Its meaning matters:
it is a fourth-order electric susceptibility, not xi. The sourced field
is Coulombic at weak field and saturates at strong field; it does not
produce the MOND square-root force. Allowing the published m32 parameter
also permits a fixed-vacuum, fixed-canonical-source deformation of T.
No all-orders nonrenormalization is inferred from the classical action.

**Common finite quantum determinant:** a constructed scalar/Dirac spectrum
makes the induced vacuum and Einstein coefficients finite and positive,
without free regulator moments. Its low-gradient expansion is analytic,
so the necessary positive cubic response is absent. Its induced scalar
spurion slope is negative, and promoting its truncated Einstein action
to a vacuum gives 3<H^2/M^2<4: this example is outside the required
low-curvature regime. It is not a complete cosmological model. These
facts are stronger diagnostics than merely leaving a cutoff unfixed.

**The thermal escape:** a gapless bosonic zero mode really generates an
X^(3/2) term and gives common amplitude ratios 16/15 or 16/5, with the
normalizations stated in PROOF.md. However its cubic sign is wrong for
healthy deep MOND, its quadratic dominates at low gradient, and the state
has w=1/3. Its small-gradient quadratic is also not a high-gradient force
coefficient. The formal ratios are therefore not predictions for xi.

**String D3 normalization:** DBI and bulk gravity fix the canonical
endpoint critical electric force to the fundamental-string tension.
An acceleration still depends on the source's actual mass; a stretched
string gives the electric-component scale c^2/L, with L a separation.
The physical vacuum is not automatically the brane tension. In the
specified tree-level GKP background the net vacuum cancels. The leading
KKLT modulus potential admits a stable Minkowski crossing and neighboring
positive-vacuum branch, so its stabilization does not fix a universal
threshold/vacuum ratio. Neither electric threshold has a MOND force tail.

These are scoped failures of explicit actions and states. They do not
exclude all local supergravities, string compactifications, critical
media or interacting infrared mechanisms.

## What remains to be forced

The essential missing object is now specific: a single healthy microscopic
state/action must generate a **positive low-gradient cubic**, a separately
force-calibrated **high-gradient quadratic**, and an **absolute positive
vacuum**, and a symmetry or exact dynamical relation must fix their amplitude
ratio to the value above. A correct ratio of unrelated thresholds does not
satisfy this condition.

The best concrete continuation is an explicit gapless interacting or
constrained medium whose response avoids the free thermal model's sign
and state failures, with its gravity and vacuum terms computed in the same
state. No such model is presently established here. Merely adding a MOND
term to the supersymmetric BI model introduces a new coefficient unless
the larger symmetry and action derive it. None of the checked sources
provides that derivation. The current work does not exhaust all such models.

## Evidence and review

See [PROOF.md](PROOF.md) for the derivations and their exact hypotheses,
[SOURCES.md](SOURCES.md) for primary versions/equations, and
[REVIEW.md](REVIEW.md) for review provenance and restrictions.

Base checkpoint: `e8bb2ae70ad6b2c86790b9312861ac2269227f71`.
Criteria were committed alone as `1eb877c0d`; explicit verification scope
was committed before checker implementation as `72630f612`. Three
read-only agents pursued the microscopic routes. The coordinator derived
the operational invariant and reconciled their raw calculations. A separate
review reconstructed the proof, including an isolated additional E review.

Results commit: `a811e18fb`. Scoped campaign rows K631-K635 record R1,
R2, R2T, R3 and the operational reduction R4. The register's integrity
check passes; no determinate operational value or menu was added, so
its existing look-elsewhere probabilities are unchanged. Current research
scope and untried continuations are in [HANDOFF.md](HANDOFF.md).

The checker has 39 exact assertions. Rational log intervals certify the
spectral signs; decimal values only report those exact intervals. There
are no numerical parameter scans. Five baseline checks fail as intended
under the four declared physical mutations, with exit 1. The common-source
rescaling remains invariant as it should. General-n flux powers and the
thermal equation of state are supplied analytically rather than inferred
from checker counts. Full cosmological stability, quantum corrections,
and the flux landscape are outside verification scope.

The first bounded run passed 39/39. Review then made small explicit domain
restrictions and separated the D3 electric component from the total BPS
force; final bounded manifests pin that corrected proof. Nice scheduling
was requested but denied by the sandbox; each run remains one Python
process and one library thread, under a few seconds.

Reproduce from repository root, supplying an output JSON path:

    OMP_NUM_THREADS=1 python3 why_4_puzzle/W4_04_microscopic_normalization/checks.py /tmp/w4_04_normal.json
    W4_04_MUTATE=1 OMP_NUM_THREADS=1 python3 why_4_puzzle/W4_04_microscopic_normalization/checks.py /tmp/w4_04_mutate.json

The control command intentionally exits 1. No source downloads, p63,
four-form or Lean duplication, manuscript integration, heavy jobs or
scheduled continuations were performed. The data quoted only as inherited
status are CFG493's kappa_Lambda=0.417+/-0.095 and kappa_crit=0.345+/-0.078;
footings are separate and neither enters this calculation.
