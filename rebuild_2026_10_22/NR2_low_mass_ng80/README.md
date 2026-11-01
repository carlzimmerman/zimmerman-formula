# NR2_low_mass_ng80: ALL-NG80 PASSES [NOISE-LIMITED]. Version N stays on SPARC's line with all three anchors at ng 80, Υ 0.75 / 0.76, but seed noise alone takes it off, on the high side

Criteria: `FROZEN_CRITERIA.md` (26b71969d4). `run_nr2.sh`, `nr2.py`, `nr2.out`, `nr2_results.json`, `nr2_bins.py`, `nr2_bins.out`; post-result `nr2_draws.py`, `nr2_draws.out`, `nr2_draws.json`. κ = ½ FITTED; no a₀ in the cold sector; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework. Snapshots stay local. **This is SPARC's line only:** the same runs still fail G-IN-all, G-MID-T3 and G-IN-Mall, all OVER.

## Measured, nine seeds finished at each mass, none flagged
| Mass | η ng 64 | η ng 80 [68 %] | ng 80 / ng 64 [68 %] |
|---|---|---|---|
| 10¹⁰ | 29.26 | 26.73 [20.75, 29.71] | 0.913 [0.696, 1.108] |
| 10¹¹ | 24.34 | 24.71 [14.86, 26.33] | 1.015 [0.604, 1.277] |
| 10¹² | 25.94 | 21.53 [14.55, 24.89] | 0.830 [0.553, 1.115] |

ρ₁₀ 1.241 [0.834, 1.864], ρ₁₁ 1.147 [0.683, 1.723]. Slope per dex: 0.047 from 10¹⁰ to 10¹², 0.060 from 10¹¹. The expected ranges on record held, and medians moved by under 25 %. None of the three ratios differs from 1 at 68 %, and each band is wide enough to hide a real change.

## Grade
| Run | ρ₁₀, ρ₁₁ | Υ A / B | rms A / B | line |
|---|---|---|---|---|
| **MEDIAN** | **1.241, 1.147** | **0.75 / 0.76** | **0.0690 / 0.0701** | **PASS** |
| Band low | 0.834, 0.683 | 1.06 / 1.05 | 0.0784 / 0.0795 | FAIL, Υ high |
| Band high | 1.864, 1.723 | 0.52 / 0.54 | 0.0688 / 0.0699 | pass, near the floor |
| MUTATE × 0.5 | 0.621, 0.574 | 1.14 / 1.14 | 0.0857 / 0.0868 | FAIL (Υ moves 0.39: bites) |

Groups Z +1.47 in every run. K1 29.259, 24.339 PASS. K2 |d| 0 PASS. A5's anchor re-read 21.531.

The ALT cell in NR1 (Υ 0.88 / 0.89, ratios held at ng 64's) is not what ng 80 reads: the low masses didn't fall by 0.83 at the median.

## Post-result, can't change the verdict
The frozen band holds η(10¹²) at 21.53 while its ratios resample η(10¹²), so it isn't the noise on the absolute η at each mass. `nr2_draws.py` resamples all three medians together and passes each draw's own values: **24 of 40 draws pass. All 16 fails are Υ high, none low.** Υ A p16, p50, p84: 0.66, 0.76, 0.92. Most fails have η(10¹¹) near 15, or η(10¹⁰) near 17–21. Nine seeds at each mass don't decide this line; the median sits inside it with room of about 0.05 below the ceiling. 40 draws is a coarse estimate, and only seed scatter is sampled.

## By V_flat, MEDIAN (reported, A background)
| V_flat | n | Υ | ΔV at Υ 0.50 | S rule | ET1 [CI] | |
|---|---|---|---|---|---|---|
| 20–60 | 13 | 1.20 | −5.0 | 48 | 69 [52, 85] | outside |
| 60–100 | 35 | 1.18 | −6.7 | 67 | 103 [81, 124] | outside |
| 100–150 | 23 | 0.90 | −12.2 | 87 | 143 [118, 200] | outside |
| 150–200 | 25 | 0.57 | −8.8 | 115 | 150 [98, 190] | inside |
| 200–250 | 18 | 0.62 | −21.6 | 140 | 215 [137, 272] | inside |
| 250–400 | 10 | 0.77 | −58.4 | 155 | 412 [182, 596] | outside |

The sample median hides a run of Υ with V_flat from 1.20 down to 0.57; S is outside ET1 in 4 of 6 bins, against 3 in NR1. The pass is on the median Υ and rms, which is what the line grades.

## Doesn't settle
Not re-run on these η: LITTLE THINGS, Local Group, Milky Way, KiDS, the surface-brightness tilt. η(10¹³), η(10¹⁴) are still ng 64 (A4) in this grader.

κ = ½ FITTED. Not theory closed.
