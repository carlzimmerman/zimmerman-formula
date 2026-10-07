# CFG393: group-catalogue RAR. Do SPARC centrals of group-mass hosts sit above the RAR, as a step in host mass?

## Verdict: NON-DISCRIMINATING on both footings. One frozen load-bearing control (C2) FAILED, so the run exits 1.

C2 failed because the control was badly designed, not because the match is wrong (see "Controls" below). The verdict stands, but
it rests on a run with rc = 1.

| statistic (frozen) | canonical a0 = 9.3603e-11 | alt a0 = 1.1312e-10 |
|---|---|---|
| N: centrals GC / satellites SAT / field F | 15 / 26 / 91 | 15 / 26 / 91 |
| (a) Delta = median R(GC) - median R(F), dex | +0.022 +- 0.037 (S = +0.61) | +0.026 +- 0.037 (S = +0.72) |
| (b) scatter ratio Q_s = rSD(GC)/rSD(F) | 0.51 (95%: 0.19-1.13) | 0.52 (95%: 0.19-1.13) |
| (c) dBIC(linear - step), > 2 favours step | -1.26 (the slope is preferred, weakly) | -1.40 |
| mass-matched control M: Delta_M | +0.005 +- 0.104 | +0.007 +- 0.104 |
| (d) satellites, cross-check: Delta_sat | +0.032 +- 0.027 (S = +1.19) | +0.035 +- 0.027 (S = +1.30) |
| C5 permutation p for abs(Delta) | 0.51 | 0.49 |
| verdict | NON-DISCRIMINATING | NON-DISCRIMINATING |

Plain reading:
- The 15 SPARC galaxies that are the brightest members of log M_h >= 12.5 groups do not sit measurably above the RAR at
  g_bar < 10^-10.5 m/s^2 compared with field galaxies. The offset is +0.02 to +0.03 dex, well within one sigma.
- The step model does not beat a linear trend in host mass (dBIC is about -1.3).
- Centrals do not scatter more than field galaxies. If anything they scatter less (Q_s about 0.5, not significant). Much of
  the field's scatter comes from dwarfs with larger errors.
- The result is not NOT SUPPORTED either. Delta + 2 sigma is about 0.10 dex, which is above the 0.05 threshold. The sample cannot
  exclude a 0.05 dex step.
- Power, shown by MUTATE: injecting +0.10 dex into every central gives Delta = +0.12 at S = 3.3-3.5. That is still not SUPPORTED,
  because dBIC is only +0.6 to +0.8 and the mass-matched Delta_M (+0.10 +- 0.10) fails the downgrade rule. As frozen, this
  sample could not have returned SUPPORTED even for a 0.1 dex step. The bottleneck is 15 centrals, and field galaxies that are
  ~2 dex fainter in L[3.6] (median log L 0.15 vs 2.40), which makes the mass-matched control noisy.
- Satellites, cross-check only: they sit +0.03 dex above field (+1.2 to +1.3 sigma). That is not the EFE's predicted negative
  sign, and it is not significant. The record's directional-EFE test is quoted, never averaged: +2.95 once, WALLABY -1.70.
- Distance-method control (C4, f_D != 1, 4 centrals): Delta is about -0.005. Most centrals have Hubble-flow distances.

Nothing here favours the framework over LCDM or the reverse. The cold-fluid mass is still required in groups and clusters
whatever SPARC shows. kappa = 1/2 is fitted.

## What was done
- Frozen criteria: `FROZEN_CRITERIA.md`, committed alone first (3a57634c6).
- Data: Kourkchi & Tully 2017 (J/ApJ/843/16, tables 2 and 3), Tully 2015 2MASS groups (J/AJ/149/171, tables 3 and 5), and SPARC
  positions (J/AJ/152/157 table1). All fetched fresh from VizieR on 2026-10-06 and logged in `FETCH_LOG.md` (URL, bytes,
  sha256). T15 table5 is 13.5 MB, so it is kept outside git in `campaign_fresh_gravity/_external_data/cfg393/`.
