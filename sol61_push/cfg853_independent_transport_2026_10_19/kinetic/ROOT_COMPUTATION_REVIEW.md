# Independent numerical review of the two-tracer construction

Reviewed 2026-10-19 by `/root/kinetic_candidate`, against the exact inputs below. I read `compute.py`, `VIRIAL_DERIVATION.md`, `source_extraction.json`, and saved results/manifests. I did **not** read the root's eventual result report. Another reviewer owns the symbolic proof audit; this review checks its numerical implementation, conventions and evidence scope.

**Verdict:** the central mass-floor arithmetic, positive-mass LP comparison, all 16 declared sensitivity corners, and all 32 saved aperture-budget rows are independently verified in their stated conditional domain. I found no computational defect that changes the main result. The observational application remains conditional on matched intrinsic tracer densities and whole-population moments; the source table does not itself certify those hypotheses.

## Authoritative run and hashes

The parent identified `run_002` as authoritative after a source-note correction and the addition of a clearly labelled new-survey global-dispersion sensitivity. Its runner-v2 manifest validates against current inputs, with `run.status=completed`, exit status 0, wall limit 30 s, CPU limit 20 s, one numerical thread, and no hard address-space limit. It reports 159 checks and no missing/invalid result files.

I first checked `run_001`, which is historical: validation correctly detects changes to `compute.py` and `source_extraction.json`. It must not be presented as a current-input reproduction. The central two-tracer result is byte-value identical between the two saved result dictionaries. No root input was changed in this review.

Observed repository HEAD during review: `e3fc772b519512de59c4b68260df00bc086d590d`. Review pins:

| Artifact relative to the root packet | SHA256 |
|---|---|
| `compute.py` | `485f065ae09b603c0f789860945fb8794cab3f27c1bf87a3627963893079a885` |
| `VIRIAL_DERIVATION.md` | `d21e561cbf81a94a5334fb465d4bc05a1e43192565deb3a008788d96894031dd` |
| `source_extraction.json` | `9a6114429005c7436d2e2cd1cf766bdeb7e11f8c2c4f6692d8f4a9d7e1115839` |
| `run_002/manifest.json` | `dcb2eaffc0f50a3b744f94b7a922298d925beb01e0ca7659f207dca180697ec3` |
| `run_002/results.json` | `69dd0c127267d36461cb9981ca0cab44c8557c0d3231894ac8e455780929f170` |
| `run_001/manifest.json` | `5a87fa58717ac7b68d64b3a6cafa892acd0f3b761043261a8ff56c05511995f4` |
| `run_001/results.json` | `f060b772f917a29e9a27ae19c64d11c6c87431f1cbddad499485e6d30c47c837` |

The current root manifest also pins the old CE086 result, CFG861 binary output and LVD catalogue. I read those raw inputs for the independent budget replay; their hashes are checked by the validated manifest. Source authentication is version/URL based; no remote-source byte hash is claimed.

## Weight, scale and unit conventions

For a spherical Plummer number-density profile, projected enclosed number is proportional to `R²/(R²+a²)`, so its projected half-number radius is exactly `a`. The use of `a=D tan(Rh)` is therefore internally consistent with the declared spherical reinterpretation. A `4/3` deprojection factor belongs to the old aperture estimator, and correctly does **not** enter this virial kernel. The two central radii independently evaluate to 501.147472006113 and 916.577979218237 pc.

Each tracer equation uses its own normalized density and second moment. Its total number or luminosity cancels separately. Consequently the table fractions `.63/.37` should not multiply the two equations, and their absence from `mass_floor` is correct. Number weighting is admissible when **both** the intrinsic tracer density and the full-population velocity moment use that weight. Mixing a number-profile scale with a different luminosity-weighted moment would need an additional bridge. A radial observational selection is not automatically a stationary dynamical tracer population.

The code's `G_PC_KMS=G*MSUN/(PC*10^6)` has units pc (km/s)²/Msun. It correctly converts the two equations to `y_i=3 a_i sigma_i²/G`. The source Gaussian width is squared once. Treating it as a whole-population virial second moment is a hypothesis, not a numerical identity established by the table. Relative population systemic velocities and any residual streaming require a common rest-frame treatment before application.

A common radius multiplier preserves `h=a2/a1` and the moment ratio, while multiplying every mass floor and shell radius by the same factor. The code's geometry cases are therefore correct sensitivities. They are not an exact theorem for two elliptical populations with arbitrary shapes.

## Independent central computation and LP

I did not import or call the root's `mass_floor`. I used 65-digit Decimal arithmetic, a separate Taylor evaluation of sine/cosine for the angular conversion, and the shell ratio equation. With `Q=(y2/y1)^(2/3)`, I independently solved

```
b² = (Q-1)/(a1^(-2)-Q*a2^(-2)),
M  = y1 [1+b²/a1²]^(3/2).
```

This gives:

| Quantity | Independent value |
|---|---:|
| `y1` | 17,124,409.069501795 Msun |
| `y2` | 70,469,629.31719157 Msun |
| `y2/y1` | 4.115156851905416 |
| `h³` | 6.118030327970613 |
| Sharp mass floor | 369,414,762.8995151354 Msun |
| Equality shell radius | 1,301.957481913719 pc |

The saved binary64 mass is 369,414,762.89951533 Msun, agreeing to its rounding precision. This verifies arithmetic for the claimed measure bound; physical stationary distribution-function existence at its shell extremizer is not established.

The root's 2,001-bin LP gives 369,465,609.8051922 Msun, about `1.3764e-4` above the analytic floor. I independently constructed a different 3,201-bin grid, from zero plus 3,200 logarithmic radii over `[10^-4,10^4] a1`, without inserting the equality shell. SciPy HiGHS returned 369,426,044.3937604 Msun, a positive relative gap `3.0538829e-5`. Only the two bins at 1,299.705273977312 and 1,307.210906675289 pc were active. Their masses were 257,070,014.037604 and 112,356,030.3561564 Msun. The equality residual was zero at displayed precision, and the solver dual objective matched the primal to rounding; the minimum grid dual slack was `3.33e-16`.

The decreasing positive discretization gap and neighboring active bins are consistent with the analytic shell extremizer. A finite LP does not prove the continuum inequality. Its result is conditional on solver tolerance; the analytic proof is the load-bearing continuum argument.

## Sensitivity and inventory coverage

I independently enumerated the Cartesian product

```
Rh_MR = {.318,.360} deg; Rh_MP = {.57,.67} deg;
sigma_MR = {6.6,7.4}; sigma_MP = {9.8,11.3} km/s.
```

All 16 unique tuples are present exactly once in saved order, without filtering or early exit. Fifteen admit finite positive mass measures. The incompatible corner is `(.360,.57,6.6,11.3)`, where `R=4.641410531898174` exceeds `h³=3.969564860795568`. Across feasible corners the saved floors range from 144,247,110.977121 to 3,414,893,936.82646 Msun. Independent mass values agree to maximum relative error `1.08e-14`.

These are **endpoint sensitivities only**: no claim about a posterior, parameter independence, confidence level, or the minimum joint floor throughout the continuous rectangle follows from this 16-point enumeration. Distance, luminosity, M/L, geometry and covariances are not varied there.

I separately reconstructed all 32 budget rows from the catalogue, CE086 and CFG861 inputs. The largest absolute difference in a free-stock fraction was `2.22e-16`. For Sextans, `M_V=-8.72`, the assumed `Upsilon=2` yields `Mstar=526,053.5983790774 Msun`. With the fixed cold/baryon ratio 5.364 and retention .1, the generous total is `(1+53.64)Mstar=28,743,568.615432784 Msun`. This includes all stars and all cold, without subtracting the retained draw twice. It is deliberately more generous than the remaining-free-stock aperture budget. The central joint and outer-only floors exceed it by factors 12.85208415983434 and 2.45166597996310 respectively.

The stock is conditional on old catalogue luminosity and M/L; it is not a measured total-mass ceiling. The new tracer radii use 84.7 kpc while the old catalogue lists 85.9 kpc and an older luminosity/structural determination. A fully updated source/inventory comparison should use matched distance and luminosity. This does not change the stated arithmetic contract.

The relative binary transfer gives Sextans sigma 6.5662003 km/s and fraction .6452872, but this is a sensitivity rescaling from a subset. The absolute cleaned-subset value is 7.9479022 km/s versus the old 7.9, giving fraction 1.0020454. The new global 8.3 km/s inserted at the **old** aperture gives 1.1038178. These three values cannot be interchanged as successive measured corrections. In particular the table's two widths are not newly binary-cleaned versions of the old one-point input.

## Source application and residual limitations

I directly checked [Tolstoy et al., arXiv2504.02787v1](https://arxiv.org/html/2504.02787v1), Table 2 and Sections 4.2–4.3. The numerical extraction is correct. The table fits elliptical Plummer number profiles and Gaussian widths to a selected 303-star sample. It does not supply certified spherical whole-population moments. Selection/completeness, intrinsic profiles, membership, relative means, radial variation and equilibrium require a forward-modelled bridge. No unconditional mass exclusion or completion/failure of the underlying field theory is established by this review.

The numerical mass-floor test additionally assumes Newtonian gravity sourced by a nonnegative finite mass measure. Additional non-Newtonian acceleration, external terms or a different tracer force are outside that model. Any added gravitating envelope must enter its total inventory and both moments. The support-radius test concerns **all** gravitating mass, not only a compact core.

My supplementary read-only arithmetic command ran in about .0204 s of Python-reported elapsed time, with observed maximum RSS 61,980,672 bytes on Darwin. Software: Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4; deterministic, no randomness. These independent checks were an inline audit command, not a separately persisted runner-v2 experiment; no independent manifest or durable executable is claimed. The original validated run and its exact command remain in `run_002/manifest.json`. Only this review file was written for the review task.
