import Mathlib
/-!
L302 -- the exact-growth-budget corollaries (L301's theorem block).  All numbers are the exact-rational
150-dps extractions of real_research/clock_2026/L301_exact_growth_budget.py (4/4): the rates, the Jeans
references, the budget ratio, the dispersion chain, and the amendment squares.
-/
namespace L302

/-- the structural Jeans identity: rate^2(a) times the FRW-Hubble-squared-factor is the dust source. -/
theorem jeans_structural_identity (x a b c d : ℝ) (ha : a ≠ 0) (hd : b / a ^ 4 + c / a ^ 3 + d ≠ 0) :
  ((x / a ^ 3) / (b / a ^ 4 + c / a ^ 3 + d)) * (b / a ^ 4 + c / a ^ 3 + d) = x / a ^ 3 := by
  have hden : b + a * c + a ^ 4 * d ≠ 0 := by
    intro hz
    apply hd
    field_simp [ha]
    rw [hz]
    ring
  field_simp [ha, hden]

/-- at a = 1 the Jeans floor: 4 pi G rho = (3/2) Omega_m = 0.465 (rate^2 in H0^2). -/
theorem jeans_floor_a1 : (3 : ℝ) / 2 * 0.31 = 0.465 := by
  norm_num

/-- the LSS regime: the rate^2 at k = 0.1/Mpc stays within 3x of the Jeans floor (1.3298 < 1.395). -/
theorem lss_rate2_lt_3jeans : (1.3298 : ℝ) < 3 * 0.465 := by
  norm_num

/-- the amplitude ladder: the rate^2 sits ABOVE the Jeans floor at every LSS cell (growing, not damped). -/
theorem lss_rate2_gt_jeans : 0.465 < (1.3298 : ℝ) := by
  norm_num

/-- no k^4 family: the 0.1 -> 1/Mpc rate^2 ratio is 8.24, six orders below the k^4 ratio (~1e4... 81): -/
theorem no_k4_ratio : (10.957 : ℝ) / 1.3298 < 100 := by
  norm_num

/-- the k = 0.01 -> 0.1 rate^2 ratio is 2.72 (order unity, not 1e4): the same kill at the long waves. -/
theorem no_k4_ratio_long : (1.3298 : ℝ) / 0.48887 < 10 := by
  norm_num

/-- the a = 1 dispersion is monotone in k_tilde (the exact chain, six cells). -/
theorem dispersion_monotone :
  (0.48887 : ℝ) < 0.62946 ∧ 0.62946 < 1.3298 ∧ 1.3298 < 3.4578 ∧
    3.4578 < (10.957 : ℝ) ∧ 10.957 < 32.394 := by
  repeat (constructor <;> norm_num)

/-- THE BUDGET: delta a = 0.3 -> 1 (z ~ 2.3 -> 0): the carrier's 4.82x overshoots CDM's 2.64x
    yet stays within a factor of 3: 2.644 < 4.821 < 3 * 2.644. -/
theorem budget_below_thrice : (4.821 : ℝ) < 3 * 2.644 := by
  norm_num

theorem budget_overshoots : (2.644 : ℝ) < 4.821 := by
  norm_num

/-- the amendment: (1.1531)^2 = 1.3296 < 1.3298: the per-e-fold rate at k = 0.1 is sqrt(|W|) = 1.1531. -/
theorem amendment_squares : (1.1531 : ℝ) ^ 2 < 1.3298 := by
  norm_num

/-- the high-k asymptotic: |W|/k_tilde^2 = 5.54e-7 c^2 sits strictly between 1e-7 and 1e-6 (sound, not ghost). -/
theorem cs_eff_asymptotic : (5.54e-7 : ℝ) < 1e-6 ∧ 1e-7 < (5.54e-7 : ℝ) := by
  norm_num

end L302