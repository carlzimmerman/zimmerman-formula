# Self-audit

No independent referee or observational validation is claimed.

- Existing field3d_capture files are imported unchanged. The full field's effective
  closure and unresolved between-node saturation bounds remain explicit.
- Adaptive cells affect only collision quadrature, never the Hamiltonian mass
  deposition. No unaccounted regridding work or density creation is introduced.
- Every particle is assigned once, its cell contains it, and both uniform and
  Gaussian integrals are tested against analytic targets. Do not infer Gaussian
  accuracy from the easier uniform test.
- Refinement initially holds spatial nodes fixed when adding velocity samples;
  their independent subsequent trajectories can alter later grids. Lower packet
  mass also changes reaction-energy granularity, an acknowledged coupled effect.
- Radiation and finite field charging enter the same pair work equation. A forced
  production reaction checks it; its huge probability interval is a unit fixture,
  excluded from live-rate statistics. Seeded-T transport controls are excluded
  from formation fractions.
- Central impulses preserve P/L. Continuous-transport mesh force symmetry errors
  are measured, not removed by force projection. Total energy is conserved to the
  stated adaptive integration tolerance, not exactly in floating-point time steps.
- The kinetic collision coefficient is common across mass/size inputs. The only
  exceptional rate is a documented100x stress experiment applied to all families.
  No reaction function reads galaxy labels, input rotation or profile indices.
- Physical support and numerical cell size must not be conflated. Macro-particle
  separations may exceed0.1kpc in a valid local kinetic approximation. Conversely,
  coarse cells do not become accurate just because the operator is called kinetic.
- Flow controls expose artificial compressional collisions at finite cell width.
  Rotation covariance with a fixed partition does not certify a rebuilt grid.
- Expected proposal exposure is a time-integrated pre-impulse hazard diagnostic.
  Sequential impulses alter later hazards; it is not an exact compensator for the
  realized interacting process or a rigorous bound over all possible trajectories.
- Rate coefficient, packet collision-mass interpretation, radiation receiver and
  Gaussian source width are effective assumptions. In particular sigma=b in live
  runs is inherited numerical smoothing, not a universally derived physical scale.
- Matched seed values do not align stochastic event streams across different time
  steps, particle counts or cell partitions. Single-event changes are not a
  statistically established rotating/pressure-supported population difference.
- High-collision-rate stress runs need their own opacity and convergence checks;
  they cannot validate a mechanism merely by producing more T.
- Scope is finite synthetic initial conditions. Instantaneously bound free mass
  is not observed extra mass, lensing sufficiency or permanent retention. No
  cosmology, actual galaxy fit or universal no-go theorem is obtained.

All evidence uses bounded runner contracts. Read completed/incomplete statuses,
manifest hashes and stderr before counting a run; preserve resource-limited runs
as such. A completed manifest does not by itself certify the physical assertion.
