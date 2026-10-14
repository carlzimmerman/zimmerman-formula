# Prediction Before Publication: Dated Zimmerman Forecasts Compared with MUSE-DARK III, MIGHTEE-HI/LADUMA, and JUNO

**Carl P. Zimmerman** · Briar Creek Tech

October 14, 2026 · Version 1.2 · Research note

## Abstract

We audit dated forecasts in the Zimmerman programme against later 2026 results, retaining their original versions and assumptions. Public Zenodo records created March 19-20 establish that a rising acceleration-scale forecast, a₀(z) = a₀(0)E(z), preceded MUSE-DARK III's April 24 submission. Using unchanged constants from the March 17 Git calculation, the forecast lies within 4.8% of MUSE's subsequently published MOND-based central redshift relation across 0.33 < z < 1.44. The public paper's slightly different local normalization gives a similarly close central-curve agreement. These are comparisons with a fitted, model-dependent relation, not a new raw-data likelihood test. The August MIGHTEE-HI/LADUMA result is compatible with a later constant-vacuum branch without selecting it over mild evolution. A March public solar-angle formula is compatible with JUNO's September update at 1.06 quoted standard errors; an older speculative mass-splitting ratio is 1.33% below the ratio computed from JUNO's normal-ordering results. Conflicting archived formulas are disclosed. Public advance publication and close numerical agreements are established; uniqueness, a new physical derivation, and formal statistical confirmation of the acceleration forecast are not.

## 1. Question and evidentiary standard

The question is chronological: was a specific forecast recorded before a later observational result was published? It differs from asking whether the forecast fits the data, whether it was novel, or whether an independently timestamped public registration existed. Each requires additional evidence.

The audit covers relevant result releases during April 13-October 13, 2026. It inspects historical repository objects rather than treating the present README as a record of what was predicted in March. Three observational papers are examined in their first arXiv versions [1, 2, 7]. A September reanalysis [3] is considered separately because it uses existing MUSE results. This is a bounded audit of these sources, not an exhaustive census of every astronomy release during the interval.

Git author and committer dates are editable metadata. The attached objects document the history now available in the repository. Public Zenodo record metadata and deposited PDFs independently establish public availability of the rising functional forecast by March 19 UTC [5, 6]. They do not establish public availability of every numerical constant in the exact March 17 Git calculation. Neither arXiv submission dates nor this audit establish when the underlying telescope observations were acquired or when investigators first inferred the result. No claim of precedence over all public talks, drafts, or antecedent analyses is made.

## 2. The forecast recorded on March 17

Commit e1603604aa02e06e5dd397234295e87bb4654b64 has identical author and committer timestamps of March 17, 2026, 23:30:47 UTC−04:00. Its manuscript, zimmerman_formula.md, Section 5.3.1, specifies the critical-density branch:

    a₀(z) = a₀(0) E(z),
    E(z) = [Ωₘ(1 + z)³ + ΩΛ]^(1/2).

Here a₀ is the MOND acceleration scale, z is redshift, Ωₘ and ΩΛ are the present matter and cosmological-constant density fractions in the assumed flat background, and E(z) = H(z)/H₀. The relation follows from adopting a₀ = (c/2)√(Gρc) and ρc = 3H²/(8πG). The adopted coefficient is not derived by this chronology audit.

The historical table gives a₀(z = 1)/a₀(0) = 1.79 and a₀(z = 1) = 2.14 × 10⁻¹⁰ m s⁻². Those values are preserved as written. The table rounds its entries and its local normalization; this note does not silently replace them with a later normalization or a refitted cosmology.

The earlier public deposit is “The Zimmerman Formula: Deriving MOND from Cosmology,” DOI 10.5281/zenodo.19104121 [5], created March 19 at 02:56:54 UTC (March 18 at 22:56 EDT). Page 2, Section 3, explicitly states the rising E(z) forecast and tabulates a factor 1.79 at z = 1. This PDF uses H₀ = 71.5 and a local scale 1.20 × 10⁻¹⁰, whereas the Git helper uses H₀ = 71.1 and gives 1.19318 × 10⁻¹⁰. The same shape is publicly dated; the small normalization difference must remain visible. The dedicated “Redshift Evolution of the MOND Acceleration Scale: A Testable Prediction,” DOI 10.5281/zenodo.19121510 [6], was created March 20 at 00:55:52 UTC. Its rough table lists 2.0 × 10⁻¹⁰ at z = 1. Thus public numerical tables should not be conflated with the exact Git calculation.

The mathematical dependence a₀ ∝ H(z) was already an idea in the MOND literature; MUSE-DARK III itself discusses prior alternatives [1]. The claim here concerns the author's dated numerical forecast, not priority for the general scaling.

