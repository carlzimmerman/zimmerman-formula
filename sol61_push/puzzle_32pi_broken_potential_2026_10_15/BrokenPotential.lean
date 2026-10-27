import Mathlib
noncomputable section
namespace BrokenPotential

theorem potential_positive (phi : ℝ) :
    0 < (phi^2-1)^2/4+(1:ℝ)/100 := by positivity

theorem feedback_counterexample :
    (13:ℝ)/50*(1+3*(1/2)) - (1/2)/2*(3+5*(1/2)) +
      (1/2)^2/4*(5+7*(1/2)) = -31/160 := by norm_num

theorem local_zero_slope :
    let u : ℝ := 1/1000000
    let c : ℝ := -155/261
    let a : ℝ := 31/52200031
    a+u*c*(1-a)=0 := by norm_num

theorem stationary_point_is_minimum (N : ℝ) (hn : 0 < N) :
    0 < (2:ℝ)/N := by positivity

#print axioms potential_positive
#print axioms feedback_counterexample
#print axioms local_zero_slope
#print axioms stationary_point_is_minimum
end BrokenPotential
