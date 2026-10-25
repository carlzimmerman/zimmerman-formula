# Self-review and retained failures

This is self-review, not an independent referee audit.

Checked: physical units; SFH fractions increasing toward younger lookback ages; their normalization; exact reproduction of the three relevant archived SFH M/L values; no field-TMass/global-mass confusion; no number-fraction/mass-fraction substitution; no cold Xi charge; matched Plummer Newtonian analytic benchmark and direct radial integration; 256/512-node baseline and cold-kernel convergence; fitted moment residuals; continuum dual bound below finite-grid witness; doubled-grid witness approaching that bound.

Analytic shell check: K_i=G a_i^2/[3(r^2+a_i^2)^(3/2)]. The derivative of K_MP-c K_MR vanishes for positive r only when (r^2+a_MP^2)/(r^2+a_MR^2)=(a_MP^2/(c a_MR^2))^(2/5). Endpoints and this stationary radius exhaust extrema. The numerical c search only strengthens an inequality that holds for any tested c; global optimizer accuracy is not necessary for validity.

Important implementation correction: the first shell-grid minimum was initially described in a draft comment as a continuum lower relaxation. Restricting support to a grid actually gives an upper witness for the continuum mass minimization. Before reporting results we added the analytic continuum dual inequality and relabeled both outputs. For one example, dual lower bound=519.432 million Msun; grid witnesses=520.207 million and 519.573 million on coarse/fine grids.

A subsequent code extension reused the scalar a in the four-dwarf control loop before an orthogonal benchmark, causing that check to fail (AssertionError). No results were accepted from that failed invocation. The loop variable is now ac; the final full run passes. Earlier successful outputs were overwritten only after all checks passed.

Limits: fixed central catalogue luminosity/distance/radii; finite metallicity and sigma corners, no joint posterior; global extrapolation of field SFHs; untruncated tracer tails; assumed isolated stationary spheres; imposed selective coupling and primordial abundance ratio; no radial Jeans likelihood, actual cold supply, spin evolution, feedback efficiency, live heating or tidal survival. Positive-shell witnesses need not be equilibria of the cold field. Common physical size/capture is an additional tested null, not a prediction. No broad observational exclusion, novelty claim, or full mechanism completion is justified.
