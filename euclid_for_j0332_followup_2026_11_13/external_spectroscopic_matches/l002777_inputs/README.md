# L002777 / SILO790: source-association rescue feasibility

**Verdict: a plausible spectroscopic candidate with an observed foreground velocity dispersion, but not yet an accepted lens model or a secure image/source association.** The local [O II] shape modestly prefers a doublet, with sensitivity to sky-flagged pixels. The released Euclid model was unanimously classified as a failure. A new gravity fit must first resolve the source association, retaining the northern point that the released gate dropped.

## Inputs and identifiers

- ECLIPSE: `EUCL-DR1-L002777`, `Tile102157516RA1412954672915DEC0634238492404`.
- SILO detection 790, `SDSS J0925+6325`, coordinate match 0.047738 arcsec. SILO numeric coordinates are RA 141.295501709, Dec 63.423854828 degrees.
- SDSS `SPECOBJID=6437911172780150784`, plate 5718, MJD 56693, fiber 56. Individual spectrum RA 141.2956065954, Dec 63.4237564396 degrees. These are separately archived target-coordinate fields, not claimed identical astrometric measurements.
- [SDSS spectrum](https://data.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/5718/spec-5718-56693-0056.fits), [Euclid portal record](https://euclid-eclipse-lenses.org/files/_site/lenses/Tile102157516RA1412954672915DEC0634238492404.json), and the [SILO primary paper](https://doi.org/10.1093/mnras/stab267).

The target-only downloader retrieved 35 Euclid files with zero failed fetches, including all eight bands, noise and PSF arrays, gate metadata, released COOLEST models, and image diagnostics. Every download has a URL/time/HTTP status/byte count/SHA-256 sidecar. The original portal page HTTP-308 failure and successful redirected retry are preserved. The SILO fixed line rows and only this target's eight spectral heap arrays were retrieved by recorded HTTP byte ranges. No other full public tile was fetched here.

The complete 4622-pixel SILO `FLUX`, `IVAR`, `AND_MASK`, and `OR_MASK` arrays match the independent individual SDSS spectrum exactly. Wavelengths agree within 0.0009766 Å, consistent with float32 evaluation. SILO residual equals flux minus SILO foreground model within 4.77e-7 in native flux-density units. Thus the local quality checks use the same spectrum as the candidate detection, with SDSS `WDISP` and `SKY` supplied by the individual spectrum.

## Observed foreground constraint

The individual SDSS spectrum reports

| Field | Observed value |
|---|---:|
| Redshift | 0.32741618 ± 0.00007120 |
| ZWARNING | 0 |
| VDISP | 203.7631 ± 19.8067 km/s |
| VDISPCHI2 / VDISPDOF | 1853.6644 / 1920 |
| VDISPNPIX | 2168 |
| SN_MEDIAN_ALL | 5.0808 |

This is an observed, independent spectral constraint. It has **not** been refit with pPXF, aperture-corrected, converted to a spherical Jeans likelihood, or disentangled from rotation. The foreground light is visibly flattened. The actual `VDISP_LNL` vector has length 35; a generic documentation grid does not uniquely establish its velocity axis, so that vector was not repurposed as a likelihood. The [SDSS algorithm documentation](https://www.sdss4.org/dr16/algorithms/redshifts/) distinguishes the reported fit/curvature quantities from its template-marginalized dispersion likelihood.

This is a **2-arcsec-diameter BOSS fiber**, not a 1.5-arcsec DESI fiber ([instrument documentation](https://www.sdss4.org/instruments/boss_spectrograph/)). The exact VIS WCS maps its reported target center to west/north offsets (-0.167620, -0.311544) arcsec. Its 1-arcsec radius is drawn in [positions_and_fiber.png](audit_02/positions_and_fiber.png). The dropped northern point is outside that nominal aperture, but seeing leakage is possible; an unresolved fiber spectrum does not locate the emission spatially. The spectrum header records 13 blue and 13 red exposures, with 11701.7 seconds combined exposure in each arm. These header values do not supply a measured seeing for an aperture model.

The catalogue lists photo-z 0.41 and conditional SED log10 mass 11.3713293 with error offsets -0.0692497/+0.0698157. **The actual SED-fit input redshift is unverified.** Catalogue photo-z presence does not prove that it was used, because the ECLIPSE SED pipeline can use spectroscopy when available. No mandatory mass/distance rescaling has been applied, and no reliable new stellar-mass likelihood has been inferred from a rejected source/light decomposition.

## Background-line check

SILO reports candidate source redshift 0.97136903, spectral grade A and total grade A, using a single-line-search detection. The source redshift is a candidate interpretation, not a new secure measurement established here. No source-redshift uncertainty is supplied or invented. The fixed line table contains only one line with S/N ≥4:

| Candidate feature | Published S/N | Fit reported |
|---|---:|---|
| [O II] doublet | 6.0386 | yes |
| Hδ | 0.5889 | no |
| Hγ | 0.3806 | no |
| Hβ | 3.3163 | yes |
| [O III] 4959 | 1.9961 | no |
| [O III] 5007 | 0.3695 | no |

The published comment discusses doublet structure and secondary lines, while also discussing sky and an alternative foreground-line identification. These comments do not turn the table into confirmed multiple-line spectroscopy. The full line metadata, including asymmetric Gaussian parameter error **offsets**, are retained in [result.json](audit_02/result.json).

At this candidate redshift, the adopted vacuum [O II] wavelengths 3727.092/3729.875 Å give 7347.4737/7352.9601 Å, separated by **5.4863 Å**. The actual local SDSS `WDISP` is about 1.0117 logarithmic pixels, corresponding to Gaussian σ=1.7122 Å and **FWHM=4.0320 Å**. The doublet is partly resolved. The official [resolution definition](https://classic.sdss.org/dr6/dm/flatFiles/spPlate.php) specifies RMS width in pixels and the conversion using ln(10) λ × 0.0001.

The bounded diagnostic fits the archived SILO foreground-subtracted residual with either one Gaussian or two Gaussians at fixed candidate separation. Both have a free centroid shift, free nonnegative intrinsic velocity width, local constant and slope; the doublet has two free nonnegative fluxes. Each component is convolved with the actual local Gaussian instrumental width and integrated over the native logarithmic pixel. The centroid search is ±8 Å and intrinsic width 0–400 km/s, with nine fixed starts per fit. The results are conditional on the released foreground subtraction, effective Gaussian line-spread function, and noise model; no sky-residual stochastic model or look-elsewhere calibration is fitted.

| Half-window | Pixels, positive IVAR / AND=0 | Δχ², SILO-rescaled noise positive IVAR | Δχ², SILO-rescaled noise AND=0 |
|---|---:|---:|---:|
| 20 Å | 23 / 18 | 4.8806 | 1.4655 |
| 30 Å | 35 / 28 | **5.3321** | 4.4221 |
| 40 Å | 47 / 37 | 5.7373 | 4.7130 |

Here Δχ²=χ²(single)−χ²(doublet), **a descriptive fit improvement, not a calibrated detection significance or Bayes factor**. The primary 30-Å case has χ²=27.1217 for the five-parameter single model and 21.7896 for the six-parameter doublet over the same 35 pixels. Original SDSS IVAR gives 1.9831–6.5520 over the same mask/window controls. Across all integrated fits the improvement is 1.4655–6.5520. A point-sampled response gives 5.5165 for the primary window, so pixel integration does not decide the interpretation. Every doublet fit reaches effectively zero intrinsic width; the line components are instrument-limited in this diagnostic. The two positive component fluxes are similar. The published same-21-pixel-window single/doublet fits separately imply Δχ²=6.1257, consistent with a modest shape preference, though their fitting convention differs.

The [spectrum window figure](audit_02/spectrum_windows.png) shows residuals, rescaled error bars, actual sky flux, and nonzero AND masks at [O II], Hβ and both [O III] lines. Full numerical windows are saved as CSV files. Within ±10 Å of the [O II] midpoint, **3/11 pixels have AND-BRIGHTSKY** and 7/11 have OR-BRIGHTSKY; the central sky range is 5.92–45.73 in the native flux-density units. The [O II] core has no AND-BADSKYCHI flag. Hβ's core has no nonzero AND flags but only weak published S/N. [O III] 5007 lies near strong sky, with core sky up to 161.6 and several pixels receiving zero rescaled weight. It cannot currently provide strong independent confirmation.

The [official DR16 quality rules](https://www.sdss4.org/dr16/spectro/quality/) define IVAR=0 as unusable and AND/OR masks as flags in all/any exposures. The [DR16 SPPIXMASK table](https://www.sdss4.org/dr16/algorithms/bitmasks/) identifies bits 19,23,25 as PARTIALREJECT, BRIGHTSKY, COMBINEREJ. OR flags are preserved, not used to discard the entire window. A positive-IVAR fit and a more conservative AND=0 sensitivity are both reported.

## Actual released modeling status and image associations

The portal records imaging grade A and completed VIS light, VIS pixelized and Sérsic runs, all eight bands available, and zero metadata errors. **All four inspection votes classify the model as Failure, with zero success votes.** Completion of the code is not approval of the model. The released record contains no specific reviewer explanation of the cause; no official cause is inferred here.

The source-position metadata originally had four candidate points. It retained pipeline `(south,west)` positions (0.65,-0.15), (-0.25,-1.05), (0.05,0.65), and dropped index 0 at (-1.35,+0.55), recorded reason `outlier_J`. In sky `(west,north)` convention the dropped point is **(+0.55,+1.35) arcsec**. It is preserved explicitly in the result and figure. The gate reports `s_min_all=0.446`, `s_final=0.0132`, threshold 0.3 arcsec, and `status=drop`; the same `.3` threshold was not satisfied by the original association. Gate definitions and source identities remain pipeline assumptions, not independent extra data.

The rejected Sérsic and pixelized models disagree: COOLEST SIE θE≈0.97124 versus 0.63791 arcsec, respectively, with substantial shear ≈0.217/0.216. The Sérsic stage assigns source effective radius ≈6.84 arcsec. The catalogue effective Einstein-radius summary ≈0.65093 arcsec is also a product of the rejected solution. **None of these radii is used as an accepted lensing constraint.** The COOLEST entity redshifts 0.5/1.0 are export/model placeholders here, not the SILO observed foreground/background pair.

The raw images show a flattened central light distribution and a separate northern blue structure; the retained positions lie close to central features while the northern point was removed. The existing model diagnostics show structured residuals. This motivates testing competing source associations and a more flexible foreground-light decomposition, but does not establish why the reviewers rejected the solution or which structure emits [O II]. A useful next rescue experiment would keep both the released three-point association and alternatives involving the dropped blue structure as explicit competing hypotheses, with matched image masks/source priors and the actual band PSFs. It should establish image correspondences before combining the candidate redshift, observed dispersion, and SED information into a gravity test. Rotation/flattening will matter if dynamics becomes load-bearing.

All 10000 pixels in each band have finite data and positive finite noise. Native PSF sums range from 0.8759 (Pan-STARRS I) to 0.9993 (MegaCam R); VIS is 0.95346. Future convolutions need explicit PSF normalization and support controls. No convolution or image fit was performed in this audit.

## Audit and reproducibility

The authoritative new run is [audit_02/manifest.json](audit_02/manifest.json), status **completed**, validated against current inputs using the computation-audit v2 validator. The contract is [audit_contract_v2.json](audit_contract_v2.json), code [inspect_target_v2.py](inspect_target_v2.py), and complete result [audit_02/result.json](audit_02/result.json). The manifest contains the actual bounded command, input/output hashes, versions, time and Git state. The command used a 180-second wall-clock bound, one requested numerical thread, 13 model comparisons and no random sampling. Scalar adaptive integration independently agrees with the Gaussian pixel integral to 1.81e-14; noiseless doublet recovery gives maximum parameter error 2.12e-13. These checks validate the local numerical construction, not the astrophysical source identity.

The first attempt [audit_01/manifest.json](audit_01/manifest.json) is preserved as **failed**: computation reached the report-writing stage, where the serialization helper rejected native Python strings. The corrected script adds native scalar passthrough, tested against that exact failure; neither prior script nor failed outputs were overwritten. No physical-model or fit-setting change was made between runs.

Outcome: **finite implementation and metadata checks verified within the stated range; astrophysical interpretation conditional and source association unresolved.** There is no theory exclusion, confirmed lens rescue, precise background-redshift uncertainty, or new stellar-mass result from this audit.
