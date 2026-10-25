# CCT-009: collapse excites the supported modes, but has not selected a safe four-dwarf remnant

**The transport mechanism is active in the finite coherent field calculation. Nonspherical self-gravity populates higher angular modes and the reference supported radial subspaces; outward waves remove positive energy and aligned spin. The incoming-pulse history improves on the old bound collapse. It still does not produce a stable observed four-dwarf solution, and a passive stellar stress test exposes substantial orbital excitation.**

This is the new, conditional CCT selectively coupled wave candidate at common eta=1500 pc km/s, not a result for current v3/AeST or retired SCT-M. Initial catchment and length scales remain assumptions tied to formed stellar mass and present stellar radius. They are not derived assembly histories. `MECHANISM.md` gives the equations, energy/geometry distinctions, continuum mass–energy bound and the exact bridge obstruction to the previous statistical endpoint.

## Frame audit: the cloud origin is not automatically a galaxy centre

The full field develops off-centre wells. In Draco the cold-potential minimum is ~173pc from the original origin at t=60 and ~428pc at t=120, with a second symmetry-related well. Its total COM is much closer to the origin. This is fragment-like/internal structure, not simply uniform translation. Recentring the instantaneous stellar monopole diagnostic on a well changes the late Draco value from 6.90 to 7.74km/s; it still does not reproduce 9.55. The mass within193pc around that well is3.39million Msun, compared with0.786million about the old origin.

Sextans' late well shifts by113pc. Recentring changes its canonical survey difference only from72.58 to71.66. The radial-retention failure persists in that diagnostic.

All original-origin aperture, time-average and passive-probe results below retain that stated reference frame. **They cannot be read as heating or disruption of stars following a moving fragment.** A material-fragment centre, its bulk velocity and the actual stellar centre must be tracked. High-l power can describe a translated/fragmented clump as well as angular support; angular growth alone does not prove formation of one extended equilibrium halo. Likewise J about the original origin includes fragment orbital angular momentum and is not automatically intrinsic fragment spin. See `centering.json` and the equations in `MECHANISM.md`.

## The mode-transfer question has a positive finite answer

At t=15 in matched source-free Sextans histories, full nonspherical gravity moves 35.74% of the initial mass into l>4, whereas the matched L=12 monopole-only force leaves only 7.6e-26 there (roundoff level). Both have the higher-l modes available and pass the 1% energy/spin checks through that interval. Doubling radial resolution and halving dt gives 36.28% at t=15 and 50.67% at t=20, compared with 50.57% at t=20 in the original full run. Those percentages are finite-basis results, not continuum predictions.

A second assay projects the actual initial/final coherent waves onto orthonormalized samples of the OCCUPIED reference radial eigenfunction spans from CCT-008. No population is reset during collapse. For the incoming-pulse histories:

| Reference-subspace squared overlap, in Msun units | Initial | Late state |
|---|---:|---:|
| Draco | 569 | 14.26 million |
| Sextans | 303 | 21.68 million |

These are finite projection norms in a specified reference potential, not independently identified parcels or a certificate for the actual nonlinear bound spectrum. The reference occupation fit is nonunique. Projection ranks, conditioning, represented angular sectors and norm bounds are saved in `supported_projection.json`.

## Incoming binding history changes the result

Three source prescriptions were tested without altering the reference profiles: the old bound cloud plus paid gas-cycle work; a source-free cloud with total binding -0.001 times its initial self-binding; and a source-free local escape-speed WKB pulse. The last has positive initial total energy and leaves a negative-energy remaining field while exporting net positive energy. This is collective binding in the finite experiment, not proof of capture from a pure positive-spectrum continuum.

The escape recipe uses a LOCAL 10km/s test-potential reference. Its equivalent initial COLLECTIVE energy speeds are 62.09km/s for Draco and 37.10km/s for Sextans. Self-interactions carry a factor 1/2 in the total Hamiltonian; therefore this is not a common 10km/s far-field energy supply. A physical source/merger history must provide the measured initial total energy. Initial monopole negative-spectrum weights are 9.17% and 3.74%; neither is a certificate for the nonspherical Hamiltonian.

