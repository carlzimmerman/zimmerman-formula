import Mathlib.Tactic

/-! QX19 MUTATE twin: three false claims that must fail to compile (m = 4 passes the 3D condition; a charge dip to
-3X stays in the exact region; the Cassini margin collapses below 1). One true sanity claim. -/

namespace QX19M

theorem power_m4_false : (3 : ℕ) + 2 < 4 := by norm_num

theorem frw_pert_false {X d : ℝ} (hX : 0 < X) (hd : -3 * X ≤ d) : (1 : ℝ) ≤ (2 * X + d) / X := by
  rw [le_div_iff₀ hX]; linarith

theorem margin_false : 4.8e7 * (1 - 2e-5) < (1 : ℝ) := by norm_num

theorem sanity_true {X : ℝ} (hX : 0 < X) : (2 * X) / X = 2 := by field_simp

end QX19M
