/-
EUC18_MUTATE: the mutation twin of EUC18.lean. Each theorem carries ONE false change (a sign, a factor or an
inequality direction) and the same proof script; every theorem here must fail to compile. They certify the algebra,
not the physics, and no number or label of the lane.

  distance_ratio_antitone_mut : the factor rises as the source moves away (direction reversed).
  distance_ratio_gt_one_mut   : the factor below 1 (direction reversed).
  einstein_mass_antitone_mut  : the Einstein mass rises with the source distance (direction reversed).
  gate_exclusive_median_mut   : the HOLDS line at 0.30 in place of 0.15.
  gate_exclusive_f25_mut      : the HOLDS line at 0.30 in place of 0.10.
  missing_share_identity_mut  : 1 + M_law / M_min in place of 1 - M_law / M_min.
  missing_mass_antitone_mut   : the excess rises with the law-plus-stars mass (direction reversed).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC18

theorem distance_ratio_antitone_mut (dl ds1 ds2 : ℝ) (hl : 0 < dl) (h1 : dl < ds1) (h12 : ds1 ≤ ds2) :
    ds1 / (ds1 - dl) ≤ ds2 / (ds2 - dl) := by
  have ha : 0 < ds1 - dl := by linarith
  have hb : 0 < ds2 - dl := by linarith
  rw [div_le_div_iff₀ hb ha]
  nlinarith

theorem distance_ratio_gt_one_mut (dl ds : ℝ) (hl : 0 < dl) (h : dl < ds) : ds / (ds - dl) < 1 := by
  have ha : 0 < ds - dl := by linarith
  rw [lt_div_iff₀ ha]
  linarith

theorem einstein_mass_antitone_mut (RE A dl ds1 ds2 : ℝ) (hA : 0 ≤ A) (hl : 0 < dl) (h1 : dl < ds1)
    (h12 : ds1 ≤ ds2) :
    Real.pi * RE ^ 2 * (A * (ds1 / (ds1 - dl))) ≤ Real.pi * RE ^ 2 * (A * (ds2 / (ds2 - dl))) := by
  have ha : 0 < ds1 - dl := by linarith
  have hb : 0 < ds2 - dl := by linarith
  have hr : ds2 / (ds2 - dl) ≤ ds1 / (ds1 - dl) := by
    rw [div_le_div_iff₀ hb ha]
    nlinarith
  have hk : 0 ≤ Real.pi * RE ^ 2 := by positivity
  apply mul_le_mul_of_nonneg_left _ hk
  exact mul_le_mul_of_nonneg_left hr hA

theorem gate_exclusive_median_mut {n : ℕ} (lo hi : Fin n → ℝ) (i : Fin n) (hlh : ∀ j, lo j ≤ hi j) :
    ¬ ((∀ j, hi j ≤ (3 : ℝ) / 10) ∧ (∀ j, (1 : ℝ) / 4 ≤ lo j)) := by
  rintro ⟨hH, hF⟩
  have a := hH i
  have b := hF i
  have c := hlh i
  linarith

theorem gate_exclusive_f25_mut {n : ℕ} (lo hi : Fin n → ℝ) (i : Fin n) (hlh : ∀ j, lo j ≤ hi j) :
    ¬ ((∀ j, (1 : ℝ) / 4 ≤ lo j) ∧ (∀ j, hi j ≤ (3 : ℝ) / 10)) := by
  rintro ⟨hB, hH⟩
  have a := hB i
  have b := hH i
  have c := hlh i
  linarith

theorem missing_share_identity_mut (Mt Ml : ℝ) (hM : 0 < Mt) :
    max 0 (Mt - Ml) / Mt = max 0 (1 + Ml / Mt) := by
  have e : 1 - Ml / Mt = (Mt - Ml) / Mt := by field_simp
  rw [e, ← zero_div Mt, max_div_div_right (le_of_lt hM), zero_div]

theorem missing_mass_antitone_mut (Mt M1 M2 : ℝ) (h : M1 ≤ M2) : max 0 (Mt - M1) ≤ max 0 (Mt - M2) := by
  apply max_le_max (le_refl 0)
  linarith

end EUC18

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
