import Mathlib

/-! Audit of a previously fixed drift. Exact conditional algebra only.
Let A=alpha*d, D=d*x with x=q+q0>0; D'=d.
Density derivatives and Ito's transformation rule are analytical inputs,
not a formalized stochastic process. No new physical axioms are declared. -/
noncomputable section
namespace DriftAudit

def current (alpha d x n np : ℝ) : ℝ := (alpha * d - d) * n - d * x * np

theorem general_stationary_current (alpha d x n : ℝ) (hx : x ≠ 0) :
    current alpha d x n ((alpha - 1) * n / x) = 0 := by
  unfold current
  field_simp [hx]
  ring

theorem stationary_slope_necessary (alpha d x n np : ℝ)
    (hd : d ≠ 0) (hx : x ≠ 0) (h : current alpha d x n np = 0) :
    np = (alpha - 1) * n / x := by
  unfold current at h
  apply (eq_div_iff hx).mpr
  have hf : d * (np * x - (alpha - 1) * n) = 0 := by nlinarith [h]
  have hz := (mul_eq_zero.mp hf).resolve_left hd
  linarith

/-- alpha=1 admits a locally constant density, instead of the chosen inverse-square-root profile. -/
theorem constant_density_alternative (d x n : ℝ) :
    current 1 d x n 0 = 0 := by unfold current; ring

theorem transformed_drift (alpha d r : ℝ) (hr : r ≠ 0) :
    alpha * d / (2 * r) - d * r ^ 2 / (4 * r ^ 3) =
      d * (2 * alpha - 1) / (4 * r) := by
  field_simp [hr]
  ring

theorem zero_transformed_drift_iff (alpha d r : ℝ) (hd : d ≠ 0) (hr : r ≠ 0) :
    d * (2 * alpha - 1) / (4 * r) = 0 ↔ alpha = 1 := by
  constructor
  · intro h
    have hp : d * (2 * alpha - 1) = 0 :=
      (div_eq_zero_iff.mp h).resolve_right (mul_ne_zero (by norm_num) hr)
    have hz := (mul_eq_zero.mp hp).resolve_left hd
    linarith
  · intro h
    rw [h]
    ring

end DriftAudit
#print axioms DriftAudit.general_stationary_current
#print axioms DriftAudit.stationary_slope_necessary
#print axioms DriftAudit.constant_density_alternative
#print axioms DriftAudit.transformed_drift
#print axioms DriftAudit.zero_transformed_drift_iff
