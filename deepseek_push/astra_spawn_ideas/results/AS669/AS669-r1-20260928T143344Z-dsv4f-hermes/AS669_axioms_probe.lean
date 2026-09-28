import Mathlib

/-! Axiom probe for the AS669 certificate file. Compile this as a SEPARATE
file so `#print axioms` output is captured independently. -/

noncomputable section
open scoped BigOperators

theorem flux_identity_fixes_volume {q V W : ℝ} (hq : q ≠ 0) (h : q * V = q * W) : V = W :=
  mul_left_cancel₀ hq h

theorem simultaneous_fixing_inconsistent {q V W : ℝ} (hq : q ≠ 0) (hV : V ≠ W) :
    ¬ (q * V = q * W) := by
  intro h
  exact hV (flux_identity_fixes_volume hq h)

theorem dilution_ratio {q1 q2 V1 V2 Φ : ℝ} (hq1 : q1 ≠ 0) (hV1 : V1 ≠ 0)
    (h1 : q1 * V1 = Φ) (h2 : q2 * V2 = Φ) : q2 = q1 * V1 / V2 := by
  have hV2 : V2 ≠ 0 := by
    intro hz
    have h : q2 * V2 = q1 * V1 := by
      rw [h2, ← h1]
    rw [hz, mul_zero] at h
    exact (mul_ne_zero hq1 hV1) h.symm
  have h : q2 * V2 = q1 * V1 := by
    rw [h2, ← h1]
  calc
    q2 = q2 * V2 / V2 := by field_simp [hV2]
    _ = q1 * V1 / V2 := by rw [h]

theorem fixed_q_law {q V1 V2 : ℝ} (hq : q ≠ 0) (hV1 : V1 ≠ 0) :
    (q * V2) / (q * V1) = V2 / V1 := by
  field_simp [hq, hV1]

theorem legendre_quadratic {Z b β q : ℝ} :
    q * (Z * q + 2 * (b * β ^ 2) * q) - ((Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2)
      = (Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2 := by
  ring

theorem eps_positive {Z b β q : ℝ} (hZ : 0 < Z) (hb : 0 < b) (hβ : β ≠ 0) (hq : q ≠ 0) :
    0 < (Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2 := by
  have hq2 : 0 < q ^ 2 := sq_pos_of_ne_zero hq
  have hβ2 : 0 < β ^ 2 := sq_pos_of_ne_zero hβ
  have hz2 : 0 < (Z / 2 : ℝ) := by positivity
  have h1 : 0 < (Z / 2) * q ^ 2 := mul_pos hz2 hq2
  have h2 : 0 < (b * β ^ 2) * q ^ 2 := mul_pos (mul_pos hb hβ2) hq2
  exact add_pos h1 h2

theorem kappa_raw_eq_simpl {Z b β q : ℝ} (hq : q ≠ 0) (_hden : Z + 2 * b * β ^ 2 ≠ 0) :
    β ^ 2 * q ^ 2 / ((Z / 2) * q ^ 2 + (b * β ^ 2) * q ^ 2)
      = 2 * β ^ 2 / (Z + 2 * b * β ^ 2) := by
  field_simp [hq, _hden]

theorem kappa_volume_blind {Z b β q1 q2 : ℝ} (hq1 : q1 ≠ 0) (hq2 : q2 ≠ 0)
    (_hden : Z + 2 * b * β ^ 2 ≠ 0) :
    β ^ 2 * q1 ^ 2 / ((Z / 2) * q1 ^ 2 + (b * β ^ 2) * q1 ^ 2)
      = β ^ 2 * q2 ^ 2 / ((Z / 2) * q2 ^ 2 + (b * β ^ 2) * q2 ^ 2) := by
  rw [kappa_raw_eq_simpl hq1 _hden, kappa_raw_eq_simpl hq2 _hden]

theorem half_iff_ratio {Z b β : ℝ} (_hden : Z + 2 * b * β ^ 2 ≠ 0) :
    2 * β ^ 2 / (Z + 2 * b * β ^ 2) = (1 : ℝ) / 4 ↔ Z = (8 - 2 * b) * β ^ 2 := by
  constructor
  · intro h
    have hc : 2 * β ^ 2 = (1 / 4 : ℝ) * (Z + 2 * b * β ^ 2) := (div_eq_iff _hden).mp h
    nlinarith
  · intro hZ
    apply (div_eq_iff _hden).mpr
    rw [hZ]
    nlinarith

theorem residual_nonzero {q V1 V2 : ℝ} (hq : q ≠ 0) (hV : V1 ≠ V2) : q * V1 ≠ q * V2 := by
  intro h
  exact hV (flux_identity_fixes_volume hq h)

#print axioms flux_identity_fixes_volume
#print axioms simultaneous_fixing_inconsistent
#print axioms dilution_ratio
#print axioms fixed_q_law
#print axioms legendre_quadratic
#print axioms eps_positive
#print axioms kappa_raw_eq_simpl
#print axioms kappa_volume_blind
#print axioms half_iff_ratio
#print axioms residual_nonzero

end
