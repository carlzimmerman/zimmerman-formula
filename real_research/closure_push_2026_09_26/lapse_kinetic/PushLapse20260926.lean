import Mathlib

/-! Real algebra for the frozen trace/lapse scalar block. Action variation,
covariant constraint closure, PDE propagation, and observational PPN limits
are not formalized or assumed as axioms. -/
namespace PushLapse20260926

noncomputable def den (E z r s : ℝ) : ℝ :=
  E * (z - 2 * r ^ 2) + 2 * r ^ 2 * z + 4 * r ^ 2 -
    4 * r * (s + 1) * z + 2 * z * s ^ 2 + 4 * z * s

theorem contact_locus_product (E z r s : ℝ)
    (h : E * r ^ 2 = z * (r - s) ^ 2) :
    E * den E z r s = z * (E - 2 * (r - s)) ^ 2 := by
  unfold den
  linear_combination 2 * (2 - E) * h

theorem contact_speed_identity (E z r s κ : ℝ)
    (h : E * r ^ 2 = z * (r - s) ^ 2)
    (hD : den E z r s ≠ 0) (hκ : κ ≠ 0)
    (hS : (E - 2 * (r - s)) ^ 2 ≠ 0) :
    2 * z * (2 - E) / (κ * den E z r s) =
      2 * E * (2 - E) / (κ * (E - 2 * (r - s)) ^ 2) := by
  have hid := contact_locus_product E z r s h
  apply (div_eq_div_iff (mul_ne_zero hκ hD) (mul_ne_zero hκ hS)).2
  linear_combination -2 * κ * (2 - E) * hid

theorem negative_E_contact_instability (E z r s κ : ℝ)
    (hE : E < 0) (hκ : 0 < κ)
    (hD : den E z r s ≠ 0)
    (h : E * r ^ 2 = z * (r - s) ^ 2) :
    2 * z * (2 - E) / (κ * den E z r s) < 0 := by
  have hid := contact_locus_product E z r s h
  have hS : (E - 2 * (r - s)) ^ 2 ≠ 0 := by
    intro hs
    rw [hs, mul_zero] at hid
    exact (mul_ne_zero (ne_of_lt hE) hD) hid
  rw [contact_speed_identity E z r s κ h hD (ne_of_gt hκ) hS]
  apply div_neg_of_neg_of_pos
  · exact mul_neg_of_neg_of_pos (by linarith) (by linarith)
  · exact mul_pos hκ (lt_of_le_of_ne (sq_nonneg _) (Ne.symm hS))

theorem positive_cell_identity (E : ℝ) :
    den E E 1 2 = (E + 2) ^ 2 := by unfold den; ring

theorem positive_cell_speed (E : ℝ) (hl : 0 < E) (hu : E < 2) :
    0 < E * (2 - E) / (5 * (E + 2) ^ 2) := by positivity

theorem positive_cell_bound_identity (E : ℝ) (h : E + 2 ≠ 0) :
    1 / 40 - E * (2 - E) / (5 * (E + 2) ^ 2) =
      (3 * E - 2) ^ 2 / (40 * (E + 2) ^ 2) := by
  field_simp
  ring

theorem positive_cell_subluminal (E : ℝ) (h : 0 < E) :
    E * (2 - E) / (5 * (E + 2) ^ 2) ≤ 1 / 40 := by
  have hn : E + 2 ≠ 0 := by linarith
  have hid := positive_cell_bound_identity E hn
  have hr : 0 ≤ (3 * E - 2) ^ 2 / (40 * (E + 2) ^ 2) := by positivity
  linarith

theorem alpha2_completed_square (E δ κ : ℝ) (h : E ≠ 2) :
    κ * ((1 - δ) ^ 2 / (2 - E) - (1 - δ)) +
      (2 - E) * (κ / 4 + 1 / 2) - 1 =
    κ * (E - 2 * δ) ^ 2 / (4 * (2 - E)) - E / 2 := by
  have hd : 2 - E ≠ 0 := by intro hn; apply h; linarith
  field_simp
  ring

theorem alpha2_speed_identity (E δ κ : ℝ)
    (hE : E ≠ 0) (h2 : E ≠ 2) (_hκ : κ ≠ 0) (_hδ : E - 2 * δ ≠ 0) :
    κ * (E - 2 * δ) ^ 2 / (4 * (2 - E)) - E / 2 =
    E / 2 * (1 / (2 * E * (2 - E) / (κ * (E - 2 * δ) ^ 2)) - 1) := by
  have hd : 2 - E ≠ 0 := by intro hn; apply h2; linarith
  field_simp
  ring

theorem alpha1_zero_requires_zero_E (E : ℝ) : -4 * E = 0 ↔ E = 0 := by
  constructor <;> intro h <;> linarith

theorem gyro_quartic_nonzero (κ γ : ℝ) (hκ : κ ≠ 0) (hγ : γ ≠ 0) :
    -κ * γ ^ 2 ≠ 0 := by exact mul_ne_zero (neg_ne_zero.mpr hκ) (pow_ne_zero 2 hγ)

end PushLapse20260926

#print axioms PushLapse20260926.contact_locus_product
#print axioms PushLapse20260926.contact_speed_identity
#print axioms PushLapse20260926.negative_E_contact_instability
#print axioms PushLapse20260926.positive_cell_identity
#print axioms PushLapse20260926.positive_cell_speed
#print axioms PushLapse20260926.positive_cell_bound_identity
#print axioms PushLapse20260926.positive_cell_subluminal
#print axioms PushLapse20260926.alpha2_completed_square
#print axioms PushLapse20260926.alpha2_speed_identity
#print axioms PushLapse20260926.alpha1_zero_requires_zero_E
#print axioms PushLapse20260926.gyro_quartic_nonzero
