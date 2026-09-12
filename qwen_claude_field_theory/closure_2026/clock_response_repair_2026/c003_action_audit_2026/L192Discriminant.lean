import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

set_option autoImplicit false

/-!
Algebraic certificate for the fixed-metric, gamma=0 two-field principal
subsystem derived separately by symbolic variation. Not a certificate of
the Einstein/clock PDE or an on-shell finite-gradient cosmology.
p=P_X, r=P_XX, q=Q², C=W_Y+2zW_YY, w=W_Y, z=Y cos²theta.
W>0 and F=W-2qC-2zw>0 are required for this elimination branch.
-/
namespace L192Discriminant
noncomputable section

def kinetic (p r q : ℝ) : ℝ := 2*p+4*q*r

def proxyXi (p r q C w W F z : ℝ) : ℝ :=
  16*q*r^2*z + kinetic p r q * (-4*r*z-8*p*q*C*z*w/(W*F))

theorem marginal_reduction (p r q C w W F z : ℝ)
    (hC : C ≠ 0) (hW : W ≠ 0) (hF : F ≠ 0)
    (hrel : F=W-2*q*C-2*z*w) :
    16*q*r^2*z + kinetic p r q *
      (2*p-4*r*z-2*(p*(W-2*q*C)/(W*C))*C*(W-2*z*w)/F) =
      proxyXi p r q C w W F z := by
  unfold proxyXi kinetic
  field_simp
  rw [hrel]
  ring

theorem discriminant_identity (p r q C w W F z : ℝ) :
    proxyXi p r q C w W F z =
      -8*p*z*(r + kinetic p r q*q*C*w/(W*F)) := by
  unfold proxyXi kinetic
  ring

theorem proxy_marginal_is_elliptic (p r q C w W F z : ℝ)
    (hp : 0 < p) (hr : 0 < r) (hq : 0 ≤ q) (hC : 0 ≤ C)
    (hw : 0 ≤ w) (hW : 0 < W) (hF : 0 < F) (hz : 0 < z) :
    proxyXi p r q C w W F z < 0 := by
  rw [discriminant_identity]
  have hK : 0 < kinetic p r q := by
    unfold kinetic
    positivity
  have hterm : 0 ≤ kinetic p r q*q*C*w/(W*F) := by positivity
  have hsum : 0 < r+kinetic p r q*q*C*w/(W*F) := by linarith
  have hprod : 0 < 8*p*z*(r+kinetic p r q*q*C*w/(W*F)) := by positivity
  nlinarith

/-- A negative quarter-discriminant prohibits any real characteristic speed. -/
theorem no_real_characteristic (K B G : ℝ) (hXi : B^2+K*G < 0) :
    ¬ ∃ c : ℝ, K*c^2+2*B*c-G=0 := by
  rintro ⟨c, hc⟩
  have heq : K*(K*c^2+2*B*c-G)=0 := by rw [hc, mul_zero]
  have hid : (K*c+B)^2 = B^2+K*G := by nlinarith [heq]
  nlinarith [sq_nonneg (K*c+B)]

#print axioms marginal_reduction
#print axioms discriminant_identity
#print axioms proxy_marginal_is_elliptic
#print axioms no_real_characteristic
end
end L192Discriminant
