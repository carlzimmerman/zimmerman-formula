# Full coupled planar cap-collapse test

Base2c69526e6b0e3b422ce81ff73f55e5859a30abf8; action b6790b6569.
User requests an inhomogeneous test of the full coupled action, including
whether the cap shifts the singularity. Owner: this chat. No action adoption.
Kappa=1/2 FITTED. Preserve failures and distinguish numerical from physical loss.

Use the exact plane-symmetric reduction with two equal transverse scale
factors, clock-adapted time tau=t, lapse N(t,x), shift w(t,x), spatial metric
h=diag(exp(2A),exp(2B),exp(2B)), scalar phi(t,x), physical longitudinal
polarization P(t,x), and cap auxiliary lambda(t,x). Retain all those equations
before choosing zero shift. No PN approximation or frozen metric/scalar.
The external S_m sector is set to zero; the canonical rolling scalar remains.
This is an invariant symmetry sector of the proposed action, not the general3D
problem and not the old tilted-clock-on-fixed-FRW example.

Domain: x periodic in[0,2pi], reflection-even metric/scalar/canonical momenta,
reflection-odd P. Constants Mpl=1,K=1/2,G=1/(8pi),beta=2/3,kappa=.5,
xi=.5/(1+beta),Vstar=.01*sinh(1),Lstar=1,gamma=K Lstar^2/2,
cap b=.1,T=1 and the previously defined Theta_star(phi).
Initial A=B=0,phi=1,pi_A=.35,pi_B=.7+.15cos(x),P=0,N=1.
Solve the scalar momentum from the full Hamiltonian constraint, choosing its
positive root; if it is not real, reject the initial-data fixture. Momentum
constraint must vanish. Compare with b=0 (cap removed, not sign-reversed),
using the same freely specified fields/momenta and recomputing pi_phi. Initial
physical expansions need not agree because the two constraint theories differ.

Derive the full reduced Hamiltonian, auxiliary constraints and equations.
In zero shift, solve polarization and lapse constraints at every RHS evaluation;
normalize mean(N)=1. Preserve the residual global Hamiltonian constraint as a
monitored conserved quantity, not by resetting the scalar energy. Do not clip
P, cap gap, lapse or scalar domain to continue an invalid branch.

Numerical design: reflection-symmetric Fourier/Galerkin collocation with odd
node counts17,33,65 (no Nyquist derivative kernel). Use the discrete variational
Hamiltonian for evolution, with automatic derivatives independently checked by
finite differences. Constrained auxiliary Newton steps must stay in|K P|<a;
report loss of convergence separately from branch/domain failure. Monitor
local Hamiltonian and momentum residuals, auxiliary stationarity, lapse sign
and range, Q=1/N, cap gap, lambda, scalar domain, volume, shear, spatial curvature,
polarization saturation, and1+gamma*D.P. Track integrated proper time.

First implement/check at17 nodes; graded runs use33 and65, each DOP853 with
rtol1e-7/atol1e-9, then a33-node time control rtol1e-9/atol1e-11.
Target coordinate time3 unless a stated failure prevents continuation.
No success label unless constraint residuals<=1e-3 normalized, time-control
observable agreement<=1e-3 and spatial observable agreement<=.02 on their
common interval. Report every failure location and last valid interval.
Time-control and grid comparison are required before interpreting a singularity.
One BLAS/Torch thread. Each pilot/test job<=120seconds; each graded evolution
<=300seconds, with durable output and partial progress if capped. No concurrent
heavy-job queue or unbounded simulation. Freeze any expansion before running it.

Known checks: exact homogeneous Hamiltonian constraint matches the prior cap
formula; b=0 recovers GR/canonical scalar; P=0 fixes spatially constant lapse;
Hamiltonian derivatives match finite differences; initial full constraints pass;
constant state gives homogeneous evolution; cap/lapse/polarization identities
match their independently varied Lagrangian equations. No numerical smoothing
or changing tolerances after seeing a failure without a separate record.
