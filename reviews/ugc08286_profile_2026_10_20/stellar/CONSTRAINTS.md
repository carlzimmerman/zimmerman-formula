# Independent stellar evidence for UGC08286 / NGC5023

Checked 2026-10-20. Scope: photometry and population evidence independent of this galaxy's rotation-curve fit. No rotation-fitted M/L was used. The source-specific records below pin the exact versions inspected. Downloaded public data and format documentation are pinned in `retrieval_manifest.json`; the earlier project data remain untouched.

## What can enter the inversion

There are independent resolved observations. What has **not** been recovered here is an intrinsic, dust-corrected, deprojected radial stellar M/L profile with per-radius uncertainty bounds over the full 17-point rotation-curve support. This is an acquisition/application limitation, not evidence that such information does not exist.

The usable population-calibration sensitivity test is:

\[
\Upsilon_{3.6}(R)\in[0.6\,10^{-\delta},\,0.6\,10^{\delta}]
\quad M_\odot/L_{\odot,3.6},
\]

with **declared analyst choices** of delta=0.1 dex or 0.2 dex. Numerically these are [0.47659694, 0.75535525] and [0.37857441, 0.95093592]. Letting annuli independently take any value in either box tests a conditional envelope; it does not encode a measured gradient, covariance, simultaneous confidence region, or a fitted gradient law. The 0.2-dex box is a deliberately widened sensitivity control, not a second published object-specific result.

This conversion concerns **old stellar light after nonstellar emission removal**, with a Chabrier IMF. Its stated precision must not be attached unchanged to the uncorrected SPARC brightness template. Using the narrower box with that template requires a contamination/photometry correspondence that has not been established here. The downloaded ICA stellar-emission map supplies an independent spatial light distribution, but turning its edge-on image into intrinsic annular mass requires the same explicit projection and vertical/support assumptions as the forward kernel.

An even less restrictive conditional test can expose the M/L values required by the rotation curve without interpreting them as independent population evidence.

For a one-sided exclusion test, an enlarged family allowing any annular effective M/L between zero and an upper ceiling can be used. Passing that test establishes only feasibility in the enlarged family. Failing it can exclude the corresponding old-star ceiling **conditionally**: the clean old-stellar luminosity density must not exceed the total-light density represented by the template, and unaccounted extinction, population/IMF variation, projection mismatch, photometric calibration, and support mismatch must not invalidate that ordering. Positive dust emission alone does not establish this bridge in an edge-on disk. The approximate calibration scatter also does not make either numerical ceiling an unconditional physical upper bound.

## Interpretation controls

- P3 profiles are averages on projected ellipses, not intrinsic face-on profiles. The fixed ellipses can differ between channels; their tabulated magnitudes cannot automatically be subtracted into a matched-aperture intrinsic stellar color.
- P3-specific intensity, surface brightness and errors are in columns 41--55; the first 40 columns contain legacy `ellipse` output whose brightness quantities should not replace the aperture-corrected products. `s4g_col.dat` defines the columns. P3 surface brightness is AB; the population color calibration below is Vega.
- ICA fixes a single stellar source color in the corrected regions. The spatial color-map file therefore does not supply independent stellar population color measurements at every radius.
- HST age-selected counts constrain stellar distribution shapes but do not by themselves give an M/L normalization. A vertical metallicity gradient is not a radial one.
- Optical colors are projected and extinction sensitive. A required intrinsic radial M/L cannot be certified or excluded solely by assigning each projected color to its projected major-axis radius.

## Status

Public S4G P3 numerical profiles and P5 stellar/color/mask FITS images were retrieved successfully. A numerical optical color profile beyond the published table entry, and numerical J-PLUS population/error maps, were not obtained in this bounded search. Published plots were inspected; no plot-digitized values were promoted into a fitted radial prior. No claim of global absence is made.

The machine-readable `source_records.json` and `observed_constraints.json` distinguish actual object measurements from calibration-derived sensitivity choices.
