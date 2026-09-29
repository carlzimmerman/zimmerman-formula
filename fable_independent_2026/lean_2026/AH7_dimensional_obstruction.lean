import Mathlib

/-!
# AH7 -- Lean certificate for the dimensional obstruction (AH5)

A monomial c^a G^b Lambda^d hbar^f (e^2)^g (rational exponents; Gaussian e^2 has dimension energy x length) is dimensionless iff the three
base-dimension equations hold.  With dimension exponents (M, L, T):
  c (0, 1, -1),  G (-1, 3, -2),  Lambda (0, -2, 0),  hbar (1, 2, -1),  e^2 (1, 3, -2).

CERTIFIED (mathematics only):
* `general_solution`: the dimensionless monomials are EXACTLY the rational combinations p * v1 + q * v2 with
  v1 = (c^-3 G Lambda hbar) = Lambda l_P^2 = x  and  v2 = (c^-4 G Lambda e^2).
* `no_dimensionless_from_c_G_Lambda`: with no hbar and no charge, the only dimensionless monomial is the trivial one.
* `gravity_hbar_is_power_of_x`: with hbar but no charge, every dimensionless monomial is a power of x = Lambda G hbar / c^3.
* `alpha_dimensionless`, `alpha_is_v2_minus_v1`: alpha = e^2/(hbar c) is dimensionless and equals v2 - v1, i.e. (Lambda G e^2/c^4)/(Lambda G hbar/c^3).
* `alpha_not_power_of_x`: alpha is not a power of x (the charge exponent is 1, a power of x has charge exponent 0).
NOT CERTIFIED: that (c, G, Lambda, hbar, e^2) are the only relevant inputs, or that no new principle could relate e to the gravity group;
this is a statement about monomials in these constants, not about physics.  Lean does not derive alpha.  Zero sorry; axioms printed below.
-/

/-- the three base-dimension equations (M, L, T) for c^a G^b Lambda^d hbar^f (e^2)^g -/
def dimless (a b d f g : ℚ) : Prop :=
  (-b + f + g = 0) ∧ (a + 3 * b - 2 * d + 2 * f + 3 * g = 0) ∧ (-a - 2 * b - f - 2 * g = 0)

theorem general_solution (a b d f g : ℚ) :
    dimless a b d f g ↔ ∃ p q : ℚ, a = -3 * p - 4 * q ∧ b = p + q ∧ d = p + q ∧ f = p ∧ g = q := by
  constructor
  · rintro ⟨hM, hL, hT⟩
    refine ⟨f, g, ?_, ?_, ?_, rfl, rfl⟩ <;> linarith
  · rintro ⟨p, q, ha, hb, hd, hf, hg⟩
    subst ha hb hd hf hg
    refine ⟨?_, ?_, ?_⟩ <;> ring

theorem no_dimensionless_from_c_G_Lambda (a b d : ℚ) (h : dimless a b d 0 0) : a = 0 ∧ b = 0 ∧ d = 0 := by
  obtain ⟨hM, hL, hT⟩ := h
  refine ⟨?_, ?_, ?_⟩ <;> linarith

theorem gravity_hbar_is_power_of_x (a b d f : ℚ) (h : dimless a b d f 0) :
    ∃ p : ℚ, a = -3 * p ∧ b = p ∧ d = p ∧ f = p := by
  obtain ⟨hM, hL, hT⟩ := h
  refine ⟨f, ?_, ?_, ?_, rfl⟩ <;> linarith

theorem alpha_dimensionless : dimless (-1) 0 0 (-1) 1 := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num

theorem alpha_is_v2_minus_v1 :
    ((-1 : ℚ), (0 : ℚ), (0 : ℚ), (-1 : ℚ), (1 : ℚ)) =
      ((-4 : ℚ) - (-3), (1 : ℚ) - 1, (1 : ℚ) - 1, (0 : ℚ) - 1, (1 : ℚ) - 0) := by
  norm_num

theorem alpha_not_power_of_x :
    ¬ ∃ p : ℚ, ((-1 : ℚ), (0 : ℚ), (0 : ℚ), (-1 : ℚ), (1 : ℚ)) = (-3 * p, p, p, p, (0 : ℚ)) := by
  rintro ⟨p, h⟩
  have h5 := congrArg (fun t => t.2.2.2.2) h
  simp at h5

#print axioms general_solution
#print axioms no_dimensionless_from_c_G_Lambda
#print axioms gravity_hbar_is_power_of_x
#print axioms alpha_dimensionless
#print axioms alpha_is_v2_minus_v1
#print axioms alpha_not_power_of_x
