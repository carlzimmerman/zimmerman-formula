import Mathlib
import Mathlib.Tactic

noncomputable section
open Real

def Kfun (C0 eps alpha : ℝ) (X : ℝ) : ℝ :=
  C0 + eps * X + alpha * (X * Real.sqrt X)

lemma t4 {C0 eps alpha x : ℝ} :
    Kfun C0 eps alpha x =
      ((fun X : ℝ => C0 + eps * X) + fun X : ℝ => alpha * (X * Real.sqrt X)) x := by
  rfl

lemma t5 {C0 eps alpha : ℝ} :
    (fun X : ℝ => Kfun C0 eps alpha X) =
      ((fun X : ℝ => C0 + eps * X) + fun X : ℝ => alpha * (X * Real.sqrt X)) := by
  ext X
  rfl

lemma t6 {x : ℝ} (hx : 0 < x) :
    3 / 2 * Real.sqrt x = 1 * Real.sqrt x + id x * (1 / (2 * Real.sqrt x)) := by
  simp [one_mul, id]

lemma t7 {x : ℝ} (hx : 0 < x) :
    3 / 2 * Real.sqrt x = 1 * Real.sqrt x + id x * (1 / (2 * Real.sqrt x)) := by
  simp [one_mul, id]
  field_simp

end