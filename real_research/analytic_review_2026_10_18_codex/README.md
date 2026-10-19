# Analytic extensions of the Zimmerman framework

18 October 2026. Checkpoint ZAR-2026-10-18-01. Review baseline: `3c01aa2861bf576f4c2d942251eb9d2f89cae108` in a shared checkout with pre-existing changes.

The most useful extension found here is a **kinetic model of tethered and free cold mass whose sum preserves the deep halo law**. It supplies reciprocal spherical forces, an explicit family of stationary distributions, and a relation between the population fraction and their velocity dispersions. It does not select that fraction, form a finite halo, derive the vacuum coefficient, or establish observational agreement.

Two complementary results make this direction testable without another simulation: an exact shape test that eliminates several shared calibration factors, and a lower bound on the donor volume required by mass conservation. No scientific scripts, registered statistics, simulations, or array analyses were run in this review. Existing jobs, frozen files, and criteria were left alone.

## What the recent evidence actually establishes

This is a focused review of the newest canonical statements, corrections, mechanism records, and selected underlying evidence. It is not an audit of every experiment. A large collection of experiments contains related implementations, shared inputs, post-preview choices, and repeated hypotheses; its size is not a count of independent confirmations.

| Question | Current reading | Evidence |
|---|---|---|
| What sets the scale? | The framework proposes a0 = kappa c sqrt(G rho_DE). kappa = 1/2 remains fitted. The vacuum offset, particle mass, response coefficient, and cosmic abundance cannot be identified by notation alone. | [Parameter coverage](../../sol61_push/coefficient_coverage_2026_10_15/COVERAGE.txt); [same-substance result](../../sol61_push/same_substance_2026_10_15/RESULT.txt) |
| Does the static law select a physical halo? | Static radial balance is substantially better understood than formation. Warm carrier support, finite supply, interfaces, and transfer remain separate obligations. | [CFG747](../../campaign_fresh_gravity/CFG747_collisionless_relaxation/README.md); [CFG749](../../campaign_fresh_gravity/CFG749_angular_momentum/README.md); [current work order](../../sol61_push/THEORY_NEXT_STEPS_2026-10-15.md) |
| Is there a two-sided attractor? | Not established as broadly as the frozen summary says. The reviewed demonstrations use radial shells and special boundaries; surplus ejection can overshoot into a deficit. | [Canonical corrections C5](../../campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14_CORRECTIONS_2026-10-16.md) |
| How is mass supplied? | Canonical v2 replaces a per-galaxy share by catchment supply. Retention is an input. A universal sharp edge at one galaxy's cosmic share is superseded in that version. | [Canonical v2 S3](../../campaign_fresh_gravity/THEORY_CANONICAL_2026-10-16.md) |
| Are cluster cold masses forced negative? | That particular conclusion used incompatible deficit definitions. The corrected accounting has positive cold mass; this does not remove the separate profile failures. | [CFG453](../../campaign_fresh_gravity/CFG453_t15_deficit_units/README.md) |
| Does freeing expelled material solve the excesses? | No. The recorded galaxy and cluster tests leave failures. Radial tether-unbinding has the wrong class ordering and releases material from the halo rather than retaining a free core. | [Canonical v2 S4](../../campaign_fresh_gravity/THEORY_CANONICAL_2026-10-16.md); [CFG837 derivation](../../campaign_fresh_gravity/CFG837_shell_bound_fraction/DERIVATION.md) |
| Has nonlinear carrier formation been demonstrated? | The inspected 1D run has transient field clumping. Its stored final intensity peak I/I_initial is 1.0391, where I = abs(Psi)^2; this is not by itself a measured cold rest-mass or charge-density peak, or a population of settled 3D droplets. ARGON11 is queued in the latest status read here. | [Clumping summary](../../sol61_push/closure_particle_bridge_2026_10_16/clumping_figure_summary.json); [field definition](../../sol61_push/closure_particle_bridge_2026_10_16/nonlinear_charge_clumping.py); [ARGON11 status](../../argon_push/ARGON11_nonlinear_fragmentation_2026-10-17/STATUS.md) |
| Do the several interpolation formulas agree? | No. The simple action law, quadratic a0-line, and exponential RAR kernel are distinct away from their asymptotes. Their successes cannot be interchanged. | [Framework equation inventory](../../FRAMEWORK_EQUATIONS_2026-10-15.md); [frozen canonical S2](../../campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md) |

