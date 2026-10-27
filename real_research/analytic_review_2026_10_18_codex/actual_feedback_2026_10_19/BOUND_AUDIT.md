# Independent audit of the actual-subfamily full linear work bound

19 October 2026. Auditor: isolated subagent `/root/audit_actual_bound`. This is an analytic proof audit; no numerical integration, scientific script, numerical array, process inspection/control, or repository edit was performed. The only write by this auditor is this new scratch report.

## Normalized claim and primary verdict

**Verdict: proved as written**, for theorem (T) in the exact synthesis revision identified below, together with its geometry and operator companions. This verdict is for the explicitly chosen small-mass subfamily. It gives no verdict of proof for an arbitrary fixed halo, a dark-dominated annulus, nonlinear receiving characteristics, or nonlinear confinement.

For fixed positive G, a0, Mb, let rM=sqrt(G Mb/a0). There exist one fixed positive dimensionless warmth delta and epsilon_*>0 such that, for every 0<epsilon<epsilon_*, the actual exact-density smooth equilibrium with

    ell=epsilon rM, f=epsilon^2, (r0,r1,r2,R)=ell(1,2,3,4)

satisfies, for every smooth compact radial fixed-L canonical generator g0 supported in its open occupied region,

    sup_{t>=0,theta0,i,q in CLOSED occupied actions} |W_i(t;theta0,q)|
      <= C_delta (G Mb/ell) epsilon ||g_hat0||C12,

where g_hat0=g0/(ell v_*), v_*^2=G Mb/ell, and the derivative norm is on one fixed enlarged dimensionless physical phase box. W is the full coupled linear field's time derivative integrated on an equilibrium receiving orbit. Both species, all nonzero harmonics, the circular line, and the flat energy cap are included. The constant is uniform in sufficiently small epsilon but may depend on fixed delta. No real-frequency spectral inverse is assumed.

The final synthesis contains two load-bearing clarifications that are absent from the raw packets taken alone: transversality on the whole coarea rectangle, and an O(epsilon) field bound for the zero receiving harmonic. Their inclusion is essential to this verdict.

## Dependency graph

1. Actual smooth cutoff p and original force laws -> exact normalized potentials and perturbation kernels.
2. Smooth parameter family through the Kepler limit, fixed intrinsic edge weight, and the parent exact inverse -> a single fixed positive delta and uniformly smooth normalized exact DFs/susceptibilities.
3. Uniform Morse-period chart and Kepler frequency on a fixed enlarged action rectangle -> a frequency lower bound, full-box lambda transversality, and bounded orbital derivatives.
4. Physical shell indicator Fourier estimate + the Lipschitz source kernel + full-box coarea -> frequency densities with the stated harmonic powers, including their zero extensions across the cap and action endpoints.
5. Spatial interpolation + the elementary Banach-valued Cauchy estimate -> upper-closure operator bound and Holder modulus O(epsilon).
6. Smallness of that established operator norm -> Neumann inverse on the whole real boundary and upper strip; no spectral exclusion leaf remains.
7. Canonical source differentiation with a fixed C12 norm -> uniform O(epsilon) Holder and weighted 1/z forcing estimates.
8. Uniform energy coercivity and small weight mass -> O(epsilon) field amplitude; this treats k=0.
9. Resolvent identity + source estimates + receiving harmonic decay + the Dini work inequality -> a summable |k|^(-3/2) log(2+|k|) bound for k!=0.
10. Sum harmonics and restore the potential unit -> theorem (T).

The parent exact inverse and classical linear evolution/energy identities are internal proof dependencies, not external citations or computations. Their raw derivations were inspected. No load-bearing scientific computation is used by this proof. The original RESULT.md's (NM_Sigma), outlined Lemma T, and outlined Prop F are bypassed by the explicit smallness/coarea/source arguments here.

## Obligation matrix

