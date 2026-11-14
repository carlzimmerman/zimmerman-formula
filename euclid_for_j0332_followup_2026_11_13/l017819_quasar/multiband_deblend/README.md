# L017819 nine-band deblend: released SED mass is not a reusable precise prior

Research resumed after explicit user authorization; PAUSED_HANDOFF.md remains historical. All work here is conditional photometry, **not a new stellar-mass/IMF/SED fit**.

## Evidentiary result

Actual nine-band fits were completed for BOTH existing SIE/light fixtures (host_control/run_04 chosen primary; run_03 chosen sensitivity). Each band has independent foreground, quasarA, quasarB and extendedhost fluxes; no quasarfluxratio or time-delay constraint. All Gaussian foreground/quasar amplitudes were positive. Host addition lowers image residuals substantially versus matched same-shape point-only controls. Nevertheless source-negativity, registration sensitivity and foregroundprofile dependence prevent treating these fluxes as a validated replacement SED or reusing the old SED mass as an independent precise constraint.

Ratios of model foreground finite-aperture flux to released catalogue lens_flux:

| Band | Primary Gaussian | Primary nonnegativehost MAP | Sensitivity Gaussian | Sensitivity nonnegativehost MAP |
|---|---:|---:|---:|---:|
| VIS | .961 | .957 | .921 | .917 |
| Y | .910 | .903 | .872 | .868 |
| J | .904 | .897 | .868 | .863 |
| H | .845 | .888 | .820 | .855 |
| HSCg | 1.201 | .778 | 1.036 | .748 |
| HSCr | .861 | .861 | .825 | .825 |
| HSCr2 | .924 | .920 | .885 | .882 |
| HSCi2 | .913 | .941 | .888 | .901 |
| HSCz | .856 | .920 | .827 | .882 |

These are discrete conditional fixtures, NOT confidence intervals. Raw exact fluxes, nativecalibration, all offset alternatives and matched point-only controls are in run_01/result.json; summary_01/flux_summary.csv is the compact audited comparison.

Gaussian g/i2/z host reconstructions contain9–18 nodes below−3 conditional standarddeviations in several cases. Nonnegativehost/lens/quasar convexMAP controls ALL converged, at frozenGaussian sourceprecision/geometry/offset. Enforcing positivity changes primaryg foreground by−35.3% relative to Gaussian and increasesχ² by12615; sensitivityg similarly changes−27.8%. For i2/z the positivityχ² increases~5500–5900, H~1250–1400. These are model-sensitivity diagnostics, not calibrated physical rejection significances. Positivitycontrols are MAPs, not positive-source marginal evidence, and do not reoptimize sourceprecision. They demonstrate that the flexible signedhost was absorbing substantial residual structure. A positivity-constrained fitted flux alone is not thereby scientifically accepted.

The old catalogue likely remains useful as a historical conditional photometric estimate, but its tiny formal errors cannot be carried through unchanged as an independent mass prior after changing host/quasar decomposition. No numerical newmass or massrescaling is inferred from these flux ratios: stellarM/L and colors change together, and the present model is not validated sufficiently for a newSED.

## Calibration and exact aperture

All nineactual BGSUB/RMS/PSF HDUs were used: VIS,Y/J/H,HSCg/r/r2/i2/z. Data AND RMS converted before priors with f_microJy=10^((23.9−MAGZERO)/2.5). NativeMAGZERO/BUNIT: VIS24.4 ADU/s; Y29.8,J30.1,H30.0 ELECTRON/s; HSC30.0 DN/pixel. Priors therefore have the same physical µJy scale instead of inadvertently suppressing highnativecount NIR fluxes.

PSFs retain full suppliedsupport, normalized by measuredfinite sums:21×21VIS,45×45NIR,47×47HSC. Finite sums range.9471–1.0032; unmeasured outsidewings remain systematic uncertainty. Pointtemplates use same empiricalPSFs, cubicsubpixel interpolation and fullcutoutnormalization. Sérsic pixelintegration uses the existing cusp-aware Renderer.

