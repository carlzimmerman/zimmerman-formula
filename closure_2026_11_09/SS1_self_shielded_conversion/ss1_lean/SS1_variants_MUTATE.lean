/-
SS1 variants B-G (AMENDMENT_A2 2b866ef57a): Lean statements for the Hill-4 switch. They certify the switch, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

F x u = -log u + x^4/4 (1 - u^4). Retention f at time alpha is the root of F x f = alpha.
  * hasDerivAt_F       : dF/du = -(1 + (x u)^4)/u           (u > 0)
  * closed_form_solves : if F x (y t) = t along a differentiable y > 0, then y' = -y/(1 + (x y)^4)
  * half_retention     : F x (1/2) = alpha  <->  x^4 = (64/15)(alpha - log 2)
  * retention_mono     : the root is monotone in x0
  * bound_195          : x0 >= 1.95, alpha = 3.80  ->  f > 0.249
  * bound_32           : x0 >= 3.2,  alpha = 3.80  ->  f > 0.958
(The third bound in the relayed list, f < 0.0235 for x0 <= 0.65, is checked numerically in parts/v_ka.json; it needs
exp(3.7554) > 42.55, which is not formalised here.)
-/
import Mathlib

namespace SS1VM

noncomputable def F (x u : ℝ) : ℝ := -Real.log u + x ^ 4 / 4 * (1 - u ^ 4)

/-- MUTATE: half-retention with the wrong constant 64/16. Must NOT compile. -/
theorem half_retention_wrong (x α : ℝ) : F x (1 / 2) = α ↔ x ^ 4 = 64 / 16 * (α - Real.log 2) := by
  have hl : Real.log (1 / 2 : ℝ) = -Real.log 2 := by rw [one_div, Real.log_inv]
  unfold F; rw [hl]
  constructor <;> intro h <;> nlinarith

end SS1VM
