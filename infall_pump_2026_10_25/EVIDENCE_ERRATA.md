# Corrections are new evidence, never overwritten results

* run_restart was intended as a restart, but its first driver failed to load
  the state and merely offset a fresh initial clock by2Myr. It was interrupted
  when this was found. It has no result/manifest and is WITHDRAWN, not a
  continuation datum. run_restart_checked explicitly loads every field and
  checks prior total energy, wave energy, grid and endpoint time before work.
* The first quiet drivers had a syntax error; their failed manifests are not
  physical evidence. The next supported quiet control correctly rejected an
  independent-residual mismatch: support was added to the energy and Torch
  residual but omitted from the hand-written auxiliary-potential force.
  support_phi_checked and run_quiet_supported_final fix BOTH implementations.
  Actual quiet infall had support=0 and was unaffected by that force omission.
* The first carrier-curvature contract duplicated an input and was rejected
  before launch. The checked contract deduplicates the list. No mathematical
  conclusion is based on the rejected invocation.
* Relative/absolute finite-difference sparse-root trials, naive Jacobian reuse,
  original-variable and hybrid-chart trials include nonconverged roots. A
  process-completed manifest is not a successful physical step. Only residual,
  cap and energy accepted states enter the evolution runs.
* The original sparse Jacobian pattern omitted the next edge in the reverse
  response recurrence. complete_* and later scripts include the second-neighbor
  dependency. Earlier accepted states still satisfy the FULL residual and
  invariant tests; their Newton matrix was approximate.
* The old enclosed-mass interpolation in radius has a central startup-gradient
  artifact. volume_initial changes the initial-data map and its claims; old
  input/state results are not silently replaced. Internal composition after
  dilation has another, distinct preparation mismatch. quiet_prepare removes
  that mismatch at identical total density; its preparation energy decrease
  is explicitly excluded from radiation.
* Early nonzero outward flux does NOT by itself prove sustained infall pumping.
  The no-transport control emits comparable early radiation. The internally
  quiet state suppresses that early signal by about five orders of magnitude.
  Field work is not interchangeable with radiation: retain signed work,
  characteristic outgoing/incoming modes and the reactive boundary energy.
* A constant-current control removes the ENTIRE g2 operator with all companions,
  not just its bulk source. Source-component self energies are not additive:
  interference and the coupled material response are essential.
* The proposed exact-edge split integrator was NOT run as a global mechanism.
  Its component lemma is audited; its separated transport/wave stability
  counterexample blocks an unchanged long split run.

* radiative_modes_checked subtracted a finite-radius outer Coulomb value and
  failed analytic calibration. radiative_modes_final retains the known zero
  retarded gauge; run_radiative_final_audit passes. Only final characteristic
  audits are used in RESULTS.md. A static tail is not escaping radiation.
* The first rotating audit failed with an undefined symbol. The checked version
  runs but all tested large roots fail. Neither is accepted physical evolution.
* C4 smoothing and the later quiet pulse do not erase the early false positive.
  The authoritative smooth run independently excludes preparation loss and
  shows gravitational energy decreasing while gradient energy increases.
* The smooth fixed-step run completes 5.7 Myr without rejected steps. Earlier
  quiet continuations used different adaptive steps and stop times: do not
  attribute solver improvement solely to smoothing or claim full convergence.
* Static positive restoring stiffness survives the CC extension, but no moving
  finite-amplitude restoration experiment was completed. Finite R and its
  instantaneous transport/conversion velocity are not that experiment.
