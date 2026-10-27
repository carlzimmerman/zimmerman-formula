# Resolution extension: isolated and host dwarf

User authorized on20October2026: push resolution until the inner density profile and host remnant converge; determine whether a flat-density core forms in isolation and whether elastic scattering changes it relative to a collisionless control. This is a bounded extension of the existing full3D finite experiment. The original experiment and its outputs remain immutable.

## Fixed physical model and scenario

Use the same prepared dilute daughter-carrier Boltzmann–Poisson reduction, revised elastic kernel sigma0/m=.3cm²/g,u*=.02,r_lambda=2, and live collisionless stars. No source production, response-field force, target profile, cooling drag, boundaries or particle deletion. Use original total masses, ellipsoid axes, stellar Plummer distribution, subvirial ratio, rotation fraction and axis, and analytic host/orbit from ../isolated_host_dwarf_2026_10_19/CONTRACT.md. This remains a prepared assembly history; source production and cosmological prediction are outside the calculation.

The new resolution family uses nested scrambled Sobol coordinates for quiet sampling of the SAME continuous initial position/velocity distributions. Antithetic points enforce zero bulk motion. Independent streams for cold/stars keep their raw phases nested as N rises; per-level virial/rotation normalization is explicitly recomputed. This changes finite particle realization relative to the original pseudorandom runs. Old and new endpoints are not a pure resolution pair. Every elastic/collisionless and isolated/host pair within one level uses identical relative initial phase space.

## Numerical approach and staged execution

Keep direct full3D high-precision softened pair gravity. An explicitly compiled parallel float64 central-pair backend may replace the serial backend only after independent force/potential/gradient/translation/P/vector-J tests and a bounded runtime benchmark. An optional GPU direct backend using explicitly declared compensated high/low expansions must independently meet a1e-11force/potential relative-error gate against nativefloat64 and integration/conservation controls before production; rawfloat32forces are insufficient. No Barnes–Hut opening approximation, spherical averaging or unchecked fast-math is authorized as a hidden substitute. Limit active numerical workers to8CPUthreads in total and keep low process scheduling priority; no unrelated job is modified.

Use a symmetric fourth-order Hamiltonian composition (three leapfrog substeps) to improve gravitational/orbital integration. Elastic scattering is applied with positive physical time only, outside the Hamiltonian composition. Negative Hamiltonian substeps must never be fed to scattering. Compare step size and document the stochastic splitting order. Keep the old collision operator and its domain/probability rejection guards; no rate clipping or enhanced cross section.

Explore increasing powers-of-two cold counts, starting4096/8192/16384 and extending32768and beyond when needed. Stellar count is one eighth of cold count. Decrease force softening and scattering support jointly; retain separate fixed-N softening/support and timestep controls so mixed refinement is not mislabeled as convergence. Do not infer physical absence from a run that times out, fails or remains below resolution. Freeze each run's exact arguments and code hashes before launching; never edit active run inputs. Individual pilot/production commands and resource caps are recorded by the computation-audit runner.

## Measurements

Record full energy and vector-J conservation with all original particles retained. Separate dwarf-internal and orbital motion and accumulate per-particle host work/torque. Save initial/final phase space plus late-cycle snapshots, allowing profile/boundness diagnostics to be rechecked without rerunning forces. No subgroup energy drift is silently called cooling.

Locate remnant minima using cold density and self-potential, excluding the host potential; use tracked seeds and record competing minima or branch jumps. Compare profiles in this frame. Record cold shell densities, counts, cumulative masses, and total-gravitation multicomponent effective counts. Estimate softened gravitational relaxation as a HEURISTIC resolution screen, not a theorem or a measured physical collision rate. Bound mass is an instantaneous iterative self-unbinding diagnostic; bracket0.5/1/2kpc cuts. Do not call it guaranteed tidal survival.

Measure host endpoint mass AND time-dependent mass through the final complete orbit and windows aligned to the same-numbered pericentre. Treat secular stripping and phase variation separately from independent seed uncertainty. Snapshot scatter is not independent-sample error. Repeat sampling/collision seeds where the signal is comparable to finite realization variation.

## Decisions, defined before high-resolution results

Energy error must stay below0.1%of initial dwarf internal binding in production; target0.03%for timestep controls. Vector-J/P defects must be negligible compared to physical transfers. Passing conservation does not supply profile convergence.

For a resolved radius require r>=2.8epsilon, at least200enclosed cold particles, and heuristic final local gravitational relaxation time>=10Gyr (prefer20Gyr). Record count/relaxation failures rather than filtering them out of plots or convergence coverage.

Convergence requires the finest two successive particle levels to agree to10%in the stated resolved radial density/cumulative range and in host remnant mass measures, with independent timestep and force-softening/support checks. A third level, sampling repeat or a held-parameter refinement must resolve apparent accidental agreement. Report the actual radial interval and numerical uncertainty; extend if criteria fail. Host remnant amplitudes are not declared converged from the same endpoint alone.

Fit the inner density slope gamma=-dlnrho/dlnr using shell count likelihoods over declared intervals; no imposed cored fit may manufacture a plateau. Conditional Poisson intervals are distinct from time/seed/systematic errors. A resolved flat core requires gamma95upper<.3 over at least a factor3in radius, stability under resolution controls, and persistence through late-time windows. A resolved cusp is evidence against a core on that measured interval, not an exclusion of every unresolved smaller radius. Allow INCONCLUSIVE if these requirements cannot be met.

Elastic effects require matched collisionless controls at the highest converged resolutions. Compare slopes, core radius if resolved, density/mass and spin/energy transport against numerical and sampling spread; quote upper bounds or inconclusiveness when no significant difference is resolved. Do not equate a small difference in M300 with identical inner profiles.
