# Cluster audit: real pipeline errors, and the discrepancy that remains

2026-09-06. Inspected HEAD `6978397a4bc47f0e1bf1ded52103371a3419fff4`, with a dirty working tree. Existing files were not edited. This is a diagnostic audit, not a new gravity action or a statistical exclusion of a theory.

## Outcome

Three load-bearing arguments in the repository are unsound: a gas-radius conversion, a comparison mixing different interpolation laws, and a purported cosmology-independent baryon-budget exclusion. Removing them does **not** make the tabulated cluster profiles agree with the exact exponential law using observed baryons alone. It does reopen an unjustifiably excluded possibility: an additional, as-yet-unidentified baryonic component. It does not establish that such a component exists.

### 1. A definite radius-unit error

`hunt_2026/h67b_xcop_core_eta.py:68` treats the gas profile's `RADIUS` as Mpc and multiplies it by 1000. The FITS column is actually `R/R500`. Its own extension header supplies `R500` in kpc. For example, A2029's header is 1414 kpc; the separate repository JSON gives 1423 kpc and must not replace the file's normalization.

The independent audit reads the units and uses the matching header. As an orthogonal check, both the gas and hydrostatic bundles contain an `M_NFW` column. Comparing those columns at the inferred physical radii gives a median-of-cluster-medians discrepancy of **38.60% with the old conversion, versus 0.0371% with the header conversion**. Agreement of two representations of the same published function validates units; it does not validate NFW physics.

The corrected gas grid begins at 29.978–30.009 kpc, depending on cluster. No extrapolation is allowed. Consequently the 30-kpc stack changes membership. Fixed-sample conclusions use radii at least 40 kpc. Even then, a tabulated model grid is not proof that raw observations independently resolve every point.

### 2. Three laws were being treated as interchangeable

Write `b = g_bar/a0` and `y = g/a0`. They are distinct variables.

| Repository usage | Prediction |
| --- | --- |
| h67b / hunt_lib Route A | `y = b/[1-exp(-sqrt(b))]` |
| User's exact exponential mu | solve `b = y[1-exp(-y)]` |
| g03r saturated carrier | exact branch for `b <= 1-1/e`; otherwise `y = b+1/e` |

g03r imports the nine Route-A residual medians into a comparison computed with its carrier law. It also compares a single assumed baryon profile with twelve-cluster medians; five clusters have imputed stellar profiles. These ratios cannot certify the carrier's fitted amplitude or profile. The reported g03r X1 numerical failure remains reproducible, but is not a clean same-theory empirical gate.

The new script recalculates each cluster from its own masses for each law, showing seven stellar-file and three relaxed-cluster subsets separately. At the adopted canonical `a0 = 9.3619e-11 m/s^2`, the seven-file acceleration-ratio medians are:

| Radius | Old gas units, Route A | Correct gas units, exact mu |
| --- | ---: | ---: |
| 100 kpc | 2.894 | 3.890 |
| 300 kpc | 2.501 | 3.540 |
| 1000 kpc | 1.613 | 2.252 |

The JSON also separates the unit correction from the kernel change. The larger alternative `a0` gives corrected exact-law medians 3.599, 3.262, 2.072 at the same radii. These are central reconstructed values, not significance estimates. Seven stellar files are not a guarantee of seven complete modern baryon inventories; the published three-relaxed subset below is the safer comparison.

### 3. The cosmic baryon fraction is not a hard ceiling for each cluster

`real_research/reviews/mi_cluster_measurement_audit_2026.py`, Part C, says supplying extra cluster baryons would require more baryons than the universe contains. That inference does not follow from a local baryon fraction exceeding the cosmic mean.

For a population containing fraction `w` of a common total-mass inventory, the actual accounting identity is

\[
\bar f_b=w f_{b,c}+(1-w)f_{b,\rm rest}.
\]

The exact counterexample `w=0.02`, `f_b,c=0.5`, `bar f_b=0.16` gives `f_b,rest=0.153061...`, with positive baryon and nonbaryon inventories everywhere. This is not an observed population or a cosmological fit. It disproves the claimed implication, not the need for a global baryon census. For a missing-baryon hypothesis, one must integrate its required extra mass over the actual cluster population and compare with the independently available inventory; one cannot replace that calculation with a local cosmic-fraction ceiling.

Furthermore, X-COP's frequently cited approximately 6% nonthermal pressure fraction was inferred using an expected universal gas fraction and simulation calibration. It is not an assumption-free direct measurement usable unchanged to veto alternative gravity. This dependence is explicit in [Eckert et al. (2019), section 3.2](https://arxiv.org/abs/1805.00034v2).

There is also no basis for treating X-ray and SZ reconstructions of the same gas as wholly independent tests of its equilibrium. Their measurements are complementary, but share physical assumptions. A fitted NFW curve to the same hydrostatic data is not a separate lensing detection.

## The gravity-independent starting point, and the conditional MOND test

