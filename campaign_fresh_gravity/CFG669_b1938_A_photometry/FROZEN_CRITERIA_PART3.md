# CFG669 PART 3 FROZEN CRITERIA (2026-10-12): improved lens model, F115W (0.031″ pixels) + F277W re-run

Committed ALONE before the F115W mosaic is downloaded or any F115W pixel seen, and before the improved model is run on anything.
Seen: Part 1 + Part 2 F277W results (χ²_ν 1337, sky unmodelled, λ and Sérsic at bounds, A-vs-arc floor ≈ 28.6 AB). Same sealed
prediction (CFG668, 9162427f…), same verdict rules.

## Model changes (fixed now, from Part 2's diagnosed failures only)
1. Sky: a constant background as an extra linear column.
2. Lens light: two concentric elliptical Sérsic components (shared centre; each R_e, n, q, φ; amplitudes linear). R_e ≤ 4″.
3. Source: 30 × 30 grid; λ grid log-spaced 1e-6…1e3 (19 values) × trace scale.
4. Everything else as Part 2 (SIE + shear, A = PSF point component at lens + 0.576″ N, 0.036″ W, sign free; 2×2 sub-pixel
   ray tracing; evidence-set λ; Nelder–Mead 4 + 2 + 1 restarts; errors stat⊕same-radius⊕sys; 28.0 AB tooth incl. one refit).

## Bands
- **F115W** (primary new data): `jw08281-o001_t001_nircam_clear-f115w_i2d.fits` + its catalogue; cutout 2.6″ (≈ 83 × 83 SW
  pixels); empirical PSF from that mosaic's catalogue stars (same selection, 21×21 → 15 × 15 stamp at SW). Prediction (CFG668):
  bright 26.90, faint 30.88 can / 31.02 alt, exclusion line 32.07 / 32.21; contamination threshold 25.7 AB (3× the bright-end
  flux). Tooth: inject 29.0 AB (≈ the middle of the sealed band) → recovered iff |Δm| ≤ 0.5 and S ≥ 3.
- **F277W** (re-run with the improved model): Part-2 thresholds; tooth 28.0 AB.

## Verdict
Per band, CFG668 rules. If both bands' teeth bite and verdicts disagree, the label is TENSION between bands (both reported). If only
one band's tooth bites, that band decides. If neither, NOT DIAGNOSTIC. Diagnostic (no weight): the χ²_ν = 1 floor per band.
Light: one process, nice; RAM < 4 GB.
