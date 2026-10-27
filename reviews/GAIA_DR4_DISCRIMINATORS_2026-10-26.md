# Gaia DR4 discriminator investigation — 2026-10-26

Investigation of existing predictions plus an analytic diagnostic and bounded force extraction. No preregistration, prediction seal, estimator or decision threshold was changed. Base HEAD: acb2bf5277fc6b69ad79bf731e1e0a199374172a. Review provenance: self-review, not independent audit. No AQUAL galaxy solve was rerun; Newtonian baryonic fields were recomputed on the inherited grids.

## Target and outcome

Target: identify observations accessible to Gaia DR4 that distinguish a specified Zimmerman-framework branch from specified rival families, without confusing survival with unique identification. A successful discriminator requires a branch-specific prediction, rival envelope, observable mapping and error budget. A numerical difference alone does not establish DR4 power.

Outcome: partial progress. There are real pairwise discriminators. A joint radial/vertical force-direction diagnostic extends the comparison from one NFW parameter choice to all spherical halo profiles. Its actual framework template and DR4 power remain to be calculated. No globally unique signature of the latest mechanism has been established.

## Branch identity

- The unscreened v3 static action gives AQUAL, mu(x)=x/(1+x): doors_push_2026_10_22/E2_field_equation/README.md. It is not a new observational force law distinct from all MOND implementations.
- AQUAL illustrative circular, orientation-averaged 20 kAU values: canonical 1.1667 and alternative 1.1986 at the primary external field; 1.1448 and 1.1730 at the alternative external field. These are not full-population estimator outputs.
- Screened D7d at L*=24 pc gives gamma_v-1 approximately 8.1e-6 at 20 kAU. The settling model is registered against the Newtonian-valued Arm C in preregistration Amendment 21.
- Original Arm A population bands, other arms, and the October 22 fork score are separate objects. Use the final Amendment A3 of NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md, not its superseded all-systematics-must-agree A2.
- mechanism_match_2026_10_26/STATUS.md and MATCH.md describe a new nonrelativistic canonical extension with assumed coefficients. The global mechanism remains open. sustained_transport_2026_10_26/STATUS.md records a failed law match in its tested evolution. Neither supplies a completed DR4 population forecast. Dates alone do not prove that these mechanisms supersede every registered branch.

## Route 1: joint Galactic force geometry

The sealed v3 table predicts a disc-concentrated effective extra density: canonical midplane 2.22 GeV/cm^3 versus shell average 0.25, compared with the registered NFW local value 0.338. The shell is a Galactocentric spherical shell |sqrt(R^2+z^2)-R0|<=0.2 kpc, not an average over local stellar heights. These numbers are model outputs, not measurements. See S3_v3_mw_seals/s3_partC_seal.py:p3_local.

The more defensible target is the spatial force field rather than one inferred density. Define signed residual acceleration components at the SAME point (R,z):

    a_R,h = a_R,observed - a_R,baryons
    a_z,h = a_z,observed - a_z,baryons
    D(R,z) = R a_z,h - z a_R,h.

For any differentiable spherical residual potential Phi_h(r), r=sqrt(R^2+z^2)>0,

    a_R,h = -Phi_h'(r) R/r,
    a_z,h = -Phi_h'(r) z/r,
    D = 0.

This identity is independent of halo normalization and radial profile: changing NFW mass/concentration, using a spherical Einasto profile, or choosing a spherical core cannot change it. D has units of squared velocity. It is not useful on the symmetry plane alone (z=0); use off-plane locations with measured radial and vertical forces. Do not substitute the midplane rotation curve for a_R(R,z) without modeling the height dependence.

Sanity and converse checks: for a residual potential (A R^2+B z^2)/2, D=(A-B)Rz; A=B returns the spherical null. D=0 in a finite sample does not prove spherical symmetry everywhere, and azimuthal structure requires an additional a_phi test. The identity holds for the assumed halo component regardless of its stellar tracer equilibrium; recovering the acceleration from tracers is a separate inference problem.

What nonzero D would establish: rejection of a spherical residual halo under the adopted baryonic subtraction and force reconstruction. It would not reject flattened/triaxial dark halos, a dark disc, or every MOND model. Errors in baryonic structure can also generate D. Use joint covariance, spatial bins, multiple tracer populations and a disturbance model. A framework field may violate this null, but that magnitude has NOT been evaluated here.

Why this improves the earlier comparison: it removes the spherical halo radial-profile freedom analytically, rather than treating one fitted NFW curve as all dark matter.

Published context: Bienayme et al. (2009), https://arxiv.org/abs/0904.3893, already propose vertical-force, radial-gradient and velocity-ellipsoid tests of a MOND phantom disc. Thus a disc-like excess is not unique to this framework. Wang et al. (2026), https://arxiv.org/abs/2605.10857, combine rotation and vertical phase-space spirals to compare specified modified-gravity and halo models. Their claimed significance is not imported as a universal exclusion of this framework.

