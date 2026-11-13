# Three alternatives to L002777: target-only observational audit

**L015442 is the strongest new source-spectroscopy follow-up, but none of these objects is currently ready for a defensible combined stellar-mass/lensing/dynamics test.** L015442 has two actual candidate emission features with published S/N above six, an observed foreground dispersion with about 11% formal error, and relatively clean local sky/flags. Its released 100×100 image is morphologically ambiguous and its Euclid grade is C. L001244 and L013442 have potentially useful arc configurations, but their source spectra are single-line candidates and their low-S/N foreground dispersions require special caution. No secure paired-redshift lens or new gravity result is claimed.

## Ranked next actions

| Priority among these alternatives | Object | Best available evidence | Limitation and useful next action |
|---|---|---|---|
| 1 | **L015442 / SILO310** | [O II] S/N 8.93 plus [O III] 5007 S/N 6.10; reported stellar dispersion 171.71±19.26 km/s | Strongest reason to obtain raw Euclid cutouts and test image associations. The central light is visibly flattened, with a northern blue structure; the released JPEG does not establish repeated images. Build a mass/light model only after a credible association is found; include disk/rotation possibilities. |
| 2 | **L001244 / SILO312** | Euclid grade A; blue features on opposite sides of the central galaxy; [O II]-candidate S/N 8.86 | Three of four reviewers rejected the released model. The doublet is not decisively resolved, and foreground S/N is low. A limited source/light-model rescue could be useful, but there is no released SED mass in the screen and the observed dispersion is not a robust joint-test shortcut. |
| 3 | **L013442 / SILO309** | Blue arc-like structures around an extended foreground; [O II]-candidate S/N 7.28 | Essentially no doublet-shape discrimination, no strong secondary line, low-S/N dispersion, mixed inspection votes and a dropped image point. Lower priority until spectroscopy or correspondence improves; a multiple-galaxy/light model may be needed. |

Relative to **L002777**, L015442 clearly outranks it in the available secondary-line evidence: L002777 has [O II] S/N 6.04 and Hβ only 3.32, while L015442 has [O II] and [O III] both above six. It does **not** yet outrank L002777 in complete joint-fit readiness, because it lacks an accepted image association, released A/B model dataset and catalogue SED mass. L001244 and L013442 do not establish an overall advantage over L002777. The efficient next discriminator is a bounded L015442 image-association/raw-data feasibility check, not an immediate AQUAL fit. These objects were already associated with Talbot et al. 2021 in the Euclid object catalogue; this is an evidence audit, not a new lens discovery.

## Observed target spectroscopy

