# Harmonic refinement supports a conditional weak-damping estimate

Doubling retained orbital harmonics from16 to32 greatly improves the full-matrix moment check while barely changing the selected mode's weak-decay diagnostic. Recomputing the absorptive matrix at neighboring frequencies shifts the local estimate by about1.6%. Across8/12/16 field shapes, a local Taylor continuation suggests a candidate frequency near .822797 and decay parameter near6.8e-5.

This remains a conditional weak-damping approximation to the continuum boundary response, not a directly solved analytically continued pole or a demonstrated formation timescale. If valid, it implies slow decay, about1930 periods per amplitude e-fold, rather than rapid settling.

## Harmonic check

Keep sixteen field shapes and the64x64 action grid. Recompute32 Fourier harmonics on every orbit, retaining the1024/2048 phase-mesh comparison. The first sixteen coefficients reproduce the prior data exactly. The full sixteen-shape high-frequency moment error decreases from .00676088 relatively to8.6343e-7: from .676% to .0000863%. This strong improvement identifies omitted harmonics as the dominant source of that earlier matrix deficit in this test.

The corresponding real-axis fixed-absorption-matrix indicator changes by only2.82e-5 relatively for sixteen shapes, or .00282%. This demonstrates why the full-matrix error and selected-mode error must be tested separately. The32-harmonic calculation was performed at action order64; a new128-order/32-harmonic combination was not run here. The earlier64/128 checks used sixteen harmonics.

Direct resonance searches at omega=.822,.8228,.8236 find no new represented roots in harmonics17–32. The new absorptive matrix is nevertheless recomputed, including the lower harmonics, rather than assumed identical. The finite-domain and PCHIP-bracketing completeness limitations from RESONANT_CURVES_RESULT.md remain.

## Frequency-dependent complex response

Previously B=-Im Pi was held at .8228 while differentiating the real matrix. Now compute B directly on resonant curves at each of the three frequencies and combine it with the matching principal-value real matrix. Follow the isolated near-zero complex generalized eigenvalue lambda(omega) of D x=lambda S x.

At sixteen shapes, the three boundary eigenvalues are approximately

    lambda(.8220)=-.00359848 + i .000317825,
    lambda(.8228)= .000012254 + i .000305898,
    lambda(.8236)= .00360689 + i .000294481.

The centered complex slope is about4.50336-i .01459. The next eigenvalue magnitude is at least .821 in this small sampled frequency interval, supporting local isolation of this branch within the retained basis; it is not a proof of global analytic isolation.

Form the local linear extrapolation

    z_linear=omega0-lambda(omega0)/lambda'(omega0),

and compare it with the nearby root of a quadratic interpolant through the same three complex boundary values. This uses a local continuation assumption. Matching a few boundary values is not itself proof that the actual Landau continuation has the predicted pole, especially with compact support, numerical interpolation and potential branch structure.

| field shapes | Re z, quadratic estimate | -Im z, quadratic estimate | conditional periods/e-fold |
|---|---:|---:|---:|
|8|.822796509|6.79511e-5|1927.15|
|12|.822797276|6.77394e-5|1933.18|
|16|.822797486|6.79334e-5|1927.66|

Linear/quadratic imaginary estimates differ by less than .0025% in this test. That is a local consistency check, not a full error bound: both approximations use the same three points. The frequency-dependent result differs from the fixed-B sixteen-shape indicator by about1.6%. The basis spread remains about .3%.

## Interpretation

The existing kinetic model supplies a plausible weak energy-transfer route through resonant orbits, dominated by the third harmonic, while the collective mode's complex shape limits its coupling. No arbitrary friction term or extra energy sink was introduced. The current convergence checks make this a more credible perturbative mechanism candidate than a mass-weighted resonance count or broadened peak fit.

Even if the local estimate is validated as a true decay rate, its conditional timescale is long: roughly1930 oscillation periods per amplitude e-fold. This does not demonstrate rapid halo formation or solve initial occupation selection. Collisionless phase-space constraints, the distinction between this identified-medium model and the independent-field action, the fitted value of kappa and the incomplete parent theory remain unchanged.

A direct causal initial-value calculation or controlled continuation, plus checks of frequency-step sensitivity and other backgrounds/occupations, would strengthen the physical interpretation. Novelty has not been established; the general resonant absorption mechanism is not presented as a new discovery.

## Evidence

Direct32-harmonic action data, principal-value results and three direct resonance calculations are preserved. harmonic32_run audits their pinned artifacts, verifies the nested coefficients and absence of new represented high-harmonic roots, and recomputes the frequency-dependent local diagnostic. Nine checks pass and the manifest validates. Original direct calculations are not represented as bounded executions inside that artifact audit. Interpretation is self-reviewed.
