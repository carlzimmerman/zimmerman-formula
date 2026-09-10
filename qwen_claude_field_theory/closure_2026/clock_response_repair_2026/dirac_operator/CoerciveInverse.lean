import Mathlib.Analysis.InnerProductSpace.LaxMilgram

open InnerProductSpace

namespace ClockLapseInverse

/- This is a conditional Hilbert-space inverse certificate. The Sobolev-space
realization and coercivity of the actual spatial operator are separate proof
obligations; this theorem does not assume they have been established globally. -/
theorem unique_weak_solution {V : Type*} [NormedAddCommGroup V]
    [InnerProductSpace ℝ V] [CompleteSpace V]
    (B : V →L[ℝ] V →L[ℝ] ℝ) (hc : IsCoercive B) (f : V) :
    ∃! u : V, ∀ w : V, B u w = ⟪f,w⟫_ℝ := by
  let e := hc.continuousLinearEquivOfBilin
  refine ⟨e.symm f, ?_, ?_⟩
  · intro w
    rw [← hc.continuousLinearEquivOfBilin_apply]
    change ⟪e (e.symm f),w⟫_ℝ = ⟪f,w⟫_ℝ
    rw [e.apply_symm_apply]
  · intro y hy
    apply e.injective
    rw [e.apply_symm_apply]
    exact (hc.unique_continuousLinearEquivOfBilin (fun w => (hy w).symm)).symm

#print axioms unique_weak_solution
end ClockLapseInverse
