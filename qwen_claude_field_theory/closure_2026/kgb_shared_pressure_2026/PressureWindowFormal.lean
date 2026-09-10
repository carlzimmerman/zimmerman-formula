import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Conditional algebra for the independently derived KGB matrix pencil.
This does NOT formalize the covariant action or certify a law of nature. -/
namespace KGBPressureWindow

theorem invariant_under_curvature (b K A shift : ℝ) :
    b*(K+shift)-(A+b*shift)=b*K-A := by ring

theorem health_requires_positive_invariant (b K A : ℝ)
    (hb : 0 < b) (hK : 0 < K) (hA : A < 0) : 0 < b*K-A := by
  have hp := mul_pos hb hK
  linarith

theorem no_curvature_repair_of_nonpositive_invariant (b K A shift : ℝ)
    (hb : 0 < b) (hbad : b*K-A ≤ 0) :
    ¬ (0 < K+shift ∧ A+b*shift < 0) := by
  intro h
  have hp := health_requires_positive_invariant b (K+shift) (A+b*shift) hb h.1 h.2
  rw [invariant_under_curvature] at hp
  linarith

theorem constructive_hyperbolic_window (b D radial cross : ℝ)
    (hb : 0 < b) (hD : 0 < D) (hr : radial < 0) :
    0 < D/(2*b) ∧ -D/2 < 0 ∧ 0 < cross^2-(D/(2*b))*radial := by
  have hk : 0 < D/(2*b) := div_pos hD (mul_pos (by norm_num) hb)
  refine ⟨hk, by linarith, ?_⟩
  have hp := mul_pos hk (show 0 < -radial by linarith)
  nlinarith [sq_nonneg cross]

theorem zero_current_chart_crossing (r X L Z PX : ℝ)
    (hr : r ≠ 0) (hcurrent : PX*r=2*X*L*Z) (hz : Z=0) : PX=0 := by
  rw [hz, mul_zero] at hcurrent
  exact (mul_eq_zero.mp hcurrent).resolve_right hr

#print axioms invariant_under_curvature
#print axioms health_requires_positive_invariant
#print axioms no_curvature_repair_of_nonpositive_invariant
#print axioms constructive_hyperbolic_window
#print axioms zero_current_chart_crossing
end KGBPressureWindow
