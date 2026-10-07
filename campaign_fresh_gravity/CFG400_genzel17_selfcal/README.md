# CFG400: the first self-calibrated a0(z) test on Genzel+2017's six deep curves. INVALID, NOT an a0(z) result

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 1dccb3a0c. Input: arXiv:1703.04310, fetched with the owner's yes (PDF 1,379,733 bytes, sha256 9926059ed950486e6982e3ec612303b4415832a3a01c091fc0035e564259e5d4; kept in _external_data/arxiv_pdf/, outside the repo).

**Digitising (`cfg400_digitise.py`):** all 180 vector markers from Figure 1 (6 velocity + 6 dispersion panels), with error bars. The axes are calibrated per panel from its own tick labels (residuals <= 0.02%; zC 400569 x-axis 1.8%). Bugs fixed during digitising, before any test number existed: the number parser, the panel splitting, and the galaxy-name lookup (caption words had overwritten the left-column labels).

**Frozen output (as computed):** Delta chi2 (RIVAL - DE) = -53.4 canonical / -45.7 alt, which by the frozen rule reads "SEPARATES (RIVAL preferred)".

**But the run is INVALID, and it must not be cited as an a0(z) result:**
1. **Frozen control C2 FAILED:** the digitised v_c(R_1/2) is within 20% of Table 1 for only 3 of 6 (COS4 01351 214 vs 276, GS4 43501 202 vs 257, zC 400569 283 vs 364 km/s; the digitised curves are beam-smeared, and Table 1 is the model value).
2. **The model is inadequate (post-run diagnostic, `cfg400_diagnostic.py`):** each galaxy alone (f and a0 free) prefers a0 of x0.09, x4.5, x7.9, x11.9 and >= x100 (twice, at the grid edge). That is 3+ dex of disagreement. The common best scale (x10.6 relative to the DE law) lies beyond even the rival (x3.3). Every law fits poorly (chi2 about 150-200 for 71 points).
3. **Why:** four of six galaxies have outer slopes dlog g/dlog R of about -1 (flat-ish) at g of about 1-3 a0, but the assumed exponential-disc baryons fall off much faster. So a0 is driven high to absorb the SHAPE mismatch (likely extended gas discs, pressure, or beam smearing). zC 406690 falls steeply (-2.36) and drives a0 low.

**Reading.** Self-calibration needs a CORRECT baryon SHAPE (it frees only the normalisation). With HST-light exponential discs as the shape, these six massive, gas-rich discs give no usable a0(z). A valid test needs resolved gas-profile shapes (CO / [CI] / dust maps) and AO-resolved inner curves, which is CFG385's specification. A bigger sample would not fix this.

MUTATE (outer v x1.3) moves Delta chi2 from -53 to -143 (the test responds); rc 1. C3 passes.
