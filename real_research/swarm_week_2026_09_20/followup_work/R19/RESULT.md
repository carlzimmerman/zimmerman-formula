# R19 — Make the load-bearing claims fail when their premise is wrong (result)

- Owner: Hermes (this lane); independent reviewer: none yet (self-review recorded)
- Execution state / claim state: completed / finite_evidence (negative controls pass)
- Baseline: followup work order `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`; HEAD
  `52a294431` + my followup dispatch `c816e5fa3`.  Inputs read/ran at HEAD:
  `real_research/clock_2026/L312_law_implications.py` (rerun: 4/4 PASS),
  `real_research/reviews/bhstar_r1_wind_kinematics.py` (rerun: 6/6 PASS),
  `deepseek_push/lean/PD21_law_of_nature.lean`, `kappa_unit_response` README.
  `python3 negative_controls.py` exit 0.
- Model/action ID: the release-candidate claims only (L311 V2, unit response,
  PD20 two-body, bhstar CAK interval).

## Exact claim and scope

Four controls, each the independently computed predicate for a release-candidate
claim: (NC1) L311 V2's r^{1/8} rise gate is a real predicate on the mass law —
a known log shell must be rejected; (NC2) the unit response mu'(0) = 2 must
move with the channel premise; (NC3) PD20's balance must break off the
diagonal; (NC4) the CAK interval membership test must reject outside radii.

## First discriminator and result

**4/4 PASS.**
- NC1: the log shell through L311's own slope estimator (300–600 kpc) gives
  0.0169 — the gate [0.06, 0.14] rejects it.  The estimator is a genuine
  predicate; combined with R02 it confirms 1/8 is not an output of the log law.
- NC2: mu'(0+) = 2λ: λ = 1.2 gives 2.4 and shifts the deep-MOND scale 20%; the
  selector responds to the assumed unit channel (the premise kappa_unit_response
  itself declares the equality an assumption).
- NC3: balance holds at (1,1), breaks at (1,1.5) and (1,4) — regresses R06.
- NC4: r* = 100 au and r_in = 2e3 au both fail membership in the CAK band
  [490, 650] au; the record's one-sided chain check is not a test (documented).

## Evidence

- `negative_controls.py` → exit 0, 4/4 PASS; `negative_controls_results.json`.
- Fresh reruns of the two source scripts (L312, bhstar_r1) logged above.

## Independent check

Each control is constructed from the claim's own published gate/constant
(L311's band, kappa_unit_response's formula, R06's theorem in Lean, the CAK
band as documented), not from a reimplementation of the claim.

## Novelty and physical interpretation

Negative-control map for the release candidate: L311 V2's rise prediction,
PD20's unequal-mass amplitude, and the bhstar interval reading are all
predicates that fail when their premise changes — as a gate must.  The unit
response's λ = 1 remains a declared postulate (unchanged); the controls only
certify that its gates can fail.

## Decision and next action

finite_evidence (controls pass; no claim changed by this lane alone —
R01/R02/R06 already carry the substantive corrections).  Deliverable
claim_check_map.json attaches each control to its claim.  Q2/Q4: attach these
logs as the negative-control appendix; R20 uses NC1 as the regression gate for
any future sqrt-law claim.