## 3. The April MUSE-DARK III result

Ciocan et al. submitted MUSE-DARK III on April 24, 2026, at 14:41 UTC, approximately 37.5 days after the forecast's Git timestamp [1]. From 79 star-forming galaxies at 0.33 < z < 1.44, they infer a characteristic scale near z = 1 of 2.38 with upper/lower reported errors 0.12/0.10, in units of 10⁻¹⁰ m s⁻², and an increasing scale with redshift. Their phenomenological linear fit has slope approximately 1.59 × 10⁻¹⁰ m s⁻² per unit redshift. Section 3.2 identifies its parameter intervals as 95% confidence intervals; they must not be read automatically as one-standard-deviation errors.

Against the near-z-one summary, the March tabulated forecast is lower by:

    (2.14 − 2.38)/2.38 = −0.10084 ≈ −10.1%.

The headline estimate is halo-dependent: Section 2 and Appendix B infer both accelerations using DC14 disk-halo fits. Stellar masses are dynamically inferred, and the neutral-gas contribution is parametrized without direct constraints. Appendix C explicitly acknowledges that the two accelerations come from the same model, rather than independent measurements. These assumptions matter for the numerical comparison.

Appendix E separately refits the MUSE data cubes using MOND. Its Eq. (13) gives a MOND-based RAR scale of 2.19 with upper/lower reported errors 0.12/0.10, in units of 10⁻¹⁰ m s⁻². Relative to that result, the March value is lower by (2.14 − 2.19)/2.19 = −2.28%. The median of the individual MOND fits is 2.27 in the same units, a distinct summary, giving a 5.73% difference. The MOND analysis shares disk/gas prescriptions and priors on common parameters and assumes isolated MOND without an external-field effect. These are alternative analyses of the same sample, not independent replications or model-independent determinations.

These are illustrative comparisons, not exact matched-redshift likelihood tests. The near-z-one summaries and fitted linear curves are different summaries of the sample. A full test would evaluate the frozen curve against the individual or binned measurements at their actual redshifts, with covariance and baryonic-model uncertainties. This note neither performs that fit nor assigns a significance to these differences.

The original authors describe the inferred rise as faster than H(z) [1, Section 4]. Alcock's September 30 reanalysis reports that Hubble tracking can describe the same binned measurements when the amplitude is allowed to float [3]. This note verifies the existence and abstract-level claim of that reanalysis, but does not reproduce its fit. A fitted amplitude changes the question from testing the fixed March forecast to testing the shape family. It supplies no additional independent observational sample.

A matched-redshift central-curve check gives a stronger comparison than the near-z-one summary. The exact March helper functions, with H₀ = 71.1, Ωₘ = 0.315 and ΩΛ = 0.685, give a₀(0) = 1.1931775786 × 10⁻¹⁰. No parameter is fitted to MUSE. Against the MOND-based relation a₀(z) = (1.03 + 1.20z) × 10⁻¹⁰ in Appendix E (PDF Eq. E.5; HTML Eq. 14), the values are:

| z | Unchanged March forecast | Published MOND central trend | Difference |
|---|---|---|---|
| 0.33 | 1.4249 | 1.4260 | −0.08% |
| 0.50 | 1.5776 | 1.6300 | −3.22% |
| 0.80 | 1.8949 | 1.9900 | −4.78% |
| 1.00 | 2.1361 | 2.2300 | −4.21% |
| 1.30 | 2.5361 | 2.5900 | −2.08% |
| 1.44 | 2.7368 | 2.7580 | −0.77% |

Accelerations in the table are in units of 10⁻¹⁰ m s⁻². A 10,001-point scan finds a largest central-curve difference of 4.78177%; an independent stationary-point check locates it at z = 0.786979875. With t = 1 + z, the derivative of the ratio vanishes at 0.378t³ − 0.16065t² − 1.644 = 0. This polynomial is strictly increasing on the sampled interval, giving one interior extremum; endpoints are closer. Retaining the public PDF's local scale 1.20 instead gives a largest absolute central-curve difference of about 4.24%.

This is a close advance forecast of the published MOND-based trend. It is not a statistical goodness-of-fit verdict. The four plotted Figure 3 bins are halo-based; approximate digitization puts the March curve 7-20% below them. The corresponding MOND bin estimates and joint posteriors were not found in the public material checked, so this note supplies no chi-square, p-value or statistical pass. A rise also does not uniquely identify the framework.

## 4. The later vacuum branch and August result

