# L017819 / SDSSJ1524+4409 literature audit

Guo latestversion: https://arxiv.org/abs/2602.13578v2 (29May2026), published MNRAS549(4),July2026,stag1029, https://doi.org/10.1093/mnras/stag1029 . Publication authenticated through primary publisher-index search; direct fulltext requests failed403/redirect. Published-table identity beyond v2 remains unchecked.

v2Table1 retains sigma_obs222.26±15km/s, lens/sourcez.320/1.210, apertureR.75arcsec, newlyfittedRe.55arcsec. Figure3 visually confirms this object among DESI DR1 spectra, labelled222.26±15.00. This is pPXF spectroscopy, not lens-inferred sigma. Method uses UVextended E-MILES and iterative source-emission masking: initial±20Å, mean normalizedresidual>.7, expand10Å. BOSS validation applies to four OTHER systems. Measurement-error construction, target-specific SNR, LSF/template-resolution matching and fit configuration are insufficiently documented to reconstruct±15. No bootstrap/MC measurement-error recipe found. The later analysis adds aperture/systematic uncertainties separately. Use native-aperture sigma conditionally; avoid double aperture correction.

Re.55 comes from Legacyz, fixedn4+PSF quasarcomponents. Major/circularized coordinate definition is not stated; lenstronomy name alone cannot resolve it. Do not silently map this to an ECLIPSE radius.

## Independent discovery astrometry

Primary Oguri2008 cached `euclid_eclipse_screen_2026_11_13/inputs/external_oguri2008.txt`, Section3.4 and Table5. Table2 convention inherited by Table5: positiveXwest,Ynorth. Relative toA=(0,0), B=(−1.485±.012,+.761±.012)arcsec; lensG=(−.576±.012,+.142±.012). A coordinate errors±.008. Statistical errors exclude systematic terms. Hence relative toG, A=(+.576,−.142), B=(−.909,+.619); these subtractions are a coordinate translation, not a new astrometric fit. Preserve shared-reference covariance rather than treating translated errors as independent.

Subaru spectroscopy separately extractedA,B,G in≈.6arcsecseeing: both quasar spectra show matching MgII/[OII] atzs1.210; lens absorption giveszl.320±.001. Table1 gives source1.210±.001. Image separation1.669±.020. Discovery paper's SIS/SIE-derived dynamical quantities are distinct from Guo's measured stellar sigma.

## Interpretation

The published measured dispersion is a useful conditional independent observable alongside resolved quasar astrometry. It does not supply a complete dynamical likelihood with certified quasar/LSF/template systematics. New imaging+Jeans analysis must use actual fiber placement/seeing, tracer geometry and anisotropy uncertainties; radius convention is unresolved. No newphysics conclusion follows here. No authors contacted.