For stationary, spherical gas with ordinary metric coupling, the thermal-pressure estimate is

\[
g_H=-\frac{1}{\rho_g}\frac{dP_{\rm th}}{dr}.
\]

Writing `M_H = r^2 g_H/G` is a convenient label, not a decision that the force is Newtonian or that the excess is CDM. With the user's *isolated spherical modified-gravity* law and no extra source, the requirement is

\[
g_b=g_H(1-e^{-g_H/a_0}),\qquad
M_{\rm source,req}=(1-e^{-g_H/a_0})M_H.
\]

Thus the additional **source** mass is `M_source,req - M_b`, not `M_H - nu M_b`. An acceleration ratio must not be relabelled as a required baryonic mass multiplier.

| Cluster, 300 kpc | `g_H/g_prediction` | Required total source / observed baryons | HSE factor needed for baryons-only equality |
| --- | ---: | ---: | ---: |
| A1795 | 3.540 | 7.533 | 0.282 |
| A2029 | 3.783 | 7.470 | 0.264 |
| A2142 | 3.254 | 6.281 | 0.307 |

These three systems are the no-known-merger subset used by Kelleher & Lelli (2024). The calculation inherits the repository's published profiles, stellar inventory, distances, geometry, and HSE assumption. It is not a refit of their newer data. Changing among FORW, NFW, and Einasto reconstructions at this radius leaves ratios above three for all three systems; that sensitivity check does not encompass all observational systematics or constitute independent evidence for CDM.

There is a useful exact necessary condition:

\[
\boxed{0\le g_H-g_b\le a_0/e.}
\]

Indeed `(g_H-g_b)/a0 = y exp(-y)`, whose derivative is `(1-y) exp(-y)` and whose unique maximum is `1/e`. SymPy verifies the stationary point and endpoint limits. At 300 kpc the observed-profile excesses are 4.192, 5.502, and 4.425 times this upper bound, respectively. This exposes a failure of the **baryons-only, isolated, spherical, equilibrium interpretation of these central profiles**. It is not a universal no-go for relativistic MOND, an external-field calculation, or an assertion that all measurement uncertainties have been bounded. The bound itself is already present in the repository's g03j/f21 line of work; no novelty claim is made.

## A pressure-only explanation has a checkable sign and boundary cost

Allow an isotropic nonthermal pressure `P_nt`. Static force balance requires