By commit 3d8c0388f0d13b6f6563143ecc0e0793e1d71519, dated June 5, 2026, the programme's confrontation script explicitly designates the vacuum-density branch as canonical:

    a₀(z)/a₀(0) = [ρDE(z)/ρDE(0)]^(1/2).

For constant vacuum density this gives a constant scale. For an evolving dark-energy model it follows the specified density history rather than H(z). The archived June script distinguishes this branch from the earlier rising critical-density branch. This establishes a recorded interpretation by June 5; it does not claim that June 5 was its first appearance.

The June interpretation postdates MUSE-DARK III's submission. It cannot be credited with the March branch's agreement with MUSE, and its constant-vacuum specialization is in tension with the reported MUSE rise if the inferred scale is interpreted as the fundamental scale. The programme's later interpretation must be judged separately.

Vărăşteanu et al. submitted their 130-galaxy MIGHTEE-HI/LADUMA analysis on August 4 [2], after the June interpretation. Their fiducial sample extends to z ≈ 0.09 and gives a RAR scale (1.50 ± 0.05) × 10⁻¹⁰ m s⁻². The within-sample linear evolution fit gives slope (−1.60 ± 2.33) × 10⁻¹⁰ m s⁻² per unit redshift, compatible with zero. Their Table 4 shows that inferred evolution changes with stellar mass-to-light assumptions and inclusion of a local SPARC anchor.

Zero slope is compatible with the constant-vacuum branch. It also cannot distinguish mild Hubble tracking over this interval: using Ωₘ = 0.315 and ΩΛ = 0.685, E(0.09) − 1 = 4.54%. Compatibility of the slope does not validate the absolute vacuum-branch normalization, approximately 0.936 × 10⁻¹⁰ m s⁻², which is appreciably below the published fitted level. Baryonic calibration and interpolation conventions must be addressed in a matched normalization test. The August result is therefore not counted as a decisive confirmation.

## 5. An additional September JUNO comparison

The public March 20 deposit “The Complete Standard Model from Geometry,” DOI 10.5281/zenodo.19140259 [8], contains the solar-angle formula sin²θ₁₂ = 1/3 − πα, with α = 1/(4Z² + 3) and Z² = 32π/3. It gives 0.31040891 (printed 0.3104). JUNO's September 29 update reports sin²θ₁₂ = 0.3036 ± 0.0064 [7], a difference of 1.06 quoted standard errors. This is an earlier public numerical hypothesis compatible with a later measurement; the formula was already chosen near older measured values, so this agreement alone does not demonstrate a new physical mechanism.

An earlier repository review also records Δm²₃₁/Δm²₂₁ = Z² = 33.5103 as a speculative hypothesis. JUNO's normal-ordering central splittings, +2.509 × 10⁻³ and 7.388 × 10⁻⁵ eV², give a ratio 33.9605: the hypothesis is 1.33% lower. No ratio significance is computed without the joint covariance. The atmospheric result uses a Daya Bay constraint to identify the fit's physical minimum [7]; it should not be called completely independent of prior oscillation information. Public preregistration of this exact ratio was not independently authenticated in this audit.

Versions matter. The public March 27 “Cube x Sphere” archive, DOI 10.5281/zenodo.19244651 [9], instead gives sin²θ₁₂ = 1/3 − 1/(3Z) = 0.275751, about 4.35 quoted standard errors below September's result. That archive also prints Δm²₃₂/Δm²₂₁ = Z²/8, a different and unsuccessful formula. These cannot be pooled with the successful-looking versions. The later conditional TM1 window [0.3162, 0.3198] also lies above the new solar central value. This audit therefore records additional compatibility, not a blanket success for the neutrino programme.

## 6. Chronology and verdict

| Recorded item | Date | What the evidence establishes |
|---|---|---|
| Critical-density forecast | March 17 | Git-dated rising curve and a numerical z = 1 value |
| Public rising forecast [5, 6] | March 19-20 UTC | Independently dated Zenodo publication of E(z) forecast |
| Public solar-angle formula [8] | March 20 UTC | 0.3104 recorded before September JUNO update |
| MUSE-DARK III v1 | April 24 | Later arXiv submission reporting an increasing fitted scale |
| Vacuum-branch confrontation | June 5 | Recorded canonical interpretation after MUSE, before the August paper |
| MIGHTEE-HI/LADUMA v1 | August 4 | Later low-redshift result compatible with zero evolution |
| JUNO update | September 29 | Later measurement compatible with some earlier hypotheses; others miss |
| Alcock reanalysis | September 30 | Reinterpretation of MUSE points, not a new sample |

