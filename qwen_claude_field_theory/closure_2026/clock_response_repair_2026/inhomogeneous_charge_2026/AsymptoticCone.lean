import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

set_option autoImplicit false
namespace AsymptoticCone
noncomputable section

/-!
Exact necessary-condition certificate for a localized repair.
The scalar characteristic after a regular constraint reduction is
K c^2 + B c - G = 0; its quarter-discriminant is B^2/4 + K G.
This file proves real algebra and the explicit epsilon definition of a
radial limit. It does not formalize the action, PDE well-posedness, existence
of constraint data, or the numerical exterior coefficients.
-/

def characteristic (K B G c : ℝ) := K*c^2+B*c-G
def quarter (K B G : ℝ) := B^2/4+K*G
def Approaches (f : ℝ → ℝ) (limit : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ R : ℝ, ∀ r : ℝ, R < r → |f r-limit| < ε

theorem completed_square (K B G c : ℝ) :
    (K*c+B/2)^2 = K*characteristic K B G c+quarter K B G := by
  unfold characteristic quarter
  ring

theorem negative_quarter_excludes_real_root (K B G : ℝ)
    (h : quarter K B G < 0) :
    ¬ ∃ c : ℝ, characteristic K B G c = 0 := by
  rintro ⟨c, hc⟩
  have hid := completed_square K B G c
  rw [hc] at hid
  have hsq := sq_nonneg (K*c+B/2)
  nlinarith

theorem wrong_sign_isotropic_form_positive (K G omega spatialNormSq : ℝ)
    (hK : 0 < K) (hG : G < 0) (hs : 0 ≤ spatialNormSq)
    (hnonzero : 0 < omega^2+spatialNormSq) :
    0 < K*omega^2-G*spatialNormSq := by
  have hminusG : 0 < -G := by linarith
  by_cases hw : omega = 0
  · subst omega
    have hsp : 0 < spatialNormSq := by nlinarith
    have hprod := mul_pos hminusG hsp
    nlinarith
  · have hwsq := sq_pos_of_ne_zero hw
    have htime := mul_pos hK hwsq
    have hspace := mul_nonneg (le_of_lt hminusG) hs
    nlinarith

theorem negative_limit_eventually_negative (f : ℝ → ℝ) (limit : ℝ)
    (hl : limit < 0) (hf : Approaches f limit) :
    ∃ R : ℝ, ∀ r : ℝ, R < r → f r < limit/2 := by
  obtain ⟨R, hR⟩ := hf (-limit/2) (by linarith)
  refine ⟨R, ?_⟩
  intro r hr
  have hupper := (abs_lt.mp (hR r hr)).2
  linarith

theorem no_everywhere_real_cone (K B G : ℝ → ℝ) (limit : ℝ)
    (hl : limit < 0)
    (htail : Approaches (fun r => quarter (K r) (B r) (G r)) limit) :
    ¬ (∀ r : ℝ, 0 ≤ r → ∃ c : ℝ, characteristic (K r) (B r) (G r) c = 0) := by
  intro hall
  obtain ⟨R, hR⟩ := negative_limit_eventually_negative
    (fun r => quarter (K r) (B r) (G r)) limit hl htail
  have hr : R < |R|+1 := by have := le_abs_self R; linarith
  have hr0 : 0 ≤ |R|+1 := by have := abs_nonneg R; linarith
  have hneg : quarter (K (|R|+1)) (B (|R|+1)) (G (|R|+1)) < 0 := by
    have := hR (|R|+1) hr
    linarith
  exact negative_quarter_excludes_real_root _ _ _ hneg (hall (|R|+1) hr0)

#print axioms completed_square
#print axioms negative_quarter_excludes_real_root
#print axioms wrong_sign_isotropic_form_positive
#print axioms negative_limit_eventually_negative
#print axioms no_everywhere_real_cone
end
end AsymptoticCone
