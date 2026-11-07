# Dynamical phase boundary and selected radius

Base00b8bd7dd535008404c97d49d244466639fdd31b. Replace prescribed R by a
thin phase wall with surface tension Sigma, interior lower vacuum energy by
DeltaV, and a positive heavy-particle mass step outside. Radiation is assumed
transparent. Derive pressure force P_inside+DeltaV-2Sigma/R and its inertial
motion; do not assign phenomenological stabilizing drag. Wall mass/gravity is
small in the specified nonrelativistic scaling. Finite barrier leakage is a
bound, not exactly zero physical escape.

Use the previous source/cooling/conduction fluid model, noting its prescribed
zero-momentum source and unresolved microphysical mapping. Preselect cases:
(gamma,Sigma,DeltaV)=(1,0.6,0.03),(1,0.6,0.05),(8,0.4,0.03).
epsilon^2=(v_scale/c)^2=1e-6; wall inertia=Sigma epsilon^2. Scan R between0.5
and40 for equilibria; do not fit radii, target rotation speed or coefficient.
Track sign changes of wall force on independently solved fluid equilibria.
Then solve a comoving staggered discretization with dynamic R and wall velocity
and compute radial eigenvalues INCLUDING boundary motion and perturbed gravity.
Refine found equilibria at24,48,72 cells (96 if needed). Separate stable/unstable
branches and failed solves. Float64, deterministic, one thread, up to240seconds.
Verify mass budget with moving volumes and wall energy/work identity. Negative
control reverses the wall vacuum pressure sign and must fail equilibrium.
No nonspherical wall stability, unique phase microphysics, radiation transfer,
parameter-fit novelty or universal no-go. Only this investigation changes; push
verified evidence and qualified findings.
