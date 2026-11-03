# AZ5 — time-dependent tracer dynamics instead of an equilibrium selector

κ = ½ FITTED; not theory closed

Pre-result. Record: ls IN1/IN2, RF2, UX4, X20; git log IC1613/disequilibrium; rg snapshot/time derivative/non-stationary/Jeans in those lanes. Inclination and hosted-dwarf heating have been tried. Distinct question: can an arbitrary time-derivative term be identified from the existing snapshot at all? On-disk IC1613 source is _external_data/ic1613_muse2024/src/ic1613_accepted.tex. No data are fetched and no inclination is refitted. CZ1 is concurrently investigating the host-field convention; do not duplicate it.

Use the exact 1D collisionless equation f_t+v f_x-omega² x f_v=0. At t=0 take f proportional to exp[-(x²+v²)/2] in synthetic dimensionless units. This same snapshot is admissible for every positive omega, but f_t=(1-omega²)xv f. Hence d<nv>/dt=(1-omega²)xn: a measured snapshot of density, mean velocity and dispersion alone cannot determine omega unless stationarity or a history is supplied. This is a structural identifiability test, not a fit to IC1613 or the MW.

Known answers: omega=1 is stationary, f_t=0. omega=2: direct velocity quadrature of v f_t equals -3 x n at x=1 to absolute 1e-10; n and velocity second moment both match Gaussian closed forms to 1e-10. MUTATE flip the force sign in f_t while holding the attractive-force moment oracle; error must exceed 1e-2. Both footing labels carry the same dimensionless identity; no a0 is estimated. Output results.json predeclared, finite bounds x=1 and omega=1,2, velocity integral over R.

PASS only for the non-identifiability identity and its controls. P5 closure label NO VERDICT: neither a rescue nor a refutation of time dependence. Every arbitrary time-derivative function, initial condition, age and feedback coefficient used to fit a real galaxy must count as fitted. No new empirical row earns credit. Next calculation must specify a causal evolution and independent initial/history data before predicting the time derivative; setting it equal to the observed residual is prohibited as a pass by construction.
