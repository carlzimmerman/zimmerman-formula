# Acquired and checked the released gas-only lensing maps

2026-10-11. Frozen criteria committed alone as `06bb63220`. **16/16 checks
passed.** This is input preparation for the raw-image cluster test, not a
candidate-B fit or a derivation of its settled cold mass.

## Sources and scope

The [authors' public lensing release](https://niriss.github.io/lensing.html)
provides the three small gas-only FITS files saved under sources/, with exact
download URLs, sizes and SHA-256 hashes in sources/provenance.json. Total
download is about 1.3 MB. No fitted dark-halo map, posterior chain or bulk
archive was downloaded. These are older Chandra-derived gas products distributed
with the 2026 lens model, not a newly observed October dataset.

[Rihtarsic et al., section 4.2](https://arxiv.org/html/2601.22245v2) describes
the gas map as an X-ray-based reconstruction using geometric components and
spectral normalization. Thus it is observation-based but not a direct 3D mass
measurement. It inherits the gas reconstruction assumptions described in the
preceding baryon_depth_2026_10_11 report. The release parameter file identifies
these xray files as its separate profile-17 gas input; the release convention
is Dls/Ds=1. Source metadata in the preceding round_lensing folder was read
without using any fitted dark-halo parameters.

## Header and coordinate audit

All arrays are 256x256 and share the same TAN WCS. Pixel spacing is
1.968000000012 arcsec; increasing array x points west, increasing y north.
The FITS headers omit BUNIT and RADESYS. We therefore checked the differential
normalization and retained the missing-frame ambiguity explicitly.

All 135 gold images lie inside the maps for both the ICRS and FK5(J2000)
interpretations. Transforming the ICRS catalogue to FK5(J2000) before applying
the same header changes positions by at most 0.012012 pixels, about 0.024 arcsec.
This small difference does not determine which frame the old map actually uses.
It must not be silently assigned zero in an eventual precision fit.

## Differential consistency

For each of eight signed component permutations, evaluate
`D=(d alpha_x/dx+d alpha_y/dy)/2` and
`C=(d alpha_y/dx-d alpha_x/dy)/2`.
The preferred convention at both difference orders is
`alpha_x=+alpha1`, `alpha_y=+alpha2`, in west/north arcseconds.
The comparison uses the interior after removing an eight-pixel border.

| Difference order | Slope in D=s*kappa+b | Offset b | Residual RMS/std(kappa) | Curl RMS/std(kappa) |
|---:|---:|---:|---:|---:|
| 2 | 0.9997998585 | -0.0001090167 | 0.00417915 | 0.00082770 |
| 4 | 0.9999857614 | -0.0001156839 | 0.00303389 | 0.00078463 |

The fourth-order raw D-kappa RMS is 0.00573197 times the interior standard
deviation of kappa. The convergence map is positive throughout, with range
0.010630–0.122349. These facts are internal consistency checks, not independent
measurements of the gas mass. Multiplying BOTH convergence and deflection by
an incorrect common factor would evade this check; absolute calibration still
depends on the source reconstruction and declared distance convention.

The small fitted offset has not been explained from the map-generation
boundary conditions. It is not equal to the full-map mean kappa (0.0335303),
so a simple removal of that whole mean is not its explanation. We neither
subtract the offset from the gas nor rescale the deflections. Finite differencing,
boundary treatment, or map construction may contribute, but none was established.
The derivative check is consistent with the standard potential/convergence
definitions in the [Lenstool documentation](https://people.lam.fr/jullo.eric/lenstool/8.6.0/section_parfile/RunMode.html).

## Verification and next use

The code checks array integrity, common WCS, image coverage and both derivative
orders. An analytic quadratic potential supplies a known divergence and zero
curl; constant deflection offsets preserve both. A sign error and a degrees/
arcseconds error are MUTATE controls and are detected. The manifest pins the
source binaries, code, criteria and gold catalogue; all hashes validate.

No gas deflections at image positions, physical masses or fitted cold residuals
were computed in this audit. Next, build an explicitly framed/interpolated gas
contribution in the existing Helmert image operator, retaining the normalization
and coordinate uncertainties. A native distance conversion must specify how the
underlying X-ray reconstruction changes; do not merely reuse author-context
physical gas masses under a new background. Stellar masses, gas depth and host
assignment are still needed for the repaired-kernel settled term.

Once those inputs are declared, subtract the baryon-plus-settled prediction and
test the remaining lensing against a positive reservoir with a shared mass
budget, separately on both a0 footings. The present gas maps add a needed
observational component but do not resolve that full inference, the cold carrier,
settling rate or action. Kappa remains fitted. No Claude files or sealed
predictions were changed.
