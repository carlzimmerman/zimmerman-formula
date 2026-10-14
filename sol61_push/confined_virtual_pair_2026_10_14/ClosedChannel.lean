import Mathlib
namespace ConfinedVirtualPair

theorem mediator_denominator_positive (E delta p M : ℝ)
    (hgap : E < delta) (hM : 0 < M) :
    0 < delta + p^2/(2*M) - E := by
  have hp : 0 ≤ p^2/(2*M) := by positivity
  linarith

theorem no_free_mediator_energy_match (E delta p M : ℝ)
    (hgap : E < delta) (hM : 0 < M) :
    E ≠ delta + p^2/(2*M) := by
  have h := mediator_denominator_positive E delta p M hgap hM
  intro he
  linarith
end ConfinedVirtualPair
#print axioms ConfinedVirtualPair.mediator_denominator_positive
#print axioms ConfinedVirtualPair.no_free_mediator_energy_match
