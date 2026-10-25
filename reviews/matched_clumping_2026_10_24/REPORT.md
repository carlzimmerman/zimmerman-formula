# Matched acceleration comparison: empirical constraints on a cold sector

This calculation finds a substantial cluster–disk offset at the same inferred baryonic acceleration, with a radial pattern that survives the specified sensitivity checks. Four supported dwarf comparisons do not establish a common extra excess. These are constraints on a framework's predictions, not a detection of a particular cold component or a derivation of its microscopic parameters.

The selection and statistic were committed in FROZEN_CRITERIA.md before this implementation. Earlier overlapping analyses were known; this is not a blind or independent observational replication. No MOND interpolation function, fitted a0, cold velocity dispersion, or per-system halo parameter enters the comparison. Existing stellar mass estimates and dynamical measurement assumptions still enter: “no new fit” does not mean assumption-free.

## What was compared

At each target's gbar, interpolate log(gobs) within adjacent accepted SPARC radial segments, with maximum separation 0.30 dex. Multiple crossings receive one median per galaxy; the reference is the median across galaxies, requiring at least eight. No extrapolation or bridging rejected points. Define Delta = log10(gobs_target) - median_galaxy(log10(gobs_SPARC)). For clusters, take the median of Delta over the six radii before comparing systems.

The reference pool contains 145 SPARC galaxies with at least one eligible adjacent segment, after quality, inclination and speed-error cuts. The cluster targets have 56–66 reference galaxies at each radius. The four supported dwarf targets have 11–59. The matched acceleration ranges are 6.45e-12–3.78e-11 m/s² for clusters and 1.91e-12–6.83e-12 m/s² for dwarfs. These are separate matches to SPARC, not a fully overlapping dwarf–cluster pair sample. SPARC has not been restricted to independently verified isolated systems.

Dwarf gobs uses the pressure-supported half-light estimator 3 sigma_los²/r_3D, with r_3D=4 r_projected/3 and stellar M/L_V=2. Cluster gobs uses published forward hydrostatic mass profiles. SPARC uses rotation curves. Stellar profiles are photometrically inferred masses, not direct mass measurements. Consequently, matching gbar does not match geometry, external fields, support mechanism or measurement bias.

## Primary results

| Targets | Systems | Median Delta (dex) | gobs / disk benchmark | 16–84% spread across systems (dex) |
|---|---:|---:|---:|---:|
| Matched dwarfs | 4 | +0.071 | 1.18 | −0.063 to +0.214 |
| X-COP clusters with stellar profiles | 7 | +0.416 | 2.61 | +0.383 to +0.446 |
| Previously designated relaxed subset | 3 | +0.403 | 2.53 | +0.386 to +0.423 |
| Lower-mass X-COP subset | 4 | +0.410 | 2.57 | +0.393 to +0.477 |
| Higher-mass X-COP subset | 3 | +0.432 | 2.70 | +0.395 to +0.439 |

The mass split is 7.63e14 solar masses in M_HSE(R500). Both subsets are massive clusters; these data do not test galaxy groups or establish a mass trend.

The 1,000-draw paired bootstrap resamples reference galaxy IDs globally and target systems, preserving cluster radial correlations. Conditional 95% sampling intervals for the median Delta are −0.086 to +0.256 dex for dwarfs and +0.372 to +0.464 dex for clusters. These omit full measurement covariance, distance and stellar-population errors, hydrostatic systematics, sample selection and non-equilibrium. They are not discovery significances or total error bars.

Matched dwarfs are Fornax (−0.075 dex), Leo I (−0.050), Leo II (+0.234), and Sculptor (+0.193). Of 33 dwarfs passing the physical/measurement cuts, 29 lack eight supported reference galaxies; 26 have zero reference galaxies, two have five, and one has three. Their apparent low-acceleration discrepancies must not be counted as matched evidence. All four baseline matched dwarfs belong to the MW sample, so this run does not establish host independence.

## Radial shape: the strongest distribution constraint in this sample

For a spherical Newtonian mass-equivalent diagnostic only, define

    M_eff(<r) = [gobs(r) - gref(gbar(r))] r² / G
    Q(r) = M_eff(<r) / Mgas(<r).

M_eff is a residual relative to an empirical disk acceleration benchmark. It is not automatically physical cold mass; in a nonlinear modified-gravity theory one must solve the source-response equation before identifying a cold density.

Across 0.1–1 R500, all seven systems have positive residuals and negative fitted slopes of log Q versus log r. With the same reference-galaxy intersection held fixed across each cluster's six radii, 25–45 reference galaxies remain, and the slopes are:

| Cluster | d log Q / d log r, descriptive fit |
|---|---:|
| A1795 | −0.641 |
| A2029 | −0.455 |
| A2142 | −0.407 |
| A2319 | −0.788 |
| A644 | −0.657 |
| A85 | −0.586 |
| ZW1215 | −0.370 |

