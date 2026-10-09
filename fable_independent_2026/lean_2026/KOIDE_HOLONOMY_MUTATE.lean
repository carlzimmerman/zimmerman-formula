import Mathlib

/-! MUTATE for KOIDE_HOLONOMY: both claims are FALSE and must fail.
(1) a single link amplitude is gauge invariant (only the ring product is).
(2) the octant flux with g = 1/2 hits the Koide target within 0.01. -/

theorem mutate_single_link (c d0 d1 : ℂ) (h0 : d0 ≠ 0) (h1 : d1 ≠ 0) : d0 * c / d1 = c := by
  field_simp

theorem mutate_octant_hits : |(1 / 2 : ℝ) * (Real.pi / 2) - 0.666666141| < 0.01 := by
  have := Real.pi_gt_d2; rw [abs_lt]; constructor <;> norm_num at this ⊢ <;> linarith
