# X70_soft_floor_x0

**Question.** The external model's final-mile spec, Task 3 (relayed by the owner, 10-29), proposed softening X43's floor
by the peak baryonic acceleration:

Σ_core = max(Σ_M F(X₀), η Σ_coll), with F = 4X₀/√(1 + 16X₀²) and X₀ = max g_bar/a₀.

The claim was that this rescues low-X₀ dwarfs such as IC 1613 while leaving the "~87 % of SPARC on the hard floor"
unchanged. Criteria were frozen first (cffa3cc8bd).

## Verdict: SOFT FLOOR FAILS, both footings; IC 1613 NOT RESCUED

| | canonical | alt |
|---|---|---|
| SPARC X₀ at Υ = 0.5 / 0.7: median, p10, p90 | 0.29, 0.06, 10.8 | 0.24, 0.05, 8.9 |
| G1: share with F < 0.794 (a shift of more than 0.1 dex); must be < 15 % | **53 %** (93/175) FAIL | **55 %** (96/175) FAIL |
| G2: SPARC rms, bg A / B; must be ≤ 0.08 | hard 0.0782 / 0.0782 → soft **0.0954 / 0.0952** FAIL | 0.0729 / 0.0728 → **0.0895 / 0.0892** FAIL |
| SPARC line (Υ median) | FAIL (1.18) | FAIL (1.09) |
| shifted galaxies whose own rms improves | 28 / 93; median change +0.056 dex | 37 / 96; median change +0.051 dex |
| k = 3.93 (the arithmetic value of the "4") | 0.0958 / 0.0957 | 0.0900 / 0.0897 |

**The premise is wrong.** The median SPARC galaxy has a peak g_bar of only about 0.3 a₀. So F(X₀) bites on more than half
the sample, not on a 10–15 % tail. Removing halo there costs more than it gains: the fits rise to Υ ≈ 1.1–1.2 to make up
the missing pull, and the worst galaxies get worse by 0.4–0.5 dex (UGC06667, F583-1, UGC07608, UGC00731, F565-V2).

**IC 1613** (IN1's HI estimator at R_max = 2.71 kpc, route E halo, M200 = 10^9.33):

| canonical, E_HI | i = 32° | i = 36° |
|---|---|---|
| hard floor | −0.279 | −0.369 |
| soft, X₀ lower bound 0.018 (F 0.07) | +0.316 | +0.226 |
| soft, X₀ exp-disc 0.051 (F 0.20) | +0.033 | −0.057 |

- IC 1613 is graded "rescued" only if |E| ≤ 0.15 on both X₀ brackets. With the lower-bound X₀ it overshoots the other way,
  so it is NOT RESCUED.
- With the exponential-disc X₀ it would sit inside the band, but that X₀ is an estimate (R_d = R_h/1.678, gas and
  stars together), not a measured profile.
- Its answer swings by 0.3 dex across the X₀ bracket. The test cannot decide IC 1613 without a measured g_bar profile.
- The alt footing gives the same pattern.

**Reading.** A floor keyed to peak baryonic acceleration moves the bulk of SPARC, not its tail, and a global test does
not allow it. F is a chosen form, so a sharper switch (MUTATE k = 8) would just be a knob scan. The record's no-knob-scan
rule applies.

κ = ½ FITTED; c_f = 4 EXTERNAL; not theory closed.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x70_soft_floor.py`, `.out` / `_results.json` (with per-galaxy X₀ and the shifted list),
`_MUTATE` versions (k = 8, SPARC rms change 0.015: sensitive), `run1.log`, `run_mutate.log`. Checks 3/3:
- K0: F ≡ 1 reproduces X43's SPARC rms exactly, both footings and backgrounds;
- K1: F algebra, and the Freeman disc vs Hankel quadrature;
- K2: RSS 0.7 GB.

**Pre-result fixes, both caught by the checks:**
- the hard-floor path dropped X43's η Σ_coll branch (K0 failed: it gave X38's 0.0795);
- K1's quadrature had a stray R_d in its prefactor.

Neither touched the graded soft-floor rule. The first run's G1 / G2 / IC 1613 lines are identical to the final ones.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x70_soft_floor.py            # ~60 s, exit 0
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x70_soft_floor.py --mutate   # k = 8
