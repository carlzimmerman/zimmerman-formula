# CFG799 ADDENDUM C RESULT: the alternate-footing line at 595.463 GHz (2026-10-19)

Criteria: `FROZEN_CRITERIA.md` (committed before any download or statistic; one path correction recorded there). Data: 46 HIFI band-1b
observations (4.61 h), all downloaded and reduced; 35 pass the Level-1 anchor, 31 contribute spectra (3.13 h, 197 spectra).
The framework predicts NO line. κ = ½ is fitted. Not "theory closed".

## Frozen run: INCONCLUSIVE (numbers from `cfg799_results.json`)
- **C2 null offsets FAIL.** z = +4.51, +6.11, +2.46, +0.38, −0.85, −3.14 at −20, −10, −5, +5, +10, +20 MHz; Σz² = 74.5, p ≈ 0.
- **ν_2 = 595.500 GHz: z = −5.96** (a = −41.5 ± 7.0 mK), REF-only z −5.44, Level-1 z −0.38. A negative total-power stack cannot
  be the hypothesised emission line, so by the frozen rule it is an artefact at the target.
- ν_t = 595.463 GHz: a = +12.6 ± 6.9 mK (z +1.83); scan maximum |z| = 6.97 at −11 MHz, 27 of 161 steps beyond 5σ.
- C1, C3 and C4 pass (C1 injection recovered, r = 1.000; IF-shuffle z +0.42; anchor 35/46).
- **MUTATE did not bite, by the frozen rule.** The injected 69 mK line is recovered (z +11.8, r = 1.000), but the class gate returns
  INCONCLUSIVE because C2 fails, and the frozen text declares the pipeline blind in that case. This is the recorded outcome.
- **Converter-window tier (addendum A): EXCLUDED, 31/31 observations at S = 10, 50 and 1000.** The thresholds are
  2750 K, 550 K and 27.5 K (DSB peak). The largest structure in any variant below is about 0.13 K, so this does not depend on
  the baseline. It is a separate single-spectrum tier and does not use the stacked controls, but it rests on the same
  calibration.
- No stacked limit is claimed as a number of record.

## Exploratory decomposition (`cfg799_C_explore.py`, declared list committed before the run; sets no class)
- **Broad structure dominates the total power.** Away from ν_t and ν_2 the z over the ±40 MHz scan has std 3.63 (REF-only 3.65;
  Level-1 1.11, calibrated). 20 of 124 far steps reach |z| ≥ 5 in total power, none in Level-1. The z grows with line width
  (ν_t +1.8 at 1.15 MHz to +4.3 at 16 MHz; ν_2 −6.0 to −11.0), so it is baseline structure, not a narrow line.
- **At 541.7 the H and V structure cancelled; here it adds.** H-only z(δ) has std 2.4, V-only 3.3, and corr(H, V) is **+0.61**
  (±60 MHz) and +0.71 (±40 MHz), against −0.85 and −0.91 at 541.7. The combined stack spans −6.4 to +7.0 over ±40 MHz. The
  clean combined null at 541.7 was helped by an anticorrelation that does not repeat here.
- **ν_2 is a negative feature in both polarisations and every subset.** H −42.1 mK (z −3.9), V −41.1 mK (z −4.5); stronger
  in LSB spectra (−53.1 ± 7.7 mK, z −6.9) than USB (−7.1 ± 14.2 mK; difference z +2.85); early −35 and late −53 mK; line-rich
  −36 and other −46 mK. Leave-one-out z runs from −6.36 to −5.25, so no single observation drives it.
- **ν_t is not a fixed-RF line.** USB −27.0 ± 11.8 mK vs LSB +25.8 ± 8.3 mK (difference z −3.67), and H −8.8 vs V +27.8 mK
  (difference z −2.64). A line at fixed RF should agree between sidebands.
- **Baseline variants** (a sensitivity table, no variant chosen; ν_t ε95 at S = 50, whole table 1.7e-11 to 5.1e-11):

  | baseline | ν_t a ± σ | ν_2 a ± σ | far-step std | ε95 (S = 50) |
  |---|---|---|---|---|
  | deg 2, ±50 | +13.0 ± 7.1 | −44.3 ± 6.9 | 3.79 | 2.67e-11 |
  | **deg 3, ±50 (frozen)** | +12.6 ± 6.9 | −41.5 ± 7.0 | 3.64 | 2.64e-11 |
  | deg 4, ±50 | −1.3 ± 6.1 | −9.8 ± 6.5 | **1.00** | 1.71e-11 |
  | deg 5, ±50 | −1.2 ± 6.1 | −9.3 ± 6.5 | **1.03** | 1.71e-11 |
  | deg 2/3, ±100 | +66.7 / +67.8 ± 12.5 | −133.9 / −132.6 ± 11.7 | 8.1 | 5.0e-11 / 5.1e-11 |
  | deg 4/5, ±100 | +39.9 / +37.6 ± 9.1 | −84.3 / −80.9 ± 8.5 | 6.5 / 6.2 | 4.0e-11 / 3.9e-11 |

  Amplitudes in mK. Only degree 4 and 5 over ±50 MHz give a calibrated empirical null (std 1.0), with nothing at either
  frequency (ν_t z −0.2, ν_2 z −1.5). Choosing them is a **post-hoc** decision made after the frozen estimator failed C2, so
  they are not the number of record. Scaling the frozen formal σ by the empirical std 3.63 gives ε95 = 3.96e-11 (S = 50).

## Reading
- **The converter window for the alternate footing is closed** at every coupling tested, by the single-spectrum tier, and the
  quoted range of the ν_t limit is **ε95 = 1.7e-11 to 5.1e-11 at S = 50** (converter window closed by ×80 to ×235). The kill line
  1e-12 is missed by ×17 to ×51 and is **not** tested here, as declared in advance.
- The frozen stacked search could not classify the data: broad common-mode structure and a negative artefact at ν_2 fail C2.
  There is no sign of a narrow line at either frequency in any variant, but the only variant with a calibrated null was chosen
  after the fact.
- A cleaner test of 595.463 GHz needs data that average the baseline down (many LO settings per target, both polarisations) or a
  pre-declared higher-order baseline on new data, not more of this archive: the 6 excluded-mode observations hold 1.16 h.
