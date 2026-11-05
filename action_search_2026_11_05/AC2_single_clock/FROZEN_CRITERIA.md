# AC2: single canonical clock, smooth polarization stiffness

New candidate, not adoption or inherited v3s PASS. Owner authorized continued
action calculations. Motivated by AC1's exact independent-clock caustic branch.
Kappa=1/2 FITTED. No cold component added. Base includes 3fe720ef92 and AC1.

Candidate: signature(-+++), X=-grad(phi)²/2>0, n=-grad(phi)/sqrt(2X),
A_mu=n.nabla n_mu, spatial projector h, intrinsic derivative D, n.P=0.
S=integral sqrt(-g)[Mpl² R/2+X-V(phi)+P.A-W(p,a)
                  -gamma/2*(D.P)²+lambda*n.P]+S_b[g].
K=4piG, p=K|P|, W=a²/K[-p/a-log(1-p/a)], a²=xi G V,
gamma=K Lstar²/2, xi=2*kappa²/(1+beta).
No independent tau and no additional mu_K norm penalty. Smooth unswitched
stiffness replaces max(D.P,0)²; this changes negative-divergence statics and
cannot inherit v3s's observational passes. n is defined by phi, not varied
as an independent vector. phi kinetic term is canonical, not cuscuton.

First discriminator: scalar-dominated flat FRW, rolling phi, P=0; positive
potential with a constant-epsilon background (the late exponential limit of
AZ40 is a concrete example). epsilon=-Hdot/H²=phidot²/(2 Mpl² H²)>0.
No dust perturbations are retained in this first calculation. Unitary gauge
phi=phi_bar(t), lapse 1+alpha, shift gradient beta_shift, h_ij=a_FRW² exp(2zeta)delta_ij.
Retain lapse/shift constraints, integrate the longitudinal P constraint.
Derive cY(k)=1/[1+Lstar²*k_phys²/2] and its positive lapse-gradient term.
Derive the curvature-mode quadratic action, integrating zeta*zetadot with
the time-dependent a_FRW/H coefficient; do not infer its sign before this step.
Check independently by variation of the shift and then eliminating lapse.

Expected checks, not assumptions: K_zeta>0, gradient coefficient positive,
0<instantaneous phase speed<=1 and 0<group speed<=phase speed, if derived.
This is a frozen-background frequency diagnostic; expansion friction and
nonlinear evolution are not replaced by it. Tensor trace-free quadratic mode
has no linear lapse acceleration or P source; justify only its leading FRW
light-cone statement. Do not claim a full nonlinear DOF count solely from
absence of lapse/P time derivatives in this gauge.

Known answer: switch off P.A coupling to recover canonical single-field FRW
curvature kinetic and gradient coefficients. Lstar->0 has unscreened response;
k_phys->0 has cY->1. Fourier P elimination must agree with direct completing
the square. Negative control reverse the induced lapse-gradient term and
require loss of kinetic positivity on at least one declared fixture.

Fixtures epsilon=.05,.5,1; H Lstar/sqrt(2)=1e-8,1e-4,1;
k_phys/H=.01,1,1e4,1e8: 48 combinations. Compare formulas and independent
mpmath differentiation of omega(k) at 40/80 digits, normalized <1e-25.
No empirical input or kappa measurement. Positive linear checks mean only
this one-clock, scalar-only, homogeneous smooth-stiffness quadratic sector
survives. Open obligations: dust/matter modes, sourced inhomogeneous backgrounds,
X>0 preservation, full constraints and boundary conditions, strong coupling,
nonlinear caustics, observational force/PPN/lensing tests and density-tie history.