| Obligation | Status | Decisive check |
|---|---|---|
| Actual profile and species fractions | Passed | M/Mb=epsilon p, Mt/Mb=epsilon^3 p, Mf/Mb=epsilon(1-epsilon^2)p, with the original smooth cutoff and exact M=Ar annulus. |
| Actual potentials and reciprocal kernels | Passed | The tether equilibrium repulsion is epsilon^4 Vp2; its perturbation kernel is 2 epsilon integral p/u^4. Cross kernels remain -1/max. |
| Deep-cubic/core restrictions | Passed | f rM/r0=epsilon and 2f^2 rM/((1-f)r0)=2epsilon^3/(1-epsilon^2). Both improve as epsilon decreases. |
| One fixed positive warmth | Passed | After normalization the radial interval, intrinsic H, normalized target p', and edge logarithmic derivative bounds are fixed. The potential family is uniformly smooth through epsilon=0. Choose the X5 inverse and positivity width once, then decrease epsilon for feedback. |
| Uniform higher inverse/DF derivatives | Passed | The error is inverted only in X5; q=e-Eq and the one-derivative gain bootstrap every fixed higher norm. Fixed exponential edge flatness absorbs the finite inverse powers introduced by physical derivatives. No simultaneous smallness in all Xs is used. |
| Actual susceptibility smallness | Passed | Linearity in target amplitude gives w_f=epsilon(1-epsilon^2) mathfrak_w_f and w_t=epsilon^3 mathfrak_w_t with uniform fixed-order derivatives at fixed delta. This is more than a mass estimate. |
| Epicyclic taper estimates | Passed | Recomputed p'<=17, |p''|<=336; positive p'' only inside rho<=2. Thus Bp<=1344 and Cp>=-2858, giving decreasing K_i^2 for epsilon<=1/4096. |
| Full-box transversality | Passed in synthesis | On [1/2,6] x [0,j_*], Omega_K=(j+sqrt(lambda))^-3 and its lambda derivative is strictly negative with a compact positive margin. Uniform parameter-dependent period derivatives preserve this margin after shrinking epsilon_box. Occupied-set monotonicity alone would not suffice. |
| Regular circular chart | Passed | The smooth orbital map uses a=sqrt(j); dJ=2a da. No 1/a derivative is introduced in coarea. At a=0 nonzero radial harmonics vanish. |
| Flat cap/L-edge extension | Passed | The exact susceptibility and its needed derivatives extend by zero. At each fixed a, zero endpoint traces permit clipping the inverse lambda chart; the a integration domain remains fixed. |
| Physical shell harmonic exponent | Passed | A radial sublevel set is one interval on the angle circle, so its nonzero Fourier coefficient is <=1/(pi |n|). Integrating the radial derivative from above apocenter gives the full Lip_r bound O(1/|n|). |
| Coarea exponent and output interpolation | Passed | P_n contributes n^-1, the Jacobian contributes n^-1, and phi_n contributes n^-1/2; hence c_n=O(epsilon n^-5/2). Interpolation gives beta=1/4 in C^(1/2)_r, and multiplication by nu gives F_n=O(epsilon n^-3/2). |
| Cauchy Holder estimate | Passed | Symmetric subtraction controls the near singularity, exterior integration costs log(2+D), increments cost h^beta(1+log(1/h)), and Poisson extension gives every alpha<beta on the upper closure. alpha=1/8 is valid. |
| Uniform operator norm and decay at infinity | Passed | Sum n^-3/2 log(2+n). Each fixed harmonic tends to zero at infinity and this summable operator majorant permits dominated convergence. |
| Actual inverse, without an assumed spectral leaf | Passed | Choose C_delta epsilon<1/2. The Neumann inverse has norm <=2 and the resolvent identity gives its Holder modulus. Embedded and threshold kernels are excluded by a proved norm inequality. |
| Uniform C12 canonical source norm | Passed | D costs one derivative, six integrations by parts in theta and one lambda derivative cost at most seven more. Smooth orbit maps and smooth zero-extended w control the coefficients. C12 is ample and there is no division of generator derivatives by w. |
| Weighted 1/z source bound | Passed | Small n have support separated from z by |z|/2; the large-n Cauchy tail has six powers of harmonic decay. The support-length logarithm remains summable. |
| O(epsilon) zero harmonic | Passed in synthesis | Integral w=O(epsilon), Q0=O(epsilon N^2), uniform coercivity, and Cauchy-Schwarz give m=O(epsilon N) and sup psi=O(epsilon N). Using only ||h0||Q would lose the required factor. |
| Closed-set receiving estimate | Passed | Uniform receiving coefficient decay is |k|^-1/2, with Omega>=Omega_->0. The Dini split adds the needed |k|^-1 log factor. Sum the resulting |k|^-3/2 log(2+|k|). |
| Physical units and generator norm | Passed | J_*=ell v_*, t_*=ell/v_*, so D_physical g0=v_*^2 D_hat g_hat0. Work restores one factor v_*^2=G Mb/ell, exactly as in (T). |
| Arbitrary fixed halo/dark-dominated annulus | Out of scope | The actual annulus here is baryon dominated; mass ratio is O(epsilon). The smallness argument cannot be substituted at order-one mass ratio. |
| Nonlinear actual paths and confinement | Out of scope | The receiving trajectories and dynamics in this theorem are linear/equilibrium ones. No nonlinear label-gradient or path estimate is supplied. |

## Decisive checks and potential failure points

### Uniform exact inverse constants

The normalized potential family is

    phi_f=-1/rho+epsilon Vp,
    phi_t=-1/rho+epsilon(1-epsilon^2)Vp+epsilon^4 Vp2.

It is uniformly smooth on fixed positive compact radial intervals. The intrinsic coordinate obeys d rho/d xi=H(rho) with the same fixed H=(rho-1)^2(4-rho)^2/27 for every epsilon. The normalized density shape p' is also fixed. Thus the parent inverse's constants depend on uniformly bounded inputs, including uniformly comparable edge weights and uniformly positive circular-well curvature. Scalar density amplitude cancels from the relative Xs norm. This justifies the fixed-delta and O(epsilon) susceptibility use; positivity of the total mass alone would not justify it.

No arbitrary smooth extension at t=0 is being substituted for physical smoothness. Physical states have t>=0; the parent construction is smooth through t=0, and the a=sqrt(j) orbit chart avoids differentiating a singular angle chart in j.

