/-
EUC20: Lean statements for the algebra of the grade-B re-read at the in-mask mass, covering the pair EUC20 (lead)
and EUC20R (blind re-grade, closure_2026_11_14/EUC20R_blind_grade_b_regrade). They certify the algebra, not the
physics, and no number or label of the lane. TEST lane; adopts nothing.

  bin_count_cannot_rise : in any bin, the number of lenses above the 0.25 dex margin after the shift b + log10 f
                          (log10 f <= 0 per lens) is at most the number before (G1's f25 can only fall).
  speed_cube_scaling    : LNJ1's model-rule speed has v^3 = K M_b; at the corrected mass M_b / f the new speed v'
                          satisfies v'^3 f = v^3, so the speed rises by f^(-1/3).
  above_boundary_kept   : a lens at or above the boundary speed (v* <= (K M_b)^(1/3)) stays above it at the
                          corrected mass M_b / f with 0 < f <= 1 (membership above the boundary can only grow; G3).
  no_switch_vs_step     : on one interval of the step in the share above the band, a REAL step (lower point >= 0.20)
                          and NO SWITCH (upper point < 0.10) cannot both hold.
  dyn_minus_lens_invariant : a per-lens shift l added to both the dynamical boost and the lensing bound leaves their
                          difference unchanged (EUC5 A1 reading, both builds).
  worth_gap             : the two builds' EUC6 worths (slope times the median mass difference, on 249 or 243 pairs)
                          differ by at most |slope| times the difference of the two medians.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC20

theorem bin_count_cannot_rise {ι : Type*} (s : Finset ι) (b l : ι → ℝ) (hl : ∀ i, l i ≤ 0) :
    (s.filter (fun i => (1 : ℝ) / 4 < b i + l i)).card ≤ (s.filter (fun i => (1 : ℝ) / 4 < b i)).card := by
  apply Finset.card_le_card
  intro i hi
  rw [Finset.mem_filter] at hi ⊢
  refine ⟨hi.1, ?_⟩
  have h1 := hi.2
  have h2 := hl i
  linarith

theorem speed_cube_scaling (v v' K M f : ℝ) (hf : f ≠ 0) (h0 : v ^ 3 = K * M) (h1 : v' ^ 3 = K * (M / f)) :
    v' ^ 3 * f = v ^ 3 := by
  rw [h1, h0]
  field_simp

theorem above_boundary_kept (K M f vs : ℝ) (hK : 0 ≤ K) (hM : 0 ≤ M) (hf0 : 0 < f) (hf1 : f ≤ 1)
    (h : vs ≤ (K * M) ^ ((1 : ℝ) / 3)) : vs ≤ (K * (M / f)) ^ ((1 : ℝ) / 3) := by
  have hMf : M ≤ M / f := by
    rw [le_div_iff₀ hf0]
    nlinarith
  have hr : (K * M) ^ ((1 : ℝ) / 3) ≤ (K * (M / f)) ^ ((1 : ℝ) / 3) :=
    Real.rpow_le_rpow (by positivity) (mul_le_mul_of_nonneg_left hMf hK) (by norm_num)
  linarith

theorem no_switch_vs_step (lo hi : ℝ) (hlh : lo ≤ hi) :
    ¬ ((1 : ℝ) / 5 ≤ lo ∧ hi < (1 : ℝ) / 10) := by
  rintro ⟨h1, h2⟩
  linarith

theorem dyn_minus_lens_invariant (bdyn binf l : ℝ) : (bdyn + l) - (binf + l) = bdyn - binf := by
  ring

theorem worth_gap (k d1 d2 : ℝ) : |k * d1 - k * d2| ≤ |k| * |d1 - d2| := by
  rw [← mul_sub, abs_mul]

end EUC20

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
