import Mathlib
noncomputable section
namespace IncrementAudit
-- Incremental versus total potentials only; no field theory is formalized.
theorem slip_increment (alpha phiN : ℝ) :
 (1+alpha)*phiN-phiN=alpha*phiN := by ring

theorem zero_increment_nonzero_total (phiN : ℝ) (h : phiN ≠ 0) :
 phiN-phiN=0 ∧ phiN ≠ 0 := ⟨sub_self _, h⟩

theorem denominator (b : ℝ) :
 (1-2*b)^2-(-2*b*(2*(1-2*b)+b))/2=(1-b)^2 := by ring

theorem rational_witness (phiN : ℝ) (h : phiN ≠ 0) :
 (3/2:ℝ)*phiN-phiN ≠ 0 := by
 intro hz
 apply h
 linarith

#print axioms slip_increment
#print axioms zero_increment_nonzero_total
#print axioms denominator
#print axioms rational_witness
end IncrementAudit
