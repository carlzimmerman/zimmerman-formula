# L017819 standard-SIE extended-host photometric control

This is an actual VIS image fit using released PSF/RMS/artifact mask, a Sérsic foreground, two independent quasarPSFs and a continuous bilinear pixelized common host source. It is NOT a stellar-mass or gravity-theory fit. Inputs remain read-only.

## Model and API

`fit_host_v3.py::Host.run(p)` and refined `fit_host_v4.py::Host.run(p)` accept p=[lnRe_major,lnn,q_light,phi_light,thetaE,q_mass,phi_mass,ln_source_precision]. Lenslight center fixed to precedingVISpoint fit; masscenter fixed to releasedCOOLEST. Quasar coordinates fixed at new photometric valuesA(.48981745,−.13692158),B(−1.13191305,+.65957510). No fourpointgate or fluxratio/timedelay constraint. Two shearcomponents are solved exactly from the two-point common-source equation for each SIE, then sourcegrid is centered at that mappedquasar. This uses the twoimage shear degeneracy explicitly: no mass information comes from the two positions alone. Extendedhost pixels can add information conditional on its sourceprior and foregroundmodel.

SIE is the existing analytic sqrt(q)-normalized implementation. Source interpolation has independent perneighbor zero padding, avoiding the old hard sourcewindow discontinuity. Full supplied21x21 normalized VIS PSF convolution acts on both host and lens. Fixed3arcsec circular likelihood mask centered(−.15,+.05), excluding releasedartifact pixels;2778pixels match precedingpoint-onlyfit. Foregroundlight Renderer is pixelintegrated with cusp quadrature and paddedconvolution.

For source s, priorprecision exp(lnlambda)*(LᵀL+.01I), where L firstdifferences on sourcegrid edges. Nuisance lensflux/Aflux/Bflux independent zero-mean Gaussian sigma10000nativeintegratedunits, sky sigma10nativeunits/pixel. Linear posterior/evidence obtained by Cholesky Gaussian elimination; source and nuisance amplitudes are signed, NOT a positivity-constrainedphysicalposterior. Properprior determinants retained; image-noise normalization omitted only because it is constant across same-mask parameterfits. Scores across source discretizations are conditional on different discrete priors and must not be sold as representation-independentBayesfactors. No shear prior imposed;zeroκ.

## Runs and validation

run_01:14iteration L-BFGS pilot, both hitcap; preserved, NOTconverged.
run_02:100iteration L-BFGS continuation, both line-searchfailure; preserved, NOTconverged. Continuous bilinear basis derivative kinks make derivativeoptimizer unreliable here.
run_03:Powell continuation from both recordedstarts; both reportconvergence. χ²4264.23/4247.24 versus point-only32147.33, same2778pixels. Regeom.83137/.80329arcsec,n5.0666/4.9482, compared point-onlyRe1.764,n6.124. Shear.0943/.0321 differs. This shows large omittedhostbias and multiplebranch/sourceprior sensitivity; not a unique lenssolution. Positive fittedlens/quasarcoefficients at thesefits do not establish everyhostsourcepixelpositive.
run_04:refined21²h.06arcsec source and2x2image rayquadrature, same two-startPowell. See result.json and final checkpoint below when completed.

validation_01 independently checks q→1SISlimit error1.73e−8arcsec and sparsePSF convolution versus independentFFT difference1.89e−15. Same-forward fixedgeometry positivehost syntheticcase recoversχ²1.95e−6 with tinyimposednoise; this is a bookkeepingcontrol, NOT independentnonlinearparameterrecovery or PSFmismatch validation. Sourceprecision/sampling checks show substantial residual changes at fixedgeometry, so a singlecoarsegrid optimum is insufficient. All completedruns havecontracts, exactargv, source/input/outputhashes and v2manifests; validation_01 andrun_03 validated successfully.

## Scientific limitations and next discriminator

A Gaussian source can absorb foregroundmodel residuals; sourceedges carry nonzeroflux and sourcecoverage sensitivity must be inspected. A usefulhostfit is not a calibrated goodness-of-fit probability. DiagonalRMS, fixedquasarpositions/PSFs, fixedcenters, singleSérsic, no hostcolorgradient or foregroundmulticomponent model remain strong assumptions. PointsourcePSF/residual contamination can affect centralhost. Published222.26±15km/s is independent conditional spectroscopy, but thiscontrol has NOT yet predicted the nativefiber dispersion.

Before a precise stellarSED prior, propagatehost intoNIR/optical photometricdeblending, testpositivehost/foregroundflexibility, and compare sourcecoverage/refinement. Then test whether a physical field/dynamics prediction fitsresolvedhost+fiberkinematics with consistenttracer/seeing/anisotropy; do not infer a0 or physicalmass from thisSIE control.

## Final bounded checkpoint: refinement exposes uncertainty

run_04 completed94.54s, bothPowellstartsconverged, but the two refined solutions differ substantially. Start1:chi²5141.01,Regeom1.17471,n6.26907,q.579839,PA53.55553°,shear.29874. Start2(selectedconditionalhigher-score):chi²5061.73,Regeom.958880,n5.52493,q.569735,PA54.56245°,shear.0255112. This differs from coarsechosenRe.803292,n4.94823. Thus refinement does NOT establish a stable precise foregroundshape. It does establish that omittinghost severely biases the originalpoint-onlyfit. Residualstructures remain near central/quasarfeatures. Gaussian source has42.6%negative nodes, often lowamplitude, and12.6%absolute sourceflux atboundary; no physicalpositive-source posterior or sourcecoverageconvergence is claimed. Smallerh.045 atsame21² changeschi² to5123.01 atfixednonlinears andsameprecision; varyinglnprecision±2 changeschi² to4631.76/5494.32. These are sensitivities, not independently reoptimizedglobalresults.

Frozen operator: `arbitrary_field_adapter.py::FieldAdapter(light_parameters,ns=21,step=.06,supersample=2).evaluate(deflection,log_regularization,return_arrays=True)`.
`light_parameters=[cx,cn,lnRe_major,lnn,q,phi_west_radians]`. The callable must return PURE **already source-distance-reduced** deflection in west/northarcsec, with noexternal shear/convergence. Adapteradds exacttwoquasarpoint shear and recomputes sourcecenter/grid for eachfield. It profilesidenticalsource/lensflux/twoquasarflux/sky Gaussianpriors. `candidate_foreground.json` gives exactfixedshape/centers/positions andcodehashes, explicitly only an SIE-deblend-dependent candidate, NOT an independent stellarphotometryprior. Sourceprecision must be reoptimized consistently for a matchedfieldcomparison.

adapter_validation_01 checks the arbitrarycallableSIE against originalHost onactualdata; modeldifference0 andscoredifference0 atsameparameters, v2manifestcompletedvalidated. run_04 manifestalso validates. No furtherexpansive fits performed; root can now match physicalfield andSIE throughsameoperator while keepinglightshape branches andsourcegriddependence explicit.
