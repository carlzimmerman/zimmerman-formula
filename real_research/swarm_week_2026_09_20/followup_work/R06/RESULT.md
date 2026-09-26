# R06 — Lock down the unequal-mass conservation obstruction (result)

- Owner: Hermes (this lane); independent reviewer: none yet (self-review recorded)
- Execution state / claim state: completed / proved (Lean + numeric)
- Baseline: followup work order `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`;
  inputs `deepseek_push/lean/PD20_two_body_factor.lean` and
  `PD21_law_of_nature.lean` read at HEAD `29b5c74ff` and preserved as sources.
  `python3 mass_ratio_counterexamples.py` exit 0;
  `PairObstruction.lean` compiled `lake env lean` exit 0, zero `sorry`,
  axioms = [propext, Classical.choice, Quot.sound].
- Model/action ID: PD20's per-body ansatz (isolated static pair), audited only.

## Exact claim and scope

For positive masses: m1 sqrt(m2) = m2 sqrt(m1) iff m1 = m2 (Lean, all positive
reals).  Under PD20's per-body law the opposing force magnitudes are F_i =
m_i sqrt(a0 G m_j)/r; translation invariance (Newton III) requires equality,
so the per-body ansatz conserves momentum only for equal masses.  Scope: the
isolated static per-body ansatz only; it does not cover actions with field
momentum (R07's route).

## First discriminator and result

**3/3 PASS + Lean.**  C1: (m1, m2) = (1, 4), sqrt(a0 G)/r = 1 gives F1 = 2,
F2 = 4 — a factor-of-2 momentum violation.  C2: on an extensive grid (9
diagonal, 30 off-diagonal pairs) the balance holds exactly on the diagonal
only.  C3: the test-particle limit is the single consistent limit — both
forces vanish as m2 -> 0.  Lean T1 (`pair_obstruction`) is the certificate
for all positive reals; T2 the counterexample; T4 the limit proposition.

## Evidence

- `mass_ratio_counterexamples.py` → exit 0, results JSON (full grid),
  `premise_scope.md`.
- `PairObstruction.lean` → exit 0; #print axioms = standard three.

## Independent check

The Lean proof is machine-checked and independent of the numeric scan; the two
agree (grid: no off-diagonal balance; theorem: equality only on the diagonal).
Boundary rows of the gradient-free derivation are not an issue here (exact
algebra).

## Novelty and physical interpretation

PD20's "derived" sqrt(2) two-body factor rests on the per-body premise that
each comparable mass follows the other's isolated test-body law — precisely the
premise that violates momentum conservation for unequal masses.  PD20/PD21
retain their status as conditional algebra (the equal-mass special case is
legitimate); their unequal-mass content cannot be imported into an action-based
two-body force.  Nearest prior: the followup work order's G1 packet (this
obstruction was predicted there); it is now locked.

## Decision and next action

proved.  Route the actual two-body force to R07 (action translation identity /
stress-flux integral), with this file as the regression control.  Add the
mass-ratio control to R19's negative-control suite.  Dependent: R07, G1, G2,
R09.