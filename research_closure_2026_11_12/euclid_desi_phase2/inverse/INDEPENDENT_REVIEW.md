# Independent phase-2 inverse-route review

12 November 2026. Read-only inspection of sparse/dense selections, contracts, scripts and all six completed result/manifest blocks. No refits, extra experiments or observed gravity residuals. Source copies match their four declared SHA256 hashes.

## Verdict

The scoped synthetic implementation is internally consistent. The dense shared-reference contrast covariance is correctly whitened; analytic velocity Jacobians have the correct factors; all six blocks have the expected 48 full cases and successful recorded best/profile optimizations. This is a finite, noiseless synthetic design study on old SPARC grids, not a measured posterior, a validated galaxy model, an AQUAL result or a precision forecast with actual independent population/gas/geometry data.

A necessary metadata correction is identified below. The strongest useful conclusion is conditional: source-mode coverage, angular-gas calibration and inclination information are different requirements. Population-profile precision alone does not remove the remaining amplitude directions. A precise but wrong inclination prior can leave substantial T bias.

## Coverage and reproducibility

Sparse per galaxy: 3 smooth injected shapes x 2 inclination truths x 2 inverse families x 4 population-error brackets =48 cases. Dense per galaxy: 3 shapes x 2 inclination truths x 2 inclination-prior widths x 2 gas-prior brackets x 2 population-error brackets =48 cases. Across three galaxies this is 288 full-case fits; these are correlated scenarios, not 288 independent galaxies or repeated-noise coverage trials. Each full fit uses three T starts. Sparse has four bump profile curves per galaxy; dense eight, all on a 25-node -.30 to +.30dex grid. Additional +/-.05dex probes are only in the declared zero-inclination-bias subsets.

All six manifests record completed status. Stored all-checks flags are true, all best/profile success flags pass, and recorded full-fit multistart objective spreads are small. Sparse DDO154 has two active-bound full cases; dense has none. Sparse bump profiles hit their scan edge in DDO154 and NGC3198; dense DDO154 has four edge-touching intervals. These outputs must remain truncated/grid intervals, not closed confidence bounds.

## Covariance: correct dense implementation, important interpretation

For independent raw node log-M/L errors e_j with variance sigma² and a common independent reference error e_0 of the same variance, relative errors d_j=e_j-e_0 have

    Cov(d_j,d_k)=sigma²(delta_jk+1).

Thus C=sigma²(I+11^T), each individual contrast has standard deviation sqrt(2)sigma and every distinct contrast pair correlation 1/2. The dense code builds L L^T=I+11^T and uses solve(L,r/(sigma ln10)); its objective is r^T C^-1 r. The same whitening is used in its Jacobian. This is correct under the specified independent raw-node model.

The sparse block instead assumes independent direct contrast measurements. That is a distinct hypothetical measurement model, not the same shared-reference covariance with fewer nodes. Sparse-to-dense comparisons must therefore name the changed source model and not attribute every change solely to radial knot count.

**Necessary metadata fix:** `selection_dense.json` retains the old `external_constraints` wording saying only R/Rd=.3,3,10. The actual dense script uses all nine non-reference knots [.1,.3,.6,1.5,2,3,6,15,40], relative to the reference at 1. There is no dense knot at 10. The later `population_covariance` text correctly describes raw errors, but the key `external_relative_population_contrast_errors_dex` can still suggest marginal contrast errors. Correct publication wording to 'raw node sigma=.02/.05dex, nine correlated contrasts'. If changing selection or code, preserve existing manifested inputs and add a fix-forward notice rather than silently rewriting a run's provenance.

These are hypothetical all-stellar-M/L measurements, including IMF. No instrument, spectroscopy or colours-to-M/L calibration demonstrating such information is supplied. Some dense knots, particularly 40Rd, are beyond the observed rotation range and depend on a very faint extrapolated stellar profile. This is a demanding stipulated information pattern, not information Euclid currently supplies.

## Forward model, mismatch and gradient scope

The truth functions are smooth bend, bump and soft break in log radius. The inverse uses either a single power or piecewise-linear log-M/L values. Thus the nonlinear source shapes genuinely differ between truth and inverse families; this improves on injecting the exact fitted power law. Truth is positive and computed through the ring source integral. Global source amplitudes remain positive and free.

However truth and inverse share the same SB continuation, source cutoff at 2Rmax, softened ring kernel h=.1Rd and calibration to the published disk force. This does not test geometry mismatch, alternate thickness, unknown gas radial structure, coupled imaging inclination, noncircular motion, PSF convolution or a self-consistent nonspherical AQUAL field. The evaluated law is the pointwise simple-mu prescription. No quadratic-law or general gravity class result follows from this phase-2 block.

The dense inverse has only nine relative knot parameters with linear interpolation and constant endpoint continuation. It is not an arbitrary positive function: between-knot wiggles or additional gas components can restore inverse degeneracies. The three tested truth shapes are not an exhaustive adversarial/minimax class. The source-grid tail and low-radius continuation remain assumed; numerical optimizer success does not validate them.

