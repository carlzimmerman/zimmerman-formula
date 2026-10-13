# CFG674 (dir CFG669_b1938_A_photometry) PART 4 FROZEN CRITERIA (2026-10-12): production lens model (PyAutoLens) of GO 8281 F115W

Committed ALONE before any PyAutoLens fit is run. Seen: Parts 1–3 (all NOT DIAGNOSTIC; F115W own-model floor 31.4 AB, limit 28.67).
Scores the sealed CFG673 prediction (9162427f…) with its rules: F115W faint end 30.88 can / 31.02 alt, exclusion 32.07 / 32.21,
contamination threshold 25.7 AB. Tool: PyAutoLens 2026.10.12.1 in an isolated env (`_external_data/pyautolens_env`, Python 3.12).

## Data
Same F115W cutout (2.6″, nucleus centre rule of Part 1 corrected), ERR as noise, Part-3 empirical PSF (13 stars), mask: circle 1.2″.

## Model (three stages; addresses the assumptions listed for the published analyses: smooth-model multipoles, source priors,
lens-light subtraction)
1. Lens light: two linear elliptical Sérsics (shared centre); mass: PowerLaw + ExternalShear; source: linear Sérsic. Nautilus.
2. Mass: PowerLaw + ExternalShear + PowerLawMultipole m = 4 and m = 3; source: Delaunay mesh (adapted to the stage-1 source image)
   with adaptive-brightness regularisation; lens light as stage 1 (re-fit). Nautilus.
3. A test at the stage-2 maximum-likelihood model: add `lp_linear.PointSource` (lens plane, centre fixed at A = nucleus +
   0.576″ N, 0.036″ W), linear amplitude, sign free; also re-fit the regularisation hyper-parameters with A present.
   - f_A from the linear solution; σ_stat from the inversion's linear covariance (or, if not exposed, from 200 noise-realisation
     re-solves); σ_pos from the same component at 12 same-radius positions (MAD); σ_sys from the m=3 multipole on/off and mesh
     resolution ×{0.7, 1.4}. σ_tot = quadrature sum. ΔlogE (with A − without A) reported, no verdict weight.
   - Tooth: inject 29.0 AB PSF point source at A, re-solve stage 3: recovered iff |Δm| ≤ 0.5 and S ≥ 3. Tooth fails ⇒ NOT DIAGNOSTIC.
## Verdict (CFG673 rules), per footing
SURVIVES: S ≥ 3 and m_A ≤ faint end (and not brighter than 25.7). EXCLUDED: S < 2 and 2σ limit fainter than the exclusion line
(Part 3 showed this is not reachable; stated). NOT DIAGNOSTIC: 2σ limit brighter than the faint end. TENSION: otherwise.
Light: nice, one process; RAM < 8 GB. If the stage-2 search cannot finish in 12 h of wall time, the lane reports NOT RUN.
