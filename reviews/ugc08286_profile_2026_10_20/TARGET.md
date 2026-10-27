# UGC08286: physical profile inversion

Checkpoint `ugc08286-profile-2026-10-20`. Assessment base
`e8bb2ae70ad6b2c86790b9312861ac2269227f71`.
Parent: `reviews/collective_state_door_2026_10_20/CHECKPOINT.json`.

User authorizes execution: run the UGC08286 profile inversion with actual
disk geometry, test positive finite extra mass against independently
constrained stellar mass-to-light gradients, and determine what is forced
without new fitted physical parameters. The 17 SPARC rotation/model points
have already been read; this is not a blind pre-registration.

Use the frozen canonical simple interpolation law and its inherited a0
as the primary class-A additive-surplus comparison, not a re-fit of a0.
Carry the alternative inherited footing separately as a diagnostic. The
published SPARC gas/stars geometry and its observational origin must be
authenticated. Recompute a radially varying stellar mass distribution
through its nonlocal disk kernel; multiplying a constant-M/L rotation
template by a local M/L is not an admissible gradient calculation.

No new fitted force coupling, halo shape law, smoothing scale, stellar
gradient, hidden likelihood floor or release lifetime is introduced.
Recovered nonnegative source-bin masses are inverse quantities, not new
fundamental parameters or parameter-free predictions. Report their
nonuniqueness and support/geometry restrictions. Independent stellar
constraints must come from photometry/spectroscopy/population data not
the rotation curve. If the needed resolved information is unavailable,
state that limitation and return the strongest calculated conditional
constraint rather than invent a gradient prior.

Initially execute three checks:

1. Reproduce UGC08286's existing AG4h discrepancy with raw 17-point data
   and pin the baseline/source/units, cuts and distance/inclination.
2. Build bounded axisymmetric positive-mass forward kernels, benchmark
   them against analytic and published disk controls, and run finite
   nonnegative source feasibility/range problems over explicitly declared
   support/thickness/resolution controls. Propagate the quoted measurement
   errors; no covariance matrix is assumed to have been observed.
3. Locate independent radial stellar-population constraints and apply them
   through the same geometry. Test stellar-only feasibility where justified;
   otherwise quantify what constraint is absent and what gradient would be
   required, without promoting a required gradient into independent evidence.

Class-A baseline plus Newtonian extra mass is a conditional observational
comparison. It does not solve a coupled nonlinear polarization field or
identify a physical collective state. Positive source feasibility is not a
unique density, detection, formation mechanism or memory lifetime.

Write only this new packet and, after reconciliation, the designated live
pointer. Earlier packets, original actions, campaigns, external datasets,
publication and Git state are immutable; copy inputs into this packet if
needed for explicit runner provenance. No process/owner-job inspection or
job control. Small deterministic single-thread runs only, nominal working
memory well below 1 GB, minutes per run at most. macOS affinity/RLIMIT_AS
are known unsupported here and must not be retried; report unenforced
caps honestly. Use the computation-audit runner with supported time/CPU/
thread/output caps and explicit input/output manifests. Independent raw
implementation/result checks are required before strong numerical claims.
