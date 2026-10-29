# CFG438B post-freeze diagnostic: split-half invariance (NOT part of any verdict)

Written 2026-10-29, before any split mosaic was built. These tests ask how accurate the BX442 numbers are: do the quoted errors hold when the same galaxy is measured twice from independent frames? They grade nothing and change no CFG438/438B verdict.

## Splits
Each split uses CFG438's own differenced cubes, the DRP Mosaic Frames (MEANCLIP, TEL), and CFG438's unchanged smoothing, noise, line fit and 75% coverage mask. The same splits are repeated on the S cubes once those exist.
- **N1 / N2:** night 2011-08-23 (22 cubes) against night 2011-08-24 (18 cubes).
- **HA / HB:** the 20 AB sequences, alternating in time order, so each half is 20 cubes spread over both nights.

## Tests (all at the true z = 2.1765)
- **I1 (honest errors).** Take the spaxels fitted in both halves of a split with S/N ≥ 3 in both, inside the coverage mask and not at a bound. Form the pulls (x1 − x2)/√(e1² + e2²) for v, sigma and H-alpha flux. Honest errors give a robust std (1.4826 × MAD) near 1. A value above 1.5 means the fit errors are underestimated by that factor, and every S/N in CFG438 is overstated by the same amount.
- **I2 (√N scaling).** Compare the summed-spectrum S/N of each half, over CFG438's 27 passing spaxels, with that of the full stack. White noise predicts a half-to-full ratio of √(n_half/40). A ratio well below that means the noise does not average down: correlated OH residuals or systematics.
- **I3 (systemic velocity stability).** The summed-spectrum velocity in each half. If the 80–100 km/s offset from z = 2.1765 holds in both nights, to within the errors, it is a property of the data or the z definition, not a one-night artefact.
- **I4 (52-frame forecast).** If I2 is consistent with white noise, 52 frames would raise the S/N by √(52/40) = 1.140. The forecast count is then the number of full-stack spaxels with S/N ≥ 5/1.140 = 4.39 (not at a bound). The split-half scatter of the count is reported alongside. If I2 shows non-white noise, the forecast is reported as unreliable.
- **I5 (PA stability).** CFG438's PA grid fit on each half's S/N ≥ 5 spaxels, where there are at least 10. Reported only.
