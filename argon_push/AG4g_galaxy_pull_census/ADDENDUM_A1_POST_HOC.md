# AG4g ADDENDUM A1 (POST HOC, 2026-10-20): a mock-calibrated null for stage 2

Committed alone, after the frozen run and before any A1 number.

## What failed, and why a new null is needed
- In the frozen run, stage 1 = EXCESS: 13 of 170 large pulls against at most 1 in 200 law-true mocks.
- Stage 2 flagged Q (signed, ρ −0.281, Holm 0.0066) and Inc (signed, ρ −0.233, Holm 0.040).
- **K3 FAILED: 46 of 50 law-true mocks produced at least one Holm "lead".** The permutation null assumes that pulls are
  exchangeable across galaxies when the law is true. They are not: the MAP-Υ estimator's bias depends on each galaxy's errors
  and acceleration regime, which correlate with the properties.
- **Stage 2 is VOID as frozen.** Its two leads are not reported as leads.
- MUTATE bit: an injected Hubble-type dependence was flagged (ρ +0.605, Holm 0.0022).

## A1 null (post hoc, disclosed)
- **Reference distribution:** for each of the 22 tests, the Spearman ρ between each law-true mock's pulls and the real
  properties, over the 200 stage-1 mocks (seeds 1–200, n=1, canonical, the fit's own error model).
- **Empirical p:** two-sided, p = (1 + #{mocks with |ρ_mock − m| ≥ |ρ_data − m|})/201, where m is the median mock ρ.
- **Correction:** Holm across the 22 tests, α = 0.05. An **A1 LEAD** is a test with Holm-adjusted p < 0.05.
- **Resolution floor:** 200 mocks give a minimum p of 1/201. Holm's first step needs p < 0.05/22 = 0.0023, which is reachable
  only when the data lie outside every mock.

## A1 control (must pass, or the A1 reading is void too)
- **K3-A1:** on 50 fresh law-true mocks (seeds 1001–1050), the family-wise rate of A1 leads under this null must be ≤ 0.10.

## What A1 does not change
- Stage 1, its reading and the frozen K1, K2, K3 and MUTATE results all stay as recorded.
- A1 runs in a separate script, `ag4g_a1.py` → `ag4g_a1.out` and `ag4g_a1_results.json`. `ag4g.py` is not edited.
