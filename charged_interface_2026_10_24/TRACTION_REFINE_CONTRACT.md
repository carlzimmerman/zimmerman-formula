# CI-10: refine positive-pressure cell, without assuming success

The CI-9 k120,tau1 cell passes the necessary kinetic-stress bound and
isotropic pressure check at n256, while preserving inner law and free outer
phase. Refine to n512, decrease delta from 1e-5 to 1e-6, then n1024.
Repeat plus/minus .2 kpc displacements at the last resolution. All phase
variables free. Report both species, Hessian, stationarity and force errors.
No positivity-of-distribution-function, dynamical formation or continuum
stability claim follows from necessary pressure and finite Hessian tests.
Resource cap 240s; incomplete iterations mean inconclusive, not failure.
