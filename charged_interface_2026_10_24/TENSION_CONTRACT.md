# CI-6: area tension with polarization-dependent charge

The independent new surface term is tau J, J=integral r^2 |dq|. Charge
capacity remains I=integral r^2 F(u)|dq|. Both vanish in homogeneous phases.
Energy is E_parent + tau J + k/I. This tests whether penalizing area
independently of polarization prevents the fragmented storage in CI-4.
It does not assume conserved T mass, fix a front radius, or pin the exterior.

Finite test: large disk, n=128, beta=20,1000, k=10,100,1000,
tau=.1,1,10, initial front .5R, regularizer 1e-5. Eigh and gradient
checks, independent T and F mass variations. Candidate requires qinner>=.95,
qouter<=.05, interior force error<=.05, one crossing, positive Hessian
and metric speed<=1e-8 before refinement. Passing these is not a live matter
equilibrium, formation result, data fit, or microscopic derivation.

In a sharp spherical wall with fixed unit contrast and total profile held,
E(R)=E_parent(R)+tau R^2+k/I(R). Thus force is
-E_parent'(R)-2tau R+k I'(R)/I(R)^2 and stiffness is
E_parent''+2tau+k[2 I'^2/I^3-I''/I^2]. These are conditional wall-coordinate
formulas; the field test must also admit amplitude and multiple-wall modes.
