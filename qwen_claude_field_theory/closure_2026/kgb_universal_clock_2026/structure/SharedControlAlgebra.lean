import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-! Conditional algebra for any finite or indexed collection of preservation
equations. The vector fields and physical mapping are checked separately in
SymPy/prose, not formalized here. No numerical rank or DOF count is assumed. -/
namespace SharedClockControl

theorem pivot_fit_of_minors {ι : Type*} (A B : ι → ℝ) (i0 : ι)
    (hB : B i0 ≠ 0) (hm : ∀ i, A i * B i0 - A i0 * B i = 0) :
    ∀ i, A i + (-A i0 / B i0) * B i = 0 := by
  intro i
  field_simp
  nlinarith [hm i]

theorem common_scalar_control_iff {ι : Type*} (A B : ι → ℝ) (i0 : ι)
    (hB : B i0 ≠ 0) :
    (∃ u : ℝ, ∀ i, A i + u * B i = 0) ↔
      ∀ i, A i * B i0 - A i0 * B i = 0 := by
  constructor
  · rintro ⟨u,hu⟩ i
    calc
      A i * B i0 - A i0 * B i =
          (A i + u * B i) * B i0 - (A i0 + u * B i0) * B i := by ring
      _ = 0 := by rw [hu i,hu i0]; ring
  · intro hm
    exact ⟨-A i0 / B i0,pivot_fit_of_minors A B i0 hB hm⟩

theorem nonzero_pivot_control_unique (a b u v : ℝ) (hb : b ≠ 0)
    (hu : a+u*b=0) (hv : a+v*b=0) : u=v := by
  have h : (u-v)*b=0 := by nlinarith
  have hdiff : u-v=0 := (mul_eq_zero.mp h).resolve_right hb
  linarith

theorem zero_control_nonzero_residual (a b u : ℝ) (hb : b=0) (ha : a≠0) :
    a+u*b≠0 := by simpa [hb] using ha

theorem determinant_tangency_on_first_preservation
    (A B C D f DA DB DC DD : ℝ)
    (h1 : A+f*B=0) (h2 : C+f*D=0) :
    DA*D+A*DD-DC*B-C*DB = (DA+f*DB)*D-(DC+f*DD)*B := by
  calc
    DA*D+A*DD-DC*B-C*DB =
        (DA+f*DB)*D-(DC+f*DD)*B+(A+f*B)*DD-(C+f*D)*DB := by ring
    _ = (DA+f*DB)*D-(DC+f*DD)*B := by rw [h1,h2]; ring

theorem matched_third_jet_has_no_FXXX
    (ell dk j E f N B : ℝ) (hd : dk=0) (hE : E=0) :
    ell*dk+2*j*E+f*(N+j*B)=f*(N+j*B) := by simp [hd,hE]

theorem signed_H_matching_iff (P F gamma H1 H2 : ℝ) (hg : gamma≠0) :
    (2*P/F+H1*gamma=2*P/F+H2*gamma) ↔ H1=H2 := by
  constructor
  · intro h
    have hprod : (H1-H2)*gamma=0 := by nlinarith
    have hd : H1-H2=0 := (mul_eq_zero.mp hprod).resolve_right hg
    linarith
  · intro h
    rw [h]

theorem limiting_lower_determinant_negative
    (A X e : ℝ) (hA : 0<A) (hX : 0<X) (he : 0<e) (he1 : e<1) :
    -2*A*(12*e^3-32*e^2+28*e+3)/X < 0 := by
  have hsub : 0<1-e := sub_pos.mpr he1
  have hpoly : 0<12*e^3-32*e^2+28*e+3 := by
    have heq : 12*e^3-32*e^2+28*e+3 =
        3+4*e*(2+2*(1-e)+3*(1-e)^2) := by ring
    rw [heq]
    positivity
  apply div_neg_of_neg_of_pos _ hX
  nlinarith [mul_pos hA hpoly]

#print axioms pivot_fit_of_minors
#print axioms common_scalar_control_iff
#print axioms nonzero_pivot_control_unique
#print axioms zero_control_nonzero_residual
#print axioms determinant_tangency_on_first_preservation
#print axioms matched_third_jet_has_no_FXXX
#print axioms signed_H_matching_iff
#print axioms limiting_lower_determinant_negative
end SharedClockControl
