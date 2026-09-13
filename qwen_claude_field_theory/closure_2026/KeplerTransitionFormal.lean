import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Algebraic certificate for the orbital laws used by the exact-exponential
    Kepler prediction.  The dynamical input is only the spherical field
    equation; no observed value or desired ratio is hard-coded. -/

namespace KeplerTransition

theorem circular_frequency_ratio
    {G M r g mu omegaSq omegaNSq : ℝ}
    (hG : G ≠ 0) (hM : M ≠ 0) (hr : r ≠ 0) (hmu : mu ≠ 0)
    (hfield : mu * g * r ^ 2 = G * M)
    (hOmega : omegaSq = g / r)
    (hOmegaN : omegaNSq = G * M / r ^ 3) :
    omegaSq / omegaNSq = 1 / mu := by
  rw [hOmega, hOmegaN]
  field_simp [hG, hM, hr, hmu]
  nlinarith [hfield]

theorem circular_period_ratio
    {G M r g mu pSq pNSq : ℝ}
    (hG : G ≠ 0) (hM : M ≠ 0) (hr : r ≠ 0) (hg : g ≠ 0) (hmu : mu ≠ 0)
    (hfield : mu * g * r ^ 2 = G * M)
    (hP : pSq = r / g)
    (hPN : pNSq = r ^ 3 / (G * M)) :
    pSq / pNSq = mu := by
  rw [hP, hPN]
  field_simp [hG, hM, hr, hg, hmu]
  nlinarith [hfield]

theorem epicyclic_ratio
    {A omegaSq dlogg kappaSq : ℝ}
    (hA : A ≠ 0)
    (hdlogg : dlogg = -2 / A)
    (hkappa : kappaSq = omegaSq * (4 + (dlogg - 1)))
    (homega : omegaSq ≠ 0) :
    kappaSq / omegaSq = 3 - 2 / A := by
  rw [hkappa, hdlogg]
  field_simp [hA, homega]
  ring

end KeplerTransition
