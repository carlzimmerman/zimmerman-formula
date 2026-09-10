import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace CubicSelectedEpoch

/- One reconstructed epoch: a=M2=1, gamma=1/1000000, A=1/10,
q=10/11, U=1/110, B0=231/100, qdot=-5H/77-1/(242H).
point_certificate.py compares THESE actual definitions to derive.py's actual
expressions by exact polynomial remainder modulo H^2=4/15 and checks original
denominators. That source bridge is not a Lean formalization of the action.
No history-wide, gradient, mass, observational, or nonlinear conclusion follows.
The physical lapse/shift elimination still excludes k=0. -/

noncomputable def pointD0 (H : ℝ) : ℝ :=
  (-1014222000*H - 74405562000183)/(86089080000*H + 15277942064032340)

noncomputable def pointD2 (H : ℝ) : ℝ :=
  (-2541000*H - 109)/(1639792000*H)

noncomputable def pointA0 (H : ℝ) : ℝ :=
  (204615295500363 - 483153000*H)/(998250000*H + 177156100000375)

theorem selected_epoch_signs (H : ℝ) (hH : 0 < H) (hsq : H^2 = 4/15) :
    pointD0 H < 0 ∧ pointD2 H < 0 ∧ 0 < pointA0 H := by
  have hlt : H < 1 := by nlinarith [sq_nonneg (H-1)]
  have hn0 : -1014222000*H - 74405562000183 < 0 := by nlinarith
  have hd0 : 0 < 86089080000*H + 15277942064032340 := by positivity
  have hn2 : -2541000*H - 109 < 0 := by nlinarith
  have hd2 : 0 < 1639792000*H := by positivity
  have hnA : 0 < 204615295500363 - 483153000*H := by nlinarith
  have hdA : 0 < 998250000*H + 177156100000375 := by positivity
  exact ⟨div_neg_of_neg_of_pos hn0 hd0,
         div_neg_of_neg_of_pos hn2 hd2, div_pos hnA hdA⟩

/-- The algebra holds for all nonnegative wave2; physical reduction needs k != 0. -/
theorem selected_epoch_schur_positive (H J wave2 : ℝ)
    (hH : 0 < H) (hsq : H^2 = 4/15) (hw : 0 ≤ wave2) :
    pointD0 H + pointD2 H*wave2 < 0 ∧
    0 < pointA0 H - J^2/(pointD0 H + pointD2 H*wave2) := by
  obtain ⟨h0, h2, hA⟩ := selected_epoch_signs H hH hsq
  have hp : pointD2 H*wave2 ≤ 0 :=
    mul_nonpos_of_nonpos_of_nonneg (le_of_lt h2) hw
  have hD : pointD0 H + pointD2 H*wave2 < 0 := by linarith
  have hr : J^2/(pointD0 H + pointD2 H*wave2) ≤ 0 :=
    div_nonpos_of_nonneg_of_nonpos (sq_nonneg J) (le_of_lt hD)
  exact ⟨hD, by linarith⟩

#print axioms selected_epoch_signs
#print axioms selected_epoch_schur_positive

end CubicSelectedEpoch
