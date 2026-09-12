import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

set_option autoImplicit false
namespace ClockElimination
noncomputable section

/-!
Conditional real algebra for an auxiliary-field reduction and an isotropic
static gradient density. Exact covariant formulas, implicit-function existence,
field equations and numerical roots are audited outside Lean. This file does
not certify a gravitational action, a Hamiltonian DOF count or nonlinear health.
-/

def quadraticAlong (a b c alpha : ℝ) := a+2*b*alpha+c*alpha^2
def quarticAlong (b c d e f g h alpha beta : ℝ) :=
  d+e*alpha+f*alpha^2+g*alpha^3+h*alpha^4+2*(b+c*alpha)*beta

theorem stationary_auxiliary_quadratic_schur (a b c alpha : ℝ)
    (hstationary : b+c*alpha = 0) :
    c*quadraticAlong a b c alpha = a*c-b^2 := by
  unfold quadraticAlong
  have hid : c*(a+2*b*alpha+c*alpha^2)-(a*c-b^2) =
      (b+c*alpha)^2 := by ring
  rw [hstationary] at hid
  nlinarith

theorem quartic_independent_of_cubic_auxiliary_response
    (b c d e f g h alpha beta : ℝ) (hstationary : b+c*alpha=0) :
    quarticAlong b c d e f g h alpha beta =
      d+e*alpha+f*alpha^2+g*alpha^3+h*alpha^4 := by
  unfold quarticAlong
  rw [hstationary]
  ring

def blockQuadratic (a b c x y : ℝ) := a*x^2+2*b*x*y+c*y^2

/-- The reduced quadratic form follows from its stationarity relation and
the Schur identity; no rank is inserted into a certification flag. -/
theorem eliminate_stationary_block (a b c reduced x y : ℝ)
    (hstationary : b*x+c*y=0)
    (hschur : reduced*c=a*c-b^2) :
    c*blockQuadratic a b c x y = c*reduced*x^2 := by
  unfold blockQuadratic
  have hid : c*(a*x^2+2*b*x*y+c*y^2)-(a*c-b^2)*x^2 =
      (b*x+c*y)^2 := by ring
  rw [hstationary] at hid
  nlinarith [congrArg (fun z : ℝ => z*x^2) hschur]

def isotropicGradientQuadratic (slope curvature dotValue normSq : ℝ) :=
  2*slope*normSq+4*curvature*dotValue^2

/-- For F(|u|^2), a nonzero stationary gradient has F'=0. -/
theorem nonzero_stationary_gradient_has_zero_slope (radius slope : ℝ)
    (hr : radius ≠ 0) (h : 2*radius*slope=0) : slope=0 := by
  have h2r : 2*radius ≠ 0 := mul_ne_zero (by norm_num) hr
  exact (mul_eq_zero.mp h).resolve_left h2r

/-- A transverse direction has dotValue=0; its static quadratic form then
vanishes. Existence of two such spatial directions is separate geometry. -/
theorem stationary_transverse_gradient_null
    (radius slope curvature dotValue normSq : ℝ)
    (hr : radius ≠ 0) (hstationary : 2*radius*slope=0)
    (htransverse : dotValue=0) :
    isotropicGradientQuadratic slope curvature dotValue normSq=0 := by
  have hs := nonzero_stationary_gradient_has_zero_slope radius slope hr hstationary
  unfold isotropicGradientQuadratic
  rw [hs, htransverse]
  ring

theorem quartic_nonzero_stationary_radial_curvature (c2 c4 u : ℝ)
    (hu : u ≠ 0) (hstationary : 2*c2*u+4*c4*u^3=0) :
    2*c2+12*c4*u^2 = -4*c2 := by
  have hf : u*(2*c2+4*c4*u^2)=0 := by nlinarith [hstationary]
  have hroot := (mul_eq_zero.mp hf).resolve_left hu
  nlinarith

theorem quartic_nonzero_stationary_is_radial_maximum (c2 c4 u : ℝ)
    (hc : 0 < c2) (hu : u ≠ 0)
    (hstationary : 2*c2*u+4*c4*u^3=0) :
    2*c2+12*c4*u^2 < 0 := by
  rw [quartic_nonzero_stationary_radial_curvature c2 c4 u hu hstationary]
  linarith

/-- Conditional application of the independently derived affine cubic/
Einstein transverse correction. Nonzero cosmological Hessians are excluded
from this stated correction; their contribution cannot be discarded. -/
theorem affine_metric_exchange_negative_gradient (G0 gamma X M2 : ℝ)
    (hzero : G0=0) (hg : 0 < gamma) (hX : 0 < X) (hm : 0 < M2) :
    G0-2*gamma^2*X^2/M2 < 0 := by
  have hn : 0 < 2*gamma^2*X^2 :=
    mul_pos (mul_pos (by norm_num) (sq_pos_of_pos hg)) (sq_pos_of_pos hX)
  have hd := div_pos hn hm
  rw [hzero]
  linarith

theorem negative_transverse_gradient_has_no_real_speed (K G c : ℝ)
    (hk : 0 < K) (hg : G < 0) : K*c^2-G ≠ 0 := by
  have hnonneg := mul_nonneg (le_of_lt hk) (sq_nonneg c)
  linarith

/-- Necessary, not sufficient, nonaffine Hessian contribution at a zero-G0
stationary branch. The premise is the independently derived transverse
principal identity after multiplying by positive M2. -/
theorem nonaffine_escape_requires_hessian
    (G gamma X M2 B : ℝ) (hg : 0 < gamma) (hm : 0 < M2)
    (hG : 0 < G)
    (hidentity : M2*G=4*gamma*M2*B-2*gamma^2*X^2) :
    gamma*X^2 < 2*M2*B := by
  by_contra hnot
  have hb : 2*M2*B-gamma*X^2 ≤ 0 := by
    linarith [le_of_not_gt hnot]
  have htwo : 0 ≤ 2*gamma := by linarith
  have hprod := mul_nonpos_of_nonneg_of_nonpos htwo hb
  have hpositive := mul_pos hm hG
  nlinarith

#print axioms stationary_auxiliary_quadratic_schur
#print axioms quartic_independent_of_cubic_auxiliary_response
#print axioms eliminate_stationary_block
#print axioms nonzero_stationary_gradient_has_zero_slope
#print axioms stationary_transverse_gradient_null
#print axioms quartic_nonzero_stationary_radial_curvature
#print axioms quartic_nonzero_stationary_is_radial_maximum
#print axioms affine_metric_exchange_negative_gradient
#print axioms negative_transverse_gradient_has_no_real_speed
#print axioms nonaffine_escape_requires_hessian
end
end ClockElimination
