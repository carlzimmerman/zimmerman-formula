import Mathlib

/-!
Static equilibrium and a reciprocal energy ledger do not select dynamics.
This is an abstract transfer countermodel, not a halo mechanism. q is one
population's mass and B-q the other; E = D*q + H. Their local derivatives
are supplied explicitly. No cosmology or MOND law enters the model.
-/
noncomputable section
namespace StaticIsNotAttractor

def transfer (rate target q : ℝ) : ℝ := -rate * (q - target)

/-- Every rate shares the same equilibrium, including the unstable sign. -/
theorem shared_equilibrium (rate target : ℝ) : transfer rate target target = 0 := by
  unfold transfer
  ring

/-- Reciprocal population transfers preserve the total mass. -/
theorem mass_ledger (rate target q : ℝ) :
    transfer rate target q + (-transfer rate target q) = 0 := by ring

/-- The reciprocal receiver reaction conserves energy for every rate sign. -/
theorem energy_ledger (D rate target q : ℝ) :
    D * transfer rate target q + (-D * transfer rate target q) = 0 := by ring

/-- The supplied chain-rule derivative of squared target error. -/
theorem squared_error_rate (rate target q : ℝ) :
    2 * (q - target) * transfer rate target q = -2 * rate * (q - target)^2 := by
  unfold transfer
  ring

/-- Positive rate contracts the target error away from equilibrium. -/
theorem positive_rate_decreases (rate target q : ℝ) (hr : 0 < rate)
    (hne : q ≠ target) : 2 * (q - target) * transfer rate target q < 0 := by
  rw [squared_error_rate]
  have hs : 0 < (q - target)^2 := sq_pos_of_ne_zero (sub_ne_zero.mpr hne)
  nlinarith [mul_pos hr hs]

/-- Reversing the rate increases target error while preserving both ledgers. -/
theorem negative_rate_increases (rate target q : ℝ) (hr : 0 < rate)
    (hne : q ≠ target) : 0 < 2 * (q - target) * transfer rate target q := by
  rw [squared_error_rate]
  have hs : 0 < (q - target)^2 := sq_pos_of_ne_zero (sub_ne_zero.mpr hne)
  nlinarith [mul_neg_of_neg_of_pos hr hs]

/-- Nontrivial positive populations witness the unstable case locally.
The state is interior to a total mass B; the conclusion is not global
positivity after the unstable flow reaches the boundary. -/
theorem admissible_unstable_state (B target ε : ℝ)
    (ht : 0 < target) (he : 0 < ε) (hs : target + ε < B) :
    0 < target + ε ∧ 0 < B - (target + ε) ∧
    transfer (-1) target target = 0 ∧
    transfer (-1) target (target + ε) + (-transfer (-1) target (target + ε)) = 0 ∧
    0 < 2 * ((target + ε) - target) * transfer (-1) target (target + ε) := by
  refine ⟨by linarith, by linarith, shared_equilibrium _ _, mass_ledger _ _ _, ?_⟩
  exact negative_rate_increases (-1) target (target + ε) (by norm_num) (by linarith)

end StaticIsNotAttractor

#print axioms StaticIsNotAttractor.shared_equilibrium
#print axioms StaticIsNotAttractor.mass_ledger
#print axioms StaticIsNotAttractor.energy_ledger
#print axioms StaticIsNotAttractor.squared_error_rate
#print axioms StaticIsNotAttractor.positive_rate_decreases
#print axioms StaticIsNotAttractor.negative_rate_increases
#print axioms StaticIsNotAttractor.admissible_unstable_state
