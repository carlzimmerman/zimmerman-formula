# CFG438 FROZEN CRITERIA: H-alpha kinematics from our own OSIRIS DRP reduction of BX442 (z = 2.1765) and A1689B11.2 (z = 2.540)

Frozen before any kinematic extraction was run. The cubes are the official Keck OSIRIS DRP (run under GDL, see README for the infrastructure-only port patches). Raw data: KOA lev0, listed in ../_external_data/cfg437_work/koa_filelist.csv. Reduction outputs live in ../_external_data/cfg438_work/ (not in git).

## Inputs to the extraction
- BX442: the DRP mosaic (Mosaic Frames, MEANCLIP, TEL offsets) of the 40 A-B / B-A differenced 900 s Kn2 0.100" cubes (2011-08-23/24). Spaxels covered by fewer than 75% of the input frames are masked (Law+12's rule). No telluric/flux calibration (not needed for line centroids and widths).
- A1689B11.2: the DRP mosaic of the 8 object-minus-nearest-sky Kn5 0.050" cubes (2017-06-06). Image plane only (no lens model). Same 75% coverage mask.
- Spatial smoothing before fitting: Gaussian kernel FWHM 0.16" in each channel (Law+12's choice), i.e. 1.6 spaxels for BX442 and 3.2 spaxels for A1689B11.2.

## Per-spaxel line fit
- Model: H-alpha plus [N II] 6585 and 6549 as Gaussians with one common velocity and one common sigma; amplitudes free and >= 0, [N II]6549 = [N II]6585 / 2.95; plus a constant continuum. Weighted least squares (scipy curve_fit).
- Window: rest 6530-6610 A at the trial redshift, i.e. about +-1800 km/s around H-alpha.
- Noise per channel: the robust (1.4826 x MAD) standard deviation over all off-source spaxels of the smoothed cube in that channel. This carries the OH-residual structure.
- Bounds: |v| <= 500 km/s from the trial redshift; 15 <= sigma_obs <= 300 km/s.
- S/N cut: integrated H-alpha flux / its fit error >= 5. A spaxel passes only if the fit converges inside the bounds.
- Instrumental sigma: measured from isolated OH lines in a DRP cube of one BX442 frame reduced with no frame subtraction (Gaussian fits to >= 5 OH lines inside Kn2, median). Fallback if that fails: R = 3100 (Law+12), sigma_inst = c / (2.355 R) = 41 km/s. The intrinsic sigma is sqrt(sigma_obs^2 - sigma_inst^2), with spaxels where sigma_obs < sigma_inst set to 0 and flagged.

## Geometry
- Centre: the H-alpha-flux-weighted centroid of the passing spaxels.
- Kinematic PA: grid search over 0-359 deg (1 deg) of the model v = v_sys + V_t * tanh(d / r_t) * sign, with d the projected distance along the PA, fitted to the passing-spaxel velocities with v_sys, V_t, r_t free. The PA with the minimum chi^2 is adopted; its 1-sigma range is from delta chi^2 = 1 after rescaling chi^2_min to the degrees of freedom.
- V(R): a pseudo-slit 3 spaxels (0.3") wide for BX442 and 5 spaxels (0.25") wide for A1689B11.2, along the kinematic PA. Bins of 0.1" in projected radius on each side; inverse-variance mean of the velocity and intrinsic sigma of passing spaxels; folded V(R) = (V(+R) - V(-R))/2 where both sides exist. Deprojected by 1/sin(i) with Law+12's i = 42 +- 10 deg for BX442. No inclination is assumed for A1689B11.2 (projected only).
- Physical scale: flat LCDM H0 = 70.4, Omega_m = 0.272 (Law+12 cosmology), giving about 8.4 kpc/" at z = 2.1765.

## Validation (BX442 only; Law et al. 2012)
Published: kinematic PA 168 +- 1 deg E of N; observed gradient about +-150 km/s along the major axis; V_c = 234 (+49, -29) km/s at R = 8 kpc (i = 42 deg, from a PSF-convolved disk model); flux-weighted mean sigma_m = 66 +- 6 km/s; model sigma_z = 71 +- 1 km/s.

- V1 (line found): the S/N >= 5 spaxel count is >= 30, and the H-alpha line in the summed spectrum of passing spaxels has a fitted S/N >= 10 at |v| <= 300 km/s from z = 2.1765.
- V2 (PA): the kinematic PA is within 20 deg of 168 deg (or of 348 deg, sign convention).
- V3 (rotation): our deprojected folded V at the outermost bin with R >= 6 kpc (or the outermost bin reached, if it is < 6 kpc, reported as such) versus 234 (+49, -29). PASS if the difference is within the quadrature sum of the published error on the relevant side and our 1-sigma (bin error plus the i = 42 +- 10 deg propagation is NOT added again, since the published error is already dominated by i). MARGINAL within 2x that sum. FAIL beyond. Our raw V(R) is not PSF-corrected, so a low value from beam smearing is expected and is reported, not fixed after the fact.
- V4 (dispersion): our flux-weighted mean intrinsic sigma over passing spaxels versus 66 +- 6. PASS within the quadrature sum of 6 km/s and our error (bootstrap over spaxels, 1000 draws); MARGINAL within 2x; FAIL beyond. 71 km/s (sigma_z) is reported alongside.
- Lane verdict: VALIDATED if V1-V4 all PASS; PARTIAL if V1 passes and the rest are PASS or MARGINAL with at most one FAIL; NOT VALIDATED otherwise. A1689B11.2 is descriptive only (no published number is used as a tolerance).

## MUTATE (broken control, must fail)
Rerun the identical BX442 per-spaxel fit and the summed-spectrum fit at the wrong redshift z = 2.200 (H-alpha at 2100.8 nm, about 2200 km/s red of the true line, still inside Kn2 and outside the +-500 km/s velocity bound). The control works if (a) the S/N >= 5 spaxel count is < 10% of the true-z count and (b) the summed spectrum fit gives H-alpha S/N < 5. If MUTATE "finds" a line, the S/N machinery is broken and the true-z results are void.

## What this lane does not claim
- No a0 or acceleration claim is drawn here; this lane only establishes whether our own reduction reproduces the published kinematics. A one-galaxy kinematic result can never establish a0 evolution.
- Outputs: maps (PNG), V(R) and sigma(R) tables, JSON of all numbers, the README with the verdict.
