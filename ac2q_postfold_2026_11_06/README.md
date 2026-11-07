# AC2q post-fold investigation — PF17 source-variation checkpoint

**Current result:** the full coupled constraints give the missing spatial
source-variation bound for existing solutions with continuous BV clock
gradient, including the regular rolling potential. The bound is C(1+Z)^2.
The native absolute-value/interaction estimate remains unproved, so full weak
existence, uniqueness and Cantor exclusion remain open. An extension is not
proved necessary.

[PF17 result and exact gaps](pf17/STATUS.md) ·
[Native source estimate](pf17/SOURCE_VARIATION.md) ·
[Cantor-source identity](pf17/CANTOR_SOURCE.md) ·
[Independent audit](pf17/review/SOURCE_AUDIT.md)

## PF16: conditional temporal regularity

Existing bounded on-branch BV solutions evolve absolutely continuously in
spatial L1. This excludes purely temporal Cantor activation but allows moving
spatial Cantor variation. A local positive density cannot universally cancel
acoustic compression. See [PF16 status](pf16/STATUS.md).

## PF15: diffuse singularities

Diffuse stress divergence adds no independent Cantor principal restriction.
Acoustic polarization does not establish existence or unique flow. A checked
SBV theorem has not been shown applicable to the native coupling, and SBV
alone would not restore strong regularity. See [PF15 status](pf15/STATUS.md).

## PF14: native compactness and auxiliary reconstruction

The bounded native source has a fixed conditional limit; spatial auxiliary
reconstruction is unique, with local existence and stability on branch. Small
BV clock jumps are excluded in the declared neighborhood. See
[PF14 status](pf14/STATUS.md). None is a coupled temporal uniqueness theorem.

## PF13: direct weak formulation

A bounded first-order variational weak system is defined with all Einstein
equations retained. The differentiated inverse has a one-time forcing-path
obstruction, not a demonstrated native spacetime ambiguity. See
[PF13 status](pf13/STATUS.md); PF14 narrows its interpretation.

## PF12: controlled incoming terminal data

The breaking packet has compact fields, Lipschitz polarization, controlled
metric derivatives and unique BV clock-gradient terminal traces. These are
incoming results, not postbreak evolution. See [PF12 status](pf12/STATUS.md).

## PF11: coupled surface balance

A positively fed combined clock/boost sheet cannot grow from zero initial
charge in the regular matched Einstein-interface class, without assuming
finite interior-current variation. See [PF11 status](pf11/STATUS.md) and
[its independent audit](pf11/review/FED_LAYER_AUDIT.md).

## PF10: full-current exclusion and positive-feed question

The finite-current matched-layer exclusion, restricted hyperbolicity barrier,
and scalar-only positive-feed condition are preserved in
[PF10 status](pf10/STATUS.md). PF11 resolves the positive-feed mechanism in the
regular matched Einstein junction class with zero incoming slice charge.

## PF09: native coupled breakdown

**Outcome: native coupled strong evolution can break. A uniquely selected
singular completion has not been established; unavoidable new physics is not
proved.**

The finite-regularity evolution and constraint-propagation gap is now closed
in the stated periodic planar class. The native hold-law cusp is retained.
An independently audited construction proves local strong evolution and a
continuation criterion; exact homogeneous residual equations preserve every
constraint. Combined with a uniform geometric/variation bootstrap and weighted
Riccati comparison, it proves finite-gradient breakdown for sufficiently narrow
small-amplitude packets. Regular positive rolling potentials are covered by
explicit checked source terms. This is not a curvature-singularity or
astrophysical event-time prediction.

Singular stress exclusions have also been strengthened, but retain explicit
trace, geometry and measure hypotheses. No general singular native
existence/uniqueness theorem or universal exclusion has been proved.

[Current result and exact limits](pf09/STATUS.md) ·
[Theorem chain](pf09/THEOREM_CHAIN.md) ·
[Local evolution audit](pf09/review/LOCAL_EVOLUTION_AUDIT.md) ·
[Constraint propagation](pf09/review/RESIDUAL_PROPAGATION.md) ·
[Packet-breakdown audit](pf09/review/COMPACT_BOOTSTRAP_AUDIT.md)

## PF08: full coupled steepening and conditional breakdown structure

The reduced constrained evolution now checks mean and differentiated-constraint
compatibility against the native canonical equation. Refinement from 511 to
2047 independent points extends the resolved interval while gradients grow;
all reported late stops are resolution limits, not physical events. Curved
coercivity and exact weighted characteristic identities remove two obstacles
to a full coupled breakdown argument. Local-existence/continuation foundations
and singular native selection remain open.

