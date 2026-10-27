# Viability of the force-mimicking dark disc — 2026-10-26

## Verdict

The fitted disc is an explicit positive-density mathematical mimic, **not an established viable Milky Way model**. It has substantial tension with existing dynamical measurements and is unlike dark discs produced in the cited collisionless merger simulations. A dissipative dark component is a possible formation route in principle, but no specified particle model, equilibrium distribution function, or evolution simulation has been shown to produce and preserve these fitted profiles. This does not establish exclusion of every dark-matter model.

Crucially, force-based observational objections largely apply to the isolated census v3 target too. Formation objections distinguish the physical explanations; a disagreement with measured gravity cannot be assigned only to the Newtonian model when it reproduces v3 gravity.

## Executed diagnostics

New computation: `viability.py`, `viability_contract.json`, `viability_run/results.json`, `viability_run/manifest.json`. Input fits: authoritative previous `run_v3/results.json`. No fits were changed, and no sealed files edited. Densities in Msun/pc3; columns in Msun/pc2; R=8.122 kpc. The two columns are separate v3 acceleration footings.

| Diagnostic | Canonical | Alternative |
|---|---:|---:|
| Dark-disc midplane density | 0.03742 | 0.04272 |
| Accompanying spherical-halo density | 0.00467 | 0.00524 |
| Total dark midplane density | 0.04209 | 0.04796 |
| Dark-disc/halo midplane density ratio | 8.01 | 8.16 |
| Local disc half-column height | 180.7 pc | 180.4 pc |
| Baryonic midplane density in fitted model | 0.11249 | 0.11376 |
| Total midplane density | 0.15458 | 0.16172 |
| Dark column within +/-1.1 kpc | 32.80 | 37.19 |
| Baryonic column within +/-1.1 kpc | 58.59 | 59.43 |
| Total column within +/-1.1 kpc | 91.39 | 96.62 |

Half-column height is computed by integrating the actual Miyamoto–Nagai density until half of the full local vertical column is enclosed. It is not the fitted parameter b (~313 pc), an exponential scale height, or a global half-mass height. The earlier fit used z>=300 pc; its approximately 1% force agreement is not a promise of 1% agreement in midplane density or its force derivatives.

The MN density was independently checked against the divergence of its analytic force, with maximum fractional error 3.74e-8 in the tested positions. The manifest validates with status completed. This establishes the diagnostics of the fitted profiles; it does not validate an observational likelihood, phase-space distribution or stability.

## Existing observations

Horta et al.'s Gaia/APOGEE Orbital Torus Imaging analysis reports local total column 72(+6,-9), dark column 24+/-4, and total midplane density 0.081(+0.015,-0.009). The fitted profiles above substantially exceed these central estimates. Their paper discusses a one-dimensional orbital model and disequilibrium, so dividing the discrepancy by a quoted error would not be a robust model-exclusion significance. The columns and densities are correlated derived results, not independent likelihood factors. [Primary paper](https://arxiv.org/html/2312.07664v2).

