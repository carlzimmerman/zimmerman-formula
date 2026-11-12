/-
  OUT-5 MUTATE twin.  Every statement here is the FALSE version of a load-bearing
  OUT5 theorem.  The twin must FAIL TO COMPILE; if it compiles, the corresponding
  OUT5 theorem proves nothing.

    M1  muS_inv       with (1-mu)/mu = 2/u            (the true value is 1/u)
    M2  muS_slope     with mu' u / mu = 1/(1+u)^2     (the true value is 1/(1+u))
    M3  lawS_quadratic with u^2 = y (u + 2)           (the true law S is u^2 = y(u+1))
    M4  lawB_quadratic with y^2 + y = 2 u^2           (the true a0-line is y^2 + y = u^2)
    M5  muK_match     with mu_K^2 = 1/(r^2 L^2)       (the true match is 1/(r^2 L))
    M6  dust_cold_iff with 9 w0 <= a^3                (the true bound is 99 w0 <= a^3)
    M7  kappa_is_a_flat_direction, false version: the deep pinned density depends on a0
        (the true statement is that it does not) -- this is the claim OUT-5's G11 rests on

  TEST lane, quarantined.  Adopts nothing.  kappa = 1/2 FITTED; not theory closed.
-/

import Mathlib

noncomputable section

namespace OUT5M

def muS (u : ℝ) : ℝ := u / (1 + u)

-- M1: the enclosed-mass coefficient is 1/u, not 2/u.
theorem muS_inv_FALSE (u : ℝ) (hu : u ≠ 0) (h1 : 1 + u ≠ 0) :
    (1 - muS u) / muS u = 2 / u := by
  unfold muS
  field_simp [hu, h1]

-- M2: the gradient coefficient is 1/(1+u), not 1/(1+u)^2.
theorem muS_slope_FALSE (u : ℝ) (hu : u ≠ 0) (h1 : 1 + u ≠ 0) :
    (1 / (1 + u) ^ 2) * u / muS u = 1 / (1 + u) ^ 2 := by
  unfold muS
  field_simp [hu, h1]

-- M3: law S is u^2 = y (u + 1), not u^2 = y (u + 2).
theorem lawS_quadratic_FALSE (u : ℝ) (h1 : 1 + u ≠ 0) :
    (u ^ 2 / (1 + u)) * (u + 2) = u ^ 2 := by
  field_simp [h1]
  ring

-- M4: the a0-line is y^2 + y = u^2, not 2 u^2.
theorem lawB_quadratic_FALSE (u s : ℝ) (hsq : s ^ 2 = 1 + 4 * u ^ 2) :
    ((s - 1) / 2) ^ 2 + (s - 1) / 2 = 2 * u ^ 2 := by
  rw [show ((s - 1) / 2) ^ 2 + (s - 1) / 2 = (s ^ 2 - 1) / 4 by ring]
  rw [hsq]
  ring

-- M5: mu_K^match is 1/(r^2 L), not 1/(r^2 L^2).
theorem muK_match_FALSE (r L v : ℝ) (hr : r ≠ 0) (hL : L ≠ 0) :
    (1 / (r ^ 2 * L ^ 2)) * (v ^ 2 * L) = v ^ 2 / r ^ 2 := by
  field_simp [hr, hL]

-- M6: w <= 1/100 gives 99 w0 <= a^3, not 9 w0 <= a^3 being the tight statement.
--     (9 w0 <= a^3 is WEAKER, so it is provable; the FALSE claim is the converse
--      direction used as the lane's line: that 99 is not needed.  We assert the
--      stronger false form: w <= 1/100  <=>  w0 <= a^3 / 9 forces 99 w0 <= a^3 is FALSE.)
theorem dust_cold_FALSE (w0 a : ℝ) (hpos : 0 < w0 + a ^ 3) :
    w0 / (w0 + a ^ 3) ≤ (1 / 100 : ℝ) → 99 * w0 ≤ a ^ 3 / 99 := by
  intro hw
  rw [div_le_iff₀ hpos] at hw
  nlinarith

-- M7: the deep pinned density carries no a0.  The FALSE version says it is linear in a0.
def rhoPinDeepOf (dsg G : ℝ) (a0 : ℝ) : ℝ := dsg / (4 * Real.pi * G)

theorem kappa_is_a_flat_direction_FALSE (dsg G a0a a0b : ℝ) :
    rhoPinDeepOf dsg G a0a = a0a / a0b * rhoPinDeepOf dsg G a0b := by
  simp [rhoPinDeepOf]

end OUT5M
