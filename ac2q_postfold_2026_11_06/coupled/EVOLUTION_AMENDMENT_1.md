# Post-result implementation and timestep diagnostic

The original and centered-derivative runs fail earlier at higher spatial
resolution; this is NOT a continuum singularity result. Centering derivative
inputs removes cancellation of large homogeneous backgrounds (FRW error falls
from 5.5e-9 to 9.4e-17), but does not cure the stop. Direct initial-data momentum
constraint time derivative is 4e-15 to 5e-14 on grids 16–64. Frozen long-run
success criteria have not passed.

Next diagnostic, declared before execution: at n=64 use dt=0.00015625 (1/16
of the original) to test sensitivity to the severely conditioned algebraic-lapse
formulation, keeping all equations, data, filters and stopping rules unchanged.
This is outside the original two dt values and carries no retroactive pass.
Compare at matched times; if failure persists, record this formulation as not
yet validated through the nonlinear regime rather than an AC2q failure.
