/-
LFS1 MUTATE twin: false versions of LFS1.lean's statements. Every one must fail to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib.Tactic

namespace LFS1M

open Finset

-- M1: the region's polarization charge equals the enclosed charge at the boundary plus one (false)
theorem net_zero_false (f : ℕ → ℝ) (n : ℕ) (h0 : f 0 = 0) (hn : f n = 0) :
    ∑ i ∈ range n, (f (i + 1) - f i) = 1 := by
  rw [Finset.sum_range_sub, hn, h0]; ring

-- M2: the edge carries +C, not -C (false)
theorem edge_is_plus (f : ℕ → ℝ) (m n : ℕ) (C : ℝ) (h0 : f 0 = 0) (hn : f n = 0) (hm : f m = C) :
    (∑ i ∈ range n, (f (i + 1) - f i)) - (∑ i ∈ range m, (f (i + 1) - f i)) = C := by
  rw [Finset.sum_range_sub, Finset.sum_range_sub, hn, h0, hm]; ring

-- M3: the frozen charge grows as X squared (the MU1 sign flip gives X^-2; neither is the identity)
theorem frozen_square (C X : ℕ → ℝ) (h : ∀ k, C (k + 1) * X k = C k * X (k + 1)) (hX : ∀ k, X k ≠ 0) :
    ∀ n, C n * X 0 ^ 2 = C 0 * X n ^ 2 := by
  intro n
  induction n with
  | zero => ring
  | succ k ih => nlinarith [h k, hX k]

-- M4: the growth bound without the 1/(1-e) factor (false for e > 0)
theorem growth_bound_false (C0 Cn X0 Xn e : ℝ) (hC0 : 0 < C0) (he : 0 < 1 - e) (he0 : 0 ≤ e)
    (hX0 : 1 - e ≤ X0) (hXn : Xn ≤ 1 + e) (hfro : Cn * X0 = C0 * Xn) :
    Cn ≤ C0 * (1 + e) := by
  nlinarith

-- M5: Gauss with the wrong sign
theorem gauss_false (g a0 : ℝ) (h : g + a0 ≠ 0) :
    g * a0 / (g + a0) = g + g ^ 2 / (g + a0) := by
  field_simp; ring

-- M6: cap with X^2 in place of X (X + 1)
theorem cap_false (a0 X : ℝ) (hX : X ≠ 0) :
    let gN := a0 / (X * X)
    let g := (1 + X) * gN
    g ^ 2 = gN * (g + a0) := by
  intro gN g
  simp only [g, gN]
  field_simp
  ring

end LFS1M

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
