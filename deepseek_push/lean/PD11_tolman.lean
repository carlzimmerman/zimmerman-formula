/-
  PD11 -- THE TOLMAN FACE: the third appearance of the two, from exact GR.

  The vacuum's ACTIVE gravitational density -- the density that sources the
  acceleration equation (the Tolman/Komar density) -- is

      rho_active = rho + 3p/c^2 = rho (1 + 3w),

  the standard GR identity (it is the source of the Friedmann ACCELERATION
  equation: ddot a/a = -(4 pi G/3) rho (1 + 3w)).  For the vacuum's
  equation of state w = -1 (the corpus's certified stage-17 vacuum):

      rho_active = -2 rho.

  The magnitude is EXACTLY TWO -- the third independent appearance of the
  count: the metric's two channels (computed, PD01/PD02), the equilibrium's
  kinetic half (Lean, G03G), and now the Tolman factor |1 + 3w| = 2 (exact
  GR).  Certified here as pure algebra.

  AND THE DIMENSION TENSION, recorded: in d spatial dimensions the Tolman
  factor is |1 - d| = d - 1 at w = -1 -- d-DEPENDENT, while the channel
  count is dimension-INVARIANT at 2 (PD02).  Both give 2 in our d = 3; the
  coincidence is our universe's.  Recorded, not resolved.
-/

import Mathlib

/-- **T1** -- the active gravitational density of a perfect fluid with
equation-of-state parameter `w` (p = w rho c^2): the Tolman density
`rho (1 + 3w)` -- the source of the Friedmann acceleration equation. -/
theorem tolman_density {rho p c w : ℝ} (hc : c ≠ 0) (h : p = w * rho * c^2) :
    rho + 3 * p / c^2 = rho * (1 + 3 * w) := by
  subst h
  field_simp

/-- **T2** -- the vacuum (w = -1): the active gravitational density is
EXACTLY minus twice the energy density. -/
theorem vacuum_tolman {rho c : ℝ} (hc : c ≠ 0) :
    rho + 3 * (-(rho * c^2)) / c^2 = -(2 * rho) := by
  have hc2 : c^2 ≠ 0 := pow_ne_zero 2 hc
  field_simp [hc2]
  norm_num

/-- **T3** -- the Tolman factor's magnitude at w = -1 is exactly two: the
third face of the count. -/
theorem tolman_factor_two {rho c : ℝ} (hρ : rho ≠ 0) (hc : c ≠ 0) :
    |(rho + 3 * (-(rho * c^2)) / c^2) / rho| = 2 := by
  rw [vacuum_tolman hc]
  field_simp [hρ]
  norm_num

/-- **T4** -- THE DIMENSION TENSION, as an algebraic fact: in d spatial
dimensions the Tolman factor at w = -1 is |1 - d| = d - 1 -- it COUNTS
d - 1, while the channel count is dimension-INVARIANT at 2 (PD02).  Both
give 2 exactly at d = 3; the two readings separate for d ≠ 3 (3 at d = 4). -/
theorem tolman_signed (d : ℕ) : (1 : ℤ) + (d : ℤ) * (-1 : ℤ) = 1 - (d : ℤ) := by ring

theorem tolman_two_at_three : |((1 : ℤ) + (3 : ℤ) * (-1 : ℤ))| = 2 := by norm_num

theorem tolman_three_at_four : |((1 : ℤ) + (4 : ℤ) * (-1 : ℤ))| = 3 := by norm_num
