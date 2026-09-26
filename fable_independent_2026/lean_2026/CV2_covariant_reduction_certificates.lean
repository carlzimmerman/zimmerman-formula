import Mathlib

/-!
# CV2 — V0 for the C-H/K branch: certificates for its reductions

SCOPE. `real_research/chk_v0_2026/CV2_covariant_action.py` writes V0 as one covariant action and checks three of its
reductions symbolically. Lean certifies the algebra those reductions rest on. The weak-field expansion, the 6×6 block
and the minisuperspace are computed in the lane.

* `periodic_laplacian_kernel_const`: on a periodic chain with ANY positive link weights (a discretised leaf with any
  metric), a field with zero weighted Laplacian is constant. This is why the plateau constraint Δ_h(Y − U) = 0 gives
  Y = U + const for every leaf metric, so the elimination behind B2 is exact nonlinearly. It is a discrete, one-dimensional
  analogue; the continuum statement on a closed connected leaf is the standard ∫|∇u|² = 0 argument.
* `yPsi_block_det`: the (Y, Ψ) block [[4k²C, −2k²], [−2k², 0]] has determinant −4k⁴, nonzero for k ≠ 0, so eliminating
  (Y, Ψ) multiplies L340's determinant by an ω-independent factor and adds no mode.
* `plateau_U_equation`: with Y = U and Ψ = 2CY (the δΨ and δY equations), V0's δU equation is L340's.
* `frw_leaf_average`: with the leaf-averaged λ-term (which vanishes on FRW), the lapse constraint gives GR's Friedmann
  equation (G_cos = G).
* `frw_plain_c2`: with the plain −c₂K² term (the control), it gives H²(1 + 3c₂/2) = … (L350 G1).
-/

open Finset

theorem periodic_laplacian_kernel_const (n : ℕ) (hn : 0 < n) (x c : ℕ → ℝ) (hc : ∀ i, 0 < c i)
    (hper : x n = x 0)
    (hL : ∀ i, c (i + 1) * (x (i + 2) - x (i + 1)) = c i * (x (i + 1) - x i)) :
    ∀ i, x i = x 0 := by
  -- the flux is the same on every link
  have hF : ∀ i, c i * (x (i + 1) - x i) = c 0 * (x 1 - x 0) := by
    intro i
    induction i with
    | zero => simp
    | succ k ih =>
      have h := hL k
      rw [show k + 1 + 1 = k + 2 from rfl]
      rw [h]
      exact ih
  set F := c 0 * (x 1 - x 0) with hFdef
  have hd : ∀ i, x (i + 1) - x i = F / c i := by
    intro i
    rw [eq_div_iff (ne_of_gt (hc i))]
    rw [mul_comm]
    exact hF i
  -- telescoping over one period
  have htel : ∑ i ∈ range n, (x (i + 1) - x i) = x n - x 0 := Finset.sum_range_sub x n
  have hsum : ∑ i ∈ range n, (x (i + 1) - x i) = F * ∑ i ∈ range n, 1 / c i := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [hd i]
    ring
  have hS : 0 < ∑ i ∈ range n, 1 / c i := by
    apply Finset.sum_pos
    · intro i _
      exact one_div_pos.mpr (hc i)
    · exact ⟨0, Finset.mem_range.mpr hn⟩
  have hF0 : F = 0 := by
    have h0 : F * ∑ i ∈ range n, 1 / c i = 0 := by
      rw [← hsum, htel, hper, sub_self]
    rcases mul_eq_zero.mp h0 with h | h
    · exact h
    · exact absurd h (ne_of_gt hS)
  have hstep : ∀ i, x (i + 1) = x i := by
    intro i
    have := hd i
    rw [hF0, zero_div] at this
    linarith
  intro i
  induction i with
  | zero => rfl
  | succ k ih => rw [hstep k, ih]

theorem yPsi_block_det (k C : ℝ) (hk : k ≠ 0) :
    (4 * k ^ 2 * C) * 0 - (-2 * k ^ 2) * (-2 * k ^ 2) = -4 * k ^ 4 ∧ -4 * k ^ 4 ≠ 0 := by
  constructor
  · ring
  · have : k ^ 4 ≠ 0 := pow_ne_zero 4 hk
    intro h
    apply this
    linarith

theorem plateau_U_equation (k C U phi Y Psi : ℝ) (hY : Y = U) (hPsi : Psi = 2 * C * Y) :
    4 * k ^ 2 * (U - phi) + 2 * k ^ 2 * Psi = 4 * k ^ 2 * (U - phi) + 4 * k ^ 2 * C * U := by
  rw [hPsi, hY]
  ring

theorem frw_leaf_average (a ad Λ κρ : ℝ) (ha : 0 < a)
    (hN : 6 * a * ad ^ 2 - 2 * Λ * a ^ 3 = κρ) :
    (ad / a) ^ 2 = κρ / (6 * a ^ 3) + Λ / 3 := by
  have ha3 : 0 < a ^ 3 := by positivity
  field_simp
  nlinarith [hN]

theorem frw_plain_c2 (a ad Λ κρ c2 : ℝ) (ha : 0 < a)
    (hN : (6 + 9 * c2) * a * ad ^ 2 - 2 * Λ * a ^ 3 = κρ) :
    (ad / a) ^ 2 * (1 + 3 * c2 / 2) = κρ / (6 * a ^ 3) + Λ / 3 := by
  have ha3 : 0 < a ^ 3 := by positivity
  field_simp
  nlinarith [hN]

#print axioms periodic_laplacian_kernel_const
#print axioms yPsi_block_det
#print axioms plateau_U_equation
#print axioms frw_leaf_average
#print axioms frw_plain_c2
