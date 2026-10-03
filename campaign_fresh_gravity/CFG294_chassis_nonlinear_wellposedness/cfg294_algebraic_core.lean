import Mathlib

/-!
# CFG294 — algebraic core of the chassis local well-posedness derivation

SCOPE. Lean certifies only the algebraic facts used by
`cfg294_chassis_nonlinear_wellposedness.py`. It does not certify any analysis theorem: not Kreiss, Kato, Andersson–Moncrief,
elliptic regularity, or well-posedness.

The rational numbers are the lane's exact record values (6 significant digits, CFG292 rounding):
alpha_max = 3.2e-9 = 1/312500000 and the lowest record c_2 = 6.30957e-4 = 630957/1000000000.
The scalar speed is c_S² = c₂(2 − α)/(α(2 + 3c₂)) at beta = 0.

* `cs2_gap_window`: on the whole window (0 < α ≤ α_max, c₂ ≥ c₂_low), c₂(2 − α) > 443² α(2 + 3c₂), i.e. c_S > 443 > 1.
  The two families {±1} and {±c_S} never cross (S1b).
* `cs2_gap_real`: the same as a statement about c_S².
* `crossing_locus`, `crossing_outside_window`: c_S² = 1 exactly on α = c₂/(1 + 2c₂), which lies above α_max for every
  c₂ ≥ c₂_low (S1d; the MUTATE locus).
* `projector_sum_bound`: ‖x₁ + x₂ + x₃ + x₄‖² ≤ 4 Σ‖x_j‖². With x_j = P_j v and Σ P_j = I this is vᵀHv ≥ |v|²/4 for
  H = Σ P_jᵀP_j (S2: λ_min(H) ≥ 1/4).
* `lapse_signs`: for 0 < α < 1/2 the physical lapse coefficient 4α is positive and the F2a coefficient (2α − 1)/4 is
  negative (S4b).
* `f2a_bianchi_definite`, `physical_resonance`: if W < 0 then (α − 1/2)k² + W < 0 for every k² ≥ 0, so the F2a lapse
  operator has no kernel. The physical αk² + W vanishes at k² = −W/α (S4c Lag).
* `dust_threshold`: the dust term of W is negative iff u² < 2/3.
-/

theorem cs2_gap_window (α c : ℝ) (ha : 0 < α) (ham : α ≤ 1 / 312500000) (hc : 630957 / 1000000000 ≤ c) :
    c * (2 - α) > 443 ^ 2 * (α * (2 + 3 * c)) := by
  have hD : 0 ≤ 2 - α * (1 + 3 * 443 ^ 2) := by nlinarith
  have h1 : 0 ≤ (c - 630957 / 1000000000) * (2 - α * (1 + 3 * 443 ^ 2)) := mul_nonneg (by linarith) hD
  have h2 : 0 ≤ (630957 / 1000000000 : ℝ) * (1 + 3 * 443 ^ 2) * (1 / 312500000 - α) := by
    apply mul_nonneg; · norm_num
    · linarith
  nlinarith [h1, h2]

theorem cs2_gap_real (α c : ℝ) (ha : 0 < α) (ham : α ≤ 1 / 312500000) (hc : 630957 / 1000000000 ≤ c) :
    c * (2 - α) / (α * (2 + 3 * c)) > 443 ^ 2 := by
  have hc0 : 0 < c := by linarith
  have hden : 0 < α * (2 + 3 * c) := by positivity
  rw [gt_iff_lt, lt_div_iff₀ hden]
  exact cs2_gap_window α c ha ham hc

theorem crossing_locus (α c : ℝ) (_ha : 0 < α) (hc : 0 < c) :
    c * (2 - α) = α * (2 + 3 * c) ↔ α = c / (1 + 2 * c) := by
  have h12 : 0 < 1 + 2 * c := by linarith
  rw [eq_div_iff h12.ne']
  constructor <;> intro h <;> linarith

theorem crossing_outside_window (c : ℝ) (hc : 630957 / 1000000000 ≤ c) :
    (1 / 312500000 : ℝ) < c / (1 + 2 * c) := by
  have h12 : 0 < 1 + 2 * c := by linarith
  rw [lt_div_iff₀ h12]
  nlinarith

theorem projector_sum_bound {E : Type*} [SeminormedAddCommGroup E] (x₁ x₂ x₃ x₄ : E) :
    ‖x₁ + x₂ + x₃ + x₄‖ ^ 2 ≤ 4 * (‖x₁‖ ^ 2 + ‖x₂‖ ^ 2 + ‖x₃‖ ^ 2 + ‖x₄‖ ^ 2) := by
  have ht : ‖x₁ + x₂ + x₃ + x₄‖ ≤ ‖x₁‖ + ‖x₂‖ + ‖x₃‖ + ‖x₄‖ := by
    calc ‖x₁ + x₂ + x₃ + x₄‖ ≤ ‖x₁ + x₂ + x₃‖ + ‖x₄‖ := norm_add_le _ _
      _ ≤ ‖x₁ + x₂‖ + ‖x₃‖ + ‖x₄‖ := by gcongr; exact norm_add_le _ _
      _ ≤ ‖x₁‖ + ‖x₂‖ + ‖x₃‖ + ‖x₄‖ := by gcongr; exact norm_add_le _ _
  have h0 : 0 ≤ ‖x₁ + x₂ + x₃ + x₄‖ := norm_nonneg _
  have hsq : ‖x₁ + x₂ + x₃ + x₄‖ ^ 2 ≤ (‖x₁‖ + ‖x₂‖ + ‖x₃‖ + ‖x₄‖) ^ 2 := by
    exact pow_le_pow_left₀ h0 ht 2
  nlinarith [sq_nonneg (‖x₁‖ - ‖x₂‖), sq_nonneg (‖x₁‖ - ‖x₃‖), sq_nonneg (‖x₁‖ - ‖x₄‖),
    sq_nonneg (‖x₂‖ - ‖x₃‖), sq_nonneg (‖x₂‖ - ‖x₄‖), sq_nonneg (‖x₃‖ - ‖x₄‖)]

theorem lapse_signs (α : ℝ) (ha : 0 < α) (hh : α < 1 / 2) :
    (2 * α - 1) / 4 < 0 ∧ 0 < α / 2 ∧ 0 < 4 * α := by
  refine ⟨by linarith, by linarith, by linarith⟩

theorem f2a_bianchi_definite (α W k2 : ℝ) (hh : α < 1 / 2) (hW : W < 0) (hk : 0 ≤ k2) :
    (α - 1 / 2) * k2 + W < 0 := by
  nlinarith

theorem physical_resonance (α W : ℝ) (ha : 0 < α) (hW : W < 0) :
    0 < -W / α ∧ α * (-W / α) + W = 0 := by
  refine ⟨div_pos (by linarith) ha, ?_⟩
  field_simp
  ring

theorem dust_threshold (u : ℝ) : 0 < 2 - 3 * u ^ 2 ↔ u ^ 2 < 2 / 3 := by
  constructor <;> intro h <;> linarith

#print axioms cs2_gap_window
#print axioms cs2_gap_real
#print axioms crossing_locus
#print axioms crossing_outside_window
#print axioms projector_sum_bound
#print axioms lapse_signs
#print axioms f2a_bianchi_definite
#print axioms physical_resonance
#print axioms dust_threshold