The October 12 mechanism synthesis is useful history, but later stiffened-action work changes parts of its structural fork. Likewise, ARGON08's one-field, response-time, and photon-line language is stronger than the later source/force and same-substance audits support. Use the dated successor with its hypotheses rather than averaging incompatible summaries.

The canonical and alternative acceleration footings remain separate: 9.3603e-11 and 1.1312e-10 m/s^2 in the October canonical record. The new results below are symbolic and apply independently at either positive a0. They do not pool the footings.

## The proposed theory extension

[Kinetic partition derivation](KINETIC_PARTITION.md) makes the following controlled change: the tether responds to tethered mass; all actual mass gravitates. It supplies a conservative, nonlocal spherical energy for that dictionary, rather than assigning a free population an extra gravitational effect without reciprocal work.

In the deep cubic regime, let the total cold profile be M_c(<r) = A r, where A = sqrt(a0 M_b/G), and let a constant fraction f be tethered. The family has

\[
\sigma_t^2(r)=\frac{GM_b(1-f^2)}{3r}+\frac{(1-f)V_f^2}{2},\qquad
\sigma_f^2(r)=\frac{GM_b}{3r}+\frac{V_f^2}{2},
\]

where V_f^2 = sqrt(G M_b a0), and the sigmas are one-dimensional dispersions of the **cold carriers**, not stars or gas. On its bounded outer branch,

\[
\frac{\sigma_t^2}{\sigma_f^2}\longrightarrow 1-f.
\]

This is an equilibrium compatibility relation, not a derived selector. It shows how warm carrier motion and the total deep law can coexist without adding a complete free halo on top of a complete tethered halo. Positive isotropic phase-space distributions exist for the idealized infinite profiles. Their singular center, infinite mass, omitted finite stiffness, and absent formation mechanism prevent identifying them with physical galaxies.

The serious new obligation is now specific: derive a finite, dynamically stable member and its fraction from a mass/current-conserving carrier action, rather than assigning the fraction from hot-gas content or expelled baryons. Literal charge-changing conversion also needs a charge-carrying receiver. This family does not repair the measured early-type or cluster excesses by itself.

## A cleaner test of the force law

[Shape null derivation](SHAPE_NULL.md) eliminates a common distance/velocity factor, the value of a0, and a common gas conversion for gas-only or fixed-composition baryons. Define q = v_los^2/theta, gas acceleration template h > 0, and z = q^2/h. Then:

| Candidate algebraic law | Necessary three-radius condition |
|---|---|
| Simple action law: g^2 - b g = a0 b | det[z, q, 1] = 0 |
| Quadratic a0-line: g^2 - b^2 = a0 b | det[z, h, 1] = 0 |

These are different tests. They cannot both hold exactly for three distinct h values generated by either positive-a0 law. In practice their separation becomes weak in the deep or Newtonian limit. Radial stellar contamination, warps, correlated velocity errors, and the difference between an algebraic disk rule and a full field equation remain material. A zero determinant also requires positive fitted coefficients to represent a physical law.

This eliminates nuisance factors rather than importing a halo mass inferred under another gravity model. It also deliberately eliminates a0: a success would support the chosen force-law shape, not independently confirm its dark-energy normalization. No observational statistic has been evaluated and no frozen test has been amended.

## A conservation bound for the supplying environment

Assume an initially uniform positive cold density rhobar_c, mass-conserving spherical redistribution, and a final density contrast that vanishes outside r_c. If its enclosed excess within r_e is M_h > 0, positivity of the remaining physical density gives

\[
M_h=-4\pi\int_{r_e}^{r_c}\delta\rho_c(r)r^2dr
\leq \frac{4\pi}{3}\bar\rho_c(r_c^3-r_e^3),
\]

and therefore

\[
\boxed{r_c^3\geq r_e^3+\frac{3M_h}{4\pi\bar\rho_c}}.
\]

The positive inner excess cannot be the entire conserved perturbation. The donor region is part of the model. A compact spherical compensated contrast has DeltaSigma = 0 beyond r_c, whereas an isolated truncated positive mass retains M_h/(pi R^2). A depletion shell need not yield negative DeltaSigma at intermediate radii; projection includes the inner excess.

This sharpens an existing direction, not a new compensation mechanism: [mass-response inventory](../../sol61_push/mass_response_identity_2026_10_15/RESULT.txt) already requires depletion/inflow, and [CFG546](../../campaign_fresh_gravity/CFG546_drained_shell_cluster_lensing/README.md) already forecasts drained-shell lensing with unresolved convergence and diagnostic limitations. Uniform donors, compact compensation, and closed boundaries are extra hypotheses; a measured overdense catchment changes the bound.

