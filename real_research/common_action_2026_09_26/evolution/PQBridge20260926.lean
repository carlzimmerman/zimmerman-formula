import Mathlib

/-! Conditional real-algebra bridges for the inactive de Sitter PQ scalar block.
The ADM derivation, exponential-function estimates, PDE evolution, and homogeneous
constraint are not Lean-certified by this file. No physical conclusion is an axiom. -/
namespace PQBridge20260926

theorem effective_alpha_window (a r : ℝ)
    (ha : 0 < a) (ha1 : a ≤ 1) (hr : 0 < r) (hr4 : r ≤ 1/4) :
    0 < 2 - (2-a)*(1-r)^2 ∧ 2 - (2-a)*(1-r)^2 ≤ 23/16 := by
  have h2 : 0 < 2-a := by linarith
  have hr2 : 0 < 2-r := by linarith
  have hprod : 0 < (2-a)*r*(2-r) := by positivity
  have hlo : 9/16 ≤ (1-r)^2 := by nlinarith
  have hmul := mul_nonneg (show 0 ≤ 1-a by linarith) (sq_nonneg (1-r))
  constructor <;> nlinarith

theorem d_window (a eta f : ℝ) (ha : 0 < a) (hau : a ≤ 23/16)
    (he : 0 ≤ eta) (heu : eta ≤ 1/10) (hf : 0 ≤ f) (hfu : f ≤ 1) :
    0 < a+eta*f ∧ a+eta*f ≤ 123/80 ∧ a+eta*f < 2 := by
  have hl := mul_nonneg he hf
  have hu := mul_nonneg he (show 0 ≤ 1-f by linarith)
  constructor
  · linarith
  · constructor <;> nlinarith

theorem derivative_margin (d r eta da db : ℝ)
    (hd : 0 ≤ d) (hr : r ≤ 1/4) (he : eta ≤ 1/10)
    (hda : -4*r ≤ da) (hdb : -4*eta ≤ db) :
    3/5 ≤ 2+d+da+db := by linarith

theorem reduced_kinetic_positive (K H x d : ℝ)
    (hK : 0 < K) (hH : 0 < H) (hx : 0 < x) (hd : 0 < d) :
    0 < K*x*d/(K*H^2+x*d) := by positivity

theorem integrated_gradient_negative (K H x d dp : ℝ)
    (hK : 0 < K) (hH : 0 < H) (hx : 0 < x) (hd : 0 < d)
    (hd2 : d < 2) (hb : 0 < 2+d+2*x*dp) :
    -2*x^2*(K*H^2*(2+d+2*x*dp)+x*d*(2-d))/(K*H^2+x*d)^2 < 0 := by
  have hn : 0 < K*H^2*(2+d+2*x*dp)+x*d*(2-d) := by positivity
  have hden : 0 < (K*H^2+x*d)^2 := by positivity
  apply (div_neg_iff).2
  right
  constructor
  · have hxx : 0 < x^2 := by positivity
    nlinarith [mul_pos hxx hn]
  · exact hden

theorem IR_tuning (H r z : ℝ) (hH : H ≠ 0) (hr : r ≠ 0) :
    6*H^2*r*(1-(1+z)*r)=0 ↔ z=1/r-1 := by
  have hn : 6*H^2*r ≠ 0 := by positivity
  rw [mul_eq_zero, or_iff_right hn]
  constructor
  · intro h
    apply (eq_sub_iff_add_eq).2
    apply (eq_div_iff hr).2
    nlinarith
  · intro h
    rw [h]
    field_simp
    <;> ring

end PQBridge20260926
#print axioms PQBridge20260926.effective_alpha_window
#print axioms PQBridge20260926.d_window
#print axioms PQBridge20260926.derivative_margin
#print axioms PQBridge20260926.reduced_kinetic_positive
#print axioms PQBridge20260926.integrated_gradient_negative
#print axioms PQBridge20260926.IR_tuning
