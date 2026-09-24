import Mathlib

/-!
# ZD12 — The Phantom Halo Laws (agent-derived, independently verified)

Framework premise (docstring scope, NOT certified here): the a0-line
g_obs^2 - g_bar^2 = a0 * g_bar (PD08/PD13). Certified here, all new:

  1. THE PHANTOM SHARE AT THE SCALE RADIUS: phi(a0) = a0(sqrt 2 - 1),
     so M_phi(r0) = (sqrt 2 - 1) M where r0^2 = G M / a0.
     FULL PROFILE M_phi(<r) = M(sqrt(1 + r^2/r0^2) - 1): verified
     symbolically (sympy, residual 0) and numerically in lane ZD12;
     its composite sqrt-folding fights this Lean build's quotient-sqrt
     lemmas -- NAMED BLOCKER, the ratio form and the at-r0 value carry
     the certified core here.
  2. THE QUARTIC LAW: v^4 = G^2 M^2 / r^2 + a0 G M exactly -- v^4 is
     affine in 1/r^2 with slope G^2 M^2 (a0-free) and intercept a0 G M
     (r-free).
  3. THE SATURATED GAIN: the envelope at the stripping surface equals
     8 sigma^4 / (G a0) (the pie-band tie: 2.15e14 Msun at sigma =
     809 km/s).
  4. THE WEDGE LADDER (arithmetic): a0* = (8/15) a0_L implies
     a0* = (16/15)(a0_L/2) -- the deep scale sits 1/15 of the cap above
     a0/2.

Lean certifies the algebra; the a0-line premise is the framework's law.
-/

noncomputable section
open scoped Real

/-- The phantom acceleration normalized by a0 (ZD01 restated inline). -/
noncomputable def phi (a0 x : ℝ) : ℝ := Real.sqrt (x^2 + a0 * x) - x

/-- THE PROFILE VALUE AT THE SCALE RADIUS: phi(a0) = a0(sqrt 2 - 1). -/
theorem phi_at_a0 (a0 : ℝ) (ha0 : 0 < a0) :
    phi a0 a0 = a0 * (Real.sqrt 2 - 1) := by
  unfold phi
  have harg : a0^2 + a0 * a0 = 2 * a0^2 := by ring
  rw [harg]
  have hmul : Real.sqrt (2 * a0^2) = Real.sqrt 2 * Real.sqrt (a0^2) :=
    Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 2) (a0^2)
  rw [hmul, Real.sqrt_sq (le_of_lt ha0)]
  ring

/-- THE PHANTOM SHARE AT r = r0: M_phi(r0) = (sqrt 2 - 1) M. -/
theorem mphi_at_r0 (a0 G M r0 : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hM : 0 < M)
    (_hr0 : 0 < r0) (hrd : r0^2 = G * M / a0) :
    r0^2 * phi a0 (G * M / r0^2) / G = (Real.sqrt 2 - 1) * M := by
  rw [hrd]
  have harg : G * M / (G * M / a0) = a0 := by field_simp [hG.ne', hM.ne', ha0.ne']
  rw [harg, phi_at_a0 a0 ha0]
  field_simp [hG.ne', ha0.ne']

/-- FULL PROFILE (blocked in this build -- named blocker): the composite
sqrt folding M_phi(<r) = M(sqrt(1 + r^2/r0^2) - 1) from the ratio
g_obs/g_bar = sqrt(1 + r^2/r0^2) fights this Lean build's sqrt-quotient
lemmas; both forms verified symbolically (sympy residual 0) and
numerically in lane ZD12; the at-r0 value is certified above. -/
theorem mphi_profile_blocked_note : True := by trivial

/-- THE QUARTIC LAW: v^4 = G^2 M^2 / r^2 + a0 G M (v^2 = r^2 g_obs^2). -/
theorem quartic_law (a0 G M r : ℝ) (_ha0 : 0 < a0) (_hG : 0 < G) (_hM : 0 < M)
    (hr : 0 < r) :
    r^2 * (Real.sqrt ((G * M / r^2)^2 + a0 * (G * M / r^2)))^2 = G^2 * M^2 / r^2 + a0 * G * M := by
  have hnn : 0 ≤ (G * M / r^2)^2 + a0 * (G * M / r^2) := by positivity
  rw [Real.sq_sqrt hnn]
  field_simp [hr.ne']

/-- THE SATURATED GAIN: the envelope at the stripping surface =
8 sigma^4 / (G a0); at sigma = 809 km/s this is 2.15e14 Msun, the pie
band tie. -/
theorem saturated_gain (a0 G sigma : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (_hs : 0 < sigma) :
    a0 * (4 * sigma^2 / a0)^2 / (2 * G) = 8 * sigma^4 / (G * a0) := by
  field_simp [ha0.ne', hG.ne']
  norm_num

/-- THE WEDGE LADDER: a0* = 8/15 a0_L means a0* = (16/15)(a0_L/2):
the deep scale sits 1/15 of the cap above a0/2. -/
theorem wedge_ladder (a0 : ℝ) (_ha0 : 0 < a0) :
    (8 / 15 : ℝ) * a0 = (16 / 15 : ℝ) * (a0 / 2) := by ring

end

#print axioms phi_at_a0
#print axioms mphi_at_r0
#print axioms quartic_law
#print axioms saturated_gain
#print axioms wedge_ladder