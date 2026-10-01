import Mathlib
import Mathlib.Tactic

noncomputable section

def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2

-- attempt A: fun_prop + deriv
example (u : ℝ) (hu : 1 + u ≠ 0) : deriv mu2 u = 2 / (1 + u)^3 := by
  unfold mu2
  fun_prop

-- attempt B: HasDerivAt chain
example (u : ℝ) (hu : 1 + u ≠ 0) : HasDerivAt mu2 (2 / (1 + u)^3) u := by
  unfold mu2
  convert ((hasDerivAt_id u).add_const 2).mul ?_ using 1
  sorry

-- attempt C: simp with deriv rules
example (u : ℝ) (hu : 1 + u ≠ 0) : deriv (fun x : ℝ => 1 - (1 + x)⁻¹ ^ 2) u = 2 * (1 + u)⁻³ := by
  simp [deriv_const_sub, deriv_inv, hu]
  ring

end
