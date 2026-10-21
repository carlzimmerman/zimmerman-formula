# Independent follow-up observation-adapter audit

No serious coordinate-axis, restoring-beam, or integrated-flux normalization
error was found in the frozen adapter under its stated parent-frame
convention. This conclusion is supported by a bounded analytic response
experiment; it is not verification of an observed older-data remainder.

Reviewed `followup_model.py` SHA256:
`dd7f2dee4c2045bb1c146ea978b26aaa6097ffafcfa1822cb1ea2810da66da3a`.
Its `component_geometry` and `render` function ASTs match those in the
independently audited `forward_model_v2.py` exactly. The source fields,
side-dependent geometry, source-cloud fluxes, vertical lag, and arm quadrature
are therefore unchanged; the new code adapts the observation operator.

## Operator and unit inspection

The adapter loads each actual native header and uses its NCP pixel geometry.
It uses the dataset's J2000/HALOGAS or B1950/WHISP tangent reference, rather
than feeding J2000 coordinates into the B1950 header. All three actual
velocity axes increase, and all three spatial pixel grids are square, so
the used `np.interp` direction and `ds**2` pixel area are appropriate here.

For common-40-arcsec predictions, the total model covariance is a circular
40-arcsec Gaussian in native pixels. The observed cubes are broadened by
the difference between that target covariance and each native restoring
covariance. Thus the model applies the total target response once; it does
not add the native restoring beam twice. The HR40 and LR40 model operators
are exactly equal on their identical native grids, as expected; their
observed data and noise are still different image products of the same
observations.

Cloud weights enter as integrated Jy km/s. The normalized spatial/spectral
kernels preserve deposited flux before finite-ROI loss; division by pixel
area and channel spacing yields Jy per square arcsec. The model consequently
does not acquire the observed WHISP W.U.-to-Jy/beam conversion factor:
that factor belongs to the real-data reader, not a model already in physical
flux units.

WHISP's optical velocities use its legacy secondary velocity zero and the
frequency-dependent conversion. Model deposition and final sampling use
the nonlinear tabulated velocity axis. Convolution and brightness
normalization use mean optical channel spacing, which is a declared finite
approximation. The actual spacing ranges from 4.1268472 to 4.1410783 km/s,
a 0.344% full range. It is not an exact constant-km/s LSF operator.

The 192-by-192 spatial model ROI covers 768 arcsec for HALOGAS and about
960 arcsec for WHISP. WHISP has 127 native channels; its refined spectral
dimension is 253. Any copied metadata listing 69 native channels applies
only to HALOGAS, not WHISP. No hard memory cap was attempted or claimed.

## Independent bounded analytic fixtures

`followup_check.py` runs circular 40-arcsec Gaussian point-cloud references
on the actual native grids. It independently reads FITS headers, constructs
Cartesian tangent-to-sky coordinates, native NCP coordinates and inverse
tangent coordinates, computes optical velocities, and applies its own
eight-weight trilinear native-analysis sampler. Production code is used
only to evaluate the adapter under test. No observed intensity values are
used and no physical/data fit occurs.

The completed `audit/followup_run001` manifest validates against current
inputs. All ten coordinate/axis checks pass. Independently rebuilt target
coordinates agree within 4.1e-11 pixel. Independent optical velocities agree
within 1.2e-13 km/s. HR40 and LR40 point-cloud predictions are identical.

| WHISP40 cloud (major, minor, velocity offset) | Native L1 error | Refined L1 error |
|---|---:|---:|
| (0, 0, 0) | 0.792% | 0.242% |
| (0.7, 1.3, 2.1) | 1.382% | 0.289% |
| (13.7, -8.1, 23.6) | 0.497% | 0.187% |
| (170.3, 57.4, 38.2) | 0.503% | 0.232% |

Each cloud carries 0.3 Jy km/s and uses effective dispersion10 km/s. Deposited
and native postconvolution fluxes equal 0.3 to floating-point accuracy.
Native-to-refined L1 differences range from 0.429% to 1.096%. The off-center
cloud's final analysis-aperture flux differs from the continuous-velocity
analytic reference by about 0.036%, consistent with small projection,
nonlinear-channel, interpolation, and finite-aperture approximations. Central
WHISP40 checks at effective sigma8 and12 give native L1 errors of 1.184% and
0.604%. These point-cloud tests quantify finite behavior; they are not
uniform numerical bounds for every physical family member or box.

## Remaining interpretation limits

The coordinate fixture verifies the frozen parent convention. The adapter
and parent sampler keep the same numerical PA28 and local east/north offsets
when moving between the J2000 and B1950 tangent references. They do not
transform each complete sky point or the local tangent basis between frames.
An exact astrometric orientation-conversion audit is therefore separate
from the passed NCP/reference-center checks. This inherited approximation
should remain explicit if a subpixel cross-epoch agreement is claimed.

Effective sigma10 was inferred for the HALOGAS model including instrumental
effects. Carrying it into WHISP is a profile assumption, not an independently
measured older-cube intrinsic dispersion or exact transfer function. The
nominal sigma8/12 test is useful sensitivity, not exhaustive LSF propagation.
Restoring-Gaussian tests do not recover dirty-beam, CLEAN, calibration,
missing-spacing, baseline, or source-dependent noise uncertainty.

`run_followup.py` retains the original HR-calibrated component amplitudes
and does not fit WHISP or LR brightness. It compares the same frozen boxes
and retained-family gates. Its explicit native and common40 measurements
and real-blank scatter are needed to decide whether the older data had
useful sensitivity; failure to see a faint feature is not informative by
itself. The previously examined WHISP cube is not a blind holdout, HR/LR are
not separate observing campaigns, and complete visibility disjointness is
unverified. A known published HI extension cannot become a new phenomenon
merely because it lies outside a narrower frozen exclusion list.

The adapter audit does not cure the inadequate ordinary-disk fit documented
in `FAMILY_REVIEW.md`, establish residual significance, or identify a physical
memory state.
