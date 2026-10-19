# CFG799 ADDENDUM C FROZEN CRITERIA: the alternate-footing line at 595.463 GHz (committed before any download or statistic)

**Why.** CFG797 gives two framework-native lines, one per a₀ footing. CFG799 searched the canonical one (541.664 GHz). The
alternate footing (a₀ = 1.1312e-10) gives m = 2.46264 meV and **ν = 595.4630 GHz** (CFG797 `foot/alt`), with intrinsic width
0.350 MHz. CFG798 listed 52 HIFI observations covering 595.5 GHz (5.77 h) and judged the total below its own 10 h
feasibility threshold, so nothing has searched it. This addendum runs the CFG799 pipeline there. A null closes the converter
window for the alternate footing at the sensitivity reached. The framework predicts NO line; a line would kill it. Not
"theory closed". κ = ½ is fitted, and the two footings are not pooled.

**What is unchanged.** Everything in CFG799 `FROZEN_CRITERIA.md`, its addendum A, and the pipeline as implemented by
`cfg799_fetch.py` and `cfg799.py` (including the disclosed deviations D1 and D2): selection and masks M1–M4, total-power
calibration, the Level-1 anchor, the statistic, controls C1–C4, MUTATE, the classes, and the converter-window tier. The two
script copies in this folder differ from the CFG799 originals **only** in frequency constants (`DIFF_vs_CFG799.txt`, 8 changed at first commit, 9 after the correction below
lines):
- primary ν_t = **595.463 GHz** (CFG797 value 595.46298); secondary ν_2 = **595.500 GHz** (the rounded value of the brief);
- profile FWHM = √(0.35² + 1.1²) = 1.154 MHz (intrinsic 0.35 MHz from CFG797);
- the hot/cold J(T) conversion at 595.5 GHz, the observation list filter `595.5`, and labels.
- sha256 of the originals: `cfg799.py` 7486117b9e1c8c1e0736e811f606fc58502c311dbc96712fcd06faa840a81488,
  `cfg799_fetch.py` 84bb972c43deeb84fbe3f520388fe501d1b5ff6cebac14d3fae0d99293a0a784.
- sha256 of the copies in this folder: `cfg799.py` a5820f71ef94151683c4556c04bf67f65ed1f863931166f21cf47eac54042154,
  `cfg799_fetch.py` cd111e2191234672d5f2e78a55d2bf2c7f74acc7627fb08a718478f76c10aeec.
- **Correction, 2026-10-19, before any download or statistic.** The first committed copy of `cfg799_fetch.py` (sha256
  549c30a85acaf0c4404d7b2d8e4749544b37e9be40f57650333e96cf383bd125) read the CFG798 observation list through a path that
  is one folder too short for this directory. The copy now reads `../../CFG798_herschel_hifi_dish/cfg798_matches.csv`, which
  changes one more line (9 in all) and no logic. The 46-row selection was checked against that file.

**Data.** The 595.5 rows of `../../CFG798_herschel_hifi_dish/cfg798_matches.csv`, in the same four modes as CFG799 (DBS and
FastDBS, point and spectral scan): **46 observations, 4.61 h, all band 1b, none already reduced**. Excluded by the frozen mode
rule: 3 LoadChop and 3 FSwitch scans (6 observations, 1.16 h). Download from the ESA HSA one observation at a time, delete
the tars after reduction, keep a manifest. Expected volume ≈ 8 GB in total (by-mode mean of the 90 CFG799 downloads), under
0.5 GB in flight. Disk rule: no download if free space would fall below 25 GB.

**Pre-declared reading of the reach.** CFG798's forecast for 595.5 GHz was ε₅σ ≈ 7–9.6e-12 at S = 50 on radiometer noise
alone. CFG799 showed the 541.7 stack is limited by baseline structure and not by noise, with the honest 95% limit
between 1.4e-11 and 3.3e-11 across baseline choices. With 4.6 h against CFG799's 8.5 h expect this search to land at about
1.2e-11 to 5e-11 (S = 50). **The converter window (4e-9) is the target; the kill line (1e-12) is declared out of reach**
(a miss of ×10 to ×50). Nothing here can claim the kill-line test.

**Pre-declared reporting (lessons of CFG799 ADDENDUM B).** The class is set by the frozen H+V combined stack only. Beside it,
always report (informational, none sets a class):
1. H-only and V-only stacks at ν_t and ν_2;
2. the empirical-null scale: the standard deviation of the total-power z over a ±40 MHz scan (0.5 MHz steps) excluding ±5 MHz
   about ν_t and ν_2, and the 95% limit with σ_a scaled by max(1, that standard deviation), next to the frozen limit;
3. the ν_t limit across baseline variants (degree 2 to 5, half-window 50 and 100 MHz), reported as a range. The ±25 MHz
   window is not used (it falls under the frozen 100-channel minimum);
4. an exploratory decomposition like ADDENDUM B parts 1 to 4 (splits, width, H/V structure), with its declared list committed
   before it runs.
Any quoted limit is the range of 2 and 3, with the frozen number named as the number of record.

**Machine rule.** Runs go at the lowest priority (`nice -n 19`, background QoS) with swap watched; they go beside a live 1024³
run only on the owner's instruction for this lane.

External numbers stay provisional (sideband gain 0.5, load coupling 1, WBS response, S).
