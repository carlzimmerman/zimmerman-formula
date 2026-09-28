import Mathlib

noncomputable section
open Filter
open scoped Topology

-- probe: are the instance-path goals rfl-closable?
example : Real.instAddCommGroup = DenselyNormedField.toNontriviallyNormedField.toDivisionRing.toAddCommGroup := by
  rfl

example : Semiring.toModule = (NormedAlgebra.toNormedSpace ℝ).toModule := by
  rfl

-- probe: convert with all_goals (try rfl | simp) against instances
example (yp : ℝ) (y : ℝ) (hyy : 0 < y + yp) :
    HasDerivAt (fun y : ℝ => Real.log (y + yp)) ((y + yp)⁻¹) y := by
  have hin : HasDerivAt (fun z : ℝ => z + yp) 1 y := by
    simpa [id_eq] using ((hasDerivAt_id y).add_const yp)
  have hc1 := HasDerivAt.comp (x := y) (hh₂ := Real.hasDerivAt_log hyy.ne') (hh := hin)
  convert hc1 using 1
  · rfl
  · simp [mul_one]
  all_goals try rfl
  all_goals try simp
