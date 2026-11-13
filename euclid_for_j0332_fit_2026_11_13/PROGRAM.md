LATEST LIVE HANDOFF: ../euclid_for_j0332_followup_2026_11_13/CHECKPOINT.txt. L015780 finite source-capacity/dynamics study and Lean certificate completed; broader breakthrough goal remains active and unachieved. New L002777 archival candidate has actual stellar dynamics but unresolved background identification and failed source/lens modelling. Earlier FOR phase material below is historical; use the aperture-corrected report.

CURRENT CORRECTION (2026-11-13): finite-aperture SED masses were previously compared with infinite Sersic masses. That interpretation is withdrawn. The corrected FOR image fit requires aperture mass8.80e11Msun versus SED6.78e11Msun, about1.31 upper-side error units, under fixed geometry and constant M/L. See ../euclid_for_j0332_followup_2026_11_13/mass_convention/CORRECTED_FOR_REPORT.txt and reweighted_geometry_01. Earlier phase descriptions below are historical. Broader breakthrough goal remains active; no full physical-theory pass is certified.

# FOR J0332 empirical test and Euclid/DESI research

Base checkpoint: Git HEAD `5ffd920204c2588a0a3c72bac6f89b4c69efc4ad`; working tree contains unrelated, uncommitted research. This task writes only this directory. The preceding ECLIPSE screen is an input, not a fitted result.

User target: fit FOR J0332 with the adopted dark-energy-density acceleration relation, including stellar-mass uncertainty; continue Euclid/DESI investigation toward a substantive result and certify any suitable mathematical implication in Lean.

Empirical success means a specified predictive model reproduces the observed images with an adequate noise/source model, while its required stellar mass is assessed against the released stellar-population uncertainty. A flexible fit alone is not confirmation. Disagreement in a restricted galaxy model is not a theorem excluding every completion of the action. Novelty and formal proof are separate obligations.

## Work packages

1. **Image likelihood (root):** obtain calibrated images, PSF, noise, masks and known-model controls. Solve the axisymmetric simple-mu AQUAL equation and project its gradient, then fit the source and lens nuisance parameters. First discriminator: reproduce a known lens model and verify a spherical analytic field benchmark. Scope: isolated, unscreened, stellar mass following measured light, specified deprojection; departures are named explicitly.
2. **Independent mass constraint (mass_constraint):** exact spherical Abel/Einstein-radius diagnostic and released conditional mass uncertainties. First discriminator: required mass versus photometric mass. This is an independent diagnostic, not an image-fit surrogate.
3. **Theory closure (sensitivity_design):** establish the adopted static field equations, screening parameters and boundary conditions; locate a faithful field solver. First discriminator: whether the published/adopted theory uniquely specifies this galaxy's lensing field. An unspecified sector is an interpretation gap, not a numerical failure.
4. **Data audit (verify_radio_news):** provenance, coordinate/shape conventions, noise properties and published-model residuals, independently of the proposed gravity law.
5. **Formal consequence (pending):** identify a mathematically substantive implication actually needed by the empirical analysis, prove it in Lean with explicit hypotheses and no empirical facts promoted to axioms of physical truth. A certificate does not certify the universe or the fit.

The fixed relation is a0 = c sqrt(G rho_DE)/2; canonical a0=9.3603e-11 m/s^2, alternative footing 1.1312e-10. The coefficient is fitted in the adopted record. The current action leaves some screening/boundary choices to be checked. Source and lens spectra are z_s=3.773+-0.003 and z_l=0.986+-0.005. The released stellar mass uses Salpeter and fixed photometric z_l=0.98. Neither its IMF nor its conditional error will be changed silently.

Status: active broader research goal; immediate conditional FOR J0332 image-fit investigation completed. See REPORT.txt for the exact outcome and limitations. Nine conditional algebraic identities now have an independently reviewed Lean certificate. No breakthrough or complete physical-theory pass has been established. Numerical runs retain their own bounded contracts and manifests.

Final phase checkpoint: `gated_posterior_02` passes its registered finite sampling checks. Source-association-gated wide/compact fits give logM12.0333–12.0412 versus the released SED median11.8311: about1.6times the mass, moderate conditional tension. The source-window audit recovered demagnified branches, so mass inference must explicitly condition on the released association gate. This is not a source-prior-independent mass measurement. Exact flux/mass-sheet identities are certified; empirical theory success is not.

Executed further routes: official DESI VAC crossmatch and a bounded background-line search in recovered L015780 spectra. No verified background redshift recovered. Routes remain open: resolve FOR's light-profile/stellar-population uncertainty with a joint fit and independent imaging; constrain its line-of-sight environment and external-field assumptions; recover paired redshifts and independent dynamics for the Euclid/DESI matches. These are distinct remaining empirical inputs, not unproved Lean lemmas that can be filled by asserting data.
