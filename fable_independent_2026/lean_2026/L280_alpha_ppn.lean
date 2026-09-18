import Mathlib

/-!
# L280 -- the clock host's preferred-frame parameters: exact identities

Foster-Jacobson (2006) Einstein-aether preferred-frame parameters
  α₁ = -8 (c₃² + c₁ c₄) / (2 c₁ - c₁² + c₃²),
  α₂ = α₁/2 - (c₁ + 2c₃ - c₄)(2c₁ + 3c₂ + c₃ + c₄) / ((c₁ + c₂ + c₃)(2 - c₁ - c₄)),
under the pipeline's map c₁ = K_B, c₃ = -K_B, c₄ = c₁₄ - K_B (so c₁₃ = 0 and c₁ + c₄ = c₁₄):
  1. α₁ = -4 c₁₄ exactly (K_B drops out);
  2. α₂ = c₁₄ [c₁₄ (1 + 2 c₂) - c₂] / [c₂ (2 - c₁₄)] exactly;
  3. α₂ = 0 ⟺ c₂ (1 - 2 c₁₄) = c₁₄, the equal-speed locus c₂ = c₁₄/(1 - 2c₁₄);
  4. the khronometric α₂ of Blas-Pujolàs-Sibiryakov 2011 (eq. 5.34) at β = 0, α = c₁₄, λ' = c₂ is (c₁₄/2)(c₁₄/c₂ - 1),
     and α₂(FJ) - α₂(BPS) = c₁₄² (c₁₄ + 3 c₂) / (2 c₂ (2 - c₁₄)), second order in c₁₄.
Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

noncomputable def alpha1FJ (c1 c3 c4 : ℝ) : ℝ := -8 * (c3 ^ 2 + c1 * c4) / (2 * c1 - c1 ^ 2 + c3 ^ 2)
noncomputable def alpha2FJ (c1 c2 c3 c4 : ℝ) : ℝ :=
  alpha1FJ c1 c3 c4 / 2 - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4) / ((c1 + c2 + c3) * (2 - c1 - c4))
noncomputable def alpha2closed (c14 c2 : ℝ) : ℝ := c14 * (c14 * (1 + 2 * c2) - c2) / (c2 * (2 - c14))
noncomputable def alpha2BPS (c14 c2 : ℝ) : ℝ := (c14 / 2) * (c14 / c2 - 1)

theorem alpha1_clock (KB c14 : ℝ) (hK : KB ≠ 0) : alpha1FJ KB (-KB) (c14 - KB) = -4 * c14 := by
  unfold alpha1FJ
  have h : (2 * KB - KB ^ 2 + (-KB) ^ 2) = 2 * KB := by ring
  rw [h, div_eq_iff (mul_ne_zero two_ne_zero hK)]; ring

theorem alpha2_clock (KB c14 c2 : ℝ) (hK : KB ≠ 0) (hc2 : c2 ≠ 0) (h2 : 2 - c14 ≠ 0) :
    alpha2FJ KB c2 (-KB) (c14 - KB) = alpha2closed c14 c2 := by
  unfold alpha2FJ alpha2closed
  rw [alpha1_clock KB c14 hK]
  have e1 : KB + c2 + -KB = c2 := by ring
  have e2 : 2 - KB - (c14 - KB) = 2 - c14 := by ring
  rw [e1, e2]
  field_simp
  ring

theorem alpha2_zero_locus (c14 c2 : ℝ) (h14 : c14 ≠ 0) (hc2 : c2 ≠ 0) (h2 : 2 - c14 ≠ 0) :
    alpha2closed c14 c2 = 0 ↔ c2 * (1 - 2 * c14) = c14 := by
  unfold alpha2closed
  rw [div_eq_zero_iff, mul_eq_zero, mul_eq_zero]
  constructor
  · rintro ((h | h) | (h | h))
    · exact absurd h h14
    · linarith
    · exact absurd h hc2
    · exact absurd h h2
  · intro h; left; right; linarith

theorem alpha2_FJ_minus_BPS (c14 c2 : ℝ) (hc2 : c2 ≠ 0) (h2 : 2 - c14 ≠ 0) :
    alpha2closed c14 c2 - alpha2BPS c14 c2 = c14 ^ 2 * (c14 + 3 * c2) / (2 * c2 * (2 - c14)) := by
  unfold alpha2closed alpha2BPS
  field_simp
  ring

#print axioms alpha1_clock
#print axioms alpha2_clock
#print axioms alpha2_zero_locus
#print axioms alpha2_FJ_minus_BPS
