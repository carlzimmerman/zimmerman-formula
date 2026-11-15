/-
EUC20_MUTATE: the mutation twin of EUC20.lean (pair EUC20 / EUC20R). Each theorem carries ONE false change (a sign,
a factor or an inequality direction) and the same proof script; every theorem here must fail to compile. They
certify the algebra, not the physics, and no number or label of the lane.

  bin_count_cannot_rise_mut    : the per-lens shift taken as non-negative (sign flipped).
  speed_cube_scaling_mut       : v'^3 = v^3 f in place of v'^3 f = v^3.
  above_boundary_kept_mut      : the corrected mass M_b f in place of M_b / f.
  no_switch_vs_step_mut        : the REAL line at 0.05 in place of 0.20.
  dyn_minus_lens_invariant_mut : the lensing bound shifted by -l in place of +l.
  worth_gap_mut                : the sum of the two medians in place of their difference.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC20

theorem bin_count_cannot_rise_mut {ι : Type*} (s : Finset ι) (b l : ι → ℝ) (hl : ∀ i, 0 ≤ l i) :
    (s.filter (fun i => (1 : ℝ) / 4 < b i + l i)).card ≤ (s.filter (fun i => (1 : ℝ) / 4 < b i)).card := by
  apply Finset.card_le_card
  intro i hi
  rw [Finset.mem_filter] at hi ⊢
  refine ⟨hi.1, ?_⟩
  have h1 := hi.2
  have h2 := hl i
  linarith

theorem speed_cube_scaling_mut (v v' K M f : ℝ) (hf : f ≠ 0) (h0 : v ^ 3 = K * M) (h1 : v' ^ 3 = K * (M / f)) :
    v' ^ 3 = v ^ 3 * f := by
  rw [h1, h0]
  field_simp

theorem above_boundary_kept_mut (K M f vs : ℝ) (hK : 0 ≤ K) (hM : 0 ≤ M) (hf0 : 0 < f) (hf1 : f ≤ 1)
    (h : vs ≤ (K * M) ^ ((1 : ℝ) / 3)) : vs ≤ (K * (M * f)) ^ ((1 : ℝ) / 3) := by
  have hMf : M ≤ M / f := by
    rw [le_div_iff₀ hf0]
    nlinarith
  have hr : (K * M) ^ ((1 : ℝ) / 3) ≤ (K * (M / f)) ^ ((1 : ℝ) / 3) :=
    Real.rpow_le_rpow (by positivity) (mul_le_mul_of_nonneg_left hMf hK) (by norm_num)
  linarith

theorem no_switch_vs_step_mut (lo hi : ℝ) (hlh : lo ≤ hi) :
    ¬ ((1 : ℝ) / 20 ≤ lo ∧ hi < (1 : ℝ) / 10) := by
  rintro ⟨h1, h2⟩
  linarith

theorem dyn_minus_lens_invariant_mut (bdyn binf l : ℝ) : (bdyn + l) - (binf - l) = bdyn - binf := by
  ring

theorem worth_gap_mut (k d1 d2 : ℝ) : |k * d1 - k * d2| ≤ |k| * |d1 + d2| := by
  rw [← mul_sub, abs_mul]

end EUC20

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
