# AG1_g081_mode_adjudication — lane record

**Date:** 2026-10-15 · **Track:** argon (interactive session; user push instruction for
argon_push) · **Status: LANDED — 7/7 main gates PASS, C6 anchor PASS, M1–M4 as designed.**

Adjudicates GF2's flagged boundary 4: G081's committed [SELF-CONSISTENT] radial mode
equation omits −δρ∇Φ₀. **Verdict: FLAG UPHELD.** G081's V2/V3/V4 stability verdicts
(ω₀² = 0 exact, cap-invariant neutral continuum, well-posed relaxation) are REVERSED;
corrected structure: ξ″ + (ω²/σ² + 2/r²)ξ = 0 at closure, ξ = √r J_{±i√7/2}(ωr/σ),
BC-ladder thresholds (DD/FF e^{2π/√7} = 10.749; DF 7.4403; FD 1.4447), ball ill-posed
(limit-circle, fall-to-center −0.0245/x_in²). GF2's κ = ½ algebraic base UNAFFECTED;
its P1-acceptance boundary SHARPENS (stability requires inner cutoff r_in > 0.85 kpc
(MW, DF-binding) or dissipation). G111 reading-(c) needs re-spec (inputs in IDEA.md §3).
EB control: ξ_crit 6.4508 / contrast 14.0420 / turning point 6.4500; M3: the omitted
term is the sole driver of the classical instability.

## Files

- `FROZEN_CRITERIA.md` — pre-registered gates, ladders, kill logic (committed ALONE
  before any run: c902d2cdd).
- `ag1_adjudicate.py` / `ag1_adjudicate.out` / `ag1_adjudicate_results.json` — main lane
  (C0–C5, C7, M1/M2/M4, corrected fixed-well spectrum, verdict table). Run:
  `python3 ag1_adjudicate.py` (exit 0 iff all gates pass).
- `ag1_eb_control.py` / `ag1_eb_control.out` / `ag1_eb_control_results.json` — C6
  Ebert–Bonnor anchor + M3 mutation + C6b turning point. Run: `python3 ag1_eb_control.py`.
- `ag1_eb_diagnostic.py` / `ag1_eb_diagnostic.out` — debug artifact preserved: first C6
  direction check FAILED because Sturm zero-counting is invalid under the Robin surface
  BC (the λ=0 solution's first zero sits at x ≈ 8.99, OUTSIDE the ξ_R = 8 domain);
  direct residual scan is the eigenvalue definition and gives the classical signs.
- `IDEA.md` — the brief-format write-up (idea / algebra / kill test / objections).
- `HANDOFF_TO_CONDUCTOR.md` — register-row proposals + G111 re-spec flag + AG2/AG3/AG1-L
  spawn proposals (ledger rows left to the conductor tick per LOOP_CONDUCTOR §2.9).

## Inputs (read at runtime, zero typed framework constants)

- `deepseek_push/G081_results.json` — constants (C, σ², r_M, r_break, a0, α_break, Mb)
  and the committed verdict strings being adjudicated.
- Literature control targets (C6 only, typed per freeze): ξ_crit 6.451, contrast 14.04.

## Scope notes (honest)

- Adjudication is internal to G081's declared model (isothermal phantom fluid reading,
  Newtonian radial Lagrangian perturbation, inner mass frozen). The full tether medium
  (W_rem + stiffness) is NOT analyzed here → AG2.
- FF/FD ladder rungs are mathematical structure of (E-corr*) with the inner-gravity-frozen
  caveat (a moving inner interface would add an inner-mass-perturbation term); the
  verdict table uses the consistent pairs DD and DF.
- No Lean certification in this landing: the exact identities (residuals 2/r and 4, drift
  cancellation, ladder phase) are one-line sympy facts recorded in the results JSON;
  AG1-L proposed in the handoff if the conductor wants them in the Mathlib tree.
