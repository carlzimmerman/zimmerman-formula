/-
LFS1 (criteria 8ddf81950c): Lean statements for the structural claims. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  net_zero         : shells' polarization charges telescope: with zero flux at the centre and at the outer boundary
                     (f 0 = 0, f n = 0, f = enclosed flux X Y), the region's total polarization charge is 0.
  edge_is_minus    : if the charge enclosed at shell m is C, the shells from m to the boundary carry exactly -C.
  frozen_ratio     : discrete form of S1(d)/(e): if each step's charge ratio is the ratio of X, then C/X is constant.
  growth_bound     : with X in [1 - e, 1 + e] (0 <= e < 1), that charge can grow at most by (1 + e)/(1 - e).
  gauss_lawS       : KA2's algebra: g a0/(g + a0) = g - g^2/(g + a0)  (4 pi R^2 P_r = M_b (nu - 1) on law S).
  cap_lawS         : g_N = a0/(X (X + 1)), g = (1 + X) g_N solve law S: g^2 = g_N (g + a0)  (R_cap's definition).
-/
import Mathlib.Tactic

namespace LFS1

open Finset

theorem net_zero (f : ℕ → ℝ) (n : ℕ) (h0 : f 0 = 0) (hn : f n = 0) :
    ∑ i ∈ range n, (f (i + 1) - f i) = 0 := by
  rw [Finset.sum_range_sub, hn, h0]; ring

theorem edge_is_minus (f : ℕ → ℝ) (m n : ℕ) (C : ℝ) (h0 : f 0 = 0) (hn : f n = 0) (hm : f m = C) :
    (∑ i ∈ range n, (f (i + 1) - f i)) - (∑ i ∈ range m, (f (i + 1) - f i)) = -C := by
  rw [Finset.sum_range_sub, Finset.sum_range_sub, hn, h0, hm]; ring

theorem frozen_ratio (C X : ℕ → ℝ) (h : ∀ k, C (k + 1) * X k = C k * X (k + 1)) (hX : ∀ k, X k ≠ 0) :
    ∀ n, C n * X 0 = C 0 * X n := by
  intro n
  induction n with
  | zero => ring
  | succ k ih =>
    have hk := h k
    have hXk := hX k
    have : C (k + 1) * X 0 * X k = C 0 * X (k + 1) * X k := by
      calc C (k + 1) * X 0 * X k = (C (k + 1) * X k) * X 0 := by ring
        _ = C k * X (k + 1) * X 0 := by rw [hk]
        _ = (C k * X 0) * X (k + 1) := by ring
        _ = (C 0 * X k) * X (k + 1) := by rw [ih]
        _ = C 0 * X (k + 1) * X k := by ring
    exact mul_right_cancel₀ hXk this

theorem growth_bound (C0 Cn X0 Xn e : ℝ) (hC0 : 0 < C0) (he : 0 < 1 - e) (he0 : 0 ≤ e)
    (hX0 : 1 - e ≤ X0) (hXn : Xn ≤ 1 + e) (hfro : Cn * X0 = C0 * Xn) :
    Cn ≤ C0 * (1 + e) / (1 - e) := by
  have hX0pos : 0 < X0 := lt_of_lt_of_le he hX0
  rw [le_div_iff₀ he]
  have h1 : Cn * X0 ≤ C0 * (1 + e) := by
    rw [hfro]; exact mul_le_mul_of_nonneg_left hXn hC0.le
  by_cases hCn : Cn ≤ 0
  · have hA : 0 < C0 * (1 + e) := mul_pos hC0 (by linarith)
    have hB : Cn * (1 - e) ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hCn he.le
    linarith
  · have hCn' : 0 < Cn := lt_of_not_ge hCn
    have hB : Cn * (1 - e) ≤ Cn * X0 := mul_le_mul_of_nonneg_left hX0 hCn'.le
    linarith

theorem gauss_lawS (g a0 : ℝ) (h : g + a0 ≠ 0) :
    g * a0 / (g + a0) = g - g ^ 2 / (g + a0) := by
  field_simp; ring

theorem cap_lawS (a0 X : ℝ) (hX : X ≠ 0) (hX1 : X + 1 ≠ 0) :
    let gN := a0 / (X * (X + 1))
    let g := (1 + X) * gN
    g ^ 2 = gN * (g + a0) := by
  intro gN g
  simp only [g, gN]
  field_simp
  ring

end LFS1

#print axioms LFS1.net_zero
#print axioms LFS1.edge_is_minus
#print axioms LFS1.frozen_ratio
#print axioms LFS1.growth_bound
#print axioms LFS1.gauss_lawS
#print axioms LFS1.cap_lawS

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
