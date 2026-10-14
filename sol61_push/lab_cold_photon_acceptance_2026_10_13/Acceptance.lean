import Mathlib

namespace LabColdAcceptance

-- If the two daughter kinetic energies are a+b and a-b, BOTH pass exactly
-- when their common part plus the absolute boost term passes.
theorem both_daughters (a b limit : ℝ) :
    (a+b ≤ limit ∧ a-b ≤ limit) ↔ a+|b| ≤ limit := by
  constructor
  · rintro ⟨h1,h2⟩
    have h : |b| ≤ limit-a := abs_le.mpr ⟨by linarith, by linarith⟩
    linarith
  · intro h
    have hb : |b| ≤ limit-a := by linarith
    rcases abs_le.mp hb with ⟨h1,h2⟩
    constructor <;> linarith

end LabColdAcceptance

#print axioms LabColdAcceptance.both_daughters
