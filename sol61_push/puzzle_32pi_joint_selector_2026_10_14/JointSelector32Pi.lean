import Mathlib

noncomputable section
namespace JointSelector32Pi

def ratio (gamma : ℝ) : ℝ := 3/(4*gamma)

theorem target_iff (gamma : ℝ) (hg : 0 < gamma) :
    ratio gamma = 32*Real.pi ↔ gamma = 3/(128*Real.pi) := by
  unfold ratio
  have h4 : 4*gamma ≠ 0 := by positivity
  have hp : 128*Real.pi ≠ 0 := by positivity
  constructor
  · intro h
    apply (eq_div_iff hp).2
    have h' := (div_eq_iff h4).mp h
    nlinarith
  · intro h
    rw [h]
    field_simp
    <;> ring

theorem stable_mass (z e : ℝ) (hz : 0 < z) (hu : z < 1) (he : 0 < e) :
    0 < 12*(1-z)/(e+6*z) := by
  apply div_pos <;> linarith

theorem unstable_mass (z e : ℝ) (hz : 1 < z) (he : 0 < e) :
    12*(1-z)/(e+6*z) < 0 := by
  apply div_neg_of_neg_of_pos <;> linarith

theorem pure_power_unstable (p u a : ℝ)
    (hp : 0 < p) (hu : 0 < u) (ha : 0 < a) :
    -(p^2*u/a^2) < 0 := by
  have h : 0 < p^2*u/a^2 := by positivity
  linarith

theorem target_and_alternative :
    ratio (3/(128*Real.pi)) = 32*Real.pi ∧
    ratio (3/(64*Real.pi)) = 16*Real.pi := by
  unfold ratio
  have hp : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  constructor <;> field_simp <;> ring

theorem additive_offset_changes_ratio (r t : ℝ) (hr : 0 < r) (ht : 0 < t) :
    r/(1+t) < r := by
  apply (div_lt_iff₀ (by linarith : 0 < 1+t)).2
  have h : 0 < r*t := mul_pos hr ht
  nlinarith

#print axioms target_iff
#print axioms stable_mass
#print axioms unstable_mass
#print axioms pure_power_unstable
#print axioms target_and_alternative
#print axioms additive_offset_changes_ratio
end JointSelector32Pi
