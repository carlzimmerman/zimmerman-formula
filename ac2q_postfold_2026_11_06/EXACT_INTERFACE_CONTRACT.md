# PF02: exact planar stationary interface, declared after PF01

PF01 found a cubic mismatch between the positive-charge potential-flow and
momentum jump conditions. Next discriminator: does keeping the relativistic
clock and canonical X terms remove it? No parameter fitting or adoption.

Scope: local flat 1+1 planar stationary interface in its rest frame, timelike
scalar phi=s t+psi(x), s>0, n=(cosh theta,sinh theta), v=tanh theta=-psi'/s,
P^mu=P(sinh theta,cosh theta). Positive switched charge on both sides; P and
phi continuous, bounded one-sided derivatives, finite W; no added surface
stress/charge or unresolved oscillatory defect. Potential V and W coefficients
are continuous and thus do not supply a delta jump. Metric/tangential
variation across the layer must be bounded for this reduction to apply.

Compute D.P and P.A directly. Integrate the acceleration term by parts for
continuous P. Derive necessary variational corner conditions: continuity of
L_{P'}, L_{psi'}, and the spatial Hamiltonian. Try to exclude a finite shock
with same-sign nonzero relative velocities. Retain full dependence on v and
on epsilon=gamma*s^2; test 0<=epsilon<1/3. Opposite-sign velocities, surface
defects, switch crossings, nonplanar/multidimensional solutions, and global
Cauchy uniqueness are excluded. Source-free smooth breaking in PF01 does not
prove that this exact full theory forms the tested discontinuity.

Symbolic identities must vanish exactly. Test derivative convexity analytically,
then finite fixtures epsilon=0,1e-17,0.01,0.1,0.3 and A=1.01,1.2,2, with v in
(0,sqrt(1-1/A^2)); only fixtures with a pair of same-current roots count.
Report failures to construct a pair as such. Finite fixtures are corroboration,
not the proof. Negative control: reverse the derived jump defect and require
its sign check to fail. Record provenance and do a separate self-audit.
