# FGF028 coordinator review

Accepted only as response-derived finite identification, exact stored-coefficient controls and deterministic sensitivity, conditional on the inherited pressure basis/support, fixed zero offset and finite beam model. No calibrated gradient, map fit, covariance, force or theory closure is accepted.

All three cached outer-annulus response rows [2,3),[3,4),[4,5) jointly identify the target and fifteen pressure coefficients. Every single and pair fails. Original twelve rows reproduce bitwise. Root independently solved the full15 transpose system over rationalized binary64 and checked all seven subsets, preserving strict monotone null witnesses for the failing ones. Its fifteen exact dual weights equal the worker's Schur reconstruction weights. The raw target L1 gain is50.26948356094382, reduced condition2 is22.8806626801 and full pressure condition2 is1445.025474317. The separately row-normalized reduced condition is15.7704579178.

Worker adapted the explicitly read parent projector, rather than claiming independent response derivation. Root inspected its actual code, including geometry, FFT angular spacing, cutoff, pressure support, mask weights and import-safe reviewed validator. Independent response reviewer used a different spherical angle formula and direct32-point line-of-sight quadrature for one outer pressure basis (x=4), followed by the declared beam. The old12 and new3 column entries agree within1.33e-15 and8.88e-16 respectively. All15 annular mask-weight hashes agree; outer usable counts13036,18240,23474 with mask1. This one-column independent check plus code review does not certify continuum accuracy of the beam/padding model or all basis refinements.

For componentwise data error |delta y_i|<=epsilon, exact reconstruction gives |delta g|<=epsilon||r||1 and the saved worst-sign perturbation attains it. Root used synthetic1e-9 y (1.36419% of synthetic baseline); worker used1e-8 y (13.6419%). These intentionally different controls have identical gain; neither is measured noise or a confidence bound. No inequality-admissibility claim is made for the noisy unconstrained inverse profile.

Root's separate changed-premise negative control releases the fixed offset. It solves Uv=-1 and verifies two strict positive monotone profiles with opposite offsets that preserve all15 bins. Their gradient moves by -sum(r)t, where sum(r)=-0.028902247822995483. This proves calibration of the offset cannot simply be dropped; it is not an inferred real background correction. The reviewer checks this small certificate/code and generic proof separately from its response computation.

Three bounded manifests (worker construction, root target audit, reviewer response) validate. Declared input and artifact hashes are current; no scientific run failure was reported. Exact rank and data-error gain do not bound physical response error r DeltaU p. Cached geometry and mask are used, but fiducial distance, finite support, spherical profile, flat-sky response, calibration and shared-map covariance remain assumptions or gaps. Annuli from one map are not independent instruments.

Next prioritize FGF027 quantitative coupled-slab gap. FGF029 is a separate unlaunched source-support robustness child: release p(5)=0 by adding node5 and moving zero endpoint to6, then test finite target identification. Any later source bridge must use total-pressure/density conversion, both a0 normalizations, distinct vacuum/H histories and separate Q/RAR/registered M. Physical metric/photon and common-framework closure remain open.

## Pinned evidence

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-028/fgf028_run_001/result.json` SHA256 `0092943a66e281f25deb80167347f4ee1ef2373948710bc1abab8ca05b7233ca`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-028/fgf028_run_001/outer_response.py` SHA256 `44dcdb8addb325b12f39222afaafdc745eb604680a5e31903636b05498476625`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-028/fgf028_run_001/numeric_001/response_rows.npz` SHA256 `15b06368f5d0609f85ccc9717a669614dfe948121d70ecad3f96e7325ae96843`.
- `campaign_fresh_gravity_astra/stage_13/target_audit/DERIVATION.md` SHA256 `0c925114a1b99d195ad12bf01ccaddbc4960d95aeb68b449fc25acd7a4773867`.
- `campaign_fresh_gravity_astra/stage_13/target_audit/run_001/results.json` SHA256 `2ead1fe4d3ea7b790006f57fe2ec5412a15534d57f0a241af169642f9da6e3af`.
- `campaign_fresh_gravity_astra/stage_13/target_audit/CROSS_IMPLEMENTATION.json` SHA256 `97d23ec10918004633bb2992778ce7f4717c6b344b1e779fa3cbf6f47d4adf8f`.
- `campaign_fresh_gravity_astra/stage_13/response_audit/INDEPENDENT_AUDIT.md` SHA256 `dd4e3c79dab96f08176188e073f37df3ed2dc2d8f7203fec5e8e4ff3ece6a275`.
- `campaign_fresh_gravity_astra/stage_13/response_audit/audit_result.json` SHA256 `b465d980debdd8de12633078708f218ec1b93ff823e0705c995ed30d4afdf62f`.

Reconciled 2026-09-30T07:35:47.653428+00:00.
