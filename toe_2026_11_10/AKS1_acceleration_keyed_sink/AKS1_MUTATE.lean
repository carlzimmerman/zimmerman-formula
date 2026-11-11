/-
AKS1 false twin: each statement below is false and must fail to compile.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

open Real

/-- FALSE: the per-period bound without the coefficient C (fails for C > 1). -/
theorem aks1_false_period (Γ g v r c C : ℝ) (hv : 0 < v) (hr : 0 < r) (hc : 0 < c)
    (hg : g = v ^ 2 / r) (hΓ : Γ ≤ C * g / c) :
    Γ * (2 * π * r / v) ≤ 2 * π * v / c := by
  have hT : 0 < 2 * π * r / v := by positivity
  nlinarith

/-- FALSE: the terminal speed is c, whatever C is. -/
theorem aks1_false_terminal (g c C : ℝ) (hg : 0 < g) (hc : 0 < c) (hC : 0 < C) :
    g / (C * g / c) = c := by
  field_simp

/-- FALSE: with C = 1 and x <= 1/5 the sink reaches one e-fold over the age. -/
theorem aks1_false_age (x q : ℝ) (hx0 : 0 ≤ x) (hx : x ≤ 1 / 5) (hq0 : 0 ≤ q) (hq : q ≤ 33 / 200) :
    1 ≤ 1 * x * q := by
  nlinarith
