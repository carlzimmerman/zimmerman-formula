# Can a flexible dark component mimic isolated v3? 2026-10-26

**Yes: an NFW halo plus a positive-density extended dark disc reproduces the tested v3 radial and vertical forces to approximately 1.1% RMS on held-out positions. A single oblate NFW density halo does substantially worse. Gaia DR4 discrimination against the disc-plus-halo model is not established; it requires unusually well-controlled joint force inference.**

This concerns the existing isolated, static v3 AQUAL implementation and its two separate acceleration footings. It is not a forecast for the unfinished newer mechanism, or evidence that v3 fits the real Galaxy. Earlier Milky Way rotation-curve tensions remain relevant.

## Experiment and limits

Target: cached census-baryon v3 potential, sampled on the fine numerical grid. Training: 30 positions, R=7,9,11,13,15,17 kpc and z=0.3,0.7,1.2,2,3 kpc. Validation: 20 different positions, R=8,10,12,14,16 kpc and z=0.5,0.95,1.6,2.5 kpc. Each position supplies both positive potential gradients FR and Fz. Each component is weighted by its own target total force; these are uniform fractional weights, not observed Gaia uncertainties.

Models: spherical NFW; oblate NFW density with q in [0.6,1]; oblate NFW density with q in [0.08,1]; spherical NFW plus a Miyamoto–Nagai disc. All component densities and amplitudes are positive. NFW scale radius is bounded at 0.5–100 kpc. The disc has mass 1e7–2e11 Msun, radial parameter a=0.1–30 kpc, vertical parameter b=0.03–5 kpc. A positive density does not establish a viable equilibrium distribution function or cosmological formation history. Neither the q>=0.6 restriction nor the uniform force weighting is a measured cosmological prior.

Each model is fitted with fixed baryons and with a stellar normalization nuisance parameter in [0.8950,1.1050], holding gas fixed. This is only one baryonic uncertainty, not uncertainty in disc lengths, heights, gas, the bar, or disequilibrium. The target remains the same census v3 realization. Three deterministic starts converge to essentially the same objective in each fit; global optimality is not proved. This is 16 fits and 48 optimization runs.

## Results

Held-out RMS fractional errors in **total** force, permitting stellar normalization adjustment:

| Dark component | Canonical | Alternative |
|---|---:|---:|
| Spherical NFW | 18.60% | 20.09% |
| Oblate NFW, density q>=0.6 | 13.28% | 14.39% |
| Oblate NFW, density q free down to 0.08 | 9.16% | 9.81% |
| NFW plus extended dark disc | 1.078% | 1.138% |

For fixed baryons the corresponding canonical errors are 20.08%, 14.37%, 9.58%, and 1.140%; alternative errors are 21.51%, 15.44%, 10.22%, and 1.210%.

The freely flattened single halos prefer density q=0.316 and 0.306, respectively, but still have vertical-force RMS discrepancies of 12.75% and 13.64%. Their radial-force discrepancies are 2.29% and 2.59%. These q values are density axis ratios, not the effective force-direction quantity in the previous report. All single-halo fits push the stellar normalization to its upper bound; the canonical moderately oblate fit also reaches the 100 kpc scale-radius bound. Relaxing those or changing the halo density profile could improve those particular fits. No claim excludes every possible single halo.

The disc-plus-halo fits have:

| Quantity | Canonical | Alternative |
|---|---:|---:|
| Stellar normalization | 1.083 | 1.103 |
| Dark disc mass | 3.40e10 Msun | 3.83e10 Msun |
| Disc radial parameter a | 10.91 kpc | 10.78 kpc |
| Disc vertical parameter b | 0.313 kpc | 0.313 kpc |
| Halo NFW scale radius | 59.51 kpc | 55.73 kpc |
| Disc density at R=8.122,z=0 | 0.0374 Msun/pc3 | 0.0427 Msun/pc3 |
| Disc column within +/-1.1 kpc there | 22.56 Msun/pc2 | 25.71 Msun/pc2 |
| Radial force RMS residual | 0.367% | 0.384% |
| Vertical force RMS residual | 1.479% | 1.563% |
| Maximum component residual | 2.275% | 2.407% |

The Miyamoto–Nagai parameters are not exponential scale length/height measurements. This is a substantial extra disc-like mass component, not a small reshaping of a conventional round halo. Its acceptability needs a joint fit to real data, outer-halo constraints and independent baryonic evidence. Existing limits on extremely thin dark discs must not be applied directly: Widmark et al. give a roughly 5 Msun/pc2 upper limit for scale heights <=50 pc, whereas this fitted component is much thicker. Their inferred dark-component uncertainties are dominated by baryonic modelling: https://arxiv.org/abs/2105.14030 .

## What DR4 would need

