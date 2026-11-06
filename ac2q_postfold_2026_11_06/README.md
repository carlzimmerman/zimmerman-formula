# AC2q post-fold investigation — PF10 combined-layer checkpoint, 2026-11-06

**Current result:** the combined clock/boost stress construction fails the
full scalar equation in the matched finite-current regular-interface class.
A separate small-kinetic branch barrier rules out reaching its high-clock
component through an everywhere-hyperbolic smooth layer. General singular
continuation and unique selection remain open; unavoidable new physics is not
proved.

[PF10 result, hypotheses and remaining gap](pf10/STATUS.md) ·
[Full-current exclusion](pf10/COMBINED_CURRENT_EXCLUSION.md) ·
[Independent audit](pf10/review/COMBINED_CURRENT_AUDIT.md) ·
[Restricted branch barrier](pf10/BRANCH_BARRIER.md)

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
