# A resolved kinematic test of the extra speed

19 October 2026. LRP-PROFILE-1. Base review revision: `18a81657e3e77d81f152fa73ca558dbc85ab6414`; the shared repository advanced during this review. This is a mathematical discriminator for CFG856/857, not an observational validation or a new derivation of the galaxy law.

## Global moments have an exact degeneracy

Let a stationary spherical tracer have density nu(r), total tracer weight L, radial stress p=nu sigma_r^2, and anisotropy beta. Use the same tracer weight in the velocity moment. Let g(r) be the inward total acceleration. Suppose the moments exist and r^3 p vanishes at both endpoints. Spherical Jeans is

    p' + 2 beta p/r = -nu g.

Multiply by 4 pi r^3 and integrate. The boundary terms give

    integral 4 pi r^2 (3-2 beta) p dr
        = integral 4 pi r^3 nu g dr.

Angular averaging one Cartesian velocity component supplies the factor 1/3. Therefore the whole-tracer line-of-sight second moment S satisfies

    3 S = (4 pi/L) integral nu(r) r^3 g(r) dr = <r g>_nu.

No velocity-isotropy assumption is required here. Streaming must be included in the second moment or removed by a consistent stationary nonrotating model. Finite apertures and unmatched selection weights do not automatically obey this formula.

For an additive force g=g0+V_x^2/r on the occupied tracer domain,

    S - S0 = V_x^2/3.

This is independent of tracer density and anisotropy. A spatially constant, zero-mean LOS contamination with independent variance b^2 gives the identical global moment when b^2=V_x^2/3. With multiple populations, the equivalence requires the same b^2 in each; their residuals must then agree. Unequal residuals refute both simple descriptions, subject to the equilibrium, baseline and weighting assumptions. This does not prove that any actual measurement floor exists.

Consequently a nearly universal V_x inferred from one dispersion per galaxy neither establishes an isothermal mass profile nor distinguishes it from an additive variance. The half-light estimator in CFG856 is only an approximation to this whole-population identity, so this statement is not a claim that its reported V_x equals a newly estimated virial amplitude.

The projected virial method is established prior art: Agnello and Evans, *A Virial Core in the Sculptor Dwarf Spheroidal Galaxy*, arXiv:1205.6673v1, section II, equations 3–5. The exact-version HTML was checked on 19 October 2026: https://arxiv.org/html/1205.6673v1. The local `sol61_push/cfg853_independent_transport_2026_10_19/VIRIAL_DERIVATION.md` already develops a different two-tracer finite-mass bound. That bound and its conditional observational applications are not new results of this review. The present addition is the explicit constant-variance degeneracy and the following resolved-kernel check; no global novelty is claimed.

## A resolved Jeans kernel distinguishes the two moment models

As an illustrative mathematical fixture only, take a Plummer tracer nu proportional to (1+r^2/a^2)^(-5/2), isotropic incremental stress and zero stress at infinity. The response of its Jeans second moments to V_x^2/r is

    delta p(r) = V_x^2 integral_r^infinity nu(s)/s ds,

    delta[ Sigma(R) sigma_los^2(R) ]
      = 2 V_x^2 integral_R^infinity nu(s) sqrt(s^2-R^2)/s ds.

The second formula follows by interchanging the two pressure/projection integrals. Write y=R/a. Dividing by the Plummer surface density yields delta sigma_los^2=V_x^2 F(y), with

    F(y) = (3/2)(1+y^2)
             [2/3+y^2-y(1+y^2) arctan(1/y)]   (y>0),
    F(0)=1,   F(1)=5-3 pi/2,   F(infinity)=1/5.

For a stable alternative integral set q^2=y^2/(1+y^2):

    F(y)=(3/2) integral_0^1 (1-u^2)u^2/[q^2+(1-q^2)u^2] du.

The luminosity-weighted aperture integral is

    integral_0^infinity 2y F(y)/(1+y^2)^2 dy = 1/3,

consistent with the independent global virial derivation. A constant LOS variance has no such radial variation. However this radial formula depends on isotropy; it is not an anisotropy-independent prediction.

**Physical admissibility matters.** An unsoftened logarithmic central potential and an exactly flat Plummer tracer core do not admit a nonnegative isotropic distribution function. Indeed any nonzero energy interval of such a distribution contributes density proportional to at least sqrt(-Phi) as Phi tends to minus infinity. These formulas are therefore a Jeans-moment fixture and an implementation check, not a constructed physical stellar model. A finite core, admissible stellar distribution, anisotropy and selection must be included before applying a radial prediction to observations. The companion kinetic analysis adds a second central-consistency condition when the adopted law itself gives g0 proportional to r^(1/2).

## Finite verification and continuation

The script `check_profile.py` compares the analytic expression with direct LOS and compact-domain quadratures at nine named radii. It separately integrates the whole-tracer moment and checks three characteristic values/limits. The main run passes 13 checks; largest pointwise discrepancy is about 1.04e-12, and its aperture integral is 0.3333333333333333. These are floating-point cross-checks of the derivation, not certified interval bounds. A deliberate 20 percent change to the analytic response is tested separately and must fail the projection comparisons.

Reproduction commands and exact input/output hashes are in `profile_run_001/manifest.json`; `profile_contract.json` records the finite assertion, versions and tolerances. The mutation record is `profile_mutate_001/manifest.json` and is expected to have run status `failed`.

The existing conditional Sextans baseline packet already makes this diagnostic concrete. In `sol61_push/cfg853_independent_transport_2026_10_19/baseline_run_002/results.json`, its canonical exponential-law case has residual second moments 32.547035 and 89.227294 (km/s)^2 for the two populations. Those central summaries cannot both equal one V_x^2/3, or one common variance floor. This is a conditional algebraic reading of an existing result, not a new observational exclusion: its tracer weights, selected Gaussian widths, geometry and stellar-mass mixture remain the application assumptions stated in that packet. No uncertainty significance is assigned here, and no old scientific script was rerun.

The next physical discriminator is a single selection-aware fit of the resolved positions, velocities and metallicities in Sextans or Sculptor, with consistently weighted populations, a nonnegative stellar distribution and a finite extra-mass component. Compare its held-out resolved moments against a constant-variance observation model. Use the existing Sextans source extraction and finite-stock bounds as conditional inputs, not as already certified whole-population moments. Repeating a one-dispersion-per-galaxy amplitude fit cannot resolve the exact global degeneracy derived above.
