# FT-I4R: resolve an entire transport trajectory at doubled resolution

The implicit alpha1,iota.1, f.95 run now completes 12 dynamical times.
Its sampled peak T fraction is .28974; it does not meet the .95 formation
target. Repeat its exact initial continuous profile and parameters at n12,
nq512, rtol2e-8 with the same Radau method and duration. Maximum wall time
240 seconds. Parent n6,nq256,rtol2e-7 is run_stiff/results.json.

Require energy drift<1e-4 and relative J error<1e-9. Compare peak q within
.05 and final-window minimum q within .02; record a failed comparison
rather than claiming converged detailed trajectories. The changing shell
discretization also changes the numerical radial boundary. A domain exit
would therefore need a matched physical-boundary test before comparison.
No infinite-resolution, asymptotic retention or observational claim follows.
