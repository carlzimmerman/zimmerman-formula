import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/- Exact theorem statements/proofs from Mondlean.lean at 0eee1a513, isolated
   to distinguish their algebra from the full file's dependency build.
   The hstate premise is NOT derived from the action here. In particular,
   it omits the W0 counterterm of the canonical tracked action; see REPORT.md.
   Namespace is added only to avoid collisions with other project theorems. -/
namespace ReviewedClaudeTime

theorem clock_rate_from_conservation (U mrel s0 γ q qd w : ℝ) (hU : U ≠ 0) (hm : mrel ≠ 0)
    (hstate : w * (U / mrel) = U * (s0 - 1) + 2 * γ * q ^ 2 * qd) :
    s0 - 1 = w / mrel - 2 * γ * q ^ 2 * qd / U := by
  field_simp at hstate ⊢
  linear_combination -hstate

theorem clock_rate_is_pressure_over_margin (U mrel s0 q qd w : ℝ) (hU : U ≠ 0) (hm : mrel ≠ 0)
    (hstate : w * (U / mrel) = U * (s0 - 1) + 2 * 0 * q ^ 2 * qd) :
    s0 - 1 = w / mrel := by
  have h := clock_rate_from_conservation U mrel s0 0 q qd w hU hm hstate
  simpa using h

theorem clock_runs_fast_iff_pressure_positive (mrel s0 w : ℝ) (hm : 0 < mrel)
    (h : s0 - 1 = w / mrel) : 1 < s0 ↔ 0 < w := by
  have hw : w = (s0 - 1) * mrel := by
    field_simp at h; linarith
  constructor
  · intro hs; rw [hw]; exact mul_pos (by linarith) hm
  · intro hp; rw [hw] at hp; nlinarith

#print axioms clock_rate_from_conservation
#print axioms clock_rate_is_pressure_over_margin
#print axioms clock_runs_fast_iff_pressure_positive
end ReviewedClaudeTime
