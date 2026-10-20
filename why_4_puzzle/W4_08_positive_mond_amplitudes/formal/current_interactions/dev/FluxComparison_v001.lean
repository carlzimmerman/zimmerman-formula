module

public import Mathlib.Algebra.Order.Field.Basic
meta import Mathlib.Tactic.Ring.Basic
meta import Mathlib.Tactic.Linarith.Frontend

@[expose] public section

/-!
Jet and energy algebra for the compact-profile electric-flux trial.
Mixed partial equality, admissibility, integration, and the physical
variational upper bound are explicit analytic inputs, not field theorems
formalized here. No microscopic normalization is selected.
-/

namespace Why4.FluxComparison

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

theorem gauss_trial_jet
    (k d u ux uy vx vy vxy vyx : K) (hmixed : vxy = vyx) :
    -k * d ^ 2 * (ux * vy + u * vxy) +
      k * d ^ 2 * (uy * vx + u * vyx) =
      -k * d ^ 2 * (ux * vy - uy * vx) := by
  rw [hmixed]
  ring1

theorem maxwell_trial_energy (k d u vx vy : K) :
    ((-k * d ^ 2 * u * vy) ^ 2 + (k * d ^ 2 * u * vx) ^ 2) / 2 =
      k ^ 2 * d ^ 4 * u ^ 2 * (vx ^ 2 + vy ^ 2) / 2 := by
  ring1

theorem quartic_upper_excludes_cubic
    (E d C4 C3 : K) (hd : 0 < d)
    (hupper : E ≤ C4 * d ^ 4) (hsmall : C4 * d < C3) :
    E < C3 * d ^ 3 := by
  have hmul := mul_lt_mul_of_pos_right hsmall (pow_pos hd 3)
  have hpow : C4 * d ^ 4 = (C4 * d) * d ^ 3 := by ring1
  rw [hpow] at hupper
  exact lt_of_le_of_lt hupper hmul

#check @gauss_trial_jet
#check @maxwell_trial_energy
#check @quartic_upper_excludes_cubic
#print axioms gauss_trial_jet
#print axioms maxwell_trial_energy
#print axioms quartic_upper_excludes_cubic

end Why4.FluxComparison
