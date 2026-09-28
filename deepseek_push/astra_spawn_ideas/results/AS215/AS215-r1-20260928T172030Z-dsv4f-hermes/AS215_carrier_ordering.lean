-- AS215 -- criterion-B characteristic ordering test, TIER-0 seed
-- Certificate 1: carrier/tensor block ordering (CA5-GNC-R, vacuum/ACTION.md R1)
--
-- Claimed content (see derivation.md):
--  L1  For frozen t_c > 0 the carrier block symbol
--        X_C(w,k) = -w^2 + k^2 / t_c^2
--      is annihilated by its two real roots w = +/- k/t_c (substitution-back).
--  L2  Future-sheet contraction: with future normal n (N = X_tau^(-1/2) > 0),
--      the invariant identity  xi_mu tau^mu = -xi(n)/N  makes the d-tau
--      contraction of the future sheet strictly negative for w > 0, N > 0.
--  L3  Composite carrier metric: -g_d(d tau,d tau) = t_c^-2 X_tau > 0 for EVERY
--      t_c > 0 -- superluminal carrier (t_c < 1 -> v = c/t_c > c) never breaks
--      the foliation ordering ("no metric-cone speed restriction").
--  L4  Ghost control (NC-b): -X_C with the kinetic sign flipped has no real
--      root at all (ill-posed in tau): w^2 + v^2 k^2 > 0 for v*k != 0.
--
-- Zero sorry. Axioms must be a subset of {propext, Classical.choice, Quot.sound}.

import Mathlib

namespace AS215

-- L1 : substitution-back of the two real roots of the carrier symbol.
theorem carrier_root_subst (t k : ℝ) (ht : t ≠ 0) :
    -((k / t) ^ 2) + k ^ 2 / t ^ 2 = 0 := by
  field_simp [ht]
  ring

-- L1b : the second root (negative sheet) also annihilates the symbol.
theorem carrier_root_subst_neg (t k : ℝ) (ht : t ≠ 0) :
    -((-(k / t)) ^ 2) + k ^ 2 / t ^ 2 = 0 := by
  field_simp [ht]
  ring

-- L1c : factorization of the symbol (root set = {+k/t, -k/t}).
theorem carrier_symbol_factor (w t k : ℝ) :
    -w ^ 2 + k ^ 2 / t ^ 2 = -(w - k / t) * (w + k / t) := by
  ring_nf

-- L1d : the two sheets are distinct for k != 0, t != 0 (two-sided cone).
theorem carrier_roots_distinct (t k : ℝ) (ht : t ≠ 0) (hk : k ≠ 0) :
    k / t ≠ -(k / t) := by
  intro h
  have hd : (k / t) * t = k := by field_simp [ht]
  have hn : (-(k / t)) * t = -k := by field_simp [ht]
  have hm := congrArg (fun x : ℝ => x * t) h
  rw [hd] at hm
  rw [hn] at hm
  have hk0 : k = 0 := by linarith
  exact hk hk0

-- L2 : future-sheet contraction sign:  xi_mu tau^mu = -w / N^2 < 0 for w > 0, N > 0.
theorem future_sheet_contraction_negative (w N : ℝ) (hw : w > 0) (hN : N > 0) :
    -w / N ^ 2 < 0 := by
  have hN2 : N ^ 2 > 0 := sq_pos_of_ne_zero (ne_of_gt hN)
  exact div_neg_of_neg_of_pos (neg_lt_zero.mpr hw) hN2

-- L2b : invariant identity  xi_mu tau^mu = - xi(n) / N:
--       tau^mu = (-1/N^2, 0, 0, 0), n^mu = (1/N, 0, 0, 0), so
--       xi(d tau) = -w/N^2  and  xi(n) = w/N.
theorem contraction_ratio_identity (w N : ℝ) (hN : N ≠ 0) :
    (-w / N ^ 2) * N = -(w / N) := by
  field_simp [hN]

-- L3 : composite carrier metric block-lapse identity:
--       -g_d^{mu nu} tau_mu tau_nu = t_c^-2 X_tau > 0 for every t_c > 0.
theorem composite_block_lapse (Xtau t : ℝ) (hX : Xtau > 0) (ht : t > 0) :
    Xtau / t ^ 2 > 0 := by
  exact div_pos hX (sq_pos_of_ne_zero (ne_of_gt ht))

-- L3b : the composite metric stays foliation-compatible under the superluminal
--       carrier (t_c = 0.7 -> v = c/t_c > c): no sign change for any t_c > 0.
theorem superluminal_carrier_ordered (Xtau t : ℝ) (hX : Xtau > 0) (ht : t > 0) :
    Xtau / t ^ 2 > 0 := by
  exact composite_block_lapse Xtau t hX ht

-- L4 : ghost control (NC-b): the sign-flipped kinetic symbol has no real root.
theorem ghost_no_real_root (v k : ℝ) (hv : v ≠ 0) (hk : k ≠ 0) :
    ∀ w : ℝ, w ^ 2 + v ^ 2 * k ^ 2 ≠ 0 := by
  intro w
  have hpos : w ^ 2 + v ^ 2 * k ^ 2 > 0 := by positivity
  exact ne_of_gt hpos

-- L1e : tensor block is the carrier block at t_c = 1 (speed 1 = c).
theorem tensor_root_subst (k : ℝ) :
    -((k) ^ 2) + k ^ 2 = 0 := by
  ring

-- Sanity examples (house rule: the tactic stack is verified by usage, never by
-- #check).
example (t k : ℝ) (ht : t ≠ 0) : -((k / t) ^ 2) + k ^ 2 / t ^ 2 = 0 := by
  field_simp [ht]
  ring

example (w N : ℝ) (hw : w > 0) (hN : N > 0) : -w / N ^ 2 < 0 := by
  exact future_sheet_contraction_negative w N hw hN

example (v k : ℝ) (hv : v ≠ 0) (hk : k ≠ 0) : ∀ w : ℝ, w ^ 2 + v ^ 2 * k ^ 2 ≠ 0 := by
  intro w
  positivity

end AS215