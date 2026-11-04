import Std
/- Rational controls for the derived local branch; not a physical kappa theorem. -/
namespace AZ19

def branch (b g s t : Rat) : Prop := b * g = s * t

theorem known_branch : branch 2 1 1 2 := by decide +kernel

theorem shifted_source_branch : branch 1 2 1 2 := by decide +kernel

theorem source_dependence_witness :
    ∃ b₁ b₂ g₁ g₂ : Rat,
      0 < b₁ ∧ 0 < b₂ ∧ 0 < g₁ ∧ 0 < g₂ ∧
      branch b₁ g₁ 1 2 ∧ branch b₂ g₂ 1 2 ∧ b₁ ≠ b₂ := by
  exact ⟨2, 1, 1, 2, by decide +kernel⟩

theorem frozen_b_fails_changed_source : ¬ branch 2 2 1 2 := by decide +kernel
end AZ19
#print axioms AZ19.known_branch
#print axioms AZ19.shifted_source_branch
#print axioms AZ19.source_dependence_witness
#print axioms AZ19.frozen_b_fails_changed_source
