# Core survival and finite-time enclosed-mass convergence

The repaired solver now completes t=30 through 512 shells. A frozen 5% criterion for two late-time averaged enclosed masses passes spatial, barrier-cutoff and integration-tolerance comparisons. This is a bounded coarse-observable convergence result; individual trajectories and an asymptotic profile are not certified. Separately, CORE_ENERGY_BOUND.md proves a nonzero localized cold-mass bound for the exact closed model and these negative-energy initial data. These statements must not be conflated.

## Final finite-time comparison

The t_eval-only 512-shell rerun completes with maximum absolute energy error 1.46e-8. The final comparison in assess_core_run completes and its manifest validates. The criterion was specified before reading the 512-shell result: each trapezoidal time-averaged cold mass inside radii 3 and 5, over t=20..30, must change by less than 5% relative to the 256-shell reference.

| Test | Mean M(r<3) | Mean M(r<5) | Relative changes from reference |
|---|---:|---:|---:|
|256 shells, epsilon=1e-8, rtol=2e-11|0.423102|0.551219|reference|
|512 shells, same cutoff/tolerance|0.431522|0.549611|1.99%, 0.292%|
|256 shells, epsilon=1e-6|0.417037|0.548701|1.43%, 0.457%|
|256 shells, rtol=2e-10|0.406159|0.538730|4.00%, 2.27%|

All four runs complete, preserve the sampled domain and satisfy the energy checks. This supports a robust finite-time inner concentration in the approximate hard-wall model: approximately 42–43% inside r=3 and 55% inside r=5 in the reference/finer-resolution averages. It does not establish 5% total error, the exact zero-cutoff limit, a permanent bound fraction of 43%, or a steady halo. The robust existence statement about some localized material comes from the separate continuum energy inequality. The original reduced model's cold initial population and gas entropy remain assumptions.

## Extended runs

collapse_core_run uses epsilon=1e-8 and rtol=2e-11 for all three shell counts, retains the original reciprocal Hamiltonian between elastic cutoff events, and saves radii and velocities at each sample. The manifest validates with completed status. Maximum absolute energy errors are respectively 3.30e-9, 4.35e-9 and 2.16e-9. All sampled states remain ordered with q<1. The cutoff remains an approximation to the logarithmic turn, as documented in REFLECTION_COLLAPSE_RESULT.md.

| Shells | M(r<3) at t=30 | M(r<5) at t=30 | Half-mass radius | Gas radius |
|---|---:|---:|---:|---:|
|32|0.32755|0.53208|4.9313|0.7447|
|64|0.34597|0.46429|5.3460|0.9310|
|128|0.38153|0.49381|5.8079|1.1855|

These enclosed masses use linear interpolation of the Lagrangian mass nodes. They are profile diagnostics, not classifications of permanently bound particles. The exact energy theorem instead uses positive quadrature weights, including and then subtracting the fixed central half-cell.

Over t=20..30 the RMS differences between 32/64 and 64/128 shells in M(r<3) are 0.0501 and 0.0859. The corresponding half-mass-radius differences are 0.481 and 0.974. They do not decrease under refinement. M(r<5) differences do decrease, from 0.0706 to 0.0416, but one improved diagnostic cannot certify convergence of the core.

The mean M(r<3) over t=25..30 is 0.3529,0.3593,0.4203. Thus short time averaging does not establish a unique retained profile either. At t=15 the total variation of node velocities grows from 33.7 to 63.6 to 116.5, while the largest adjacent velocity jump stays about 3. This is evidence of unresolved small-scale velocity structure. It is not by itself a proof of a shock, nonexistence of a continuum limit, or a license to add physical viscosity.

An additional 64/128-shell comparison at epsilon=1e-6, rtol=2e-9 reaches t=20 in collapse_core_spatial_run. It varies both numerical controls and is a robustness comparison, not an isolated test of either cutoff or time tolerance.

## Compiled force and retained-output repair

The Python 256-shell runs timed out after 900 seconds, with their last logged event at t=19.0981. Moving the identical force evaluation to collapse_force.cpp allows the 256-shell run to finish t=30. audit_compiled_force_run compares 15 saved states and finds maximum scaled force difference 5.90e-16 against the original Python equations; selected Hamiltonian finite-difference force checks differ by at most 1.24e-5. This is a numerical implementation change, not a new force. The shared library can be rebuilt with `clang++ -O3 -std=c++11 -dynamiclib collapse_force.cpp -o collapse_force.dylib` in this directory; both source and binary are hashed in the run manifests.

The completed compiled 256-shell run has maximum energy error 1.54e-6, M(r<3)=0.39281 and M(r<5)=0.48493 at t=30. Relative to 128 shells, late-window RMS differences fall to 0.0244 and 0.00981 for the two enclosed-mass diagnostics. This improves the coarse profile comparison but does not establish pointwise convergence.

For a declared 5% criterion on trapezoidal time-averaged enclosed masses during t=20..30, the 256-shell reference means are 0.423102 and 0.551219. Changing only the barrier cutoff from 1e-8 to 1e-6 gives 0.417037 and 0.548701, changes of about 1.43% and 0.46%. Changing only rtol from 2e-11 to 2e-10 gives 0.406159 and 0.538730, changes of about 4.00% and 2.27%. Both checks pass that finite-observable criterion. The percentages are separate sensitivity tests, not a certified bound on their combined error.

The first 512-shell run was terminated by SIGKILL after its last logged event at t=8.0338, without its declared result file; the cause of the external kill was not directly observed. Its solver retained an interpolation object for every accepted internal step. The replacement uses t_eval-only output and retains only requested samples and event states, avoiding that growing history. audit_streaming_output_run finds exactly identical sampled and event states through the first 32-shell barrier event, with no persistent interpolant. This verifies the output-retention change in that bounded test. That repair enabled the completed 512-shell rerun summarized above; no result is inferred from the killed run.

## What can already be stated about survival

Gas alone, with its fixed thermal coefficient, has minimum energy -0.3. The initial combined energy is about -0.4033 in the finer discretizations. The missing negative energy must remain in baryon–cold coupling; positive cold internal and kinetic energies cannot supply it after complete dispersal. The explicit finite-radius inequality in CORE_ENERGY_BOUND.md therefore enforces persistent cold localization for any global admissible conservative evolution.

For the exact continuum initial data, the rational series calculation establishes M(r<20)>0.03516 at every admissible time. If an asymptotic escaping/retained decomposition exists, its retained mass exceeds 0.06378. These bounds use no fixed central numerical node. They are lower bounds, not the much larger finite-time masses in the table and not a settled core radius.

The constraint is already encoded in the chosen initial negative energy. It does not prove natural capture from an unbound cosmological state or production of the initially cold material. Allowing gas cooling changes the energy floor and requires a new calculation. Solver conservation tests cannot remove those physical assumptions.
