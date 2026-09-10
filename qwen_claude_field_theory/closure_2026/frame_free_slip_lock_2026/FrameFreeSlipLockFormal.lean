import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Kernel certificate for the fixed curvature-coupling ray.

The geometric calculation in `nonlocal_door/ghost_theorem_lensing.py` gives
the quasi-static curvature direction v=(-2,4).  A healthy frame-free mode with
positive inverse kernel L contributes -L*v*vᵀ.  The theorems below verify the
resulting response algebra without assuming an expected slip or enhancement.
-/

namespace FrameFreeSlipLock

noncomputable section

def phi (L m rho : ℝ) : ℝ := rho * (8 * L + m) / (2 * m * (6 * L + m))
def psi (L m rho : ℝ) : ℝ := rho * (4 * L + m) / (2 * m * (6 * L + m))

theorem denominators_positive (L m : ℝ) (hL : 0 < L) (hm : 0 < m) :
    0 < 2 * m * (6 * L + m) := by positivity

theorem locked_response_solves
    (L m rho : ℝ) (hL : 0 < L) (hm : 0 < m) :
    (-4 * L) * phi L m rho + (2 * m + 8 * L) * psi L m rho = rho ∧
      (2 * m + 8 * L) * phi L m rho + (-2 * m - 16 * L) * psi L m rho = 0 := by
  have hden : 2 * m * (6 * L + m) ≠ 0 :=
    ne_of_gt (denominators_positive L m hL hm)
  constructor <;> dsimp [phi, psi] <;> field_simp [hden] <;> ring

theorem slip_ratio_formula
    (L m rho : ℝ) (hL : 0 < L) (hm : 0 < m) (hrho : rho ≠ 0) :
    psi L m rho / phi L m rho = (4 * L + m) / (8 * L + m) := by
  have h8 : 8 * L + m ≠ 0 := by positivity
  have h6 : 6 * L + m ≠ 0 := by positivity
  have h2m : 2 * m ≠ 0 := by positivity
  have h4 : 4 * L + m ≠ 0 := by positivity
  dsimp [phi, psi]
  field_simp [h8, h6, h2m, h4, hrho]

theorem slip_is_not_one (L m : ℝ) (hL : 0 < L) (hm : 0 < m) :
    (4 * L + m) / (8 * L + m) ≠ 1 := by
  have hden : 8 * L + m ≠ 0 := by positivity
  intro h
  field_simp [hden] at h
  nlinarith

theorem enhancement_is_strict (L m : ℝ) (hL : 0 < L) (hm : 0 < m) :
    1 < (8 * L + m) / (6 * L + m) := by
  have hden : 0 < 6 * L + m := by positivity
  apply (lt_div_iff₀ hden).2
  nlinarith

end
end FrameFreeSlipLock
