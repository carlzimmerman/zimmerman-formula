# PF06d: joint lapse/polarization diagnostic

Motivation: the algebraic-lapse Newton method can reject an RK stage because
its previous-stage P makes X negative before solving the stage constraints.
Such a rejection does not show the stage has no physical constraint solution.
Solve the same Hamiltonian and polarization equations jointly in log(N), P.
Retain momentum reconstruction, branch guards, and no viscosity/filter.
This is a numerical diagnostic, not an added field or changed physical action.

Bounds: odd n=31,63; k=128; dt=.0025,.00125,.0001; t<=.5.
Use analytic block Jacobian; line search keeps final X>0, q>0, cap<1.
Accept only max Hamiltonian residual <=1e-10 and polarization <=2e-9.
Inspect spectral tail at every full step, stop at 1e-3; report constraint
failures separately. FRW and finite-difference Jacobian validation required.
Failure to converge or grid-sensitive failure is not a physical singularity.

Exploratory predecessor /tmp/ac2q_trial.py used the previous reconstruction
solver at n31, dt=.0001,.000025, stopping respectively at t=.060,.0525
for excessive spectral tail. These were unregistered diagnostics and are not
load-bearing evidence; the command is retained in exploratory_trial.py.