Analytic derivatives are consistent with pred=sqrt(r g) sin(i)/sin(i0): stellar/gas log-amplitude columns pred*(1-t)*fraction/2, T column pred*t/2, source-mode columns from the derivative of exp(B shape) through the ring kernel, and inclination column pred*cot(i). SI/kilometre conversions are consistent. Sparse code's finite-difference derivative checks support its shared model implementation; dense uses the same formulas with an enlarged basis, not a separate physical verification.

## Angular gas prior and distance independence

The dense .03dex prior is on log10 A_gas with A_gas=D*conversion and mean fixed to the injected true angular amplitude. It is not merely a .03dex conversion-factor prior. The selection correctly states that independent distance and conversion information, or an equivalent genuinely independent angular-mass constraint, is needed.

This calibrated angular amplitude breaks an actual null direction. If supplied via an absolute distance assumption it reintroduces that absolute information into the galaxy T inference; one cannot then describe the precision gain as distance-free without carrying the distance likelihood and its cross-covariance into q and BAO. The algebraic q construction may remain ruler-invariant, but the statistical input is no longer free of the distance calibration used to obtain A_gas. A prior inferred from the same galaxy gravity fit would be circular and is not independent.

The mean is centred on truth in these synthetic gas-prior cases. The experiments do not inject gas-calibration bias. Therefore they establish conditional sensitivity given an unbiased stipulated prior, not robustness to a wrong gas amplitude.

## Inclination bias: useful negative result

Truth i is either the catalogue value or +3deg. The inverse prior stays centred at the catalogue value with width 3deg or .5deg. Only velocity projection changes; the source/light deprojection remains fixed. This is a clean amplitude-error experiment, not a full warped-disc geometry test.

For +3deg truth, making the wrong prior .5deg is not automatically safer than a broader prior. Dense .03dex-gas and .5deg-i cases retain maximum T biases about .0436dex (NGC2403), .0239dex (NGC3198) and .0448dex (DDO154), across the tested shapes. Very small velocity residual powers coexist with these shifts. Thus external precision without accuracy does not certify T. Profiling all amplitudes can absorb projected-velocity bias, while independent gas information only partly restricts that tradeoff.

## Nominal objective markers and uncertainty claims

These are noiseless alternative-profile means. Gaussian population/gas/inclination residuals are hypothetical priors centred as declared, not sampled measurement realizations. A delta-objective=1 curve is a nominal profiled penalized-likelihood marker, not a coverage-calibrated 68% interval or proof of a .05dex measurement. Boundary effects, misspecification and nuisance-prior bias invalidate automatic chi-square confidence interpretations.

The +/-.05dex probes are placed around the injected truth, not necessarily around each best fit. A minimum delta>=1 at those two points does not by itself determine a symmetric sigma, exclude disconnected minima, or show interval coverage. Full bump curves provide more information but are only 25-node scans and are run for one truth shape. Profile fits are warm-started single runs, not the three-start search used at the unconstrained optimum; optimizer success is local, and absence of a lower-than-recorded-best profile is useful but not a global-optimum proof.

The dense gas-free rows are instructive: max best-fit biases can be small while +/-.05dex profile penalties remain far below one. Accurate recovery of noiseless truth does not imply high information. With .03dex angular gas and .5deg inclination priors, all three templates have minimum +/-.05dex penalties above one in the recorded finite shapes, but that is explicitly conditional on those stipulated external constraints and the restricted inverse family.

## Required publication corrections and safe conclusion

1. Fix forward the dense external-node description and distinguish raw-node sigma from correlated contrast sigma. Do not alter manifested run inputs silently.
2. Name the angular-gas prior's distance requirement next to every precision statement; it is not conversion-only information.
3. Keep nuisance bias, nominal profile width and measured coverage separate. State that no observation or posterior-coverage experiment was run.
4. Preserve nonspherical-gravity, source-mode and shared-geometry limitations; no AQUAL or all-positive-profile claim is warranted.

Safe conclusion: 'For three synthetic source-shape families on three old radial grids, denser hypothetical all-M/L information reduces some template bias, but useful T constraints additionally depend on angular-gas amplitude and inclination. Even precise external priors can transmit calibration bias. These are input requirements for a future measurement, not a validated measurement.'

No additional experiment is requested by this review.

## Reviewed hashes
- `selection.json`: `0ef744e0bfbbecc060b691d1f1d80f0ca2bf55dd0441c06dbc56f15f0228651f`
- `contract.json`: `e6104a339022514971b6c374e2dc11db6e9bd83bf82ba087ee38fb421a4f4595`
- `experiment.py`: `4fc6f6f836f079556f5135f8a55c43ecb429c50bf9cd8664ab866ad855f42588`
- `selection_dense.json`: `eb42e105987ce5b038ec8a6c58f54ea3e8494bdfc598f19cb1ea0144b747ada7`
- `contract_dense.json`: `559c22cb677a805da1dbf10e6a287fecea20dc2d724b9782e2bc936f7fb12afb`
- `experiment_dense.py`: `0bae1a4a3c1dba5e5080cb56187c77f2e701929495770638894ce9d0b572ae5d`
