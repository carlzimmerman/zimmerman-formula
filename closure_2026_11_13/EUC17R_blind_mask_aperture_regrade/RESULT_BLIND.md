# EUC17R (BLIND RE-GRADE OF EUC17): RESULT

2026-11-14. κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not
"theory closed". A re-read: it adopts nothing, edits no README, ledger or scorecard, and no outcome is a pass of the
lensing gate. Reading committed alone first (`READING.md`, 0aee9d1a75); the lead's EUC17 outputs were not opened
before this file was committed (leaks disclosed in READING.md §0: a memory-index line saying the lead's as-frozen
reading was voided by a harness tolerance, and the lead folder's file names).

## Labels (as frozen; every check K0–K4 passes; both twins exit 1)

| Row | canonical | alt | against committed | brackets |
|---|---|---|---|---|
| **R1** EUC1, sample P, source at infinity | **CEILING HOLDS** | **CEILING HOLDS** | **CHANGED** (was NO VERDICT / NO VERDICT) | **ROBUST** / **ROBUST** |
| **R2** EUC4, W_B (grade B, θ_E ≥ 1.7″) | **WIDE LENSES BREAK THE CEILING** | **WIDE LENSES BREAK THE CEILING** | **UNCHANGED** | **ROBUST** / **ROBUST** |
| **R3** EUC1-F as EUC16 graded it (11 lenses) | **NO VERDICT** | **NO VERDICT** | **UNCHANGED** | **ROBUST** / **ROBUST** |

No lane-level word. R1's CHANGED is toward the law: a hit, **not a pass**. CEILING HOLDS says only that, with every
source placed at infinity, the corrected sample does not exclude "law + catalogued stars" (EUC1 criteria §4). With the
source at z_s ≈ 2 (EUC1's conditional reading C2, reported, would-be) the corrected sample still reads CEILING BROKEN
(f₂₅ 0.272 [0.257, 0.288], alt). The failing row R2 survives the correction. R3 stays NO VERDICT.

**S1 says doubt the size of the correction.** The median −log₁₀ f on P is 0.071 dex, above the ≈ 0.05 dex to which the
uncorrected ECLIPSE scale already agrees with Auger 2009 and DESI CIGALE (EUC12). The corrected scale would therefore
sit above the total-magnitude scales by more than their present agreement: a reason to doubt the extrapolated Sérsic
wings that `M★ / f` adds (criteria §6 requires this sentence). The correction also grows with θ_E (median 0.050,
0.084, 0.121, 0.147 dex in the four classes), so it bites hardest exactly where R2 sits.

**Premise.** Everything corrected here rests on the catalogue paper's definition (stellar mass from the flux inside
the modelling circle) and on one lens (K4, FOR J0332). If the released masses are infinite-profile totals, every
corrected number is void.

## Numbers (law S unless stated; 95 % bootstrap, EUC1's `stats`, stream as in READING.md §3)

| | committed (f = 1) | corrected (b + log₁₀ f) |
|---|---|---|
| R1 canonical f₂₅ | 0.156 [0.143, 0.168] | **0.060 [0.052, 0.068]**, N = 3192 |
| R1 alt f₂₅ | 0.139 [0.127, 0.151] | **0.050 [0.043, 0.058]** |
| R1 canonical / alt f₀ | 0.472 / 0.436 | 0.313 [0.298, 0.329] / 0.273 [0.258, 0.289] |
| R1 canonical / alt b_med | −0.019 / −0.044 | −0.104 [−0.113, −0.094] / −0.130 [−0.138, −0.118] |
| R2 canonical f₂₅ | 0.758 [0.677, 0.831] | **0.444 [0.355, 0.524]**, N = 124 |
| R2 alt f₂₅ | 0.702 [0.621, 0.774] | **0.379 [0.298, 0.460]** |
| R2 canonical / alt b_med | +0.364 / +0.343 | +0.221 [+0.174, +0.260] / +0.197 [+0.151, +0.238] |
| R3 canonical b_med | +0.405 [+0.137, +0.589] | **+0.192 [+0.079, +0.338]**, N = 11 |
| R3 alt b_med | +0.385 [+0.121, +0.574] | **+0.174 [+0.061, +0.322]** |

Reported beside the rows (no word, or a would-be / secondary word):
- **Law B.** R1 canonical f₂₅ 0.092 [0.082, 0.102] (EUC1's rule would read NO VERDICT), alt 0.079 [0.069, 0.088]
  (would read CEILING HOLDS); committed 0.200 / 0.183. R2 canonical 0.556 [0.476, 0.645], alt 0.516 [0.427, 0.605]
  (BREAK both; committed 0.831 / 0.798).
- **EUC1's conditional readings, alt, would-be words.** C3 (z_s = 3): 0.296 → 0.149 [0.137, 0.161], CEILING BROKEN →
  NO VERDICT. C2 (z_s = max(2, z_l + 0.5)): 0.435 → 0.272 [0.257, 0.288], CEILING BROKEN → CEILING BROKEN.
- **EUC4's secondary and complement bins: NOT EVALUABLE (no mask).** 288 of 292 and 2022 of 2045 lenses have no mask:
  the frozen fetch covered only the union of the four per-lens files (§1 of the criteria), and grade-B lenses with
  θ_E < 1.7″ are in none of them except a handful from EUC16's table. Their committed words (BREAK / BREAK and NO
  VERDICT / NOT CONFIRMED) are not re-read. This is a gap in the frozen download list, not a failed check; closing it
  needs a download, which this re-grade was told not to make.
- **EUC10's reading (11 lenses with valid inputs).** b_med +0.543 → +0.337 [+0.079, +0.576] (canonical), +0.526 →
  +0.320 [+0.062, +0.560] (alt); f₂₅ 0.727 → 0.545 [0.273, 0.818] both. Its EUC1-F line (L016382, L015871): b_med
  +0.554 → +0.404, +0.536 → +0.386, N = 2, NOT EVALUABLE as before.
- **No mask.** 0 of 3192 (R1), 0 of 124 (R2), 0 of 11 (R3), 0 of 11 (EUC10). Of the table's 3366 lines, 3357 hold a
  usable mask; the 9 without are in none of the graded rows.

## Checks (frozen, as read in READING.md §4)

- **K0 PASS**, 24 of 24 items. R1 (S, B × both footings), R2 and both bins: N exact, every point value and bound
  identical to the committed ones (difference 0), every word. C3 / C2 (committed four-decimal columns): point values
  within 3.1e-4 = 1/N (one lens next to the 0.25 line flips with the rounding), bounds within 6.2e-4. R3, EUC10's
  reading and its EUC1-F line: within 5e-5. **Under the other stream reading (a fresh generator per statistic, same lens
  order) K0 also passes, 24 of 24**: the stream choice of READING.md §3 does not decide this check here.
- **K0b PASS.** Recomputed vs committed four-decimal b: R1 max 5.0e-5 over 12,768 values; R2 max 5.0e-5 over 248.
- **K1 PASS.** Half-light share 0.5 to 2.9e-7 (n = 1, 4, 8); n = 1 form with the function's own b₁ to 5.6e-17. With
  the exact b₁ = 1.67834699 instead of the function's 1.67834607 the form agrees to 2.2e-7, which would not meet
  1e-8 (READING.md §4 fixed the function's constant before the run).
- **K2 PASS.** EUC1's solver with M★/f returns b + log₁₀ f to 1.9e-14 on 20 lenses of P (every 159th with a mask),
  laws S and B, both footings.
- **K3 PASS.** 3,352 lenses with a mask across all rows: every radius > 0 and f in (0, 1]. No mask radius is smaller
  than the lens's Einstein radius (0 in every row).
- **K4 PASS** (FOR J0332, own code). Released unconvolved lens-light map (`pre_psf.fits` VIS_GALAXY_0, ADU/s, zero
  point 24.5 AB) summed inside the mask circle (r = 4.770″, centre (y, x) = (+0.35, −0.25)″, 7,128 pixels): 9.428 μJy
  against the catalogue's `lens_flux_max_lh` 9.325 μJy, **+1.10 %** (≤ 3 %; the other map orientation gives +0.14 %;
  against the median `lens_flux` +1.52 %). Analytic infinite Sérsic total from the released VIS Sérsic fit: 11.81 μJy,
  **1.266 ×** the catalogue flux (> 1.10). The premise is not contradicted. **Fragility of K4(b):** the conventions the
  released file does not state were fixed by the pre-registered match rule (intermediate-axis radius, intensity per
  pixel: in-mask model / map = 0.976). The major-axis reading matches the map worse (0.808) and would give 1.030 ×,
  which would fail (b). The per-arcsec² readings miss the map by a factor of 100.
- **K5 (no threshold).** f = 0.822 for FOR J0332 against the other agent's 0.804; 0.637 for L015780 against 0.587.
  The released elliptical Sérsic model of FOR J0332 puts 0.779 of its light inside the circle, so the circular,
  catalogue-parameter f of this lane is, on that lens, a smaller correction than the released model implies.
- **Twins.** `EUC17R_MUTATE=nomask`: all 16 committed words (rows, law B, both bins, C3, C2) come back; exit 1.
  `EUC17R_MUTATE=invert`: f₂₅ rises in R1 (0.156 → 0.283, 0.139 → 0.258) and R2 (0.758 → 0.903, 0.702 → 0.871), b_med
  rises in R3 (+0.405 → +0.547, +0.385 → +0.528); exit 1.

## Brackets (law S; no corrected word changes in any bracket, so every label is ROBUST)

| bracket | R1 f₂₅ upper bound, can / alt (HOLDS needs ≤ 0.10) | R2 f₂₅ lower bound, can / alt (BREAK needs ≥ 0.25) | R3 b_med bounds, can / alt |
|---|---|---|---|
| primary | 0.068 / 0.058 | 0.355 / 0.298 | [+0.079, +0.338] / [+0.061, +0.322] |
| F1a R_e × 0.80 | 0.085 / 0.066 | 0.403 / 0.355 | [+0.092, +0.370] / [+0.074, +0.354] |
| F1b R_e × 1.25 | 0.059 / 0.051 | 0.298 / **0.258** | [+0.063, +0.302] / [+0.046, +0.286] |
| F2 n = 4 | 0.078 / 0.063 | 0.371 / 0.315 | [+0.119, +0.356] / [+0.103, +0.341] |
| F3a r + \|c\| | 0.070 / 0.060 | 0.363 / 0.323 | [+0.080, +0.340] / [+0.062, +0.324] |
| F3b r − \|c\| | 0.066 / 0.056 | 0.331 / 0.282 | [+0.078, +0.336] / [+0.060, +0.320] |
| F4 no mask kept (none exist) | 0.068 / 0.058 | 0.355 / 0.298 | as primary |
| F5 n > 9.5 dropped | 0.062 / 0.051 (N 2919) | 0.330 / 0.275 (N 109) | [+0.072, +0.410] / [+0.055, +0.397] (N 10) |

The closest approach to a line is R2 alt under F1b (lower bound 0.258 against 0.25).

## Hand estimates in the criteria against the result

R1's f₂₅ was expected to fall to 0.08–0.12; it fell further, to 0.060 / 0.050. R2 was expected to stay above 0.25: it
did (0.444 / 0.379). R3's median was expected at +0.25 to +0.33: it fell further, to +0.192 / +0.174, and stays NO
VERDICT. f ≈ 0.8–0.9 for a typical lens: median f on P is 10^−0.071 = 0.85.

## Limits

- One lens checks the premise (K4); K4(b) passes only under the radius convention the match rule chose (above).
- f is the circular share of the catalogue's posterior-median Sérsic (R_e, n) inside a circle centred on the lens. The
  released elliptical model of the one lens with maps gives a lower share (0.779 vs 0.822).
- `M★ / f` is EUC1's infinite body normalised to the in-mask mass: an extrapolation of the fitted wings, not a
  measurement of outer light (criteria §8). S1 above says the extrapolated scale already sits beyond the 0.05 dex
  agreement with total-magnitude masses.
- R1 HOLDS is with every source at infinity; at z_s ≈ 2 the corrected sample would still break the ceiling (C2).
- EUC4's two reported bins are not re-read (no masks fetched for them).
- Blindness: partial, as disclosed in READING.md §0. The K0 stream choice was made after the leak; K0 passes under
  both readings, so the leak did not decide any check here.

## Files

`READING.md` (committed alone first); `euc17r.py`; `euc17r.out`, `euc17r_results.json`, `euc17r_f.csv` (per lens:
rows, mask radius and offset, θ_E, θ_e, n, f); twins `euc17r_MUTATE_nomask.{out,_results.json}`,
`euc17r_MUTATE_invert.{out,_results.json}`. Run from the repository root:
`python3 -I closure_2026_11_13/EUC17R_blind_mask_aperture_regrade/euc17r.py` (22 s; exit 0), the twins with
`EUC17R_MUTATE=nomask|invert` (exit 1 each). The main script was run once; nothing was repaired between runs.
