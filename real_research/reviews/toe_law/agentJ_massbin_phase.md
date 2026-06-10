# AgentJ — the phase-chain mass-trend test on Brouwer's released mass-binned RAR (Fig-9)

*2026-06-11. Script `agentJ_massbin_phase.py` (agent-written, orphaned at the spend limit; run + memo completed by the
orchestrator from the verified `.out`; one numpy version call patched, `trapezoid`→`trapz`, no logic change). Data:
the released `Fig-9_RAR-KiDS-isolated_Massbin-{1..4}` profiles + covariance, mass-bin edges log₁₀M\* = [8.5, 10.3,
10.6, 10.8, 11.0]. Locked wording: this tests the real-lensing-mass class's PHASE mechanism (the H3-T4 chain); it
does not confirm or refute any specific model.*

## The pre-registered fork and what the data said
**The chain's sharp form** (condensation boundary at fixed halo mass; H3-T4's machinery): predicted condensation
fractions per mass bin **0%, 0%, 90%, 100%** → a staircase with bin4−bin1 = **+0.344 dex** and slope **+0.297 dex/dex**.

**Measured** (reference = framework ν at a₀ = 9.36×10⁻¹¹; bin-1-reference variant consistent; full covariance):
offsets **[+0.112, +0.175, +0.177, +0.165]** — *not monotonic*; slope **+0.041 ± 0.037** (1.1σ); bin4−bin1 =
**+0.053 ± 0.040** vs the demanded +0.344 → **the sharp staircase is missed by ≈7.3σ. PHASE-REFUTED in the
sharp-boundary form.**

## The two-sided residual (full weight, both directions)
- **A mild mass trend is real where it should be if anything physical survives**: the 1-halo-safe subset (probe radius
  < r200 in all four bins; g_bar bins 10–14) shows slope **+0.122 ± 0.062 (2.0σ)**, Δχ²(flat→line) = 3.9 — while the
  2-halo-dominated complement is dead flat (+0.000 ± 0.047) and the modeled 2-halo-induced slope is only +0.008.
  **The control INVERTS the boring explanation**: contamination would put the trend in the dirty bins; it sits in the
  clean ones.
- 2-halo-corrected full-set slopes stay small (+0.008 to +0.059 across amplitude ×0.5–×2) — nothing approaches +0.297.

## Consequence for the H3 sign-match
H3-T4's result (early-above-late, +0.261 inside the predicted [+0.119, +0.401]) **stands as a sign/type statement** —
but the mass-binned data refuse the mechanism's sharp form: if the type split is phase-driven, the condensation
fraction must be a much **smoother** function of halo mass than the boundary model (or keyed to a second variable —
merger history/temperature — rather than mass alone). Verdict on the fork: **PHASE-REFUTED (sharp form, 7.3σ) /
PHASE-NEUTRAL-leaning-mild-trend (2.0σ, 1-halo-safe)**. The whitepaper carries both numbers.
