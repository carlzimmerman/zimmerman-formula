# HC-004 checkpoint — first investigation executed; original physics question remains open

**Newest mathematical answer:** [HC011](records/HC011_MATH_ANSWER.md). Explicit force fits give outer NGC7331 held-out errors 25.20 km/s (central inverse-square), 11.99 (inverse-radius), 2.54 (post-hoc constant acceleration), 2.06 (free power), at nominal stellar masses. These are one-galaxy interpolation tests. Source/response variation and the independent vacuum term expose missing physical equations. Correct area target is AΛ=32π²; two earlier checkpoint summaries omitted the square.

**Source correction and newest checkpoint:** [HC008–HC010](records/HC008_HC010.md). Sixteen original BH entries trace to inclination-dependent upper limits, not secure detections; four temperatures were inferred. The association survives their exclusion (65 objects: held-out error 0.429→0.330 dex) and updated masses (54 objects: 0.411→0.333). NGC7331 is not a secure BH detection; the earlier conditional radial results must be read accordingly. Corrected the cluster integral in a separate audit; original source preserved.

**Newest error-model audit:** [HC-007 results](records/HC007.md). The positive rotational coefficient survives quoted measurement errors, but its likelihood preference weakens. Final continuation, curvature and latent-model manifests are validated; independent OLS reproduces the zero-error limit.

**Latest continuation:** [HC-005/006 results](records/HC005_HC006.md), 2026-11-05. Group-held-out hot-gas association survives; new rotational association weakens under structural controls; exact curvature-equality prescription does not select a universal acceleration. The HC-004 record below is preserved as the earlier checkpoint.

2026-11-05. The comprehensive queue is [PLAN.md](PLAN.md). The first computational phase and feasibility audit are complete. This is not a completed explanation of dark matter, galaxy clusters, or the 32π coefficient.

## What was actually done

- Extracted 104 published galaxy/BH/stellar-mass entries; 102 have spheroid radii, 93 survive the source's exclusions for the descriptive fits.
- Parsed 85 optical and 85 hot-halo rows from a versioned author manuscript; joined their names, crossmatched 61 names against the size sample, and separated environment categories.
- Calculated horizon areas, surface gravities, MOND radii, BH circular-speed contributions, stellar mass fractions, and 85 approximate gravitational influence radii.
- Evaluated 1001 spin values, 9 independent Λ/a0 combinations, 27 illustrative pair configurations, 36 feedback-energy combinations, and 45 collective-flux configurations at three quadrature orders.
- Ran morphology-aware regression, bootstrap, leave-one-object-out prediction, an exploratory permutation diagnostic, measurement-perturbation sensitivity, and environment/distance controls.
- Scanned all 175 local SPARC rotation curves. Only two exact-name overlaps exist in the acquired BH samples; one is source-excluded. Computed distance-adjusted single-object BH contributions without claiming a population result.
- Derived a scoped enclosing-sphere inequality and corrected the older unrestricted finite-radius invariance statement. See [THEORY.md](THEORY.md).
- Verified 108 checks in the main run and 33 in a separate numerical robustness run, including adaptive vector quadrature and explicit refitted leave-one-out predictions. Both final manifests validate against current inputs. Self-review only.

## Findings that change the next step

### 1. Literal horizon areas do not explain the target

The tabulated BH detections give AΛ from 2.08e-33 to 4.76e-24 (fiducial Λ=1.09e-52 m^-2), compared with 32π²=315.83. Spin changes the area by at most a factor of two at fixed mass. Even assigning 10^15 solar masses to one hole yields only 1.19e-14. Summing individual areas at fixed total mass makes the bound smaller. These results reject this literal area interpretation; they do not rule out an unspecified new coupling.

The formal puzzle radius is 50.76 billion light-years and its Schwarzschild-assigned mass is 1.63e23 solar masses. It is 7.52 times the Nariai mass for the same Λ. No actual astrophysical object is inferred from these formal numbers.

### 2. Size has a strong raw association but little incremental prediction here

For the 93 author-clean size entries, descriptive log MBH versus log Re slope is 1.20, with bootstrap interval [1.02,1.37] and RMS scatter 0.59 dex. This is not an errors-in-variables physical slope measurement. Horizon-radius/spheroid-radius ratios span over a factor 400 across these entries, so no tight universal proportionality is evident.

Using spheroid stellar mass and broad morphology, leave-one-out prediction error is 0.422 dex. Adding spheroid radius gives 0.428 dex, slightly worse. Partial size correlation is 0.062. This does not prove size has no independent role: mass-size collinearity, selection, missing size systematics and distance covariance matter. The declared 0.1-dex-size/quoted-mass perturbation experiment shifts the fitted size coefficient substantially, illustrating why naive error perturbation is not a causal or hierarchical inference.

### 3. Hot gas is the most useful observed association in this pass

