import Mathlib

/-!
Necessary pointwise compatibility of the declared canonical ONE-real-scalar
source model, with no additional interaction stress. Receiver local energy
source is pi*S, and momentum source is -gradient*S. Cold sources q,m balance
them only when pi*S=-q and gradient*S=m. This physical dictionary is supplied,
not derived from tensor geometry here. Additional fields/stress alter the model.
-/
noncomputable section
namespace FrameworkScalarCompatibility

theorem source_compatibility (pi gradient S q m : ℝ)
    (hE : pi*S = -q) (hP : gradient*S = m) :
    gradient*q + pi*m = 0 := by
  have he : pi*S+q=0 := by linarith
  have hp : gradient*S-m=0 := by linarith
  linear_combination gradient*he-pi*hp

/-- Nonzero heat transfer with no cold recoil needs a zero local field gradient
within this one-source canonical model; no wider dark-sector no-go is claimed. -/
theorem zero_recoil_requires_flat (pi gradient S q : ℝ)
    (hq : q ≠ 0) (hE : pi*S = -q) (hP : gradient*S = 0) :
    gradient=0 := by
  have h := source_compatibility pi gradient S q 0 hE hP
  have hz : gradient*q=0 := by simpa using h
  exact (mul_eq_zero.mp hz).resolve_right hq

/-- A concrete local desired source pair lies outside the receiver's source span. -/
theorem no_source_for_unit_heat_zero_recoil :
    ¬ ∃ S : ℝ, (1 : ℝ)*S = -1 ∧ (1 : ℝ)*S = 0 := by
  rintro ⟨S,hE,hP⟩
  linarith

end FrameworkScalarCompatibility
#print axioms FrameworkScalarCompatibility.source_compatibility
#print axioms FrameworkScalarCompatibility.zero_recoil_requires_flat
#print axioms FrameworkScalarCompatibility.no_source_for_unit_heat_zero_recoil
