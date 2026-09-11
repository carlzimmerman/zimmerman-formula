import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/- Conditional algebra only. The independent SymPy calculation supplies the
   action-to-coefficient bridge; no covariant variation is formalized here. -/
namespace ClockConstraintLength
noncomputable section

theorem shifted_constraint (d0 d2 e0 e2 j ud u f x : ℝ)
    (h0 : d0 ≠ 0) (h2 : d2 ≠ 0) (hd : d0+d2*x ≠ 0) :
    (1+(d2/d0)*x)*(-(j*ud+(e0+e2*x)*u+f)/(d0+d2*x)+(e2/d2)*u) =
      (j*ud+(e0-e2*d0/d2)*u+f)/(-d0) := by
  field_simp [h0,h2,hd]
  ring

theorem spatial_denominator_nonzero (d0 d2 x : ℝ)
    (h0 : d0 < 0) (h2 : d2 < 0) (hx : 0 ≤ x) :
    d0+d2*x ≠ 0 := by
  have hm : d2*x ≤ 0 := mul_nonpos_of_nonpos_of_nonneg (le_of_lt h2) hx
  have hn : d0+d2*x < 0 := by linarith
  exact ne_of_lt hn

def ellH2 (m v : ℝ) : ℝ := m*(m+2)/(9*(m+1)*v*(1-v))

/- gamma=0, specified stationary profile. f=m/(1+m) is the background
   W(0)/rho_clock ratio, NOT the fraction of dust inside a galaxy. -/
theorem length_coefficient_bound (m v : ℝ) (hm : 0 < m)
    (hv : 0 < v) (hv1 : v < 1) :
    (8/9 : ℝ)*(m/(m+1)) ≤ ellH2 m v := by
  have hp : 0 < m+1 := by linarith
  have hden : 0 < 9*(m+1)*v*(1-v) :=
    mul_pos (mul_pos (mul_pos (by norm_num) hp) hv) (by linarith)
  unfold ellH2
  rw [le_div_iff₀ hden]
  have he : (8/9 : ℝ)*(m/(m+1))*(9*(m+1)*v*(1-v)) =
      8*m*v*(1-v) := by
    field_simp [ne_of_gt hp]
  rw [he]
  have hs := mul_nonneg (le_of_lt hm) (sq_nonneg (2*v-1))
  nlinarith [sq_nonneg m]

theorem short_length_requires_small_coefficient (m v r : ℝ)
    (hm : 0 < m) (hv : 0 < v) (hv1 : v < 1)
    (hr : ellH2 m v ≤ r^2) :
    m/(m+1) ≤ (9/8 : ℝ)*r^2 := by
  have hb := length_coefficient_bound m v hm hv hv1
  linarith

theorem fixed_epoch : ellH2 (1/10) (1/2) = 14/165 := by
  norm_num [ellH2]

#print axioms shifted_constraint
#print axioms spatial_denominator_nonzero
#print axioms length_coefficient_bound
#print axioms short_length_requires_small_coefficient
#print axioms fixed_epoch
end
end ClockConstraintLength