Disposition: highest-priority open route. Next: extract matched off-plane baryonic and v3 force grids, evaluate D for both footings and baryonic variants, then fit flattened-halo rivals to the same grid and construct an observation-level covariance forecast. Existing sealed Kz and midplane Vc values alone cannot do this.

## Route 2: binary mean plus separation-dependent orientation

The aggregate screened/unscreened distinction remains large. It cannot identify a screened medium over a Newtonian halo with the same binary prediction.

A more detailed candidate is the radius-resolved orientation pattern. PREREGISTRATION_DR4.md Amendment 10(d2) records a transition from perpendicular-dominant to parallel-dominant enhancement near r=1.96 r_M for its MG calculation. It gives a projected SAMPLE-level difference only +0.0013 to +0.0046 in velocity-boost units. Older hunt_2026/k04 estimates of several-percent projected anisotropy must not replace this later population calculation. The sign-flip prediction remains branch-specific; conventional EFE models can also produce orientation dependence.

Amendment 20 makes the anisotropy diagnostic unmeasurable if either orientation fit hits a frozen grid boundary. Frozen diagnostic constants include older MI conventions, so theoretical sign and pipeline diagnostic cannot be silently equated.

Disposition: potentially informative shape test, no demonstrated DR4 detection power. Need the same forward model for both rival theories, orientation-dependent selection, binaries/triples and mass distribution. An absence of a subpercent orientation signal is not strong evidence against the model at percent-level errors.

## Route 3: cluster scales, tidal tails and streams

Open clusters bridge binary and galaxy scales and are a plausible screening-scale test, but no sharp current-template claim is justified by the records reviewed.

hunt_2026/h39_open_cluster_tails.py computes an older unscreened-law Jacobi-radius enhancement of about 11%, not a full N-body tail prediction. Its static external-field-gradient tail asymmetry is of order 1e-4 to 1e-3; it does not explain the reported 0.1–0.2 population asymmetry. The source's verbal claim of a 36% smaller inferred mass is also imprecise: if effective G is 1.36 times G, the corrected mass is M_Newton/1.36, about 26% smaller, not 36%. Do not transfer either number to screened v3 without solving its cluster response.

Kroupa et al. (2024), https://arxiv.org/abs/2405.09609, claim leading-tail excess consistent with Milgromian dynamics. Membership selection, Galactic perturbations, escape dynamics and the actual framework force must be simulated before using their claim as ours.

real_research/reviews/v1_stream_memory_kernel.py labels its proposed release-phase memory HYPOTHESIS-WITH-FREE-KNOB. Its stronger verbal contrast with ordinary gravity is not sufficient: even a memoryless gravitational force produces stream populations whose widths and velocities depend on their past stripping histories. Two co-located debris populations with different dispersions do NOT by themselves demonstrate nonlocal inertia. A distinct response must survive matched initial-condition dynamical forward models.

Smooth cold components could differ from subhalo populations in stream perturbations, but a particle-free field need not be fluctuation-free or incapable of bound clumps. No framework-specific substructure spectrum/rate was found in the records reviewed. https://arxiv.org/abs/2502.07781 forecasts stream impact detectability; it is not a prediction that this framework supplies zero impacts.

Disposition: open but not ready for a numerical DR4 claim. The first missing inputs are the cluster response across size/mass/environment and the medium's fluctuation/response spectrum, respectively.

## Route 4: joint-pattern discrimination and its exact limit

A useful comparison vector is (binary mean boost, binary orientation-by-separation, D(R,z), rotation slope, azimuthal force pattern). The screened-v3 candidate could combine near-Newtonian binaries with a disc-linked Galactic response; the unscreened v3 candidate changes the binary coordinate. Neither combination is automatically unique among all dark-sector models.

In the weak-field conservative-force regime, if two models supply the same Phi(x,t), the same luminous tracer initial conditions, and the same non-gravitational physics, then the same equation x_ddot=-grad Phi gives the same stellar trajectories. Astrometric kinematics cannot identify a microscopic particle versus field label in that exact degeneracy. This is a conditional statement about identical potentials, not a claim that arbitrary dark-matter models can physically realize every proposed potential. Poisson positivity, distribution-function consistency, formation history and independent observations restrict that realization.

Thus the actual target is a predicted force/response pattern outside physically allowed rival envelopes, not a new label for the same potential. A joint pattern can distinguish named rivals without uniquely proving the underlying cosmological origin of a0.

## Review and continuation

Analytic spherical-null identity: proved as written under its hypotheses, self-reviewed; no external theorem needed. Its astronomical application is conditional on field inference, baryonic subtraction and branch-specific template. Source extraction and code inspection are not an independent reproduction of the stored galaxy computations.

