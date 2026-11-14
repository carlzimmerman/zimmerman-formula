/-
BJ1: Lean statements for the algebra of the charge-budget junction. They certify the algebra, not the physics, and no
number or label of the lane. Written by the lead. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  under_branch_monotone : in the "under" branch the law's enclosed charge inside R_set never exceeds the captured
                          charge, so the emptied shell keeps the layout non-decreasing.
  under_gap_to_reference : and the captured charge never exceeds the reference's enclosed charge beyond the caustic.
  equal_charge_no_rescale : at a radius where the law's and the reference's enclosed charges agree, FZS1's factor s
                          and the exact junction's factor t are both 1: nothing is rescaled.
  no_charge_crosses    : the charge inside the capture surface is the reference's: (law inside) + (emptied shell)
                          adds nothing and removes nothing.
-/
import Mathlib

namespace BJ1

theorem under_branch_monotone (CBr CBset Q : ℝ) (h1 : CBr ≤ CBset) (h2 : CBset = Q) : CBr ≤ Q := by
  linarith

theorem under_gap_to_reference (Q CRk CRr : ℝ) (hQ : Q = CRk) (hmono : CRk ≤ CRr) : Q ≤ CRr := by
  linarith

theorem equal_charge_no_rescale (T CB CR : ℝ) (hT : T - CR ≠ 0) (hCB : CB ≠ 0) (heq : CB = CR) :
    (T - CB) / (T - CR) = 1 ∧ CR / CB = 1 := by
  subst heq
  exact ⟨div_self hT, div_self hCB⟩

theorem no_charge_crosses (CBset Q CRk : ℝ) (hset : CBset = Q) (hQ : Q = CRk) : CBset + (Q - CBset) = CRk := by
  linarith

end BJ1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
