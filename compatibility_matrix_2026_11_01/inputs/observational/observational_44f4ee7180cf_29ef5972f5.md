# Clump screen: a few per cent of baryons is short; halo infall remains energetically open

This finite calculation uses **historical ER1, ng64-era z=0 profiles**, not an ng80 rerun. It finds no measured instability selector or delivered response. The gas-clump route remains open because local gas structure, dispersions, clump histories and the native cold-field wake are absent. Cold dark energy is a gravitating field component, never a particle. No a0 enters. This is not a full theory grade.

`CONTRACT.md` was written before calculation; `contract.json` pins the 182 declared input files. `clump_screen.py` ran in 0.69 s. `run002/manifest.json` has status **completed** and passes the installed v2 validator. `run001` has status **launch-failed** from the POSIX-cap pre-execution hook; no science result came from it. The successful run enforces wall time, output size and numerical thread count, and claims no memory/CPU cap.

The failed run001 manifest is **stale under current `--root` validation** because its `CONTRACT.md` input was later amended to document the launch failure. No hashes or original manifest were altered. The exact original contract is preserved separately as `CONTRACT_run001_original.md`, verified against run001's observed input hash. The current successful run002 remains valid. No failed-run scientific evidence is used.

## What was actually computed

For 123 of 175 SPARC galaxies (Q<=2, inclination>=30 degrees, 20<=Vflat<400), reconstruct the historical native spherical halo plus ER1's baryon proxy, then integrate the circular-orbit energy lost if clumps sink to rest at the first observed radius. We use two initial radii: today's HI radius, and the native total halo radius. Perfect transfer into the cold field, a fixed final baryon profile, final clump kinetic energy zero and no disruption all make this an optimistic supply calculation. It is an upper allowance **inside this stated static-potential model**. An evolving formation history, a smaller final radius, different orbits or different total baryonic mass lies outside it.

For a specified potential,

`work / clump_mass = integral[rf,ri] G Mtotal(r)/r dlnr + Vc(ri)^2/2`.

Thus DR5's entire present-disc rotation energy does **not** bound the available energy of material infalling from the halo. The orbital potential drop matters. Conversely, enough orbital energy alone does not say where the wake deposits it or whether the final central profile survives baryonic infall.

The target is ER1's **binned**, canonical-A `f_req(Upsilon=.50)` (0.20 and 0.4667 in the two affected bins). This is a disclosed conditional target, not a galaxy-by-galaxy required-response determination. All per-galaxy results are retained. Bins here are half-open to avoid double-counting exactly 60 km/s: the lowest bin has 12 rather than ER1's inclusive 13.

## Result: the meaning of “2–3 per cent” changes the answer

Values below are medians. Required fraction is clump mass / **observed baryonic mass**, assuming perfect delivery. The 3%-baryon supply divided by required work is reported separately.

| Vflat | n | Required baryon fraction, from RHI | Required baryon fraction, from halo | 3% baryons / need, RHI | 3% baryons / need, halo |
|---|---:|---:|---:|---:|---:|
| 150–200 | 25 | 0.1403 | 0.1027 | 0.214 | 0.292 |
| 200–250 | 18 | 0.0726 (17 with RHI) | 0.0567 | 0.413 (17) | 0.529 |

**3% of baryons is short for every targeted galaxy**, even allowing infall from the halo: 0/25 and 0/18 reach the conditional target. Minimum required baryon fractions are 7.22% and 3.95% in these two bins. Therefore this narrowly specified 2–3%-of-baryons model fails the energy screen.

**2–3% of total halo mass is a different, energetically allowed assumption.** At 3% it consumes median 48.7% /44.6% of today's baryons; at 2%, 32.5% /29.7%. The 3%-halo supply from the halo is median 4.88 /7.89 times the work needed and reaches all 43 targeted galaxies. It is not an observed or derived clumped fraction. Present total gas, if all delivered with perfect efficiency, supplies median 1.66 /3.05 times the target from the halo; this does not establish that the gas ever forms surviving clumps.

## Independent structural selector: inputs stop short of a physical Q

The catalogue supplies MHI and RHI, so an independently calculable gas diagnostic is

`Sigma_mean = 1.33 MHI/(pi RHI^2)`, `kappa = sqrt(2) Vflat/RHI`,

`sigma_crit_mean = pi G Sigma_mean/kappa = G (1.33 MHI)/(sqrt(2) Vflat RHI)`.

This substitutes a **mean** density and a flat-curve epicycle. It is not measured local Q. SPARC's downloaded mass models have gas gravitational contributions but no radial gas-density profile or gas velocity dispersion. The required support can be calculated; whether the gas is unstable cannot. A stellar required radial dispersion at 2 Rd uses observed surface brightness and the rotation-curve derivative; actual stellar dispersion is also missing.

| Vflat | n | Gas sigma_crit, km/s | Stellar sigma_crit(2Rd), km/s | Rotation-limited gas patch mass, Msun | Conditional t_df at RHI, Gyr |
|---|---:|---:|---:|---:|---:|
| 20–60 | 12 | 4.76 (11) | 1.38 | 6.02e7 | 1.16 |
| 60–100 | 35 | 5.83 | 2.99 | 1.74e8 | 2.46 |
| 100–150 | 23 | 5.78 | 6.02 | 1.59e8 | 9.84 |
| 150–200 | 25 | 6.79 | 23.61 | 2.72e8 | 15.54 |
| 200–250 | 18 | 6.93 (17) | 20.82 | 2.45e8 | 26.01 |
| 250–400 | 10 | 4.75 | 32.46 | 8.55e7 | 147.54 |

