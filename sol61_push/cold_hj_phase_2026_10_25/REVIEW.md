# Independent read-only review

A separate reviewer inspected both new solvers, conservation_v2.py, the energy/spin derivation and actual source pins. Verdict: no blocker to archiving failed/limited numerical experiments; computationally verified only in recorded finite ranges, audited rather than independently re-executed.

The review confirmed lens factors/signs, compensated HJ phase signs, distinction between phase-fitted approximation and exact discrete covariance, action/energy/stress signs, Fisher tag-interface correction and once-counted gravitational cross energy. Its exact endpoint table is reflected in RESULT.md: Fornax is .653% and Leo2.445%, while D/S range3.163–4.484%. Not all galaxies have3–4.5% drift.

Minor limits are explicit: diagnostics sample every five steps; recorded bond residuals are asserted in the summary audit (not producer loop); exact discrete rephasing proves no resolution improvement. No late stellar, retained-mass, outgoing receiver or no-overboost inference is accepted. A subsequent author-side boundary check added BOUNDARY_LIMIT.md: lens gravitational boundary work is not separated from raw energy drift, even at negligible material boundary mass. This further limits lens interpretation without changing any frozen producer or result.
