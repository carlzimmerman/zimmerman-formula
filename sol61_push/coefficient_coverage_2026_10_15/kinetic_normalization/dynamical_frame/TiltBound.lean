import Mathlib
noncomputable section
namespace TiltBound

def dispersion (a s b v k w : ℝ) : ℝ :=
 (a*w-s*k^2)*(b*w-b*k^2+(a-s)*v^2)-(a-s)^2*v^2*w

theorem homogeneous_factor (a s b v w : ℝ) :
 dispersion a s b v 0 w = w*(a*b*w+(a-s)*s*v^2) := by
 unfold dispersion
 ring

theorem growing_root_sign (a s b v : ℝ)
 (hs : 0 < s) (ha : s < a) (hb : 0 < b) (hv : 0 < v) :
 -((a-s)*s*v^2)/(a*b) < 0 := by
 apply div_neg_of_neg_of_pos
 · exact neg_neg_of_pos (mul_pos (mul_pos (sub_pos.mpr ha) hs) (sq_pos_of_pos hv))
 · exact mul_pos (lt_trans hs ha) hb

theorem finite_band_constant_negative (a s b v k : ℝ)
 (hs : 0 < s) (hk : 0 < k)
 (hband : b*k^2 < (a-s)*v^2) :
 dispersion a s b v k 0 < 0 := by
 have hid : dispersion a s b v k 0 = s*k^2*(b*k^2-(a-s)*v^2) := by
  unfold dispersion
  ring
 rw [hid]
 exact mul_neg_of_pos_of_neg (mul_pos hs (sq_pos_of_pos hk)) (sub_neg.mpr hband)

theorem homogeneous_root (a s b v : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :
 dispersion a s b v 0 (-((a-s)*s*v^2)/(a*b)) = 0 := by
 rw [homogeneous_factor]
 field_simp
 <;> ring

#print axioms homogeneous_factor
#print axioms growing_root_sign
#print axioms finite_band_constant_negative
#print axioms homogeneous_root
end TiltBound