DR4 covers 66 months: https://www.cosmos.esa.int/web/gaia/dr4 . Its catalogue astrometric precision does not directly specify precision in reconstructed Galactic forces. For orientation, a transverse acceleration of 2e-10 m/s2 at 1 kpc produces only 0.0201 microarcseconds of curvature displacement in 5.5 years before fitting out position and proper motion. This order-of-magnitude estimate uses the full acceleration; the difference between these two models is smaller, and actual relative observer/source acceleration also matters. Galactic-force tests therefore use populations and dynamical modelling, not individual-star acceleration detections at these scales.

The relevant significance is deltaF^T C^-1 deltaF after treating fitted parameters and nuisance freedoms consistently. C must include observational, tracer/selection, baryonic, disequilibrium and numerical uncertainty, with their correlations. We do not have such a DR4 covariance here.

A deliberately optimistic sensitivity calculation freezes the models fitted on the training positions, treats the 40 held-out force components as independent, and gives them equal fractional standard errors. For the disc-plus-halo residual:

| Assumption | Canonical expected template S/N | Alternative |
|---|---:|---:|
| 5% independent error per force component | 1.36 | 1.44 |
| 2% independent error per force component | 3.41 | 3.60 |
| 2% independent plus a 1% RMS systematic aligned with the residual pattern | 1.03 | 1.09 |

The last row is a sensitivity illustration, not an estimate of Gaia's actual covariance. It uses C=sigma^2 I+s_sys^2 vv^T, with v=delta/rms(delta). At these positions the 3-sigma fixed-template threshold is 2.27–2.40% independent error. If uncertainty is fully aligned with the distinguishing pattern, its RMS must instead be below roughly 0.36–0.38% for a 3-sigma result. Refitting halo and baryon parameters to the same data further weakens a naive fixed-template comparison. Counting many nearby bins as independent would overstate the evidence.

Published inference work illustrates the modelling challenge rather than supplying a DR4 error bar: a three-dimensional perturbed-galaxy validation found 7% scatter in inferred vertical **potential**, not force (https://arxiv.org/abs/2201.04637); a distant-disk EDR3 application estimated aggregate biases comparable to 10–20% azimuthal surface-density variations (https://arxiv.org/abs/2111.13707). These are neither universal floors nor directly interchangeable with the force errors in our table. They do not justify assuming sub-percent accuracy for DR4.

Thus a single moderately flattened halo presents a much more accessible difference than the flexible disc-plus-halo example. Against the latter, DR4 alone has no demonstrated decisive power from this calculation. Joint constraints on vertical force versus height, off-plane radial force, baryonic mass, streams and the outer halo are needed. Better performance could make the restricted comparison decisive; additional dark-density flexibility could also reduce the residual further.

## Mathematical degeneracy and what remains testable

For a specified v3 potential, a Newtonian model would need rho_dark = laplacian(Phi_v3)/(4 pi G)-rho_baryon. If that density is everywhere nonnegative in the required global model and has acceptable dynamics, it reproduces the static force exactly. We have not established those conditions globally. The explicit positive-component fit demonstrates approximate degeneracy only over the tested region. It nevertheless prevents treating a mismatch with one NFW template as exclusion of all dark matter.

The previous force-direction null remains useful against spherical residual potentials. Variable effective flattening does not by itself exclude a flattened density halo: even a constant-density-axis-ratio halo has a force geometry that changes with position. The stronger present result comes from fitting both components across multiple heights, not from reusing that null against a class it does not cover.

## Verification and reproduction

Authoritative outputs are `run_v3/results.json` and `run_v3/manifest.json`; `run/` is historical, before adding extra checks, and its script hash no longer matches the current script. `run_v2/` failed during the added column-density diagnostic because a quadrature-error variable shadowed the integration function; this was corrected before the authoritative rerun. The final run uses the skill bounded runner with a 240-second cap, one numerical thread and a 100000-byte output cap. The contract and script specify all inputs and limits. The manifest records input hashes, software, execution command and completion status.

Analytic spherical NFW forces agree with the homoeoidal integration to 1.6e-15 relative. Quadrature doubling from 128 to 256 nodes differs by at most 1.5e-12 over tested q values. A finite-difference divergence of the flattened force is separately checked against 4 pi G rho. Main/fine target force differences are at most 0.143% over these positions. This supports the percent-scale fit comparison but does not establish sub-per-mille physical accuracy; numerical convergence is not an observational error forecast. Caches were read, not regenerated. No sealed predictions were changed.

Outcome: **conditional numerical evidence for approximate force mimicry in the specified finite domain; no actual DR4 power forecast or global halo exclusion.**


## Subsequent viability check

[The viability investigation](VIABILITY.md) finds that the explicit mimic has a local disc/halo density ratio near eight and substantial tension with existing mass/force inferences. It is not an established viable Milky Way model. The gravitational tensions are shared with the isolated census v3 target; the collisionless-formation objection is specific to a material dark disc. See the separate audited `viability_run` outputs.
