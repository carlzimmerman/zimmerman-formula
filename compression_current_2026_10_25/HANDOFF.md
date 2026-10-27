# Continue with the energy cascade, not another static force fit

Read STATUS.md, ACTION.md, LINEAR_RESPONSE.md and SELF_REVIEW.md. The previous
phase is nonlinear_transfer_2026_10_25/HANDOFF.md; its parent is
front_dynamics_2026_10_25/HANDOFF.md. The user wants formation plus preservation,
not merely a source, boundary optimizer or compatible static profile.

Retain the established static branch, finite relaxed restoring force, and
100Myr local preservation tests. Do not retune those potentials to hide the
17.37% infall law residual. Do not remove the outer reservoir, erase material
gradients, force density to a target, call optimizer energy loss radiation,
or drive a prescribed full-release sinusoid. Those dead ends remain excluded.

The direct compression source is now a concrete candidate, not a missing
algebraic term. All of its canonical forces have been audited. Increasing its
coupling is not sufficient: the actual coherent-mode rate is optimized near
eta=1 and remains slow. Its microscopic coefficient is still unprovided.
A new density gate or arbitrary saturation function is another hypothesis,
not an explanation supplied by the formula.

The next useful route must resolve transfer across scales. Options require
a precise discriminator: measure actual source/velocity spectra and mode work
in free dynamics, derive an on-shell nonlinear coupling with backreaction,
or derive a consistent fast-sector reduction. A triad resonance or allowed
kinematics alone does not establish a populated cooling channel. Independent
nonradial mechanics is not covered by the radial single-mode rate.

The current finite-carrier solver becomes expensive because of fast coupled
motion. Do not count an energy-preserving but spectrally underresolved run as
formation. Do not turn numerical energy correction into physical escape.
A justified multiscale or discrete-gradient scheme would need its own force,
charge, mass, energy and time/spatial convergence checks. The global conserved
mass in a relativistic kinetic completion may not equal sum|a|²; derive it.

## Runs and reproduction

Every contract/script/result that has a manifest is frozen. Use a fresh output
folder for reproduction. For example:

    python3 physical_completion_2026_10_25/launch.py compression_current_2026_10_25/mode_rate_contract.json NEW_MODE_RUN compression_current_2026_10_25/mode_rate.py 180
    python3 physical_completion_2026_10_25/launch.py compression_current_2026_10_25/infall_weak_contract.json NEW_WEAK_RUN compression_current_2026_10_25/infall_weak.py 300

The immutable continuation scripts read their original accepted checkpoints
and cumulative work/flux histories. They rebase the shift charge on the segment
start and report the previous error bound separately; use their sum for a
whole-history bound. The energy reference and scalar work are not rebased.
Continuation outputs are wall-limited partial histories, not completed4Myr
experiments. Changing the source checkpoint requires a new script/contract.

MANIFEST_AUDIT.json records all process outcomes and input-hash validation.
The first Picard audit and failed import are deliberately preserved. Process
completion is different from a completed physical trajectory or success.

All files of this phase remain local. No commit, index update, remote push,
or unrelated file edit was performed. The parent phase began at observed
HEAD b5e95b9c9e84fc745e8cef6a18cffe71b584c75f; other research may advance HEAD.