The gas-only mean-density diagnostic changes mildly from dwarfs to the target spirals. The conditional collisionless circular-isothermal friction estimate predicts faster sinking in dwarfs, with 11/11 and 34/35 below 100 km/s sinking within 10 Gyr, compared with 5/25 and 0/17 targeted spirals. This does not supply the needed dwarf protection. The stellar diagnostic has a much stronger structural difference, but missing dispersions prevent a measured stability test; bars are a separate follow-up.

The gas patch mass uses `lambda_rot=4 pi^2 G Sigma_mean/kappa^2` and `Mrot=pi Sigma_mean(lambda_rot/2)^2`, capped by total gas for the friction calculation. It is the zero-pressure rotation-limited scale, **not an observed clump mass**. The result field called `mean_gas_proxy_local_regime` only tests `lambda_rot<RHI`; it is a permissive geometry flag, not a verified WKB regime. Only 7/11 and 31/35 dwarf cases meet even that test; local gas structure can materially change these estimates. The friction coefficient and Coulomb logarithm are disclosed assumptions in the contract.

## Applicability to the gravitating field

The mechanism has particle-based precedent, not a native-field derivation. [El-Zant, Shlosman & Hoffman (2001), v2](https://arxiv.org/abs/astro-ph/0103386) study gravitational energy transfer from massive baryonic clumps in a collisionless halo. Their abstract's individual-clump scale is >=0.01% of total system mass; it does not establish an observed 2–3% population fraction. [Cole, Dehnen & Wilkinson (2011)](https://arxiv.org/abs/1105.4050) find strong effects for an imposed clump of 1% of halo mass. [Inoue & Saitoh (2011), sections 3–4](https://academic.oup.com/mnras/article/418/4/2527/1027187) demonstrate core formation followed by partial cusp revival when the clumps assemble a bulge, and identify clump survival and later accretion as limitations. These papers justify testing the channel, not transferring their halo result to this framework.

A multistream phase-space continuum obeying the collisionless Boltzmann/Poisson equations can have the same gravitational wake without interpreting numerical tracers as physical particles. A single-velocity dust field is different: its Euler description ceases to be single valued at shell crossing. The record provides no accepted field action/stress/caustic completion that gives the required virialized distribution. Thus native eta from the collisionless zoom and the Chandrasekhar friction law remain conditional on that missing completion. A fluid wake also need not equal a collisionless wake: [Ostriker (1999)](https://arxiv.org/abs/astro-ph/9810324) derives explicitly Mach-dependent drag in a gaseous medium. No native sound speed, dispersion relation, small-scale regularizer or retarded response kernel is supplied here.

Kelvin circulation conservation does not set a nonaxisymmetric gravitational torque to zero: `r cross (-grad Phi)` can be nonzero while a single barotropic stream stays irrotational. This clump route concerns orbital energy/angular-momentum transfer, not vortices or centrifugal expulsion. An actual field calculation still needs the wake and its completion after caustics.

## Provenance and checks

The independent ER1 reconstruction reveals that its per-galaxy energy dictionary is overwritten across backgrounds: the retained record matches **B_cfg886_bg**, maximum relative difference 9.99e-15, rather than canonical A (difference 0.00587). The historical binned target is A. This is a disclosed historical comparator mismatch, small in these energies but not silently pooled. No claim is made that the calculation is a corrected A or ng80 result.

The point-mass closed-form orbital energy agrees to 3.52e-8; 2048 versus 4096 quadrature points differ by at most 3.86e-7; the two critical-dispersion formulas agree to floating precision; E(.872)=0 exactly. All 175 records/curves/table names match. There are 52 excluded galaxies, with overlapping reasons: quality 12, inclination 12, missing/out-of-range Vflat 41. `run002/results.json` retains all rows, denominators and omissions; `run002/manifest.json` retains every observed before/after input hash.

Reproduce into a new directory:

`python3 rebuild_2026_10_22/ER2_clump_route/run_screen.py run003`

Validate:

`python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/ER2_clump_route/run002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula`

Key SHA256: historical ER1 results `a65e254e5290ca257ab520f0c3a5c314c77d80ba66aeef4207b82cfa463b5110`; native profiles `6dd04418b17d08c3d8b85d19a9f5a34b981538651cc1d6094889260f9eca9905`; SPARC table `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`; new results `e27073865735474374aa9e4430657ad365490bed8071358223ce88491e00e5ee`. Raw primary-source tool evidence is `primary_sources_web_raw.json` (SHA256 `a485a35db0af2432e694c3dfd61c60c2e67e850de3dea35d416d2279437b1a81`).

The next discriminating inputs are independently measured radial gas/stellar dispersions and gas structure or a supplied clump history, plus an actual native-field wake/caustic completion. No efficiency or velocity-bin threshold was fitted.
