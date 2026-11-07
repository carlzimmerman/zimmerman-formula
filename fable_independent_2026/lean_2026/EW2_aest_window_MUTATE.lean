/-
EW2 MUTATE twin: false variants of EW2_aest_window.lean. Each must FAIL to compile (the twin bites iff Lean rejects
every one). kappa = 1/2 FITTED; not theory closed.
M1: the capped map returns v = g (no cap).  M2: the leakage inequality reversed.  M3: the window overlaps.
-/
import Mathlib

namespace EW2M

theorem M1_capped_map_is_identity {a0 g : ℝ} (ha : 0 < a0) (hg : 0 ≤ g) : a0 * g / (a0 + g) = g := by
  field_simp; ring

theorem M2_leakage_reversed {ι : Type*} (s S : Finset ι) (hS : S ⊆ s) (w B : ι → ℝ) (b : ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1) (hB1 : ∀ i ∈ s, 1 ≤ B i) (hBb : ∀ i ∈ S, b ≤ B i) :
    ∑ i ∈ s, w i * B i - 1 ≤ (b - 1) * ∑ i ∈ S, w i := by
  linarith

theorem M3_window_overlaps (web host : ℝ → Prop) (mu_w mu_h : ℝ) (hw : ∀ m, web m → mu_w ≤ m)
    (hh : ∀ m, host m → m ≤ mu_h) (hlt : mu_h < mu_w) : ∃ m, web m ∧ host m := by
  exact ⟨mu_h, by simp_all, by simp_all⟩

end EW2M
