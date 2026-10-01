import Mathlib

/-!
AS236 certificates (Tier-0b: cosmological versus local G for the centered clock).
Algebraic identities from the exact symbolic lane, certified in Lean 4.
- A: ratio-in-alpha equivalence used by the seed:  1/(1 - alpha/2) = -2/(alpha - 2)
- B: uncentered Friedmann coefficient bookkeeping: 3(1 + 3 c2/2) = 3 + (9/2) c2
- C: negative control fires: c2 != 0 -> uncentered coefficient != centered coefficient
- D: ratio chain: G_N = G_bare/c_N and G_cosm = G_bare imply  G_N/G_cosm = 1/c_N
-/

noncomputable section

open scoped Real

namespace AS236

lemma one_minus_half_ne (α : ℝ) (hα : α ≠ 2) : 1 - α / 2 ≠ 0 := by
  intro hz
  have : α = 2 := by linarith
  exact hα this

-- A: ratio in alpha, the seed's claim in closed form.
theorem ratio_in_alpha (α : ℝ) (hα : α ≠ 2) : 1 / (1 - α / 2) = -2 / (α - 2) := by
  have hd : 1 - α / 2 ≠ 0 := one_minus_half_ne α hα
  have h2d : 2 - α ≠ 0 := by
    intro hz
    have : α = 2 := by linarith
    exact hα this
  have hd2 : α - 2 ≠ 0 := by
    intro hz
    have : α = 2 := by linarith
    exact hα this
  have hrel : 1 - α / 2 = (2 - α) / 2 := by ring
  rw [hrel]
  field_simp [h2d, hd2]
  ring

-- B: uncentered Friedmann coefficient = centered coefficient + (9/2) c2 M_P^2 H^2
--    (factor bookkeeping, M_P^2 H^2 factored out)
theorem uncentered_coeff_factor (c2 : ℝ) :
    3 * (1 + (3:ℝ) / 2 * c2) = 3 + (9:ℝ) / 2 * c2 := by
  ring

-- C: negative control fires: with c2 != 0 the uncentered coefficient strictly
--    differs from the centered one.
theorem control_fires (c2 : ℝ) (hc : c2 ≠ 0) : 3 * (1 + (3:ℝ) / 2 * c2) ≠ 3 := by
  intro hz
  have hz2 : (9:ℝ) / 2 * c2 = 0 := by nlinarith
  have : c2 = 0 := by nlinarith
  exact hc this

-- D: ratio chain: G_N = G_bare/c_N, G_cosm = G_bare  =>  G_N/G_cosm = 1/c_N
theorem ratio_chain (G_N G_bare G_cosm c_N : ℝ)
    (h1 : G_N = G_bare / c_N) (h2 : G_cosm = G_bare)
    (hb : G_bare ≠ 0) (hc : c_N ≠ 0) : G_N / G_cosm = 1 / c_N := by
  rw [h1, h2]
  field_simp [hb, hc]

-- D2: same chain, expressed through alpha:  G_N/G_cosm = 1/(1 - alpha/2)
theorem ratio_chain_alpha (G_N G_bare G_cosm c_N α : ℝ)
    (h1 : G_N = G_bare / c_N) (h2 : G_cosm = G_bare) (h3 : c_N = 1 - α / 2)
    (hb : G_bare ≠ 0) (hα : α ≠ 2) :
    G_N / G_cosm = 1 / (1 - α / 2) := by
  rw [h1, h2, h3]
  have hc : 1 - α / 2 ≠ 0 := one_minus_half_ne α hα
  field_simp [hb, hc]

end AS236

/-! Axiom audit (unfiltered output, verified by the harness). -/

#print axioms AS236.ratio_in_alpha
#print axioms AS236.uncentered_coeff_factor
#print axioms AS236.control_fires
#print axioms AS236.ratio_chain
#print axioms AS236.ratio_chain_alpha