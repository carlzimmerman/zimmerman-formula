import Mathlib

/-! MUTATE for KOIDE_TRIALITY_45: both claims below are FALSE and must fail to compile.
(1) the descent's mod-3 step with 3 replaced by 2: a^2 + c^2 = 2(b^2+d^2) has (1,1,1,0), so the mod-2
    analogue of `zmod3_sum_sq` must fail.
(2) the GO without unit-normalising the root (b = √2 instead of √2/2) must NOT give Q = 2/3. -/

theorem mutate_mod2 : ∀ a c : ZMod 2, a ^ 2 + c ^ 2 = 0 → a = 0 ∧ c = 0 := by decide

theorem mutate_unnormalised :
    let a := Real.sqrt 3 / 3
    let b := Real.sqrt 2
    ((a + b) ^ 2 + a ^ 2 + (a - b) ^ 2) / ((a + b) + a + (a - b)) ^ 2 = 2 / 3 := by
  intro a b
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hnum : (a + b) ^ 2 + a ^ 2 + (a - b) ^ 2 = 2 := by
    simp only [a, b]; linear_combination (1 / 3 : ℝ) * h3 + (1 / 2 : ℝ) * h2
  have hden : ((a + b) + a + (a - b)) ^ 2 = 3 := by
    simp only [a]; linear_combination h3
  rw [hnum, hden]