These are finite-range slopes, not exact power laws or fitted microscopic constants. Individual profiles need not be monotonic at every sampled point. With the primary reference construction, median Q falls from 8.19 at 0.1 R500 to 1.85 at R500. Median acceleration excess falls from a factor 3.18 to 1.43. A decreasing cumulative mass ratio means the effective residual is more centrally concentrated than the hot gas over this range; it does not measure subhalo abundance, compact clumps, local density slope or particle properties.

## Prespecified sensitivities

Each row changes one assumption; this is not a joint uncertainty envelope.

| Change | Cluster median acceleration ratio |
|---|---:|
| Baseline | 2.61 |
| Maximum interpolation gap 0.15 / 0.50 dex | 2.60 / 2.61 |
| SPARC stellar masses ×0.8 / ×1.2 | 2.35 / 2.79 |
| Cluster stellar masses ×0.5 / ×2 | 2.66 / 2.48 |
| Hydrostatic bias b=0.2 / 0.3, Mtrue=MHSE/(1−b) | 3.26 / 3.72 |

All available common-reference radial slopes remain negative under these checks. Positive conventional hydrostatic mass corrections increase the discrepancy. The stellar-mass tests cover the stated multipliers only; they do not exhaust alternative stellar-remnant populations or missing baryonic components.

Changing dwarf M/L_V to 1 yields two supported dwarfs and a ratio 1.18; changing it to 3 yields seven and 0.96. Because match eligibility changes, this is a selection-plus-mass sensitivity, not a fixed-sample error bar. It reinforces that a precise universal dwarf cold amplitude is not identified here.

## Consequences for the framework

1. A universal empirical algebraic response gobs=F(gbar) alone does not describe the central values of these disk and cluster measurements. Subject to the baryon and dynamical estimates, the theory must predict the cluster offset through additional gravitating material, structural/environmental response, or another independently constrained physical effect. Geometry and external fields are not controlled by this test, so it does not exclude every universal field equation.
2. If an additional cold component contributes an additive Newtonian acceleration on top of the disk benchmark, a radius-independent cold/gas mass ratio is incompatible with these central profiles: Q decreases strongly outward. Under that restricted interpretation its cumulative distribution must be more concentrated than the hot gas. For nonlinear coupling, translate this diagnostic through the field equations before imposing a cold-mass profile.
3. The four supported dwarfs provide no basis for assigning every dwarf a new common excess amplitude. The 29 unsupported systems cannot be used to infer such an amplitude by extrapolation in this lane.
4. The lower/higher cluster subsets do not identify a new mass-dependent parameter. The residual also persists in the designated relaxed subset, so restricting to that subset does not remove the observed offset.
5. These observations constrain macroscopic predictions, not u^3/(v sqrt(e)), a quantum symmetry, a cold-sector sound speed, particle mass, self-interaction cross section, thermalization threshold or a0. None is measured by this run. Keep the microscopic matching problem open.

The useful reduction is to reject, conditional on the measurement model, a gbar-only algebraic description and a gas-tracing additive residual. Require a candidate cold-sector dynamics to predict the cluster radial pattern while preserving the disk relation, without assigning each object a fitted cold normalization. The present data do not select a unique mechanism among candidates.

## Scope and provenance

Inputs are existing local copies; none were downloaded or modified. SPARC uses gas plus fixed stellar coefficients 0.5 (disk) and 0.7 (bulge); the gas squared-speed term retains its sign. Seven of the twelve locally available X-COP clusters have stellar profiles and enter, each at six radii. The remaining five are explicitly excluded. Model-derived cluster radial points are correlated, not 42 independent systems. Globular cluster dynamical-fit masses were excluded as circular baryonic inputs. Low-mass groups, matched supernova histories, lensing, merger offsets, direct cold substructure measurements and an isolation-matched galaxy sample are absent.

Primary source descriptions: [SPARC data](https://astroweb.cwru.edu/SPARC/) and [mass-model paper](https://arxiv.org/abs/1606.09251); [Local Volume Database](https://arxiv.org/abs/2411.07424) and [catalog repository](https://github.com/apace7/local_volume_database); [X-COP mass-profile paper](https://arxiv.org/abs/1805.00035) and [data products](https://dominiqueeckert.wixsite.com/xcop/data). The numerical results above are this local computation, not quotations from those papers.

Artifacts: compare.py, contract.json, run/result.json, run/targets.csv, run/reference_matches.csv, run/rejections.csv, run/comparison.png. The normal and deliberate-mutation run manifests hash declared raw inputs and outputs and record software versions and resource limits. Ten controls cover interpolation, lack of extrapolation, adjacency, signed gas, SI conversion, known residuals and physical-acceleration reconstruction. The deliberate mutation doubles target accelerations and must fail the reconstruction check; this is a pipeline-integrity control, not independent authentication of the catalog measurements.
