# Frozen bounded validation

Main_a: 64 exact checks pass, including 495 retained Cartesian monomial comparisons for N=0,...,8. Control_degree_a: 46 pass and 18 intended failures (retained moments and first nonzero coefficient). Control_flux_a: 46 pass and 18 intended failures (positive flux and nonzero evolution). Each control exits 1; failure logs/results are preserved. All three standard-runner manifests validated against current input and result hashes. No report is an execution input.

The symbolic checks corroborate the finite implementation; the universal-N argument is the analytic Rodrigues integration-by-parts proof in REPORT.md. No quadrature or astronomical analysis was performed.

Regularity reconciliation: REPORT now explicitly restricts the initial-data class to smooth velocity interiors with a C³ escape cutoff. REPORT was not an execution input; script, contracts, results and run hashes are unchanged. No C-infinity distribution theorem is claimed.
