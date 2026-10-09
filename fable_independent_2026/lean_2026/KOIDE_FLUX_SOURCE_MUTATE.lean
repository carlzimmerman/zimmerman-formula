import Mathlib

/-! MUTATE for KOIDE_FLUX_SOURCE: both claims are FALSE and must fail.
(1) the Farey bound strengthened to N ≥ b + d + 1 (the mediant n = a + c, N = b + d violates it).
(2) the Koide-branch bound raised to 113089 (the mediant 11999/113088 sits inside the interval). -/

theorem mutate_farey (a b c d n N : ℤ) (hb : 0 < b) (hd : 0 < d) (hN : 0 < N)
    (hdet : b * c - a * d = 1) (h1 : a * N < n * b) (h2 : n * d < c * N) : b + d + 1 ≤ N := by
  have e : N = b * (c * N - d * n) + d * (n * b - a * N) := by linear_combination (-N) * hdet
  have i1 : 1 ≤ c * N - d * n := by linarith
  have i2 : 1 ≤ n * b - a * N := by linarith
  nlinarith

theorem mutate_mediant_outside :
    ¬ ((0.6666661401 : ℝ) ≤ 2 * Real.pi * 11999 / 113088 ∧ 2 * Real.pi * 11999 / 113088 ≤ 0.6666661425) := by
  have pl := Real.pi_gt_d20; have pu := Real.pi_lt_d20
  rintro ⟨h1, h2⟩; norm_num at *; nlinarith
