import Mathlib

/-! Algebra for the stated frozen scalar action only. No action-to-block bridge,
physical field classification, PDE theorem or observational bound is assumed as
an axiom or claimed as a conclusion. E is the independently derived static
coefficient. The positive-minor witness has K = 16 I and zeta = 1/4. -/
namespace DoorsResponse20260926

theorem matched_static_gain (μ : ℝ) (hμ : μ ≠ 0) :
    2 / (2 - 2 * (1 - μ)) = 1 / μ := by
  have hden : 2 - 2 * (1 - μ) ≠ 0 := by intro h; apply hμ; linarith
  field_simp [hμ, hden]
  ring

theorem high_response_parameter_negative (μ : ℝ) (hμ : 1 < μ) :
    2 * (1 - μ) < 0 := by linarith

theorem scalar_speed_negative (E B : ℝ) (hE : E < 0) (hB : 0 < B) :
    B * (2 - E) / ((2 + 3 * B) * E) < 0 := by
  apply div_neg_of_pos_of_neg
  · exact mul_pos hB (by linarith)
  · exact mul_neg_of_pos_of_neg (by positivity) hE

theorem potential_direction_identity (a b d : ℝ) (hd : d ≠ 0) :
    a + 2 * b * (-b / d) + d * (-b / d) ^ 2 = a - b ^ 2 / d := by
  field_simp
  ring

noncomputable def v11 (E : ℝ) : ℝ := 4 / (E - 1 / 4) - 2
noncomputable def v12 (E : ℝ) : ℝ := (1 / 2) / (E - 1 / 4)
noncomputable def v22 (E : ℝ) : ℝ := E / (4 * (E - 1 / 4))

theorem potential_determinant (E : ℝ) (hE : E - 1 / 4 ≠ 0) :
    v11 E * v22 E - (v12 E) ^ 2 = 2 * (2 - E) / (4 * E - 1) := by
  have hfour : 4 * E - 1 ≠ 0 := by intro h; apply hE; linarith
  unfold v11 v12 v22
  field_simp
  ring

theorem causal_complement_determinant (E : ℝ) (hE : E - 1 / 4 ≠ 0) :
    (16 - v11 E) * (16 - v22 E) - (v12 E) ^ 2 =
      54 * (21 * E - 10) / (4 * E - 1) := by
  have hfour : 4 * E - 1 ≠ 0 := by intro h; apply hE; linarith
  unfold v11 v12 v22
  field_simp
  ring

theorem low_branch_positive_minors (E : ℝ) (hl : 1 / 2 < E) (hu : E < 2) :
    0 < v11 E ∧ 0 < v11 E * v22 E - (v12 E) ^ 2 := by
  have hd : 0 < E - 1 / 4 := by linarith
  constructor
  · unfold v11
    have h : 2 < 4 / (E - 1 / 4) := (lt_div_iff₀ hd).2 (by nlinarith)
    linarith
  · rw [potential_determinant E (ne_of_gt hd)]
    apply div_pos <;> nlinarith

theorem low_branch_causal_minors (E : ℝ) (hl : 1 / 2 < E) :
    0 < 16 - v11 E ∧
      0 < (16 - v11 E) * (16 - v22 E) - (v12 E) ^ 2 := by
  have hd : 0 < E - 1 / 4 := by linarith
  constructor
  · unfold v11
    have h : 4 / (E - 1 / 4) < 16 := (div_lt_iff₀ hd).2 (by nlinarith)
    linarith
  · rw [causal_complement_determinant E (ne_of_gt hd)]
    apply div_pos <;> nlinarith

noncomputable def rankDen (E z r : ℝ) : ℝ :=
  E * (z - 2 * r ^ 2) + 2 * r ^ 2 * z + 4 * r ^ 2 - 4 * r * z

theorem rank_contact_zero_cases (E z r : ℝ) (h : r ^ 2 * (E - z) = 0) :
    r = 0 ∨ E = z := by
  rcases mul_eq_zero.mp h with hr | he
  · left; nlinarith [sq_nonneg r]
  · right; linarith

theorem equal_parameter_rank_square (E r : ℝ) :
    rankDen E E r = (E - 2 * r) ^ 2 := by unfold rankDen; ring

theorem high_branch_contact_cancellation_unstable (E z r κ : ℝ)
    (hE : E < 0) (hz : z ≠ 0) (hκ : 0 < κ)
    (hD : rankDen E z r ≠ 0) (hcontact : r ^ 2 * (E - z) = 0) :
    2 * z * (2 - E) / (κ * rankDen E z r) < 0 := by
  rcases rank_contact_zero_cases E z r hcontact with hr | he
  · subst r
    have he0 : E ≠ 0 := ne_of_lt hE
    have hk0 : κ ≠ 0 := ne_of_gt hκ
    have hid : 2 * z * (2 - E) / (κ * rankDen E z 0) =
        2 * (2 - E) / (κ * E) := by
      unfold rankDen
      field_simp [hz, he0, hk0]
      ring
    rw [hid]
    apply div_neg_of_pos_of_neg
    · nlinarith
    · exact mul_neg_of_pos_of_neg hκ hE
  · subst z
    rw [equal_parameter_rank_square] at hD ⊢
    have hs : 0 < (E - 2 * r) ^ 2 := lt_of_le_of_ne (sq_nonneg _) (Ne.symm hD)
    apply div_neg_of_neg_of_pos
    · have hp : 0 < 2 - E := by linarith
      exact mul_neg_of_neg_of_pos (by linarith) hp
    · exact mul_pos hκ hs

end DoorsResponse20260926

#print axioms DoorsResponse20260926.matched_static_gain
#print axioms DoorsResponse20260926.high_response_parameter_negative
#print axioms DoorsResponse20260926.scalar_speed_negative
#print axioms DoorsResponse20260926.potential_direction_identity
#print axioms DoorsResponse20260926.potential_determinant
#print axioms DoorsResponse20260926.causal_complement_determinant
#print axioms DoorsResponse20260926.low_branch_positive_minors
#print axioms DoorsResponse20260926.low_branch_causal_minors
#print axioms DoorsResponse20260926.rank_contact_zero_cases
#print axioms DoorsResponse20260926.equal_parameter_rank_square
#print axioms DoorsResponse20260926.high_branch_contact_cancellation_unstable
