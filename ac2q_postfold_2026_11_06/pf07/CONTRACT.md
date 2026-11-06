# PF07: constraint-adapted evolution and time-dependent interfaces

Base e50f32a0a7. Original scientific objective remains full-action unique
continuation versus necessary extension; bounded numerical success is partial.

Route A: test canonical cancellation as a numerical failure mechanism. Define
S=2 beta_xx+3 beta_x^2, C=2 Mpl^4 exp(4 beta)/p_lambda, and
r=p_beta-C S. Then the Hamiltonian constraint is algebraic in r:
h=(p_lambda^2-2 p_lambda r)/(4 Mpl^2 exp(2lambda+4beta)).
Transform evolution by the exact chain rule, initially without momentum
projection, filtering or viscosity. Test the transformation against the canonical
RHS and its linear benchmark before interpreting longer evolutions.

Fixture unchanged from PF06: Mpl^2=1,K=.5,gamma=.1,s^2=.01,V=.01,a0=.3,
P0=.002/k sin(kx), k=128. Odd grids n=15,31,63,127, dt=.0025,.00125,.000625
and additional smaller steps only to diagnose stability. Targets .1,.5,1,2;
advance only while resolved and constraints controlled. Per run <=120 seconds.
Stop: X<=0,q<=0,cap>=1,1-2gamma D<=0, |p_lambda| tending to zero,
polarization residual>2e-9, relative momentum>1e-7, spectral tail>1e-3.
Report stop as numerical/domain event; a physical endpoint requires refinement.
FRW <1e-8 and Jacobian directional relative error<1e-4 are mandatory controls.
Require convergence at a shared prebreak time before declaring solver fixed.
Original-variable run with identical initial data is the failure control.

Route B: exact regular time-dependent planar interface. At a locally resting
interface with continuous fields and common bounded tangential derivatives,
D=e^-alpha C_lorentz(ell+vT), ell=P_x+2P beta_x,
T=P_t+2P beta_t. Test the full normal partial Legendre transform, all metric
fluxes and scalar flux; determine whether the tangential term is only affine
in v. A verified exclusion is restricted to regular trace/no-defect solutions.

Route C: integrate current and stress balance across a dynamic thin layer.
Derive surface evolution including storage and tangential transport. Distinguish
necessary balance equations from a constitutive law and unique native limit.
No arbitrary stress, regulator, or free layer state can count as a prediction.
Neither lack of a proof nor failed numerics establishes nonuniqueness.
