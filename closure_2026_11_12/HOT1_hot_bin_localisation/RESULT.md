# HOT1 RESULT: where are the hot 30 to 40 kpc BHB stars?

2026-11-12. TEST lane. Adopts nothing. Criteria `FROZEN_CRITERIA.md` (sha256 b86ab1cc..., `FREEZE_STAMP.txt`,
frozen 2026-11-12T22:45:18Z), written before any star of the catalogue was looked at in this lane. No
amendment. One run (`hot1.out`).

## Label

**CLUMPED** (L3 p = 0.0018). Not LOCALISED (L1 p = 0.0108, just above 0.01, and removing the top cell does
not bring the bin down to its neighbours). Not SAGITTARIUS RESIDUE (L2 one-sided p = 0.72; the stars nearer the
Sgr plane are slightly colder). Significance of the excess itself over the neighbours: z_ex = 2.25
(one-sided Gaussian p 0.012). It may be a fluctuation.

Read with the controls: the label does not explain the excess.
- The clumping is not special to the hot bin. The 40-55 kpc control bin, which is not hot (92.6 km/s), is
  more clumped (p = 0.0002), and 20-30 gives p = 0.063. Pairs close on the sky and in velocity are common
  throughout this halo sample.
- The clumped stars are the cold part of the bin. Removing every star in a counted pair (201 of 264, post hoc)
  RAISES the dispersion of the rest to 124.9 [114.6, 137.0] km/s. The rescaled f values (1.410, 1.352, 1.328,
  1.304) only show that the clumps are not the source of the heat. They are not a correction.
- The heat is spread over the footprint. Galactic north 107.3 [102.0, 113.1] (190 stars) and south 103.4
  [95.5, 112.6] (74 stars) are both above the neighbours' mean of 94.93. The two hottest cells are
  HEALPix cell 1 (l ~ 140, b ~ +48; 38 stars, 125.6 [112.4, 141.5]) and cell 8 (l ~ 58, b ~ -32; 38 stars,
  119.7 [107.1, 134.8]). They sit in different hemispheres. The L1 top cell is cell 0 (l ~ 49, b ~ +39;
  75 stars, mean +33.1 km/s, sigma 106.4). It is flagged mainly for its mean offset. Without it the bin is
  104.0 [98.9, 109.6], above the frozen threshold of 100.3.

## Numbers (test bin, 264 stars; permutation nulls 5,000, seeded)

| statistic | observed | null | p |
|---|---|---|---|
| L1 signed LR, max over 6 cells with >= 15 stars | 10.16 (cell 0) | | 0.0108 |
| L1b dispersion z (reported) | 1.98 | | 0.081 |
| L2 Sgr 15-30 deg (121) vs >= 30 deg (143) | z = -0.61; sigma 103.4 vs 108.4 | | 0.72 (two-sided 0.55) |
| L3 pairs < 10 deg and < 30 km/s | 213 of 1,125 close pairs | 172.9 | 0.0018 |
| L3 variant < 5 deg and < 20 km/s | 50 of 405 | 41.9 | 0.11 |
| L3 3-D (260 stars with PMs; < 10 deg, dV < 50 km/s) | 52 of 1,072 | 28.7 | 0.0002 |

Cell occupancy (nside 1, RING, Galactic): 75, 38, 46, 9, 0, 36, 0, 0, 38, 17, 5, 0. Per-cell mean and
dispersion are in `hot1.out`. Cell 5 (l ~ 91, b ~ +21; 36 stars) is the coldest at 76.1. Cell 3 (9 stars) has
mean -89.

Sub-bins: 30-35 kpc 102.4 [96.7, 108.7] (148), 35-40 kpc 111.0 [104.1, 118.8] (116). Bin mean v_gsr +0.2 km/s;
excess kurtosis -0.63; Shapiro-Wilk W 0.984, p = 0.0047. The velocities are flat-topped and not Gaussian,
which fits a mixture of offset components better than a hot Gaussian. This is reported without a label.

Controls (same statistics): 20-30 kpc L1 p 0.020, L1b 0.13, L2 0.25, L3 0.063, L3(5 deg, 20 km/s) 0.41;
40-55 kpc L1 p 0.030, L1b 0.054, L2 0.58, L3 0.0002, L3(5, 20) 0.0002.

## Checks (all passed before the label)

- K-H: HEALPix cells are equal area to within 0.5 per cent (10^6 points), and the pixel centres map to their
  own pixels.
- K-S: counts 865 / 264 / 241 / 125, and the 30-40 dispersion is 106.739.
- K-N: 200 smooth synthetic bins fire at p < 0.05 in 13 (L1), 9 (L2) and 15 (L3) of 200. At p < 0.01: L1 0,
  L2 1, L3 2 of 200, so L1 is somewhat conservative.
