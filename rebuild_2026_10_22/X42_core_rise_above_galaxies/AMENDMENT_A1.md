# X42 AMENDMENT A1 (reported-only additions; committed before any graded number of this lane)

Timing disclosed: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md were committed in 4a13086d02. Step 0 (`x42_step0.py`, a rerun
of X40b) had run before this amendment; it produces only X40b's own numbers. No H1, H2 or variant number had been computed.
The amendment comes from the coordinator, after the peer lane `X41_collapse_floor_sigma` (0ea05957ee / e9c1b9abe4) landed.
Verdict classes, graded lines, H1, H2, checks and MUTATE are UNCHANGED.

## A1.1 H1-EPS variant (reported only, never a verdict)

- s = max(1, (M/M_x)^{α_EPS}), with α_EPS = log₁₀[Σ_coll(10¹⁵)/Σ_coll(10¹³)] / 2 read from the committed
  `X41_collapse_floor_sigma/x41_collapse_floor_results.json` (`sigma_coll_table`, first entry of each row = Σ_coll in
  M☉ pc⁻²). Read at run time, not refit.
- M_x calibrated exactly as H1 (cluster MID terciles only, h 0.672, per footing). Graded on every line as H1, with SPARC and
  groups out of sample; its groups prediction is reported beside H1's.
- If α_EPS lies on the α-free profile, its Δχ²_cal is reported.

## A1.2 Implied core-concentration factor (reported only)

For H1 and H1-EPS, the calibrated Σ_ss(M) divided by the peer's Σ_coll(M) (EPS, same table, log-log interpolated), at
M = 10¹³, 10¹⁴, 10¹⁵ M☉ and at the median cluster M_fair (h 0.672), per footing. The peer's own "eta_needed" (11–23×) is
quoted beside it from its JSON. Disclosed: the table is footing-independent in the peer's JSON and the background is the
peer's; Σ_ss is the calibrated (data-tuned) amplitude, so this factor is a diagnostic of what a collapse-to-core relation
must supply, never a derivation.