- Cross-match: the nearest catalogue galaxy within 60 arcsec, KT2017 first, then T15. Results are in `cfg393_match_table.csv`.
  - 138 matched in KT2017 and 16 in T15.
  - 1 was ambiguous (NGC1090) and 20 were unmatched (mostly the distant F5xx LSB galaxies, plus UGC00128/00731/01230/05005/05750).
    All of these are excluded, not treated as field.
  - A post-run name check found 43 KT2017 matches whose catalogue name differs from the SPARC name. All are alias pairs at
    <= 26 arcsec (for example UGC02953 = IC0356, UGCA444 = WLM, D631-7 = UGC04115). They were checked by eye, and no mismatches were found.
- Script: `cfg393_group_rar.py` produces every number above. Outputs are `cfg393_group_rar.out` and `_results.json`. The
  MUTATE run writes `_MUTATE.out` and `_results_MUTATE.json`.

## Controls (kept as they fell)
- C1 PASS: 175 galaxies, 163 with Q <= 2.
- **C2 FAIL (load-bearing):** only 6 of the 28 Ursa Major (f_D = 4) galaxies matched in KT2017 share one group PGC1. The
  control assumed KT2017 lists UMa as one group. It does not: it splits UMa into 12 groups, each of log M about 12.5-13.
  Post-hoc diagnostic C2b (reported, added after the failure) confirms 26 of 28 share one KT2017 association, PGC1+ 37617. So
  the matches are right and the control's premise was wrong. The run still exits 1, as frozen.
- C3 PASS (identity, 0 difference). MUTATE breaks it as designed.
- C4 and C5: see the table above.
- MUTATE (+0.1 dex on centrals): Delta shifts by exactly +0.1000 on both footings and the verdict does not move down. C3 fails,
  so rc = 1.

## Departures after freezing (disclosed)
1. C2b (association-level UMa check) was added after C2 failed. It is diagnostic only.
2. A post-hoc sensitivity, "POSTHOC assoc", re-classifies the KT2017 galaxies at the association level: mass = sum of member
   groups' 10^logMK, central = PGC1+. Result: 8 GC, 52 F, Delta +0.004 +- 0.039 (canonical) and +0.007 +- 0.039 (alt). No
   verdict weight.
3. The cross-match distance computation was switched from a matrix product to an explicit sum. The macOS Accelerate matmul was
   raising spurious floating-point warnings. The numbers are identical.
4. The frozen text said T15 group masses come from table3 via Nest. That is what the script does: table5 supplies membership
   and table3 supplies Mlum.

## Sensitivities (reported, canonical; alt within 0.005 dex)
| variant | N GC / F | Delta |
|---|---|---|
| threshold 12.3 | 24 / 81 | +0.016 +- 0.030 |
| threshold 12.7 | 13 / 107 | +0.022 +- 0.040 |
| KT2017 dynamical logMd | 6 / 44 | -0.012 +- 0.040 |
| KT2017 only | 6 / 88 | -0.007 +- 0.037 |
| T15 only | 9 / 3 | +0.160 +- 0.087 (3 field galaxies, meaningless) |
| f_D != 1 | 4 / 41 | -0.006 +- 0.043 |
| POSTHOC association | 8 / 52 | +0.004 +- 0.039 |

The only positive lean comes from the T15-matched centrals: the distant, bright UGC/NGC discs beyond 3500 km/s. Their
comparison set is 3 galaxies, so the lean is not interpretable. The KT2017 centrals show nothing.

## Caveats
- Group masses are model-dependent. KT2017 logMK and T15 Mlum come from different luminosity-to-mass recipes, and the primary
  sample mixes them (as frozen).
- SPARC is not complete or environment-selected. Classified centrals are bright discs, and field galaxies are mostly dwarfs and
  LSBs, so mass and environment are entangled. Control M addresses this, and it has a large error.
- KT2017 covers only V < 3500 km/s. T15 covers only 2MRS-bright galaxies.
- The step test (c) compares classes that are fully separated in x (all GC >= 12.5, all F < 12.5). The step and the slope differ
  only in how the field spans its own mass range, so (c) has little leverage with N = 106.
- This is a test of late-type centrals. cm08/cm09 measured the 0.13 vs 0.6 levels on early types. A null here does not erase
  that measurement. It says the two-regime excess does not show up at the outer RAR of SPARC group centrals at the 0.1 dex level
  this sample can resolve.

## Owner items
- None blocking. A decisive version needs about 3x more group centrals with deep outer HI and luminosity-matched field
  controls (for example, WALLABY or MIGHTEE discs cross-matched to a group catalogue). That would be a new fetch and a new lane.
