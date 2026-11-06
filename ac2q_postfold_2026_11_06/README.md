# AC2q post-fold investigation — PF07 dynamic-layer checkpoint, 2026-11-06

**Outcome: a standard shock prescription does not close AC2q. Its post-break
predictivity needs a justified completion. Full-action failure is not proved.**

The requested three-way classification is only partially resolved: the ordinary
finite-shock survival route is excluded under explicit conditions; whether the
native action avoids that route or generates its own stress-carrying completion
remains open. Do not relabel this as "AC2q globally refuted" or "extension proved
unavoidable for every possible solution".

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