## What raw data means for this framework

Raw detector output is not the same as a released observable, and a released observable is not the same as an inferred mass. The useful goal is an explicit forward model whose assumptions can be varied, with no imported halo-fit answer.

| Evidence | What is on disk | Assumptions that remain |
|---|---|---|
| SPARC | Reduced rotation curves and baryonic acceleration templates | Geometry, circular-motion interpretation, gas conversion, stellar mass-to-light ratio, and correlated errors. Shared normalization can cancel in the shape null; radial errors cannot. |
| KiDS cosmic shear | Calibrated xi-plus/minus, covariance, source redshift distributions | Shape/redshift calibration, intrinsic alignments and likelihood choices. CFG596 explicitly retains an inherited initial spectrum/amplitude, background, turnaround table and nuisance priors. |
| Gaia wide binaries | Calibrated astrometry/photometry plus derived pair tables | Distance and mass estimators, perspective correction, orbital population, unresolved companions, selection, and measurement covariance. |
| X-ray cluster masses | Gas/X-ray products and model-based dynamical estimates | Hydrostatic and geometry assumptions where used. A mass deficit from them is not a direct detector measurement. |

Two concrete readiness issues emerged in the existing wide-binary table. All pairs are already non-single-star screened, so that proposed contamination branch is identical to the primary; the catalogue ends below 30 kAU, so a 50-kAU cap does nothing. Also, its stage-G distance/velocity construction differs from the Cookson estimator described in the frozen source disclosure. These are issues to resolve in separately dated pipeline decisions, not permission to change frozen criteria here. See [the data audit](SHAPE_NULL.md#existing-data-and-pipeline-provenance).

The CFG596 KiDS exclusion applies to the implemented source/settling rule under its declared inherited assumptions. Calling those assumptions visible does not erase the exclusion or establish that they caused it. Canonical v2 and the later T1x records concern different tested prescriptions; keep those evidence labels attached to their actual candidates.

## Recommended continuation after the existing jobs

1. **First resolve the algebraic target.** The nuisance-eliminated shape test can distinguish simple and quadratic laws in principle. Check whether existing gas-rich data have transition leverage and a usable covariance before registering an empirical threshold; do not choose radii after inspecting residuals.
2. **Continue the kinetic model analytically.** Match a finite core and finite donor reservoir with continuous stress and counted energy. Then prove or refute stability for that same candidate. If this fails, retain the virial constraint rather than adding an uncounted force or wall.
3. **Make the physical selector earn its role.** Derive mass/current transfer and its receiver. Hot-gas state, merger history, and baryon loss are correlated observables, not interchangeable operators. No new numerical scan is justified before this arrow is specified.
4. **Use full mass contrasts for lensing.** Include the donor/depletion region, lens isolation, and two-halo environment. Test released shear or calibrated observables with the candidate's own forward model, rather than treating an NFW-derived halo mass as raw data.

## Review and novelty status

The kinetic Jeans/phase-space results and shape-null algebra received separate same-team derivations. [AUDIT.md](AUDIT.md) records their precise scope. Agent agreement is not a proof certificate; the arguments are written out for inspection. These are conditional mathematical advances and proposed empirical tools, not a validated new theory.

Prior overlap was checked in targeted campaign, hunt, argon, and sol61 records. Generic shape tests, tethered/free populations, at-rest polarized equilibria, compensation, and the missing source/current bridge already exist. The useful additions here are the explicit constant-partition compatibility family, its spherical reciprocal functional and positive distributions, the exact simple-versus-quadratic null presentation, and the donor-volume inequality. None carries a global novelty claim.

Primary-source checks on 18 October 2026 included the [SPARC paper](https://astroweb.case.edu/ssm/papers/AJv152n157.pdf) and [catalogue definitions](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/AJ/152/157?format=html&tex=true). They support the reduced-observable provenance, not these new derivations. [Stahl et al. 2022, arXiv v1](https://arxiv.org/pdf/2209.07831), abstract and section 3, explicitly studies at-rest polarized equilibria; its different dipolar dynamics do not prove this partition family. Searches for MOND collinearity/determinant tests and dipolar velocity-dispersion equilibria did not establish global novelty. Citation-chain coverage is incomplete.

Input hashes and the no-compute boundary are recorded in [PROVENANCE.json](PROVENANCE.json). No old result, public manuscript, frozen prediction, or shared ledger was rewritten.
