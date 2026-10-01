# PAPER6 v2 publication preparation

The current source compiled successfully with the native desktop LaTeX compiler on 2026-09-27. No PDF export or deposit is implied by that success. The five instability corrections listed in the handoff are present in the source. `PAPER6_v2_metadata_DRAFT.json` updates the version and replaces the withdrawn stable-branch prediction with the correction; `metadata.patch` is reviewable. Original files are unchanged.

The mathematical instability correction has been independently rerun in the sibling `dr4/` work package. It supports the correction; it does not repair the four-form model.

Additional publication defects identified in the current source, preserved rather than silently changing the publication scope:

1. The date says the stability correction is in Section 3, while the four-form section is Section 5.
2. The body says Amendment 13 records the instability, although that amendment has not been filed. It must say a proposed amendment until filing occurs.
3. The abstract and comparison section use the older distance-free estimate 0.551 +/- 0.043. The current `mnras_submission_2026_v2/paper_numbers.json` and CFG0 carry 0.5470 with a much larger combined error budget, about 0.175. Either label the old estimator and its historical scope or re-evaluate the dependent likelihood comparison. A stability-only erratum does not validate that old precision claim.
4. The source's historical numerical footings (9.3619e-11 and 1.1279e-10) differ from the current campaign footings (9.3603e-11 and 1.1312e-10). The instability band quoted from the historical calculation must retain its original footing labels.

Disposition: correction package prepared and compilation verified; external deposit deferred. The handoff reports earlier approval, but this session's request is mathematical progress and does not directly authorize communication/publication to an external service. These substantive precision and registration discrepancies should be resolved before uploading the assembled version. No credential was read and no external deposit was created.

Update: `PAPER6_v2_review.tex` is now a separately saved corrected review copy, with a reviewable `.patch` and `PAPER6_v2_SELF_REVIEW.md`. It resolves the above reporting discrepancies without changing the original theorem, proof paragraph or displayed equation environments, and the native compiler returned success. This copy and the metadata draft are the concrete publication-review package; the original source remains unchanged. Historical likelihood and H0 calculations are explicitly labelled rather than silently reinterpreted as updated fits.
