import Std

/- Integer witnesses for denominator-cleared reduced equations.
   Positive radius and reaction coefficient permit clearing denominators.
   No numerical halo, physical realizability or stability is certified. -/
namespace PhaseNonselection
abbrev balance (p delta sigma radius : Int) : Prop :=
  (p + delta) * radius = 2 * sigma
abbrev normalized (radius coefficient : Int) : Prop :=
  3 * coefficient = radius -- gravity=shape=reaction=1

theorem distinct_equilibria :
    balance 3 (-1) 3 3 ∧ balance 3 (-1) 6 6 ∧
    normalized 3 1 ∧ normalized 6 2 ∧
    (0 : Int) < 3 ∧ (0 : Int) < 6 ∧ (1 : Int) ≠ 2 := by decide

theorem balance_does_not_force_half :
    ¬ (∀ p delta sigma radius coefficient : Int,
      0 < sigma → 0 < radius → balance p delta sigma radius →
      normalized radius coefficient → 2 * coefficient = 1) := by
  intro h
  have bad := h 3 (-1) 3 3 1 (by decide) (by decide) (by decide) (by decide)
  have unequal : (2 : Int) * 1 ≠ 1 := by decide
  exact unequal bad

#print axioms distinct_equilibria
#print axioms balance_does_not_force_half
end PhaseNonselection