Checked corrections: shell definition; AQUAL vs QUMOND; population vs illustrative binary; late anisotropy amplitude and boundary gate; old cluster mass conversion; stream history confound; current mechanism scope. The S3 azimuthal estimate uses a pointwise 3-D correction validated on a tilted Plummer test (C5); an earlier grid anisotropy check failed at 0.63%. It is not a precision full Milky Way non-equilibrium calculation.

Next concrete calculation at this initial checkpoint: evaluate D on existing off-plane force grids with a self-consistent baryonic field, identify its covariance with the rotation/vertical data, and optimize spherical then flattened rival families. The first step was subsequently executed below. Preserve the current sealed files. Do not attach a detection significance until the observation-level steps are complete.

## Executed continuation: off-plane force geometry

Code: dr4_force_geometry_2026_10_26/check.py. Contract: contract.json in the same directory. Authoritative results: run_v2/results.json; validated evidence manifest: run_v2/manifest.json. Runner status completed; Python 3.9.6, numpy 1.26.2, scipy 1.11.4; one numerical-library thread, 60-second wall limit. The runner records input hashes before/after, versions, actual runtime, revision and dirty state.

Finite assertion: extract the isolated static v3 census extra field at R=8.122,12,16 kpc and z=0.5,1.1,2 kpc, both footings, on both stored main/fine grids; subtract a Newtonian field solved from the same baryons. No cached AQUAL solve was silently regenerated. Cached residual metadata and cache hashes are retained per row. No randomness.

Define q_eff^2 = z F_R,h/(R F_z,h), where F=grad(Phi) is used here rather than signed acceleration. A spherical halo has q_eff=1. An ellipsoidally stratified potential Phi_h=f(R^2+z^2/q^2) has q_eff=q everywhere with nonzero derivatives. This q is a force-direction diagnostic or equipotential flattening in that restricted family; it is NOT the density axis ratio of a general halo.

Fine-grid canonical values:

| R kpc | z=0.5 kpc | z=1.1 kpc | z=2 kpc |
|---|---|---|---|
| 8.122 | 0.4154 | 0.5347 | 0.6456 |
| 12 | 0.4294 | 0.5517 | 0.6580 |
| 16 | 0.4407 | 0.5715 | 0.6771 |

The alternative footing changes these rounded values by at most about 0.0001. Main/fine maximum differences are 0.000361 canonical and 0.000364 alternative. Both footings show the same height trend despite different extra-force amplitudes.

At R=8.122,z=1.1, the extra vertical force is approximately 3.50 times the vertical force of a spherical residual halo matched to the extra radial force at that SAME point. This is a geometric ratio of the extra force, not a factor of 3.5 in total stellar gravity. The canonical excess over that spherical value is 587.22 (km/s)^2/kpc. A basic source check gives total Kz/(2piG)=92.43 Msun/pc^2 on the fine grid, close to the sealed isolated canonical value 92.5; this does not validate the whole solver independently.

Controls: analytic spherical and q=0.7 logarithmic potentials were passed through the SAME finite-difference/interpolation estimator. Maximum errors in q_eff^2 were 0.00360 / 0.00176 on the main grid and 0.00158 / 0.00077 on the fine grid, respectively. The geometry difference is much larger than these controls' numerical offsets. Initial run used numpy.gradient for controls; run_v2 corrects that control mismatch without changing any framework result. The old run is historical and its script-input hash no longer matches current code; use run_v2.

Outcome label: numerical extraction verified in this stated finite setup, conditional on inherited AQUAL cache validity; self-reviewed. Exact analytic null is proved independently. The extracted field differs from every spherical profile and from every single constant-q equipotential profile over these locations, although neither statement supplies an observation significance. A halo whose shape changes with position can evade this restricted comparison. No baryonic-prior sweep, tilted external-field calculation, realistic halo distribution-function test or DR4 covariance forecast has been run. The findings belong to isolated v3, not automatically to the latest mechanism model.

Updated next obligation: evaluate the same diagnostic over the existing baryonic variants and external-field cases, then fit a physically admissible variable-shape halo and forward-model the off-plane DR4 tracer inference. This is a stronger and more specific continuation than merely refining the original one-NFW rotation comparison.


## Flexible-halo continuation

A subsequent executed comparison finds that a positive-density NFW halo plus an extended Miyamoto–Nagai dark disc matches the isolated v3 forces to 1.08–1.14% held-out RMS, allowing the restricted stellar normalization nuisance. Single oblate NFW density halos remain at 9.16–9.81%. This narrows the earlier discriminator substantially: spherical/constant-potential-shape rejection is not general dark-matter rejection. See [experiment report](dr4_flexible_halo_2026_10_26/REPORT.md), including conditional precision thresholds and the limits of translating DR4 astrometry into force accuracy.
