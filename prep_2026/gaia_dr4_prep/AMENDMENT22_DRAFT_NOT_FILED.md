### 🚨 AMENDMENT 22 — 2026-10-15, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.

**THIS AMENDMENT DEFINES THE ERROR σ AND THE SCOPE OF THE CFG800 DR4 DECISION RULE, WHICH LEFT BOTH UNDEFINED. IT CHANGES NO CUT, THRESHOLD, ESTIMATOR SETTING, GRID, σ_tot, DECISION ROW, SEED OR ARM OF THIS DOCUMENT.**
**κ = ½ FITTED, NOT DERIVED. THE COLD MASS IS STILL REQUIRED; NO DARK-MATTER PARTICLE IS ADDED.**

**(a) What CFG800 registered.** `campaign_fresh_gravity/CFG800_wb_2026_scoring/FROZEN_CRITERIA.md` (aa71ca510, 2026-10-15) freezes a decision rule on a second statistic R: the median ṽ at r_p/r_M > 1 (s ≤ 50 kAU) over the Newtonian-regime normalization, with the Cookson quality checklist and a calibrated triple fraction. The rule: "FRAMEWORK KILLED if R − 1 ≥ 0.01 at ≥ 3σ; CONSISTENT if |R − 1| < 0.01 at 2σ; UNDECIDED otherwise." It defines no σ and does not say what "FRAMEWORK" means.

**(b) The gap.** This document's error model (§1.5) is σ_tot = 0.028 at the frozen N = 30,000, of which σ_sys = 0.02 is irreducible (Amendment 7: 3σ is unreachable at any N). At that σ the CFG800 rule reads: KILLED needs R − 1 ≥ 3σ = 0.084, so the "0.01" does nothing; CONSISTENT cannot be reached, because a 2σ interval (±0.056) is wider than ±0.01. The same rule at a statistical-only σ ≲ 0.005 would read differently. Without a registered σ the outcome would depend on a choice made after DR4.

**(c) What is registered here.**
1. **σ for R** is the larger of (i) σ_tot of this document (§1.5: σ_fit scaling as √(30000/N), in quadrature with σ_sys = 0.02, irreducible) and (ii) R's own calibrated statistical error from the same selection and bootstrap. Call it σ_R.
2. **KILLED** requires both R − 1 ≥ 0.01 and R − 1 ≥ 3σ_R. At σ_R = σ_tot = 0.028 this is R ≥ 1.084.
3. **CONSISTENT** requires both |R − 1| < 0.01 and 2σ_R ≤ 0.01, so that the 2σ interval lies inside ±0.01. If σ_R > 0.005 the CONSISTENT class is **unavailable** and the result is UNDECIDED (or KILLED under 2). No other reading of "at 2σ" may be used after DR4.
4. **Scope.** "FRAMEWORK KILLED" in CFG800 means **the stiffness construction of CFG740 is killed** (CFG740's own falsifier is γ_v ≥ 1.01 at s ≤ 50 kAU). Arm A, Arm B, Arm C and the settling model are scored by their own rows in this document and are not moved by R. R and γ̂ are two statistics: reported side by side with their distance to every arm, never pooled and never averaged (Amendment 7(c)).
5. **"Standard MOND excluded"** (CFG800's consequence of CONSISTENT) is instead scored by the z-rule against the registered MOND benchmark of the statistic in question (for γ̂, the benchmark registered in §1; for R, the range 1.15–1.20 that CFG800 cites), with σ_tot. It is available whether or not CONSISTENT is reached.

**(d) Stated against interest.**
- Under (c) the CFG800 rule is hard to satisfy in either direction. At σ_tot, KILLED needs R ≥ 1.084 and CONSISTENT cannot occur, so DR4 will most probably return UNDECIDED on R. That is the intended reading of an irreducible σ_sys, not a rescue.
- A boost between 1.01 and 1.084 would, under (c)(4), kill CFG740 only if it is significant at 3σ_R, and in any case leave Arm C alive by its own rows (alive until 1.084 at σ_tot).
- This amendment was filed after CFG800's freeze the same day, before DR4. The choices in (c)(1) and (c)(4) were made by the filing session under the owner's instruction to file the amendment, taking the smallest new assumption (this document's existing error model; the narrowest reading of "framework"). They cannot be changed after filing except by a further dated amendment.

**(e) Unchanged.** Arms A, B and C and their rows; the settling model's registration (Amendment 21); the estimator and its grid; the 16-row cut table; the error model and σ_tot; the strictness ladder; the frozen N = 30,000; both a₀ footings; the κ window and the no-verdict edge 1.23; the sealed CFG740 files (SHA-256 5336fd99…a944a); the CFG800 criteria text itself; Amendments 1–21; the seeds. No new cut may be added after DR4.

**Provenance.** `campaign_fresh_gravity/DR4_OUTCOME_MAP_2026-10-15.md` (0aec66b39) found the gap; `campaign_fresh_gravity/CFG800_wb_2026_scoring/FROZEN_CRITERIA.md` (aa71ca510); `campaign_fresh_gravity/CFG740_sealed_wb_slope2/` (criteria c4f88c6ee, sealed 2026-10-13). Filed on the owner's explicit instruction, 2026-10-15.
