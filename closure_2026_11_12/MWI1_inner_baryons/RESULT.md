# MWI1 RESULT: the stellar mass the rotation curve needs is above every published central value

2026-11-12. Criteria `FROZEN_CRITERIA.md` (2d31b06102), committed alone before the script. TEST lane.
Adopts nothing. Relabels no other lane. The published masses are web look-ups of abstracts and are
PROVISIONAL. kappa = 1/2 FITTED; not theory closed.

## Labels

| footing | required stellar mass [10^10 Msun] | label |
|---|---|---|
| canonical | 7.05 to 7.41 | **SUPPLIED BY 1 OF 5 (Licquia and Newman 2015); AT THE RECORD'S CENSUS NOT SUPPLIED** |
| alt | 6.36 to 6.73 | **SUPPLIED BY 2 OF 5 (Licquia and Newman 2015; Imig 2025 plus a bulge); AT THE RECORD'S CENSUS WITHIN 2 SIGMA** |

The required stellar mass is the rotation curve's baryon need (record, hunt item 35) less the cold
gas (1.191) and the hot gas inside 27 kpc (0.15).

## The comparison

z = (lower end of the need minus the published mass) / the published upward error.

| inventory | stellar mass | z canonical | z alt | the need as a multiple of it (canonical / alt) |
|---|---|---|---|---|
| Licquia and Newman 2015 | 6.08 +- 1.14 | +0.85 | +0.24 | 1.16 to 1.22 / 1.05 to 1.11 |
| Imig 2025 disc plus bulge | 6.18 + 0.21 | +4.14 | +0.84 | 1.14 to 1.20 / 1.03 to 1.09 |
| McMillan 2017 (the record's census) | 5.43 +- 0.57 | +2.84 | +1.62 | 1.30 to 1.36 / 1.17 to 1.24 |
| Cautun 2020 | 5.04 + 0.43 | +4.68 | +3.06 | 1.40 to 1.47 / 1.26 to 1.34 |
| Lian 2025 | 2.607 +- 0.363 | +12.2 | +10.3 | 2.70 to 2.84 / 2.44 to 2.58 |

## What it says

1. **The need is above every published central value, on both footings.** No inventory has the
   Galaxy as massive in stars as the rotation curve requires.
2. **Canonical is supplied only by the oldest and widest estimate.** It sits inside the error bar of
   the 2015 meta-analysis (0.85 sigma) because that error is 19 per cent. Against the census the
   record uses it is 2.8 sigma high, and against the two tighter recent values more than 4 sigma.
3. **Alt is supplied by two.** It is within one sigma of the 2015 meta-analysis and of the 2025
   APOGEE disc plus a bulge, and 1.6 sigma above the census in use.
4. **The newest estimate would break both.** Lian et al. 2025 put the stellar mass at 2.6 x 10^10,
   which the need exceeds by a factor of 2.4 to 2.8. An erratum is listed for that paper and its
   content was not found, so this row is the least secure.
5. **Geometry cannot supply it.** At fixed stellar mass, moving both stellar discs' scale length
   across the published range (2.15 to 3.0 kpc) changes the in-plane baryonic force at 12 to 27 kpc
   by -2 to +1 per cent; 3.5 kpc gives +1.7 per cent. That is at most 7 per cent of the canonical
   need.

So the Milky Way chain ends here: the outer data ask for nothing once hot gas is counted (MWG1), and
the inner need is a stellar mass of 7.05 to 7.41 x 10^10 (canonical) or 6.36 to 6.73 x 10^10 (alt).
That is a number a stellar census can decide.

## Checks

KA1: the ported census gives stars 5.4903, cold gas 1.1911, total 6.6814 x 10^10. KA2: the in-plane
force routine reproduces DW1's committed ratios at 20, 25 and 30 kpc (1.0599, 1.0614, 1.0586). KA3:
the need 7.050 to 7.411 and 6.356 to 6.730. M1: halving the excess amplitude changes two classes on
each footing (`mwi1_mut.out`).

## Limits

- The need is the record's rotation-curve fit (a uniform scaling on two pipelines, with no error bar
  on the amplitude), not recomputed here. Its radii are 12 to 27 kpc.
- Published stellar masses depend on the IMF, the assumed disc profile and what counts as bulge. The
  rows are not independent and are not on one convention.
- Imig's disc mass has a large downward error (-1.5); only the upward error enters here. The bulge
  added to it is Licquia and Newman's.
- McMillan's error is statistical only.
- The cold gas is held at the census value; a larger gas disc would lower the stellar need one for
  one.
- Bland-Hawthorn and Gerhard 2016 was not graded (no number in its abstract).

## Files

`FROZEN_CRITERIA.md`, `mwi1.py`, `mwi1.out`, `mwi1_results.json`, `mwi1_mut.out`.

Sources (abstracts, looked up 2026-11-12): Licquia and Newman 2015, arXiv:1407.1078; McMillan 2017,
arXiv:1608.00971; Cautun et al. 2020, arXiv:1911.04557; Imig et al. 2025, arXiv:2507.17629; Lian et
al. 2025, arXiv:2508.13665.
