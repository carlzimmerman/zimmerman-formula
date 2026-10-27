import Mathlib
noncomputable section
namespace DensityMicro

theorem vacuum_maximum_on_negative_branch (X g n : ℝ)
    (hX : X ≤ 0) (hg : 0 < g) (hn : 0 ≤ n) : n*X-g*n^3/3 ≤ 0 := by
  have h1 : n*X ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hn hX
  have h2 : 0 ≤ g*n^3/3 := by positivity
  linarith

theorem stable_response_slope (v m n susceptibility : ℝ)
    (hm : 0 < m) (hn : 0 < n) (hs : 0 ≤ susceptibility) :
    1-v^2*susceptibility/(m*n) ≤ 1 := by
  have h : 0 ≤ v^2*susceptibility/(m*n) := by positivity
  linarith

theorem no_quadratic_response (v m n susceptibility : ℝ)
    (hm : 0 < m) (hn : 0 < n) (hs : 0 ≤ susceptibility) :
    1-v^2*susceptibility/(m*n) ≠ 2 := by
  have h := stable_response_slope v m n susceptibility hm hn hs
  linarith

theorem negative_branch_convexity_violation (A offset : ℝ) (hA : 0 < A) :
    (5/8:ℝ)*(-A-offset)+(3/8:ℝ)*(-27*A-offset) < -8*A-offset := by
  nlinarith

#print axioms vacuum_maximum_on_negative_branch
#print axioms stable_response_slope
#print axioms no_quadratic_response
#print axioms negative_branch_convexity_violation
end DensityMicro
