# CCT-005: observed stellar populations constrain cold supply

Authorized question: can data-constrained assembly produce Draco/Sextans cores without excessive stellar gravity in Fornax/Leo I or stellar disturbance?

Finite assertion tested: under the explicitly postulated spherical two-potential action in ../continuous_cold_envelope_2026_10_24/COUPLING_BRIDGE.md, evaluate full Plummer tracer virial moments using the archived LVD observations and SFH-weighted E-MILES stellar masses. Fit a nonnegative Plummer cold profile to both Sextans population moments where possible. Report supply requirements, rather than treating 53.64 times present stellar mass as an observation.

All quantities are physical pc, km/s and solar masses; G=0.00430091 pc (km/s)^2/Msun. Both previously specified a0 footings are kept. Stellar gravity is rational-law baryonic gravity plus Newtonian cold gravity exactly once. This is a new selective-coupling candidate, not a test of v3s or SCT-M.

Inputs: local Pace LVD snapshot; Weisz 2014 table5 cumulative formed-mass fractions (per-field SFHs); E-MILES Kroupa/Padova SSP table. The field SFH shape is provisionally assigned to the global luminosity; field TMass is never interpreted as a global mass. Metallicity and Sextans old-burst choices are sensitivities, not a posterior. Sextans Tolstoy et al. 2025 two-population values are explicitly transcribed with source and number-fraction caveat. The spherical radius conversion is a tested convention, not a measured spherical population shape.

Primary summaries use catalogue spherical radii and central observed values. Sextans population tests use quoted elliptical radii at catalogue distance, and a separate sqrt(1-e) circularization sensitivity. Unknown mass fraction of the two stellar populations is scanned at 0.1,0.3,0.5,0.7,0.9, not equated to their number fraction. Population sigma endpoints are a finite corner sensitivity, not joint confidence limits. Grid is not a full Jeans/selection/binary/anisotropy inference.

Numerical checks: recover Newtonian matched-Plummer sigma^2=pi G M/(32a), compare quadrature orders, reproduce existing SFH M/L, verify fitted moments. Below 1 GB, one numerical thread. Command: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_data_constraints_2026_10_24/constrain.py

Recorded extension during implementation: remove the Plummer cold-profile restriction using a positive spherical shell measure. Derive a continuum dual mass bound analytically; use a finite shell LP as an upper witness for the optimal mass, not as a rigorous continuum lower bound. Test the explicitly additional common-physical-size/common-capture-per-formed-stellar-mass null against the other three galaxies. Neither assumption follows from a universal action. No observed-data thresholds are retuned.

Outcome interpretation: mass/profile feasibility is only a necessary stationary constraint. No observed SFH uniquely fixes initial gas, cold capture, angular momentum, orbital history, feedback timing, or heating. Passing moment fits cannot establish core formation or survival. Failure excludes only the stated finite profile/data assumptions. No live simulation, frozen criteria or publications are changed.
