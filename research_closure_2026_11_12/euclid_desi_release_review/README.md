# Euclid DR1 and DESI DR2 review

12 November 2026. **Working checkpoint: paper review and repository comparison in progress.**

The task is to identify genuinely executable tests of the Zimmerman acceleration-scale relation using Euclid DR1-Foundation, check all papers in the official release cohort, incorporate public DESI DR2 results, and distinguish new tests from predictions or verdicts already present in this repository. No new observational fit or theory-validation claim has been made.

## Current evidence

- The [official Euclid publication index](https://pubs.euclid-ec.org/public/) lists **26 manuscripts** under its November 2026 DR1-Foundation heading. All 26 PDFs were retrieved; `paper_inventory.json` records their URLs, sizes and SHA-256 hashes. Full source PDFs remain in temporary storage, outside the repository.
- The review covers relevant methods, data products, validation, limitations and conclusions. It is a targeted scientific review, not a line-by-line audit of every derivation in every paper.
- Foundation supplies imaging, morphology, photometry, redshift products and galaxy physical-property estimates. Enia et al., Tables 2–3 and section 3, explicitly describe `PHYSPARAM`, stellar mass, SFR and uncertainty summaries. These are inferred quantities with stellar-population and cosmological assumptions, not direct baryon measurements. [Paper](https://pubs.euclid-ec.org/public/dr1/enia.pdf)
- The ECLIPSE lens release is a promising new independent sample. Its model fits assume singular isothermal ellipsoids plus external shear, and individual parameter uncertainties are not supplied. A model-derived mass or velocity dispersion is not independent evidence for the repository's gravity law. [Nightingale et al.](https://pubs.euclid-ec.org/public/dr1/nightingale.pdf)
- Gabarra et al. demonstrate a bespoke internal-velocity-gradient measurement for one galaxy. This qualifies the earlier blanket statement that Euclid cannot provide kinematic information: standard SPE outputs are not rotation curves, but a carefully validated custom extraction may supply useful information. The example is illustrative and is not a validated rotation-curve catalogue. [Paper](https://pubs.euclid-ec.org/public/dr1/gabarra.pdf)
- Calibrated weak-lensing shape products and the full cosmological analyses are deferred to 2027. Some masks and related products are already released; it is incorrect to say that every Level 3 product is absent. [Overview](https://pubs.euclid-ec.org/public/dr1/aussel.pdf), [masks](https://pubs.euclid-ec.org/public/dr1/odier.pdf)
- DESI DR2 BAO/cosmology products and recent papers are public, but the underlying DR2 spectra and redshifts remain unreleased according to the [official DESI publication page](https://data.desi.lbl.gov/doc/papers/). Public DESI DR1 can supply object-level crossmatches now.

## Repository baseline

The current headline relation is `a0 = kappa c sqrt(G rho_DE)`, with `kappa = 1/2` adopted/fitted. The canonical vacuum-density and alternative total-density normalizations must be kept separate. The relation alone does not specify the force-law interpolation, light deflection or structure growth. See [framework equations](../../FRAMEWORK_EQUATIONS_2026-10-15.md) and the [November 12 review](../three_model_review/REVIEW.md).

Already identified:

1. `campaign_fresh_gravity/CFG681_bao_raw_geometry` and `CFG689_native_ruler_bao` already use March 2025 DESI DR2 BAO. The inferred dark-energy density uses additional priors and assumptions; it is not a direct BAO observable. July 2026 Ly-alpha AP geometry may provide an update, replacing correlated earlier measurements rather than adding an independent duplicate.
2. `closure_2026_11_11/DW1_desi_dr2_mw_mass` already examines the November 2026 DESI Milky Way paper. Its covariance and calibration caveats must accompany any reuse.
3. `closure_2026_11_11/FINAL4_growth_history/FROZEN_CRITERIA.md` contains PR-F4, an unrun lensing redshift-split test with a split at lens redshift 0.5. Its target is a conditional formation model, not the bare acceleration-scale identity.
4. `prep_2026/cluster_kink_spec/PREREGISTRATION_EUCLID_NULL.md` explicitly retires the old Euclid weak-lensing cluster-kink test. Its exterior differential signal vanishes in the stated model.
5. The November 12 review requires a single fixed interpolation kernel and consistent physical versus Newtonian external fields. Historical AQUAL rescue claims were corrected; they cannot be imported as current passes.
6. `deepseek_push/DS_FINAL_2026_10_21/A55_lensing_prediction/report.md` already tests 70 SLACS lenses. Its fixed-normalization Einstein-radius gate fails; the reported agreement requires a fitted stellar-mass enhancement. Euclid can supply an independent extension of this existing adverse test, not its first application.
7. `rebuild_2026_10_22/SP1_sealed_lensing_step` and `SP2_sealed_basin_lensing` contain older step/environment predictions that must be checked as recorded. The initial search has identified conflicting inequality directions in their criteria versus explanatory text. Do not silently repair or score those gates while this audit is in progress.
8. Later strong-lens work also matters: `deepseek_push/DS_FINAL_2026_10_21/A85_slacs_jeans_joint/VERDICT.md` reports conditional lensing-to-dynamics consistency after calibrating each lens's stellar normalization to its Einstein radius. This is not a parameter-free baryonic prediction or a measurement of kappa. A80/A85 must be read alongside A55 before ranking the independent Euclid test.

## Work in progress

- Finish the per-paper comparison and consolidate all 26 records.
- Search dated prediction-bearing lanes more broadly, including older photon-lensing and redshift-evolution tests.
- Audit which specified models actually pass which existing gates, preserving failed, conditional, post-hoc and no-verdict statuses.
- Rank executable tests by independent information, systematic-error burden and missing measurements.
- Produce the complete report and a concrete next experiment. A breakthrough requires a new discriminating result; a large catalogue alone does not establish one.

## Handoff and access

Temporary source directory on the current machine: `/private/tmp/euclid_dr1_review_20261112/`. Another machine should re-fetch sources from the recorded public URLs and compare hashes. `paper_inventory.json` is the reproducible source list, not a claim that every manuscript has finished review.

A live query of IRSA `TAP_SCHEMA.tables` for Euclid names returned only Q1 tables during this session; the advertised IRSA DR1 overview returned 404. This is an access observation about that mirror, not evidence that the ESA release is absent. ESA release pages and public paper PDFs were accessible through direct HTTPS. No DR1 observational catalogue was fitted in this checkpoint.

Publishing is authorized by the user's request to push the work as it lands. The working checkout has substantial unrelated modifications and divergent history. This review is being published as a document-only branch based on remote `main`, preserving that working state.
