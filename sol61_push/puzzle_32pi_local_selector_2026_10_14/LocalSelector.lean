import Mathlib
noncomputable section
namespace LocalSelector

-- e = F^2/M^2; gamma = beta*e. No ODE or physical dictionary is assumed proved.
theorem rate_bound (z e : ℝ) (hz : 0 ≤ z) (he : 0 < e) :
    12*(1-z)/(e+6*z) ≤ 12/e := by
  have hd : 0 < e+6*z := by positivity
  apply (div_le_div_iff₀ hd he).2
  nlinarith

theorem fast_requires_coupling (z e beta gamma : ℝ)
    (hz : 0 ≤ z) (he : 0 < e) (hb : 0 < beta)
    (hg : gamma = beta*e) (hf : 1 ≤ 12*(1-z)/(e+6*z)) :
    gamma/12 ≤ beta := by
  have h := le_trans hf (rate_bound z e hz he)
  have he12 : e ≤ 12 := by simpa using (le_div_iff₀ he).mp h
  rw [hg]
  apply (div_le_iff₀ (by norm_num : (0:ℝ)<12)).2
  nlinarith

-- q0 is a proposed lower root; analytic integration must supply hcharge.
theorem charge_root_bound (q q0 eps k I : ℝ)
    (hq : 0 ≤ q) (_h0 : 0 ≤ q0) (he : 0 < eps) (hk : 0 ≤ k)
    (hroot : q0*(eps+k*q0)=I) (hcharge : I ≤ q*(eps+k*q)) :
    q0 ≤ q := by
  by_contra h
  have hlt : q < q0 := lt_of_not_ge h
  have hs : 0 ≤ k*(q0+q) := mul_nonneg hk (by linarith)
  have hp : 0 < (q0-q)*(eps+k*(q0+q)) := mul_pos (by linarith) (by linarith)
  nlinarith

theorem local_fraction_bound (delta eps q qmin tail J : ℝ)
    (he : 0 < eps) (hj : 0 ≤ J) (hq : qmin-tail ≤ q)
    (hd : q*J ≤ delta) : (qmin-tail)*J/eps ≤ delta/eps := by
  exact div_le_div_of_nonneg_right (le_trans (mul_le_mul_of_nonneg_right hq hj) hd) (le_of_lt he)

#print axioms rate_bound
#print axioms fast_requires_coupling
#print axioms charge_root_bound
#print axioms local_fraction_bound
end LocalSelector
