import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

set_option autoImplicit false

/-!
Algebraic certificates for the accompanying covariant/kinetic derivation.
These certify real-valued central moments and the necessary integrability
identity at the level of first/second jets. They do NOT formalize variation,
angular integration, a Boltzmann hierarchy, observational viability, or all
the gravitational field equations. There are no custom axioms or sorry terms.
-/
namespace ClockMoments

def twoStreamVariance (w v₁ v₂ : ℝ) : ℝ :=
  w * v₁^2 + (1-w) * v₂^2 - (w*v₁ + (1-w)*v₂)^2

theorem variance_factorization (w v₁ v₂ : ℝ) :
    twoStreamVariance w v₁ v₂ = w*(1-w)*(v₁-v₂)^2 := by
  unfold twoStreamVariance
  ring

theorem distinct_streams_positive (w v₁ v₂ : ℝ)
    (hw : 0 < w) (hw₁ : w < 1) (hne : v₁ ≠ v₂) :
    0 < twoStreamVariance w v₁ v₂ := by
  rw [variance_factorization]
  have hs : 0 < (v₁-v₂)^2 := sq_pos_of_ne_zero (sub_ne_zero.mpr hne)
  exact mul_pos (mul_pos hw (sub_pos.mpr hw₁)) hs

theorem bulk_shift_invariant (w v₁ v₂ b : ℝ) :
    twoStreamVariance w (v₁+b) (v₂+b) = twoStreamVariance w v₁ v₂ := by
  unfold twoStreamVariance
  ring

theorem positive_kick_pressure_source (rho rate speed : ℝ)
    (hrho : 0 < rho) (hrate : 0 < rate) (hspeed : 0 < speed) :
    0 < rho * rate * speed^2 / 3 := by
  positivity

/-- dnᵢⱼ denotes ∂ᵢ nⱼ; this is (n wedge dn)₀₁₂. -/
def frobenius (n₀ n₁ n₂ dn₀₁ dn₀₂ dn₁₀ dn₁₂ dn₂₀ dn₂₁ : ℝ) : ℝ :=
  n₀*(dn₁₂-dn₂₁) + n₁*(dn₂₀-dn₀₂) + n₂*(dn₀₁-dn₁₀)

/-- Every scaled gradient n=f dτ has zero Frobenius coefficient, assuming
the stated symmetric second jet (h₀₁,h₀₂,h₁₂) represents commuting derivatives. -/
theorem scaled_gradient_integrable
    (f f₀ f₁ f₂ t₀ t₁ t₂ h₀₁ h₀₂ h₁₂ : ℝ) :
    frobenius (f*t₀) (f*t₁) (f*t₂)
      (f₀*t₁+f*h₀₁) (f₀*t₂+f*h₀₂)
      (f₁*t₀+f*h₀₁) (f₁*t₂+f*h₁₂)
      (f₂*t₀+f*h₀₂) (f₂*t₁+f*h₁₂) = 0 := by
  unfold frobenius
  ring

theorem rotating_form_coefficient (omega x y : ℝ) :
    frobenius (-1) (-omega*y) (omega*x) 0 0 0 omega 0 (-omega) = -2*omega := by
  unfold frobenius
  ring

theorem rotating_form_not_integrable (omega x y : ℝ) (hw : omega ≠ 0) :
    frobenius (-1) (-omega*y) (omega*x) 0 0 0 omega 0 (-omega) ≠ 0 := by
  rw [rotating_form_coefficient]
  intro h
  apply hw
  linarith

#print axioms variance_factorization
#print axioms distinct_streams_positive
#print axioms bulk_shift_invariant
#print axioms positive_kick_pressure_source
#print axioms scaled_gradient_integrable
#print axioms rotating_form_coefficient
#print axioms rotating_form_not_integrable
end ClockMoments
