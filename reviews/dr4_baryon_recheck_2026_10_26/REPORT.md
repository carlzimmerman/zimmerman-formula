# Revised baryons and v3 discrimination — 2026-10-26

## Answer

Changing the baryons materially improves isolated static v3. It does not yet produce a demonstrated joint fit to the Galaxy. The new finite experiment finds a continuing trade-off between vertical and radial forces, while the revised force targets remain readily distinguishable from the tested single NFW halos but closely mimicked by a positive disc-plus-halo model. The old 1.1% mimicry figure cannot be carried over unchanged: the revised examples admit 0.63–0.73% residuals in this new restricted sample.

No universal exclusion of v3, baryonic families, or dark matter follows. No sealed prediction has been changed. This is a new exploratory calculation, not an updated preregistration or DR4 power forecast.

## Existing work recovered

X5 had already solved 175 baryon cells per footing. Lighter local columns and shorter discs made its loose local goodness-of-fit line pass in 11 cells, but its stricter vertical-force summary and full rotation curve still disagreed. The original census local speed and vertical-force failures were therefore partly baryonic, not universal properties of the equation. X5's scale-length priors were provisional. Its earlier narrow Licquia/Newman prior is not the only contemporary structural estimate: Imig et al. report a mass-weighted mean 2.37+/-0.2 kpc in a multi-population, partly broken-exponential model. That mean cannot be equated to a single exponential at all radii. [Imig et al.](https://arxiv.org/abs/2507.17629).

## New finite experiment

`check.py` uses the existing P4 AQUAL solver via X5's read-only loader, with mu=x/(1+x), isolated boundary conditions, L=0 and each acceleration normalization separately. It first reproduces one stored X5 unscreened cell's local K to better than 1e-6.

Twenty-four models span:
- local all-height baryonic disc column 40, 44, 47 Msun/pc2;
- common stellar radial length 2.24 or 2.37 kpc;
- compact bulge normalization 1.64e10 or 2.12e10 Msun;
- stellar exponential heights 0.3 and 0.9 kpc, fixed thin fraction;
- gas local column 11 Msun/pc2, exponential height 0.2 kpc, inherited radial surface-density shapes.

These are **illustrative, literature-motivated combinations, not a reconstruction of any cited full model**. The 2.24 value comes from a dynamical scale-length inference and is not a purely photometric constraint. Bulge normalizations inherit the provisional X5 bounds and are not gravity-independent measurements. We do not include the true nonaxisymmetric bar, broken stellar profiles, full gas components, dust, EFE or disequilibrium. Gas thickness is changed alongside its column, so this run does not isolate which change causes each improvement.

The adopted rotation comparison is the repository's 38-point Eilers table with its prescribed statistical-plus-2%-systematic diagonal errors. Chi-square is a descriptive score for that adopted error treatment, not a complete correlated-data likelihood. The local speed target is about 229.05+/-4.645 km/s. The vertical measurement Kz/(2 pi G) is a force proxy with column units, **not the true integrated mass column**.

## Results

The previous fine-grid census targets have K(1.1)=92.43 canonical and 97.01 alternative. The new 24 models cover K(1.1)=71.36–86.07. The price of the lowest K values is insufficient rotation.

| Example | Local all-z baryonic column | Rd | Bulge mass | K(1.1) | Vc(R0) | Full rotation chi2 |
|---|---:|---:|---:|---:|---:|---:|
| Canonical low-column, low-force | 40 | 2.37 | 1.64e10 | 71.36 | 207.28 | 739.8 |
| Canonical local compromise, refined | 44 | 2.24 | 2.12e10 | 78.49 | 226.56 | 109.9 |
| Canonical smallest RC chi2 | 47 | 2.24 | 2.12e10 | 82.24 | 231.47 | 62.6 |
| Alternative local compromise, refined | 40 | 2.24 | 2.12e10 | 76.97 | 224.96 | 85.7 |
| Alternative smallest RC chi2 | 47 | 2.37 | 2.12e10 | 84.78 | 230.56 | 28.8 |

Columns are Msun/pc2, lengths kpc, masses Msun, velocities km/s. Examples described as local compromises were chosen post hoc using an explicitly heuristic score around K=72 and V=229.05. **K=72 in that score is an illustrative force scale, not a use of Horta's true-column measurement as a force likelihood.** This is not a joint observational optimum. The lowest full-RC chi2 examples were not selected for the halo-mimicry experiment.

The two refined compromises have baryonic midplane densities 0.07285 and 0.06735 Msun/pc3, respectively: much lower than the prior dark-disc mimic's ~0.113, illustrating a real improvement in local baryonic normalization. Their true baryonic columns within 1.1 kpc are 40.77 and 37.16, which must not be confused with their all-height inputs 44 and 40.

