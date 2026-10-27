import Mathlib
noncomputable section
namespace TrackingBackreaction

theorem timelike_implies_a_lt_one (a w : ℝ) (hw : 0 ≤ w)
    (ht : (a+w)/(1+w) < 1) : a < 1 := by
  have hd : 0 < 1+w := by linarith
  have h := (div_lt_iff₀ hd).mp ht
  linarith

theorem cancellation (a w u N S : ℝ) (hn : N ≠ 0) :
    -((1-u)/N)*(a+w)-(u/N)*(1+w)-S*(1-a) =
    -((a+w)/N+(u/N+S)*(1-a)) := by ring

theorem circular_speed_strictly_decreases (a w u N S : ℝ)
    (hn : 0 < N) (hu : 0 ≤ u) (hs : 0 ≤ S) (hw : 0 ≤ w)
    (hp : 0 < a+w) (ha : a < 1) :
    -((a+w)/N+(u/N+S)*(1-a))/(1+w)^2 < 0 := by
  have h1 : 0 < (a+w)/N := div_pos hp hn
  have h2 : 0 ≤ (u/N+S)*(1-a) := by positivity
  have hd : 0 < (1+w)^2 := by positivity
  exact div_neg_of_neg_of_pos (by linarith) hd

theorem physical_log_slope_bound (a w u N S : ℝ)
    (hn : 0 < N) (hu : 0 ≤ u) (hs : 0 ≤ S) (hw : 0 ≤ w)
    (hp : 0 < a+w) (ha : a < 1) :
    -1/(N*(1+w)^2) - (u/N+S)*(1-a)/((a+w)*(1+w)^2)
      ≤ -1/(N*(1+w)^2) := by
  have h : 0 ≤ (u/N+S)*(1-a)/((a+w)*(1+w)^2) := by positivity
  linarith

#print axioms timelike_implies_a_lt_one
#print axioms cancellation
#print axioms circular_speed_strictly_decreases
#print axioms physical_log_slope_bound
end TrackingBackreaction
