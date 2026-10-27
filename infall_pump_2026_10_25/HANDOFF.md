# Continue the actual unseeded-infall state

Original joint objective OPEN. Read RESULTS.md and EVIDENCE_ERRATA.md first.
The advance is a real outgoing pulse with backreaction, not a sustained cascade
or galaxy formation.

Accepted continuation: run_smooth_infall/state.npz, actual physical time
5.7 Myr. Its manifest pins the model and run_smooth_prepare/state.npz. Retain
every material complex amplitude, carrier coordinate/momentum, chi and pi,
with existing energy, charge, mass, exterior grid and work ledgers. Never reset
fields or manufacture parent-mode populations. The withdrawn run_restart reset
the state; evolve_restart_checked demonstrates explicit loading and prior
energy/time checks that a new driver must retain.

Reproduction entry point: smooth_infall.py, smooth_infall_config.json and
smooth_infall_contract.json through physical_completion_2026_10_25/launch.py.
Use a fresh output directory; never overwrite a manifested run. Copy and update
the contract before changing sources. The actual command, bounds, software and
hash-pinned dependencies are recorded in run_smooth_infall/manifest.json.

Next physical discriminants:

1. Continue beyond the first pulse/turnaround with the positive coupled
   phase/current near-field block and finite carrier intact. Establish repeated
   export rather than extrapolating the packet's power. Qualify solver changes
   on residuals, forces, energy, charge, continuity and matching small steps.
2. Create paired mass/charge-preserving radial boundary perturbations at a
   specified moving state, plus an unperturbed companion; allow density and
   exterior to evolve. Measure difference force and response. Static k_R is
   not a substitute for live restoration.
3. Track enclosed mass at 10, 25 and 50 kpc, law residual, transition minimum,
   moving/fixed exterior T fractions, outgoing/incoming energy and cap slack
   together. Front conversion is not total-mass transfer. Substantial
   redistribution requires much longer evolution.
4. Refine the smooth trajectory through the first pulse at matched endpoints
   before assigning a converged spectrum or cooling efficiency.

Successful fixed 0.0025-Myr steps do not show that C4 smoothing alone cured
coarse-step stiffness: previous runs had different step histories. Do not retry
failed rotating-coordinate large steps, unitary/hybrid guesses or split_engine
unchanged. Exact edge flow is valid, but separated transport/wave evolution
fails its coupled stability test. A homogeneous parametric equation cannot
populate exact zero by itself.

No all-F birth or angular cascade is demonstrated. The coefficient remains
phenomenological. Do not add seeds, fitted cooling or a target-density force to
declare the law passed.

All phase work is in infall_pump_2026_10_25. Starting observed HEAD:
38a418bf889b9dd9ef8caa175ffaed8c26c36b5e; another observed HEAD during work:
ef9496bfd5a22e7c16551d6a8fa8d356dd8fce1c. Unrelated research was present and
was not edited. This phase has not been committed or pushed. PROVENANCE.json
records final observed HEAD and the artifact-index policy. Failed manifests
and the withdrawn restart are history, not physical evidence.
