/-
PAR1 MUTATE twin: false versions of PAR1.lean's statements. Every one must fail to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib.Tactic

namespace PAR1M

-- MU-a: a restoring force around free fall (false: omega^2 <= 0)
theorem scr_pos (K n chi k2 : ℝ) (hK : 0 < K) (hn : 0 < n) (hc : 0 ≤ chi) (hk : 0 < k2) :
    0 < -(K * n) * (K * chi) / (K * chi + k2) := by
  have hd : 0 < K * chi + k2 := by positivity
  positivity

-- MU-b: the span reaches c0^2/2 (false: strictly below)
theorem span_ge (c0 n0 n : ℝ) (hc : 0 < c0) (h0 : 0 < n0) (hn : n0 ≤ n) :
    c0 ^ 2 / 2 ≤ c0 ^ 2 / 2 * (1 - n0 ^ 2 / n ^ 2) := by
  nlinarith

-- MU-c: the frozen sign of S8 (false: the defect is +b D^3/12)
theorem shock_defect_frozen_sign (t1 D a b : ℝ) (hD : D ≠ 0) :
    (-(a * D + b * D ^ 2 / 2) / D) * ((t1 + D) ^ 2 - t1 ^ 2) / 2
      + (a * ((t1 + D) ^ 2 - t1 ^ 2) / 2 + b * (t1 * D ^ 2 / 2 + D ^ 3 / 3)) = -(b * D ^ 3 / 12) := by
  field_simp; ring

-- MU-d: a tighter filling (false at the line)
theorem mg_bound_tight (f : ℝ) (h0 : 0 ≤ f) (h1 : f < 1) (h : 3 / 2 * f / (1 - f) ≤ 0.0354) : f ≤ 0.02 := by
  have hpos : 0 < 1 - f := by linarith
  rw [div_le_iff₀ hpos] at h
  nlinarith

-- MU-e: the runaway root negative (false)
theorem rel1_root_neg (K rho k : ℝ) (hK : 0 < K) (hr : 0 < rho) (hk : 0 < k) :
    (K * rho + Real.sqrt (K ^ 2 * rho ^ 2 + 4 * K * k)) / 2 < 0 := by
  nlinarith [Real.sqrt_nonneg (K ^ 2 * rho ^ 2 + 4 * K * k)]

end PAR1M

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
