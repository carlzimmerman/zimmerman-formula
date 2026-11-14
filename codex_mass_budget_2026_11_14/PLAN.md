# Mass-budget correction and closure investigation

Base checkpoint: `38b52055e1` (2026-11-14); the shared checkout is active, so individual evidence records pin input hashes. User authorized correction of the argument and grading bug, the actual enclosed-mass calculation, latest-work review, an attempt toward theory closure, and a Claude handoff.

## Contract

Correct the conditional algebra and its physical interpretation without changing historical numerical labels. Compute the masses of the implemented profiles, distinguish a fixed-law interior from a rescaled halo, and establish the conditions for a conserved, nonnegative joined profile. Verify any existing grading fix rather than replace it redundantly. A final theory would additionally require a well-posed dynamical completion, derived transition, stability, and appropriate observational tests; algebraic matching alone does not meet that target. A TOE additionally requires a specified connection to nongravitational interactions, absent from this calculation.

## Implementation and research routes

- [x] Inspect newest Claude work and pin current source versions. Preserve deposited artifacts and historical results.
- [x] Correct CJ1 and the local PAPER72 source with a dated correction; preserve the deposited v1.4 receipt and make clear the edited source is an undeposited correction. Recheck scientific wording and literal audit dependencies.
- [x] Verify the already-present per-footing WLJ1 fix, add a regression that rejects the former shared flag, and reproduce grading into a separate directory. Owner: fix_wlj1.
- [x] Execute actual FZS1/JNT2 enclosed profiles at both footings and stated mass/redshift/radius grids, with analytic benchmarks, mass conservation and force-law residual checks. Owner: actual_mass_budget; writes calculation/ only.
- [x] Independently audit XJ1's exact junction and derive its existence/positivity conditions, then test the missing dynamical matching condition. Owner: latest_closure_audit; writes latest_review/ only.
- [x] Reconcile the three routes, retain unresolved dynamics explicitly, and compile the corrected document.
- [x] Save the concrete Claude handoff in the shared repository. Direct app delivery was unavailable because access to Claude was not approved; no external message was sent.

The three distinct scientific discriminators are (1) common-radius algebra against the claimed budget implication, (2) actual implemented radial mass and force-law checks, and (3) conserved-current and field matching at the proposed moving boundary. Each can refute a specific step without refuting the underlying a0-density postulate.

## Verification and ownership

Root owns this plan, CJ1/PAPER72 correction and handoff. Existing lane calculations and outputs are read-only except the separately assigned grading source/test scope. New numerical results require input hashes before/after, environment, command, outcome and non-claims. Avoid full forest boxes and do not publish/deposit from this task. Verify latest changes again before any targeted edit. No bulk staging or branch switching in the active shared checkout.
