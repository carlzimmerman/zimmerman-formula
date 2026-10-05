import Mathlib

/-!
# CFG337 -- sign / positivity certificates for the inverted-symmetron switch

The decisive inequalities behind CFG337's quadratic-action verdict:

* `kin_pos_def` / `kin_ghost` : the kinetic matrix diag(rho, eps) is positive definite for rho > 0, eps > 0,
  and NOT for eps = -1 (the MUTATE ghost).
* `dispersion_bounded` : with the switch field dynamical (gradient energy, mass M^2 > 0) the deficit term is
  bounded, a k^2/(k^2+M^2) <= a, so omega^2 is bounded below uniformly in k (Hadamard well-posed).
* `slaved_unbounded` : in the slaved (prescribed-gate) limit, c_gate^2 > c_s^2 makes k^2 (c_s^2 - c_gate^2)
  unbounded below (the DE12 Hadamard failure).
* `extra_growth_max` : the exact maximum of the switch-induced growth, a q/(q+M^2) - c_e^2 q <= M^2 (c_g - c_e)^2
  with a = c_g^2 M^2.
* `trigger_concave_stiffness` : the trigger T(U) = 1 - 1/U has T'' = -2/U^3 < 0, so its direct baryon stiffness
  -(1/2) mu0^2 T'' sigma^2 is >= 0.
* `frw_mass_pos` : on FRW (U < 1, B = O(delta^3) absent at quadratic order) the symmetric-phase mass is positive.
* `transition_obstruction` (+ numeric instances) : if the switch length is <= ell_loc < ell_min, the extra growth
  exceeds the gravitational rate.
-/

/-- Kinetic matrix diag(rho, eps) is positive definite. -/
theorem kin_pos_def (rho eps : ℝ) (hr : 0 < rho) (he : 0 < eps) (x y : ℝ) (hxy : x ≠ 0 ∨ y ≠ 0) :
    0 < rho * x ^ 2 + eps * y ^ 2 := by
  rcases hxy with h | h
  · have : 0 < x ^ 2 := by positivity
    have : 0 ≤ eps * y ^ 2 := by positivity
    nlinarith
  · have : 0 < y ^ 2 := by positivity
    have : 0 ≤ rho * x ^ 2 := by positivity
    nlinarith

/-- MUTATE: with the switch kinetic sign flipped (eps = -1) the kinetic form takes a negative value: a ghost. -/
theorem kin_ghost (rho : ℝ) : ∃ x y : ℝ, rho * x ^ 2 + (-1) * y ^ 2 < 0 :=
  ⟨0, 1, by norm_num⟩

/-- Dynamical switch: the deficit a k^2/(k^2+M^2) never exceeds a (bounded below => Hadamard well-posed). -/
theorem dispersion_bounded (a q M2 cs2 : ℝ) (ha : 0 ≤ a) (hq : 0 ≤ q) (hM : 0 < M2) (hc : 0 ≤ cs2) :
    -a ≤ cs2 * q - a * q / (q + M2) := by
  have hpos : 0 < q + M2 := by linarith
  have h1 : a * q / (q + M2) ≤ a := by
    rw [div_le_iff₀ hpos]; nlinarith
  have h2 : 0 ≤ cs2 * q := mul_nonneg hc hq
  linarith

/-- Slaved (prescribed-gate) limit: c_gate^2 > c_s^2 gives omega^2 = k^2 (c_s^2 - c_gate^2) unbounded below. -/
theorem slaved_unbounded (cs2 cg2 : ℝ) (h : cs2 < cg2) (K : ℝ) :
    ∃ q : ℝ, 0 ≤ q ∧ q * (cs2 - cg2) < -K := by
  refine ⟨(|K| + 1) / (cg2 - cs2), ?_, ?_⟩
  · apply div_nonneg <;> [positivity; linarith]
  · have hd : 0 < cg2 - cs2 := by linarith
    have : (|K| + 1) / (cg2 - cs2) * (cs2 - cg2) = -(|K| + 1) := by
      field_simp; ring
    rw [this]; have := le_abs_self K; have := neg_abs_le K; linarith

/-- Exact maximum of the switch-induced growth rate^2 over q = k^2 >= 0. -/
theorem extra_growth_max (cg ce M2 q : ℝ) (hM : 0 < M2) (hq : 0 ≤ q) :
    cg ^ 2 * M2 * q / (q + M2) - ce ^ 2 * q ≤ M2 * (cg - ce) ^ 2 := by
  have hpos : 0 < q + M2 := by linarith
  have key : cg ^ 2 * M2 * q - ce ^ 2 * q * (q + M2) ≤ M2 * (cg - ce) ^ 2 * (q + M2) := by
    nlinarith [sq_nonneg (q * ce - M2 * (cg - ce))]
  have : cg ^ 2 * M2 * q / (q + M2) - ce ^ 2 * q
      = (cg ^ 2 * M2 * q - ce ^ 2 * q * (q + M2)) / (q + M2) := by
    field_simp
  rw [this, div_le_iff₀ hpos]; linarith

/-- The trigger T(U) = 1 - 1/U is concave (T'' = -2/U^3), so the direct baryon stiffness is non-negative. -/
theorem trigger_concave_stiffness (mu0 U s : ℝ) (hU : 0 < U) (hs : 0 ≤ s) :
    0 ≤ -(1 / 2) * mu0 ^ 2 * (-2 / U ^ 3) * s := by
  have : 0 < U ^ 3 := by positivity
  have : -(1 / 2) * mu0 ^ 2 * (-2 / U ^ 3) * s = mu0 ^ 2 * s / U ^ 3 := by field_simp
  rw [this]; positivity

/-- FRW / OFF side: for 0 < U < 1 the symmetric-phase mass mu0^2 (1/U - 1) is positive. -/
theorem frw_mass_pos (mu0 U : ℝ) (hm : 0 < mu0) (hU : 0 < U) (h1 : U < 1) :
    0 < mu0 ^ 2 * (1 / U - 1) := by
  have : 1 < 1 / U := by rw [lt_div_iff₀ hU]; linarith
  have : 0 < mu0 ^ 2 := by positivity
  nlinarith

/-- Transition obstruction: with switch length ell <= ell_loc < X / Gamma, the extra growth X / ell exceeds Gamma. -/
theorem transition_obstruction (X Γ ell ell_loc : ℝ) (hΓ : 0 < Γ) (hl : 0 < ell)
    (hle : ell ≤ ell_loc) (hlt : ell_loc < X / Γ) : Γ < X / ell := by
  have h1 : ell < X / Γ := lt_of_le_of_lt hle hlt
  have hX : 0 < X := by
    have : 0 < X / Γ := lt_trans hl h1
    exact (div_pos_iff_of_pos_right hΓ).mp this
  rw [lt_div_iff₀ hl]
  rw [lt_div_iff₀ hΓ] at h1
  linarith

/-- Numeric instances (kpc, floors of CFG337's committed ell_min): the 100 kpc tolerance is below every legal ell_min.
C1 lenient 2865, C2 lenient 182, C2 single-constant E_c 29051. -/
theorem ell_min_instances : (100 : ℝ) < 2865 ∧ (100 : ℝ) < 182 ∧ (100 : ℝ) < 29051 ∧ (500 : ℝ) < 29051 := by
  norm_num

#print axioms kin_pos_def
#print axioms dispersion_bounded
#print axioms slaved_unbounded
#print axioms extra_growth_max
#print axioms trigger_concave_stiffness
#print axioms frw_mass_pos
#print axioms transition_obstruction
#print axioms ell_min_instances
#print axioms kin_ghost