### Coarea and Cauchy bounds

At fixed a, |Delta lambda|<=C|Delta nu|/|n|. The source-radius kernel difference is min(n^-1,|Delta lambda|), while the field coefficient difference is min(n^-1/2,|Delta lambda|^1/2). Combined with w and the coarea Jacobian this gives exactly the c_n estimates used in the synthesis. Across clipped frequency endpoints, the vanishing w trace supplies the same bound. Flat cap motion contributes no moving-domain boundary term because w is already extended by zero in the fixed rectangle.

For a C^beta Banach-valued density, the symmetric local subtraction is a Bochner-integrable difference bounded by |u|^(beta-1). The exterior kernel integral over an interval of length D costs at most C log(2+D), uniformly in its location. The boundary increment estimate h^beta log(1/h) implies C^alpha for any alpha<beta. The Poisson argument preserves the Banach norm bounds and yields vertical as well as horizontal upper-closure continuity. These bounds are uniform operator bounds, rather than estimates only after evaluating on individual fields.

### The epsilon factor in work

The spectral companion's displayed bound by N6(h0)=||h0||Q+B6(h0) is not by itself a proof of the requested epsilon rate: ||h0||Q is normally O(sqrt(epsilon)). The final synthesis correctly avoids that inference. The nonzero receiving harmonics use only the O(epsilon N) weighted/Holder transform bounds. The zero harmonic uses the separate O(epsilon N) field bound.

The parent energy constants are uniform here: its B_i and restoring lower bounds are positive Kepler perturbations on the fixed normalized shell, and its field coefficients and mass derivatives have bounded normalized norms. Equivalently, the bounded physical shell kernel gives an immediate small-weight estimate for the interaction quadratic relative to A. Either check supports the uniform coercivity already used in the synthesis. Conservation is the original symmetric-kernel quadratic conservation, not a spectral exclusion assumption.

For the Dini step one may use a common upper bound L=C_delta epsilon N for both the full transform's Holder seminorm and weighted supremum. Near omega=k Omega(q), the receiving density is bounded by C L |k|^-3/2, whereas its modulus is bounded by C L |k|^-1/2 s^(1/8). Integrating their minimum against ds/s gives C L |k|^-3/2 log(2+|k|), uniformly in q and the Laplace damping. This avoids any hidden loss through a ratio of data norms. At k=0 the work is a field endpoint difference.

## Remaining gap and strongest safe statement

There is no remaining load-bearing gap in the precisely restricted synthesis theorem (T) at the audited revision. The raw companion packets alone did not explicitly close the full rectangle extension and the epsilon scaling through the zero harmonic; Sections 2, 4, and 5 of the synthesis close those points.

The strongest safe conclusion is the existence of a nonempty, positive-warmth, exact two-species halo subfamily with a whole-closed-occupied-set bound for full linear work on equilibrium orbits, uniform as epsilon decreases in the chosen normalized norms. It is not a theorem for every member of the original family. The original general fixed-halo spectral/boundary problem and nonlinear confinement problem remain open. For the next broader claim, the cheapest meaningful check is an exact statement of its fixed profile and the replacement for the small-susceptibility bound; the present Neumann estimate cannot establish an order-one-mass assertion.

## Provenance and exact revisions

This is an independent audit by an isolated subagent. The auditor was given raw artifacts and derived the scaling, harmonic powers, endpoint treatment, Cauchy estimate, and source/work estimates independently. The coordinator was informed of the two raw-packet omissions before supplying the final synthesis. Agreement between authors is not used as evidence.

Audited synthesis:

* `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/ACTUAL_SUBFAMILY_BOUND.md`, SHA-256 `2f5c920eb1a73a5215bb0ef93d8dc261dac212fbf4cb3e0deb8d59cc6af262b4`.

Audited raw companion revisions (the coordinator's repository copies are intended to be byte copies):

* `/private/tmp/halo_actual_geometry_20261019.md`, SHA-256 `1848347266a2254e18fc579c3c6804cd6703895ce9d298f804a69acd977558c9`.
* `/private/tmp/halo_actual_spectral_20261019.md`, SHA-256 `52c042ff02f04c0e6917e2591d9527fbf07952ce64b6f674b240f83e4c9fb47c`.

Parent raw proofs inspected:

* `full_feedback/RESULT.md`, source SHA-256 recorded by the companions as `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
* `smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`, source SHA-256 `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.
* `finite_halo_2026_10_18/BOUNDARY_MATCHING.md`, source SHA-256 `eab2312cf87a23267dd639c064ee8fb39a5b07d809e27ffae0b3eedd1557b774`.
* `smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md`, SHA-256 freshly checked as `ff33f52fb33a7166a10ae5ba0c99b873ae581916286c6eefca2f70f86b880cb4`.

Read-only commands used: `cat`, `sed`, `rg`, `rg --files`, and `shasum -a 256`; applicable proof-audit skill and checklist were read. No existing artifact or ledger was edited by this auditor. This report is not a computation certificate or an external literature verification.
