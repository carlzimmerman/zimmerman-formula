# CFG914 AMENDMENT A1 (POST HOC): a fit consistent with the sector test

**Status: post hoc.** Written after (1) the frozen primary run (criteria 6ec526287) had been run and seen, with NO COMMON
ORDERING in all four graded cases (both footings, ρ̄_law and ρ̄_b), and (2) the frozen MUTATE-INJECT FAILED (3 of 4 cases: PARTIAL
×3 with SPARC small/large flagged; the 4th was COMMON THRESHOLD but missed the ρ* recovery by 1.6 dex). Committed alone, before
the amended method is run on the real data. The frozen results and the frozen MUTATE failure stay in the record unchanged.

## Why
A scratch diagnostic (not committed; disclosed here) of the failed injection found an inconsistency in the frozen method:
- the **fit** treats the systematic floor as independent per bin (weights 1/(SE² + σ_floor²));
- the **sector test** treats it as one common offset per sector (σ_floor² added to every element of the sector covariance).

With a true common threshold injected, each sector draws its own offset (e.g. SPARC small +0.22, SPARC large −0.21 in the seed-914
draw). The frozen fit then put the threshold one bin too low (f > 0 on a SPARC-small bin whose truth is 0) and pulled the high
level to 0.58 instead of 0.70. The precise SPARC bins (SE ≈ 0.03) cannot absorb a pattern that is not a constant offset, so they
"violated" at z 5–13.

Over 100 seeded injections (same recipe as the frozen MUTATE-INJECT: f_inj = 0.7 H(log ρ − median), draws from each sector's
covariance incl. the correlated floor), the frozen classifier returned COMMON THRESHOLD in only **21 / 41 / 17 / 43 %**
(canonical ρ̄_law / canonical ρ̄_b / alt ρ̄_law / alt ρ̄_b), and NO COMMON ORDERING in 14–23 %. A frozen NO COMMON ORDERING
on the real data is therefore weak evidence by itself.

## A1 method (everything not listed is unchanged)
- **Fit with per-sector offsets.** The common function f (zero below ρ*, isotonic non-decreasing ≥ 0 above) is fitted jointly
  with one offset δ_s per sector, with prior δ_s ~ N(0, σ_floor²), the same floor the test uses. For each threshold candidate:
  alternate (i) the isotonic fit of E − δ_s with statistical diagonal weights 1/SE² and (ii) the GLS offset
  δ_s = 1ᵀC_s⁻¹(E_s − f_s) / (1ᵀC_s⁻¹1 + 1/σ_floor²), until max |Δδ| < 1e-10 (≤ 200 iterations). Objective
  Σ (E − δ − f)²/SE² + Σ δ_s²/σ_floor²; the candidate with the minimum objective is chosen (ties → lower ρ*).
- ρ*_eff, the validity rule, and the ≥ 3σ excess rule are unchanged; the excess is computed on the offset-corrected E with the
  frozen weights 1/(SE² + σ_floor²).
- **The sector test is unchanged:** residual E_s − f_s (no δ), covariance C_s + σ_floor² J. That marginalises the same offset
  with the same prior, so fit and test now agree. Greedy subset and class rules are unchanged.
- Also reported: ρ*_half, the lowest bin density where f ≥ ½ max f (a steadier location estimate; not used in any class).

## A1 controls (reported; expectations stated, but the scratch diagnostic already showed them)
- **Power (MUTATE-INJECT, A1):** the same 100 seeded injections per footing × variable (one generator, seed 914). The scratch
  diagnostic already gave COMMON THRESHOLD in 83 / 78 / 79 / 77 %. Seven sectors each tested at z > 2 give a nominal
  1 − 0.977⁷ ≈ 85 % if the tests were exact and independent. So ≥ 70 % is stated as the expectation; it was seen before this
  file was written, so it is not a test. ρ* recovery within 0.5 dex is reported. The frozen seed-914 single injection is
  re-scored under A1.
- **False-positive check (new, post hoc):** 100 seeded injections in which each sector gets its OWN threshold, log ρ*_s =
  median + U(−1.5, +1.5) dex (seed 9141). The fraction returning COMMON THRESHOLD is reported, i.e. how often unrelated per-sector
  thresholds pass as one common threshold.
- The frozen K-tests and MUTATE-SHUFFLE are unaffected (they do not use the fit).

## Reporting
- The **frozen class** (as run) and the **A1 class** are both reported for the primary and V1 densities on both footings, plus
  A1 for the inverted mirror and the variants R1–R8.
- The ledger headline will state both. If they agree, the reading is that class, with a classifier of measured power. If they
  differ, the A1 class is labelled post hoc and the frozen class is not overwritten.
