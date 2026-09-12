# L191: statistical and code reconciliation

L191's reported PASS count does not establish the original spiral gate or one common parameter pair across both footings. The committed best selections fail the original ceiling, the source relaxes that ceiling, and its boundary comparison changes the kick speed at the same time. A small independent benchmark also finds substantial drift in the allegedly equilibrium controls. None of these findings is a universal exclusion of an action-derived C003 completion.

Audited exact source revision: **9b97161a6**. Current files matched the committed source when the benchmark ran. No Fable files, Git state, or other agents' reports were changed.

## Findings decided directly from committed code and results

1. **Different fitted velocities across footings.** The absorbing canonical best is `(700 km/s, n=2)`; the alternative best is `(1000 km/s, n=2)`. V1 checks their separately selected retention vectors while describing them as one pair. It does not implement a common-pair condition. This does not prove no common pair exists: the full alternative grid was not saved in the JSON.

2. **The spiral ceiling changed.** The original 0.105 becomes `0.105*1.35 = 0.14175` in V1. The four saved best spiral values are 0.128128, 0.126939, 0.128334, and 0.122778. All fail 0.105; all pass 0.14175. At fixed n=2, the no-kick probability is exp(-2)=0.135335, 28.89% above the original ceiling. Under the parent's explicitly stated homogeneous-Poisson, fixed-flow assumptions, the expected no-kick contribution already prevents the strict gate; equality to that floor additionally requires zero positive-kick contribution to the chosen final observable.

3. **The boundary comparison confounds the kick speed.** V2 compares canonical absorbing best700 with free best1000. The cluster difference is `0.533500 - 0.664304 = -0.130804`. The same committed JSON permits the actual fixed1000 comparison: `free1000 0.533500 - absorb1000 0.491394 = +0.042106`. Changing the velocity reverses the apparent sign and triples its magnitude. The analogous common1000 spiral difference is -0.013626; the best-to-best comparison was +0.000207.

4. **Annular mass is not enclosed mass.** `simulate` returns mass in `0.3 <= r/r_anchor < 1`, despite the introductory description of N(<r_anchor). No mass initially lies below 0.3. Heating can change the profile, so multiplying an annular mass by its initial isothermal fraction does not recover the heated enclosed mass. The new benchmark records both separately.

5. **The implemented initial condition is not an equilibrium distribution.** The untruncated isothermal distribution in a log potential is stationary. Multiplying it by a spatial indicator `0.3 <= r/r_anchor <= RMAX` is not a function of conserved energy and removes inward/outward orbital phases. Free evolution refills and empties the cuts. An absorbing outer boundary further drains the controls. Normalizing by an evolving control can cancel some initialization effects but does not prove stationary-halo behavior or identify a fraction of the original physical halo mass.

6. **The claim “every galaxy has exactly exp(-n) retention” is stronger than the computation.** For paired particles, the zero-kick particles follow their controls identically. The total observable also includes a nonnegative contribution from particles kicked at least once. Its size depends on the observable, kick speed, potential, observation time, and boundary. Finite independently seeded ratios can sit below exp(-n) because exp(-n) is a population expectation, not a pathwise lower bound on an independently normalized ratio. L191 reports neither the zero-kick contribution nor statistically calibrated confidence intervals. Its monotonicity tolerance of 0.05 is not an energy/convergence test.

7. **L191 changes more than the orbit solver.** It changes NFW confinement to a fixed baryonic log potential, replaces the original `(650 km/s, 2.307794872...)` parameters by fitted `(700 or1000 km/s,2)`, and distributes events uniformly over10 Gyr rather than using L189's DE-weighted event history. Thus its output cannot serve as a reproduction of the original fixed650 point or isolate why the earlier fixed-NFW test differed. The infinite log potential has no finite formal escape speed; claims based on kicks exceeding its escape speed require an additional truncation/EFE model.

8. **The latest project KiDS convention changed.** L190 now defines the repository gate as one-halo retained mass inside R200, superseding the earlier shell diagnostic. This audit records that source convention; it does not independently authenticate its observational interpretation. L191's galaxy anchor annuli do not evaluate that R200 observable. The cluster R200 numbers below likewise are not a1e12-host KiDS test.