\[
g_{\rm model}=g_H-\frac{P'_{\rm nt}}{\rho_g},\qquad
P'_{\rm nt}=\rho_g(g_H-g_{\rm model}).
\]

Where the baryons-only prediction is below `g_H`, the pressure must therefore **increase outward** to remove the discrepancy. A decreasing outward pressure provides extra support and requires *more* inward gravity. A positive pressure fraction alone does not determine the sign; the derivative matters.

Integrating gives a precise boundary condition:

\[
P_{\rm nt}(r)=P_{\rm nt}(R)-\int_r^R\rho_g(s)[g_H(s)-g_{\rm model}(s)]\,ds.
\]

Consequently nonnegative pressure throughout the interval demands

\[
P_{\rm nt}(R)\ge\max_{r\le R}\int_r^R\rho_g(s)[g_H(s)-g_{\rm model}(s)]\,ds.
\]

The three relaxed profiles have a positive deficit throughout the sampled 50–1000-kpc interval. Using the derivative of the same log-interpolated cumulative gas mass, the required outer pressure is 1.467, 2.896, and 1.986 times `10^-11 Pa`. These equal **71.9%, 73.6%, and 72.2% of the thermal-pressure DROP across that interval**, not percentages of the local outer pressure. Refining 400 to 1600 radial points changes these pressure requirements by less than 0.011%. This is numerical convergence of a profile surrogate, not observational precision.

With zero nonthermal pressure at the outer endpoint the required inner nonthermal pressure is negative: that restricted proposed explanation is impossible. Nonzero boundary confinement, anisotropic stresses, nonequilibrium motions, and errors in reconstructed thermal gradients were not excluded. In the purely thermal time-dependent case, Euler's equation instead requires an outward material acceleration `Dv_r/Dt = g_H-g_model`; the JSON records its required value rather than assuming equilibrium.

## What is open and the next discriminating calculation

The result is **OPEN**, not a completed theory and not a detection of bad cluster measurements. A core-weighted residual in the supplied profiles survives this audit. Its identity is not fixed by calling the inferred acceleration a mass.

The efficient next calculation is a joint, per-cluster fit for A1795, A2029, and A2142 using the published nonparametric pressure/density posterior samples and independently analysed lensing or galaxy kinematics, with the same physical baryon profiles and exact kernel. Keep boundary pressure, nonthermal gradients, stellar inventory, and distance uncertainties explicit; do not insert a universal baryon-fraction prior. A mismatch confined to gas would implicate equilibrium/plasma modelling; a matching discrepancy in independent metric probes would demand missing source or modified field response. A geometric clock must then derive the required response from its own action—it cannot be inserted as an empirical mass profile and declared closed.

Undetected cold baryons are a legitimate, constrained alternative to particle CDM, not a discovery made here. [Kelleher & Lelli (2024), sections 5.1 and 5.4](https://arxiv.org/abs/2405.08557v2), explicitly study missing baryons and hydrostatic bias in MOND clusters. Their models and interpolation law are not substituted for this project's exact exponential law, and their fitted mass ratios are not imported into our results. Cold-cloud survival, star formation, emission/absorption, merger behaviour, and the global baryon inventory remain tests to do.

## Reproduction and exact files

Created in this directory: `cluster_audit.py`, `test_cluster_audit.py`, `results.json`, `manifest.json`, `verification.json`, and this report. Only these six artifacts belong to this audit. They were initially delivered without a commit or push; publication was subsequently requested. Before publication, all nine regression tests passed again and an independent rerun reproduced every stored result field on HEAD `a4afae4dc3170456ca993349b89924afb370fa88`. The original manifest retains its actual computation commit. Other dirty files were preserved.

The producer uses the installed Conda `python` at `/opt/homebrew/Caskroom/miniconda/base/bin/python`; the system `python3` lacks Astropy. No dependency was installed. `manifest.json` records software versions, input FITS hashes, source hashes, runtime, commit and dirty state. `verification.json` records exact important commands and outputs.

```sh
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/cluster_audit.py --write
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/cluster_audit.py --require-central-profile-agreement
OPENBLAS_NUM_THREADS=1 python -B hunt_2026/h67b_xcop_core_eta.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/g03j_scalar_carrier_kernel.py
```

Producer: exit 0. New regression tests: 9 passed, exit 0 (initial red run: 9 failures, exit 1 before implementation). Exact central-profile agreement diagnostic: exit **2**, failure; its `10^-6` tolerance is numerical equality, not an observational confidence interval. Existing h67b: 10 checks, exit 0 **despite the demonstrated units bug**. Existing g03j: 4 checks, exit 0; this reproduces its numerical assertions, not a certification of every physical claim in its prose. Manifest schema validation: exit 0.

## Source ledger and limits

Checked 2026-09-06 using primary arXiv PDFs, with SciSpace and web search for discovery. No global novelty search was attempted. PDFs were inspected through the browser, not copied into this audit. Full source provenance of the older local stellar files, including differences from the later complete five-cluster inventory, remains to be authenticated. The 2022 BCG mass-to-light estimates include NFW halo modelling; satellite profiles are extrapolated fits, and intracluster light is omitted (sections 2.4 and 5.3). The local stellar files must not be called a gravity-independent or complete census. A joint reanalysis must revisit these assumptions too.

- **Ettori et al., Hydrostatic mass profiles in X-COP galaxy clusters**, A&A 621 A39 (2019), DOI `10.1051/0004-6361/201833323`; arXiv `1805.00035v3`, revised 2018-10-31. Section 3.1 distinguishes fitting thermal profiles in the forward method from imposing a parametric gravitational mass profile in the backward method. The implication “FORW assumes an NFW dark-matter halo” is not supported. Spherical HSE and fitted thermal profiles remain assumptions. [Source](https://arxiv.org/abs/1805.00035v3).
- **Eckert et al., Non-thermal pressure support in X-COP galaxy clusters**, A&A 621 A40 (2019), DOI `10.1051/0004-6361/201833324`; arXiv `1805.00034v2`, revised 2018-10-04. Section 3.2, equations 6–9, infer nonthermal pressure using expected gas fractions and a simulation-motivated radial parametrization. Their `alpha=P_NT/P_tot` is a pressure fraction, not generally the hydrostatic mass bias. Importing its numerical value as an assumption-free MOND constraint is invalid. [Source](https://arxiv.org/abs/1805.00034v2).
- **Eckert et al., The gravitational field of X-COP galaxy clusters**, arXiv `2205.01110v1`, 2022-05-02. Sections 3.3–3.4 distinguish parametric pressure fitting from the nonparametric reconstruction. Section 5's decreasing inferred MOND missing-mass profile is explicitly conditional on systematic uncertainties. This is adjacent work, not proof that the current local FITS bundle contains those newer nonparametric posteriors. [Source](https://arxiv.org/abs/2205.01110v1).
- **Kelleher & Lelli, Galaxy clusters in Milgromian dynamics: Missing matter, hydrostatic bias, and the external field effect**, arXiv `2405.08557v2`, 2024-05-15. Table 1 and section 2 distinguish three systems without known merger signatures from A644/A2319. Sections 5.1 and 5.4 discuss missing baryons and systematic-dependent mass profiles. This supports keeping those alternatives open, not their empirical confirmation or this exact kernel. [Source](https://arxiv.org/abs/2405.08557v2).
