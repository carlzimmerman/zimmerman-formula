import Mathlib

/-! SV5 MUTATE twin: four declared FALSE claims (each must fail; sorry marks the attempt). -/

open scoped RealInnerProductSpace

noncomputable def nuS (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)

-- FALSE 1: the law-on power bound with (m + 1)^2 in place of m^2
theorem mut_power_bound {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] (g gN : E) (m : ℝ)
    (hm : 0 ≤ m) (h : m * ‖gN‖ ^ 2 ≤ ⟪g, gN⟫) : (m + 1) ^ 2 * ‖gN‖ ^ 2 ≤ ‖g‖ ^ 2 := by
  have hcs : ⟪g, gN⟫ ≤ ‖g‖ * ‖gN‖ := real_inner_le_norm g gN
  nlinarith [norm_nonneg g, norm_nonneg gN]

-- FALSE 2: nu increases with y
theorem mut_nu_monotone (y1 y2 : ℝ) (h1 : 0 < y1) (h12 : y1 ≤ y2) : nuS y1 ≤ nuS y2 := by
  unfold nuS
  have : 1 / y2 ≤ 1 / y1 := one_div_le_one_div_of_le h1 h12
  linarith [Real.sqrt_le_sqrt (by linarith : 1 / 4 + 1 / y2 ≤ 1 / 4 + 1 / y1)]

-- FALSE 3: the host requirement transfers to an arbitrary epoch (no image hypothesis)
theorem mut_stiff_anywhere (F r : ℝ → ℝ) (ZH : Set ℝ) (L z' : ℝ) (hH : ∀ z ∈ ZH, L ≤ F (r z)) :
    L ≤ F (r z') := by
  sorry

-- FALSE 4: an antitone switch makes the more-charged web SOFTER than the host
theorem mut_switch_reversed (mu : ℝ → ℝ) (hmu : Antitone mu) (sh sw : ℝ) (h : sh ≤ sw) : mu sh ≤ mu sw := by
  exact hmu h

#print axioms mut_power_bound
#print axioms mut_nu_monotone
#print axioms mut_stiff_anywhere
#print axioms mut_switch_reversed
