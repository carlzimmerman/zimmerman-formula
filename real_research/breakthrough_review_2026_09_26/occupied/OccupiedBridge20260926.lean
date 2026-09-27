import Mathlib

/-! Conditional algebra for the occupied-FRW reduction. This does not formalize
the ADM derivation, heat operator, or finite-wavelength evolution. -/
namespace OccupiedBridge20260926

theorem occupation_control_identity (T V V0 f1 f2 r : ℝ) :
    T+(V-T-V0*f1)*r-(V+V0*f2/2)*r^2-T*(1-r)^2 =
      r*((1-r)*(T+V)-V0*(f1+f2*r/2)) := by ring

theorem parallel_Schur_determinant (M K H F Q v : ℝ)
    (hM : M ≠ 0) (hF : F ≠ 0) :
    (M*K-(M*K*H)^2/(M*F))*(1-Q^2*v^2/(M*F))-(K*H*Q*v/F)^2 =
      M*K*(F-K*H^2-Q^2*v^2/M)/F := by
  field_simp
  <;> ring

theorem PQ_control_positive (a x M r r0 E V0 : ℝ)
    (ha : 0 < a) (hx : 0 < x) (hM : 0 < M)
    (hr : 0 ≤ r) (hr0 : 0 < r0) (hrr : r ≤ r0) (hr01 : r0 ≤ 1)
    (hE : 0 ≤ E) (hV : 0 ≤ V0) :
    0 < a*x+2*(r*(1-r)*E+V0*r*(1-r/r0))/M := by
  have hr1 : 0 ≤ 1-r := by linarith
  have hrat : r/r0 ≤ 1 := (div_le_one hr0).2 hrr
  have hrat1 : 0 ≤ 1-r/r0 := by linarith
  have hh : 0 ≤ 2*(r*(1-r)*E+V0*r*(1-r/r0))/M := by positivity
  have hh2 : 0 < a*x := mul_pos ha hx
  linarith

theorem flat_control_positive (a x M r E : ℝ)
    (ha : 0 < a) (hx : 0 < x) (hM : 0 < M)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hE : 0 ≤ E) :
    0 < a*x+2*r*(1-r)*E/M := by
  have hh : 0 ≤ 1-r := by linarith
  have ht : 0 ≤ 2*r*(1-r)*E/M := by positivity
  have hp : 0 < a*x := mul_pos ha hx
  linarith

theorem occupied_IR_floor (M r E : ℝ)
    (hM : 0 < M) (hr : 0 < r) (hr1 : r < 1) (hE : 0 < E) :
    0 < 2*r*(1-r)*E/M := by
  have hh : 0 < 1-r := by linarith
  positivity

theorem constraint_determinant_positive (M c2 cN x F : ℝ)
    (hM : 0 < M) (hc2 : 0 < c2) (hcN : 0 < cN)
    (hx : 0 < x) (hF : 0 < F) :
    0 < 4*M^4*c2*cN^2*x^4*F := by positivity

end OccupiedBridge20260926
#print axioms OccupiedBridge20260926.occupation_control_identity
#print axioms OccupiedBridge20260926.parallel_Schur_determinant
#print axioms OccupiedBridge20260926.PQ_control_positive
#print axioms OccupiedBridge20260926.flat_control_positive
#print axioms OccupiedBridge20260926.occupied_IR_floor
#print axioms OccupiedBridge20260926.constraint_determinant_positive
