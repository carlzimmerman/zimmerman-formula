import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Local clock geometry, conditional on a Lorentz metric of signature -+++.
This is algebra at one event, not a derivation of a spacetime manifold,
the origin of time, a thermodynamic arrow, or the dynamics of the full action.
The normalization s is assumed positive and to obey the timelike norm identity.
No axiom identifies the scalar clock rate with an atomic clock reading.
Positive rescaling invariance below is a geometric identity; it is not a claim
that clock reparameterization is a symmetry of P(X,tau)-V+s W(Y,tau).
-/

namespace LocalClockGeometry

noncomputable section

structure Four where
  t : ℝ
  x : ℝ
  y : ℝ
  z : ℝ

def minkowskiNorm (v : Four) : ℝ := -v.t^2 + v.x^2 + v.y^2 + v.z^2

def clockPairing (dτ v : Four) : ℝ :=
  dτ.t*v.t + dτ.x*v.x + dτ.y*v.y + dτ.z*v.z

def clockNormal (dτ : Four) (s : ℝ) : Four :=
  ⟨dτ.t/s, -dτ.x/s, -dτ.y/s, -dτ.z/s⟩

def scale (c : ℝ) (v : Four) : Four := ⟨c*v.t, c*v.x, c*v.y, c*v.z⟩

theorem normalized_clock_is_unit_timelike
    (dτ : Four) (s : ℝ) (hs : 0 < s)
    (ht : s^2 = dτ.t^2-dτ.x^2-dτ.y^2-dτ.z^2) :
    minkowskiNorm (clockNormal dτ s) = -1 := by
  have hn : s ≠ 0 := ne_of_gt hs
  unfold minkowskiNorm clockNormal
  dsimp
  field_simp
  nlinarith [ht]

theorem clock_increases_along_normal
    (dτ : Four) (s : ℝ) (hs : 0 < s)
    (ht : s^2 = dτ.t^2-dτ.x^2-dτ.y^2-dτ.z^2) :
    clockPairing dτ (clockNormal dτ s) = s := by
  have hn : s ≠ 0 := ne_of_gt hs
  unfold clockPairing clockNormal
  dsimp
  field_simp
  nlinarith [ht]

theorem clock_normal_pairing_positive
    (dτ : Four) (s : ℝ) (hs : 0 < s)
    (ht : s^2 = dτ.t^2-dτ.x^2-dτ.y^2-dτ.z^2) :
    0 < clockPairing dτ (clockNormal dτ s) := by
  rw [clock_increases_along_normal dτ s hs ht]
  exact hs

theorem positive_rescaling_preserves_normal
    (dτ : Four) (s c : ℝ) (hs : 0 < s) (hc : 0 < c) :
    clockNormal (scale c dτ) (c*s) = clockNormal dτ s := by
  have hs0 : s ≠ 0 := ne_of_gt hs
  have hc0 : c ≠ 0 := ne_of_gt hc
  cases dτ
  unfold clockNormal scale
  congr 1 <;> field_simp

theorem positive_rescaling_preserves_timelike_identity
    (dτ : Four) (s c : ℝ)
    (ht : s^2 = dτ.t^2-dτ.x^2-dτ.y^2-dτ.z^2) :
    (c*s)^2 = (scale c dτ).t^2-(scale c dτ).x^2
      -(scale c dτ).y^2-(scale c dτ).z^2 := by
  dsimp [scale]
  nlinarith [mul_nonneg (sq_nonneg c) (sq_nonneg s), congrArg (fun x : ℝ => c^2*x) ht]

#print axioms normalized_clock_is_unit_timelike
#print axioms clock_increases_along_normal
#print axioms clock_normal_pairing_positive
#print axioms positive_rescaling_preserves_normal
#print axioms positive_rescaling_preserves_timelike_identity

end
end LocalClockGeometry
