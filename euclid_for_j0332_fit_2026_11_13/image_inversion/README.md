# Independent Gaussian pixelized-source inversion

API (coordinates arcseconds, X=WEST,N=NORTH):

```python
from inversion import setup
obj = setup(nsource=25, source_pixel=.04, source_center=(-.03,-.05), supersample=1)
obj.operator(lambda X,N: (alpha_west(X,N),alpha_north(X,N)))
r = obj.optimize_regularization()  # or obj.evaluate(log_regularization=6.8)
# r: score/log_evidence, chi2, source, model_valid, lens_amplitude, sky, diagnostics
# full predicted image:
model = (obj.fullB @ r['source'].ravel()).reshape(100,100) + r['lens_amplitude']*obj.lens+r['sky']
# optional posterior marginal std at FIXED lens model / regularization:
r = obj.evaluate(log_regularization=6.8, posterior_uncertainty=True)
```

External callable is evaluated on all100x100image positions plus subpixel offsets. It must accept matching numpy arrays and return matching angular deflection arrays. Sampling is bilinear in a finite square source grid. Outside the grid, source light is ZERO, including the bilinear support crossing the edge. Pixelized source values have the same surface-brightness convention as image values (ADU/s per0.1arcsec image pixel); there is no area rescaling when changing source sampling. Supersample2 averages4ray positions before blurring. All21x21supplied PSF values retained and normalized to unit sum. Convolution is zero-padded beyond science-image boundaries; no original external blurring-region pixels available.

Mask: supplied circle intersect positiveRMS, exclude artefact_binary. Source and lens segmentation do not restrict likelihood: their diagnostic regions and counterimage holdout are additional checks. Exactly6711pixels in standard fit. Template for lens light is released convolved VIS_GALAXY_0; its amplitude is freely fit with a proper Gaussian prior. Released source image/template is NOT used. Thus this tests mass-map-to-source consistency conditional on the published lens-light morphology, not an independent lens-light analysis.

## Proper Gaussian prior / evidence

Let s be ns^2 source coefficients, a be lens amplitude minus1, b uniform sky. Prior mean0 and precision Q=blockdiag(lambda*(L.T L+.01I),4,100). L consists of unscaled horizontal/vertical first differences on every internal source-grid edge; boundary has no wrapping. Thus a~N(0,.5^2), b~N(0,.1^2 ADU^2/s^2). Source prior is proper even in constant mode due ridge. It allows negative surface brightness. The data vector subtracts unit-amplitude lens template. At fixed deflection/lambda, source+nuisance posterior is exactly Gaussian: H=D.T N^-1 D+Q; posterior mean H^-1D.TN^-1y. Source_std includes marginalization over both nuisance parameters, conditional on lens/lambda. No positivity constraint, noise inflation or fitted RMS applied.

Returned log_evidence = -.5*(chi2 + coefficient.T Q coefficient + logdetH - logdetQ + sum(log(2pi*sigma^2))). Both linear nuisance parameters are marginalized with their normalized proper priors. optimize_regularization selects maximum evidence over ln(lambda) in[-5,18]; it does NOT integrate over lambda. It is empirical Bayes, not full parameter-marginalized model evidence. Cross-resolution evidence comparisons change source priors and discretization and are a diagnostic, not literal Bayes factors. For comparing gravity models use identical sourcegrid,prior,mask,PSF,lenslight and noise; check larger grids/subsampling before interpreting differences.

## Verified benchmark

Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 and the installed fit venv. benchmark.py saves fullsource/model/residual maps, benchmark.json and counterimage_holdout.json; sie_baseline.py exposes the independent exact SIE+shear callable. It matches all102x102released deflections to vectorRMS6.25e-16arcsec (sie_deflection_check.json).

25x25,.04arcsec,1ray/pixel: chi2=3065.425, ln(lambda)=6.84324, log_evidence29543.524; source-mask chi2=298.814 (415pixels); lens amplitude1.00745. Setup+optimization .185s with single-thread BLAS. Released model on identical mask had chi2=4086.861, source-mask1150.672, so this independently reconstructed source fits substantially better under the diagonal-RMS metric.

33x33,.03arcsec,sameouterextent: chi2=3024.874, loge29553.788; runtime .381s. 25x25,.04arcsec,2x2rays:chi2=3111.194, loge29531.096;runtime .176s. Evidence is NOT converged with respect to these numerical choices. A finer sourcegrid and further supersampling/sourceregularization checks are needed if relative evidence differences are of order10or smaller.

Counterimage prediction: train excluding49pixels where source segmentation & N<-.4 &X<0, then predict them. Holdout chi2=36.374/49, mean normalized residual-.0725,std.8585. This is a real withheld-counterimage check, although some PSF leakage/nearby pixels remain in training; it is not an independent observation. It demonstrates source flexibility has not merely fitted each arc pixel independently in this baseline.

Gaussian source has ~40%negative coefficients, mostly lowbrightness/background; do not interpret those as physical emission. No positivity significance audit performed yet. Only~13%valid imagepixels raytrace inside finite sourcegrid; this is expected because the likelihood includes broad background, but finite boundary sensitivity must be checked for other deflection models. RMS correlations~.23nearest-neighbour from data_audit mean diagonal Gaussian score is a relative objective conditional on that noise approximation. Formal rejection probabilities and physical-theory claims are unwarranted from these outputs alone.

baseline.png was visually inspected: recovered mainarc and faintcounterimage with no supplied source template. Inputs untouched. Source provenance resides in inputs/fetch_provenance.json; data_audit/audit.json hashes sharedinputs. Numerical code and outputs confined to image_inversion/.
