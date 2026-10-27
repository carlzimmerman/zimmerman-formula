# CI-7: tension candidate refinement and matter forces

Polish CI-6 beta1000 k100 tau.1 at n128, interpolate to n256 and n512,
then change regularization from 1e-5 to 1e-6. All phase variables remain free.
Report full Hessian, stationarity, inner and outer fractions, force residual
and both species' zero-outer-pressure isotropic Jeans necessary pressures.
The species potentials include all mass and phase derivatives, including
the polarization-charge mass dependence. Negative pressure excludes this
isotropic closure, not every anisotropic stress or live density rearrangement.
This tests the most promising single-wall cell; not the whole parameter space.
