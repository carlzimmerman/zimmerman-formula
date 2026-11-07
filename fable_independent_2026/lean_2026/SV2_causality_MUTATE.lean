/-
SV2_causality MUTATE twin: three planted false claims, each must fail.
M1: a SPACELIKE displacement (k0^2 < |k|^2) advances tau.
M2: a chain with no sign condition on its legs has positive total d tau.
M3: a luminal return leg arrives at t = 0 (closes the loop).
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SV2CM

theorem tau_advances_spacelike {u0 u1 u2 u3 k0 k1 k2 k3 : ℝ} (hu0 : 0 < u0) (hk0 : 0 < k0)
    (hu : u1 ^ 2 + u2 ^ 2 + u3 ^ 2 < u0 ^ 2) (hk : k0 ^ 2 < k1 ^ 2 + k2 ^ 2 + k3 ^ 2) :
    0 < u0 * k0 - (u1 * k1 + u2 * k2 + u3 * k3) := by
  nlinarith [sq_nonneg (u1 * k2 - u2 * k1), sq_nonneg (u1 * k3 - u3 * k1), sq_nonneg (u2 * k3 - u3 * k2),
    mul_pos hu0 hk0]

theorem chain_any_sign {ι : Type*} (s : Finset ι) (d : ι → ℝ)
    (hpos : ∃ i ∈ s, 0 < d i) : 0 < ∑ i ∈ s, d i := by
  obtain ⟨i, hi, h⟩ := hpos
  positivity

theorem luminal_return_zero {c w L t : ℝ} (hc : 0 < c) (hL : 0 < L)
    (hreach : L - |w| * t ≤ c * t) : t = 0 := by
  nlinarith [abs_nonneg w]

end SV2CM

#print axioms SV2CM.tau_advances_spacelike
#print axioms SV2CM.chain_any_sign
#print axioms SV2CM.luminal_return_zero
