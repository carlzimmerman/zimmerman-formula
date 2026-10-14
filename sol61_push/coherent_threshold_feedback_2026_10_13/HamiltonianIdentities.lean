import Mathlib

namespace CoherentThreshold
open scoped BigOperators

-- Tangent identity for a real source/continuum coupling and arbitrary real
-- mode energies, including a common density-dependent Hartree shift.
theorem norm_tangent {ι : Type*} (s : Finset ι) (x y D : ℝ)
    (a b v E : ι → ℝ) :
    2*x*(D*y + ∑ j ∈ s, v j*b j) +
    2*y*(-D*x - ∑ j ∈ s, v j*a j) +
    (∑ j ∈ s, (2*a j*(E j*b j+v j*y) +
                 2*b j*(-E j*a j-v j*x))) = 0 := by
  have h : (∑ j ∈ s, (2*a j*(E j*b j+v j*y) +
                 2*b j*(-E j*a j-v j*x))) =
      2*y*(∑ j ∈ s, v j*a j) - 2*x*(∑ j ∈ s, v j*b j) := by
    simp only [Finset.mul_sum, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro j hj
    ring
  rw [h]
  ring

-- Canonical Hamiltonian gradient cancellation. Deriving the gradient and
-- applying the chain rule to a solution are separate mathematical obligations.
theorem energy_tangent {ι : Type*} (s : Finset ι) (Hx Hy : ℝ)
    (Hu Hv : ι → ℝ) :
    Hx*(Hy/2) + Hy*(-Hx/2) +
    (∑ j ∈ s, (Hu j*(Hv j/2)+Hv j*(-Hu j/2))) = 0 := by
  have h : (∑ j ∈ s, (Hu j*(Hv j/2)+Hv j*(-Hu j/2))) = 0 := by
    apply Finset.sum_eq_zero
    intro j hj
    ring
  rw [h]
  ring
end CoherentThreshold

#print axioms CoherentThreshold.norm_tangent
#print axioms CoherentThreshold.energy_tangent