After 120 source dynamical units (149Myr Draco; 636Myr Sextans), the incoming-pulse runs give:

| Finite-run quantity | Draco | Sextans |
|---|---:|---:|
| Remaining cold mass | 372.81 million Msun | 325.40 million Msun |
| Mass removed at absorber | 64.27% | 64.21% |
| Initial aligned spin removed | 51.51% | 71.80% |
| Original-aperture Jz/M / incoming specific J | +1.108 | -0.0733 |
| Mass inside stellar half-light radius | 0.786 million Msun | 6.371 million Msun |
| CCT-008 reference mass inside that aperture | 11.615 million Msun | 8.623 million Msun |
| Cold half-mass radius | 2.145kpc | 5.412kpc |

The late Sextans original-axis aperture has very little net aligned spin, with compensating spin in the outer field. Its well remains on that axis; the off-axis Draco wells require a separate intrinsic/orbital decomposition. That is a useful formation effect. But it retains only 19.25 million Msun inside 972pc and 31.99 million inside 1458pc, versus the reference 50.99 and 115.56 million. Its problem is radial retention in the survey region, not just total inventory or spin capacity. Removing more mass cannot alone fill that region.

Draco illustrates why one snapshot is insufficient. At t=60 its equilibrium stellar-dispersion diagnostic was 9.27km/s, close to the observed 9.55. The extended run varies between 6.90 and 11.17km/s in the last quarter; its mean-potential diagnostic is 9.21km/s. That is one global-moment clue, not a resolved-profile or stability pass. The compact reference profile is illustrative and is not an independent observational total-mass floor for all extended Draco halos.

## Actual Sextans survey comparison

The recorded cold profiles were scored against the same 298 selected velocities, radii and metallicities as CCT-006, with fixed tracer assumptions and mean/population fraction nuisance fits. This uses the actual source catalogue, not an invented global mass requirement.

The incoming pulse improves substantially over the bound history, but does not retain that improvement:

| Canonical isotropic monopole diagnostic | 2 Delta NLL above reference |
|---|---:|
| Bound history, t=120 final | 208.00 |
| Incoming pulse, t=60 final | 30.07 |
| Incoming pulse, t=120 final | 72.58 |
| Incoming pulse, t=120 late-mean potential | 110.69 |

Posthoc beta=-0.5 and alternate-footing checks remain worse than their corresponding fixed-beta reference fits: at t=120 final, the smallest reported difference is 55.68; for late means it is 96.32. Footings are scored separately. These descriptive likelihood differences are not converted into significance probabilities or a full nonspherical DF exclusion.

## Fixed-origin stellar approximation: a stress check, not physical heating

The failed original profile/stationarity gates were NOT relabeled as passed. A separate posthoc test checks whether replacing the measured varying force by its mean is harmless for passive circular stellar cohorts. Each cohort starts circular in the future-window mean potential, with a Plummer radial sample truncated at six tracer scales. The cold monopole then varies according to the saved history; baryonic gravity is held fixed. This is neither a live DF nor a reconstruction of observed stellar orbits.

For Draco, probes starting at t=60 and t=90 end with 3D tracer half-mass radii 1.606 and 1.440 times their initial values. Median final radial speeds are 11.51 and 9.40km/s. Relative to the static mean potential, the median radial excitation is 1.185 and 0.540 times initial circular-speed squared. Static-mean controls remain circular. The final expansion is an instantaneous/coherent response, not an established irreversible heating rate.

Sextans' earlier cohort also changes substantially: compact and extended tracer half-mass radii end at 1.704 and 1.286 times their initial values. Later cohorts change much less (1.009 and 1.048), but their background still fails the survey profile test. Changing the birth epoch is not a demonstrated physical selection mechanism.

