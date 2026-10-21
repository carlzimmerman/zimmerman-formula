# AG7 FROZEN CRITERIA (2026-10-21): power pre-flight. Can published stacked pair-lensing tell "no saddle trough" from MOND's trough?

Committed alone, before any AG7 script or number. Owner's go (2026-10-21, in chat): "freeze and run a power pre-flight of the
saddle no-trough prediction against published stacked pair-lensing measurements (verify the papers first; no data download
without my OK)". No data are downloaded; only published numbers are used.

## The two predictions
- **AQUAL/QUMOND (the law with phantom density allowed to go negative):** a negative surface-density strip through the
  midpoint of a galaxy pair, perpendicular to the pair axis.
  - This is prior art: Oria et al. 2021, arXiv:2109.10160, QUMOND, κ ~ −10⁻³ for single galaxies with an external field; and
    the Famaey & McGaugh review, arXiv:1112.3960.
  - Its size comes from AG6C's deep equal-mass pair solution (argon_push/AG6C_relativistic_completion, reviewed): the negative
    region is |z| ≲ 0.05d along the axis and R ≲ 0.43d across it; the edge-on line column through the saddle is
    Σ_line = |C_line| √(M_b a₀/G)/d, with C_line = −0.2064 (grid h) and −0.2158 (h/2).
- **PAPER49 v1.1 (a real medium):** no negative strip; zero trough.

## Published data (verified from the paper's own text, pdftotext of arXiv:1702.08485)
Epps & Hudson 2017, CFHTLenS × BOSS LRG pairs:
- About 23,000 pairs with 6 h⁻¹ ≤ R_sep < 10 h⁻¹ Mpc (mean 8.23 h⁻¹ Mpc); ⟨z⟩ ~ 0.42; ⟨log M*⟩ ~ 11.3; Σ_crit = 1640 M☉/pc².
- Filament box Δx × Δy = 7.1 h⁻¹ Mpc along the pair axis (excluding 2r₂₀₀ around each LRG) × 2.5 h⁻¹ Mpc across it.
- M = (1.6 ± 0.3)×10¹³ M☉, with the error from 1000 shape-noise realisations.
- Clampitt et al. 2016 (arXiv:1402.3302) and Kondo et al. 2019 (arXiv:1905.08991) are not used: no per-region surface-density
  error was verified from their text.

## Pre-flight (every choice favours detecting the trough, so NOT DIAGNOSTIC is robust)
- **Conversions:** h = 0.7. σ_box = σ_M/A_box. The trough is taken with no external-field suppression, d = the projected
  separation, and |C_line| = 0.2158 (the larger).
- **Upper bound:** the full line column Σ_line fills the whole strip.
- **Baryonic mass per LRG:** primary M_b = 10^11.3 M☉ (stars). Bracket M_b = 2×10¹² M☉ (×10, generously adding hot gas).
- **d:** primary 8.23 h⁻¹ Mpc; bracket 6 h⁻¹ Mpc (the closest pairs).
- **(a) Box statistic** (the published one): trough mean in the box ≤ Σ_line × (0.1d/Δx); S/N_a = that / σ_box.
- **(b) Optimal strip aperture** (not published; the best any re-analysis of the same data could do):
  - The aperture is 0.1d along the axis × Δy, so S/N_b = Σ_line / (σ_box √(A_box/A_strip)).
  - This assumes white shape noise. Kaiser–Squires map noise is correlated, so this, too, is optimistic.
- **Reading:**
  - **DIAGNOSTIC** iff S/N_b ≥ 3 at the primary M_b and d;
  - **MARGINAL** iff S/N_b ≥ 3 only inside the brackets;
  - **NOT DIAGNOSTIC** otherwise.
  - The filament's positive mass, which must be modelled to isolate a trough, is ignored. It only makes detection harder.
- **Forecast (reported):** the number of pairs N₃ needed for S/N_b = 3 at the primary values, scaling as √N at fixed source
  density, and a scaling to a ~100× larger pair sample with ~2× source density (DESI × LSST/Euclid-like). Labelled a forecast.

## Controls
- **K1:** C_line = −0.2064 with AG6C's F1 fiducial (8×10¹⁰ M☉ each, 0.77 Mpc, canonical a₀) reproduces AG6C's AQUAL negative
  column, −1.9647 M☉/pc², within 1%.
- **K2 (reported):** the mean box surface density M/A_box, and its significance, which must match the paper's ~5σ.
- **MUTATE (`AG7_MUTATE=1`):** the trough amplitude × 100. The primary reading must then be DIAGNOSTIC, and the script exits 1
  (the control bites).

## Settings
κ = ½ fitted; canonical a₀ (alt reported); not theory closed. A pre-flight decides only whether a test is possible, never which
prediction is right. Outputs: `ag7.py` → `ag7.out`, `ag7_results.json`; MUTATE → `_MUTATE`.
