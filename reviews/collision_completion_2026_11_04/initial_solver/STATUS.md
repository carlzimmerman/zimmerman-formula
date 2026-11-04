# Initial checkpoint solver closeout

Base research checkpoint: `fd417eea045a0b6259b8efff5e20ca62a2e14f7e`.
Actual input revisions are pinned by the v2 manifests and `PROVENANCE.json`.
Only `initial_solver/` was written; the statistics and integration-solver
packages remain frozen.

The new positive log-number route succeeds on the actual fresh checkpoint
where nearly empty number coordinates slowed the original nonlinear merit.
This is a numerical solver result for a declared finite collision operator,
not a change of physics or evidence against the microscopic history.

## Frozen API

Import `QuantumState, implicit_step` from `log_number.py` after adding this
directory to the import path. Call

    next_state, info = implicit_step(events, state, dt,
                                    tol=2e-8, number_floor=1e-14)

The state uses the existing explicit-availability number/hole interface.
`next_state.numbers()`, `Z`, `holes`, and `arrays()` retain their usual meaning.
The backend supplies physical-number RHS, physical-number Jacobian and gross
measure. Initial represented Z must be positive. This holds for the declared
fresh checkpoint with its previously quantified seed; an exactly zero
fractional boundary is not certified by this route.

Frozen solver source SHA256:
`42b35c80b7e8b661910824639fbf594e580b6f5c6f8a57e20218c00d24a21b21`.
Its solver-only source dependencies are frozen `integration_solver/protocol_holes.py`
and `integration/holes_v2.py`, plus NumPy/SciPy. Backend, background, orbit and
data dependencies are separately pinned in every run manifest.

## Verified finite checkpoint

Both new v2 runs completed and all seven declared checks pass. They use the
actual N=.0002999746374639217 fresh state, eight actual orbit phase nodes and
the frozen fast exact-angular full 25-group backend.

* `run_log001`: one dN=5e-5 step takes six Newton iterations, 7.97 child
  seconds, versus the baseline's 19 iterations and about 22 seconds. Recorded
  aggregate charged number and entropy agree at displayed precision. Full
  baseline Y was not saved, so full-vector bitwise agreement is not claimed.
  Two half steps take five plus five iterations. Positivity, Pauli, entropy,
  local energy and physical number balance all pass.
* `run_log002`: four quarter versus eight eighth steps over the same interval.
  Three to five iterations per step. Refinement changes charged number by
  -7.62e-5 relative, U1 yield by -.23161%, and mean momentum by -1.46e-6
  relative. Finest Y_U1=1.26699766e-10. Whole-number relative L1 difference
  is 1.295e-4. The run uses 67.88 child seconds and RSS 657784832 bytes.

The pure rare-number floor residual budget is 2e-19 numbers, equivalent to
3.42e-26 yield. The actual full physical-number balance includes the bulk
float floor and is at most 5.55e-16 numbers, or 9.47e-23 yield. The latter
is stated independently; it is not mislabeled as 1e-18 total-number accuracy.
Local collision energy relative errors remain below 1.70e-17. `DERIVATION.md`
distinguishes these solver budgets from collision-time and physical-model
errors.

The coordinator and history agent have the frozen API and hashes. The history
agent independently owns comparison against the original floor solver at the
later fresh checkpoint and the subsequent common field history. Those are
not inferred from this fixed-background control. The route remains open for
that coupled continuation and broader convergence, with no further experiment
started by this package. No jobs remain active.
