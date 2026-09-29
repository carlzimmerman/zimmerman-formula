import Mathlib
/-!
# AH7 MUTATE control -- the certificates must have power.
(1)-(3): deliberately FALSE variants closed with the same tactics; each must FAIL to compile.
(4): positive control -- allowing a charge exponent DOES admit a second independent group, so 'nullity 1 even with charge' is false;
     the true two-parameter statement compiles.
Expected: errors at (1), (2), (3); (4) compiles.  Run: lake env lean AH7_dimensional_obstruction_MUTATE.lean
-/
def dimless (a b d f g : ℚ) : Prop :=
  (-b + f + g = 0) ∧ (a + 3 * b - 2 * d + 2 * f + 3 * g = 0) ∧ (-a - 2 * b - f - 2 * g = 0)

-- (1) FALSE: wrong coefficient of q in the exponent of c
theorem mutate1 (a b d f g : ℚ) :
    dimless a b d f g ↔ ∃ p q : ℚ, a = -3 * p - 3 * q ∧ b = p + q ∧ d = p + q ∧ f = p ∧ g = q := by
  constructor
  · rintro ⟨hM, hL, hT⟩
    refine ⟨f, g, ?_, ?_, ?_, rfl, rfl⟩ <;> linarith
  · rintro ⟨p, q, ha, hb, hd, hf, hg⟩
    subst ha hb hd hf hg
    refine ⟨?_, ?_, ?_⟩ <;> ring

-- (2) FALSE: with hbar but no charge the Lambda exponent is 2p, not p
theorem mutate2 (a b d f : ℚ) (h : dimless a b d f 0) :
    ∃ p : ℚ, a = -3 * p ∧ b = p ∧ d = 2 * p ∧ f = p := by
  obtain ⟨hM, hL, hT⟩ := h
  refine ⟨f, ?_, ?_, ?_, rfl⟩ <;> linarith

-- (3) FALSE: alpha IS a power of x
theorem mutate3 :
    ∃ p : ℚ, ((-1 : ℚ), (0 : ℚ), (0 : ℚ), (-1 : ℚ), (1 : ℚ)) = (-3 * p, p, p, p, (0 : ℚ)) := by
  refine ⟨1, ?_⟩
  norm_num

-- (4) POSITIVE CONTROL: the two-parameter family really is dimensionless for every p, q (compiles)
theorem control_two_parameter_family (p q : ℚ) :
    dimless (-3 * p - 4 * q) (p + q) (p + q) p q := by
  refine ⟨?_, ?_, ?_⟩ <;> ring
