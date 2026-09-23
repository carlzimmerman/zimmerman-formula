import Mathlib

/-!
A single exact local jet of the Lorentz-well static spatial principal block.
The block is [[2-alpha,-d],[-d,d*B_L]]. Its variational derivation is external
(the adjacent symbolic audit), while every coefficient and sign below is
checked exactly. This is not a global halo solution, a temporal-instability
proof, or a proof of full-theory closure.
-/
namespace LorentzWellStaticWitness

noncomputable def alpha : ℝ := 1 / 40000
noncomputable def d : ℝ := 9 / 5
noncomputable def beta : ℝ := d / (2 - alpha)
noncomputable def s : ℝ := 1
noncomputable def epsilon : ℝ := 1 / 1000000000
noncomputable def n : ℝ := 93 / 50
noncomputable def Y : ℝ := 1 / 100000000
noncomputable def a0 : ℝ := 1 / 10
noncomputable def Qsq : ℝ := s ^ 2 + Y

noncomputable def oldBL : ℝ := beta + 2 * beta ^ 2 * Real.sqrt Y / a0
noncomputable def wellBL : ℝ :=
  n / (2 * d * s) * (1 + Y / s ^ 2 - Y / (s * epsilon))
noncomputable def newBL : ℝ := oldBL + wellBL
noncomputable def oldDet : ℝ := (2 - alpha) * (d * oldBL) - d ^ 2
noncomputable def newDet : ℝ := (2 - alpha) * (d * newBL) - d ^ 2
noncomputable def temporalHessian : ℝ :=
  n * (Qsq / (epsilon * s ^ 2) - Y / s ^ 3)

noncomputable def oldMatrix : Matrix (Fin 2) (Fin 2) ℝ :=
  !![2 - alpha, -d; -d, d * oldBL]
noncomputable def newMatrix : Matrix (Fin 2) (Fin 2) ℝ :=
  !![2 - alpha, -d; -d, d * newBL]

theorem sqrtY_exact : Real.sqrt Y = (1 / 10000 : ℝ) := by
  have hy : Y = (1 / 10000 : ℝ) ^ 2 := by norm_num [Y]
  rw [hy, Real.sqrt_sq_eq_abs]
  norm_num

theorem determinant_bridge :
    Matrix.det oldMatrix = oldDet ∧ Matrix.det newMatrix = newDet := by
  constructor <;> simp [oldMatrix, newMatrix, Matrix.det_fin_two, oldDet, newDet]
  <;> ring

theorem oldDet_exact : oldDet = (11664 / 1999975 : ℝ) := by
  unfold oldDet oldBL
  rw [sqrtY_exact]
  norm_num [alpha, d, beta, a0]

theorem newDet_exact :
    newDet = (-535479983488514879907 / 31999600000000000000 : ℝ) := by
  unfold newDet newBL oldBL
  rw [sqrtY_exact]
  norm_num [wellBL, alpha, d, beta, a0, n, s, Y, epsilon]

theorem temporalHessian_exact :
    temporalHessian = (9300000092999999907 / 5000000000 : ℝ) := by
  norm_num [temporalHessian, n, Qsq, s, Y, epsilon]

theorem oldDet_positive : 0 < oldDet := by
  rw [oldDet_exact]
  norm_num

theorem newDet_negative : newDet < 0 := by
  rw [newDet_exact]
  norm_num

theorem temporalHessian_positive : 0 < temporalHessian := by
  rw [temporalHessian_exact]
  norm_num

theorem timelike_and_supersonic :
    0 < s ^ 2 ∧ Qsq - Y = s ^ 2 ∧ epsilon / s < Y / Qsq := by
  norm_num [s, Qsq, Y, epsilon]

theorem local_static_tradeoff :
    0 < 2 - alpha ∧ 0 < Matrix.det oldMatrix ∧
      Matrix.det newMatrix < 0 ∧ 0 < temporalHessian := by
  obtain ⟨ho, hn⟩ := determinant_bridge
  exact ⟨by norm_num [alpha], by rw [ho]; exact oldDet_positive,
    by rw [hn]; exact newDet_negative, temporalHessian_positive⟩

#print axioms sqrtY_exact
#print axioms determinant_bridge
#print axioms oldDet_exact
#print axioms newDet_exact
#print axioms temporalHessian_exact
#print axioms oldDet_positive
#print axioms newDet_negative
#print axioms temporalHessian_positive
#print axioms timelike_and_supersonic
#print axioms local_static_tradeoff
end LorentzWellStaticWitness
