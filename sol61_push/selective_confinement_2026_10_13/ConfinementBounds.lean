import Mathlib
namespace ConfinementBounds
 theorem positive_effective (d k g mu : ℝ) (hd : 0 < d) (hk : 0 < k)
  (hgap : g^2 < k*d) (hmu : mu ≤ 0) : 0 < k-g^2/(d-2*mu) := by
  have hden : 0 < d-2*mu := by linarith
  have hkm : k*mu ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (le_of_lt hk) hmu
  apply sub_pos.mpr
  apply (div_lt_iff₀ hden).2
  nlinarith
 theorem stationary_contradiction (mu N T e U : ℝ) (hm : mu ≤ 0)
  (hN : 0 ≤ N) (hT : 0 ≤ T) (he : 0 < e) (hU : 0 < U)
  (hbalance : T+2*e*U ≤ mu*N) : False := by
  have hl : mu*N ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hm hN
  have hp : 0 < e*U := mul_pos he hU
  nlinarith
 theorem selective_window (u E : ℝ) (hE : 0 < E) :
  u < u+E/2 ∧ u+E/2 < u+E := by constructor <;> linarith
end ConfinementBounds
#print axioms ConfinementBounds.positive_effective
#print axioms ConfinementBounds.stationary_contradiction
#print axioms ConfinementBounds.selective_window
