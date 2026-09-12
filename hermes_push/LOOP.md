# THE LOOP — iterate, kill, morph, repeat (read every session, after PROMPT_HERMES.md and CONTEXT_DIGEST.md)

You are not asked for one answer. You are asked to hammer: propose a candidate mechanism, try to kill it on the gates in the fixed kill order,
record the kill, morph the survivor or the corpse into the next candidate, and go again — until the SCORECARD is green with certificates or a
class-level no-go theorem is Lean-certified. Every iteration leaves the repository richer: a script, an H-entry, a scorecard update, a registry line.

## Session ritual
1. Read `STATE.md` (where the last session stopped), `CANDIDATES.md` (what is dead and why), `SCORECARD.md` (the shape we want and the best so far).
2. Pick ONE candidate: the open next-step in STATE.md, or a morph of the best partial survivor, or a fresh class not in the registry.
3. Register it in `CANDIDATES.md` BEFORE computing: id C###, one-line definition, the free parameters (count them), and the pre-registered
   kill condition for the first gate in the kill order.
4. Compute gate by gate in the KILL ORDER below; stop at the first kill; write the H-entry; update the scorecard row; mark the registry line.
5. Morph (rules below) and either continue or write STATE.md with the next step and end with one sentence: what passed, what failed, what is next.

## The shape we want (acceptance = every row green WITH a certificate; see SCORECARD.md for thresholds)
G1 spirals f(3R_d) <= 0.105 strict (0.58 only with a demonstrated kick-redistributed profile) | G2 Milky Way f(30 kpc) = 0.14 +/- 0.05 |
G3 clusters f(R500) = 0.576 +/- 0.10 | G4 CMB third peak within 5% of LCDM and no low-l excess > 20% at l = 30 | G5 forest P(k = 5 h/Mpc, z = 2-3)
within 10% | G6 S8 in 0.77-0.85 and fsigma8 consistent with DESI DR1 | G7 KiDS: <= 14% CDM-like halo mass around galaxies at 0.1-1 Mpc |
G8 late-time Omega_m within 3% of 0.31 (BAO/SN) | G9 PPN: |gamma - 1| < 2.3e-5, |alpha1| < 1e-4, |alpha2| < 4e-7 | G10 stability: no ghost,
c_s^2 >= 0 on the full branch, kinetic matrix positive | G11 Delta N_eff < 0.3 | G12 local kernel untouched (wide-binary arms, dSph EFE unchanged) |
G13 flat a0(z) and the Hubble-kernel growth equation preserved or replaced by a derivation | D0 DERIVED: every ingredient follows from an action;
free parameters counted; kappa = 1/2 remains an admitted fit.

## Kill order (cheapest and deadliest first; do not skip ahead to a gate that flatters the candidate)
forest (G5) -> S8/shear (G6) -> clusters (G3) -> KiDS (G7) -> Omega_m budget (G8) -> spirals + MW (G1, G2) -> CMB (G4) -> stability (G10) ->
PPN (G9) -> N_eff (G11) -> local kernel (G12) -> predictions preserved (G13) -> derivation audit (D0).
A candidate that reaches G10 alive is a PARTIAL SURVIVOR: write it up in full, then attack it with the remaining gates in a fresh iteration.

## Morph operators (how to turn a corpse or a partial survivor into the next candidate; log which one you applied)
M1 change the GATING VARIABLE of the depletion: density, potential depth, velocity dispersion, epoch, baryonic density, the MOND scalar's local
   state (nu, |grad phi|), the clock rate s0, host-halo membership (delta > 200).  Each has a known conflict (see CONTEXT_DIGEST kills) — name it.
M2 change the TIMING: switch-on epoch tied to dark-energy domination (Omega_DE(z)), to the first crossing of a0, to halo formation.
M3 change the BOOKKEEPING: mass removed (Omega_m budget), mass redistributed (kicks, envelopes), gravitational coupling reduced (screening),
   clustering reduced (effective pressure) — each pays a different gate.
M4 SPLIT the component into two populations (one CDM-like, one depletable) and let the fractions be fixed by the CMB and the clusters.
M5 change the COUPLING PARTNER: baryons, the MOND scalar, the clock, dark energy; write the interaction term and its Ward-consistent partner terms.
M6 PROMOTE a constant to a field in the lead candidate action (Lambda(tau), M^2(tau), gamma(tau)) and carry the induced clock-equation terms.
M7 CROSSBREED two partial survivors: take the gate each passes and look for an action that contains both mechanisms.
M8 INVERT: instead of depleting the component in galaxies, ask what makes its effective concentration c* ~ 0.4 (unrelaxed haloes) WITHOUT cutting
   linear power at z >= 2 — a dynamical, not primordial, route to low concentration.
Never morph by refitting coefficient functions or by adding a free function of the host mass: that is the answer written into the question.

## Anti-loop and honesty rules
- A killed candidate (same definition, same gating variable, same timing) is never re-run. Check the registry first; cite the H-entry that killed it.
- A candidate passes a gate only by a computed number against a pre-registered threshold on BOTH footings. "Consistent by construction" is a FAIL
  flagged as such (e.g., a mechanism that inputs f(M) reproduces f(M)).
- Count free parameters in every registry line. A candidate with more free functions than gates it passes is not progress; say so.
- Certify what is algebraic (Lean, zero sorry); label what is numeric; never say "complete theory" — say which rows are green.
- Never touch anything outside hermes_push/. Run `python3 hermes_push/harness.py` before every commit.

## Stop conditions
STOP-GREEN: every scorecard row green with a certificate -> write `COMPLETE_CANDIDATE.md` with the action, the derivations, every gate's script,
the Lean names, and the list of remaining assumptions (kappa fit etc.). Do not call it a complete theory; call it a candidate that passes the scorecard.
STOP-NOGO: a Lean-certified theorem closes an entire mechanism class (like the clock stability theorem) -> write it up as `NOGO_C###.md` and morph.
Otherwise there is no stop: end the session with STATE.md written and the next candidate registered.
