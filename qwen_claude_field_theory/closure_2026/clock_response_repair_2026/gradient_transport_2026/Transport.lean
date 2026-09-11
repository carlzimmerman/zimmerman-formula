import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic.Linarith

namespace ClockTransport
noncomputable section

theorem endpoint_positive (n a : ℝ) (hn : 0 < n) (ha : (4:ℝ)/27 < a) :
    0 < n^3-n^2+a := by
  have hs := mul_nonneg (sq_nonneg (n-2/3)) (show 0 ≤ n+1/3 by linarith)
  nlinarith only [hs,ha]

theorem positive_chord (f0 f1 theta correction : ℝ)
    (h0 : 0 < f0) (h1 : 0 < f1) (ht0 : 0 ≤ theta)
    (ht1 : theta ≤ 1) (hc : 0 ≤ correction) :
    0 < (1-theta)*f0+theta*f1+correction := by
  have hp0 := mul_nonneg (show 0 ≤ 1-theta by linarith) h0.le
  have hp1 := mul_nonneg ht0 h1.le
  by_cases he : theta = 1
  · subst theta; nlinarith
  · have ht : 0 < 1-theta := by rcases lt_or_eq_of_le ht1 with h | h; linarith; exact False.elim (he h)
    have hp := mul_pos ht h0
    linarith

theorem transport_budget (gap delta u cubic flux : ℝ)
    (hd : 0 ≤ delta) (hg : delta ≤ gap)
    (he : gap*u = cubic-flux) :
    delta*|u| ≤ |cubic|+|flux| := by
  calc
    delta*|u| ≤ gap*|u| := mul_le_mul_of_nonneg_right hg (abs_nonneg u)
    _ = |gap*u| := by rw [abs_mul, abs_of_nonneg (le_trans hd hg)]
    _ = |cubic-flux| := congrArg abs he
    _ ≤ |cubic|+|flux| := abs_sub cubic flux

#print axioms endpoint_positive
#print axioms positive_chord
#print axioms transport_budget
end
end ClockTransport