Bienaymé et al. report Kz/(2 pi G) of 45.4, 63.6, 81.5 and 96.4 at heights 0.5, 1.1, 2 and 3 kpc. Our same-height fitted values are 74.03, 92.19, 101.85, 105.98 (canonical), and 77.75, 96.75, 106.95, 111.44 (alternative). This is a height-dependent discrepancy, especially near the disc, not just a difference in inferred dark density. Their analysis adopts a Galactic population model and stationarity assumptions; its published numbers are not raw accelerometer readings. [Primary paper](https://arxiv.org/html/2406.08158v2).

A 2025 K-dwarf Jeans analysis finds local dark density 0.0117+/-0.0035, with a substantial shift when changing tilt modelling. This supports concern about a fitted dark density near 0.04–0.05, but is not a direct profile-specific exclusion of our nonuniform disc: the inference must be rerun with this density profile rather than treating its scalar estimate as a model-independent prior. [Primary paper](https://arxiv.org/html/2506.02956v2).

The baryonic input is part of the problem. Our model puts 58.6–59.4 in baryonic column within 1.1 kpc; the Horta analysis uses 47+/-3. Reducing baryons could relieve the full model's mass excess, but would change the v3 target and require recomputing both theories and fitting actual observations. The present numbers do not show that the dark disc by itself causes the whole discrepancy.

Thin-dark-disc exclusions cannot simply be imported. The roughly 5 Msun/pc2 limit in Widmark et al. concerns scale heights <=50 pc. Buch et al.'s 5–12 constraints concern their thin-disc profile below 100 pc. Our local half-column height is ~180 pc with a different functional form. A profile-specific likelihood is required. [Widmark et al.](https://arxiv.org/abs/2105.14030), [Buch et al.](https://arxiv.org/abs/1808.05603).

## Collisionless formation

Purcell, Bullock & Kaplinghat compare satellite-merger simulations with the Milky Way thick disc and obtain an accreted dark-disc density around 20% of the host halo or less. Our fitted ratio is about eight, roughly forty times that benchmark. This is a simulation-based formation tension, not a universal 95% upper bound. [Primary paper](https://arxiv.org/abs/0906.5348).

Earlier simulations were more optimistic: Read et al. found dark-disc densities 0.25–1.5 times the non-rotating halo in three cosmological examples. Even these are below our required ratio. Those results establish that collisionless dark discs are possible, not that the required dominant, concentrated disc follows naturally. [Primary paper](https://arxiv.org/abs/0902.0009).

In APOSTLE, Schaller et al. found only one detectable disc among 24 simulated analogues; its local-density enhancement was about 35%. This is evidence against treating a large dark disc as generic, rather than a probability calculation for the actual Milky Way. [Primary paper](https://arxiv.org/abs/1605.02770).

Collisionless material cannot radiatively cool like gas. Merger deposition can create rotating structures, but the associated stellar heating and merger history constrain that route. A positive spatial density alone says nothing about whether an admissible orbit distribution produces it. We have not computed rotation, velocity dispersion, a nonnegative equilibrium distribution function, Toomre stability, bending modes, or long-term survival. Consequently neither stable nor necessarily unstable is justified.

## Dissipative formation remains a distinct, unverified possibility

Double-Disk Dark Matter explicitly introduces cooling interactions in a subcomponent; it is not merely a more flexible parameterization of ordinary collisionless CDM. [Fan et al.](https://arxiv.org/abs/1303.1521).

Roy et al. simulate a 6% atomic dark component: rotating discs can form, but much of the material collapses into clumps and becomes centrally concentrated, affecting the baryonic galaxy. Their simulation is not a demonstration that our smooth, radially extended 34–38 billion solar mass disc survives. [Primary paper](https://arxiv.org/abs/2304.09878).

Cosmological atomic-DM constraints depend on the dark coupling, constituent masses, temperature ratio and abundance; the fitted galactic mass alone does not specify those. There is no justified universal fraction cutoff to apply here. [Bansal et al.](https://arxiv.org/abs/2212.02487). A viable dissipative explanation would need cooling and angular-momentum evolution to yield this profile, consistency with cosmological data, and treatment of fragmentation and its gravitational effects. Direct-detection or annihilation exclusions also require particle couplings, not just density.

## Consequence for v3 and DR4

The static v3 calculation itself gives Kz/(2 pi G)=92.43 and 97.01 at R0,z=1.1 kpc, almost identical to the fitted models' 92.19 and 96.75. Thus existing low-force results are a warning for this particular v3 realization as well. The sealed census midplane densities (~0.166 and 0.175 isolated) are also large; the mathematical mimic does not create that problem from nothing.

The defensible comparison now has three levels:

1. Ordinary restricted halo families leave appreciable residuals against v3.
2. A positive dark disc can hide most of those residuals mathematically, but the explicit fitted example has observational and collisionless-formation problems.
3. More general dissipative or differently shaped dark components remain unexcluded here. Rejecting them requires a specified model and a joint fit, not extrapolating an objection to this example.

DR4 should therefore test the common predicted vertical-force profile against the real Galaxy first, with consistent baryons, selection and non-equilibrium treatment. If the profile survives, formation and independent dark-sector constraints become useful discriminators. If it fails, both this v3 realization and its fitted Newtonian mimic must change or be rejected.


## Revised-baryon continuation

A subsequent [24-model baryon experiment](../dr4_baryon_recheck_2026_10_26/REPORT.md) reduces the excess vertical force and exposes a continuing rotation/vertical trade-off. The original census-mimic numbers above must not be applied to the new models. Refitted disc-plus-halo rivals match two revised targets at 0.63–0.73% RMS in a different finite validation sample; their viability is not established.
