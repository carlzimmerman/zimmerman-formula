# What the KURVS-CDFS paper (arXiv:2305.04382) says about its radii, velocities and gas (record only, read from the paper's TeX)

No g_bar or g_obs is computed here. Section and line references are to `kurvs_I_arXiv_May2023.tex` (kept outside the repo in `~/new_physics/_external_data/arxiv_src/2305.04382/`).

## 1. The radii R'_3D and R'_6D
- The disc scale radius is measured on HST imaging and is tied to the half-light radius: the paper writes that R_3D is "equivalent to ~1.8 times the half-light radius" (line 133) and that 3.4 R_D corresponds to "2 times the effective radius"
  (line 389). Both are consistent with R_D = R_eff / 1.68.
- R' is the "KMOS radius": "convolving the radius measured on HST observations with the 1 sigma-width of the seeing", "following Tiley+2019" (line 383). The seeing is FWHM 0.57 arcsec on average, with a 1 sigma width of about 0.25 arcsec
  (lines 268 and 361). **The convolution formula is not given in the paper; it refers to Tiley+2019, which I have not read.**
- Per-galaxy R'_3D and R'_6D in kpc are not tabulated. The paper states averages of about 7 kpc (3D) and 13 kpc (6D) (line 529). With R_D = R_eff/1.68 and the tabulated R_eff (mean 3.59 kpc, median 3.30 kpc), the mean 3 R_D is 6.4 kpc and the
  mean 6 R_D is 12.8 kpc, consistent with those averages; a seeing convolution changes the means by less than 0.5 kpc under the simple quadrature form I tried (6.8 and 13.0 kpc), which is my guess of the recipe and is not verified.

## 2. What the tabulated velocities are (the radii table, columns 2 to 5)
- Column 3: "Inclination-corrected velocity at the maximal extent of the observed rotation curve", with column 2 the "Maximal extent of the observed rotation curve" (7.9 to 15.2 kpc). These are data points.
- Column 4: "Inclination- and beam-smearing corrected velocity at R'_3D". Column 5: "Inclination-corrected velocity at R'_6D" (no beam-smearing correction; the paper assumes it is negligible beyond 3.4 R_D, line 389).
- The velocities at R'_3D and R'_6D are read off a **best-fit Freeman exponential-disc model of the observed curve**: "We measure the observed rotation velocity at different radii from the best-fit, centered exponential disc model" (line 382), and
  "measurements of the rotation velocity are extrapolated from the best-fitting model when the observed data do not extend far out" (line 386). The paper adds that for most sources the extrapolation is small.
- None of these velocities is corrected for pressure support. The paper applies an asymmetric-drift correction only for f_DM at R_eff, with "the Burkert+2010 formalism" and sigma_0 taken from the observed Halpha dispersion profile (line 631); no formula or
  further recipe is printed. It says the correction "increases as a function of radius" and assumes a constant sigma_0 and an unconstrained vertical geometry, and that circular velocities at high z "are largely dependent on the pressure-support correction" (line 766).

## 3. Gas
- No gas mass is tabulated. For the dark-matter fraction the paper models the baryons as a Freeman thin disc with mass "the sum of the stellar mass and a 40% molecular gas fraction", defined as M_mol / (M_star + M_mol), "the typical value expected from
  scaling relations" of Tacconi+2020 at the sample's mean stellar mass and redshift (line 635). It states that evaluating the fraction from the Tacconi+2020 relation at each galaxy's own stellar mass "does not affect the results" for f_DM at R_eff.
  The baryonic effective radius is the HST near-infrared one; a thick disc (q0 = 0.2) would lower the baryonic velocity by about 10% at R_eff.
- Stellar masses are MAGPHYS SED fits with typical uncertainty 0.2 dex (table note, line 251).