A stronger vertical test compares multiple heights. At z=(0.5,1.1,2,3) kpc, the canonical compromise predicts K=(57.80,78.49,94.06,103.93); the alternative predicts (56.73,76.97,92.59,102.84). Bienaymé et al.'s corresponding published values are (45.4,63.6,81.5,96.4). Both revised examples still overshoot, especially at small height. This is conditional tension with that inferred force field, not a raw-data exclusion or independent sigma count. [Bienaymé et al.](https://arxiv.org/html/2406.08158v2).

Horta et al.'s total-column estimate of 72(+6,-9) uses a different inference method; it should not simply replace K(1.1) in a likelihood. Survey, baryonic and non-equilibrium modelling must be reconciled before declaring a joint fit. [Horta et al.](https://arxiv.org/html/2312.07664v2).

## Does the remaining force shape distinguish dark matter?

`compare.py` refits previously benchmarked positive-density analytic models to the two refined compromise targets, holding the revised baryons fixed. Training uses six radii 7,9,11,13,15,17 kpc and three heights 0.5,1.1,2 kpc (18 positions). Validation uses 8,10,12,14,16 kpc at those same heights (15 positions). Thus radii are held out; heights are not. Both force components are weighted equally in fractional total-force units. This sample differs from the earlier census comparison, so changes in numerical RMS cannot be attributed solely to baryons.

| Rival | Canonical RMS | Alternative RMS |
|---|---:|---:|
| Spherical NFW | 17.65% | 19.64% |
| Oblate-density NFW, q>=0.08 | 8.32% | 9.29% |
| Spherical NFW plus positive MN disc | 0.634% | 0.728% |

The freely oblate halos prefer q=0.371 / 0.363. The discs in the last row have mass 2.57e10 / 2.92e10 Msun, a=9.76 / 10.07 kpc and b=0.420 / 0.408 kpc. Their physical viability must be checked afresh; the prior census disc/halo density ratio of eight must not be reused for these new models. Positive density alone still does not establish equilibrium, formation or survival.

The disc-plus-halo residuals are mostly vertical: RMS 0.891% / 1.020% versus radial RMS 0.102% / 0.139%. Maximum component differences are 1.47% / 1.73%. Three starts agree on the fitted solutions; this is not a global-optimum proof or an exhaustive dark-density family.

For the deliberately optimistic fixed-template case of 30 independent validation force components with equal fractional Gaussian errors, a nominal S/N=3 would need errors below 1.16% / 1.33%. A systematic error aligned with the residual pattern cannot be averaged down this way; its RMS would need to be below approximately 0.21% / 0.24% if it dominated. These are conditional precision requirements, not predicted DR4 performance. Main/fine force differences for the two targets reach 0.164% / 0.160%; numerical uncertainty is already relevant when discussing such a demanding systematic threshold. Further solver convergence and full nuisance marginalization would be required.

The remaining useful prediction is therefore the **joint radial/vertical force relation across radii and heights given independently constrained baryons**. It can distinguish v3 from the tested restricted halos. It is not guaranteed to distinguish an arbitrary, physically allowed dark-density distribution. Baryon readjustment that fixes observations is scientifically legitimate only if constrained independently and used consistently in all comparisons; fitting on DR4 and calling those same points an independent prediction is not valid.

## Literature cross-check and scope

Wang et al. (2026) combine rotation and phase-spiral information with a broken-exponential baryonic model and report difficulty fitting both with QUMOND. This supports the relevance of the joint test, not a transferable numerical exclusion of v3: their equation, acceleration choices, priors and likelihood differ from this AQUAL calculation. Their quoted significance has not been reproduced here. [Primary paper](https://arxiv.org/html/2605.10857v1).

A complete next observational test would derive a permitted baryon family from counts, gas and stellar-population data, fit existing kinematics with consistent covariance, then reserve DR4 populations or spatial regions for prediction. The present result is narrower: **lighter/thicker baryonic models improve v3 substantially, but the tested family does not establish full agreement; force geometry remains distinctive against simple halos and nearly degenerate against a flexible disc-plus-halo.**

## Evidence

`run/manifest.json` and `compare_run/manifest.json` both validate with completed status. Contracts specify bounds, inputs, units and non-claims; manifests record hashes and commands. Baseline X5 reproduction passes. Two selected targets were rerun at 45 radial cells/decade and 72 angular cells, versus 30 and 48. Maximum relative target-force differences are recorded above. The main sweep comprises 24 new cells plus one baseline and two refinements. Neither a low nonlinear residual nor an execution success is evidence that the model fits the Galaxy.
