# CFG669 PART 2 FROZEN CRITERIA (2026-10-12): full lens + source + light model to score CFG668 at perturber A

Committed ALONE before any Part-2 code is run or any model fit is seen. Part 1 (aperture photometry) was NOT DIAGNOSTIC (arc
light). Same lane, same question, same sealed prediction (CFG668, 9162427f…), same verdict rules. Seen so far: the F277W cutout
image (Part 1 PNGs) and the Part-1 numbers only.

## Data
GO 8281 F277W level-3 mosaic (SCI, ERR), cutout 2.6″ × 2.6″ (41 × 41 LW pixels) centred on the nucleus (Part-1 corrected centre
rule). Noise = ERR. Pixels with non-finite SCI/ERR masked.

## PSF (empirical)
Pipeline-catalogue point sources in the same mosaic: is_extended = False, 20 ≤ aper_total_abmag ≤ 23.5, nn_dist ≥ 3″, ≥ 2″ from
the mosaic edge. Each 21 × 21 cutout, local median background removed, sub-pixel re-centred (first moment, scipy.ndimage.shift),
normalised, median-stacked, cropped to 11 × 11, renormalised. If fewer than 5 stars qualify: Gaussian FWHM 0.092″ (disclosed).

## Model (semilinear inversion; Warren & Dye 2003, Suyu et al. 2006)
- Lens light: elliptical Sérsic (centre, R_e, n, q, φ nonlinear; amplitude linear).
- Lens mass: SIE (θ_E, q, φ; centre = light centre + free offset ≤ 0.05″) + external shear (γ1, γ2). A's own deflection (θ_E ≈ 0.003″,
  sub-pixel at 0.063″) is neglected (stated).
- Source: 24 × 24 pixel grid over the bounding box of back-traced ring-annulus pixels (0.25″–0.85″), bilinear interpolation, 2 × 2
  image sub-pixel ray-tracing, first-order gradient regularisation, strength λ set by maximising the Bayesian evidence (grid of 13
  values, log-spaced 1e-3…1e3 × trace scale) at the best nonlinear fit.
- **A light component:** PSF-shaped point source at A's position (lens + 0.576″ N, 0.036″ W), amplitude linear, sign free.
- Fit: nonlinear parameters by Nelder–Mead with 4 restarts on −log evidence at fixed λ, then λ re-maximised; one iteration more.

## A's flux and its error
- f_A, σ_stat from the posterior covariance of the linear parameters, σ_stat × √(χ²_ν) if χ²_ν > 1.
- σ_pos: the same point component placed instead at 12 positions on the circle of radius |A| around the nucleus, every 30°, skipping
  any within 0.25″ of A, linear re-solve at the best nonlinear model; σ_pos = 1.4826 × MAD of those amplitudes (arc-absorption
  systematic). σ_sys: half-range of f_A over λ × {1/3, 3} and source grids 18² and 30² (linear re-solve).
- σ_tot = √(σ_stat² + σ_pos² + σ_sys²). S = f_A/σ_tot. EE correction: none (PSF-model flux is total). m_lim = AB(2σ_tot).

## Verdict (CFG668 rules; faint end 29.63 can / 29.77 alt; exclusion line 30.82 / 30.96)
SURVIVES: S ≥ 3 and m_A ≤ faint end. EXCLUDED: S < 2 and m_lim fainter than the exclusion line. NOT DIAGNOSTIC: m_lim brighter
than the faint end. TENSION otherwise. **Physical sanity (frozen):** a detection brighter than 25.4 AB (≥ 3 × the predicted bright
end in flux… i.e. M_* > M_lens) is classed NOT DIAGNOSTIC (contamination), never SURVIVES.

## Tooth (MUTATE, decides diagnosticity)
Inject a PSF point source of 28.0 AB at A into the data, full linear re-solve at the best nonlinear model, plus one full nonlinear
refit: recovered iff |m − 28.0| ≤ 0.5 and S ≥ 3. Also report 29.6 AB. If the 28.0 AB tooth fails, the lane is NOT DIAGNOSTIC.
Light: one process, nice, < 2 GB RAM (allowed while the 1024³ run is live).
