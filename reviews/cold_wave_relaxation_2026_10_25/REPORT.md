# Can gravitational wave relaxation select the cluster state?

**The tested secular process is much too slow.** With the current candidate's imposed eta=1500 pc km/s, the fastest estimated wave-interference relaxation time in the tested cluster shells is 8.34e12 Gyr. This is 5.96e11 times a 14-Gyr comparison age. It does not select the inferred present-day cluster occupations on cosmic time. This is a conditional kinetic estimate, not a theorem excluding violent relaxation, dense early assembly, coherent collapse or new interactions. No parameter-free profile or vacuum/force matching has been found.

This continuation tests a different route from the preceding static-support calculation. Small smooth gradient stress does not by itself imply weak stochastic relaxation; the latter has now been evaluated separately. The repository already records the exact density-matrix isospectral invariants in cold_envelope_formation_2026_10_24/MECHANISM.md; those are not claimed as a new result here.

## Source-to-framework translation

[Bar-Or, Fouvry & Tremaine, arXiv:2010.10212v1](https://arxiv.org/pdf/2010.10212), equation (3), gives the approximate secular wave gravitational-relaxation scale

    t_relax ~ sigma^6 / [G² rho² eta³ ln(R sigma/eta)],
    eta = hbar/m,  lambda_sigma = eta/sigma.

The paper treats self-gravitating wave kinetics. We transfer its Schrödinger-Poisson scaling to the selective cold-wave candidate because the nonrelativistic kinetic and Newtonian self-gravity operators match. This does not transfer its particle ontology, cosmological inference or a fitted halo relation. The estimate assumes a weak-scattering, incoherent bath, a velocity scale sigma and R much greater than lambda_sigma; its coefficient and Coulomb-log cutoff are approximate. It does not describe the rapid rearrangement of orbits during a changing mean potential.

The candidate's eta is an existing adjusted input, not fixed by vacuum energy. Cold modes feel Phi_b,Newtonian+Phi_c; stars feel the separate baryon-only law plus Phi_c. We have not used the baryon MOND force as the cold's orbital force.

## Fixed calculation

Use the same seven X-COP clusters and six radii from 0.1 to 1 R500. For each of five released hydrostatic mass reconstructions and each of the two inherited a0 footings, reconstruct the selective cold source

    Mc = H - [B + sqrt(B²+4AB)]/2,
    B=Mgas+Mstar, A=a0 r²/G.

For each shell use its actual inferred positive mass difference divided by shell volume. Exclude, count and retain every nonpositive shell rather than clipping it to a positive density. Evaluate at its geometric central radius R. Obtain vc²=G(Mb+Mc)/R from log-interpolated enclosed mass, then test sigma=vc/2, vc/sqrt(2), vc. These are specified support-scale sensitivities, not measured cold dispersions or a solution of Jeans balance. No relaxation parameter or velocity is fitted.

There are 350 shell/model/footing combinations. Of these, 303 have positive source density and yield 909 velocity-scale evaluations; 47 nonpositive combinations are explicitly excluded. Repeated reconstructions and footings are not independent observations. The source profiles exactly reproduce the preceding selective-coupling audit.

## Results

Minimum relaxation times across seven systems, positive shells and all three velocity-scale choices, in Gyr:

| Released mass model | Canonical a0 | Alternative a0 |
|---|---:|---:|
| Forward | 2.57e13 | 2.54e13 |
| NFW | 2.93e13 | 2.91e13 |
| Einasto | 3.10e13 | 3.09e13 |
| Isothermal | 8.85e12 | 8.34e12 |
| Burkert | 1.19e13 | 1.14e13 |

The fastest case is the alternative-footing isothermal reconstruction of ZW1215, innermost shell:

- R=192,050 pc;
- rho=5.43e-4 solar masses/pc³;
- sigma=344.9 km/s (the vc/2 sensitivity);
- lambda_sigma=4.35 pc;
- R/lambda_sigma=44,155;
- t_relax=8.34e12 Gyr.

The scale separation R/lambda_sigma is at least 44,155 in every tested state, supporting the small-wavelength prerequisite. It does not independently validate a Maxwellian/incoherent bath, weak collective response, or the chosen velocity proxy.

Dividing every timescale by 100 as a deliberately generous prefactor sensitivity still leaves a minimum 8.34e10 Gyr. This is not a rigorous lower bound over all possible dynamics. It shows that an ordinary order-unity normalization uncertainty cannot bridge the discrepancy within this kinetic scaling.

Holding the fastest case's sigma, R and eta fixed, t scales as rho^-2. Reaching 14 Gyr would require rho larger by about 7.72e5, approximately 419 solar masses/pc³. That is a conditional algebraic comparison, not a prediction of a dense phase. Such density is not the reconstructed cluster envelope and cannot be substituted without changing its mass profile. Early compact substructures are a separate, uncomputed regime.

## What has been removed from the mechanism search

The proposal “wave interference will gradually thermalize the broad cluster component and thereby choose its occupations today” does not work on these reconstructed states and support-scale assumptions. The slow process cannot erase their assembly memory on cosmic time. This is a useful distinction from merely saying that occupation weights are unknown.

Three different mechanisms must not be conflated:

1. **Smooth wave gradient support:** previously too weak to hold the broad envelope at the imposed eta.
2. **Secular gravitational wave relaxation:** now quantitatively too slow on the tested envelope states.
3. **Violent relaxation/formation:** changing mean potentials can redistribute orbital energy on crossing times without the weak-scattering process above. This remains possible, but its source mass, energy, angular momentum, baryonic history and boundary flux must be specified and derived independently if a no-new-input prediction is claimed.

The present source-free action conserves the global cold norm. It does not select its primordial value, and local escape/retention depends on initial and boundary data. These conservation facts do not forbid an emergent statistical profile, but they prevent treating an assigned occupation distribution or retained mass as an absolute prediction from vacuum energy.

Preserving the galaxy law remains a separate condition. Under selective coupling, positive cold mass inside a galaxy adds GMc/r² to its already-calibrated baryon law. Slow relaxation in present clusters does not supply a mechanism that removes this extra contribution from galaxies. That requires a demonstrable formation/exclusion history or a changed action, not a temperature chosen to fit clusters.

## Limits and next discriminating step

The preceding negative-shell uncertainty result remains unchanged: actual joint covariance is missing, and reconstruction/coupling choices affect the signs. This timescale audit does not solve that likelihood problem. It evaluates only the positive central shell requirements without covariance propagation.

The remaining formation route should be tested as an initial-value problem with an independently constrained supply and energy budget. A density target alone is insufficient. The existing CCT transport program has not yet demonstrated a converged late outcome for all matched dwarf controls; this work does not restart its jobs or claim those open gates passed. A new cluster run would need the same bookkeeping and a galaxy control from the same physical prescription.

Collective near-instability enhancement, coherent nonlinear collapse, early compact environments and external driving are not covered by the secular estimate. None has been shown here to select both the vacuum/force ratio and the required retained mass without additional inputs. The original mechanism objective remains OPEN; the named secular route has a scoped quantitative obstruction.

## Checks and reproducibility

The normal run completes; a separate mutation multiplies eta by 1000 in the pc-km/s implementation and fails the independent SI comparison. The unmutated maximum SI relative discrepancy is 8.89e-16. Density-squared and eta-cubed scaling checks pass, with the logarithm held fixed where appropriate. Every source mass is compared with the committed prior calculation. Both run manifests validate with raw input and output hashes.

All calculations use one numerical thread and a 60-second bound. No large simulation, new dataset, parameter fit or modification of shared experiments was performed. Full evaluated rows and exclusions are in run/timescales.csv and run/excluded_shells.csv. Evidence is a self-reviewed finite calculation with an explicitly approximate kinetic transfer, not a peer-reviewed theory completion.