There is a documented prediction-before-paper sequence for MUSE-DARK III in both the Git record and independently dated public Zenodo deposits. The unchanged March forecast anticipated the MOND-based central trend closely across the reported redshift interval. There is also a recorded vacuum-branch interpretation before MIGHTEE-HI/LADUMA, whose slope is compatible with constant a₀ but is insufficiently discriminating to confirm that branch.

No branch receives a decisive statistical confirmation from this audit. The public rising forecast precedes the MUSE submission; the published solar-angle formula precedes the September JUNO submission. This note documents those prior publications rather than creating a retroactive registration. A future decisive test should freeze the branch, normalization, interpolation, baryonic treatment and likelihood before a genuinely independent result is accessed, and report all outcomes, including adverse ones.

## 7. Reproducibility and disclosure

The companion script PREDICTION_CHRONOLOGY_2026_build.py extracts the original March manuscript and June confrontation from their exact Git objects, records hashes and timestamps, and recomputes the numerical comparisons. The attached evidence archive contains those snapshots and the manifest. The PDF is built from this Markdown source; both are supplied. No galaxy data have been refitted and no external observational paper is redistributed. Version 1.2 adds verified public-deposit timestamps, the matched-redshift central-curve computation and the JUNO comparisons. Earlier versions were unpublished local drafts. Companion check.py, CSV/JSON results, plots, and the public-source verification records are included in the evidence archive. The older source snapshots are historical evidence, not endorsements of all claims they contain.

This note was prepared with AI assistance for source discovery, drafting, chronology extraction and arithmetic. The historical forecast belongs to the author. The chronology and scientific conclusions are limited to the evidence stated here. The acceleration-scale relation's coefficient remains adopted/fitted; a complete gravity theory is not established.

## References

[1] Ciocan, B. I., Bouché, N. F., Fensch, J., et al. (2026). MUSE-DARK III: The evolution of the radial acceleration relation at intermediate redshifts. A&A 709, L16. arXiv:2604.22613v1, submitted April 24. https://arxiv.org/abs/2604.22613v1. Published DOI: https://doi.org/10.1051/0004-6361/202659230.

[2] Vărăşteanu, A. A., Jarvis, M. J., Desmond, H., et al. (2026). MIGHTEE-HI / LADUMA: Investigating the link between baryons and dynamics with 130 resolved HI-selected galaxies. arXiv:2608.03576v1, submitted August 4. https://arxiv.org/abs/2608.03576v1.

[3] Alcock, G. T. (2026). Is the acceleration scale of the radial acceleration relation tracking the cosmic expansion rate? arXiv:2609.38796v1, submitted September 30. https://arxiv.org/abs/2609.38796v1. Abstract-level comparison only; full fit not reproduced here.

[4] Zimmerman, C. (2026). Historical manuscript and confrontation script, exact commits e1603604aa02e06e5dd397234295e87bb4654b64 and 3d8c0388f0d13b6f6563143ecc0e0793e1d71519. Repository: https://github.com/carlzimmerman/zimmerman-formula. Immutable-content snapshots supplied in the accompanying evidence archive; Exact Git-object snapshots supplied; the related public forecast deposits are authenticated separately in [5, 6].


[5] Zimmerman, C. (2026). The Zimmerman Formula: Deriving MOND from Cosmology. Zenodo record created March 19, 02:56:54 UTC. Deposited file zimmerman_formula_v1.0.1.pdf, page 2. https://doi.org/10.5281/zenodo.19104121.

[6] Zimmerman, C. (2026). Redshift Evolution of the MOND Acceleration Scale: A Testable Prediction. Zenodo record created March 20, 00:55:52 UTC. https://doi.org/10.5281/zenodo.19121510.

[7] JUNO Collaboration (2026). Measurement of Neutrino Oscillation Parameters at JUNO and Indication of the Neutrino Mass Ordering. arXiv:2609.37895v1, submitted September 29. https://arxiv.org/abs/2609.37895v1.

[8] Zimmerman, C. (2026). The Complete Standard Model from Geometry: Deriving All 36 Parameters from Z = 2√(8π/3). Zenodo record created March 20, 22:17:28 UTC. Deposited file ZIMMERMAN_UNIFIED_THEORY_v7.pdf, PMNS Matrix section. https://doi.org/10.5281/zenodo.19140259. Only the stated prior numerical hypothesis is used here; the other broad claims in the deposit are not validated by this note.

[9] Zimmerman, C. (2026). Cube x Sphere. Zenodo record created March 27. Archive zimmerman_framework_v2.zip, NEUTRINO_FORMULAS.py and ZIMMERMAN_FRAMEWORK_PUBLICATION.md. https://doi.org/10.5281/zenodo.19244651. Cited to disclose incompatible historical formulas.
