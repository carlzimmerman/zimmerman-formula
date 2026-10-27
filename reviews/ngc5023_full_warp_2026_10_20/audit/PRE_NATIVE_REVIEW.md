# Independent review of the first native forward implementation

Files inspected: `forward_model.py`, `compare_model.py` and the completed
`nominal_run001` outputs. This report applies to those exact versions, not a
subsequent renderer revision. Hashes are in `PRE_NATIVE_PROVENANCE.json`.

## Verified finite obligations

The renderer's optically thin source measure, disk/arm Gaussian angular
normalization, side geometry selection, angular center conversion, native
NCP deposition and Jy/arcsec2/channel-density division are consistent with
the stated model class. Its vertical normal has the opposite sign from
the right-handed basis in `FORWARD_METHOD.md`; because each vertical source
profile is reflection symmetric, that sign has no effect on the emitted cube.

`audit/nominal_run001` independently reconstructs the masks and source-flux
bounds, solves bounded three-component least squares by enumerating all27
active sets rather than using scipy's optimizer, and checks residual metrics.
All16 finite checks pass. Analytic angular plus piecewise/continuous radial
integration agrees with the renderer's component fluxes to maximum relative
error5.42e-4. These checks do not validate the exact original TiRiFiC profile
conventions or establish predictive adequacy.

The preferred amplitudes are approximately0.9980,1.1417,1.0785. The two arm
coefficients reach their upper source-flux bounds; those source ranges are
not a measured posterior on the reconstructed fit. The separately labelled
"free amplitude" diagnostic still imposes bounds0..3 and must not be called
unbounded NNLS.

The training mask selects bin centers|Z|<=10arcsec, which is the full strip
|z|<=20arcsec. Validation bin centers>=50 mean footprints|z|>=40; guarded
centers>=70 mean footprints|z|>=60. The known-feature exclusions correctly
include bin halfwidth and a20arcsec beam guard on both inverted sides.

## Material refinement/response issue

For refinement f>1, the first NativeObservation implementation deposits on
a shifted fine lattice and samples the fine convolved cube directly at target
analysis coordinates. The actual observation is sampled first on the native
pixel/channel grid and only then linearly resampled by the analysis. Thus
f1-versus-f2 changes the observation operator as well as numerical resolution.
It is not a same-operator convergence check.

`audit/native_run001` compares four synthetic0.3Jy km/s single-cloud responses
against independently evaluated analytic spatial/velocity Gaussians on the
actual native NCP coordinates, followed by an independent eight-weight
trilinear sampler. No observed intensity values are used. The compensated
f1 renderer has relative L1 differences1.19–2.17%; the direct f2 renderer
has3.98–4.56%; f1-versus-f2 differences are3.97–5.66%. Total aperture flux
remains close to the input, showing why flux normalization alone does not
catch this shape error. The test reuses the production coordinate table
but independently implements sky inversion, Gaussian response and sampling.

A consistent refinement can anchor fine nodes exactly on native centers,
using shape`((Naxis-1)*f+1)` and cloud coordinates`native_coordinate*f`.
After convolution, restrict to the native nodes`[::f,::f,::f]`, then use the
unchanged native-analysis interpolator. This preserves the actual observation
operator and leaves f1 unchanged. A new renderer version and fresh fixture
check are required before calling its refinement converged. Alternatively,
retain the original f2 only as combined response/numerical sensitivity.

CIC mean-variance subtraction is an approximation: a point source's actual
subpixel CIC variance depends on its fractional position. It can correct
average blur but not exactly invert the deposition transfer. Its remaining
shape error belongs in any tiny-residual envelope. Exact native LSF,
dirty-beam/CLEAN response and source deprojection remain separate uncertainties.

## Interpretation of nominal actual data

Preferred-model training RMS is8.19 measured blank-scatter units, versus
8.64 for the author base model; median absolute training residual is about
1.28 units. Thus the reconstruction does not predict the bright disk to its
measurement noise. Validation RMS is1.143 and guarded-validation RMS1.053;
the author base model has1.282 and1.062. These are correlated-bin descriptive
ratios, not chi-square or confidence levels.

No broad excess is established in the protected outer strip at this stage,
but training inadequacy and the missing joint profile covariance prevent an
absence theorem. Remaining bright-disk hotspots cannot be promoted into new
physics by subtracting an approximate reconstruction. A robust localized
remainder still owes model-family uncertainty and numerical/response controls.
