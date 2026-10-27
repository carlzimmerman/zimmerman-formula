import Mathlib

/-! Static auxiliary-field and constant-shift algebra only.
No assertion that a microscopic or gravitational theory selects a constant. -/
namespace Coupled32Pi
noncomputable section

def potential (E x y : ℝ) : ℝ :=
  E + x^2/2 + x^3/6 + x^4/16 + (y+x^2/2)^2/2

theorem relaxed (E x : ℝ) :
    potential E x (-(x^2/2)) = E + x^2/2 + x^3/6 + x^4/16 := by
  unfold potential
  ring

theorem minimum_certificate (E x y : ℝ) :
    potential E x y - E =
      x^2*((x+4/3)^2/16+7/18) + (y+x^2/2)^2/2 := by
  unfold potential
  ring

theorem global_lower_bound (E x y : ℝ) : E ≤ potential E x y := by
  have h := minimum_certificate E x y
  have hx := mul_nonneg (sq_nonneg x)
    (by positivity : (0:ℝ) ≤ (x+4/3)^2/16+7/18)
  have hy := sq_nonneg (y+x^2/2)
  linarith

theorem vacuum (E : ℝ) : potential E 0 0 = E := by
  unfold potential
  ring

theorem auxiliary_relaxation (E x y : ℝ) :
    potential E x (-(x^2/2)) ≤ potential E x y := by
  rw [relaxed]
  unfold potential
  have h := sq_nonneg (y+x^2/2)
  linarith

theorem constant_shift_preserves_minimizers {α : Type*} (V : α → ℝ)
    (c : ℝ) (z : α) :
    (∀ w, V z ≤ V w) ↔ (∀ w, V z+c ≤ V w+c) := by
  constructor
  · intro h w
    have hw := h w
    linarith
  · intro h w
    exact (add_le_add_iff_right c).mp (h w)

def fingerprint (C : ℝ) : ℝ := 4*C
def areaLambda (C : ℝ) : ℝ := 2*Real.pi*C

theorem target_iff_input (C : ℝ) :
    fingerprint C = 64*Real.pi ↔ C = 16*Real.pi := by
  unfold fingerprint
  constructor <;> intro h <;> linarith

theorem area_target : areaLambda (16*Real.pi) = 32*Real.pi^2 := by
  unfold areaLambda
  ring

theorem alternative_positive : 0 < (8:ℝ)*Real.pi := by
  positivity

theorem alternative_misses_target :
    areaLambda (8*Real.pi) ≠ 32*Real.pi^2 := by
  unfold areaLambda
  have hp : 0 < Real.pi^2 := sq_pos_of_pos Real.pi_pos
  nlinarith

#print axioms relaxed
#print axioms minimum_certificate
#print axioms global_lower_bound
#print axioms vacuum
#print axioms auxiliary_relaxation
#print axioms constant_shift_preserves_minimizers
#print axioms target_iff_input
#print axioms area_target
#print axioms alternative_positive
#print axioms alternative_misses_target
end
end Coupled32Pi
