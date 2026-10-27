import Mathlib
noncomputable section
namespace NonlinearTracking

theorem potential_numerator_nonnegative (phi v : ℝ)
    (hv : 0 ≤ v) (hp : v ≤ phi) : 0 ≤ phi*(phi^2-v^2) := by
  have hphi : 0 ≤ phi := le_trans hv hp
  have hdiff : 0 ≤ phi^2-v^2 := by nlinarith
  exact mul_nonneg hphi hdiff

theorem envelope_derivative_nonpositive (f q df dq M : ℝ)
    (hf : 0 ≤ f) (hq : 0 ≤ q) (hdf : df ≤ 0) (hdq : dq ≤ 0)
    (hm : 0 < M) : (df*q+f*dq)/M ≤ 0 := by
  apply div_nonpos_of_nonpos_of_nonneg
  · exact add_nonpos (mul_nonpos_of_nonpos_of_nonneg hdf hq)
      (mul_nonpos_of_nonneg_of_nonpos hf hdq)
  · exact le_of_lt hm

theorem inverse_square_envelope (f1 f2 q1 q2 g1 g2 r1 r2 M : ℝ)
    (hf2 : 0 ≤ f2) (hq1 : 0 ≤ q1) (hf : f2 ≤ f1) (hq : q2 ≤ q1)
    (hm : 0 < M)
    (h1 : M*r1^2*g1 = f1*q1) (h2 : M*r2^2*g2 = f2*q2) :
    r2^2*g2 ≤ r1^2*g1 := by
  have hleft : f2*q2 ≤ f2*q1 := mul_le_mul_of_nonneg_left hq hf2
  have hright : f2*q1 ≤ f1*q1 := mul_le_mul_of_nonneg_right hf hq1
  have hprod : f2*q2 ≤ f1*q1 := le_trans hleft hright
  nlinarith

#print axioms potential_numerator_nonnegative
#print axioms envelope_derivative_nonpositive
#print axioms inverse_square_envelope
end NonlinearTracking
