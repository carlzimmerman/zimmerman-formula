import Mathlib

/-! Algebraic consequences of explicitly supplied statistical dictionaries.
No microscopic ensemble is asserted to carry cosmological vacuum stress. -/
namespace Micro32Pi

theorem exponential_response (j : ℝ) (hj : 0 ≤ j) :
    1-1/(1+j)=j/(1+j) := by
  have h : 1+j ≠ 0 := by linarith
  field_simp
  <;> ring

theorem force_inverse (x : ℝ) (hx : x < 1) :
    (x/(1-x))/(1+x/(1-x))=x := by
  have h : 1-x ≠ 0 := by linarith
  field_simp
  <;> ring

theorem quantum_shape_gap (v : ℝ) (hv : 0 ≤ v) :
    (2+6*v)/(1+4*v)-(3/2:ℝ)=1/(2*(1+4*v)) := by
  have h : 1+4*v ≠ 0 := by linarith
  field_simp
  <;> ring

theorem quantum_shape_not_logarithmic (v : ℝ) (hv : 0 ≤ v) :
    (3/2:ℝ) < (2+6*v)/(1+4*v) := by
  have hg := quantum_shape_gap v hv
  have hp : 0 < 1/(2*(1+4*v)) := by positivity
  linarith

/-- Fixing the statistical temperature prefactor leaves the energy offset. -/
theorem thermal_offset_required (e C : ℝ) (h : C=1+e) :
    C=16*Real.pi ↔ e=16*Real.pi-1 := by
  constructor <;> intro hh <;> linarith

theorem positive_entropy_not_vacuum (energy pressure temp entropy : ℝ)
    (hT : 0<temp) (hS : 0<entropy)
    (hthermo : energy+pressure=temp*entropy) : pressure ≠ -energy := by
  have hp := mul_pos hT hS
  intro h
  linarith

#print axioms exponential_response
#print axioms force_inverse
#print axioms quantum_shape_gap
#print axioms quantum_shape_not_logarithmic
#print axioms thermal_offset_required
#print axioms positive_entropy_not_vacuum
end Micro32Pi
