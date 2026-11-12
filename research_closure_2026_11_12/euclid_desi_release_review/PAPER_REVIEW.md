# Review of all 26 DR1-Foundation manuscripts

Scope: the 26 manuscripts under the November 2026 heading of the [official Euclid publication index](https://pubs.euclid-ec.org/public/), retrieved on 12 November. This is a targeted full-text review of relevant methods, products, validation and limitations, not a line-by-line audit or an assertion of peer-review completion. Page references below record the actual reading scope. No PDF or extracted full text is redistributed. Source SHA-256 hashes are in [paper_inventory.json](paper_inventory.json).

## 1. Aussel et al.: Euclid Data Release 1 (DR1). Data release overview

[Manuscript](https://pubs.euclid-ec.org/public/dr1/aussel.pdf) — reviewed pp. 1–6, 8–10; sections 2.4, 3.5–3.8, Table 5

Defines Foundation versus full DR1, explains the VIS PSF issue behind the staggered release, and identifies the PHZ and mask products that are available now. Full shear/correlation/cosmology products follow in June 2027. Areas differ by instrument, processing and masking; a headline sky area is not an effective sample area. Release overview is not a cosmological measurement or an acceleration-law test. Do not infer validated shear from morphological ellipticities.

## 2. Tereno et al.: Euclid Data Release 1 (DR1). The Euclid surveys at DR1

[Manuscript](https://pubs.euclid-ec.org/public/dr1/tereno.pdf) — reviewed pp. 1, 10–13, 18–23; survey/field definitions and Table 6

Defines Wide, Deep, auxiliary and calibration fields with differing depth and usable product coverage. COSMOS and the deeper fields are promising intersections with existing ancillary observations, but field membership is not guaranteed complete multiband or spectroscopic coverage. Raw observed area, validated area and quality-masked area are different. Actual object-level overlap with repo samples has not been computed.

## 3. Ruffenach et al.: Euclid Data Release 1 (DR1). An overview of the Science Ground Segment architecture and operations

[Manuscript](https://pubs.euclid-ec.org/public/dr1/ruffenach.pdf) — reviewed pp. 1–4, 7–8, 12–14; archive provenance and release validation

Describes the Science Ground Segment and archive lineage linking exposures, calibrations, images and catalogues. The Science Archive and Data Space expose validated products through discovery/retrieval services. Pipeline validation does not establish that every downstream gravity-analysis sample or derived likelihood is calibrated.

## 4. McCracken: Euclid Data Release 1 (DR1). VIS processing and data products

[Manuscript](https://pubs.euclid-ec.org/public/dr1/mccracken.pdf) — reviewed Targeted review: PDF pages 1–3, 11–12; not a line-by-line full-paper audit.

Calibrated VIS frames and stacks support galaxy and lens imaging. Catalogue PSF-fitting photometry has a quadrant-normalization problem; distortion residuals and flagged observations require quality control. Calibrated-frame MAG_MODEL values require caution; astrometric caveats apply to particular skypatches.

## 5. Polenta: Euclid Data Release 1 (DR1). Near-infrared processing and data products

[Manuscript](https://pubs.euclid-ec.org/public/dr1/polenta.pdf) — reviewed Targeted review: PDF pages 1, 8–11; not a line-by-line full-paper audit.

DR1 contains 71,659 calibrated near-infrared images. Relative photometry is generally accurate, but persistence, detector backgrounds and bright-star artifacts remain relevant to faint-galaxy applications. Persistence masking can be excessive; residual stripes, diffuse structures and bright-star arcs remain.

## 6. Radovich: Euclid Data Release 1 (DR1). NIR astrometric calibration

[Manuscript](https://pubs.euclid-ec.org/public/dr1/radovich.pdf) — reviewed Targeted review: PDF pages 1, 9–11; not a line-by-line full-paper audit.

Typical astrometric precision is about 10 mas, with 99% of dithers below 20 mas. Persistence-related failures affect a small area and are characterized through quality maps. Approximately 3% of the area has degraded astrometry from persistence-related failures.

## 7. da Silva: Euclid Data Release 1 (DR1). NISP-P point-spread function modelling pipelines

[Manuscript](https://pubs.euclid-ec.org/public/dr1/dasilva.pdf) — reviewed Targeted review: PDF pages 1, 7, 13–14; not a line-by-line full-paper audit.

NISP PSF models improve photometric and structural inference. Residual PSF-fitting magnitude offsets require post-processing correction; within-detector and chromatic PSF refinements remain future work. Models are constant within each detector; PSF-fitting photometry retains offsets.

## 8. Fumana: Euclid Data Release 1 (DR1). SIR spectroscopic calibration

[Manuscript](https://pubs.euclid-ec.org/public/dr1/fumana.pdf) — reviewed Targeted review: PDF pages 1–2, 10–11; not a line-by-line full-paper audit.

Spectroscopic calibration supports reliable wavelengths and line fluxes; validation finds flux variations around 0.7%. Slitless observations mix spatial morphology with spectral information, while extraction and wavelength-model refinements remain planned. Overlapping spectra, morphology-dependent resolution, background and grism-positioning effects matter.

## 9. Kubik: Euclid Data Release 1 (DR1). Persistence in NISP detectors

[Manuscript](https://pubs.euclid-ec.org/public/dr1/kubik.pdf) — reviewed Targeted review: PDF pages 1–2, 11–14; not a line-by-line full-paper audit.

Detector persistence can create false sources and spectral features. DR1 uses five hours of illumination history for conservative masking; the procedure sometimes masks more than 10% of photometric pixels. Masking is conservative and the empirical model does not capture all signal and decay regimes.

## 10. Corcho-Caballero: Euclid Data Release 1 (DR1). Colouring Euclid with external ground-based imaging data

[Manuscript](https://pubs.euclid-ec.org/public/dr1/corcho-caballero.pdf) — reviewed Targeted review: PDF pages 1–2, 7–12, 14–15; not a line-by-line full-paper audit.

External optical imaging enables photometric redshifts and SED reconstruction. Most wide-field calibration is homogeneous, but some northern colour residuals and deep-field calibration failures require spatial quality controls. Northern colour residuals can reach 10–25 mmag; some deep stacks have calibration failures.

## 11. Kümmel: Euclid Data Release 1 (DR1). The MERge processing

[Manuscript](https://pubs.euclid-ec.org/public/dr1/kuemmel.pdf) — reviewed Targeted review: PDF pages 1, 4–6, 8–9, 12–15; not a line-by-line full-paper audit.

DR1 explicitly provides multiband photometry and morphology, including FLUX_RADIUS and Sérsic effective radius, index and axis ratio. Quality flags and brightness selection are essential; wide/deep consistency is useful but is not total external accuracy. Deblending, depth dependence, PSF treatment and fit quality must be controlled.

## 12. Gasparetto: Euclid Data Release 1 (DR1). Multi-band photometry validation on COSMOS extragalactic sources

[Manuscript](https://pubs.euclid-ec.org/public/dr1/gasparetto.pdf) — reviewed Targeted review: PDF pages 1, 7–15; not a line-by-line full-paper audit.

Comparisons with COSMOS-based predictions generally find photometric offsets within 10%, with larger offsets in some deep NIR model-fitting comparisons. Blending and faint-limit selection affect results; reference-model uncertainties limit interpretation. Some offsets reach approximately 12–13%; SED/reference errors and selection effects contribute.

## 13. Hartley et al.: Euclid Data Release 1 (DR1). Photometric redshift pipeline overview and validation

[Manuscript](https://pubs.euclid-ec.org/public/dr1/hartley.pdf) — reviewed pp. 1–4, 9–10, 14–15, 19–20; Tables 1–2 and summary

Foundation supplies object photo-z distributions, corrected photometry, classifications and SED products. At the nominal IE<24.5 depth, point-estimate scatter and catastrophic-outlier rates miss design targets; brighter selections improve performance. COSMOS reference-sample structure and photometric calibration matter. Calibrated sample-level n(z) for cosmology is deferred. Do not transfer bright spectroscopic-validation accuracy to the complete faint sample, or replace redshift PDFs with exact distances.

## 14. Enia et al.: Euclid Data Release 1 (DR1). The PHZ processing function for physical properties of galaxies

[Manuscript](https://pubs.euclid-ec.org/public/dr1/enia.pdf) — reviewed pp. 1–7, 11–12; Tables 2–3, pipeline/priors and validation

Explicitly releases PHYSPARAM stellar-mass, SFR, formation-age and related estimates, with medians, modes and intervals. PPSAMPLINGINDEX preserves reference-neighbour information; PPSAMPLINGFILE supplies 50 draws for deep processing. Inference uses COSMOS-trained SED labels, population priors, a Chabrier IMF and Planck-2016 flat-Lambda-CDM distances. Stellar mass is inferred, not total baryonic mass; neutral/molecular gas is not supplied by Halpha/SFR. Recompute or bracket cosmology/IMF assumptions for native-framework tests.

## 15. Le Brun et al.: Euclid Data Release 1 (DR1). Performance of the redshift measurement and spectroscopic analysis

[Manuscript](https://pubs.euclid-ec.org/public/dr1/lebrun.pdf) — reviewed pp. 1–8, 10–12, 18–19; quality validation and Appendix C query joins

Describes classification, ranked redshift solutions, lines and quality flags. Selected deep-field DESI matches reach high agreement, whereas Wide purity and low-redshift performance differ substantially. A statistical cosmology sample needs further selection calibration. Appendix C gives joins by object_id and solution rank. Redshift probability is not universal correctness; line widths mix spectral and source morphology. Standard SPE data are not circular-velocity curves.

## 16. Odier: Euclid Data Release 1 (DR1). Euclid photometric masks

[Manuscript](https://pubs.euclid-ec.org/public/dr1/odier.pdf) — reviewed Targeted review: PDF pages 1–6, 8; not a line-by-line full-paper audit.

Photometric masks and random catalogues support controlled scientific samples. Effective wide-survey coverage is 1642.4 square degrees compared with 2008.8 square degrees geometric coverage; these products qualify blanket statements that all higher-level products are deferred. Bright-star masks and invalid coverage reduce usable area; spatial selection must be modelled.

## 17. Schirmer: Euclid Data Release 1 (DR1). Calibration strategy and observations

[Manuscript](https://pubs.euclid-ec.org/public/dr1/schirmer-calibration.pdf) — reviewed Targeted review: PDF pages 1, 4–5, 9–15; not a line-by-line full-paper audit.

Most top-level spectrophotometric requirements are met. Shear and VIS PSF calibration remain under development, and the highest-purity spectroscopic reference sample requires additional observations. DR1 does not complete every final-mission calibration requirement.

## 18. Schirmer: Euclid Data Release 1 (DR1). Spacecraft performance in the L2 environment

[Manuscript](https://pubs.euclid-ec.org/public/dr1/schirmer-spacecraft.pdf) — reviewed Targeted review: PDF pages 1–2, 7, 10–13, 18, 20–23, 28–29; not a line-by-line full-paper audit.

Spacecraft, contamination and background behaviour explain instrumental variations relevant to precision imaging. Severe ice contamination caused loss of roughly 300 square degrees of VIS observations during March–June 2024. Time-dependent ice, thermal response, solar contamination and straylight require pipeline corrections.

## 19. Gatto et al. (Euclid Collaboration): Euclid Data Release 1 (DR1). Pushing back the borders of the invisible with Euclid. A systematic search for resolved low-surface-brightness stellar systems from the Milky Way halo to the Local Volume

[Manuscript](https://pubs.euclid-ec.org/public/dr1/gatto.pdf) — reviewed Targeted full-text scientific review: pp. 1–3, 5–13; Tables 1–3; distance-robustness discussion and Appendix A text. Text extraction used; figure images were not independently rendered.

Fifteen resolved low-surface-brightness systems (five new discoveries) provide structural measurements and distances, with stellar-population masses for most. No internal velocities are measured. These are follow-up targets, not acceleration-law confirmations; photometry alone cannot settle cluster versus dark-matter-dominated dwarf status.

## 20. Lines et al. (Euclid Collaboration): Euclid Data Release 1 (DR1). Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) A: Strong Lens Catalogue Overview

[Manuscript](https://pubs.euclid-ec.org/public/dr1/lines.pdf) — reviewed Targeted full-text scientific review: pp. 1–5, 7–14; catalogue, spectroscopy, modelling summary, completeness/selection and availability; relevant appendix text. Figure images not independently rendered.

The ECLIPSE object release contains 6,073 grade-A and 8,999 grade-B candidates, plus C/X grades. It identifies 84 double-source-plane candidates. DESI spectroscopy supplies 20 paired lens/source systems in aggregate, but the small archive lacks row-level source linkage. Visual grades are not a complete confirmed-lens selection function.

## 21. Holloway et al. (Euclid Collaboration): Euclid Data Release 1 (DR1). Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) B:  Discovery pipeline overview

[Manuscript](https://pubs.euclid-ec.org/public/dr1/holloway.pdf) — reviewed Targeted full-text scientific review: main discovery methods/results and selection/completeness in pp. 1–10; Appendix B simulation description and Appendix E completeness derivation, pp. 18–23. No independent figure-image QA.

ECLIPSE discovery combines automated searches, volunteers and expert grading. Reported completeness is conditional on the catalogue-eligible parent population, expert labels and detection pipeline. A count or abundance test requires forward selection modelling and a theory for galaxy populations; the bare acceleration relation supplies neither.

## 22. Nightingale et al. (Euclid Collaboration): Euclid Data Release 1 (DR1). Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) C: Lens modelling pipeline overview

[Manuscript](https://pubs.euclid-ec.org/public/dr1/nightingale.pdf) — reviewed Targeted full-text scientific review: pp. 1–8, 10–17; all mass/source/light modelling, fit-stage definitions, inspection results, error/PSF caveats, scientific-use discussion and data availability; Appendix A model/likelihood definitions checked. Figures not independently rendered.

SIE plus external-shear fits yield 7,980 consensus successes (7,976 finite summaries). The isothermal slope is fixed, so these are not independent slope measurements. Model summaries support candidate selection; images permit new forward fits. Formal bounds in the archive do not supply calibrated individual uncertainty or systematic-error budgets.

## 23. Nersesian et al. (Euclid Collaboration): Euclid Data Release 1 (DR1). Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) D: Photometric redshifts and the first census of strong lenses in the galaxy evolution framework

[Manuscript](https://pubs.euclid-ec.org/public/dr1/nersesian.pdf) — reviewed Targeted full-text scientific review: pp. 1–14; quality cuts, deblending, redshift/SED methods, scaling relations, limitations and availability; Appendices B–D, pp. 22–26, on photometric calibration, posteriors and method dependence.

The final physical-property sample includes 9,538 DR1 lenses, not the same set as successful C models. Lens photo-z, light profiles and Salpeter-based stellar masses are valuable. A same-photometry method difference of about 0.23 dex exceeds the distinctive normalization signal. Source photo-z is deferred; stellar mass, IMF and cosmology remain assumptions.

## 24. Bergamini et al. (Euclid Collaboration): Euclid Data Release 1 (DR1). NISP spectroscopy of gravitational arcs and multiple images

[Manuscript](https://pubs.euclid-ec.org/public/dr1/bergamini.pdf) — reviewed Main scientific text pp. 1–8 and Appendix A pp. 14–15; Table 1, spectral extraction, redshift errors and preliminary mass formula reviewed. No independent figure rendering.

Four lensed sources have NISP redshifts, with single-line identifications qualified in the paper. PS1J1821+7130 has z_source=1.366±0.008 with DESI support. These redshifts can unlock geometric tests, but published GR/distance-derived lens masses are not theory-independent data. Our identified pilot fails the current strict detection-quality cut.

## 25. Gabarra et al.: Euclid: Data Release 1 (DR1) -- First NISP emission-line maps: Methodology, validation, and applications to galaxy evolution

[Manuscript](https://pubs.euclid-ec.org/public/dr1/gabarra.pdf) — reviewed Main scientific text pp. 1–15: dataset, reconstruction, source injections, PSF, every scientific demonstration, statistical applications and caveats; Table 1 and Fig. 7 velocity example text reviewed. No independent rendering of figures.

GELSA extracts emission-line maps from 116 single-orientation blue-grism exposures over about 0.5 square degrees in COSMOS. One illustrative velocity-gradient calculation gives 407 km/s differential and 252 km/s inclination-corrected rotation. Neither a velocity error budget nor a flat outer curve is established. This is a new extraction lead, not a BTFR datum.

## 26. Dunn et al.: Euclid: Data Release 1 (DR1) -- Bayesian 3D shape inference of star-forming galaxy populations

[Manuscript](https://pubs.euclid-ec.org/public/dr1/dunn.pdf) — reviewed Main text pp. 1–12; selection Appendix A p. 17, shape comparison Appendix B pp. 18–20, completeness Appendix E p. 23, modelling results Appendix F pp. 24–25, individual-class discussion Appendix G p. 26. No independent figure-image QA.

Population-shape inference uses over 40 million star-forming galaxies with mass and redshift cuts. The inferred three-dimensional ellipsoid distributions can inform morphology priors. They do not supply individual inclinations or dynamics; axis ratio cannot universally be replaced by cos(inclination).
