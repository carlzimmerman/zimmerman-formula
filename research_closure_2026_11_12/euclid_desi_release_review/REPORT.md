# What Euclid Foundation and DESI DR2 can test

12 November 2026. Literature and repository review complete at the scope below; exploratory derivations continue in the route records. **No Euclid gravity-law fit or new observational confirmation has been performed.**

## Finding

The strongest immediate connection is between the new Euclid light-profile measurements and the repository's existing A80/A85 strong-lensing work. A80 identified unmeasured Sérsic shape as a major degeneracy; A85 obtained conditional mean lensing-to-dynamics agreement after calibrating a stellar normalization per lens. Euclid can provide independent morphology and a much larger candidate population. It does not yet provide all the independent redshifts, stellar dynamics and calibrated model errors needed to turn that connection into a passed test.

The more ambitious opportunity is to construct observables that cancel nuisance normalizations, then ask whether their remaining shape or redshift dependence differs between specified theories. The user explicitly requested that research step. It is being pursued separately from this release audit; candidate algebra is not an empirical breakthrough.

## 1. What was released, and what was actually inspected

The [official Euclid index](https://pubs.euclid-ec.org/public/) lists 26 manuscripts in the November DR1-Foundation cohort. All 26 PDFs were downloaded and reviewed in the relevant methods, validation, products and interpretation sections. [PAPER_REVIEW.md](PAPER_REVIEW.md) records coverage paper by paper; [paper_inventory.json](paper_inventory.json) pins source hashes. This is not a complete audit of every derivation in all 26 manuscripts.

Foundation includes calibrated imaging, photometry, morphology, object redshift products, galaxy physical-property estimates, masks and random catalogues. The blanket description “images only” is too restrictive. Conversely, morphological ellipticities are not calibrated weak-lensing shear. The full shear/correlation/cosmology products follow in June 2027 under the current staged release. [Aussel et al.](https://pubs.euclid-ec.org/public/dr1/aussel.pdf), [Odier et al.](https://pubs.euclid-ec.org/public/dr1/odier.pdf).

Important distinctions for a gravity test:

| Released input | Useful information | What cannot be treated as an independent measurement |
|---|---|---|
| MER morphology | Sérsic index, radius, axis ratio, segmentation and fit flags | A universal inclination, baryonic density profile, or calibrated shear |
| PHZ physical properties | Stellar-population mass/SFR estimates and uncertainty products | Gas mass, total baryonic mass, or a cosmology/IMF-free mass |
| SPE spectra | Ranked redshift solutions and line measurements | A rotation curve or independent stellar dispersion from an arbitrary line width |
| ECLIPSE lens models | Candidate configurations and image-model starting points | A free density slope: C fixes an isothermal model; an SIE velocity scale is not measured dynamics |
| ECLIPSE physical properties | Lens redshifts and light/mass metadata | Source redshifts for every lens, or an externally calibrated total mass-error budget |
| GELSA demonstration | A possible custom spatial/spectral separation route | A validated survey velocity catalogue or a measured flat outer speed |

The general PHZ inference uses a Chabrier IMF; ECLIPSE D uses Salpeter. Both employ fiducial distance/population assumptions. These cannot be mixed without conversion. Stellar mass is not stellar-plus-gas mass. [Enia et al.](https://pubs.euclid-ec.org/public/dr1/enia.pdf), [Nersesian et al.](https://pubs.euclid-ec.org/public/dr1/nersesian.pdf).

Redshift validation is selection dependent. Deep, bright spectroscopic subsets do not establish universal purity for the wide/faint catalogue. Object and solution-rank joins must be respected. [Hartley et al.](https://pubs.euclid-ec.org/public/dr1/hartley.pdf), [Le Brun et al.](https://pubs.euclid-ec.org/public/dr1/lebrun.pdf).

## 2. The concrete ECLIPSE sample audit

The [public ECLIPSE archive](https://doi.org/10.5281/zenodo.19654904) was reachable. We downloaded the 3.66 MB object catalogue and 26.97 MB physical-property archive and verified their published MD5 checksums, also recording SHA-256. The large image partitions and 236 MB model archive were not needed for this metadata audit.

The object table has 26,662 rows. The D key table has 15,072 A/B rows; all join uniquely with matching grades. The cumulative quality selection is:

| Stage | Rows |
|---|---:|
| All A/B | 15,072 |
| Grade A | 6,073 |
| Consensus-success lens model | 4,098 |
| Also D final-sample flag | 3,202 |
| Also valid mass/light metadata and no large-system warning | 3,202 |
| Also vetted positive DESI deflector redshift | **39** |

These 39 are candidate deflectors, **not 39 usable gravity tests**. Row-level source-redshift linkage is absent from the inspected small archives, including the full D FITS. The paper reports 20 DESI paired systems, 12 grade A before our cuts; their clean intersection is unknown. The count of clean two-redshift systems is therefore null/undetermined, not zero and not 39. The “at most 12” bound refers only to that reported DESI grade-A paired subset. [Lines et al.](https://pubs.euclid-ec.org/public/dr1/lines.pdf).

One named system, PS1J1821+7130, matches EUCL-DR1-L015763 within 0.111 arcsec and has a source redshift from Bergamini et al. It fails the strict D detection-quality flag despite good model votes. It cannot quietly be promoted into the clean sample. [Bergamini et al.](https://pubs.euclid-ec.org/public/dr1/bergamini.pdf).

We found three definition issues to settle before physical inference: the D README and paper differ on whether available spectroscopic redshifts were used in SED fits; they differ on circularized versus non-circularized radius wording; and formal model bounds in the archive are not the calibrated individual-error treatment deferred in C. The audit records these conflicts rather than choosing the convention that improves a result. [Nightingale et al.](https://pubs.euclid-ec.org/public/dr1/nightingale.pdf).

The [audit](sample_access_audit.md), [machine-readable record](sample_access_audit.json) and [reproducer](audit_eclipse_catalogs.py) contain exact predicates, identifiers and hashes. These are metadata quality cuts applied before formula scoring, not a sealed preregistration. Selecting successful SIE reconstructions may induce model-dependent selection; it must be conditioned on or modelled in population claims.

## 3. Which Zimmerman claim is under test?

The current headline relation is

\[
a_0(z)=\kappa c\sqrt{G\rho_{\rm DE}(z)},\qquad \kappa=1/2\ \text{adopted/fitted}.
\]

The canonical normalization is approximately 9.36×10⁻¹¹ m s⁻². The older alternative total-density normalization, approximately 1.13×10⁻¹⁰, is a distinct footing. Neither may be selected after inspecting a residual. See the repository's FRAMEWORK_EQUATIONS_2026-10-15.md and research_closure_2026_11_12/three_model_review/REVIEW.md.

With constant κ,

\[
\frac{a_0(z)}{a_0(0)}=\sqrt{\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}}.
\]

Constant vacuum density means constant a₀, even while H(z) changes. A prediction proportional to H(z) is a competitor, not this formula. Recovering dark-energy density from BAO requires an expansion model, matter-density information and consistency assumptions.

The scale relation does not by itself fix an interpolation kernel, metric light deflection, external-field response or cosmological growth. For example, the quadratic rule and simple-μ rule are different:

\[
g^2=g_b^2+a_0g_b,\qquad
g_b=\frac{g^2}{g+a_0}.
\]

At g_b=a₀ they differ in g by about 14.4%. A SPARC fit with one cannot validate a lensing action that implements the other. A lensing test must specify the metric potentials as well as the nonrelativistic force law.

## 4. Existing predictions and results: do not reset the evidence

The bounded search covered **48,432 Markdown/Python files**, excluding archived/snapshot copies, environments, duplicate evidence inputs and this review. We inspected 20 prediction-bearing records with 48 source references. [prior_lane_inventory.json](prior_lane_inventory.json) gives paths, line spans, hashes, qualifications and statuses; [search scope](prior_lane_search_scope.json) preserves terms and matched paths. This is broad coverage, not a proof that no undiscovered lane exists. A no-match for case-sensitive “ECLIPSE” or slitless velocity terms is not a literature novelty result.

| Prior lane | Recorded result/prediction | What carries into Euclid |
|---|---|---|
| A55, then A80 | Fixed-IMF Einstein radii were too small; changing measured-versus-assumed Sérsic shape can materially alter the residual | Reproduce with independent light profiles and a clear total/aperture stellar-mass convention |
| A85 | Lensing-calibrated stellar normalization predicts aperture dispersions with mean −2.33%; scatter 13.29%, χ²/N=3.89 | Conditional mean consistency exists; neither a fixed-baryon pass nor a κ measurement |
| CFG710/712/713 | One blind lens had slope success but axis-ratio failure; population slopes were too steep; an IMF-only remedy failed in that model | Include an independent profile-shape gate, not just mean radius/dispersion agreement |
| SP1 / SP2 | Sealed mass-switch and environment-step predictions for retired route E | Preserve the seals and owner instruction to score the historical predictions; do not attribute them to the current plain law |
| PR-F4 | Lens-redshift split at 0.5, testing a conditional formation-dependent radius | Already on record; needs calibrated shear/high-redshift lens coverage and other model gates |
| GATE1 / E13 | Weak-lensing RAR and photon normalization tests | Baryon systematics exceed the small distinctive normalization difference; matching a common deep slope is not unique confirmation |
| D2 cluster kink | Retired target: exterior differential signal identically zero in that branch | More stacking cannot recover an identically zero signature |
| CT4 / AT1 / KC1 | Colour/environment lensing residuals, high-z common-mode limits and coefficient-precision requirements | New imaging does not erase measured-gas or precision requirements |
| CFG681–689 / DW1 | DESI BAO and the November Milky Way profile already analysed | Updates must identify genuinely new inputs and retain calibration/covariance caveats |

A80's shape correction is conditional: a total-SED-mass anchor allows the old trend to vanish near n=6.09, while a fixed aperture-mass interpretation behaves differently. Fitting n from gravitational residuals is not measuring n. A85 calibrates one stellar boost per lens using its Einstein radius, so its dispersion prediction is a cross-observable test rather than an absolute stellar-mass prediction. Its κ–mass degeneracy remains broad.

The CFG712 slope comparison used a specified kernel, n=4 and a local-to-global slope mapping. It is an essential adverse predecessor to reconstruct under one common forward model, not automatically an identical-model rejection of every A85 successor. C's fixed SIE slopes cannot resolve it; arc-image refits with flexible profiles are necessary.

**Integrity issue in SP1/SP2:** the frozen rejection inequalities say “below” a midpoint even though the predicted step is itself below that midpoint; SP1's README says “above.” Prediction hashes match their seals. Preserve this conflict. Any prospective clarification must be dated before examining the relevant signal, retain the original, and distinguish original from amended scoring. We did not edit or score those gates.

## 5. DESI: which part is actually new?

The [DESI public-paper page](https://data.desi.lbl.gov/doc/papers/) distinguishes released paper products from the underlying DR2 spectra/redshifts, which it still describes as unreleased. Public DR1 remains available for object-level work. “DR2 exists” is not equivalent to “every DR2 spectrum is public.”

| DESI material | Date | Repository implication |
|---|---|---|
| DR2 BAO/cosmological likelihood products | 19 March 2025 | Already used in CFG681–689; not a new validation today |
| Lyα full-shape/AP geometry | 30 July 2026 | A potentially material replacement for the older correlated Lyα pair |
| Milky Way halo mass-profile paper | 4 November 2026 | Already examined in DW1 and subsequent November 12 corrections |

The BAO public product contains 13 observables: one D_V/r_d and six correlated D_M/r_d, D_H/r_d pairs. In the July Lyα paper, at z=2.33, D_M/r_d=39.32±0.33 and D_H/r_d=8.600±0.066, correlation 0.225. The older CFG681 pair was 38.988±0.531 and 8.632±0.101 with correlation −0.431. An update must replace overlapping information or use its joint likelihood, not add it as independent evidence. [DESI DR2 products](https://data.desi.lbl.gov/doc/papers/dr2/), [Results IV, Eq. 26](https://arxiv.org/html/2607.27410v3#S5.SS3).

CFG689's a₀(z) bands depend on Planck early-density priors, a CAMB ruler and cold-mass conservation. Constant dark energy survives its stated uncertainties. BAO alone does not measure a₀ or model-independent ρ_DE, and this conditional reconstruction does not prefer Zimmerman over ΛCDM.

The [Milky Way paper](https://arxiv.org/html/2611.05518v1#S6.SS1) supplies a 20–80 kpc profile and M(<80 kpc)=6.36(+0.53/−0.48)×10¹¹ solar masses. Its NFW-extrapolated M200 is not a direct measurement of M(<200 kpc). The profile covariance and mock calibration matter. DW1's recorded agreement is not an unrestricted pass; two instrument checks fail. The newer local correction report withdraws an earlier AQUAL rescue caused by mixing physical and Newtonian external fields. That correction is recorded, not rerun here.

## 6. Does any inspected completion already pass all gates?

**No inspected record establishes that.** This statement is scoped to the current review and linked evidence, not a universal nonexistence theorem.

| Candidate | Surviving content | Missing or adverse evidence |
|---|---|---|
| Bare scale relation | A useful acceleration-scale correlation and conditional redshift rule | Not a force law, metric, action or growth model |
| Quadratic empirical law | Recorded galaxy-fit success on specified nuisance conventions | Cannot inherit simple-μ lensing/action results |
| AQUAL/QUMOND simple-μ | Defined nonrelativistic field equations and conditional lensing/dynamics work | Matched external fields remove the earlier large MW rescue; metric and other scales remain separate obligations |
| Screened v3s | Some local-gravity gates pass | Galaxy χ², cluster/cosmological and other documented gates do not all pass |
| Native rule N / retired route E | Some historical conditional fits and sealed forecasts | Removal of the a₀ floor changes the claim; failures and the owner retirement remain |
| Healthy scalar candidate C (CT7) | Local constancy and weak-field gates under conditions | Tracks potential V rather than total ρ_DE; the attempted exact-density portal has a health failure in this construction |
| Conserved cold/retention candidates | Conditional static identities or selected linear constraints | Formation, amount, stress, retention and full likelihood consistency are not supplied by those identities |
| Corrected G242 environment route | A radius-ratio inequality can open with specified assembly growth | No derivation of the environmental field/history or full joint forest/lensing pass |

Current anchors include the November 12 three-model review and combined_route/deepseek_corrections/REPORT.md, V3S_FINAL_VERDICT_2026-10-24.md, the October 31 no-floor and November 1 retirement decisions, and CT7_REPORT.md. A pass may not be transferred between different kernels, components, boundary conditions or data likelihoods.

## 7. Executable sequence and discovery standard

1. Freeze the model's kernel, metric light-deflection rule, acceleration footing and baryonic convention before scoring. Keep absolute mass, shape and independent dynamics as separate gates.
2. Resolve the ECLIPSE definition conflicts and source-redshift joins. Refit light and stellar populations at verified lens redshifts using targeted images, PSF, noise and masks. Condition on the model-success selection.
3. Test the fixed stellar-mass prediction of lens images. Separately, if using lensing to calibrate mass, predict held-out profile information or independent dynamics; do not relabel that calibration as an absolute-mass success.
4. Require the same model to face the CFG712-type slope residual, population scatter and radial coverage in Einstein-radius/effective-radius ratio. A common mean alone cannot pass.
5. Pursue the exploratory nuisance-cancelling routes in the research records. Each must expose identifiability conditions, a counterexample and the measurements needed to distinguish competing predictions.
6. Execute the sealed weak-lensing gates only when calibrated shear and a resolved scoring convention exist. Reuse existing lanes rather than claiming their predictions were newly invented today.

A breakthrough would be a new, independently checked mechanism or a discriminating measured result that survives these controls. The release provides concrete new inputs and research directions; it does not itself establish that result.

## Reproducibility and publication scope

The comparison uses the shared local checkout, including previously existing working-tree research. Hashes pin the evidence actually read; source paths may refer to files not yet present on the publication branch. No historical result was rerun merely because it was cited. The metadata selection is reproducible without network access once the two public ZIPs are downloaded:

    python3 audit_eclipse_catalogs.py --data-dir /path/to/downloads --reference sample_access_audit.json --output sample_access_reproduced.json

The IRSA mirror exposed only Q1 tables in our live schema query; its DR1 overview returned 404. ESA release pages and the public papers were accessible. This is an access limitation of that mirror, not evidence against the release.

Publication uses codex/euclid-desi-review-2026-11-12, based on remote main, with an isolated Git index. The shared dirty/diverged checkout is preserved. New research checkpoints are pushed as they land; no main-branch integration is implied.
