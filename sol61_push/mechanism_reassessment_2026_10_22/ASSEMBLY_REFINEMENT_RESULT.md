# Assembly survives refinement, but spatial and physical-time limits matter

The T400 live cold assembly is insensitive to halving the tested time step at fixed64 shells, and its excitation energy remains similar at256 shells. However, small displacement relative to a discrete equilibrium is not the same as an accurate continuum acceleration profile. The innermost sampled acceleration still has a2.85% deficit at256 shells. A physical-unit conversion also shows that the successful ramp can be very long for galaxy-scale final masses.

## Independent temporal check and larger spatial grid

At64 shells, compare dt=.001 in the new run with dt=.0005 in the previous run, both T400. Excitation energy changes by5.72e-8 relatively. This isolates time-step sensitivity for that observable and trajectory; it does not validate the failed fast ramp.

At256 shells and dt=.0005, excitation energy is1.53004e-5 and final weighted position error is.001583 relative to its discrete equilibrium. Compare1.53454e-5 at64 shells and1.53112e-5 at128. The discrete equilibrium edges are1.68829,1.69333 and1.69687, approaching the continuum value1.70505 slowly. This is convergence evidence, not an extrapolated error certificate.

The new run stores final shell radii, velocities and equilibrium radii. Enclosed mass at a probe radius is reconstructed linearly in r³ within each shell, consistent with its piecewise constant density. Compare total acceleration g_N+m/r² against the continuum gamma=.01 cold equilibrium:

| radius | final relative error,64 shells | final relative error,256 shells | static discrete error,256 shells |
|---|---:|---:|---:|
|.1|-10.01%|-2.850%|-2.856%|
|.3|-.295%|-.0390%|-.0421%|
|.5|-.0564%|-.00238%|-.00516%|
|1|-.0314%|+.0434%|-.000251%|

The central deficit is mainly spatial discretization, whereas residual dynamics contributes appreciably at r1. Four probes do not bound a whole profile. The reference is the continuum finite-mass cold equilibrium, not the algebraic acceleration law or observational data.

## Physical-time conversion

The established units in FINITE_KINETIC_RESULT.md are GM_b=a0=r_M=1, with r_M=sqrt(GM_b/a0). Consequently

    t_unit=sqrt(r_M/a0)=(GM_b/a0³)^(1/4).

Here M_b is the final baryonic mass, since beta reaches1. For the repo's canonical a0=9.3603e-11 m/s², use GM_sun_nominal=1.3271244e20 m³/s² and a Julian year365.25 days. The nominal mass parameter is a conversion constant from [IAU2015 Resolution B3, p.2](https://www.iau.org/common/Uploaded%20files/IAUGA2015-Resolution-B3-recommended-nominal-conversion.pdf), checked2026-10-22; it is not an independently measured galaxy parameter.

| final mass in nominal solar masses | T100 in Gyr | T400 in Gyr |
|---|---:|---:|
|1e8|1.130|4.521|
|1e9|2.010|8.039|
|1e10|3.574|14.296|
|1e11|6.356|25.422|

These are arithmetic conversions of this dimensionless experiment. The Plummer length remains r_M and dimensionless gamma remains.01; this table is not a prediction for a population with one independently fixed physical stiffness or measured sizes. No evolving a0 or cosmological expansion is included. The T400 success therefore cannot simply be called a realistic galaxy-formation timescale. Nor is T400 a proven minimum: only one ramp shape and a few durations were tested. A rate adjusted to the changing response, a different nonzero seed, or a cosmological initial-value problem could differ and requires fresh calculation.

## Evidence

cold_assembly_refinement_run completed and its manifest validates. Four checks pass: force derivative, work balance, shell ordering and fixed-N temporal comparison. Source inputs include the prior v3 result for the comparison. The new contract states the shell conventions explicitly; the earlier v3 contract inherited an irrelevant action-coordinate conventions string from a template, while its actual code, bounds and mathematical input fields identify the shell experiment. That documentation defect is disclosed rather than silently editing its pinned contract.

Physical-unit entries were independently evaluated by direct Python arithmetic using the displayed formula and constants; they are not outputs of the bounded live-run manifest. The interpretation remains conditional assembly from a cold seed, not primordial formation, observational validation or novelty.
