/-
DP7 MUTATE twin: the statements of DP7.lean, each with one false change (a factor, a constant, a sign, an inequality
direction or a denominator) and the same proof script. Every theorem is false and must fail (expected: exit 1, an error
in every theorem). TEST lane; adopts nothing.

kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
-/
import Mathlib

namespace DP7_MUTATE

open Finset

theorem sigma_b_floor_mut (sp : ℝ) :
    (20 / 1000 : ℝ) ≤ max (20 / 1000) (sp / 2) ∧ (max (20 / 1000 : ℝ) (sp / 2) = 20 / 1000 ↔ sp ≤ 20 / 1000) := by
  refine ⟨le_max_left _ _, ?_⟩
  rw [max_eq_left_iff]
  constructor <;> intro h <;> linarith

theorem sigma_b_mono_mut (sp1 sp2 : ℝ) (h : sp1 ≤ sp2) :
    max (20 / 1000 : ℝ) (sp2 / 2) ≤ max (20 / 1000) (sp1 / 2) := by
  apply max_le_max le_rfl
  linarith

theorem spread_nonneg_mut (S : Finset ℝ) (hS : S.Nonempty) : 0 < S.sup' hS id - S.inf' hS id := by
  obtain ⟨x, hx⟩ := hS
  have h1 := Finset.inf'_le id hx
  have h2 := Finset.le_sup' id hx
  simp only [id] at h1 h2 ⊢
  linarith

theorem spread_mono_mut (S T : Finset ℝ) (hS : S.Nonempty) (hST : S ⊆ T) (x : ℝ) :
    T.sup' (hS.mono hST) id - T.inf' (hS.mono hST) id ≤ S.sup' hS id - S.inf' hS id ∧
    S.sup' hS id - S.inf' hS id ≤ (insert x S).sup' (hS.mono (Finset.subset_insert x S)) id -
      (insert x S).inf' (hS.mono (Finset.subset_insert x S)) id := by
  constructor
  · have h1 := Finset.sup'_mono id hST hS
    have h2 := Finset.inf'_mono id hST hS
    linarith
  · have h1 := Finset.sup'_mono id (Finset.subset_insert x S) hS
    have h2 := Finset.inf'_mono id (Finset.subset_insert x S) hS
    linarith

theorem mean_of_diff_mut (K : ℕ) (r b : ℕ → ℝ) :
    (∑ k ∈ Icc 1 K, (r k - b k)) / K = (∑ k ∈ Icc 1 K, r k) / K + (∑ k ∈ Icc 1 K, b k) / K := by
  rw [Finset.sum_sub_distrib, sub_div]

theorem m1_all_equal_mut (K : ℕ) (hK : 0 < K) (Δ : ℕ → ℝ) (Δ0 g0 r0 : ℝ) (h : ∀ k ∈ Icc 1 K, Δ k = Δ0)
    (h0 : Δ0 = r0 - g0) :
    (∑ k ∈ Icc 1 K, Δ k) / K = K * Δ0 ∧
    ∑ k ∈ Icc 1 K, (Δ k - (∑ j ∈ Icc 1 K, Δ j) / K) ^ 2 = 0 ∧
    g0 + (∑ k ∈ Icc 1 K, Δ k) / K = r0 := by
  have hs : ∑ k ∈ Icc 1 K, Δ k = K * Δ0 := by
    rw [Finset.sum_congr rfl h, Finset.sum_const, Nat.card_Icc, nsmul_eq_mul]
    simp
  have hK' : (K : ℝ) ≠ 0 := by exact_mod_cast hK.ne'
  have hm : (∑ k ∈ Icc 1 K, Δ k) / K = Δ0 := by
    rw [hs]
    field_simp
  refine ⟨hm, ?_, ?_⟩
  · rw [hm]
    apply Finset.sum_eq_zero
    intro k hk
    rw [h k hk]
    ring
  · rw [hm, h0]
    ring

theorem m2_rung_is_base_mut (K : ℕ) (r b : ℕ → ℝ) (g0 : ℝ) (h : ∀ k ∈ Icc 1 K, r k = b k) :
    (∑ k ∈ Icc 1 K, (r k - b k)) / K = 0 ∧ g0 + (∑ k ∈ Icc 1 K, (r k - b k)) / K = 0 := by
  have hz : ∑ k ∈ Icc 1 K, (r k - b k) = 0 := by
    apply Finset.sum_eq_zero
    intro k hk
    rw [h k hk]
    ring
  rw [hz]
  simp

theorem se_sq_mut (sd K : ℝ) (hK : 0 < K) : (sd / Real.sqrt K) ^ 2 * K = sd ^ 2 * K := by
  rw [div_pow, Real.sq_sqrt hK.le]
  field_simp

theorem decision_se_mut (u v : ℝ) (hu : 0 ≤ u) (hv : 0 ≤ v) (hu2 : u ^ 2 * 50 = (43 / 1000) ^ 2)
    (hv2 : v ^ 2 * 50 = (29 / 1000) ^ 2) :
    6 / 1000 ≤ u ∧ u ≤ 60 / 10000 ∧ 41 / 10000 ≤ v ∧ v ≤ 42 / 10000 ∧ u < 20 / 1000 ∧ v < 20 / 1000 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> nlinarith

theorem jackknife_is_se_mut (n : ℕ) (hn : 2 ≤ n) (x : Fin n → ℝ) :
    ((n : ℝ) - 1) / n * ∑ i, ((∑ j, x j - x i) / ((n : ℝ) - 1) -
        (∑ l, (∑ j, x j - x l) / ((n : ℝ) - 1)) / n) ^ 2 =
      (∑ i, (x i - (∑ j, x j) / n) ^ 2) / (n * (n : ℝ)) := by
  have hn1 : (2 : ℝ) ≤ n := by exact_mod_cast hn
  have hn0 : (n : ℝ) ≠ 0 := by linarith
  have hm1 : (n : ℝ) - 1 ≠ 0 := by linarith
  set S := ∑ j, x j with hS
  have hl : (∑ l, (S - x l) / ((n : ℝ) - 1)) / n = S / n := by
    rw [← Finset.sum_div, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul]
    field_simp
    ring
  rw [hl]
  have hterm : ∀ i, ((S - x i) / ((n : ℝ) - 1) - S / n) ^ 2 = (x i - S / n) ^ 2 / ((n : ℝ) - 1) ^ 2 := by
    intro i
    field_simp
    ring
  rw [Finset.sum_congr rfl (fun i _ => hterm i), ← Finset.sum_div]
  field_simp

end DP7_MUTATE

-- kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