Halving the probe timestep leaves these results nearly unchanged in the SAVED interpolated force. It does not establish cold-force cadence convergence, live stellar self-gravity, nonspherical torques or backreaction. The experiment defeats a claim that this FIXED-ORIGIN mean force automatically reproduces its varying counterpart. The frame audit prevents interpreting it as a co-moving fragment stellar-heating verdict. A near-correct time-mean dispersion still does not establish real-star protection.

## Fornax and Leo I have no matched successful control

The bound-history finite controls still produce excessive global stellar-gravity diagnostics: 46.06 vs 12.1km/s for Fornax and 52.01 vs 9.29 for Leo I. Their L=8 edge populations are large; these are failed finite stress diagnostics, not converged astrophysical exclusions.

The near-marginal binding preflight also fails the chosen compact inventories: it starts roughly 119 and 38 times more tightly bound than their target energies, respectively, before any positive-energy wave loss. The escape-pulse control preflights are energy-admissible, but their full matched Fornax/Leo I capture histories were NOT run. There is therefore no four-dwarf selector pass.

## New equations that constrain the continuation

- A history emitting only nonnegative-energy diffuse outflow must satisfy E_initial+W_external >= E_target. The old oversized bound cloud cannot reach an arbitrarily weakly bound small inventory merely by stronger cooling. Negative-energy self-bound ejecta or another paid receiver change the bookkeeping and must be identified.
- For an isolated star-free continuum field, completing a square gives E >= -G²M³/(8 eta²). A remnant's retained mass cannot be chosen independently of its binding and gradient stress.
- A pure-wave correlation operator evolves by a commutator and remains rank one. The literal high-rank statistical CCT-008 endpoint is not created by closed pure-wave evolution or a deterministic absorber. A coherent stationary alternative, or a justified time/ensemble averaging bridge, is required.
- Averaging gravity leaves negative correlation binding energy. The finite windows also include ongoing mass loss. The measured monopole contribution is approximately 0.74% of mean binding-energy magnitude in late Draco and 0.31% in late Sextans. It is not energy radiated away. Full nonspherical correlations also matter. Gravity is sourced once throughout.

## Numerical interpretation and audit

Independent checks cover direct Green kernels, transform inverses, dense Hermitian exponentials, energy gradients, torque, Parseval energy, Fourier representations and restarted-field equivalence. Main runs close their finite energy/spin/mass ledgers; the two monopole control ENDPOINTS fail the stricter 1% energy gate and are retained as failures. Their earlier matched t=15 interval is valid for the mode-generation comparison.

Increasing mmax from4 to6 materially changes mode populations, while leaving both early Sextans profiles much too concentrated. Radial/dt refinement preserves the high-l population but substantially changes central mass. Late export fractions and aperture values are therefore finite-run diagnostics, not physical predictions. One positive-energy absorber and outward flux are not an asymptotic/boundary-convergence certificate. No thresholds or old failures were edited.

`PROTOCOL_ADDITIONS.md`, `REVIEW.md`, raw JSON/NPZ states and `CLOSEOUT_RECEIPT.json` preserve source revisions, posthoc branches and unresolved checks. Largest observed process RSS is about207MB, below1GB. Shared jobs, publications, automation and remote repository state were not changed.

[Diagnostic figure](formation_diagnostics.png)

**Next decisive work:** an energy-paid initial supply and azimuthal/radial-converged capture history that retains Sextans mass at 0.5–1.5kpc; fragment-centred mass/momentum/intrinsic-spin tracking and a settled/coarse-grained field whose averaging bridge conserves correlation energy and gives acceptable moving-frame stellar response; and matched Fornax/Leo I controls. More high-l power alone, or a correct total mass or global dispersion at one time, is insufficient.

An additional action-level host preflight is saved in `host_threshold.json`. Because the stated selective Xi coupling accelerates stars and cold mass differently, unchanged co-moving profiles require an internal restoring bound. The reference Sextans profile reaches that necessary bound at a spherical host baryonic SOURCE MASS of~3.99e10Msun (canonical) or~3.25e10Msun (alt), using its actual Galactocentric distance. No Milky Way source mass is adopted here and no observational exclusion is issued. This must be checked in a full model-native host calculation.
