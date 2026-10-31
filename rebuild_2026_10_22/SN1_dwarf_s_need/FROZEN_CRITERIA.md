# SN1_dwarf_s_need: FROZEN CRITERIA

Committed alone, before any script or number from this lane. κ = ½ FITTED. Cold dark energy, never a particle. Footings never pooled. Not theory closed. Nothing here will say the data favour the framework.

## Question
The floor stays out of version N, and RG1 found the collapse rule, extrapolated, misses all five Local Group classes. So ask the data directly: what core strength S do the dwarfs need, is it one S or an S(M), and does any such curve join SPARC's measured need?

## Inputs (read only)
X49's data path, unchanged: `X1_hosted_recount/x1_per_system.csv`, CFG257's binary table, EM1's M200 relation, F3's h. The same five classes and 82 systems. The same E = log10(g_obs / g_pred), s from X1's Monte Carlo, Z from X49's bootstrap (median over systems, resample + noise), |Z| < 2 = REPRODUCED. The primary halo is the smooth core, B = 4(asinh x − x/√(1+x²)); Burkert is reported.

## Primary measures
- **S_need by class:** the S at which the class median E = 0, with M200 on EM1's relation. "NOT REACHED" if the median stays above 0 at S = 3000 Msun/pc².
- **S_min per system:** (M_need / r₁₂²) / 2.1907, the smooth core's own bound, needing no M200. M_need comes from g_obs − g_N. Reported with the M200 it implies, against EM1's.
- **Mass-capped systems:** count where M_need > M200 on EM1's relation; there, no S reaches them on that mass.

## Frozen verdicts (each on both footings; differing = UNDECIDED)
**V1, one S.** Scan lg S from 0.5 to 3.5, step 0.01. **ONE S ADMITTED** if some S has |Z| < 2 in all five classes; otherwise **NO ONE S**. Report the admitted range, and whether Σ_a0 (107.3 canonical, 129.7 alt) lies inside it. Being inside would be a coincidence on record, not a derivation.

**V2, power law.** S = S9 (M200 / 1e9)^p, on the same E, scanning lg S9 0.5–3.5 (step 0.01) and p −0.6 to +0.6 (step 0.01). Report the admitted region. **COLLAPSE SLOPE ADMITTED** if p = 0.24 (CR2's measured 0.238 ± 0.034, X80's 0.24) has an admitted S9, and report S9 / 29.4, the normalisation over the rule at lg M200 9. Otherwise **COLLAPSE SLOPE EXCLUDED**, and report the nearest admitted p.

**V3, join to SPARC (out of sample).** ET1's bands as ND1 tabulates them, Υ 0.50: lg M200 9.97, S [52, 85]; 10.59, [81, 124]; 11.13, [118, 200]. **CURVE JOINS** if any member of V2's admitted region lies inside all three bands. **JOINS LOW BINS ONLY** if inside the first two only. Otherwise **NO JOIN**. V2's region uses no SPARC number. Extrapolating the power law above the dwarfs is the test's own assumption, and it may fail for that reason alone: stated.

**V4, M200 removed.** Each class median of S_min and its Z-style band from X49's bootstrap. **ONE S_min** if a single S_min lies within 2 sd of all five class medians; otherwise **S_min VARIES**. Report S_min's Spearman against r₁₂, M★, and g_N, without a verdict.

## Reported, no verdict
Burkert rows. Fair-share M200 rows. Satellites against LG field, since the field has no host. Whether S_need moves past the rule at lg M200 9 (29.4). Each V2 region's lowest-mass and highest-mass end, stated as extrapolation.

## Limits stated in advance
EM1's M200 is carried 3–6 dex below its SPARC fit, with no scatter. Dwarfs are taken as in equilibrium, and no tides or stripping are modelled. Spherical, one r₁₂. ET1's bands depend on Υ 0.50 and on its fit choices. The S here is a description of what is needed, and no mechanism follows from it. If an S(M) is admitted it is a fit, and if it rests on a hand-set value it must be labelled that way.

## Checks
- **K1** S = Σ_a0, Burkert reproduces X49's class medians, |d| < 0.001.
- **K2** S from RG1's table, smooth core reproduces RG1's medians, |d| < 0.001.
- **K3** S_min bound: smooth core at x-peak gives 2.1907 S r², |d| < 1e-3.
- **MUTATE** Read S × 0.5 in the halo: S_need must exactly double where reached. Written to separate outputs.
- One thread, under 1 GB, nice 15. Rerun identical at fixed seed.

## Then
Also, separately from this lane's numbers: record in the owner's decision file that the working statement takes clusters as ZN3's native z = 0 profile, with its limits (gas-scale dependent, RF3's HSE-free narrow fail) and the seam with galaxies (ZN2: the same profile fails SPARC at low mass).
