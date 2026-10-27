import Mathlib
noncomputable section
namespace WZKinetic

theorem healthy_iff (e z : ℝ) (he : 0 < e) :
    0 < (e-6+6*z)/e ↔ 6*(1-z)<e := by
  rw [div_pos_iff_of_pos_right he]
  constructor <;> intro h <;> linarith

theorem positive_mass (e z : ℝ) (hz : z<1) (hh : 6*(1-z)<e) :
    0 < 12*(1-z)/(e-6+6*z) := by
  apply div_pos <;> linarith

theorem kinetic_reduced (e z : ℝ) (he : 0 < e) :
    (e-6+6*z)/e < 1+6*z/e := by
  apply (div_lt_iff₀ he).2
  have hh : 6*z/e*e=6*z := div_mul_cancel₀ _ (ne_of_gt he)
  nlinarith

theorem planck_ratio_bound (e z q : ℝ) (he : 0 < e)
    (hq : q=e*z) (hh : 6*(1-z)<e) : e-e^2/6<q := by
  have h := mul_lt_mul_of_pos_left hh he
  nlinarith

theorem healthy_witness :
    ((12:ℝ)-6+6*(1/2))/12=3/4 ∧
    12*(1-(1/2:ℝ))/(12-6+6*(1/2))=2/3 := by norm_num

#print axioms healthy_iff
#print axioms positive_mass
#print axioms kinetic_reduced
#print axioms planck_ratio_bound
#print axioms healthy_witness
end WZKinetic
