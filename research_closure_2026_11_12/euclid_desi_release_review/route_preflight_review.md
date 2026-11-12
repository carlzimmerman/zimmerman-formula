# Independent SPARC-grid T-identifiability preflight review

12 November 2026. Read-only code/contract/input/output review. I did not rerun the ring quadrature or any observational fit. Independently checked supplied source hashes, the 42 unique scenario records and catalogue-column/data-unit mapping; reconstructed the analytic Jacobian and exact inclination null.

## Verdict

PASS for the stated narrow computation: a local pointwise-algebraic Fisher design on three actual SPARC radial grids with quoted relative velocity errors. CONDITIONAL for the derivative used for radial source gradients, approximate inclination treatment and prior choices. NOT ESTABLISHED: observed posterior precision, fitted T/a0, held-out predictive success, correct nonspherical AQUAL dynamics, full baryon/geometry covariance or a high-redshift/Euclid feasibility forecast.

No core algebra error was found. One presentation/model-scope correction is necessary before using the smallest errors to support the joint distance-free route: 'gas_known' fixes the angular gas coefficient and is not equivalent to knowing a physical gas conversion factor while distance remains unknown.

## Input and coverage checks

All four copied input SHA256 values match the predeclared source hashes. Parsed catalogue indices agree with distance, inclination/error, disk scale length and quality columns. Rotmod files provide R[kpc], Vobs/error[km/s], gas/disk/bulge velocity components and SBdisk[L/pc^2]. The acceleration conversion V^2*10^6/(R*KPC) is correct. The signed-square gas convention preserves outward gas contributions; total fiducial baryonic acceleration is required positive. All three selected templates have zero bulge in retained rows.

Exactly 42 unique records occur: 3 galaxies x 2 laws x 7 scenarios. NGC2403 uses 73 rows, R=0.16–20.87kpc; NGC3198 43 rows, 0.32–44.08kpc; DDO154 12 rows, 0.49–5.92kpc. Fiducial gb/a0 spans respectively 0.044–1.26, 0.033–2.17 and 0.015–0.063. The dwarf is deep throughout; neither spiral supplies a broad gb/a0=0.1–10 window. Samples were declared development targets, not independent/blind prediction targets. All valid radial rows are used, but this does not establish independent resolution modes.

This is real radial sampling, not a fit to the real circular-speed curve: the gravity response is evaluated at Upsilon=.5, a0=9.3603e-11 and published baryon templates. Observed V and error enter fractional-error weights; model residuals are not evaluated or used to select points.

## Independent Jacobian

Write angular source S_ang=A_star bstar+A_gas bgas, T=D a0, and w_model=f(S_ang,T). For both specified homogeneous two-scale acceleration laws, define t=dlnw/dlnT and a=1-t=dlnw/dlnS_ang. The code correctly uses t=a0/(g+2a0) for simple-mu and t=1/[2(1+S/a0)] for the quadratic law at its fiducial physical template S. Let fstar=bstar/S and fgas=bgas/S (fstar+fgas=1, including signed gas terms). For a small source slope gamma and inclination i in radians, the derivative row is

    J=[a fstar, a fgas, t, a fstar dln(gstar)/dgamma, 2cot(i)].

The inclination term is the derivative of log(v_los^2) when the intrinsic circular-velocity template is projected by sin^2(i). If instead one perturbs an already deprojected observed w, the sign changes, but the identifiable information/null space is equivalent when treated consistently. Here the fixed-geometry forward-model reading is consistent.

Since a+t=1,

    J_star+J_gas+J_T - tan(i) J_i/2 = 0.

This exact null is correctly detected; stored maximum residual is 2.22e-16. All six free-inclination cases (3x2 laws) return rank deficiency and no finite sigma_T. A finite catalogue inclination prior explicitly supplies information along this otherwise unidentifiable direction. Photometric deprojection changes with i are omitted, as disclosed; their actual coupled derivative could add information or nuisance structure, so the fixed-geometry degeneracy is a clean submodel result rather than a theorem about all possible imaging/kinematics likelihoods.

Quoted e=2 errorV/V is the linearized natural-log error in w=v^2/theta; conversion sigma_log10T=sigma_lnT/ln(10) is correct. The Gaussian i prior is converted from degrees to radians correctly. Unknown centre, beam smearing, pressure correction, warp/noncircular motions and correlated radial errors are absent. Whether quoted errors and the separate i prior are independent requires the source velocity-error definition; it is not proved by the table header.

## Necessary gas-label correction

With an independently known gas conversion factor alpha_g, b_gas is distance independent in physical acceleration units. However the angular dynamics source is D alpha_g b_gas: A_gas=D alpha_g still contains unknown D. Fixing A_gas in a T=D a0 inference is an additional angular-amplitude/distance assumption, not merely 'gas known'. In local SPARC with an adopted catalogue D it is a valid optimistic control, but its tiny ~0.004–0.013dex errors must not be promoted to distance-free joint-kappa capability. Relabel that scenario as 'fixed angular gas coefficient / fixed adopted distance control', or add D explicitly with its own likelihood. The free-A_gas scenarios already cover unknown angular gas normalization and are the relevant conservative controls for the proposed BAO-scale-free construction.

