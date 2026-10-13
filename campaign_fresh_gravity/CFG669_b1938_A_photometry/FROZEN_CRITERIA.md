# CFG669 FROZEN CRITERIA: independent F277W photometry of B1938+666 perturber A (scores CFG668)

Date: 2026-10-12. Committed ALONE before any GO 8281 pixel is opened (the F277W mosaic is downloading; not read). Block
CFG660–669 (last id). Scores the sealed CFG668 prediction (sha256 9162427f…c04e) with these rules, unchanged.

## Data
`jw08281-o001_t001_nircam_clear-f277w_i2d.fits` (MAST level 3, pipeline as delivered, 384 MB), read with `python3 -I`,
memory-mapped cutout only. Units MJy/sr → Jy via PIXAR_SR; AB = −2.5 log10(F/3631 Jy).

## Positions
- Lens centre: flux-weighted centroid (first moment, 5×5 LW pixels) around the brightest pixel within 1.0″ of the pipeline
  catalogue source nearest RA 294.6050, Dec 66.8146.
- A: lens centre + (0.576″ N, 0.036″ W) — Vegetti+2012 (0.036, 0.576) with A "on the top part of the lensed arc". Robustness
  (reported, no verdict weight): the other sign/axis readings (0.036″ E; and swapped axes).

## Measurement (no free choices)
- Aperture r = 0.075″ (0.6 kpc) centred on A; local background = sigma-clipped (3σ) median in the annulus 0.10–0.18″ around A.
  Excess E = aperture sum − background × aperture area.
- Empirical error: the same aperture + annulus at 36 positions on the circle of radius |A − lens| around the lens centre, every
  10° of azimuth, excluding positions within 0.25″ of A. σ_emp = 1.4826 × MAD of their E (this includes arc/lens-light
  structure, not just noise). Significance S = E_A / σ_emp; E_A is also ranked among the 36.
- Point-source aperture correction: divide fluxes by EE(0.075″, F277W) = 0.60 (frozen; stated as approximate).
- m_A = AB of E_A/0.60 (if E_A > 0); 2σ limit m_lim = AB of 2 σ_emp/0.60.

## Verdict (CFG668 rules, per footing: faint end 29.63 can / 29.77 alt; exclusion line 30.82 / 30.96)
- **SURVIVES**: S ≥ 3 and m_A ≤ faint end.
- **EXCLUDED**: S < 2 and m_lim fainter than the exclusion line.
- **NOT DIAGNOSTIC**: m_lim brighter than the faint end (the data, as measured here, cannot reach the prediction).
- **TENSION**: anything else.
A crude independent measurement does not replace the PI team's full lens + light modelling; the label says so.

## MUTATE (`CFG669_MUTATE=1`)
Inject a point source of 28.0 AB (PSF = 2D Gaussian FWHM 0.092″) at A in a copy of the cutout; the procedure must recover it with
S ≥ 3 and |m − 28.0| ≤ 0.5 (exit 1 iff it bites). Also report recovery at 29.6 AB (no pass weight).
