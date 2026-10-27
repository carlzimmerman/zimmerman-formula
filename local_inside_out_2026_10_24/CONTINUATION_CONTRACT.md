# LIO-3: follow the protected branch to a free exterior

The ten LIO-2 local-front trajectories all lose the interior. Test whether
this merely reflects the initial front's basin. Introduce tau multiplying
the exact exterior capacitance term; tau0 is the old no-flux protected
state, tau1 is the actual freely relaxing exterior. Tau is a diagnostic
boundary homotopy, not a tunable physical parameter or a scheduled pump.

Start x=1 at tau0 and follow local minima at tau=10^(-6)..1 (61 logarithmic
values). Beta20, f.95, profiles1 and2, ell30 kpc, n128. Use the exact parent
energy/gradient and L-BFGS-B in mass-metric scaled phase coordinates,
0<=x<=1. Report stationarity via full generalized phase speed and lowest
Hessian eigenvalue at selected/end steps. A constrained minimum at an
endpoint requires the derivative signs to be checked. Do not treat optimizer
success alone as mathematical stability or branch completeness.

Also evaluate a sufficient exclusion test: for 0<=x_i<=1,
x.grad E >= x^T[L+Ltail-2 beta diag(C F(u0) vol)]x.
Here hp>=0, mu>=0, F(u)<=F(u0), and |sp(x)|<=2x. Positive definiteness of
the matrix excludes every nonzero stationary phase in this fixed-density
box. It is only sufficient; a negative eigenvalue is inconclusive.

Numerical declaration: n64/128/256 for exclusion eigenvalues; continuation
n128, tau grid as above. Repeat a transition bracket if the branch changes
materially. No temporal evolution or formation prediction follows from tau.
