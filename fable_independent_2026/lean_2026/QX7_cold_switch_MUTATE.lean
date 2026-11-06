import Mathlib

/-! QX7 MUTATE twin: three declared FALSE claims (each must fail; sorry marks the attempt). -/

-- FALSE 1: the lapse response is exactly linear
theorem mut_lapse_linear (Φ : ℝ) (h : 1 + Φ ≠ 0) : 1 / (1 + Φ) ^ 2 = 1 - 2 * Φ := by
  field_simp
  ring_nf
  sorry

-- FALSE 2: the dark-energy fraction can reach 1 at finite a
theorem mut_omega_ge_one (L B a : ℝ) (hL : 0 < L) (hB : 0 < B) (ha : 0 < a) : 1 ≤ L / (L + B / a ^ 3) := by
  rw [le_div_iff₀ (by positivity)]
  sorry

-- FALSE 3: the heating ratio decreases with m
theorem mut_heating_decreasing (x m m' : ℝ) (hx : 1 < x) (hm : m ≤ m') : x ^ m' ≤ x ^ m := by
  exact Real.rpow_le_rpow_of_exponent_le hx.le hm

#print axioms mut_lapse_linear
#print axioms mut_omega_ge_one
#print axioms mut_heating_decreasing