- K-P: the planted stream gives L1 p = 0.0004 and L3 p = 0.0002.
- Mutation M1 (one seeded shuffle): label DIFFUSE, L1 p 0.78, L2 0.60, L3 0.69. Passes (`hot1_mut.out`).

Disclosed design choice: L1 is a signed likelihood ratio, not the plain dispersion difference the brief named.
A design study on fully synthetic positions showed the plain difference cannot see a planted cold stream.
The plain difference is reported as L1b (p = 0.081).

## Limits

264 stars. The DESI footprint fills only 9 of 12 cells and 6 have >= 15 stars, so most of the southern and
inner sky is missing. L1 responds to mean offsets as well as to spread. A sky-wide dipole such as the LMC reflex
is not tested and could be part of the heat. DIFFUSE was not reached, so a wide structure (a shell, or the
Sgr or other debris beyond 30 deg) is neither shown nor excluded. CLUMPED does not identify any structure, and
the control shows clumping is common at these radii. The 3-D variant ignores tangential-velocity errors. The
null shuffles velocities among positions, so it tests position-velocity association, not equilibrium.
Known structures were named from memory (PROVISIONAL).

## Lead's verification and post hoc checks (2026-11-12, after the result above; not graded; no label changes)

Verification: the criteria file matches its stamp; the lead re-ran `hot1.py` and the three outputs came back
equal byte for byte; an independent recount of the L3 pairs (haversine on l, b) gives the same 213 of 1,125.
The script's "invalid value encountered in matmul" console warnings are harmless (every statistic is finite
and the recount agrees).

Post hoc (`hot1_posthoc.py`, `hot1_posthoc.out`; 5,000 permutations, seeds in the script). L3's null shuffles
velocities over the whole bin, so it also fires when the mean velocity or the dispersion merely differs from
one part of the sky to another. Three checks on that:

| | 30-40 kpc (hot) | 20-30 kpc | 40-55 kpc |
|---|---|---|---|
| L3 against a within-cell null (velocities shuffled only inside each HEALPix cell) | p = 0.019 | 0.29 | 0.0002 |
| dipole in v_gsr, amplitude and permutation p | 43 km/s toward l 56, b +39; p = 0.048 | 24 km/s; 0.040 | 26 km/s; 0.33 |
| between-cell mean offsets larger than chance | p = 0.011 | 0.12 | 0.078 |
| dispersion with the bin's own dipole removed | 104.6 | 96.9 | 92.2 |
| dispersion with each cell's own mean removed | 103.3 | 96.5 | 91.0 |

1. **The frozen label rests partly on sky-scale offsets.** With each cell's own velocity distribution kept,
   the pair excess in the hot bin drops from 40 pairs to 25 and p rises from 0.0018 to 0.019, above the
   frozen 0.01. The label CLUMPED stands as frozen; read against this null it would not have been reached.
   The 40-55 kpc bin, which is not hot, stays clumped under either null.
2. **Mean offsets across the sky are there, and they carry about a fifth of the excess.** The bin has a
   marginal dipole and cell-to-cell mean offsets (p 0.05 and 0.011). Treating all three bins the same way,
   the excess over the neighbours goes from 11.8 km/s (z = 2.25) to 10.1 (z = 1.95) with dipoles removed and
   9.6 (z = 1.87) with cell means removed.
3. **The rest has no identified source.** About 10 km/s of extra dispersion remains, under 2 sigma, spread
   over both hemispheres, with the pairs colder than the rest and no Sagittarius signal. A fluctuation is not
   excluded and no structure is shown.
4. RAW1's 30-40 kpc ratios, rescaled by the bin's dispersion alone (not a correction; the predicted
   dispersion was not recomputed): 1.166, 1.118, 1.099, 1.078 with cell means removed, against 1.205, 1.155,
   1.135, 1.114 as graded, errors near 0.055. RAW1's labels are not changed by this lane.

Limits of the post hoc: the reading rule was written after the outcome; with 5 to 9 groups the cell-mean
removal also takes out a little true dispersion (the chance column in the output gives the size, about
1 per cent); the dipole is fitted on a partial footprint and is not identified with any cause.

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`, `hot1.py`, `hot1.out`, `hot1_results.json`, `hot1_mut.out`;
the lead's post hoc `hot1_posthoc.py`, `hot1_posthoc.out`.
Data: https://data.desi.lbl.gov/public/dr1/vac/dr1/mws-bhb/v1.0/MWS_BHB.fits, sha256
5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246, 8,591,040 bytes, not in the repository.
Run: `python3 -I -B hot1.py <MWS_BHB.fits>` (about 20 s).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
