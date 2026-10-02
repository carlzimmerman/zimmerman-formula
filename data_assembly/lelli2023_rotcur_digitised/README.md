# Lelli et al. 2023 rotation-curve figure, digitised: zC-400569 and zC-488879 (figure read-off only)

Radii, rotation velocities and vertical error bars read off the raster figure "Rotation curves of zC-400569 (left) and zC-488879 (right)" of Lelli et al. 2023 (arXiv:2302.00030). Symbols: green squares CO(2-1), blue circles CO(3-2), cyan squares CO(4-3), red stars H-alpha. The figure file `Rotcur.jpg` (1984 x 982 px JPEG) was already on disk at `<repo-parent>/_external_data/arxiv_src/2302.00030/` (`<repo-parent>` is the directory that holds the repository checkout); nothing was downloaded and the work was done offline. **This directory contains the digitised points and documentation only.** No acceleration, a0, baryonic mass or gravity-law quantity is computed here, and the numbers are read off a plot (accuracy stated below), not the authors' tables.

## Files

| file | what it is |
|---|---|
| `lelli2023_rotcur_digitised.csv` | 25 data rows (zC-400569: 6 H-alpha + 5 CO(3-2) + 4 CO(4-3); zC-488879: 5 CO(2-1) + 5 CO(3-2)), 9 columns, 3,265 bytes, sha256 `c67eadd84e7e2897e738c882c56bf43545201a903e9fd7d9823ca893412c960c` |
| `digitise_rotcur.py` | The whole pipeline (Python 3, numpy, Pillow, scipy; developed with 3.13 / 1.26 / 11.3 / 1.14). `python3 digitise_rotcur.py` rewrites the CSV and the overlay in about 5 s and prints the QA summary quoted below; `--image PATH` and `--outdir DIR` are optional. |
| `qa_overlay.png` | The digitised points drawn over the original at 2x (3968 x 1964 px), sha256 `0578c2cd1e7c36da1edff0ee8eae891c7a2168ba111e80a222a068bef8b34188`. |
| `README.md` | This file. |

Reproducibility: after the last edit of the script, a run in place and a second run from a different working directory into a different output directory gave byte-identical CSV and PNG, and identical QA text (hashes above); earlier runs of the same code agreed too. The CSV notes contain only integers and coarse (5 %) fractions so that the file does not depend on the JPEG decoder's last-digit behaviour.

## CSV columns

| column | meaning |
|---|---|
| `galaxy`, `line` | `zC-400569` / `zC-488879`; `Halpha`, `CO(2-1)`, `CO(3-2)`, `CO(4-3)`. Rows follow the legend order of each panel, by increasing radius. |
| `radius_arcsec` | `(pixel_x - a_x) / b_x` with the calibration below. |
| `vrot_kms` | `(pixel_y - a_y) / b_y`. |
| `err_hi_kms`, `err_lo_kms` | `v(upper cap) - v` and `v - v(lower cap)`, both positive, from the rows of the two end caps of the marker's own bar. |
| `pixel_x`, `pixel_y` | (column, row) array indices of the marker centre in `Rotcur.jpg`: the origin is the centre of the top-left pixel and y increases downward (add 0.5 for pixel-corner conventions). They are whole numbers, see the next section. |
| `notes` | How clean the marker is (`clean`, `complete`, `overlapped`, `PARTLY HIDDEN`, with the neighbour or the covered fraction) and the two cap rows used. No commas inside the field. |

## Method

