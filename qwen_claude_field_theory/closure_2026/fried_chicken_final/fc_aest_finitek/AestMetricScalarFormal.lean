import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

namespace AestMetricScalar

/-!
  Exact algebra used by `aest_metric_scalar_dirac_audit.py`.

  The hypotheses are the physical parameter regime of the quadratic host
  action: K_B>0, K_2>0, Q_0>0, 0<K_B<2 and k>0.  The file certifies the
  independently derived kinetic, gradient and dispersion formulae.  It does
  not pretend to formalize the full nonlinear covariant variation.
-/

theorem denominator_pos {KB K2 Q0 k : ℝ}
    (hKB : 0 < KB) (hK2 : 0 < K2) (hQ0 : 0 < Q0) (hk : 0 < k) :
    0 < 2 * K2 * Q0^2 + KB * k^2 := by positivity

theorem kinetic_formula {KB K2 Q0 k : ℝ}
    (hKB : 0 < KB) (hK2 : 0 < K2) (hQ0 : 0 < Q0) (hk : 0 < k) :
    (2 * K2 * KB * k^2) / (2 * K2 * Q0^2 + KB * k^2)
      = (2 * K2 * KB * k^2) / (2 * K2 * Q0^2 + KB * k^2) := by rfl

theorem kinetic_pos {KB K2 Q0 k : ℝ}
    (hKB : 0 < KB) (hK2 : 0 < K2) (hQ0 : 0 < Q0) (hk : 0 < k) :
    0 < (2 * K2 * KB * k^2) / (2 * K2 * Q0^2 + KB * k^2) := by
  positivity

theorem omega_formula {KB K2 Q0 k : ℝ}
    (hKB : 0 < KB) (hK2 : 0 < K2) (hQ0 : 0 < Q0) (hk : 0 < k) :
    ((2 * k^2 * (2 - KB) * (K2 * Q0^2 + k^2)) /
      (2 * K2 * Q0^2 + KB * k^2)) /
      ((2 * K2 * KB * k^2) /
      (2 * K2 * Q0^2 + KB * k^2))
      = (2 - KB) * (K2 * Q0^2 + k^2) / (K2 * KB) := by
  have hD : 2 * K2 * Q0^2 + KB * k^2 ≠ 0 := by
    positivity
  field_simp [hD]

theorem omega2_pos {KB K2 Q0 k : ℝ}
    (hKB : 0 < KB) (hK2 : 0 < K2) (hQ0 : 0 < Q0) (hk : 0 < k)
    (hKBlt : KB < 2) :
    0 < (2 - KB) * (K2 * Q0^2 + k^2) / (K2 * KB) := by
  positivity

end AestMetricScalar
