/-
BJ1 MUTATE twin: the statements of BJ1.lean with a sign or a term changed. Every theorem is false and must fail
(expected: exit 1, one error per theorem). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace BJ1_MUTATE

theorem under_branch_monotone_flip (CBr CBset Q : ℝ) (h1 : CBr ≤ CBset) (h2 : CBset = Q) : Q < CBr := by
  linarith

theorem equal_charge_no_rescale_flip (T CB CR : ℝ) (hT : T - CR ≠ 0) (hCB : CB ≠ 0) (heq : CB = CR) :
    (T - CB) / (T - CR) = 2 ∧ CR / CB = 1 := by
  subst heq
  exact ⟨div_self hT, div_self hCB⟩

theorem no_charge_crosses_flip (CBset Q CRk : ℝ) (hset : CBset = Q) (hQ : Q = CRk) : CBset + (Q - CBset) = CRk + 1 := by
  linarith

end BJ1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
