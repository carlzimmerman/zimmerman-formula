# MWG1 RESULT: hot halo gas does not supply the rotation curve; it does lift the outer masses

2026-11-12. Criteria `FROZEN_CRITERIA.md` (9884ea05fd), committed alone before the script. TEST lane.
Adopts nothing. Relabels no other lane. The gas masses are web look-ups of abstracts and are
PROVISIONAL. kappa = 1/2 FITTED; not theory closed.

## Labels

| footing | part 1, the rotation curve | part 2, the outer data |
|---|---|---|
| canonical | **ROTATION CURVE NOT SUPPLIED** | **RECORD'S FIELD PASSES WITH HOT GAS, FRAGILE** |
| alt | **ROTATION CURVE NOT SUPPLIED** | **RECORD'S FIELD PASSES WITH HOT GAS, FRAGILE** |

## Part 1: the rotation curve

The rotation curve (12 to 27 kpc) asks for 1.71 to 2.07 x 10^10 Msun more baryons on the canonical
footing and 1.02 to 1.39 x 10^10 on alt. The hot gas inside 27 kpc is:

| model | inside 27 kpc [10^10 Msun] | share of the need, canonical | share, alt |
|---|---|---|---|
| Miller and Bregman 2015 (primary) | 0.15 | 7 to 9 per cent | 11 to 15 per cent |
| Salem 2015 | 0.07 | 3 to 4 per cent | 5 to 7 per cent |
| Faerman 2020 | 0.16 | 8 to 10 per cent | 12 to 16 per cent |
| Faerman 2017 | 0.14 | 7 to 8 per cent | 10 to 14 per cent |

No published hot halo puts more than a sixth of the needed mass inside the rotation curve's radii.
The gas is too extended.

## Part 2: the outer data

Census baryons at A = 1, hot gas added as published, MWJ1's three gates (DESI curves at 30 and
80 kpc; published masses at 100 kpc and beyond; plateau rows beyond 150 kpc).

| model | hot gas inside 200 kpc [10^10] | field window, canonical | field window, alt | at the record's field 0.01273 |
|---|---|---|---|---|
| none | 0 | 0 to 0.0075 | 0 to 0.0075 | fails the plateau rows (satellite class -2.72) |
| Salem 2015 | 1.42 | 0 to 0.0120 | 0 to 0.0120 | fails the plateau rows, narrowly (-2.08) |
| Miller and Bregman 2015 | 3.08 | 0 to 0.0195 | 0.0005 to 0.0195 | passes all three (plateau -0.22 / -1.34; Q 2.53 / 0.96) |
| Faerman 2020 | 3.32 | 0 to 0.0200 | 0.0010 to 0.0205 | passes all three |
| Faerman 2017 | 7.68 | 0.0045 to 0.0220 | 0.0045 to 0.0235 | passes all three; with no field the line is too high |

FRAGILE because the lowest-mass model (Salem 2015) leaves the record's field just outside. Every
model still allows fields at or below the rotation curve's limit of 0.008.

## What it says

1. **The outer problem goes away once the hot gas is counted.** PLT1 found the field reading low
   against the satellite masses beyond 150 kpc. That used a census with no hot halo. With the
   Miller and Bregman gas, the line at the environment's field passes every outer gate with census
   disc baryons, and the window reaches 0.0195, which covers M31's own field (0.016 to 0.017).
2. **The inner problem stays.** The rotation curve's extra 1.7 to 2.1 x 10^10 Msun (canonical) has
   to be inside about 27 kpc, and the hot halo supplies under a tenth of it. Whatever supplies it is
   in the disc or bulge: stars or cold gas.
3. **The Milky Way's single number is now local.** MWJ1 said "about a quarter to a third more
   baryons". With hot gas counted where it is, the outer data no longer ask for anything; only the
   rotation curve between 12 and 27 kpc does.
4. **A very massive corona needs a field.** With Faerman 2017's 1.2 x 10^11 the no-field line is
   too high beyond 150 kpc; it passes only for fields of 0.0045 and above.

## Checks

KA1: with no gas the script reproduces MWJ1 (Q 4.89 / 2.91; satellite plateau median -2.72; window
0 to 0.0075 on both footings). KA2: the Miller and Bregman profile gives 3.846 x 10^9 inside 50 kpc
against their 3.8. KA3: the line at 80 kpc 5.691 / 6.218 and 4.977 / 5.109. M1: ten times that gas at
no field fails the outer masses and plateau rows on both footings (`mwg1_mut.out`).

## Limits

- The gas masses span a factor of about four and rest on assumed metallicities and extents. Only
  Miller and Bregman's shape is fixed by two published masses; the other three shapes are assumed,
  and Faerman 2017's radius and slope are from memory.
- The Faerman models are hydrostatic in a dark-matter potential, so their shapes are not the
  framework's own.
- A disc-like hot component (eROSITA) is not included; no mass was found for it. It would act inside
  the rotation curve's radii.
- Part 1 is an upper-bound argument (mass inside the outermost fitted radius), not a refit of the
  rotation curve. The rotation-curve need is the record's (hunt item 35), not recomputed.
- The outer gates have little power (NMB1, PLT1). A pass is the absence of a contradiction.

## Files

`FROZEN_CRITERIA.md`, `mwg1.py`, `mwg1.out`, `mwg1_results.json`, `mwg1_mut.out`.

Sources (abstracts, looked up 2026-11-12): Miller and Bregman 2015, arXiv:1412.3116; Salem et al.
2015, arXiv:1507.07935; Faerman et al. 2020, arXiv:1909.09169; Faerman et al. 2017,
arXiv:1602.00689; Locatelli et al. 2024, arXiv:2310.10715.
