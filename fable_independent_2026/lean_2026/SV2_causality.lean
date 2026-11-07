/-
SV2 (closure_2026_11_06/SV2_causality, criteria 7d31bb0ac2), iter_1 line P1: tau-ordering excludes closed
signalling loops for every observer.
(a) grad tau future timelike => tau advances along every future causal displacement (reverse Cauchy-Schwarz).
(b) a chain of legs with d tau >= 0 and one leg > 0 has total d tau > 0: it cannot close.
(c) a luminal return leg to an emitter moving at |w| < c arrives at t >= L/(c + |w|) > 0.
(d) a boosted observer can see an instantaneous leg run backward in its own time (so (a)-(c) carry the content).
Lean certifies only the algebra. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SV2C

theorem tau_advances {u0 u1 u2 u3 k0 k1 k2 k3 : ℝ} (hu0 : 0 < u0) (hk0 : 0 < k0)
    (hu : u1 ^ 2 + u2 ^ 2 + u3 ^ 2 < u0 ^ 2) (hk : k1 ^ 2 + k2 ^ 2 + k3 ^ 2 ≤ k0 ^ 2) :
    0 < u0 * k0 - (u1 * k1 + u2 * k2 + u3 * k3) := by
  have hcs : (u1 * k1 + u2 * k2 + u3 * k3) ^ 2 ≤ (u1 ^ 2 + u2 ^ 2 + u3 ^ 2) * (k1 ^ 2 + k2 ^ 2 + k3 ^ 2) := by
    nlinarith [sq_nonneg (u1 * k2 - u2 * k1), sq_nonneg (u1 * k3 - u3 * k1), sq_nonneg (u2 * k3 - u3 * k2)]
  have h1 : (u1 ^ 2 + u2 ^ 2 + u3 ^ 2) * (k1 ^ 2 + k2 ^ 2 + k3 ^ 2) < u0 ^ 2 * k0 ^ 2 := by
    calc (u1 ^ 2 + u2 ^ 2 + u3 ^ 2) * (k1 ^ 2 + k2 ^ 2 + k3 ^ 2)
        ≤ (u1 ^ 2 + u2 ^ 2 + u3 ^ 2) * k0 ^ 2 := by
          apply mul_le_mul_of_nonneg_left hk; positivity
      _ < u0 ^ 2 * k0 ^ 2 := by
          apply mul_lt_mul_of_pos_right hu; positivity
  have h3 : 0 < u0 * k0 := mul_pos hu0 hk0
  by_contra hcon
  push_neg at hcon
  have h4 : u0 * k0 ≤ u1 * k1 + u2 * k2 + u3 * k3 := by linarith
  have h5 : (u0 * k0) ^ 2 ≤ (u1 * k1 + u2 * k2 + u3 * k3) ^ 2 := by
    apply pow_le_pow_left₀ h3.le h4
  nlinarith

theorem chain_advances {ι : Type*} (s : Finset ι) (d : ι → ℝ) (hnn : ∀ i ∈ s, 0 ≤ d i)
    (hpos : ∃ i ∈ s, 0 < d i) : 0 < ∑ i ∈ s, d i :=
  Finset.sum_pos' hnn hpos

theorem no_closed_loop {ι : Type*} (s : Finset ι) (d : ι → ℝ) (hnn : ∀ i ∈ s, 0 ≤ d i)
    (hpos : ∃ i ∈ s, 0 < d i) : ∑ i ∈ s, d i ≠ 0 :=
  ne_of_gt (chain_advances s d hnn hpos)

theorem luminal_return {c w L t : ℝ} (hc : 0 < c) (hL : 0 < L)
    (hreach : L - |w| * t ≤ c * t) : L / (c + |w|) ≤ t ∧ 0 < t := by
  have hd : 0 < c + |w| := by positivity
  have h1 : L ≤ (c + |w|) * t := by linarith
  have h2 : L / (c + |w|) ≤ t := by
    rw [div_le_iff₀ hd]; linarith
  exact ⟨h2, lt_of_lt_of_le (div_pos hL hd) h2⟩

theorem boosted_backward {g w L c : ℝ} (hg : 0 < g) (hwL : 0 < w * L) (hc : 0 < c) :
    -g * (w * L) / c ^ 2 < 0 := by
  have : 0 < g * (w * L) / c ^ 2 := by positivity
  have e : -g * (w * L) / c ^ 2 = -(g * (w * L) / c ^ 2) := by ring
  rw [e]; linarith

end SV2C

#print axioms SV2C.tau_advances
#print axioms SV2C.chain_advances
#print axioms SV2C.no_closed_loop
#print axioms SV2C.luminal_return
#print axioms SV2C.boosted_backward
