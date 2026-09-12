import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

set_option autoImplicit false
namespace VarianceClosure
noncomputable section

/-!
Exact algebra for the second-order clock-frame gradient observable. p is a
positive spectral weight times k^2/a^2, NOT the MOND interpolation parameter.
The application to the action-derived constrained transfer system and its
admissible initial data is audited separately in geometry/ and evolution/.
These lemmas neither formalize the covariant action nor exclude a nonlinear
statistical attractor on a restricted basin of initial conditions.
-/

def variance (p x : ℝ) := p*x^2
def varianceRate (p H a b x y : ℝ) :=
  -2*H*p*x^2 + 2*p*x*(a*x+b*y)

theorem opposite_correlation_rate_gap (p H a b x y : ℝ) :
    varianceRate p H a b x y - varianceRate p H a b x (-y) =
      4*p*b*x*y := by
  unfold varianceRate
  ring

/-- An exact variance-only law on every state of a two-coordinate slice
exists iff the observed field's velocity has no coupling to the second one. -/
theorem exact_scalar_closure_iff (p H a b : ℝ) (hp : 0 < p) :
    (∃ f : ℝ → ℝ, ∀ x y : ℝ,
      varianceRate p H a b x y = f (variance p x)) ↔ b = 0 := by
  constructor
  · rintro ⟨f, hf⟩
    have heq := (hf 1 1).trans (hf 1 (-1)).symm
    have hgap := opposite_correlation_rate_gap p H a b 1 1
    rw [heq] at hgap
    have hpb : p*b = 0 := by nlinarith
    exact (mul_eq_zero.mp hpb).resolve_left (ne_of_gt hp)
  · intro hb
    subst b
    refine ⟨fun y => 2*(a-H)*y, ?_⟩
    intro x y
    unfold varianceRate variance
    ring

/-- k=0 gives no gradient observable; this says nothing about its homogeneous
Hamiltonian constraints, which cannot be obtained by dividing by k. -/
theorem homogeneous_gradient_zero (H a b x y : ℝ) :
    variance 0 x = 0 ∧ varianceRate 0 H a b x y = 0 := by
  constructor
  · unfold variance
    ring
  · unfold varianceRate
    ring

def momentRate (p H S C : ℝ) := 2*p*(C-H*S)
def momentAcceleration (p H Hd S C V D : ℝ) :=
  (4*H^2-2*Hd)*p*S - 8*H*p*C + 2*p*(V+D)

theorem instantaneous_balance_requires_correlation (p H S C : ℝ)
    (hp : 0 < p) (h : momentRate p H S C = 0) : C = H*S := by
  unfold momentRate at h
  have hp2 : 2*p ≠ 0 := by nlinarith
  have hz := (mul_eq_zero.mp h).resolve_left hp2
  linarith

theorem stationary_variance_acceleration (p H Hd S C V D : ℝ)
    (h : C = H*S) :
    momentAcceleration p H Hd S C V D =
      2*p*(V+D-(2*H^2+Hd)*S) := by
  rw [h]
  unfold momentAcceleration
  ring

theorem coherent_stationarity_requires_acceleration (p H Hd x acc : ℝ)
    (hp : 0 < p) (hx : x ≠ 0)
    (h : momentAcceleration p H Hd (x^2) (H*x^2) ((H*x)^2) (x*acc) = 0) :
    acc = (Hd+H^2)*x := by
  have hid : momentAcceleration p H Hd (x^2) (H*x^2) ((H*x)^2) (x*acc) =
      (2*p*x)*(acc-(Hd+H^2)*x) := by
    unfold momentAcceleration
    ring
  rw [hid] at h
  have hpx : 2*p*x ≠ 0 := mul_ne_zero (by nlinarith) hx
  have hz := (mul_eq_zero.mp h).resolve_left hpx
  linarith

/-- A homogeneous linear covariance system cannot select an isolated nonzero
stationary covariance: every rescaling of a stationary covariance is stationary.
This is a statement about that linear system, not its nonlinear completion. -/
theorem homogeneous_rate_preserves_stationary_ray
    (rate : ℝ → ℝ) (hscale : ∀ c x : ℝ, rate (c*x) = c*rate x)
    (x : ℝ) (hx : rate x = 0) (c : ℝ) : rate (c*x) = 0 := by
  rw [hscale, hx, mul_zero]

#print axioms opposite_correlation_rate_gap
#print axioms exact_scalar_closure_iff
#print axioms homogeneous_gradient_zero
#print axioms instantaneous_balance_requires_correlation
#print axioms stationary_variance_acceleration
#print axioms coherent_stationarity_requires_acceleration
#print axioms homogeneous_rate_preserves_stationary_ray
end
end VarianceClosure
