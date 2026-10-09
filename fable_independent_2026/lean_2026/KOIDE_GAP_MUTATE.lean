import Mathlib

/-! MUTATE for KOIDE_GAP: both claims are FALSE and must fail.
(1) Koide ⇔ e1² = 4 e2 (the true coefficient is 6).
(2) a THREE-level spectrum is never at Koide (false: (2 - √3, 0, ...) aside, e.g. Koide triples exist). -/

theorem mutate_coeff (s1 s2 s3 : ℝ) (h : s1 + s2 + s3 ≠ 0) :
    (s1 ^ 2 + s2 ^ 2 + s3 ^ 2) / (s1 + s2 + s3) ^ 2 = 2 / 3 ↔
      (s1 + s2 + s3) ^ 2 = 4 * (s1 * s2 + s2 * s3 + s3 * s1) := by
  have hp : (s1 + s2 + s3) ^ 2 ≠ 0 := pow_ne_zero 2 h
  rw [div_eq_iff hp]
  constructor <;> intro hq <;> nlinarith [hq]

theorem mutate_three_level :
    ((0 : ℝ) ^ 2 + (3 - Real.sqrt 3) ^ 2 + (3 + Real.sqrt 3) ^ 2) / (0 + (3 - Real.sqrt 3) + (3 + Real.sqrt 3)) ^ 2 ≠ 2 / 3 := by
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  intro h; rw [div_eq_iff (by ring_nf; norm_num)] at h; nlinarith [h3]
