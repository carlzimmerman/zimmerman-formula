# HL1_lensing_vs_hydrostatic_pairs: FROZEN CRITERIA (committed alone, before any value in the table is read)

**Question.** LF1 leaves about 0.12 dex at fixed gas between shear on eRASS1 clusters and hydrostatic masses on X-COP. On clusters that have both masses, with gas at the same radius, is the gap there?

**Standing.** κ = ½ FITTED. Cold dark energy, never a particle. Not "theory closed". Nothing here says the data favour the framework. No a₀, so no footing.

**A bracket, never a framework grade.** Published weak-lensing masses are NFW fits, with published distances and calibration. So every number here is LITERATURE-INPUT. It can say whether the gap appears in others' data. It can't grade a rule.

**Own shear can't do this.** Of the 326 KiDS clusters, 7 have a pointed gas match and only 2 of those a hydrostatic catalogue (A2717 and A1692 in Sun+09; A1835 in Landry+13 and Mahdavi+13 makes 3). None of X-COP's 12 is in the 326. LF1's SE on 109 clusters is 0.04, so this is NOT POWERED before reading and I won't grade it.

## Data, on disk
Mahdavi+13, `_external_data/gs4/mahdavi13/` (fetched for GS4): table 2, per cluster at r500^WL: M_WL, M_Gas, M_hydro; table 1 for z. All clusters with all three numbers finite, split components taken as tabulated.

## Statistics
- **g** = median log₁₀(M_WL/M_hydro).
- **log Y_WL** = median log₁₀[M_Gas (1 + f★)/M_WL / 0.15945]; **log Y_hyd** the same on M_hydro. f★ 0.034 and 0.0615.
- SE: cluster bootstrap of the median, 5,000 draws, seed 20261031.

## Classes on g, with the line 0.12
- **NOT POWERED:** SE > 0.04.
- **NO GAP:** |g| ≤ 2 SE.
- **GAP AS LARGE:** g > 2 SE and |g − 0.12| ≤ 2 SE.
- **GAP SMALLER:** g > 2 SE and g + 2 SE < 0.12.
- **GAP LARGER:** g − 2 SE > 0.12.
- **REVERSED:** g < −2 SE.

## Reported, not graded
- M_WL above and below the sample median; z above and below the median.
- log Y_WL beside LF1's M3 at R₅₀₀ (−0.124 to −0.104), and log Y_hyd beside X-COP's at R₅₀₀ (−0.042, −0.031).
- Mean as well as median. Fit with the aperture's correlated noise noted: gas and M_hydro are read at r500^WL, so WL scatter moves all three together, and the ratio is not free of it.
- Selection: an X-ray-luminous sample, not the eRASS1 lensing sample.

## Checks
- **K1:** M_WL against 500 ρ_c(z) (4π/3) r500^WL³ at h 0.7, Ω_m 0.3: median |difference| ≤ 3 %. An independent test of the parse and of the stated cosmology.
- **K2:** row count against the file's data rows, every skipped row listed.
- **MUTATE:** swapping M_WL and M_hydro must flip g's sign exactly. Shuffling M_hydro between clusters must raise the rms of log(M_WL/M_hydro).
- Any K failure: no verdict, exit 1.
