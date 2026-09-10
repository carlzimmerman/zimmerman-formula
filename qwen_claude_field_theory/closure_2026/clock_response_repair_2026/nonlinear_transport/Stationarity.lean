import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace ClockStationarity

/- The two-sided-minimum argument and restoring derivative are derived in
stationary.py/README.md. This proves their coefficient implication, not an
observational law or a theorem about the nonlinear constraint operator. -/
theorem required_hessian (A q U B : ℝ) (hU : U≠0)
    (h : U*(B-A/q)=2*A^2) : B=A/q+2*A^2/U := by
  have he : B-A/q=2*A^2/U := (eq_div_iff hU).2 (by simpa [mul_comm] using h)
  linarith

theorem logarithmic_restoring_cancellation (X U d : ℝ)
    (h : U-2*d*X≠0) : (d*U/(U-2*d*X))*(U-2*d*X)-d*U=0 := by
  rw [div_mul_cancel₀ _ h]
  ring

#print axioms required_hessian
#print axioms logarithmic_restoring_cancellation
end ClockStationarity
