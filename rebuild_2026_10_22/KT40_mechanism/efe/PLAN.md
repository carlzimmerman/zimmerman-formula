# KT40: constant-external-field scalar virial diagnostic

Fixed model: KT39 p=9/8, ell=3 kpc, original two a0 footings. Keep all
original dwarf Plummer profiles, mass-to-light samples and object cuts.
Test Draco, Sculptor, Leo II and Fornax at auxiliary Newtonian external
accelerations e/a0=[0,.1,.3,1,3], 41 Upsilon values in [1,3]. This is a
controlled external-field response experiment, not actual satellite fields.

Compute the trace virial from the exact energy variation under centered,
fixed-mass Plummer homology at fixed external gradient. Retain all A and B
terms. Subtract constant-background and linear energy tangents. Compare the
zero-external result with the accepted KT39 isolated full-force integral;
check the homology derivative against independently evaluated high-precision
energy differences, exact Newtonian mutation, and radial/angular/domain
refinement. No physical field floor is introduced.

Three quadrature configurations: (800r,32mu,domain1), (1600r,64mu,domain1),
(2400r,96mu,domain2); rmin=1e-6a, rmax=domain*(200a+40ell). Required dispersion
agreement .02 km/s, zero-external agreement .02 km/s, finite energies and
variances, and relative compact-domain energy-variation error<1e-5.
Negative variances, if present, are physical diagnostic failures, not clipped
into observational passes. Newton control must match pi GM/(32a) exactly.

The trace virial fixes the mean of the three global velocity variances, not
an arbitrary line-of-sight dispersion in an anisotropic external field.
The unchanged 2sigma object cut applied to its square root is therefore only
an orientation-averaged screen. No equilibrium existence, tidal background,
actual orbit, tensor virial, or continuous-external-field exclusion follows.

Owner: mechanism_dwarf_efe. Historical sources remain frozen. Bounded runs,
input hashes and failures will be preserved. First discriminating question:
can this Hessian response's external field raise its isolated scalar virial,
and can any of the declared external-field samples lift the named deficits?