[Current PF08 result and limits](pf08/STATUS.md) ·
[Live continuation record](pf08/CURRENT_WORK.md) ·
[Curved inverse audit](pf08/principal_review/CURVED_COERCIVITY.md)

## PF07: solver repair and genuinely time-dependent layers

The constrained solver now has a checked pre-break interval: curvature subtraction
and padded nonlinear evaluation remove the early aliasing instability. Space,
time, padding and raw-constraint checks pass; finer runs show steepening but
stop at their declared accuracy limits. No physical singularity time is claimed.

The regular corner obstruction survives time dependence exactly. Additional
analytic estimates exclude polarization and scalar surface storage, and native
matter surface stress, for the explicitly bounded clock/metric/cap regime with
strong continuous traces and finite current-measure limits. These are stronger
results than the earlier stationary calculation. Singular regimes outside those
hypotheses and full coupled smooth-data breakdown remain open.

[Current result and precise limits](pf07/STATUS.md) ·
[Independent dynamic-layer review](coupled/time_layer_review/REVIEW.md) ·
[Auxiliary stress and scalar-current proof](coupled/time_layer_review/AUXILIARY_STRESS.md) ·
[Checked numerical comparisons](pf07/comparison_t1/result.json) ·
[Diagnostic figure](pf07/evolution_diagnostics.png)

## Earlier PF06 coupled-field update

The native metric cannot carry the missing stress of a regular stationary
planar corner with stationary field profiles: its own conjugate-flux conditions force the metric derivatives
to be continuous. A bounded quasi-stationary negative-divergence polarization
sheet is excluded too. The coupled homogeneous scalar sector has a wave-like
high-frequency principal part, with no new k^4 regularizer.

Full nonlinear singularity avoidance and rapidly time-dependent singular
layers remain open. The longer coupled simulations are numerically unreliable;
their termination is not a physical failure result. Constraint-satisfying
initial data and independently reviewed continuum evolution equations are now
available. See [coupled status and limits](coupled/STATUS.md),
[junction derivation](coupled/JUNCTION_RESULT.md),
[ADM equations](coupled/ADM_FORMULATION.md), and
[independent solver review](coupled/REVIEW_SOLVER.md).

## Earlier PF01–03 results

- AC10's "fold" event is J=1e-3, not J=0. Its compressed positive-charge rows do
  not distinguish true crossing from native pressure steepening into a shock.
- The native positive-charge principal equations have an explicit smooth wave
  that breaks at t=5/6 with bounded density. Pressure does not imply smoothness.
- In the PN system, mass plus scalar/Bernoulli conservation and mass plus momentum
  conservation demand different finite shocks. Their mismatch is cubic in the
  density jump and nonzero for every unequal positive pair.
- Retaining the exact relativistic clock terms does not rescue a defect-free
  same-direction planar stationary on-branch shock, for 0<=gamma*s^2<1/3. The
  proof uses strict convexity of the derivative of the reduced action, not a
  small-s expansion. No global formation or singular-gravity theorem is claimed.
- Numerical continuations agree before breaking and differ afterward. At 2048
  cells their density L1 difference is 0.082548 (7.64% of the initial mean);
  refinement changes are much smaller. An independent Riemann benchmark gives
  shock speeds 0.780776 versus 0.854638. These are dimensionless model tests,
  not new galaxy predictions or two solutions of a single specified weak theory.

[Derivation and results](DERIVATION.md) · [Self-audit](AUDIT.md) ·
[Continuation](HANDOFF.md) · [Frozen criteria](FROZEN_CRITERIA.md) ·
[Exact-interface contract](EXACT_INTERFACE_CONTRACT.md)

- The exact time-dependent flat planar equations are now derived. Their native
  high-k block has no k^4 regulator; this does not exclude all nonlinear or
  gravitating completions. See [native dynamics](NATIVE_DYNAMICS.md).

## Evidence

- [PF01 result](run001/result.json): 37/37 checks, completed.
- [PF01 wrong-pressure control](mutate001/result.json): four intended RH failures.
- [PF02 result](exact001/result.json): 21/21 checks, completed; 13 root pairs,
  two explicitly reported no-pair fixtures.
- [PF02 reversed-defect control](exact_mutate001/result.json): 13 intended failures.
- [PF03 corrected run](native002/result.json): 21/21 checks. The original
  [run](native001/result.json) retains two failed hand-expectation checks; the
  [mixing control](native_mutate002/result.json) must fail two root checks.
- All seven computation manifests validate, including current input hashes.
- PF01–03 review status: self-review. The later coupled canonical equations
  and linear benchmark have an independent review. No physical parameters adopted.

Criteria commits: 57f9b8140d, 21cb54b10b, bdaee092bf. Earlier lanes were not edited.
The parent physical question remains open; this directory is the live entry
point for this investigation. No job remains running.
