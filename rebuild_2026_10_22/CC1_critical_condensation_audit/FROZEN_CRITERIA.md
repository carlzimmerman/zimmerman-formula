# CC1_critical_condensation_audit: FROZEN CRITERIA (committed alone, before this lane's stack is run)

**Question.** An outside specification proposes that a cold dark energy halo exists only where eta Sigma_coll(M) >= Sigma_a0, the law applying below, and calls the threshold parameter-free. Does the threshold survive the record's own eta(M) tables, is it new against CSM1, and does the kSZ stop rule hold on a type-corrected bin?

Disclosed before running: the spec's arithmetic, the record's eta tables, CSM1, HO2 and GH9's whole-sample A values have been read. Only the stack below is unseen. Not blind.

**Part A, threshold (arithmetic on committed tables, both footings, never pooled).** Solve eta Sigma_coll = Sigma_a0 for (a) each constant eta in the spec, (b) mass-dependent eta from ARGON_BRIEF_2026-10-30 table 3a.
- **BRACKET HOLDS:** a crossing in (1e12, 1e13) for every row of (b), canonical.
- **BRACKET FAILS:** eta(1e12) Sigma_coll(1e12) >= Sigma_a0 in any row of (b) that passes the grader.

**Part B, Tier 2 direction.** The estimator is -sum(w T u)/sum(w u^2). Monte Carlo: tau = 1, v_rec = alpha v_true + noise, rms set to 264 (mock) and 194 (data). Report the true correction factor to A for (i) same alpha, less noise, (ii) pure rescale. The spec's x264/194 holds only if the factor is >= 1 in the case considered.

**Part C, stack.** GH8's lenses, CAPs, velocities, weights, R, through its run() read-only.
- Corrected mass: passive lm + 0.14, star-forming lm + 0.31 (GH9 type offsets). Bin [10.50, 11.00].
- **Limit fixed in advance:** the cached CAPs stop at CIGALE lm 10.6, so only the upper part of the bin exists here: passive lm 10.60-10.86, star-forming 10.60-10.69. The complete bin needs new map CAPs at 6-7 GB, not run while X48 zooms are live.
- Model: GH9 build() with D = -0.14 / -0.31 by lens type. Error e = larger of shuffle and jackknife.
- **Tiers as specified:** T1 raw; T2 x264/194; T3 divided by control 0.58 +- 0.14. Report A(1), A(1.8), A(3), 95 % limits, all three R.
- **Stop rule class:** EXTENDED GAS BELOW NEED if A(1.8) + 1.96 e < 1 on T1 and T2. Otherwise NOT BELOW.
- **Extent lock:** report A(1) + 1.96 e. If it is also < 1, the shortfall does not separate k = 1 from k = 1.8, and the class cannot support "k = 1 is in no tension".

**Checks.** K1 GH9's D1 A(1.8) reproduced at 1e-3 through the same harness on the whole sample. K2 v flip gives exact sign change. NOT DECIDED if either fails.

**Limits.** No retiring of extended gas or adoption of a theory follows from Part C alone. Adoption is the owner's decision. No detection in the data (GH8 null p 0.21). GH8's marginal control, inherited beta and K2 velocity failure remain.

kappa = 1/2 FITTED; c_f EXTERNAL; core shape empirical. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
