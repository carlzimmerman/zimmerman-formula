import Std

/- Exact rational premise audit only. No claim to derive a physical constant. -/
namespace AZ18

def coefficient (b : Rat) : Rat := 1 / (2 * b)

structure TwoChannelCarrier where
  channels : Nat
  normalization : Rat
  two_channels : channels = 2
  positive_normalization : 0 < normalization

def unitCarrier : TwoChannelCarrier := ⟨2, 1, rfl, by decide +kernel⟩
def doubledCarrier : TwoChannelCarrier := ⟨2, 2, rfl, by decide +kernel⟩

theorem known_answer : coefficient unitCarrier.normalization = 1/2 := by decide +kernel

theorem conditional_half (b : Rat) (normalization_fixed : b = 1) :
    coefficient b = 1/2 := by
  rw [normalization_fixed]
  decide +kernel

theorem alternate_normalization : coefficient doubledCarrier.normalization = 1/4 := by
  decide +kernel

theorem two_channels_do_not_fix_normalization :
    ∃ C : TwoChannelCarrier, coefficient C.normalization ≠ 1/2 := by
  exact ⟨doubledCarrier, by decide +kernel⟩

/-- This matches the logical form of PD07, not its unproved physical bridge. -/
theorem reciprocal_count_implication (k : Rat) (n : Nat)
    (reciprocal_count : k = 1 / (n : Rat)) (two : n = 2) : k = 1/2 := by
  subst n
  exact reciprocal_count

end AZ18
#print axioms AZ18.known_answer
#print axioms AZ18.conditional_half
#print axioms AZ18.alternate_normalization
#print axioms AZ18.two_channels_do_not_fix_normalization
#print axioms AZ18.reciprocal_count_implication
