import Mathlib
namespace InventoryBounds
-- Common coupling multiplier cancels in any steady balance if nonzero.
theorem cancel_coupling (k S A n : ℝ) (hk : k ≠ 0)
    (h : k*S-k*A*n^2=0) : S=A*n^2 := by
  have hz : k*(S-A*n^2)=0 := by nlinarith [h]
  have ht := (mul_eq_zero.mp hz).resolve_left hk
  linarith
-- Additional nonnegative one-body loss lowers the steady density squared.
theorem loss_bound (S A n loss : ℝ) (hA : 0 < A)
    (hn : 0 ≤ n) (hl : 0 ≤ loss)
    (h : S-A*n^2-loss*n=0) : n^2 ≤ S/A := by
  apply (le_div_iff₀ hA).2
  have hp : 0 ≤ loss*n := mul_nonneg hl hn
  nlinarith
-- The same pair source and sink cannot change the charge difference.
theorem paired_charge_rate (R A np nm : ℝ) :
    (R-A*np*nm)-(R-A*np*nm)=0 := by ring
end InventoryBounds
#print axioms InventoryBounds.cancel_coupling
#print axioms InventoryBounds.loss_bound
#print axioms InventoryBounds.paired_charge_rate
