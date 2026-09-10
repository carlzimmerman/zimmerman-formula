import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-! Exact algebra for the parameter-free deep-MOND action-angle invariant. -/

namespace ActionAngleInvariant

theorem single_orbit_cancellation
    (F J R v S : ℝ)
    (hF : F ≠ 0) (hJ : J ≠ 0) (hR : R ≠ 0) (hv : v ≠ 0)
    (hscale : S = v ^ 2) :
    (F * R / v) * S / (J * R * v) = F / J := by
  rw [hscale]
  field_simp [hJ, hR, hv]

theorem two_orbit_cancellation
    (F1 F2 J1 J2 R v : ℝ)
    (hF2 : F2 ≠ 0) (hJ1 : J1 ≠ 0) (hR : R ≠ 0)
    (hv : v ≠ 0) :
    ((F1 * R / v) * (J2 * R * v)) /
        ((F2 * R / v) * (J1 * R * v)) =
      (F1 * J2) / (F2 * J1) := by
  field_simp [hF2, hJ1, hR, hv]

end ActionAngleInvariant
