/-
AS083 -- Virial surface term with both boundaries: Lean 4 certificate.

Certifies the algebraic core of the shell-virial identity

    3 * ∫_{r_in}^R P dV = 4π [ R^3 P(R) - r_in^3 P(r_in) ] + Q,
    Q = ∫ rho (x·grad Phi) dV = C * M_shell  (log well Phi = C ln r),

claimed in seed AS083 (zimmerman-formula campaign, run AS083-r1):

  * T1 the generic integration-by-parts core: for any differentiable P on a
    closed interval, (∫ x in a..b, 3x^2 P(x) + x^3 P'(x)) = b^3 P(b) - a^3 P(a).
  * T2 the phantom isothermal integrand: ∫_a^b x^2 (σ²A/x^2) = σ²A(b-a).
  * T3 the two-surface boundary algebra: b^3 P(b) - a^3 P(a) = σ²A(b-a)
    for P(x) = σ²A/x^2.
  * T4 the virgin equivalence: with the phantom volume term 12πσ²A(b-a),
    the surface term 4πσ²A(b-a) and the well term 4πCA(b-a),

        12πσ²A(b-a) = 4πσ²A(b-a) + 4πCA(b-a)  ⟺  σ² = C/2

    (the framework value; positive A, positive π, b - a ≠ 0).
  * T5 the one-boundary residual: at σ² = C/2 the one-boundary reading
    4π b^3 P(b) + Q misbooks by exactly -(4πσ²A a), i.e. the omitted inner
    surface term -Δ with Δ = 4π a^3 P(a) = 4πσ²A a.
  * T6 Newtonian cancellation: for the point-mass envelope P = AGM_b/(3x^3),
    r^3 P = const, so the boundary contribution 4π(b^3P(b) - a^3P(a)) = 0.

Every theorem is a statement about real numbers and standard interval
integrals; no physical law is claimed of the world by Lean.
-/
import Mathlib

open Set
open scoped Topology

/- ------------------------------------------------------------------ -/
/- T1: generic integration by parts on the shell                      -/
/- ------------------------------------------------------------------ -/

theorem AS083_ibp (P : ℝ → ℝ) (a b : ℝ)
    (hP : DifferentiableOn ℝ P (uIcc a b)) :
    (∫ x in a..b, 3 * x ^ 2 * P x + x ^ 3 * deriv P x) = b ^ 3 * P b - a ^ 3 * P a := by
  let f : ℝ → ℝ := fun x => x ^ 3 * P x
  have hcont : ContinuousOn f (uIcc a b) := by
    dsimp [f]
    exact (continuousOn_id.pow 3).mul hP.continuousOn
  have hderiv : ∀ x ∈ uIcc a b,
      HasDerivAt f (3 * x ^ 2 * P x + x ^ 3 * deriv P x) x := by
    intro x hx
    have hPx : HasDerivAt P (deriv P x) x := (hP x hx).hasDerivAt
    have hpow : HasDerivAt (fun y : ℝ => y ^ 3) (3 * x ^ 2) x :=
      (hasDerivAt_id x).pow 3
    have hmul := hpow.mul hPx
    -- hmul : HasDerivAt (fun y => y ^ 3 * P y) ((3 * x ^ 2) * P x + x ^ 3 * deriv P x) x
    simpa [f] using hmul
  simpa [f] using intervalIntegral.integral_deriv_eq_sub hcont hderiv

/- ------------------------------------------------------------------ -/
/- T2: phantom integrand integral                                     -/
/- ------------------------------------------------------------------ -/

theorem AS083_phantom_integral (σ2 A a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    (∫ x in a..b, x ^ 2 * (σ2 * A / x ^ 2)) = σ2 * A * (b - a) := by
  have heq : (∫ x in a..b, x ^ 2 * (σ2 * A / x ^ 2)) =
      (∫ x in a..b, σ2 * A) := by
    apply intervalIntegral.integral_congr
    intro x hx
    have hxpos : 0 < x := lt_of_lt_of_le (lt_min ha hb) hx.1
    field_simp [ne_of_gt hxpos]
  rw [heq, intervalIntegral.integral_const]

/- ------------------------------------------------------------------ -/
/- T3: two-surface boundary algebra for the phantom                   -/
/- ------------------------------------------------------------------ -/

theorem AS083_surface_algebra (σ2 A a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :
    b ^ 3 * (σ2 * A / b ^ 2) - a ^ 3 * (σ2 * A / a ^ 2) = σ2 * A * (b - a) := by
  field_simp [hb, ha]
  ring

/- ------------------------------------------------------------------ -/
/- T4: the two-boundary virial equivalence, sigma^2 = C/2             -/
/- ------------------------------------------------------------------ -/

theorem AS083_two_boundary_iff (σ2 C A a b : ℝ) (hπ : 0 < Real.pi) (hA : 0 < A)
    (hd : b - a ≠ 0) :
    12 * Real.pi * σ2 * A * (b - a) =
        4 * Real.pi * σ2 * A * (b - a) + 4 * Real.pi * C * A * (b - a) ↔
      σ2 = C / 2 := by
  constructor
  · intro h
    have h8 : 8 * Real.pi * σ2 * A * (b - a) = 4 * Real.pi * C * A * (b - a) := by
      nlinarith [h]
    have hne : 4 * Real.pi * A * (b - a) ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (by norm_num : (4 : ℝ) ≠ 0)
        (mul_ne_zero (ne_of_gt hπ) (mul_ne_zero (ne_of_gt hA) hd)))
    have h2c : (2 * σ2) * (4 * Real.pi * A * (b - a)) =
        C * (4 * Real.pi * A * (b - a)) := by
      calc
        (2 * σ2) * (4 * Real.pi * A * (b - a))
            = 8 * Real.pi * σ2 * A * (b - a) := by ring
        _ = 4 * Real.pi * C * A * (b - a) := h8
        _ = C * (4 * Real.pi * A * (b - a)) := by ring
    have h26 : 2 * σ2 = C := mul_right_cancel₀ hne h2c
    have hC : C = 2 * σ2 := h26.symm
    rw [hC]
    ring
  · intro hσ
    rw [hσ]
    ring

/- ------------------------------------------------------------------ -/
/- T5: one-boundary residual at sigma^2 = C/2                         -/
/- ------------------------------------------------------------------ -/

theorem AS083_one_boundary_residual (σ2 C A a b : ℝ) (hC : C = 2 * σ2) :
    12 * Real.pi * σ2 * A * (b - a) -
        (4 * Real.pi * σ2 * A * b + 4 * Real.pi * C * A * (b - a)) =
      - (4 * Real.pi * σ2 * A * a) := by
  rw [hC]
  ring

/- ------------------------------------------------------------------ -/
/- T6: Newtonian point-mass envelope: surfaces cancel                 -/
/- ------------------------------------------------------------------ -/

theorem AS083_newtonian_cancellation (AGMb a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :
    b ^ 3 * (AGMb / (3 * b ^ 3)) - a ^ 3 * (AGMb / (3 * a ^ 3)) = 0 := by
  field_simp [pow_ne_zero 3 hb, pow_ne_zero 3 ha]
  ring

#check AS083_ibp
#check AS083_phantom_integral
#check AS083_surface_algebra
#check AS083_two_boundary_iff
#check AS083_one_boundary_residual
#check AS083_newtonian_cancellation

#print axioms AS083_ibp
#print axioms AS083_phantom_integral
#print axioms AS083_surface_algebra
#print axioms AS083_two_boundary_iff
#print axioms AS083_one_boundary_residual
#print axioms AS083_newtonian_cancellation
