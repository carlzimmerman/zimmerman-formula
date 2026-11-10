# KO2 AMENDMENT A4 (post hoc: written after the main run's outputs were read)

Committed alone, before the diagnostics below are computed. It changes no frozen label, line, bracket, design or tolerance. The
frozen labels stand as computed: **NO VERDICT on both footings, for both types**, because KA-3b failed. Everything declared here
is reported, not gated.

## What has been seen (all of `ko2.out` and `ko2_MUTATE.out`)

- Checks: 12 of 13 pass. KA-3b fails: in all four plants the largest pull is the same 3.11. KA-4 passes (late 0.802,
  early 0.956). The cross-shear null passes.
- Primary R_ext, canonical (alt identical to three decimals): late 0.277 +- 0.183 (ABSENT on its own), early 0.487 +- 0.071
  (REDUCED on its own). B1 (115 Mpc): 0.571 / 0.565. B2 (closure zero): 0.229 / 0.393 (early ABSENT). B3 (untied): 1.071 +- 0.199
  (late PRESENT) / 0.739 +- 0.115 (early REDUCED). Secondary R_own: 0.207 +- 0.278 / 0.263 +- 0.111 (both ABSENT). The bracket
  rule alone would give NOT SEPARATED for both types: late through B3, early through B2. Floor 0.9999.
- MUTATE: M1 bites but has no power (true early - late +0.210 +- 0.194). M2 bites (neighbour share +0.001 +- 0.005 shuffled,
  against +0.205 +- 0.011). **M3 does not bite**: late WG x 0.4 in bins 0-6 moves R_ext(late) by +0.013 +- 0.075.
- Reported items R1-R7, as printed in `ko2.out`.

## Why diagnostics are needed

1. **KA-3b.** The plant's recovered amplitudes are exactly the planted ones plus the cross-shear fit, because the fit is linear
   and the noise is WX. So KA-3b tests 15 cross-shear amplitudes at 3 sigma each. The same 3.11 in all four plants points to
   one null amplitude. With 15 jackknifed amplitudes, the chance that one exceeds 3 sigma is several per cent. That would make
   the frozen KA-3b a multiple-comparison test, not a correctness test. The frozen label is not changed on this ground.
2. **M3.** In the tied design one amplitude per class serves lenses and neighbours alike. The 475,464 late pool objects enter
   12.8 million neighbour pairs. M3's failure to bite suggests that the late ext amplitude is set by late galaxies as neighbours
   of other lenses (many of them satellites near hosts), not by the late lenses' own profiles. If so, the tied primary does not
   measure "the lens's own field" for late types, and the untied bracket B3 is the reading that does.

## Diagnostics (declared now; computed in `ko2_formB.py`, which already rebuilds the main normal matrix)

- **D1** the per-amplitude pulls of the cross-shear fit in the primary design, both footings. Which amplitude reaches 3.11,
  and how many exceed 2 and 3.
- **D2** M3 (late WG x 0.4 in bins 0-6) applied to the untied design B3 and to the secondary design: the change in R_ext(late),
  and in R_own(late), with the joint jackknife. M3 bites on a design if the change is below -2 sigma.
- **D3** where each design's ext information comes from. For each class's ext amplitude in the primary design: the shares of
  the diagonal information from the lens-own columns, from the neighbour columns, and from their cross term.
- **D4** form B's prediction (A3's method) also for the untied design B3, beside the primary and the secondary.

## What would follow (stated before computing)

- If M3 bites on B3 and D3 shows the late ext information in the tied design coming mostly from neighbour columns, RESULT.md will
  say that the frozen primary does not measure the late lenses' own field. It will give B3's reading as the one that does,
  labelled post hoc, with no label attached.
- If M3 does not bite on B3 either, neither design measures the late lenses' own outer field, and RESULT.md says so.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
