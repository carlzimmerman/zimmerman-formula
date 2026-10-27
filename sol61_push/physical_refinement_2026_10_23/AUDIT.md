# Computation and interpretation audit

Outcome: finite radial evolution and aperture results conditional on float64, spherical symmetry, stated preparation and boundary conditions. No full-action bound-core certificate, selected mass, mass function or observational preservation result.

## Retained failures and corrections

- `base`: original L-BFGS preparation residual 1.66e-4 fails 1e-5. Its different collapse result is not accepted as formation evidence. `radial_v2.py` uses coupled Newton; original code/output remain unchanged.
- `check`: mass and weighted adjoint checks pass; stationary polarization and phase checks pass (phase relative residual 1.37e-8); tangent derivatives agree within 6.61e-7 for P and 3.39e-6 for chi. The original force finite difference at step 1e-8 fails its 1e-5 threshold.
- `check_v3`: force error falls quadratically: 1.10e-2 at 1e-7, 1.10e-4 at 1e-8, 1.04e-6 at 1e-9, and 4.64e-8 at 3e-10. The failed original step was truncation-sensitive. This is one particle at one state, not exhaustive force coverage.
- `check_v2`: supplemental computation failed at JSON serialization of NumPy bool. `check_v3.py` adds scalar serialization; failed files retained. This is an implementation-output failure, not a physics result.
- The homogeneous force check remains **failed** at the original absolute 1e-7 tolerance: polarization canonical acceleration is 5.23e-7. Density residual is 7.66e-15 relative; spatial differentiation and division by eta amplify that roundoff. Material cold acceleration is only 1.31e-9 and baryonic acceleration 7.61e-15.
- `null_evolution`: from z1100 to10 at n256, maximum cold and baryonic contrasts remain 2.83e-14 and 2.86e-14; no crossings, chi=1, final |P|=5.84e-19. This bounds the demonstrated effect of roundoff for this control. Its *relative* work check fails at .03684 because the maximum energy scale is about 4.92e-31. The absolute endpoint work defect is about 1.81e-32. Neither failed threshold is silently relaxed.
- `history4400`: fails during initial evaluation because the converged minimum has |P|=.99319 above the .985 guard. The supplemental initialization audit has residual 3.41e-12 and chi about19.93. Formal potential domain is |P|<1; no claim of fundamental inconsistency follows.
- `large_seed`: process completes with a scientific `reason=field_domain`; endpoint check fails near z494.6 when chi approaches .1. Its final arrays can contain the interrupted trial update while the last diagnostic describes the preceding completed step. `analyze.py` explicitly excludes all non-endpoint final arrays. Do not use this run as a z10 mass profile.
- `cold_control`: absent baryons make the diagnostic baryon contrast NaN through 0/0. Other evolved quantities are finite. Output uses Python's nonstandard JSON NaN spelling; analysis ignores that undefined diagnostic. It is not a physical divergence and the original output is preserved.

## Numerical evidence

For nonzero-seed successful endpoints, work errors are below9e-8. The .03 timestep-halving run gives second-order work improvement and essentially identical peak/aperture mass. Spatial peak convergence succeeds for .03 and fails for .05; deposited fixed physical aperture convergence succeeds for both. A finite aperture can be resolved while its central cusp is unresolved. Sharp shell aperture masses show larger jumps than integrated deposited density and are not used for mass-convergence statements.

There is no independently implemented second full solver. Invariants, the force step scan, null control, timestep and spatial refinement are orthogonal checks within this implementation. The finite tests do not validate the cosmological completion, physical baryon model or chosen initial spectrum.

## Provenance and scope

Each bounded run has `manifest.json`, stdout/stderr and declared outputs where generated. Runner status `completed` is process success, not physical acceptance; inspect result checks/reason. `history4400` and `check_v2` are preserved failed executions. Every manifest is validated separately with current input/output hashes in VALIDATION.txt.

The initial CONTRACT.md records base54ee83e, while later runner manifests observe commit330b0068 with a dirty tree. The shared repository changed during this work; no commit/reset was made here. Per-run pinned script hashes, rather than the initial base label alone, identify executed inputs.

Some inherited JSON contract inputs accidentally say “quiet Gaussian seed.” The executed and hashed code and CONTRACT.md define a deterministic radial sine displacement. This metadata error is acknowledged rather than rewriting old provenance. Later scale/control contracts use the correct description. No random seed or Gaussian ensemble was used.

The radial null test cannot establish late-time small-scale behavior for arbitrary seeds. The finite reflecting domain cannot certify outward cooling or cosmological abundance. No physical baryon pressure, radiation-era transfer, angular momentum, 3D fragmentation, metric/lensing response or fitted galaxies enter these runs. The missing physics is material, not a plotting detail.
