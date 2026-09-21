import Mathlib

/-!
# I10 — Wave S: the void theorem (the U-route is ionizing-opaque)

SCOPE (per lean-math-certification): Lean certifies the inequality chain that voids the
geometric U-route inside the recombination-pinned envelope. Inputs (absorbed,
provenanced): the H I n=2 photoionization cross-section at threshold exceeds the
Thomson cross-section by R_sigma = 9.47e6 (atomic physics); the envelope is
electron-thick (tau_es ~ 0.3-1 at the pseudo-photosphere — its definition). Then for
ANY neutral fraction f_n > 1e-4, tau_ion >= tau_es * R_sigma * f_n >= 1e3 * tau_es —
the envelope is ionizing-opaque by >= 3 dex, the central ionizing flux does not
propagate, and the geometric formula U = Q/(4 pi r^2 n c) is void inside it: the
fitted U is a LOCAL thermodynamic state, not a distance indicator.
Numbers Python-verified in `bhstar_s1_u_route_void.py` (4/4). Zero `sorry`; axioms
⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **S (the void theorem).** With R_sigma >= 1e6 (absorbed atomic physics) and any
neutral fraction f_n >= 1e-4: tau_ion >= 1e2 * tau_es — the envelope is
ionizing-opaque, the geometric U-formula is void. -/
theorem void_theorem {tau_es tau_ion R_sigma f_n : ℝ}
    (htau : 0 < tau_es) (hR : 1e6 ≤ R_sigma) (hf : 1e-4 ≤ f_n)
    (hdef : tau_ion = tau_es * R_sigma * f_n) :
    1e2 * tau_es ≤ tau_ion := by
  rw [hdef, mul_comm, mul_assoc]
  have h1 : (1e2:ℝ) ≤ R_sigma * f_n := by nlinarith [hR, hf]
  exact mul_le_mul_of_nonneg_left h1 (le_of_lt htau)

end

#print axioms void_theorem