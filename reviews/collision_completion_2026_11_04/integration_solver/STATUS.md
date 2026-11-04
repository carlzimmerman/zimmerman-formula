# Integration solver checkpoint

Base research checkpoint: `fd417eea045a0b6259b8efff5e20ca62a2e14f7e`.
Actual assessment inputs and executable versions are fixed by the v2 manifests
and the final `PROVENANCE.json`, rather than the moving shared branch.

Promoted and frozen interfaces:

* `protocol_holes.py`: mixed physical-number/Pauli-hole state, explicit
  availability backend adapter and sparse implicit driver. Requires
  `number_rhs(f,availability)`, `number_jacobian(f,availability)` with derivative
  **with respect to physical number Y**, and `number_gross(f,availability)`.
  No event-array, S or flux interface is required. SHA256
  `4025d729b63b5e6255c4cc9ce97888d84087ecc0e9abfd6e5b4253d57862d1bf`.
* `protocol_average.py`: `AveragedNumberEvents(local_events,phase_weights,xs)`
  combines these three number operations, exposes local/averaged energies and
  phase weights, and flags/combines forward omission measures. SHA256
  `f30e65fa3aa8623fa6f9b9d91147a0c75b45e4b6d4a52def69e0c725bce36e85`.

`DERIVATION.md` fixes units, the number-Jacobian chain rule, the residual
criterion, calibrated high-precision reference, and the distinction between
local energy conservation and phase-averaged field-action covariance.
No old statistics source was changed.

## Promoted evidence

* `run_toy001` completed: immutable integration/holes_v2 scalar finite-BE
  reference against a 100-digit root. A physical hole of 3.000001e-24 is
  retained at m=1e-24, dt=1 with relative error 5.1e-15. The earlier dt=1000m
  expectation of equilibrium was wrong: the correct finite-BE hole is .001996.
* `run_protocol001` completed: the generic physical-number adapter reproduces
  those sub-ulp holes through an independent analytic backend; maximum
  high-precision reference error is 3.5e-15, the coordinate Jacobian finite
  difference error is 2.88e-11, and copy type, bounds and local energy pass.
* `run_average002` completed: independent scaled-backend weighted RHS,
  Jacobian, gross measure, phase normalization, omission, energy and implicit
  physical-step controls pass.
* `run_angular001` completed in 36.61 child seconds, RSS 644448256 bytes:
  actual warm checkpoint, eight orbital phases, frozen exact-angular 25-group
  backend, two successive dN=1e-6 collision intervals. All five checks pass.
  Number balance relative residual is below 3.85e-17; local collision energy
  relative residual below 7.2e-16; entropy grows and all bounds hold. Newton
  uses 14 then 3 iterations. The old approximate warm state's saturated cells
  relax to maximum fermion f=.956741 then .926255. Final conditional
  Y_U1=1.0741454e-9 and mean p/mu=.00622925. Occupied-forward omission is
  3.125e-8; this is not a bound on inverse reactions through omitted states.
* `run_angular_refine001` completed in 169.45 child seconds, RSS 649117696
  bytes: the same actual fixed eight-phase warm operator advances total
  collision-equivalent dN=3e-5 with three steps 1e-5 versus six steps 5e-6.
  All six checks pass. Halving the step changes charged number by 4.89e-6,
  U1 number by 3.52e-5, and U1 mean momentum by -3.07e-5, all relative.
  Whole-number L1 difference is 1.50e-5. Independent coordinate balance stays
  below 4.75e-17 relative and local energy rate error below 8.92e-16.
  Entropy increases; final maximum fermion occupations are .72433/.71475.
  Initial-step Newton iterations are 33/23, later steps three iterations.

These are fixed-operator collision controls and a restart from the previous
approximate warm checkpoint. They do not certify a cosmological history or
the original candidate. The coordinator owns the exact-angular common field
evolution and its covariance/work ledger.

## Preserved experimental failures

* `run_control001`: failed second fixed-warm step with original linear-hole
  Newton at tighter tolerance 2e-9; missing full result is explicit.
* `run_control002`: stable log1p/expm1 flux alone did not remove that failure.
* `run_trace001`: the diagnostic script completed, but its contained solver
  result has `completed=false`. It traces merit-line-search damping of
  multiplicative soft-hole changes; it is not successful kinetics evidence.
* `run_control003`: log-coordinate Newton completed the first two steps but
  stalled on the third. It is not promoted for production.
* `run_control004`: adaptive log-coordinate experiment hit its 235 CPU-second
  resource bound with no completed result. It is resource inconclusive and
  is not recommended for production.
* `run_average001`: only the self-test's NumPy Boolean JSON serialization
  failed. The helper was unchanged; the separately named corrected control
  produced `run_average002`.

All original failed sources and records are retained. The promoted exact
angular backend resolves the old warm saturation issue at the tested point;
there is no need to claim that the unpromoted global-log variants succeeded.
No jobs remain active. No further experiments are implied by this checkpoint.