## One bounded adversarial benchmark

Only the L191 cluster was rerun: 8192 particles per population, 12 populations covering its two selected footings, free/absorbing boundaries, a kicked population, a paired no-kick control, and an independently seeded no-kick control. Fixed n=2; canonical vk700 and alternative vk1000; no scan or refit. The source's spatially cut isothermal IC and fixed log potential are preserved. Independent vector kicks are applied for every event; six extra events would have been coalesced by L191's same-step `sqrt(count)` approximation. The source-selected pairs are explicitly different.

| Footing / boundary | Annular retention +/- paired SE | Enclosed-anchor retention +/- paired SE | R200 retention +/- paired SE |
| --- | ---: | ---: | ---: |
| Canonical700 / free | 0.71907 +/- 0.01251 | 0.72871 +/- 0.01076 | 0.74235 +/- 0.00793 |
| Canonical700 / absorbing | 0.66213 +/- 0.01156 | 0.67800 +/- 0.00977 | 0.68041 +/- 0.00777 |
| Alternative1000 / free | 0.56795 +/- 0.01124 | 0.57257 +/- 0.00981 | 0.60543 +/- 0.00789 |
| Alternative1000 / absorbing | 0.51819 +/- 0.01065 | 0.52943 +/- 0.00924 | 0.53971 +/- 0.00785 |

The canonical absorbing annulus separates into **0.12768 zero-kick + 0.53446 positive-kick**. Every zero-kick particle has exactly the same final weighted observable as its paired control (max identity error zero); all tested total observables exceed their realized zero-kick contribution. This is an executable check of the decomposition. It is not a proof that all populations attain equality at exp(-n).

Changing to the independent control seed gives annular ratios 0.72143, 0.65414, 0.57808, and 0.52039 in the same table order. Those shifts illustrate control sampling variability. The file includes approximate independent-control errors, explicitly conditional on sampled normalized weights; they do not fully propagate their random normalization and should not be used as rigorous confidence limits. The paired errors retain numerator/denominator covariance and are the errors quoted in the table.

The canonical no-kick control ends with **72.15%** of its initial annulus mass for free boundaries and **63.40%** for absorbing boundaries. Inside R200 the corresponding fractions are **70.13%** and **54.86%**. Thus sizable control redistribution/loss is measured directly, not merely inferred from the spatial cutoff.

The force is singular at the origin. The free-control99th-percentile dimensionless energy error is at most1.41e-4, but rare central passages have very large errors: the worst normalized energy discrepancy is29.6. No timestep or particle-number convergence was run in this deliberately bounded discriminator. Its exact paired-particle identities and source mismatches remain decisive, but the benchmark must not be advertised as a certified physical retention prediction or as proof of a threshold crossing near0.70.

## Reproducibility and limits

Used computation-audit and verification-before-completion workflows. The successful bounded job took approximately10seconds and exited0. Its source revision/hash comparisons and paired zero-kick identities can fail; all passed. `run_002/manifest.json` records actual argv, runtime, exit, actual HEAD, source inputs before/after, result/log hashes, software, seeds, and resource limits. `validate_manifest.py --root ...` exited0 and verified hashes. The earlier `run_001` completed the integration but failed JSON serialization of a NumPy integer; its exit1, traceback, and missing-result status are preserved. `run_audit.py` fixes serialization without altering the first-run source, so that failed provenance also remains hash-valid.

Source SHA256 values:

    L191_c003_orbit_integration.py  5eb930a4f7d83530d5daa130ad7fac101eafc641e3dfeae1ac9570c91372f816
    L191_results.json              754d319c6cc48be4f17381a690eaa76eef54c05d4ec813b8eaf44754e9f84df5
    L190_c003_radial_kids_and_cluster_shape.py
                                  0551e2f4c0b2b0cf1091c29a6023674d6e9479a6104d195837159d54942c4b98

No new particle physics, action term, universal no-go, lensing prediction, or scalar/metric closure is supplied. The missing physical implications remain the action-derived force/source law, self-gravity, consistent clock eligibility and rate history, physical halo boundaries, a stationary initial ensemble, and the actual observational estimator. L191's modified parameters and relaxed acceptance criteria cannot close those gaps.
