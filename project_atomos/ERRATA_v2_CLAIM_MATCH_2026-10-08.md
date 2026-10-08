# Errata for PAPER_ATOMOS_NULL.md v2 (Zenodo DOI 10.5281/zenodo.21654272), found by claim match

> **Update (same day):** the v3 correction draft is now `PAPER_ATOMOS_NULL.md` (v2 kept as `PAPER_ATOMOS_NULL.v2.md`). After two more review rounds, `CLAIM_MATCH.py` passes on v3. Two counts below were themselves corrected: the deep-sample campaign is **1,191 distinct passes / 18,332 hits** (one resumed pass is logged twice), and `holdout_airtight` reports 23/26 with a FATAL label (§11 of v3).

On 2026-10-08, independent reviewers who did not write the paper traced every sentence containing a number (108 claims)
to the output files on disk. The coordinating session re-checked the substantive flags against those files.
`CLAIM_MATCH.py` enforces the result, and `CLAIM_MATCH_REVIEW.json` holds each verdict with the source file and its hash.
The published paper is **left unedited**. Whether to deposit a v3 is the owner's decision.

**Result: 57 MATCH, 26 CONTEXT, 12 WRONG, 6 OVERSTATES, 7 UNSUPPORTED.**

**The headline null is untouched.** At depth 10 the counts are 174,890,804 raw, 42,534,139 distinct, 82,613 hits and
0 certified. These match `results_grind/depth_10/VERDICT.json` exactly. Every per-target hit count matches. No hit
survives anywhere, including the deep samples, where every hit is FDR-DEAD.

## WRONG (12)
- §3 table: the hit counts are all right, but **5 of the 6 window ranges** match neither the half-width nor the full-width
  convention. The committed half-widths are:
  - 2.18e-8 – 1.89e-7
  - 6.75e-5 – 1.30e-4
  - 1.35e-3 – 3.07e-3
  - 7.18e-3 – 7.63e-3
  - 2.54e-2 – 3.96e-2
- §1: the relative windows span ~8.5 orders of magnitude (1.12e-10 to 3.96e-2), not "eleven".
- §1: the skeleton takes b_s = 1..6 steps at D = 10. D−4 is the maximum, not a fixed count.
- §3: "~1.2x, 81st percentile" is a_e's figure alone. The median over the 20 targets is 1.00x (47th percentile), and r_mu_e is 1.73x
  (98th). The conclusion "no penalty needed" still holds (net_worst_bits +6.71).
- §4: the deep-sample campaign ran **1,192 passes with 18,349 hits** (`SAMPLE_LEDGER.jsonl`, complete before publication),
  not "1,059 passes, ~29,000 hits". "Zero survivors" holds.
- §4: the m_p/m_e window slip is at `GATE_POWER_ANALYSIS.py:40`, not `:41`. The mechanism is that the absolute uncertainty
  was entered 1000x too small (3.2e-11 for 3.2e-8). It is not a relative uncertainty divided again by the value.
- §5: the permutation null runs over **18** targets (r_t_b dropped). Chance's mean maximum is 11.03, so "chance alone puts a skeleton
  on 10 of 19" should read "on ~11 of 18". Real max 10 vs chance max 11.0 is correct.
- §8: the a0/2c bridge lies **39.7** orders below the electron (`rg_flow_correspondence_log.json`), not ~38. That log's own
  verdict string says "~24", which also needs fixing.

## OVERSTATES (6)
- Abstract, §2 and §10: "depths 3–9 exhaustive clean nulls under the same machinery" is backed by machine output under
  `grind.py` **only for depths 6–9**.
  - Depths 3 and 5 ran on other engines (depth-5 raw is 918,528 there vs 19,136 under grind).
  - **Depth 4 has no output** (`results_exhaust_depth4/` is empty), and §4 itself says depth 4 cannot be built.
  - The D8/D9 ⊂ D10 nesting is printed by `effective_N_audit.py`, but that output was never saved.
- §3: "hits/2w flat at rho ~3e5 across five decades over all 19 targets" is measured only on the 13 targets that have hits,
  over ~2.8 decades (2.1e5–3.6e5). The 6 tight targets have 0 hits.
- §3: "13/13 reproduce exactly" is really 12. A key mismatch in `expected_count_audit.py` (`sin2_theta_W` vs
  `sin2_thetaW_MZ`) left sin² θ_W unchecked. Over the 13 swept targets the median is 124.6x (123x includes the holdout).
- §4: fixing only the 1000x error gives **34.7 bits**, not 30.1. The 30.1 comes from the code's propagated window, which is a further ~24x looser.

## UNSUPPORTED: no saved output carries the number (7)
- "9/9 unit probes" (`gate_b_germ_enforcement.py`, output never saved)
- "9 exactly-redundant pairs" and the 18/19 maximal set. `interlock_spec_sets_output.txt` T4 instead finds
  {r_b_tau, r_t_b} functionally independent and calls dropping r_t_b over-strict.
- 93.8 / 65.2 bits for the k=3 false positive (in a docstring only)
- the QED a_e-from-α figure 2.4e-9 (hard-coded prose; the computed value 2.280e-9 is for a different series)
- `score_holdout` passing a pool prediction (the only recorded call scores the literal 2/3)
- "transfer gain 1.000000", "0.0000 bits" (the only output gives 0.00, for koide only)
- span residuals 1.686e-10 / 3.300e-10 and the exponents ±1.0000

Most UNSUPPORTED items are probably right numbers whose script output was never saved. Re-running those scripts with
saved output would settle them. Note also that several outputs the paper leans on (e.g.
`audit_interlock/ceiling_math_audit_output.txt`, `interlock_spec_*_output.txt`) are not in git anywhere. The copy committed in
zimmerman-formula (cfb6007f) has the scripts and some JSONs, but not these files.
