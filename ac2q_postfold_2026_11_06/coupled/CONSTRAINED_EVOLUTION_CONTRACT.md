# PF06c: eliminate the independently drifting momentum-constraint sector

Declared after the original evolution fails space convergence; no old verdict
is upgraded. Fresh review independently confirmed the canonical continuum
formulas but identified severe Q^4 cancellations in scalar-time variables,
missing momentum/gauge stops, and an even-grid Nyquist null mode. Odd grids
alone did not fix the failure; centering constants and dt/16 did not either.

Diagnostic: on odd grids 31,63,127 reconstruct p_lambda at each RK stage from
p_lambda,x=beta_x p_beta, retaining the independently evolved mean p_lambda.
The zero-mode compatibility integral must be monitored; never silently discard
a significant nonzero mean. This is solving an existing constraint, not adding
viscosity or a new action. Reconstruct after each complete step as well. Other
Hamiltonian/polarization constraints remain solved as before; fix missing
stops for momentum/gauge residual and denominator 1-2gamma D. No filter.

Use k=128, dt=0.0025 and dt/2 matched grids, target t=.5 then1 then2 only if
resolution/constraint checks justify extending. Compare against the original
at t=.1 and the independent homogeneous/linear benchmarks. Keep spectral-tail
stopping at 1e-3, explicitly label it underresolution; do not continue as a
post-shock solver. Momentum normalized residual <=1e-8; gauge residual <=1e-8
relative to max|rate|; compatibility mean <=1e-8 times max(1,|beta_x p_beta|).
Compare fields and derivative growth over grids, not termination labels alone.
A favorable finite interval establishes no global regularity or weak-solution
uniqueness. A failing numerical formulation establishes no AC2q physical failure.
