# PF06b: bounded coupled pre-break evolution attempt

Declared before execution. Use the PF06a exact ADM equations in scalar-clock
time, lambda spatially uniform, beta and both gravitational momenta evolved;
solve Hamiltonian and polarization constraints for lapse N and P at every
stage. Enforce momentum constraint as an independent diagnostic, not a projection.
Exact hold law and constant test V retained. Same dimensionless fixture as
ADM_CONTRACT; choose k=128 initially, Ngrid=32,64 (128 only if discriminating),
time targets 0.1,0.5,1,2. Fixed-step RK4 with dt=0.0025, plus dt/2 at a matched
resolution; spectral derivatives with no filter or viscosity. Stop upon failure
of constraints, X>0, q>0, flux cap, or a resolved prebreak criterion; no claim
that a spectral continuation past steepening is a physical weak solution.

Validate homogeneous constant-V scalar FRW against its exact scalar-time
solution, check analytic constraint Jacobian by directional finite differences,
and check Hamiltonian/polarization residual at every stage. Numerical nonlinear
solve tolerance 2e-9 absolute; momentum drift should converge under space/time
refinement and be reported normalized to gravitational momentum-gradient scale.
Use a 90-second bounded single-thread run initially; timeout is resource
inconclusive, never a physical failure. Preserve failed implementations/runs.
If initial validation fails, diagnose before any scored evolution. A short
regular evolution does not establish global regularity; growing grid-sensitive
gradients do not by themselves prove a continuum singularity.
