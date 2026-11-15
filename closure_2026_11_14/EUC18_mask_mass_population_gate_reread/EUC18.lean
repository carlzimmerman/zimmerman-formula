/-
EUC18: Lean statements for the algebra of the population-gate re-read at the in-mask mass (EUC13's code run on the
corrected masses; euc18_collect.py's wide-lens share reading). They certify the algebra, not the physics, and no
number or label of the lane. TEST lane; adopts nothing.

  distance_ratio_antitone : with comoving distances 0 < d_l < d_s1 <= d_s2 (flat space), the factor d_s / (d_s - d_l)
                            in the critical surface density does not rise when the source moves farther away.
  distance_ratio_gt_one   : that factor exceeds 1 for every finite source, so the source at infinity gives the
                            smallest critical density.
  einstein_mass_antitone  : the Einstein mass pi R_E^2 Sigma_cr, with Sigma_cr = A d_s / (d_s - d_l) and A >= 0,
                            does not rise when the drawn source redshift rises.
  gate_exclusive_median   : POPULATION GATE HOLDS (every member's upper bound <= 0.15) and POPULATION GATE FAILS
                            (every member's lower bound >= 0.25) cannot both apply when some member exists and each
                            member's lower bound is at most its upper bound.
  gate_exclusive_f25      : the same for CEILING BROKEN (every lower >= 0.25) and CEILING HOLDS (every upper <= 0.10).
  missing_share_identity  : the share not supplied, max(0, M_min - M_law) / M_min, equals max(0, 1 - M_law / M_min).
  missing_mass_antitone   : the excess max(0, M_min - M_law) does not rise when the law-plus-stars mass rises (the
                            correction raises the stars, so it can only shrink the missing mass).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC18

theorem distance_ratio_antitone (dl ds1 ds2 : ℝ) (hl : 0 < dl) (h1 : dl < ds1) (h12 : ds1 ≤ ds2) :
    ds2 / (ds2 - dl) ≤ ds1 / (ds1 - dl) := by
  have ha : 0 < ds1 - dl := by linarith
  have hb : 0 < ds2 - dl := by linarith
  rw [div_le_div_iff₀ hb ha]
  nlinarith

theorem distance_ratio_gt_one (dl ds : ℝ) (hl : 0 < dl) (h : dl < ds) : 1 < ds / (ds - dl) := by
  have ha : 0 < ds - dl := by linarith
  rw [lt_div_iff₀ ha]
  linarith

theorem einstein_mass_antitone (RE A dl ds1 ds2 : ℝ) (hA : 0 ≤ A) (hl : 0 < dl) (h1 : dl < ds1)
    (h12 : ds1 ≤ ds2) :
    Real.pi * RE ^ 2 * (A * (ds2 / (ds2 - dl))) ≤ Real.pi * RE ^ 2 * (A * (ds1 / (ds1 - dl))) := by
  have ha : 0 < ds1 - dl := by linarith
  have hb : 0 < ds2 - dl := by linarith
  have hr : ds2 / (ds2 - dl) ≤ ds1 / (ds1 - dl) := by
    rw [div_le_div_iff₀ hb ha]
    nlinarith
  have hk : 0 ≤ Real.pi * RE ^ 2 := by positivity
  apply mul_le_mul_of_nonneg_left _ hk
  exact mul_le_mul_of_nonneg_left hr hA

theorem gate_exclusive_median {n : ℕ} (lo hi : Fin n → ℝ) (i : Fin n) (hlh : ∀ j, lo j ≤ hi j) :
    ¬ ((∀ j, hi j ≤ (3 : ℝ) / 20) ∧ (∀ j, (1 : ℝ) / 4 ≤ lo j)) := by
  rintro ⟨hH, hF⟩
  have a := hH i
  have b := hF i
  have c := hlh i
  linarith

theorem gate_exclusive_f25 {n : ℕ} (lo hi : Fin n → ℝ) (i : Fin n) (hlh : ∀ j, lo j ≤ hi j) :
    ¬ ((∀ j, (1 : ℝ) / 4 ≤ lo j) ∧ (∀ j, hi j ≤ (1 : ℝ) / 10)) := by
  rintro ⟨hB, hH⟩
  have a := hB i
  have b := hH i
  have c := hlh i
  linarith

theorem missing_share_identity (Mt Ml : ℝ) (hM : 0 < Mt) :
    max 0 (Mt - Ml) / Mt = max 0 (1 - Ml / Mt) := by
  have e : 1 - Ml / Mt = (Mt - Ml) / Mt := by field_simp
  rw [e, ← zero_div Mt, max_div_div_right (le_of_lt hM), zero_div]

theorem missing_mass_antitone (Mt M1 M2 : ℝ) (h : M1 ≤ M2) : max 0 (Mt - M2) ≤ max 0 (Mt - M1) := by
  apply max_le_max (le_refl 0)
  linarith

end EUC18

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
