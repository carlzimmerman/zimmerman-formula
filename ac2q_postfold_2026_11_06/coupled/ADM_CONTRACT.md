# PF06a: full planar ADM constraints and valid initial data

Before new numerical values. Full plane metric
 ds^2=-N^2 dt^2+exp(2lambda)(dx+w dt)^2+exp(2beta)(dy^2+dz^2).
Fix only scalar time phi=s*t, s>0. Kx=(lambda_t-w lambda_x-w_x)/N,
Ky=(beta_t-w beta_x)/N. Derive the action, canonical momenta, lapse,
polarization and momentum constraints; preserve all constraints before any
spatial gauge choice. No coupled simulation may claim validity without them.

Construct an exact family of initial data at lambda=beta=0, phi=s*t,
P=(A/k)sin(kx), D=A cos(kx), p_lambda constant. Solve the nonlinear
polarization constraint for positive N; set p_beta from the Hamiltonian
constraint. Momentum constraint then vanishes identically. W is AC2q's exact
log hold law with |K P|<a0; V is an explicitly chosen constant test potential.
Use dimensionless stress fixture Mpl^2=1, K=1/2, gamma=0.1, s^2=0.01,
V=0.01, a0=0.3, A=0.002, k=16,32,64,128. These do not grade physical footings
or fix their parameters. N(theta=0)=1. Integrate the lapse ODE in z=cos(theta)
and reconstruct its periodic branch. Compare two solver tolerances and check
residuals using independent finite differences at grids 256,512,1024,2048.
Residuals must decrease on refinement; report them, do not assert exactness
from floating outputs. Check X>0, q>0, flux-cap margin, momentum and Hamiltonian
constraints. Benchmarks: A=0 gives homogeneous scalar FRW, gamma=0 removes
stiffness. Incorrect sign of the pressure derivative must spoil the residual.

This supplies initial data and an evolution formulation, not an evolved
full-action shock. Any time integration requires a further declared run with
constraint diagnostics, convergence, and a prebreak stop rule. Keep separate
from existing source-free tests. No empirical claim.
