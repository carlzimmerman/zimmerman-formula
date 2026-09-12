import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Algebraic certificates for density_repair.py. Variational calculus and
the connection to the matter principal symbol are checked in Python.
Neither the parameters nor kappa are derived here. -/
set_option autoImplicit false
namespace DensityRepair

theorem coflow_square_identity (n m f x y : ℝ) :
    (n+m)*(n*x^2+m*y^2+f*n*m*(x-y)^2)
      = (n*x+m*y)^2+(1+(n+m)*f)*n*m*(x-y)^2 := by ring

theorem coflow_positive (n m f x y : ℝ) (hn : 0 < n) (hm : 0 < m)
    (hf : 0 < 1+(n+m)*f) (hne : x ≠ 0 ∨ y ≠ 0) :
    0 < n*x^2+m*y^2+f*n*m*(x-y)^2 := by
  have total : 0 < n+m := by linarith
  have ident := coflow_square_identity n m f x y
  by_cases hxy : x = y
  · subst y
    have hx : x ≠ 0 := by tauto
    have hx2 := sq_pos_of_ne_zero hx
    have pos := mul_pos total hx2
    nlinarith
  · have diff : x-y ≠ 0 := sub_ne_zero.mpr hxy
    have pos := mul_pos (mul_pos (mul_pos hf hn) hm) (sq_pos_of_ne_zero diff)
    have hsum := sq_nonneg (n*x+m*y)
    have hp : 0 < (n+m)*(n*x^2+m*y^2+f*n*m*(x-y)^2) := by linarith
    exact (mul_pos_iff_of_pos_left total).mp hp

theorem low_velocity_temporal_signs (dPow p b : ℝ)
    (hd : 0 < dPow) (hp : 0 < p) (hp1 : p < 1) (hb : (1:ℝ)/4 < b) :
    dPow*p*(p-1) < 0 ∧ (2-8*b)*dPow < 0 := by
  constructor
  · exact mul_neg_of_pos_of_neg (mul_pos hd hp) (by linarith)
  · exact mul_neg_of_neg_of_pos (by linarith) hd

theorem pressure_trace_negative (dPow p : ℝ) (hd : 0 < dPow) (hp : 0 < p) :
    (-2-6*p)*dPow < 0 := by
  exact mul_neg_of_neg_of_pos (by linarith) hd

def A : ℝ := 271744257575
def B (t : ℝ) : ℝ := 5507190570*t - 10325099400
def C (t : ℝ) : ℝ := 28933981*t^2 - 87987570*t + 66891825
def dispersion (u t : ℝ) : ℝ := A*u^2+B t*u+C t

theorem bernstein_pos (a b c t : ℝ) (ha : 0 < a) (hb : 0 < b)
    (hc : 0 < c) (ht : 0 ≤ t) (ht1 : t ≤ 1) :
    0 < a*(1-t)^2+2*b*t*(1-t)+c*t^2 := by
  have ha0 := mul_nonneg (le_of_lt ha) (sq_nonneg (1-t))
  have hm := mul_nonneg (mul_nonneg (mul_nonneg (by norm_num : (0:ℝ) ≤ 2)
    (le_of_lt hb)) ht) (sub_nonneg.mpr ht1)
  by_cases hz : t = 0
  · subst t
    nlinarith
  · have hp : 0 < t := lt_of_le_of_ne ht (Ne.symm hz)
    have hcp := mul_pos hc (sq_pos_of_pos hp)
    linarith

theorem constant_positive (t : ℝ) (ht : 0 ≤ t) (ht1 : t ≤ 1) : 0 < C t := by
  have h := bernstein_pos 66891825 22898040 7838236 t
    (by norm_num) (by norm_num) (by norm_num) ht ht1
  dsimp [C]
  nlinarith

theorem discriminant_positive (t : ℝ) (ht : 0 ≤ t) (ht1 : t ≤ 1) :
    0 < (B t)^2-4*A*C t := by
  have h := bernstein_pos 33897800330033062500 24855744050997090000
    14692263004121418100 t (by norm_num) (by norm_num) (by norm_num) ht ht1
  dsimp [A, B, C]
  nlinarith

theorem null_value_positive (t : ℝ) (ht : 0 ≤ t) (ht1 : t ≤ 1) :
    0 < dispersion 1 t := by
  have h := bernstein_pos 261486050000 264195651500 266934186981 t
    (by norm_num) (by norm_num) (by norm_num) ht ht1
  dsimp [dispersion, A, B, C]
  nlinarith

theorem all_angle_squared_speed_roots (u t : ℝ)
    (ht : 0 ≤ t) (ht1 : t ≤ 1) (root : dispersion u t = 0) :
    0 < u ∧ u < 1 := by
  have ha : 0 < A := by norm_num [A]
  have hb : B t < 0 := by dsimp [B]; linarith
  have hc := constant_positive t ht ht1
  have h1 := null_value_positive t ht ht1
  have hd : 0 < 2*A+B t := by dsimp [A, B]; linarith
  constructor
  · by_contra h
    have hu : u ≤ 0 := le_of_not_gt h
    have hprod := mul_nonneg_of_nonpos_of_nonpos (le_of_lt hb) hu
    have hsq := mul_nonneg (le_of_lt ha) (sq_nonneg u)
    dsimp [dispersion] at root
    linarith
  · by_contra h
    have hu : 0 ≤ u-1 := by linarith
    have hprod := mul_nonneg (le_of_lt hd) hu
    have hsq := mul_nonneg (le_of_lt ha) (sq_nonneg (u-1))
    have ident : dispersion u t = A*(u-1)^2+(2*A+B t)*(u-1)+dispersion 1 t := by
      unfold dispersion
      ring
    rw [ident] at root
    linarith

#print axioms coflow_square_identity
#print axioms coflow_positive
#print axioms low_velocity_temporal_signs
#print axioms pressure_trace_negative
#print axioms all_angle_squared_speed_roots
end DensityRepair
