# FROZEN CRITERIA: rotation curves from the SINS/zC-SINF AO Halpha cubes (data front, 2026-09-30)

Written and committed BEFORE any velocity, dispersion or flux value was extracted from these cubes. Only file names, FITS header geometry and the README were read (pixel scale, channel width, units, cube shape). Purpose: per-galaxy major-axis velocity profiles V_los(R) and V_rot(R) for the 35 galaxies of Forster Schreiber+2018 (z 1.45-2.52), from the raw cut cubes, with published values as controls. **No acceleration, a0, g_bar, baryon model or verdict is computed in this stage.**

## Inputs (input-side only)
- Cubes `*_data_cut.fits` and `*_noise_cut.fits` (W/m2/um, 0.05 arcsec pixels, 1001 channels around Halpha); centre = CRPIX1/2 of the header.
- From `highz_literature_tables/sins_ao/`: z_Halpha (Table 1), sin i and the published half velocity difference dv_obs/2 (Table 6), sigma_tot (Table 4), the PSF file for the resolution. Inclination is NOT fitted.
- Angular scale: astropy Planck18 at z_Halpha.

## Method (fixed)
1. Spatial smoothing of each channel with a Gaussian of FWHM 0.15 arcsec (variant B below: 0.10). Noise cube propagated assuming independent pixels before smoothing (error scaled by the smoothing kernel's noise-reduction factor).
2. Per-spaxel continuum-subtracted fit (local linear continuum) of Halpha + [N II] 6548, 6583 as three Gaussians with one common velocity and width, [N II] 6548/6583 fixed at 1/3, amplitudes free (Halpha, [N II] 6583). Start values: z_Halpha and sigma_tot from the tables.
3. A spaxel is ACCEPTED if Halpha amplitude / its fit error > 5 (variant: 4), fitted sigma_obs between 20 and 400 km/s, velocity error < 40 km/s.
4. Systemic velocity: the fit of the spatially integrated spectrum of accepted spaxels. Kinematic position angle: least-squares plane fit of the accepted velocity map weighted by 1/error^2; the angle of the gradient is the kinematic major axis (measured in the cube frame).
5. Major-axis profile: accepted spaxels within a strip of half-width 0.15 arcsec perpendicular to the major axis, binned in 0.15 arcsec steps along it, weighted-mean V_los per bin with propagated error; both sides kept separate. V_rot = V_los / sin i (Table 6). Radius in kpc from the scale above. Outer radius = last bin with at least 3 accepted spaxels.
6. No beam-smearing correction and no pressure-support (asymmetric-drift) correction are applied; the profiles are the OBSERVED ones.
7. All 35 galaxies are processed; none is dropped after seeing a result. A galaxy's profile is flagged `thin` (fewer than 3 bins on both sides) or `irregular` (Table 6 'Irr'), never removed.

## Controls and pass lines (fixed now)
- C1 (published comparison): (max bin V_los - min bin V_los)/2 against the published dv_obs/2 of Table 6. PASS if at least 70% of the galaxies with a profile agree within 25%. Below that the method is declared NOT validated and the profiles are reported as such.
- C2 (injection): a synthetic Halpha cube with a known arctangent rotation curve (V_max 200 km/s, r_t 0.4 arcsec, sigma 60 km/s, inclination 50 degrees, pixel scale 0.05 arcsec), noise drawn at the level of a real noise cube, put through the identical pipeline. PASS if the recovered major-axis V_los agrees with the input projected curve within 10% (rms) over radii up to 1 arcsec.
- C3 (stability): variants A (0.15 arcsec, S/N > 5) and B (0.10 arcsec, S/N > 4): report the rms difference of V_los per galaxy on common bins; stable if the median rms is below 20 km/s.
- C4 (kinematic PA): report |PA_mine - PA_published| (published PA_kin of Table 6 converted with the README rotation PASINF, both sign conventions tried and the better reported with a flag); no pass line, descriptive.

## Outputs and reporting
`sins_cubes/` CSVs (per-galaxy profile, per-galaxy summary, control results) with sha256 of each; results reported plainly including failures. The same rules would apply to KMOS3D (z >= 2) in a later stage, with its own criteria file.
