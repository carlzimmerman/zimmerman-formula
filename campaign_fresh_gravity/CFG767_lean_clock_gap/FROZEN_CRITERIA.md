# CFG767 FROZEN CRITERIA: Lean certificates for the formation clock and the P-wave gap algebra

Date: 2026-10-14. Block CFG760–769. Committed ALONE before the Lean file. κ = ½ FITTED (unused); not "theory closed". Certificates
prove algebra/analysis from stated premises, not physics or data verdicts.

Target: `fable_independent_2026/lean_2026/CFG767_clock_gap.lean`, namespace `CFG767`.

| theorem | statement |
|---|---|
| C1 `frac_mono_t` | for τ > 0: t ↦ 1 − e^{−t/τ} is strictly increasing |
| C2 `frac_anti_tau` | for t > 0, 0 < τ₁ < τ₂: 1 − e^{−t/τ₂} < 1 − e^{−t/τ₁} (slower formation, less cold energy) |
| C3 `frac_bounds` | for t ≥ 0, τ > 0: 0 ≤ 1 − e^{−t/τ} < 1 |
| C4 `window` | τ_min ≤ τ ≤ τ_max (all > 0), t > 0 ⇒ 1 − e^{−t/τ_max} ≤ f ≤ 1 − e^{−t/τ_min} (CFG763's prediction band) |
| C5 `sparc_upper` | for t > 0: 1 − e^{−t/τ} ≥ 9/10 ⇔ τ ≤ t/ln 10 (CFG763/764's upper bound) |
| C6 `below_gap_evanescent` | s > 0, v > 0, ω² < 2v/s + 2/s² ⇒ ω² − 2/s² − 2v/s < 0 (the CFG760 gap: no local propagation) |
| C7 `deep_gap_cp` | s₀ > 0, x > 0, V > 0: with ω_g = √(2/s₀), c = V/(x ω_g s₀) equals V/(x √(2 s₀)) (CFG760/761's deep-limit c_P,max) |

**Pass:** zero sorry, only [propext, Classical.choice, Quot.sound]. **MUTATE** (`CFG767_clock_gap_MUTATE.lean`): C5 with ln 9 in place of
ln 10, and C2 with the inequality reversed, must each fail.
