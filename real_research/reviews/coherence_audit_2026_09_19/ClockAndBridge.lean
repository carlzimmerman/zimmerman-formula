import Mathlib

/-!
Algebraic certificates for the September 19 review. Geometry and the extraction
of a determinant from the action are checked separately in check.py; they are
NOT formalized here. No cosmological viability or full Dirac count is asserted.
-/
namespace CoherenceAudit

/-- The missing extrinsic-curvature term cancels the homogeneous FRW Hessian.
Here K = 3 H, Q = n(phi). -/
theorem intrinsic_frw_cancellation (H Q : ℝ) :
    (-3 * H * Q) + (3 * H) * Q = 0 := by ring

theorem projected_frw_square (H Q : ℝ) :
    (-3 * H * Q)^2 = 9 * H^2 * Q^2 := by ring

/-- Linearized spatial projection: metric/shift terms cancel, leaving the
Laplacian of the relative scalar P - Q T. lapP/lapT are input symbols. -/
theorem relative_laplacian (lapP lapT shiftDiv phiDot Q : ℝ) :
    (lapP + Q * shiftDiv + 3 * Q * phiDot)
      + Q * (-lapT - shiftDiv - 3 * phiDot) = lapP - Q * lapT := by ring

theorem relative_scalar_gauge_invariant (P T Q z : ℝ) :
    (P - Q*z) - Q*(T-z) = P-Q*T := by ring

/-- The clock factor in the k^4 coefficient of the determinant, after
beta=(2-KB)/(2-c14), is 2 c14 (2-c14) (gap-W).
The determinant extraction is a separate symbolic-computation obligation. -/
noncomputable def clockGap (F Q KB c14 : ℝ) : ℝ :=
    ((2-KB)^2*Q^2/(2-c14) + F*Q/2)/c14

theorem clock_factor (F Q KB c14 W : ℝ)
    (hc : c14 ≠ 0) (h2 : 2-c14 ≠ 0) :
    -F*Q*c14 + 2*F*Q + 2*KB^2*Q^2 - 8*KB*Q^2 + 8*Q^2
      + 2*c14^2*W - 4*c14*W
    = 2*c14*(2-c14)*(clockGap F Q KB c14-W) := by
  unfold clockGap
  field_simp
  ring

/-- Changing the curvature F_QQ cannot change this displayed gap at fixed
slope F_Q and Q. This is a criterion for the frozen-background polynomial,
not a theorem that the exact expanding spacetime is unstable. -/
theorem clock_gap_negative_iff (F Q KB c14 : ℝ) (hc : 0 < c14) :
    clockGap F Q KB c14 < 0 ↔
      (2-KB)^2*Q^2/(2-c14) < -(F*Q)/2 := by
  unfold clockGap
  rw [div_lt_iff₀ hc]
  constructor <;> intro h <;> linarith

/-- Universal version of the YM07 toy-model obstruction: a term linear in
vacuum/loop mixing cannot be bounded by a fixed multiple of the quadratic
loop occupation arbitrarily near the electric vacuum. -/
theorem no_linear_by_quadratic_bound (C : ℝ) (hC : 0 < C) :
    ∃ e : ℝ, 0 < e ∧ C*e^2 < e/4 := by
  refine ⟨1/(8*C), by positivity, ?_⟩
  have hi : 0 < 1/C := by positivity
  have he : (1/(8*C))/4 - C*(1/(8*C))^2 = (1/C)/64 := by
    field_simp
    ring
  have hp : 0 < (1/C)/64 := by positivity
  linarith

/-- Exact normalized state epsilon=1/100: loop occupation=1/10001,
|magnetic deficit|=25/10001, proposed bound=(13/2)*occupation. -/
theorem ym07_counterexample :
    (13/2 : ℚ)*(1/10001) < 25/10001 := by norm_num

theorem electric_vacuum_not_ground_in_toy_model :
    (12 : ℚ)*(1/10001) - 25/10001 = -13/10001 ∧
      (-13/10001 : ℚ) < 0 := by norm_num

#print axioms intrinsic_frw_cancellation
#print axioms projected_frw_square
#print axioms relative_laplacian
#print axioms relative_scalar_gauge_invariant
#print axioms clock_factor
#print axioms clock_gap_negative_iff
#print axioms no_linear_by_quadratic_bound
#print axioms ym07_counterexample
#print axioms electric_vacuum_not_ground_in_toy_model
end CoherenceAudit
