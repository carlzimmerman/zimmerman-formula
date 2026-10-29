# Data checks of the three open predictions (2026-10-29)

**Status.** These are literature and data-availability checks. Web-search items are PROVISIONAL until the source text is
read. κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## 1. IC 1613's inclination: CHECKED, prediction fails

- **Source:** IN2 (5ce49c460e), Taibi+24 MUSE, read from the paper's TeX.
- **Independent stellar-tracer inclinations:** 36° ± 11° and 32° ± 11°. The photometric value is ≈ 37°.
- **IN1's frozen falsifier** (≥ 30° keeps it a failure) is met. **IC 1613 remains a failure**, disfavoured at about
  0.5–1.4σ, not excluded.

## 2. SLUGGS outer hot gas: NOT DECIDED (data exist, not yet extracted)

**The record's measured gas edges:** NGC 4374 at 18 kpc (outer GC bin at 22 kpc); NGC 5846 at 30 kpc (54 kpc).

**What the literature shows (provisional):**
- **NGC 4374 (M84):** the Chandra Early-Type Galaxy Atlas (Kim et al., [arXiv:1812.02718](https://arxiv.org/pdf/1812.02718))
  reports a temperature profile peaking near 1.5 keV at about 30 kpc and a ram-pressure gas tail over 10–30 kpc. Hot
  gas is detected **beyond** the record's 18 kpc edge. Its mass there is not yet extracted.
- **NGC 5846:** a joint Chandra/XMM mass-profile study (Kim et al. 2017,
  [arXiv:1706.02303](https://ar5iv.arxiv.org/html/1706.02303)) finds sloshing to the NE and hydrostatic agreement with
  optical masses to the NW. The radial extent of its gas-mass profile was not read here.
- **NGC 4365:** no deeper profile was located.

**Rigorous next step.** Download the Chandra Galaxy Atlas radial profiles for NGC 4374, 4365 and 5846, which needs the
owner's approval. Compare the measured M_gas(<r) at the GC radii with CFG331's extrapolation. SG1 passes only with the
extrapolated gas, so a measured deficit there would fail SLUGGS.

## 3. SP2 environment-split lensing: NOT TESTABLE YET

- No public environment-split galaxy–galaxy lensing product exists that isolates a central's own profile:
  - KiDS-1000's lensing-RAR release (Brouwer+21) provides **isolated** lenses only;
  - KiDS-Legacy's public products are cosmic-shear oriented;
  - Euclid DR1 is not yet public (Q1 covers too little area).
- Building the test from the full KiDS shear and lens catalogues (tens of GB, a group catalogue for the environment
  split, and covariances) is a project of its own. That is beyond the current budget.
- **SP2 stays sealed** (sha256 75b5fcdb…8b3d) for the future data.
