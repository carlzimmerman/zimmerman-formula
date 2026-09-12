import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
Exact algebra for the polynomial computed by current_action.py at n1=n2=1,
v1=-v2=3/5. The variational reduction, Dirac brackets, and mapping to the
physical principal symbol are checked outside Lean. No whole-gravity claim.
-/
set_option autoImplicit false
namespace CounterflowCone

def A : ℝ := 2851101297
def B (t : ℝ) : ℝ := 1613336721*t - 3790090569
def C (t : ℝ) : ℝ := 637297632*t^2 - 1820247721*t + 1197104272
def dispersion (u t : ℝ) : ℝ := A*u^2 + B t*u + C t

theorem bernstein_pos (a b c t : ℝ) (ha : 0 < a) (hb : 0 < b)
    (hc : 0 < c) (ht : 0 ≤ t) (ht1 : t ≤ 1) :
    0 < a*(1-t)^2 + 2*b*t*(1-t) + c*t^2 := by
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
  have h := bernstein_pos 1197104272 ((573960823:ℝ)/2) 14154183 t
    (by norm_num) (by norm_num) (by norm_num) ht ht1
  dsimp [C]
  nlinarith

theorem discriminant_positive (t : ℝ) (ht : 0 ≤ t) (ht1 : t ≤ 1) :
    0 < (B t)^2 - 4*A*C t := by
  have h := bernstein_pos 712524351048980625 4977253336574284650
    4576837276745705700 t (by norm_num) (by norm_num) (by norm_num) ht ht1
  dsimp [A, B, C]
  nlinarith

theorem null_value_positive (t : ℝ) (ht : 0 ≤ t) (ht1 : t ≤ 1) :
    0 < dispersion 1 t := by
  have h := bernstein_pos 258115000 154659500 688501632 t
    (by norm_num) (by norm_num) (by norm_num) ht ht1
  dsimp [dispersion, A, B, C]
  nlinarith

theorem all_squared_speed_roots_inside_lightcone (u t : ℝ)
    (ht : 0 ≤ t) (ht1 : t ≤ 1) (root : dispersion u t = 0) :
    0 < u ∧ u < 1 := by
  have ha : 0 < A := by norm_num [A]
  have hb : B t < 0 := by dsimp [B]; linarith
  have hc := constant_positive t ht ht1
  have h1 := null_value_positive t ht ht1
  have hd : 0 < 2*A + B t := by dsimp [A, B]; linarith
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
    have identity : dispersion u t = A*(u-1)^2 + (2*A+B t)*(u-1)
        + dispersion 1 t := by unfold dispersion; ring
    rw [identity] at root
    linarith

theorem coflow_entrainment_positive (x y : ℝ) (hne : x ≠ 0 ∨ y ≠ 0) :
    0 < x^2+y^2+(x-y)^2/16 := by
  have hd := sq_nonneg (x-y)
  rcases hne with hx | hy
  · have hp := sq_pos_of_ne_zero hx
    nlinarith [sq_nonneg y]
  · have hp := sq_pos_of_ne_zero hy
    nlinarith [sq_nonneg x]

theorem low_velocity_transverse_witness_negative :
    (-1000234998247000717:ℝ)/9000355999040001599999283 < 0 := by
  norm_num

noncomputable def transverseSmall (t : ℝ) : ℝ :=
  t*(717*t^3 - 1753*t^2 + 235*t + 1)
    / ((3*t^2 - 2*t + 1)*(239*t^2 - 374*t - 9))

theorem entire_small_velocity_interval_unstable (t : ℝ)
    (ht : 0 < t) (hupper : t ≤ (1:ℝ)/100) : transverseSmall t < 0 := by
  have ht0 : 0 ≤ t := le_of_lt ht
  have bound := mul_nonneg ht0 (sub_nonneg.mpr hupper)
  have ht2 := sq_nonneg t
  have ht3 : 0 ≤ t^3 := pow_nonneg ht0 3
  have hp : 0 < 717*t^3 - 1753*t^2 + 235*t + 1 := by nlinarith
  have hd1 : 0 < 3*t^2 - 2*t + 1 := by nlinarith
  have hd2 : 239*t^2 - 374*t - 9 < 0 := by nlinarith
  exact div_neg_of_pos_of_neg (mul_pos ht hp) (mul_neg_of_pos_of_neg hd1 hd2)

#print axioms bernstein_pos
#print axioms constant_positive
#print axioms discriminant_positive
#print axioms null_value_positive
#print axioms all_squared_speed_roots_inside_lightcone
#print axioms coflow_entrainment_positive
#print axioms low_velocity_transverse_witness_negative
#print axioms entire_small_velocity_interval_unstable
end CounterflowCone
