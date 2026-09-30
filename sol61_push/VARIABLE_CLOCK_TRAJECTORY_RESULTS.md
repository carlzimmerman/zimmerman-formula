# Evolving the variable clock from radiation to its vacuum

Base 64064c1166. Mathematical decision: does the scalar-dependent coupling probe in VARIABLE_CLOCK_RESULTS.md have actual expanding homogeneous trajectories connecting its early moving force balance to the late stable vacuum? Verdict: numerically verified for five explicitly stated initial conditions and toy parameters, conditional on numerical accuracy. No universal basin theorem, realistic cosmology or exact 32π mechanism is established. This is self-review.

## Equations and finite contract

Use A=B=M²=Z=1, lambda(q)=1+ell q, U=q^−2+q², S=2+3ell q, with radiation only. Define n=ln(a/a_initial), x=ln q, w=dx/dn, v=q w and rho=10^8 exp(−4n). The expanding lapse constraint and acceleration equation give

    H²=2(rho+U)/(3S−v²),
    h=dlnH/dn=−[4rho/(3H²)+v²]/S−3ell v/S,
    x'=w,
    w'=−w²−(3+h)w−[U'+(9ell/2)H²]/(H²q).

Require 3S−v²>0. The log scalar coordinate enforces q>0. Integrate n in [0,12], evaluating 1201 points. Constrained runs use scipy Radau, rtol=10^−8, atol=10^−10, max_step=0.02. Initial q is the zero-force root at rho=10^8, with w=4/3, for ell={0.1,1,10}. Two further ell=10 runs start at 0.9 and 1.1 times that q with w=0. These are five samples, not an exhaustive initial-condition family.

The endpoint criterion is relative q and H² distance below 10^−5 from the analytic de Sitter vacuum, and |w|<10^−4. Each sampled denominator remains positive and each run satisfies that endpoint criterion.

| ell | Initial q multiplier | Initial w | Initial lambda | Final lambda | Largest sampled kinetic fraction |
|---|---|---|---|---|---|
| 0.1 | 1 | 4/3 | 1.000511 | 1.096874 | 0.05960 |
| 1 | 1 | 4/3 | 1.002373 | 1.864916 | 0.03728 |
| 10 | 1 | 4/3 | 1.011037 | 8.795472 | 0.00987 |
| 10 | 0.9 | 0 | 1.009933 | 8.795472 | 0.00991 |
| 10 | 1.1 | 0 | 1.012140 | 8.795472 | 0.00984 |

Kinetic fraction means (qdot²/2)/(rho+U+qdot²/2); maxima are over the stated grid, not certified continuous maxima. Radiation ends at approximately 1.425×10^−13 in these units. The ell=10 tracking sample has q approximately 0.01646 at n=2, 0.33694 at n=4, and 0.77954725 at n=12, approaching the unique vacuum q*=0.77954730.

## Orthogonal equation check and numerical failures

For ell=10 with initial multiplier 1, also integrate the acceleration equation as an independent state equation rather than substituting the lapse constraint. Keep x,w and H² as three states, with (H²)'=2hH². Use rtol=2×10^−12, atol=2×10^−14, max_step=0.005. This is a second equation implementation using the same solver and scalar force, not a fully independent code or precision certificate.

The final bounded run, runs/variable_clock_trajectory_h2, passes all 19 checks. Across the comparison grid its largest relative constraint residual is 2.274×10^−8, largest relative q difference is 6.740×10^−9, and largest relative H² difference is 3.489×10^−8. The predeclared residual threshold is 10^−6; trajectory agreement threshold is 10^−5.

Earlier diagnostics are retained. An unmanaged initial log-H-state probe failed the constraint check at 1.398×10^−6. Under the bounded runner's one-thread environment, the same initial script passed with residual 7.206×10^−7. The tighter log-H-state variant, runs/variable_clock_trajectory_v2, failed with residual 1.331×10^−6 despite tighter tolerances. These are numerical-sensitivity observations, not erased failures or evidence that every implementation attains the stated precision. The H² variant keeps the same acceptance thresholds and materially reduces the residual. Its bounded evidence is the basis of the finite result above.

The exact equations explain why this redundant check is sensitive to absolute errors. Define E=(3/2)S H²−rho−U−qdot²/2. Substituting the scalar, acceleration and radiation equations gives Edot=0 identically, even for nonzero E. An initial or accumulated absolute error therefore becomes a larger relative constraint error as the density drops. The H² variant records an exact symbolic check of this identity as well as the numerical residual. This explains the sensitivity mechanism, but does not prove that roundoff alone accounts for every difference between runs.

## Formal early scaling and physical limits

The leading radiation-dominated force balance has

    q approximately c rho^−1/3,  c=(4/(3ell))^(1/3),
    w approximately 4/3.

Along this formal branch, substitution into the lapse constraint gives

    H²/(rho/3)=1−rho^−1/3/c²+O(rho^−2/3),
    kinetic_fraction=(8c²/27)rho^−2/3+O(rho^−1).

These are asymptotic expansions conditional on tracking with the displayed leading q,w behavior, not a proof of tracking from arbitrary initial data. The finite integrations establish reachability only for the tested samples. The early expansion approaches the GR expression with the bare G; that is not automatically the measured G_N. Neither the local calibration nor the scalar boundary condition in a galaxy has been solved for this new action.

The trajectory changes the premise of the constant-coupling obstruction: the early and late lambda values need not agree. It is therefore worth pursuing this route beyond the homogeneous force-balance diagram. It does not yet rescue observations. There is no matter era, entropy-transfer calculation, abundance likelihood, physical scale calibration, inhomogeneous stability or strong-coupling analysis. Approaching lambda=1 may itself create a dynamical limitation. The surface-response causality obstruction remains open, and ell and the other couplings are free rather than selected to yield 32π.

The next load-bearing question is whether the variable-coupling action admits healthy inhomogeneous modes and a consistent cosmological-to-galaxy scalar boundary condition. Either calculation can invalidate this homogeneous success; neither can be replaced by fitting ell to the target.
