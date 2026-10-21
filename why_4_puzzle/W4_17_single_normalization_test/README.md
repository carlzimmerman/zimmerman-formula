# W4-17: is the within-galaxy a₀ residual a single stellar-M/L normalisation error? Population yes; p64's 11 mixed galaxies no

**Bottom line.** This lane resolves the apparent clash between p64 (the gap persists at Υ_d 0.8) and W4-16 (the slope vanishes
near Υ_d 0.7). The two results describe different galaxies:

- **The SPARC population (130 galaxies) has no anomaly at population-synthesis M/L.** The full-point slope s and the radial
  split Δ_r (outer half minus inner half) both vanish at **Υ* = 0.48 ± 0.08** and **0.59 ± 0.08**. A single normalisation near
  Υ_d ≈ 0.5 describes them. The "outward decline" I reported for SPARC in general (W4-14/15/16) came from W4-16's error
  weighting and the fixed Υ_d 0.5, not from a robust population effect.
- **The persistent gap belongs to p64's 11 mixed galaxies,** those with both strong gas- and star-dominated regions. In them
  Δ_g and Δ_r do not cross zero anywhere in Υ_d 0.3–1.4: only 150/500 and 177/500 bootstrap resamples cross at all. s crosses
  at 0.51 ± 0.32. **The frozen verdict on S11 is NOT A SINGLE NORMALISATION (gradient-like).** For these systems a constant M/L
  cannot remove the gap; it takes something position-dependent within them (an inner-heavy M/L gradient, outer gas overcounted,
  or outskirts kinematics).

**What it means for the 4.** κ ≈ ½ at Υ_d ≈ 0.5 is internally consistent for the rotation-curve population. The residual
structure is confined to a small class of mixed-dominance galaxies. **κ = ½ is FITTED.** Not theory closed.

## Calibration (pre-freeze, synthetic; committed with the criteria)

| world | Υ* for Δ_g / s / Δ_r on S11 | verdict |
|---|---|---|
| A, exact law at true Υ 0.5 | 0.500 / 0.500 / 0.500 | SINGLE NORMALISATION |
| B, planted inner-heavy radial M/L | 1.063 / 1.194 / 0.967 (s vs Δ_r disagree) | NOT A SINGLE NORMALISATION |

**MUTATE** runs both worlds through the identical pipeline with bootstrap (`w4_17_MUTATE.out`): A gives SINGLE at 0.5 and B gives
NOT SINGLE, as calibrated (exit 1 by design). The signature directions were fixed **before** the freeze, which is the lesson from
W4-14 to W4-16.

## Files

`FROZEN_CRITERIA.md` + `w4_17_prefreeze_calibration.py` / `.out` (b0e8bee92), `w4_17.py` (numpy, 1.2 s, 98 MB), `w4_17.out` /
`_results.json`, `w4_17_MUTATE.out` / `_results_MUTATE.json`.

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_17_single_normalization_test/w4_17.py > why_4_puzzle/W4_17_single_normalization_test/w4_17.out
