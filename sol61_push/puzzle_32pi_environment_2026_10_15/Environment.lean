import Mathlib
noncomputable section
namespace TrackingEnvironment

theorem feedback_polynomial_positive (E M xi lam phi : ℝ)
    (he : 0 < E) (hm : 0 < M) (hx : 0 < xi) (hl : 0 < lam) :
    0 < E*(M^2+xi*(1+2*xi)*phi^2) +
      lam*phi^4/4*(M^2*(1+4*xi)+xi*(1+6*xi)*phi^2) := by positivity

theorem timelike_radial_branch (a w : ℝ) (hw : 0 < 1+w)
    (hp : 0 < (a+w)/(1+w)) (ht : (a+w)/(1+w) < 1) :
    0 < a+w ∧ a < 1 := by
  constructor
  · exact (div_pos_iff_of_pos_right hw).mp hp
  · have h := (div_lt_iff₀ hw).mp ht
    linarith

theorem boundary_independent_decrease (a w N T : ℝ)
    (hn : 0 < N) (hT : 0 ≤ T) (hw : 0 < 1+w)
    (hp : 0 < a+w) (ha : a < 1) :
    -((a+w)/N+T*(1-a))/(1+w)^2 < 0 := by
  have h1 : 0 < (a+w)/N := div_pos hp hn
  have h2 : 0 ≤ T*(1-a) := by positivity
  have hd : 0 < (1+w)^2 := sq_pos_of_pos hw
  exact div_neg_of_neg_of_pos (by linarith) hd

#print axioms feedback_polynomial_positive
#print axioms timelike_radial_branch
#print axioms boundary_independent_decrease
end TrackingEnvironment
