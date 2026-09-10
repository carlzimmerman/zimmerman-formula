import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! These are ordered-real cutoff statements, not a CMB or MOND model. -/
namespace L125ScaleAudit

theorem same_mode_transfer (k early late : ℝ)
    (hk : k < early) (horder : early < late) : k < late := lt_trans hk horder

theorem distinct_mode_counterexample (early late : ℝ)
    (hpositive : 0 < early) (horder : early < late) :
    ∃ kc kg : ℝ, 0 < kc ∧ kc < early ∧ kc < late ∧ late < kg := by
  refine ⟨early/2,late+1,?_,?_,?_,?_⟩ <;> linarith

theorem rational_counterexample :
    (1/10 : ℝ) < 1/5 ∧ (1/5 : ℝ) < 1 ∧ (1/10 : ℝ) < 1 ∧ ¬ ((10 : ℝ) < 1) := by
  norm_num

#print axioms same_mode_transfer
#print axioms distinct_mode_counterexample
#print axioms rational_counterexample
end L125ScaleAudit
