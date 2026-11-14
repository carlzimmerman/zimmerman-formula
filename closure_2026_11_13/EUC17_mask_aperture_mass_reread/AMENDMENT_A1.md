# EUC17 AMENDMENT A1

Committed alone, 2026-11-13, after the criteria (8b31c449c9) and after the mask fetch was started, before any
in-mask fraction, any corrected boost or any statistic has been computed. The fetch script's five-lens smoke test
showed five mask radii (4.00″, 3.78″ and three others); nothing was derived from them.

**Why.** Criteria §1 says the committed per-lens boosts are read and never recomputed, and check K0 asks for point
values reproduced to 1e-9. The committed per-lens files store `b` to four decimals, so a median or a fraction
computed from them cannot meet 1e-9. This was a design error in the check, visible from the file format alone.

**Change 1 (R1, R2 and EUC4's reported bins).** `b` is computed at full precision with the source lanes' own
imported code (EUC1's `load`, `select`, `build`, `solve_b`, exactly as EUC4 does), not read from the four-decimal
files. K0 as frozen then applies (point values to 1e-9, interval bounds to 0.01, words identical). New check
**K0b**: the computed per-lens values agree with the committed four-decimal values to 6e-5 for every lens.

**Change 2 (R3, the EUC10 reading, EUC1's conditional readings).** Their source redshifts are stored rounded, so
recomputing cannot do better than the stored boosts. The committed per-lens columns are used. For these K0's
point-value tolerance is 1e-4 on `b_med` and 1/N on fractions; interval bounds 0.01 and words as frozen.

**Change 3 (K4, which flux).** "The catalogue lens flux of the same band" is the released per-lens table's
`lens_flux_max_lh`, because the released map is the maximum-likelihood model. The median `lens_flux` is reported
beside it and is not the gate.

Nothing else changes: the correction, the rows, the lines, the words, the labels, the brackets, the twins and the
guards are as frozen.
