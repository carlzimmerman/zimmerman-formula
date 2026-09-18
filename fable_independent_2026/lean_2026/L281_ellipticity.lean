import Mathlib

/-!
# L281 -- uniform ellipticity of the candidate's scalar operator for every field strength

The linearised static scalar operator (L279's law with the healing-length term) around a background gradient of
squared norm Y has spatial principal symbol
    σ(k) = J_Y (k∥² + k⊥²) + 2 J_YY Y k∥² + ξ² (k∥² + k⊥²)²
with the deep-MOND carrier J = β Y + (2/3) Y^{3/2}/ã₀, so J_Y = β + √Y/ã₀ and 2 Y J_YY = √Y/ã₀.  Certified:
  1. σ(k) − [β k² + ξ² k⁴] = (√Y/ã₀)(k⊥² + 2 k∥²), an identity;
  2. that remainder is ≥ 0, hence σ(k) ≥ β k² + ξ² k⁴;
  3. for k ≠ 0 and β > 0, σ(k) > 0: uniform ellipticity on every leaf for every Y ≥ 0.
Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

noncomputable def sigmaSym (Y β a0t ξ kpar kperp : ℝ) : ℝ :=
  (β + Real.sqrt Y / a0t) * (kpar ^ 2 + kperp ^ 2) + (Real.sqrt Y / a0t) * kpar ^ 2 + ξ ^ 2 * (kpar ^ 2 + kperp ^ 2) ^ 2

theorem sigma_identity (Y β a0t ξ kpar kperp : ℝ) :
    sigmaSym Y β a0t ξ kpar kperp - (β * (kpar ^ 2 + kperp ^ 2) + ξ ^ 2 * (kpar ^ 2 + kperp ^ 2) ^ 2)
      = (Real.sqrt Y / a0t) * (kperp ^ 2 + 2 * kpar ^ 2) := by
  unfold sigmaSym; ring

theorem sigma_lower_bound (Y β a0t ξ kpar kperp : ℝ) (ha : 0 < a0t) :
    β * (kpar ^ 2 + kperp ^ 2) + ξ ^ 2 * (kpar ^ 2 + kperp ^ 2) ^ 2 ≤ sigmaSym Y β a0t ξ kpar kperp := by
  have h := sigma_identity Y β a0t ξ kpar kperp
  have hnn : 0 ≤ (Real.sqrt Y / a0t) * (kperp ^ 2 + 2 * kpar ^ 2) :=
    mul_nonneg (div_nonneg (Real.sqrt_nonneg Y) (le_of_lt ha)) (by positivity)
  linarith

theorem sigma_pos (Y β a0t ξ kpar kperp : ℝ) (ha : 0 < a0t) (hβ : 0 < β) (hk : kpar ^ 2 + kperp ^ 2 ≠ 0) :
    0 < sigmaSym Y β a0t ξ kpar kperp := by
  have hk2 : 0 < kpar ^ 2 + kperp ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hk)
  have h1 : 0 < β * (kpar ^ 2 + kperp ^ 2) := mul_pos hβ hk2
  have h2 : 0 ≤ ξ ^ 2 * (kpar ^ 2 + kperp ^ 2) ^ 2 := by positivity
  have := sigma_lower_bound Y β a0t ξ kpar kperp ha
  linarith

#print axioms sigma_identity
#print axioms sigma_lower_bound
#print axioms sigma_pos