1. **Calibration.** The frame (spine) lines of each panel and the 1-px inward tick marks are located from the pixel darkness; the tick labels were read visually (left panel x 0.0 to 1.0, y 0 to 350; right panel x 0.0 to 1.0, y 0 to 400) and assigned in order to the tick pixels. `pixel = a + b * value` is fitted by least squares per axis (details below).
2. **Colour classes.** Chroma scores (red = R - max(G,B), blue = B - max(R,G), cyan = min(G,B) - R, green = G - max(R,B)) separate the four series and are robust to JPEG chroma blurring. Only the classes that exist in a panel are used there.
3. **Error bars first.** Long thin vertical lines of each class are found (gaps up to 24 rows are tolerated where another marker sits on the bar; non-maximum suppression across the 1.4-px line profile). This gives the number of points independently of the markers. The end caps are the 1-row horizontal lines at the two ends of each bar (statistic: the smaller of the left and right darkness over the columns 2 to 4 px from the bar, so a neighbouring bar 4 px away cannot fake a cap).
4. **Markers.** For each class a pixel template is built from the median of the un-occluded instances (iteratively registered; the absolute centre is fixed by the template's soft centroid, which lies within 0.13 px of the window centre for all four types). Each marker is located along its own bar by an integer-lattice template match; the cost is a truncated sum of squared RGB differences evaluated only on pixels that do not show another series' colour (grown by 2 px). This is what recovers the markers that are partly hidden behind another marker from their visible edges.
5. **Sub-pixel centroids.** For the 17 un-occluded markers a soft-weight centroid was also measured (see the lattice evidence); it agrees with the lattice position to 0.045 px at most, so the lattice position is the adopted one.
6. **Legend boxes** are found as the two long horizontal frame lines inside each panel (left panel x 724 to 956, y 729 to 880; right panel x 1725 to 1958, y 776 to 880) and excluded, together with their glyph bars.
7. **Robustness.** The whole localisation (masks, templates, bars, matching) is repeated under 7 alternative settings; nothing moves (below).

## The figure lives on an integer pixel lattice (this sets the accuracy)

Every feature of this raster (tick, spine, error bar, cap, marker) was placed at a whole-pixel offset, as in a matplotlib/Agg render at 100 dpi (an inference from the pixel patterns). Consequences and evidence, all printed by the script:

- All instances of one marker type are pixel-identical at integer offsets: mean absolute difference from the median template 1.5 to 2.0 (stars, 4 clean instances), 1.3 to 2.0 (circles, 7), 1.1 to 1.7 (cyan squares, 3) and 1.0 to 1.3 (green squares, 3) grey levels, which is the JPEG noise level.
- The soft centroids of the 17 un-occluded markers lie within 0.045 px (x) and 0.035 px (y) of the integer lattice (rms 0.025 and 0.020 px, mean offsets 0.001 px).
- Ticks and spines are single-pixel lines and the tick-position fit is feasible under pure round-to-nearest-pixel quantisation (minimax t* = 0.33 to 0.40, needs <= 0.5).
- The bar column equals the marker column for 25 of 25 markers.
- The cap-midpoint row minus the marker row is only ever 0 (11 markers) or +-0.5 px (14 markers), never +-1 px; SD 0.36 px against 0.353 px predicted. That is exactly what symmetric bars rounded on the same lattice as the marker give (Monte Carlo: 50 % zero, 25 % each at +-0.5 px, SD 0.353 px, and +-1 px impossible, whereas independent roundings would give +-1 px in 17 % of cases). So the plotted bars are symmetric to within the quantisation and there is no significant relative offset between markers and caps: mean -0.12 +- 0.07 px (per class: stars -0.17 +- 0.11, circles -0.15 +- 0.13, cyan squares +0.12 +- 0.24, green squares -0.20 +- 0.12 px).

So the figure itself only carries each coordinate to whole pixels (+-0.5 px, 1 sigma 0.289 px); a sub-pixel centroid cannot improve on that and would only report JPEG noise.

## Calibration (`pixel = a + b * value`, pixels are array indices)

| axis | tick pixels used <-> labels | a | b | LS residual rms / max | minimax t* |
|---|---|---|---|---|---|
| zC-400569 x | 114, 286, 458, 630, 801, 973 <-> 0.0, 0.2, ..., 1.0 | 114.238 | 858.857 px/arcsec | 0.264 / 0.448 px (0.00031 / 0.00052 arcsec) | 0.375 |
| zC-400569 y | 897, 775, 653, 531, 408, 286, 164, 42 <-> 0, 50, ..., 350 | 897.167 | -2.4438 px/(km/s) | 0.244 / 0.405 px (0.100 / 0.166 km/s) | 0.375 |
| zC-488879 x | 1116, 1272, 1428, 1585, 1741, 1897 <-> 0.0, 0.2, ..., 1.0 | 1115.857 | 781.286 px/arcsec | 0.239 / 0.371 px (0.00031 / 0.00047 arcsec) | 0.333 |
| zC-488879 y | 897, 790, 683, 576, 469, 363, 256, 149, 42 <-> 0, 50, ..., 400 | 896.778 | -2.1367 px/(km/s) | 0.248 / 0.444 px (0.116 / 0.208 km/s) | 0.400 |

The end ticks coincide with the spine lines (bottom or left spine = 0, top spine = last y label; right spine = 1.0 in the left panel). In the right panel the right spine (pixel 1975) is the unlabelled axis end; it is not used in the fit and maps to 1.0997 arcsec (read as 1.1). Residual rms 0.24 to 0.26 px matches the 0.289 px expected for uniform whole-pixel rounding, all residuals are below 0.5 px, and the least-squares and minimax calibrations differ by at most 0.14 to 0.21 px over the axis ranges.

Cross-checks of the visually read labels: the label glyph clusters are found 6 of 6 times below each x axis (centres within 1.5 px of the ticks) and 7 of 7 and 8 of 8 times beside the y axes (a constant offset of -3.0 and -2.9 px, spread 1.0 and 1.5 px: the text sits about 3 px above its tick; the bottom "0" label is skipped because it touches the "0.0" label); the mirrored top and right ticks coincide with the bottom and left ones.

Two checks that do not enter the fit and test both axes independently:

- **Mean velocity.** The mean digitised V_rot is 254.1 km/s for zC-400569 (15 points) and 336.0 km/s for zC-488879 (10 points). The paper's table of best-fit results (`tab:3Dfits`, line 289 of `ColdGasDiskCosmicNoon.tex` in the same local arXiv source folder) lists <V_rot> = 254 +- 41 and 336 +- 29 km/s; the +- there follows Eq. 3 of Lelli et al. 2016a and is not the scatter of the points (sample SD 21.6 and 11.0 km/s; s.e.m. 5.6 and 3.5). Differences: +0.1 and 0.0 km/s, within the 0.5 km/s rounding of the quoted integers. This is consistent with the table's mean being the plain mean of the plotted points (not verified).
- **Ring radii.** Each series' radii form an arithmetic progression R_k = R_0 + k*Delta with R_0/Delta = 0.499, 0.500, 0.501 (zC-400569 Halpha, CO(3-2), CO(4-3); Delta = 0.160, 0.190, 0.250 arcsec) and 0.503, 0.501 (zC-488879 CO(2-1), CO(3-2); Delta = 0.220, 0.210 arcsec), i.e. ring centres at half-integer multiples of a ring width; the rms deviation from the progression is 0.0003 arcsec (0.0000 for the last series, whose rounded spacing is a constant 164 px). R_0 minus Delta/2 is -0.0001, 0.0000, +0.0001, +0.0007 and +0.0001 arcsec for the five series (mean +0.0002; the largest, +0.5 px, is the CO(2-1) series), which is within the whole-pixel quantisation, so the x calibration shows no offset beyond about half a pixel (0.0006 arcsec). The CSV is not altered with this.

## Accuracy (1 sigma, from the whole-pixel quantisation plus the calibration uncertainty)

| quantity | zC-400569 | zC-488879 |
|---|---|---|
| radius | 0.00038 arcsec (marker rounding 0.00034, calibration 0.00017); worst case +-0.5 px plus 1 sigma calibration 0.0008 arcsec | 0.00042 arcsec (0.00037, 0.00020); worst case 0.0009 arcsec |
| V_rot | 0.13 km/s (marker rounding 0.118, calibration 0.051); worst case 0.26 km/s | 0.15 km/s (0.135, 0.065); worst case 0.30 km/s |
| each of err_lo, err_hi | 0.17 km/s (difference of two independently rounded rows); +-1 px worst case 0.41 km/s | 0.19 km/s; worst case 0.47 km/s |

Because the bars are symmetric, the mean of err_lo and err_hi is the better half-width (1 sigma about 0.08 and 0.10 km/s); err_hi - err_lo averages +0.11 km/s with SD 0.31 km/s over the 25 points, which is the rounding noise. In short: **about 0.0004 arcsec (never worse than about 0.001) in radius and about 0.15 km/s (never worse than about 0.3) in V_rot**, against plotted error half-widths of 19.6 to 42.1 km/s (typical 29 km/s) and a marker size of about 16 px (0.019 to 0.021 arcsec; 6.5 to 7.5 km/s). This is the accuracy of reading the figure; it says nothing about how closely the plotted numbers reproduce the authors' underlying numbers (for example if those were rounded before plotting).

## QA results

**(a) Point counts, found / expected:** zC-400569 H-alpha 6/6, CO(3-2) 5/5, CO(4-3) 4/4; zC-488879 CO(2-1) 5/5, CO(3-2) 5/5. No difference. No bars of a colour class that does not occur in a panel were detected (0 green in the left panel, 0 red and 0 cyan in the right panel), and the legend glyphs were excluded.

**(b) Mean velocities:** 254.1 km/s (zC-400569) and 336.0 km/s (zC-488879); differences from the paper's table +0.1 and 0.0 km/s (see above).

**(c) Visual check of the overlay (`qa_overlay.png`, inspected in full at 2x and in zoomed crops, 6x the source pixels, of the hardest regions):** every digitised centre (magenta square) sits on its marker and on its bar, every horizontal arm is on the marker's row, and all 50 digitised cap rows (orange dashes) lie on the original caps; the legend boxes are outlined and excluded; the green calibration marks sit on the ticks. For the most hidden marker (CO(2-1) point 1 of zC-488879, tag C21-1) the fitted 16 x 16 px square reproduces the visible top, bottom and right edges; reading the edge pixels directly gave a dark top edge at row 204 and a bottom edge at row 220 in a column outside the covering circle (centre row 212) and a right edge at column 1210 (centre column 1202), identical to the CSV.

## Points to treat with care

All 25 positions are decided on the integer lattice with clear margins (the script prints, per point, the SSD of the best competitor at least 3 px away along the bar and of the best 1-px neighbour, each divided by the SSD of the chosen position). The 17 clean markers all have ratios >= 53 (competitor) and >= 22 (neighbour). The overlapped, hidden and touching ones are:

| point (overlay tag) | situation | usable window / covered | competitor / 1-px neighbour | comment |
|---|---|---|---|---|
| zC-488879 CO(2-1) #1 (C21-1) | mostly behind the CO(3-2) circle, bars 4 px apart | 37 % / 55 % | x34 / x12 | position from the visible edges (checked directly, above); caps clean. The least-constrained marker and the one a user should look at first. |
| zC-488879 CO(2-1) #2 (C21-2) | partly behind the CO(3-2) circle | 66 % / 18 % | x83 / x33 | robust |
| zC-488879 CO(3-2) #1 (C32-1) | on top of the CO(2-1) square | 64 % / 0 % | x12 / x4.6 | thinnest margin of all: dark edge pixels of the square behind it are not flagged as "another colour", which inflates the cost. Bar column and cap midpoint agree exactly and the template-free centroid of its blue fill agrees to 0.04 px. |
| zC-488879 CO(3-2) #2 (C32-2) | on top of the CO(2-1) square | 71 % / 0 % | x128 / x50 | robust |
| zC-400569 H-alpha #1 (H1) | right arm under the CO(3-2) circle | 68 % / 5 % | x87 / x46 | robust |
| zC-400569 CO(3-2) #1 (C32-1) | on top of the H-alpha star | 80 % / 0 % | x132 / x54 | robust |
| zC-400569 H-alpha #6 (H6) | star touching the CO(4-3) square, bars 4 px apart | 60 % / 0 % | x5.8 / x34 | the smallest competitor margin of the set (the best candidate at least 3 px away along the bar costs 5.8 times more); cap midpoint equal to the row. See the stress test below. |
| zC-400569 CO(4-3) #4 (C43-4) | square on top of the H6 star | 85 % / 0 % | x44 / x18 | robust |

Other limits:

- **Masking limits.** The script's robustness block repeats the whole localisation with the foreign-colour threshold 30 or 45 (instead of 20), mask growth 1 or 3 px (instead of 2), no or a halved truncation of the pixel cost, and minimum usable window 0.20 or 0.35 (instead of 0.25): in all 7 variants all 25 positions and all cap rows are unchanged. Outside that range it degrades, and the script says so: growing the mask by 4 px moves H6 by 24 px (it would be caught by the cap-midpoint test), and a threshold of 12 leaves too few clean instances to build the star template. The adopted settings are therefore inside the stable range.
- **Visually read inputs.** The tick-label values (and the right-panel x limit of 1.1) are the only human inputs; they are cross-checked by the tick spacing, the label positions, the right-spine position (1.0997) and the two independent checks above, but no OCR was run.
- **Separate err_lo / err_hi** are each rounded independently (see the accuracy table); average them for a half-width.
- **Not done here:** no pairing of H-alpha and CO points, no merging of tracers, no replacement of the digitised radii by the fitted ring grid, no use of the paper's mean velocities in any value.

## QA summary printed by the script (excerpt)

```
3. COUNTS (found / expected):   Halpha 6/6  CO(3-2) 5/5  CO(4-3) 4/4  |  CO(2-1) 5/5  CO(3-2) 5/5
4. MEAN V_rot: zC-400569 N=15 mean 254.1 km/s (SD 21.6) vs paper 254 +- 41: +0.1 | zC-488879 N=10 mean 336.0 km/s (SD 11.0) vs 336 +- 29: -0.0
5. bar column == marker column for 25 / 25; un-occluded markers n=17, soft-centroid offset from lattice rms 0.025 / 0.020 px (max 0.045 / 0.035)
   template-match sharpness: competitor/best >= 6, 1-px neighbour/best >= 5; cap peak / next row >= 3.4 over all 50 caps
   error-bar symmetry: mean -0.12 +- 0.07 px, SD 0.36 px; 11 of 25 exactly 0, 14 at +-0.5 px, none at +-1 px
6. robustness: 7 variants, all 25 positions and cap rows unchanged; stress: dilation 4 -> H6 moves 24 px; threshold 12 -> template build fails
7. ring radii: R_0/Delta = 0.499 0.500 0.501 0.503 0.501, rms 0.0003 arcsec
8. accuracy: radius 0.00038 / 0.00042 arcsec, V_rot 0.129 / 0.150 km/s (1 sigma, mean over the points)
```

Run the script for the complete output, including the per-point diagnostics table.
