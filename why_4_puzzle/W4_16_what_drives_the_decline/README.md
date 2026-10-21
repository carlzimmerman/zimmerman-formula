# W4-16: what drives the outward a₀ decline inside galaxies? UNRESOLVED (with two disclosed flaws in my own criteria)

**Bottom line.** None of the declared mechanism signatures is met at p < 0.01 across 129 SPARC galaxies. Three findings are
still informative:
- **The full-point decline depends strongly on stellar M/L.** The median slope d log a₀/d log g_bar is +0.29 at Υ_d 0.3, +0.12
  at 0.5 and −0.07 at 0.8, so it disappears near Υ_d ≈ 0.7. The slope over all points is driven by the inner, star-dominated
  points.
- **Gas-dominated points alone do not decline.** Their median slope is −0.38 ± 0.21 (17 galaxies with at least 5 gas points),
  if anything rising outward.
- **Nothing else tracks it.** Distance gives ρ +0.17 (p 0.048, opposite to the beam-smearing expectation, not significant after
  Bonferroni), inclination −0.14 (p 0.13), quality p 0.37, and V_flat +0.09 (p 0.35).

Put together with W4-12 and W4-14, the outward decline in the full-point slope is mostly a **stellar-mass normalisation effect
at the inner, star-dominated points**. A heavier stellar M/L (Υ_d ≈ 0.7–0.8) removes it in this statistic. The within-galaxy
gas/star **gap** (Δ_g) is a different statistic and still shows −0.22 dex at Υ_d 0.8 in p64's 11 galaxies. The two do not yet
tell one story, so the frozen verdict is **UNRESOLVED**. **κ = ½ is FITTED.** Not theory closed.

## Two flaws in my own frozen criteria, disclosed

1. **The D1 signature had the wrong sign.** I declared that pressure support predicts ρ(s, log V_flat) < 0. The post-hoc check
   (`w4_16_posthoc_power.py` / `.out`, no verdict weight) shows that planted pressure support (V'² = V² − 2σ² beyond R_disk)
   pushes ρ **positive**: σ 0 → +0.09, 10 → +0.10, 20 → +0.22 (p 0.02), 30 → +0.22 (p 0.03). The validity cut and the lever
   reshape which outer points survive. The data (+0.09) are consistent with little or no pressure support, but the test is weak.
2. **The frozen M1 control failed** (`w4_16_MUTATE.out`, exit 2). The σ = 10 km/s plant did not produce the (mis-signed)
   signature. This is the same root cause as flaw 1.

- **M2 (planted radial M/L gradient) works:** the median s moved from +0.12 to −0.22 while the median s_gas stayed within 1σ
  (−0.45 vs −0.38). D2's discriminator works.
- **The D2 signature itself was not met in the data:** s is not above 2σ, and s_gas is not ≈ 0.
- Under M2 a spurious inclination correlation appeared ("ATTRIBUTED to D4"), so treat the D4 test with caution.

## Files

`FROZEN_CRITERIA.md` (e8e80f10f), `w4_16.py` (numpy/scipy, 1 s, 126 MB), `w4_16.out` / `_results.json`, `w4_16_MUTATE.out` /
`_results_MUTATE.json` (exit 2: M1 failed), `w4_16_posthoc_power.py` / `.out` (no verdict weight).

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_16_what_drives_the_decline/w4_16.py > why_4_puzzle/W4_16_what_drives_the_decline/w4_16.out
