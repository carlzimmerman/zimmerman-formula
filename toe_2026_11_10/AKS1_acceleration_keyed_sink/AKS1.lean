/-
AKS1 (TOE swing follow-up, 2026-11-10): the acceleration-keyed sink's rate bounds.

Gamma(A) = (a0/c) f(|A|/a0). With f(x) <= C x and a standing clock (|A| = g = v^2/r), the sink's
e-folds per period T = 2 pi r/v are at most 2 pi C v/c: Theorem 8's c/v, in a rate. A damped,
unsupported shell falls at the terminal speed g/Gamma = c/C. A free-falling clock (A = 0, f(0) = 0)
has no sink at all. With C = 1 and x <= 1/5, the e-folds over the age (a0 t0/c <= 0.165) stay below 1/30.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

open Real

/-- Per-period bound: Gamma <= C g/c, g = v^2/r, T = 2 pi r/v gives Gamma T <= 2 pi C v/c. -/
theorem aks1_period_bound (Γ g v r c C : ℝ) (hv : 0 < v) (hr : 0 < r) (hc : 0 < c)
    (hg : g = v ^ 2 / r) (hΓ : Γ ≤ C * g / c) :
    Γ * (2 * π * r / v) ≤ 2 * π * C * v / c := by
  have hT : 0 < 2 * π * r / v := by positivity
  have h1 : Γ * (2 * π * r / v) ≤ (C * g / c) * (2 * π * r / v) :=
    mul_le_mul_of_nonneg_right hΓ hT.le
  have h2 : (C * g / c) * (2 * π * r / v) = 2 * π * C * v / c := by
    rw [hg]; field_simp
  linarith [h1, h2.le, h2.ge]

/-- Terminal speed of a damped, unsupported shell: g/Gamma = c/C when Gamma = C g/c. -/
theorem aks1_terminal_speed (g c C : ℝ) (hg : 0 < g) (hc : 0 < c) (hC : 0 < C) :
    g / (C * g / c) = c / C := by
  field_simp

/-- A free-falling clock carries no sink: A = 0 and f(0) = 0 give Gamma = 0. -/
theorem aks1_freefall_off (a0 c : ℝ) (f : ℝ → ℝ) (hf : f 0 = 0) :
    (a0 / c) * f (0 / a0) = 0 := by
  simp [hf]

/-- Over the age: with C = 1, x <= 1/5 and a0 t0/c <= 33/200, the e-folds C x (a0 t0/c) stay below 1/30. -/
theorem aks1_age_efolds (x q : ℝ) (hx0 : 0 ≤ x) (hx : x ≤ 1 / 5) (_hq0 : 0 ≤ q) (hq : q ≤ 33 / 200) :
    1 * x * q < 1 / 30 := by
  nlinarith
