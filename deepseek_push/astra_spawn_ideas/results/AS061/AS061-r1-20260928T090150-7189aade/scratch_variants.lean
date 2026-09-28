import Mathlib
import Mathlib.Tactic

noncomputable section
open Filter
open Real

def Kfun (C0 eps alpha : ℝ) (X : ℝ) : ℝ :=
  C0 + eps * X + alpha * (X * Real.sqrt X)

lemma vA {x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun X : ℝ => X * Real.sqrt X) ((3 / 2 : ℝ) * Real.sqrt x) x := by
  have hd_raw := (hasDerivAt_id x).mul (hasDerivAt_sqrt hx.ne')
  convert hd_raw using 2
  · ext X
    simp
  · rfl
  · have hsq : Real.sqrt x * Real.sqrt x = x := Real.mul_self_sqrt (le_of_lt hx)
    have hden : (2 * Real.sqrt x) ≠ 0 := by positivity
    simp [one_mul, id]
    field_simp [hden]
    nlinarith [hsq]

lemma vB {C0 eps alpha x : ℝ}
    (hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps x)
    (hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X))
      (alpha * ((3 / 2 : ℝ) * Real.sqrt x)) x) :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) (eps + (3 / 2 : ℝ) * alpha * Real.sqrt x) x := by
  convert (hlin.add hquad) using 2
  · ext X
    rw [Pi.add_apply]
    rfl
  · rfl
  · ring_nf

lemma vC {C0 eps alpha : ℝ}
    (hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps 0)
    (hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X)) 0 0) :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) eps 0 := by
  convert (hlin.add hquad) using 2
  · ext X
    rw [Pi.add_apply]
    rfl
  · rfl
  · ring_nf

end