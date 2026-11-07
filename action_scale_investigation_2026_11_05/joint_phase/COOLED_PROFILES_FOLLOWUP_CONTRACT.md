# Profile refinement and boundary dependence

Followup to the frozen COOLED_PROFILES_CONTRACT and first successful numerical
run. Preserve the executed first script. Reuse the same numerical equations in
a new script, refine gamma8 at48/72/96 cells, and vary imposed radius to2,4 and
injected kinetic energy to6 (baseline R3,ein3), gamma1, source scale1, at48/72.
This tests boundary and heating dependence rather than fitting a MOND number.
Record full steady profiles, eigenvalues, convergence, number budget, and a
volume-integrated stationary kinetic-energy budget with gravitational work.
The primitive staggered thermal/momentum discretization conserves number
exactly but only approximates total energy; measure its refinement error.
Compare edge speed at the actual fixed R using total enclosed mass, not the
last cell center. Keep wall and free-radiation qualifications.180 seconds,
single thread, Float64. No independent microphysical viability or full global
stability proof. Negative cooling control remains in the original script.