Reported foreground flux is **unconvolved** unit-total Sérsic summed through ORIGINALcatalogue circle+actual100×100cutout: radius6.003894862arcsec, centerSouth+.15/West−.15;9495selectedpixels. It is NOT the2778pixel3arcsec likelihoodmask or a pointsource+host sum. Primary zerooffset aperturefraction.85583393; sensitivity.89414659. Extrapolated infiniteprofile light remains a modelassumption. ReleasedprePSF lens maps summed in the SAMEaperture and converted usingactualMAGZERO reproduce catalogueflux to~1 (VIS.9991), verifying unit/aperture consistency. Catalogue flux and max_lh are both retained. Artifactmask affects likelihood, not the aperture definition of the unconvolved smoothlens.

## Registration information

All9nativeimageheaders have identicalWCS(CRPIX[7150,−5857],CRVAL[230.9152442,44]). Mapping the twoVISquasarpositions tosky and into eachband returns samepixels within7.1e−10pixel. Localarraycenter49.5 is NOT worldCRVAL or the separate results/wcs_vis_lp.json origin. Headernominalregistration is zero; this does not prove empiricalPSFs/centroids are registered perfectly.

Eachband tested zero plus both signs of the releasedglobaloffset transformed fromSouth/West toNorth/West. Most preferzero; primaryY/g preferonecataloguesign. This is a discrete sensitivity, not a proved physicalsign or an empiricalastrometricposterior. Primary foregroundratio ranges over these offsets are: Y.897–.910,J.862–.911,H.780–.877,g1.152–1.201,r.752–.986,r2.803–.985,i2.910–.914,z.837–.866. No tinycataloguecentroiderrors were treated as completeuncertainty. Free perbandPSF/centroid fitting may materially change centraldeblend.

## Operator, prior and controls

Code deblend.py independently builds a continuouszero-paddedbilinear21×21sourcebasis(h=.06arcsec,2×2image rays). FullnativePSF convolution of eachbasis uses FFT over imageaxes, avoiding an assumed21×21kernel forNIR/groundimages. Independent generalizedoperator agrees with existing VISreference within1.39e−16. Field is fixedstandardSIE+the exacttwo-point shear solution, and sourcegridcenter followsmappedquasar; nofourpointgate imposed. Physicalsourceidentity, geometry and inferredstellarprofile remain conditional on thisSIEdeblend.

Source priorprecision λ(LᵀL+.01I), λ profiled over lnλ∈[−12,18] separately perband. Independent properGaussian lens/A/B amplitudes sigma10000µJy, sky sigma10µJy/pixel. No sourcecolorprior; no microlensing/variability fluxratio restriction. Linear Gaussianposterior and properpriordeterminants computed by Cholesky. Image noise normalization constant for matchedsame-bandmask is omitted fromscores. Gaussian source can be signed; actualsourceedge/negative diagnostics retained. DiagonalRMS does not describe a calibrated fullcovariance, so no formal goodness-of-fit probability or gravityBayesfactor is claimed.

## Reproduction and terminal state

run_01:18Gaussianfits, completed6.20s; positive_01:18nonnegativeMAPcontrols, completed6.93s; summary_01:WCS/aggregation completed. All run.status=completed and v2manifests validated withcurrentinput/outputhashes. Exactargv in launch.json, positive_launch.json, summary_launch.json and manifest execution records. One numerical-library thread. All launchhandles terminal:51623,37675,51492; no activejob remains for thisroute. Rawinputs and sharedhostoperator were not modified.

Smallest useful next model: jointly refit registration/quasarPSFsystematics, nonnegativehost and foregroundflexibility in highresolutionVIS/NIR, then propagate intooptical bands and quantify deblend/colorcovariance beforeSED. A matchedphysicalfield comparison may use the sameoperator as a conditionaldiagnostic, but should not claim an independent tightstellarprior fromthisSIE-conditioned extraction.
