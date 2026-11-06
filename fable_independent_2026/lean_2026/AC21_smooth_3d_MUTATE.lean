/-
AC21 MUTATE twin: four planted FALSE claims (each must fail), plus one true sanity claim (must pass).
Kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace AC21M

/-- FALSE: the AC20 contact form (m = 4) has an H^s window in 3D. -/
theorem m4_ok_3d : 3 + 2 < 4 := by norm_num

/-- FALSE: B >= s without F' >= 0. -/
theorem B_ge_s_any (γ s F1 F2 : ℝ) (hγ : 0 ≤ γ) (hs : 0 ≤ s) :
    s ≤ (1 + γ * (F1 - s * F2) / 2) * s + (F2 * γ / 2) * s ^ 2 := by
  nlinarith [sq_nonneg s]

/-- FALSE: the winner's B is negative. -/
theorem winner_B_neg : (3165142806 / 44610575 : ℚ) < 0 := by norm_num

/-- FALSE: FRW exactness when the background sits below the knot (b > 2X). -/
theorem frw_exact_bad (F : ℝ → ℝ) (γ b X : ℝ) (hF : ∀ P, b ≤ P → F P = γ / 2 * P ^ 2) :
    F (2 * X) = γ / 2 * (2 * X) ^ 2 := by
  exact hF _ (by linarith)

/-- TRUE sanity: the 1D window for m = 4. -/
theorem m4_ok_1d : 1 + 2 < 4 := by norm_num

end AC21M
