/-
DP7: Lean statements for the algebra of lane DP7_seed_mean_check (dr4_push_2026_11_05/DP7_seed_mean_check:
dp7_seed_mean.py, FROZEN_CRITERIA.md, RESULT.md), of the sigma_sys recipe it feeds
(dr4_push_2026_11_05/DP3_release_day/dp3_sigma_sys.py: (b) and (e)) and of the seed-mean entry filed in
prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF.md (section 1; the standard-error remark of
section 2). They certify the algebra, not the physics, and no number or label of the lane. TEST lane; adopts nothing.

  sigma_b_floor        : sigma_sys(b) = max(0.020, spread/2) is at least 0.020, and equals 0.020 iff spread <= 0.040.
  sigma_b_mono         : sigma_sys(b) does not decrease when the spread grows.
  spread_nonneg        : the full spread max - min of a nonempty finite set of rung values is >= 0.
  spread_mono          : the spread cannot decrease when rungs are added (subset), in particular by one rung (insert).
  mean_of_diff         : Delta_bar = (1/K) sum_{k=1..K} (rung_k - base_k) = mean(rung) - mean(base).
  m1_all_equal         : if every Delta_k equals the k = 0 difference Delta_0 (mutation M1), Delta_bar = Delta_0, the
                         sum of squared deviations (so the SD) is 0, and the entry gamma_0 + Delta_bar is gamma(rung_0)
                         when gamma_0 = gamma(base_0).
  m2_rung_is_base      : if rung_k = base_k at every k (mutation M2), Delta_bar = 0 and the entry is gamma_0.
  se_sq                : SE = SD / sqrt(K) with K > 0 means SE^2 K = SD^2.
  decision_se          : 0.043 / sqrt(50) lies in [0.0060, 0.0061] and 0.029 / sqrt(50) in [0.0041, 0.0042], both
                         below the 0.020 floor (the decision's "about 0.006 canonical and 0.004 alt"), on squares.
  jackknife_is_se      : (e)'s delete-one jackknife sqrt((n-1)/n sum (loo_i - mean loo)^2) squared equals
                         sum (x_i - mean x)^2 / (n (n - 1)), the squared standard error of the mean (n >= 2).

kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
-/
import Mathlib

namespace DP7

open Finset

theorem sigma_b_floor (sp : ℝ) :
    (20 / 1000 : ℝ) ≤ max (20 / 1000) (sp / 2) ∧ (max (20 / 1000 : ℝ) (sp / 2) = 20 / 1000 ↔ sp ≤ 40 / 1000) := by
  refine ⟨le_max_left _ _, ?_⟩
  rw [max_eq_left_iff]
  constructor <;> intro h <;> linarith

theorem sigma_b_mono (sp1 sp2 : ℝ) (h : sp1 ≤ sp2) :
    max (20 / 1000 : ℝ) (sp1 / 2) ≤ max (20 / 1000) (sp2 / 2) := by
  apply max_le_max le_rfl
  linarith

theorem spread_nonneg (S : Finset ℝ) (hS : S.Nonempty) : 0 ≤ S.sup' hS id - S.inf' hS id := by
  obtain ⟨x, hx⟩ := hS
  have h1 := Finset.inf'_le id hx
  have h2 := Finset.le_sup' id hx
  simp only [id] at h1 h2 ⊢
  linarith

theorem spread_mono (S T : Finset ℝ) (hS : S.Nonempty) (hST : S ⊆ T) (x : ℝ) :
    S.sup' hS id - S.inf' hS id ≤ T.sup' (hS.mono hST) id - T.inf' (hS.mono hST) id ∧
    S.sup' hS id - S.inf' hS id ≤ (insert x S).sup' (hS.mono (Finset.subset_insert x S)) id -
      (insert x S).inf' (hS.mono (Finset.subset_insert x S)) id := by
  constructor
  · have h1 := Finset.sup'_mono id hST hS
    have h2 := Finset.inf'_mono id hST hS
    linarith
  · have h1 := Finset.sup'_mono id (Finset.subset_insert x S) hS
    have h2 := Finset.inf'_mono id (Finset.subset_insert x S) hS
    linarith

theorem mean_of_diff (K : ℕ) (r b : ℕ → ℝ) :
    (∑ k ∈ Icc 1 K, (r k - b k)) / K = (∑ k ∈ Icc 1 K, r k) / K - (∑ k ∈ Icc 1 K, b k) / K := by
  rw [Finset.sum_sub_distrib, sub_div]

theorem m1_all_equal (K : ℕ) (hK : 0 < K) (Δ : ℕ → ℝ) (Δ0 g0 r0 : ℝ) (h : ∀ k ∈ Icc 1 K, Δ k = Δ0)
    (h0 : Δ0 = r0 - g0) :
    (∑ k ∈ Icc 1 K, Δ k) / K = Δ0 ∧
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

theorem m2_rung_is_base (K : ℕ) (r b : ℕ → ℝ) (g0 : ℝ) (h : ∀ k ∈ Icc 1 K, r k = b k) :
    (∑ k ∈ Icc 1 K, (r k - b k)) / K = 0 ∧ g0 + (∑ k ∈ Icc 1 K, (r k - b k)) / K = g0 := by
  have hz : ∑ k ∈ Icc 1 K, (r k - b k) = 0 := by
    apply Finset.sum_eq_zero
    intro k hk
    rw [h k hk]
    ring
  rw [hz]
  simp

theorem se_sq (sd K : ℝ) (hK : 0 < K) : (sd / Real.sqrt K) ^ 2 * K = sd ^ 2 := by
  rw [div_pow, Real.sq_sqrt hK.le]
  field_simp

theorem decision_se (u v : ℝ) (hu : 0 ≤ u) (hv : 0 ≤ v) (hu2 : u ^ 2 * 50 = (43 / 1000) ^ 2)
    (hv2 : v ^ 2 * 50 = (29 / 1000) ^ 2) :
    6 / 1000 ≤ u ∧ u ≤ 61 / 10000 ∧ 41 / 10000 ≤ v ∧ v ≤ 42 / 10000 ∧ u < 20 / 1000 ∧ v < 20 / 1000 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> nlinarith

theorem jackknife_is_se (n : ℕ) (hn : 2 ≤ n) (x : Fin n → ℝ) :
    ((n : ℝ) - 1) / n * ∑ i, ((∑ j, x j - x i) / ((n : ℝ) - 1) -
        (∑ l, (∑ j, x j - x l) / ((n : ℝ) - 1)) / n) ^ 2 =
      (∑ i, (x i - (∑ j, x j) / n) ^ 2) / (n * ((n : ℝ) - 1)) := by
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

end DP7

-- kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
