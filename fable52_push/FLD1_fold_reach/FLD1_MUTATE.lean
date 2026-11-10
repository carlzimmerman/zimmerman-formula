/-
FLD1 MUTATE twin: the statements of FLD1.lean with a sign or factor flipped. Every theorem is false and must fail
(expected: exit 1, one error per theorem). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace FLD1_MUTATE

theorem share_of_radius_flip (X : ℝ) (hX : 0 ≤ X) : (-1 + Real.sqrt (1 + 4 * (X * (X + 1)))) / 2 = X + 1 := by
  have h : 1 + 4 * (X * (X + 1)) = (2 * X + 1) ^ 2 := by ring
  rw [h, Real.sqrt_sq (by linarith)]
  ring

theorem window_radius_flip (GM g1 g2 : ℝ) (hGM : 0 < GM) (h1 : 0 < g1) (h12 : g1 < g2) :
    Real.sqrt (GM / g1) < Real.sqrt (GM / g2) := by
  have hg2 : 0 < g2 := by linarith
  apply Real.sqrt_lt_sqrt (div_nonneg hGM.le hg2.le)
  exact div_lt_div_of_pos_left hGM h1 h12

theorem kepler_energy_flip (G M q k2 c s : ℝ) (hGM : G * M ≠ 0) (hq : q ≠ 0) (hc : 1 + c ≠ 0)
    (hk : k2 = q ^ 3 / (8 * (G * M))) (hs : s ^ 2 = 1 - c ^ 2) :
    (q ^ 2 * s ^ 2 / (4 * k2 * (1 + c) ^ 2)) / 2 - 2 * (G * M) / (q * (1 + c)) = -(G * M) / (2 * q) := by
  subst hk
  rw [hs]
  have h1 : 1 - c ^ 2 = (1 - c) * (1 + c) := by ring
  rw [h1]
  field_simp
  ring

end FLD1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