All three individual spectra are from BOSS plate 4420, MJD 55883, with **2-arcsec-diameter fibers**. The public [SDSS files](https://data.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/4420/) and targeted SILO arrays are saved under each ID with URL/time/status/hash provenance. The complete SILO `FLUX` arrays match the individual SDSS spectra exactly; wavelength and foreground-residual identities also pass the registered checks. The original SDSS `WDISP`, `SKY`, `AND_MASK`, `OR_MASK` and IVAR are used alongside SILO's rescaled IVAR and foreground-subtracted residual.

| Object | Fiber | Foreground z ± reported error | Candidate source z | Reported VDISP ± error (km/s) | SN_MEDIAN_ALL |
|---|---:|---:|---:|---:|---:|
| L015442 | 349 | 0.34340858 ± 0.00008233 | 0.81204009 | **171.7055 ± 19.2569** | 4.7943 |
| L001244 | 795 | 0.52200192 ± 0.00033281 | 1.42531312 | 157.8716 ± 46.8968 | 2.1203 |
| L013442 | 335 | 0.57596439 ± 0.00024684 | 1.36356688 | 352.5505 ± 80.4284 | 1.6716 |

All foreground `ZWARNING=0`; this validates neither the background-line identity nor lensing. The source values are SILO candidate redshifts; no source-redshift errors are supplied or invented. The small differences between original SDSS and SILO foreground redshift values are retained explicitly in [result.json](run_01/result.json).

VDISP is an **observed pipeline measurement**, not a new pPXF fit, aperture-corrected dispersion, spherical Jeans constraint, or rotation-corrected measurement. The [SDSS caveats](https://www.sdss4.org/dr16/spectro/caveats/) advise against dispersions for spectra with median per-pixel S/N² below 10, and state that their dispersions have no standard aperture correction. The low reported continuum S/N of L001244/L013442 therefore materially weakens their dynamical usefulness; the quoted formal errors alone are not a reliability certificate. No velocity-likelihood grid was inferred from an undocumented vector axis.

## Actual emission-line evidence and local quality

Published S/N values are read directly from all **14 fixed line-table rows** for these three candidates, including the repeated single-Gaussian [O II] row. They are not inferred from inspection grades. Here OIIIa is 5007 and OIIIb is 4959; HId/HIc/HIb denote Hδ/Hγ/Hβ.

| Object | [O II] | Hδ | Hγ | Hβ | [O III] 4959 | [O III] 5007 |
|---|---:|---:|---:|---:|---:|---:|
| L015442 | **8.9262** | 0 | 1.9498 | 0 | 2.5501 | **6.1048** |
| L001244 | **8.8591** | 0 | outside listed range | outside listed range | outside listed range | outside listed range |
| L013442 | **7.2848** | 0.2140 | 1.6160 | outside listed range | outside listed range | outside listed range |

Zero S/N is not automatically a physical non-detection. In particular, the entire inspected ±30 Å Hβ window for L015442 has **zero SILO rescaled IVAR**, despite positive original SDSS IVAR. It supplies no usable SILO Hβ constraint. The missing weight has not been guessed away or reinterpreted as a line-ratio exclusion. All raw window values are saved as CSV files.

For each [O II] candidate, a single and a double Gaussian were fitted to the *same* pixels with the actual local Gaussian instrumental resolution. Vacuum doublet separation is fixed by the candidate z, component fluxes are nonnegative, centroid shift is bounded ±8 Å, intrinsic velocity width 0–400 km/s, and a constant plus slope is fitted. Native log pixels are integrated. Four controls per candidate use half-widths 20/30 Å and positive-IVAR versus AND=0 masks, with nine fixed starts for each fit. These are **descriptive χ² comparisons, not calibrated significance, model probabilities or source confirmations**; foreground subtraction and coadd covariance remain conditional.

| Object | Doublet separation | Local instrument FWHM | Range of Δχ²(single−doublet) over four controls |
|---|---:|---:|---:|
| L015442 | 5.0429 Å | 3.4395 Å | **0.8114–0.9094** |
| L001244 | 6.7496 Å | 3.7101 Å | **1.0532–1.7701** |
| L013442 | 6.5778 Å | 3.9407 Å | **0.0105–0.2427** |

None has a decisive [O II] doublet-shape preference in this diagnostic. L015442's advantage comes from its **second actual line**, not from a claimed resolved doublet. L013442's published fixed single-Gaussian fit is slightly better than its fixed doublet fit; our more flexible local versions are nearly indistinguishable.

**L015442:** [O II] near 6756 Å has all 13 core pixels (±10 Å) at positive rescaled IVAR, no AND or OR quality flags among the documented bits, and core sky only 2.66–2.90 in native flux-density units. [O III] 5007 near 9075 Å has 9/10 positive-weight core pixels, no listed AND/OR flags, and sky 2.11–3.52. The weaker 4959 feature has two core AND-BRIGHTSKY pixels and S/N 2.55. The 5007 feature is visible in the actual residual, rather than being merely a grade label. However, the SILO inspection comment warns that detections at this feature's foreground-rest-frame location are more frequent than the local median. This possible contamination/background-model concern remains unresolved; no line-identification certainty or spatial source association is manufactured from clean flags alone. [Spectrum figure](run_01/EUCL-DR1-L015442/spectrum_windows.png).

**L001244:** [O II] near 9043 Å has all nine core pixels at positive rescaled IVAR, but four have AND-BRIGHTSKY and seven OR-BRIGHTSKY, with sky up to 23.59. Hδ near 9951 Å has only one of eight core pixels with nonzero SILO weight, and all eight have AND-BRIGHTSKY. The published comment says the doublet feature appears in individual exposures; this audit inspected the coadd and does not independently confirm that statement. [Spectrum figure](run_01/EUCL-DR1-L001244/spectrum_windows.png).

**L013442:** [O II] near 8813 Å has seven of nine positive rescaled-IVAR core pixels, no AND-BRIGHTSKY, and sky 2.12–4.19. The emission exists as a broad feature, but its line identity lacks doublet or secondary-line discrimination. Strong sky/residual structure appears immediately to the red. Hδ/Hγ are weak. [Spectrum figure](run_01/EUCL-DR1-L013442/spectrum_windows.png).

The [official mask definitions](https://www.sdss4.org/dr16/algorithms/bitmasks/) and [quality rules](https://www.sdss4.org/dr16/spectro/quality/) distinguish AND flags present in all exposures from OR flags present in any exposure. OR flags were preserved, not used to erase otherwise usable windows. Correlated coadd errors and possible sky/model residuals preclude a formal source-confirmation probability here.

## Euclid status and morphology

The [primary data-release description](https://zenodo.org/records/19654904) states that the 15072 A/B systems were automatically modelled and given SED fits, while colour images are released for all 26662 A/B/C/X objects. **L015442 is grade C and was not part of that automatic modelling population.** Its target portal JSON returns 404; that is not evidence of a failed completed model. It has expert score 0.62365 and individual grades B,B,A,A,C,X,X,B,C,C. Its [exact released JPEG](run_01/8542_EUCL-DR1-L015442.jpg) shows an elongated/flattened foreground with asymmetric blue structures and a northern blue object; the small colour cutout does not establish a clean multiple-image configuration. No model/SED mass exists in the screened A/B release for this object. The raw multi-band Euclid images would be the next useful data, before constructing a costly physical fit.

**L001244** has grade A, all four Euclid bands completed, zero metadata errors, and inspection votes **success 1, failure 3: Failure consensus**. Its [RGB](EUCL-DR1-L001244/results/rgb.png) shows faint blue features around the central galaxy and nearby sources. The [pixelized diagnostic](EUCL-DR1-L001244/results/vis_pix_fit.png) reconstructs opposed features but does not override the rejection. Two source points were kept: pipeline `(south,west)` = (-0.05,-0.95), (0.35,+0.65), no drops, gate 0.3 arcsec. A two-point gate is weak correspondence information. A carefully matched light/source reassessment could be useful, but no official causal explanation of failure is recorded and no released mass is accepted here.

**L013442** has grade B, all four Euclid bands completed, zero metadata errors, and votes **success 1, failure 2, multi-galaxy 1: No Consensus**. Its [RGB](EUCL-DR1-L013442/results/rgb.png) and [fit diagnostic](EUCL-DR1-L013442/results/vis_pix_fit.png) show a bright foreground with two blue arc-like structures, central residuals and neighboring light. Originally three candidate points were proposed; the gate retained `(south,west)`=(-0.55,-0.95),(+0.05,+2.05) and dropped index 2 at (+0.15,+0.65), recorded reason `outlier_geom_inner`. The dropped point, equivalent to sky `(west,north)`=(+0.65,-0.15) arcsec, is preserved in the result. Original reported source separation was 0.9412 arcsec, versus a 0.3-arcsec gate; the retained pair fits to zero reported separation. This is a pipeline selection condition, not evidence that the third structure is unrelated. Competing associations and additional foreground components would need explicit tests.

COOLEST point values, including their placeholder redshifts, are retained for provenance only. No rejected/no-consensus Einstein radius is promoted to an observational constraint. There is no verified SED-fit input redshift or new stellar mass for these alternatives; no distance-only mass correction is applied.

## Provenance, bounds and result

- [Contract](contract.json), [audit code](audit_spectra.py), [complete result](run_01/result.json), [bounded v2 manifest](run_01/manifest.json).
- The run completed and the manifest validates against all **91 declared code/data/provenance inputs**. It covers exactly three targets, all 14 line rows, 12 local model comparisons and three image members. No full AQUAL, pPXF or stellar-population fit was performed.
- Twenty of the 21 first-stage requests succeeded; the sole 404 was the expected missing grade-C model-portal record. Sixteen A/B diagnostic/metadata requests succeeded.
- The 672784933-byte colour-image archive was not downloaded. A 65558-byte tail and 2479898-byte central directory located the three entries. Only their approximately 70 kB of member ranges were fetched. The audit verifies each native ZIP filename, compression method, size and CRC32 before extraction, and records SHA-256 hashes. The directory contains 26667 entries (26662 image objects plus directory entries); the count is not silently treated as 26667 objects.
- Shared SILO fixed metadata, line-table inputs, parsing conventions and primary paper are already authenticated in the parent crossmatch audit. The local Gaussian kernel/pixel-integration code is the same pinned implementation independently checked in the prior L002777 numerical audit. All new target residual/flux/width/flag arrays and local optimizer results are saved.
- Visual inspection covered each released colour image and the A/B pixelized-fit diagnostics; images are descriptive evidence, not an independent likelihood or formal proof of lensing.

Outcome: **finite parsing and local-comparison checks verified; L015442 is a stronger multi-line background candidate, while lensing and image-source correspondence remain unresolved.** The existing Lean algebraic identities cannot certify these observational identities or candidate classifications.
