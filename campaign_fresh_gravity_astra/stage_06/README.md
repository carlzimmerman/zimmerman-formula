# Checkpoint: spatial pressure information and filter-transfer audit

2026-09-27. Parent: [stage five](../stage_05/README.md). The physical objective
remains open. This pass executed two observation calculations, independent
finite checks, a new conditional functional proof, and a scoped review of a
new primary-catalog return. Actual agents and claims are in the shared queue;
none of this work is relabeled as a DeepSeek execution.

## What changed

| Evidence | Checked result | Remaining limitation |
|---|---|---|
| FGF-019 | In the measured ZW1215 geometry, a twelve-bin spherical pressure model admits positive decreasing profiles with identical bins and slopes differing by 0.631677%. Root independently verified the returned matrix with QR and direct node slopes. | Synthetic pair, finite compression, not a fit of the observed map or a sharp range of possible slopes. |
| FGF-017 | Relative catalog distance/emissivity closure curves now specify the required independent bounds. Root reproduced 64 Q/R checks with a quartic and separate bisection. | Density-shape assumption, actual angular-distance/centering conventions and emissivity calibration remain unverified. |
| PF1 | Independently audited exact proof: under fixed bounded kernels and sufficient off-target functional rank, smooth nonnegative pressure profiles preserve all finite measurements yet have unbounded point derivatives. | Actual instrument hypotheses and physical admissibility must be established; no monotone/hydrostatic continuum construction is claimed. |
| AS006 review | Exact unfiltered scale identity survives; general-kernel asymptotics and small-filter claims require additional hypotheses. A fixed deep toy current has an algebraic outer heat correction. | The actual filtered-MONO current, radial flux constant, adjoint/domain and controlled force expansion remain open. |

FGF-019's full-annulus inspection found every A644 pixel masked and every
ZW1215 pixel unmasked within the inspected five-target-radius domains.
Coverage does not supply covariance. The operator uses an explicit fiducial
distance, finite outer support and flat-sky beam approximation. Original map
pixels and measured outer annuli contain information omitted by its twelve-bin
compression; their information is not ruled out by this result.

For FGF-017, at unchanged emissivity the earliest favorable distance factors
are 1.1027919144 (A644) and 1.3656536194 (ZW1215) on the constant-vacuum branch.
The separate H comparison gives 1.0987713667 and 1.3577908394. These use the
alternative normalization and registered M; Q and R have their own recorded
thresholds. They are conditional root locations, not measured corrections.
The root's independent Q/R check agreed within 1.71e-13 over 64 cases.
Two central ZW1215 interpolation cells retain conservative crossing ambiguity;
none of the favorable cells did. Support enclosures use binary64 analytic
slope bounds, not directed-rounding interval certificates.

## New exact proof and finite controls

[PF1](pressure_functional/DERIVATION.md) builds a local perturbation of height
O(delta^alpha), 0<alpha<1, with derivative b delta^(alpha-1). Fixed off-target
compensators cancel its finite observations using amplitudes O(delta^(alpha+1)).
Positivity on changed supports survives as delta shrinks. The exact independent
audit and [scope reconciliation](pressure_functional/RECONCILIATION.md) separate
global nonnegativity from global strict positivity and point derivatives from
finite-resolution gradients. Three exact rational C2 toy controls passed;
they are explicitly not C-infinity witnesses or actual instrument kernels.

## Primary-catalog intake: a useful physical distinction

The [AS006 intake](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/AS006_INTAKE_001.md)
and [independent audit](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/AS006_filter_audit_001/AUDIT.md)
retain B/a=x^(-2) for a point source and a specified unfiltered algebraic kernel.
That identity alone derives neither arbitrary-kernel asymptotics nor a finite
filter correction. A lower floor on xi also cannot certify uniformly tiny
error over all allowed larger xi.

For the fixed Euclidean toy current J=C n/r, C=sqrt(G M a), independent
componentwise differentiation gives Delta J=-2 C n/r³. A cutoff and Gaussian
tail argument proves on compact annuli

    exp[(xi²/2) Delta] J = J - xi² C n/r³ + O_K(xi^4).

This is a small-xi expansion for a fixed toy current. It identifies why an
exponentially small change in the inner filtered Newtonian argument does not
automatically imply an exponentially small change after the outer filter.
It does not establish the operative force correction: its nonlinear current
also depends on xi, and the source/flux condition must eliminate any additional
A/r² field. No missing mechanism, actual metric coupling or closure is supplied.
The audit also identifies a dimensionally inconsistent vacuum substitution in
the returned closure prose; the correct substitution is
G M a = kappa G M c sqrt(G rho_Lambda).

## Evidence and freshness

Scoped reviews: [FGF-017](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-017_RECONCILIATION.md),
[FGF-019](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-019_RECONCILIATION.md).
[Coordinator verification](COORDINATOR_VERIFICATION.json) pins this pass's
evidence. Five computation manifests validate against current inputs. FGF-017's
main run additionally has an explicit historical-metadata reconciliation:
live source_snapshot.json changed after execution, and the exact prior bytes
were recovered and verified without editing the manifest or rerunning science.
The live-path freshness failure remains visible; all actual scientific inputs
and output hashes match.

Seven newly visible primary-catalog returns were inventoried read-only. Their
claims still said running when result bundles said completed; actual external
execution was not independently observed or reassigned. AS009's seven artifact
paths resolve correctly relative to the catalog rather than the repository;
AS002 has a changed live source manifest. Both qualifications are recorded.
AS006's result bytes changed after review, while its raw derivation and quoted
issues remained. A separate current-result snapshot preserves that distinction;
the entire revised result was not silently promoted. Peer coordination handles
ownership; no primary catalog files were edited.

## Next executable decisions

1. FGF-021, newly ready and not launched: compute sharp positive/monotone
   pressure-gradient extrema for the saved finite matrix with primal/dual
   checks. For real bins, a minimum deterministic residual is not an instrument
   noise estimate or statistical exclusion. The exhibited 0.63% width alone
   does not answer whether a discrepancy-sized change is possible.
2. Authenticate actual distance, aperture, centering and thermal-response
   conventions before interpreting FGF-017 thresholds as empirical bounds.
3. Coordinate AS006's actual filtered-force continuation with its existing
   owner; do not duplicate its seed or assume exponential suppression as the
   desired answer. FGF-014 remains an independent ready dynamical obligation:
   combine conserved scale and matter perturbations on the explicitly
   supported/subtracted background, not an unsupported physical equilibrium.

Both a0 normalizations and separate vacuum/H histories remain explicit in
all applicable calculations; Q, RAR, registered M and the full filtered MONO
theory remain distinct. No partial inference result closes the physical theory.
