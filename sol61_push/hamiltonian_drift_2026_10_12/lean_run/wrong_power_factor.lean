import Mathlib

/-! Exact algebra conditional on the analytical Ito and orbit-averaging derivation.
No stochastic process, empirical halo, or microscopic reservoir is formalized. -/
noncomputable section
namespace HamiltonianDrift

theorem action_to_gap_drift (w wp d dp : ℝ) (hw : w ≠ 0) :
    (-2 * wp * d - w * dp) + (w ^ 2 * d) * (wp / w ^ 2) =
      -w * dp - wp * d := by
  field_simp
  ring

theorem density_of_states_current (d dp t tp f fp b : ℝ) (ht : t ≠ 0) :
    (dp + d * tp / t + b) * (t * f) -
      (dp * (t * f) + d * (tp * f + t * fp)) =
        b * t * f - d * t * fp := by
  field_simp
  ring

theorem selector_cancellation (d t f q : ℝ) :
    (-d / (2 * q)) * t * f - d * t * (-f / (2 * q)) = 0 := by
  ring

theorem selector_requires_extra_drift (d t f q b : ℝ)
    (ht : t ≠ 0) (hf : f ≠ 0)
    (h : b * t * f - d * t * (-f / (2 * q)) = 0) :
    b = -d / (2 * q) := by
  have hm : (b + d / (2 * q)) * (t * f) = 0 := by
    calc
      _ = b * t * f - d * t * (-f / (2 * q)) := by ring
      _ = 0 := h
  have hz := (mul_eq_zero.mp hm).resolve_right (mul_ne_zero ht hf)
  rw [neg_div]
  exact eq_neg_of_add_eq_zero_left hz

theorem regularized_mean_power (d a b : ℝ)
    (ha : a ≠ 0) (hb : b ≠ 0) (hba : b - a ≠ 0) :
    d * (1 / a - 1 / b) / (2 * (b - a)) = d / (a * b) := by
  field_simp

theorem momentum_kick_antidamping (k v q : ℝ) :
    (k / (2 * q)) * v = (k * v) / (2 * q) := by ring

end HamiltonianDrift
#print axioms HamiltonianDrift.action_to_gap_drift
#print axioms HamiltonianDrift.density_of_states_current
#print axioms HamiltonianDrift.selector_cancellation
#print axioms HamiltonianDrift.selector_requires_extra_drift
#print axioms HamiltonianDrift.regularized_mean_power
#print axioms HamiltonianDrift.momentum_kick_antidamping
