# Continue from the accepted full state; solve spatial mode transfer

Original objective OPEN. Read RESULTS.md, TRANSPORT_COUPLING.md and
EVIDENCE_ERRATA.md. Do not restart the search for any outlet or any static
restoring force: unseeded continuing radiation and a live local restoring
response are now demonstrated in their stated finite ranges. The law has not
formed, the mass deficit barely changes and a density trough grows.

## Exact accepted checkpoint

Use run_continue_large/state.npz at actual physical time 12.882499999999546 Myr.
All fields a, alpha, carrier_p, chi and pi must be loaded. Carry the existing
wave population generated autonomously from the original zero-wave state;
never erase or replace it. Preserve the total energy/charge/mass and inherited
work/flux ledgers. run_assessment/results.json joins the authoritative chain:

1. infall_pump_2026_10_25/run_smooth_infall, 0--5.7 Myr;
2. run_continue, 5.7--9.765 Myr;
3. run_continue_second, 9.765--12.135 Myr;
4. run_continue_large, 12.135--12.8825 Myr.

These are actual bounded partial endpoints, not their planned 20/30-Myr limits.
The current driver verifies loaded energy, field energy, shape and physical
time. For any new run copy the contract/config into new files and choose a fresh
output directory. The runner command is recorded in each manifest. Never edit
manifested scripts, contracts, states or results.

## Next mathematical obligation

The leading compact source sees L(v), whereas the required total-mass current
is a different functional. The required transport tangent has tiny bright
projection. Finite-size harmonic retardation does not repair that direct
projection in the sampled family. Initially dark directions can still mix into
radiating modes under the nonlinear Hamiltonian: this has not been excluded.

Derive or measure that spatial/compositional mixing with freely evolving mean
density and carrier. A useful sufficient condition would control the physical
energy above a relevant restoring equilibrium by outgoing flux over a finite
window on the actual mass/charge-constrained basin. Such an observability or
mixing inequality has NOT been proved. Rank-one instantaneous visibility is
not proof of an invariant dark subspace or impossibility.

Any reduced model must retain both species, finite-carrier obligations, all
positive current/phase companions and reciprocal mean force, and be calibrated
against the actual accepted full trajectory. A local fixed-mean triad, fitted
cooling or a density target cannot test the joint goal. Do not silently supply
fast modes or change g2 to force a positive result.

## Numerical and physical discriminants

* One-point large-step success did not yield a faster sustained solver: later
  roots/energy guards force shrinkage. Do not continue that strategy unchanged.
  Save full checkpoints more often in a new driver before long experiments.
* The scalar exterior's 2-kpc spacing cuts off arbitrary ~500-rad/Myr radiation.
  Refine it if studying fast carrier escape, with a conservative no-seed field
  remap and independent energy/charge/flux checks. The present measured slow
  radiation is supported by a high-resolution inner-annulus bandwidth audit.
* Track enclosed total mass at 10,25,50 kpc independently of q-boundary motion.
  The actual repaired fraction is only 0.03356% at 50 kpc. Conversion cancels
  from total-mass continuity.
* Keep both density-trough/rebound and transition minimum. A positive minimum
  does not establish a monotonic gap-free profile. Exterior T remains tiny only
  in the tested window.
* Paired response probes leave scalar fields unchanged, preserve initial total
  cell density/charge and then release density fully. At 5.7 Myr they return
  over 0.5 Myr; at final time only instantaneous restoring response is tested.
  Do not promote these to arbitrary or asymptotic stability.

The full objective is not closed. Longer evolution and nonlinear mixing remain
open because the present stiff solver cannot yet economically reach the much
longer mass-redistribution scale; no physical no-go is inferred from wall limits.
All new work is confined to this directory. Unrelated work was left alone;
no commit, push, external message or automation was performed.
