import Mathlib
namespace SignedShell

/-- For a0=1, the signed radial flux is g |g|/(1+|g|).
A two-atom mean with inward radial components violates the algebraic
extension of SV1's shell bound. This is not a constructed PDE solution. -/
theorem signed_shell_counterexample :
    let mean : ℝ := (99/100) * 1 + (1/100) * (-50)
    let flux : ℝ := (99/100) * (1 * |(1:ℝ)| / (1+|(1:ℝ)|)) +
      (1/100) * ((-50) * |(-50:ℝ)| / (1+|(-50:ℝ)|))
    0 < mean ∧ 0 < flux ∧ flux < mean^2 / (1+mean) := by
  norm_num

end SignedShell
#print axioms SignedShell.signed_shell_counterexample