In the 85-object sample, adding galactic hot-gas temperature to velocity dispersion, K-band luminosity, optical radius, distance and environment lowers leave-one-out error from 0.391 to 0.307 dex. Residual correlation is 0.611; refitting after removing each object gives 0.578–0.637. It survives removal of NGC7331 or the two objects with log MBH≥10. The temperature coefficient's bootstrap interval is [1.11,2.12]. All are exploratory, selection-uncorrected results.

This is a reanalysis of an already published BH/hot-gas association. It does NOT show the BH produces missing gravity. Accretion, feedback, halo depth and assembly history remain competing explanations. Galaxies in the same group are not fully independent observations; a group-blocked validation and latent covariance model remain necessary.

### 4. Galaxies attract one another; their BHs are usually small contributions to that attraction

Illustrative example, not a measured pair: a 10^8-solar-mass BH inside a 10^11-solar-mass host contributes 0.1% of that host's monopole acceleration at the same separation. Two such BHs alone separated by 100 kpc have a Newtonian circular orbital period of about 209 Gyr. The host and cluster potential must be included; this pair estimate is not a prediction of an actual galaxy orbit. Λ becomes comparable to the isolated BH contribution on these scales, not to the much larger total cluster attraction.

For NGC7331, accepting the tabulated BH estimate provisionally and rescaling it linearly to the SPARC distance gives a BH contribution of 0.026–0.051% of observed v² in the outer half of the measured radial range. The BH mass's original determination still needs verification. NGC5055 is excluded, even though its tabulated value would also be a small outer contribution. These are diagnostics, not an eligible two-galaxy regression.

### 5. Collective gravity result has a precise scope

The two-clump QUMOND calculations never exceed the same-mass spherical reference for the named kernels and enclosing boundaries. At offset 0.9R and monopole gN/a0=0.01, the ratio is 0.73246, independently reproduced by adaptive quadrature. An analytic inequality explains this for any positive distribution entirely inside the sphere under the stated kernel assumptions. External fields, boundaries cutting sources, projected lensing and different field equations are outside that proof.

### 6. Feedback energy needs an aperture and efficiency, not just a BH mass

An illustrative accreted mass of 10^9 solar masses with net coupling efficiency 0.01 supplies 1.79e54 J. A 10^14-solar-mass gas reservoir at kT=5 keV has thermal energy 2.38e56 J, so that example supplies 0.75%. Smaller cooling cores have different budgets. This neither rules out maintenance feedback nor demonstrates it: actual cavity energy, cooling losses, duty cycle and coupled accreted mass must be measured. Heating energy was never added to the dark-matter budget.

## Open dependencies and next execution order

1. Obtain independently measured outer dynamics/lensing for a substantially larger direct-BH sample. The current exact-name SPARC overlap cannot identify a conditional BH–gravity-discrepancy coefficient. Extend to resolved H I/CO/IFU data after auditing BH measurements, not by inventing BH masses from host scaling relations.
2. Build a group-aware, errors-in-variables hot-gas analysis with covariance and sample-selection terms. Freeze an independent validation sample; current regressions are discovery diagnostics.
3. For the eight cluster centrals, acquire matched-aperture gas density/temperature profiles, stellar mass, lensing mass, and cavity power. Temperature-derived R500/mass proxies cannot serve as independent confirmation of a temperature correlation.
4. Compute the Ricci/Weyl invariants directly and test curvature-based candidate source laws only after their equations are independently specified.
5. A new horizon coupling remains an open model specification, not a simulation ready to run. It must survive the coefficient-offset freedom, lensing/dynamics consistency, and existing local-gravity constraints.

These tasks remain open in PLAN.md; none is marked exhausted. No request for new permission is needed for routine continuation within this research scope. No background job is running.

## Reproducibility and audit history

- Main executable: analyze.py; contract.json; final results in run002/. Outcome: implementation and finite assertions checked in the documented range, statistical interpretation conditional on the stated model/data assumptions.
- Independent executable: robustness.py; robustness_contract.json; final results in robustness002/. Bootstrap seed 32006; main seed 32005.
- run001/ is a failed historical attempt: the interaction-grid coverage assertion incorrectly expected 81 instead of 3×3×3=27. The declared count was corrected; no grid was silently enlarged or case dropped.
- robustness001/ completed but the platform's pseudoinverse calculation emitted numerical warnings. robustness002/ uses full-rank QR leverages, explicit finite checks, and matches the explicit refitted LOOCV error to floating precision with an empty stderr. Earlier result is retained, not silently overwritten.
- Numeric tables have source provenance in SOURCES.md; acquisition hashes in records/acquisition.json. Published values are not presumed current-best measurements.
- Visual summary: run002/overview.png, inspected after rendering. Raw values and uncertainty caveats take precedence over the plot.

Validation commands:

    python /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py horizon_cluster_2026_11_05/run002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
    python /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py horizon_cluster_2026_11_05/robustness002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

Exact execution argv are in each manifest. Reruns must use fresh output directories and update both output/result arguments; historical evidence must not be overwritten.
