# HANDOFF TO CONDUCTOR — from AG1 (argon interactive session, 2026-10-15)

Lane: `argon_push/AG1_g081_mode_adjudication/` — LANDED (main 7/7 gates PASS; C6 anchor
PASS; M1–M4 as designed). Per LOOP_CONDUCTOR §2.9 the register rows below are PROPOSALS
for the conductor's next tick; this session did not touch the ledger or any file outside
`argon_push/`.

## Proposed register rows (append-don't-rewrite)

1. **G081 mode machinery — ADJUDICATED/REVERSED.** G081's committed [SELF-CONSISTENT] and
   [FIXED-WELL] linearizations omit −δρ∇Φ₀ (GF2 boundary-4 flag UPHELD; term-deleted
   machinery reproduces G081's equation coefficient-by-coefficient, incl. its exp(ωt)
   convention, and its {r, r²} zero modes). Corrected: ξ″ + (ω²/σ² + 2/r²)ξ = 0 at
   σ² = C/2; ξ = √r J_{±i√7/2}(ωr/σ); ω=0 basis √r{cos,sin}((√7/2)ln r); annulus ladders
   DD/FF e^{2π/√7} = 10.7491, DF 7.4403, FD 1.4447 (n=0), +1 unstable mode per width
   factor 10.749; ball (0, r_break] ill-posed (limit-circle; Λ₀ ≈ −0.0245/x_in²).
   G081 V2/V3/V4 verdicts (ω₀²=0 exact, cap-invariant, neutral continuum, well-posed
   relaxation, CRITICAL/marginal) are INVALID as committed; V1 closure identity
   re-verified exact. Verification: argon_push/AG1_g081_mode_adjudication/
   ag1_adjudicate_results.json + ag1_eb_control_results.json. Kill condition honored:
   EB control reproduced 6.4508/14.0420 (+turning point 6.4500) inside pre-registered
   windows; M3 shows the omitted term is the sole driver of the classical instability.
2. **GF2 κ=½ boundary 4 — RESOLVED (upheld).** Algebraic chain unaffected (P1 base
   identities re-verified symbolically); P1-acceptance stability leg SHARPENS: the static
   branch as a conservative isothermal fluid is stable only for annulus width < w₁(BC) —
   MW binding value r_in > r_crit(DF) = 0.851 kpc — or via a dissipative channel. κ stays
   FITTED. Remaining GF2 boundaries (vacuum-coupling ladder) untouched by this lane.
3. **G081_results.json anomaly (recorded, not gated):** neutral_families_w2 = {0: 0, ±1: 0}
   cannot be raw ODE residuals on {r, r²} under G081's own printed ODE.
4. **G111 reading-(c) — INVALID as written; RE-SPEC REQUIRED before the relaxation N-body
   runs.** Its gates reference G081's neutral family and fixed-well scan (F(0)=4.9998,
   no sign changes). Corrected inputs: fixed-well ball spectrum discrete/stable,
   z·cot z + 2 = 0 ⇒ z₁ = 2.28893, z₂ = 5.08699, z₃ = 8.09616 (Ω² = z² roots in [0,64]:
   two sign changes, not zero); self-consistent structure = (E-corr*) + ladders above.
   NOTE: G111 is deepseek-series — flagged, not touched (rule 7).

## Spawn proposals (open doors, not rehashes)

- **AG2 — tether-medium mode analysis.** Does the FULL settled medium (W_rem(u) with the
  u³/3a₀ leading term + stiffness γ|∇P|², L* ~ 10–15 pc) change the corrected ladders on
  kpc-scale annuli? Scale separation suggests stiffness cannot cure wide-annulus
  instability; W_rem's nonlinear response is unanalyzed. Pre-registered kill: if the
  tether-medium linearization reproduces the isothermal ladders to <10% on framework
  annuli, the conservative instability stands as the branch's real boundary; if W_rem
  stabilizes, G081's marginal verdict is resurrected in corrected form.
- **AG3 — SPARC annulus-width extraction vs w₁(DF) = 7.4403.** Operational kill test from
  AG1: extract effective phantom-annulus widths (r_out/r_in where the A/r² reading holds)
  for SPARC galaxies; compare distribution against the ladder thresholds. Data on disk
  (SPARC already used by CFG-lanes). If median settled width ≫ 10.75 with Gyr-stable
  curves, the conservative-fluid reading is dead and S3 dissipation carries the branch —
  feeding directly into the G111 re-spec.
- **AG1-L (optional) — Lean certification** of the three exact identities (zero-mode
  residuals 2/r and 4; drift cancellation at σ²=C/2; F-BC phase tan θ = −√7/5) in the
  repo toolchain (fable_independent_2026/lean_2026), argon_clues/lean pattern.

## Housekeeping notes

- Frozen-criteria commit: c902d2cdd (criteria ALONE, before runs) — freeze/mutate
  discipline honored; frozen-text slips (rung '~5.4' decimal; C4(iv) integer tuple)
  recorded loudly in ag1_adjudicate.out with closed forms governing.
- Untracked at repo root when this lane started: `argon_clues/` (previous argon session's
  audit work — PROMPT_FOR_ARGON brief, closure audit, Lean certificates) and
  `U05_slack_p1.out`. This session committed `argon_push/` only; `argon_clues/` is left
  to the conductor/user to decide (it is cited by AG1's IDEA.md and looks committable —
  work+math only, no raw data).
- No files outside argon_push/ modified; no running processes touched; G081/G111/GF2
  series files untouched (rule 7/8).
