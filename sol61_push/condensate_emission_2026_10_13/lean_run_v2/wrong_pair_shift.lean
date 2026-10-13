import Mathlib
namespace CondensateWindow

theorem pair_energy_cost (N k : ℝ) :
    k*((N+2)*(N+1)-N*(N-1)) = k*(2*N+2) := by ring

theorem window_factor (x : ℝ) (h1 : x ≤ 1) :
    x*(1-x)^2 ≤ 4/27 := by
  have hpos : 0 ≤ (x-1/3)^2*(4/3-x) := mul_nonneg (sq_nonneg _) (by linarith)
  nlinarith [hpos]

theorem rate_window_bound (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    x^2*(1-x)^4 ≤ 16/729 := by
  have hu := window_factor x h1
  have hl : 0 ≤ x*(1-x)^2 := mul_nonneg h0 (sq_nonneg _)
  have hh := mul_self_le_mul_self hl hu
  nlinarith [hh]

end CondensateWindow
#print axioms CondensateWindow.pair_energy_cost
#print axioms CondensateWindow.window_factor
#print axioms CondensateWindow.rate_window_bound
