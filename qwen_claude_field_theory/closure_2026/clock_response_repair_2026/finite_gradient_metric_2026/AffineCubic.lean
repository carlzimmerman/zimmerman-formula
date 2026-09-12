import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

set_option autoImplicit false
namespace AffineCubic
noncomputable section

/-!
Conditional exact algebra after action variation and Einstein trace reversal.
q=Q², x=X=Q²-Y>0, z=(v dot khat)², 0<z<=Y, t=2 gamma² X/M²>=0.
p=P_X>0, r=P_XX>0, C=W_Y+2z W_YY, w=W_Y, F=W-2qC-2zw>0.
This is the affine-Hessian principal class, not a solved cosmology. Nonzero
background Hessian adds a separate term linear in gamma, NOT covered here.
-/

def K (p r q : ℝ) := 2*p+4*q*r
def G (p r q C w W F z : ℝ) := -4*r*z-8*p*q*C*z*w/(W*F)
def xi (p r q C w W F z x t : ℝ) :=
  16*q*(r+t)^2*z + (K p r q+t*(4*q-x))*(G p r q C w W F z-t*(x+4*z))
def linearCoeff (p r q C w W F z x : ℝ) :=
  -8*p*z-2*p*x-4*r*x*(q-z)-(4*q-x)*8*p*q*C*z*w/(W*F)
def quadraticCoeff (q z x : ℝ) := x*(x-4*q+4*z)

theorem exact_coupling_expansion (p r q C w W F z x t : ℝ) :
    xi p r q C w W F z x t =
      -8*p*z*(r+K p r q*q*C*w/(W*F)) +
      t*linearCoeff p r q C w W F z x + t^2*quadraticCoeff q z x := by
  unfold xi G K linearCoeff quadraticCoeff
  ring

theorem quadratic_coefficient_negative (q z x : ℝ)
    (hx : 0 < x) (hgap : x ≤ q-z) : quadraticCoeff q z x < 0 := by
  unfold quadraticCoeff
  have hfactor : x-4*q+4*z < 0 := by linarith
  exact mul_neg_of_pos_of_neg hx hfactor

theorem linear_coefficient_negative (p r q C w W F z x : ℝ)
    (hp : 0 < p) (hr : 0 < r) (hz : 0 < z) (hx : 0 < x)
    (hgap : x ≤ q-z) (hC : 0 ≤ C) (hw : 0 ≤ w)
    (hW : 0 < W) (hF : 0 < F) :
    linearCoeff p r q C w W F z x < 0 := by
  have hq : 0 ≤ q := by linarith
  have hqz : 0 ≤ q-z := by linarith
  have h4q : 0 ≤ 4*q-x := by linarith
  have h1 : 0 < 8*p*z := by positivity
  have h2 : 0 ≤ 2*p*x := by positivity
  have h3 : 0 ≤ 4*r*x*(q-z) := by positivity
  have h4 : 0 ≤ (4*q-x)*8*p*q*C*z*w/(W*F) := by positivity
  unfold linearCoeff
  linarith

theorem no_affine_cubic_repair (p r q C w W F z x t : ℝ)
    (hp : 0 < p) (hr : 0 < r) (hz : 0 < z) (hx : 0 < x)
    (hgap : x ≤ q-z) (hC : 0 ≤ C) (hw : 0 ≤ w)
    (hW : 0 < W) (hF : 0 < F) (ht : 0 ≤ t) :
    xi p r q C w W F z x t < 0 := by
  have hq : 0 ≤ q := by linarith
  have hK : 0 < K p r q := by unfold K; positivity
  have hfrac : 0 ≤ K p r q*q*C*w/(W*F) := by positivity
  have hsum : 0 < r+K p r q*q*C*w/(W*F) := by linarith
  have hbase : -8*p*z*(r+K p r q*q*C*w/(W*F)) < 0 := by
    have hpos : 0 < 8*p*z*(r+K p r q*q*C*w/(W*F)) := by positivity
    nlinarith
  have hlin := linear_coefficient_negative p r q C w W F z x hp hr hz hx hgap hC hw hW hF
  have hquad := quadratic_coefficient_negative q z x hx hgap
  have hterm1 := mul_nonpos_of_nonneg_of_nonpos ht (le_of_lt hlin)
  have hterm2 := mul_nonpos_of_nonneg_of_nonpos (sq_nonneg t) (le_of_lt hquad)
  rw [exact_coupling_expansion]
  linarith

#print axioms exact_coupling_expansion
#print axioms quadratic_coefficient_negative
#print axioms linear_coefficient_negative
#print axioms no_affine_cubic_repair
end
end AffineCubic