## Gradient prior and geometry audit

The code computes a softened axisymmetric ring response for a source perturbation Sigma_star(r)->Sigma_star(r)(r/Rd)^gamma. Its derivative uses log(r/Rd), correctly corresponding to a natural-log power exponent gamma. Gaussian sigma_gamma=.1 or .3 is NOT a .1/.3 dex radial M/L uncertainty. Across the observed radial interval, .1 corresponds to differential log10 M/L uncertainties .212dex (NGC2403), .214dex (NGC3198), .108dex (DDO154); .3 triples those numbers. Prior means are implicitly gamma=0. These are sensitivity brackets, not independently observed population-gradient constraints.

The ring response includes off-radius source contributions, improving on an incorrect local acceleration rescaling. But it interpolates sampled SB logarithmically, assumes a central continuation, extrapolates the outer profile, cuts the source at twice the maximum sampled R and fixes a Plummer-like softening h=.1Rd. It then transports fractional response gg/g0 to the published disk force. That is a surrogate derivative, not an exact rederivation of the original published disk model. Agreement of baseline shape and thickness kernels has not been shown. Varying source cutoff, SB continuation and softening is needed to establish physical robustness. A single gamma direction does not cover arbitrary M/L or unseen-gas gradients; the earlier exact counterexample remains applicable.

The two quadrature resolutions change derivative values by at most .00581, .00894 and .000163 respectively. These are absolute derivative differences, not errors on T and not evidence that source geometry is correct. They are recorded rather than threshold-tested or propagated through the Fisher calculation. For a precision claim, rerun local information with both grids and compare marginalized sigma_T and gradient response; also perform a small finite-gamma source perturbation to verify the linear derivative and its applicable range. At gamma uncertainty .3 and large r/Rd, nonlinear effects may matter.

## Meaning of the reported errors

The printed sigmas are square roots of inverse expected Fisher curvature plus specified Gaussian prior precisions, at a fixed fiducial model and diagonal log-error approximation. They are local Gaussian forecasts, not observed posterior intervals or frequentist coverage statements. Full rank after a prior does not mean the data themselves identify every parameter. With near-degeneracy, broad posterior nonlinearity, positivity boundaries and real model mismatch, Fisher intervals can be misleading.

Rank/eigenvalue thresholds are applied to unnormalized parameters mixing logarithms, gamma and inclination in radians. Condition numbers and threshold rank (outside exact nulls) depend on parameter scaling; interpret them as implementation diagnostics, not invariant physical precision. A scaled Jacobian SVD and nuisance-projected T information are preferable for quantitative design decisions. The analytically demonstrated free-i null does not depend on this numerical convention.

Useful reported pattern, with no promotion to achieved performance: freeing gas shifts the fixed-i error to ~.039/.026dex for NGC2403 (simple/quadratic), .114/.069dex for NGC3198 and .390/.598dex for DDO154. With catalogue i and gamma=.1 brackets they become .080/.056, .140/.086 and .392/.600dex. Thus the data grids do not support a universal precision claim. The deep dwarf loses most information when gas amplitude is free, in line with the analytic deep-regime degeneracy. Catalogue-i floors and other common errors do not disappear by adding galaxies.

## Smallest useful next checks

1. Correct the angular-gas label/parameterization before quoting the optimistic row in the joint distance-free route.
2. Report nuisance-projected data information separately from prior-restored information, with standardized parameter scaling. Explicitly state no posterior/coverage calibration has been performed.
3. On one preselected spiral only, verify the source-gradient derivative using direct small positive/negative gamma perturbations and variation of thickness/source cutoff; propagate the coarse/fine derivative difference to sigma_T.
4. Inject a physically allowed inclination plus radial-population perturbation into a synthetic observable on this actual grid and attempt parameter recovery with one held-out independent radial mode. The key output is T bias/identifiability under the nuisance envelope, not agreement with the real observed curve.

Until those checks, the result is a useful local warning and design discriminator: under optimistic template assumptions some grids have conditional T information; free inclination destroys it and flexible gas/gradients substantially degrade it. It is not yet a validated observable or a pathway that has passed the joint cosmological gate.

## Reviewed artifact hashes
- `route_redshift_sparc_preflight.py`: `244c1df756fa86dd6c19d4227b2d80ae29fe24c4d32b73da826caa75d7635181`
- `route_redshift_sparc_selection.json`: `e6da2d63b6a06122b0fae0c8ca6377563bbad45e2b9de0d920ca6065c31a73fa`
- `route_redshift_sparc_contract.json`: `4ac6599af6033142ea13c07f5bcf68948248f371cef3a456160c09a1fb7135a5`
- `route_redshift_sparc_run01/results.json`: `7d0765ce5a52ff015c20f06417d05f8c412d77cb03c21ed4f6ceb5e5b3d0cc9f`
