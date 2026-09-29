import Mathlib

/-!
# M3B -- the reciprocal barrier F(t) = 1 + (t + 1/t - 2)^2: derivative chain, flat jet, Taylor remainder

Source: `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md` (R2) and `vacuum/check.py`
(checks `first_derivative`, `convexity_factor`, `third_derivative`, `flat_derivative_1..3`,
`fourth_derivative_24`, `Taylor_remainder_factor`, `general_IR_condition`).
The committed `ReciprocalVacuum20260926.lean` proves the algebraic identities (quartic form, inversion,
positive floor, factored curvature) but DEFINES `curvature` by its formula; it never proves that this is
the second derivative of F.  AS229's Lean file says the derivative chain was not achieved.  Here it is.

CERTIFIED (for every real t != 0):
  * F' = 2 (t-1)^3 (t+1) / t^3,  F'' = 2 (t-1)^2 (t^2+2t+3) / t^4,  F''' = 24 (t-1) / t^5,
    F'''' = 24 (5 - 4 t) / t^6, each as a `HasDerivAt` link of one chain;
  * the flat jet at t = 1: F(1) = 1, F'(1) = F''(1) = F'''(1) = 0, F''''(1) = 24;
  * `taylor_remainder`: F(t) - [F(d) + F'(d)(t-d) + F''(d)(t-d)^2/2] = (t-d)^3 (4 d t - d - 3 t) / (d^4 t^2)
    (d, t != 0), the identity behind the BARRIER_PROOF.md regularisation;
  * `IR_condition_general`: for the general-vacuum coefficient D_F(0) = -6 H^2 r0 (f1 + r0 f2/2),
    with H, r0 != 0:  D_F(0) = 0  <->  f1 + (r0/2) f2 = 0   (R6 as an equivalence);
    the reciprocal barrier has f1 = f2 = 0 (from the jet above) so R6 holds for every r0.

NOT CERTIFIED: that D_F has the displayed form (it is a hypothesis-free definition here), the
claim that R6 is sufficient for all-mode stability (ACTION.md says it is not), V0, anything about the
full field theory.  No physical claim is an axiom.
-/

noncomputable section
namespace M3B

/-- F(t) = 1 + (t + 1/t - 2)^2 -/
def F (t : ℝ) : ℝ := 1 + (t + t⁻¹ - 2) ^ 2
def F1 (t : ℝ) : ℝ := 2 * (t - 1) ^ 3 * (t + 1) / t ^ 3
def F2 (t : ℝ) : ℝ := 2 * (t - 1) ^ 2 * (t ^ 2 + 2 * t + 3) / t ^ 4
def F3 (t : ℝ) : ℝ := 24 * (t - 1) / t ^ 5
def F4 (t : ℝ) : ℝ := 24 * (5 - 4 * t) / t ^ 6

theorem hasDeriv_F (t : ℝ) (ht : t ≠ 0) : HasDerivAt F (F1 t) t := by
  have h0 : HasDerivAt (fun s : ℝ => s + s⁻¹) (1 + -(t ^ 2)⁻¹) t :=
    (hasDerivAt_id' t).add (hasDerivAt_inv ht)
  have h1 : HasDerivAt (fun s : ℝ => 1 + (s + s⁻¹ - 2) ^ 2)
      (2 * (t + t⁻¹ - 2) * (1 + -(t ^ 2)⁻¹)) t := by
    have := ((h0.sub_const 2).pow 2).const_add 1
    simpa using this
  refine h1.congr_deriv ?_
  unfold F1
  field_simp
  ring

theorem hasDeriv_F1 (t : ℝ) (ht : t ≠ 0) : HasDerivAt F1 (F2 t) t := by
  have hn : HasDerivAt (fun s : ℝ => 2 * (s - 1) ^ 3 * (s + 1))
      (2 * (3 * (t - 1) ^ 2) * (t + 1) + 2 * (t - 1) ^ 3) t := by
    have h1 := ((hasDerivAt_id' t).sub_const 1).pow 3
    have h2 := (h1.const_mul 2).mul ((hasDerivAt_id' t).add_const 1)
    refine h2.congr_deriv ?_
    simp
  have hd : HasDerivAt (fun s : ℝ => s ^ 3) (3 * t ^ 2) t := by
    simpa using hasDerivAt_pow 3 t
  have h := hn.div hd (pow_ne_zero 3 ht)
  refine h.congr_deriv ?_
  unfold F2
  field_simp
  ring

theorem hasDeriv_F2 (t : ℝ) (ht : t ≠ 0) : HasDerivAt F2 (F3 t) t := by
  have hn : HasDerivAt (fun s : ℝ => 2 * (s - 1) ^ 2 * (s ^ 2 + 2 * s + 3))
      (2 * (2 * (t - 1)) * (t ^ 2 + 2 * t + 3) + 2 * (t - 1) ^ 2 * (2 * t + 2)) t := by
    have h1 := ((hasDerivAt_id' t).sub_const 1).pow 2
    have h3 : HasDerivAt (fun s : ℝ => s ^ 2 + 2 * s + 3) (2 * t + 2) t := by
      have := (((hasDerivAt_id' t).pow 2).add ((hasDerivAt_id' t).const_mul 2)).add_const 3
      refine this.congr_deriv ?_
      simp
    have h2 := (h1.const_mul 2).mul h3
    refine h2.congr_deriv ?_
    simp
  have hd : HasDerivAt (fun s : ℝ => s ^ 4) (4 * t ^ 3) t := by
    simpa using hasDerivAt_pow 4 t
  have h := hn.div hd (pow_ne_zero 4 ht)
  refine h.congr_deriv ?_
  unfold F3
  field_simp
  ring

theorem hasDeriv_F3 (t : ℝ) (ht : t ≠ 0) : HasDerivAt F3 (F4 t) t := by
  have hn : HasDerivAt (fun s : ℝ => 24 * (s - 1)) 24 t := by
    have := ((hasDerivAt_id' t).sub_const 1).const_mul 24
    refine this.congr_deriv ?_
    simp
  have hd : HasDerivAt (fun s : ℝ => s ^ 5) (5 * t ^ 4) t := by
    simpa using hasDerivAt_pow 5 t
  have h := hn.div hd (pow_ne_zero 5 ht)
  refine h.congr_deriv ?_
  unfold F4
  field_simp
  ring

theorem flat_jet :
    F 1 = 1 ∧ F1 1 = 0 ∧ F2 1 = 0 ∧ F3 1 = 0 ∧ F4 1 = 25 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> norm_num [F, F1, F2, F3, F4]

/-- The whole chain at t = 1, stated as derivatives of the functions. -/
theorem jet_at_one :
    HasDerivAt F 0 1 ∧ HasDerivAt F1 0 1 ∧ HasDerivAt F2 0 1 ∧ HasDerivAt F3 24 1 := by
  have h0 := hasDeriv_F 1 one_ne_zero
  have h1 := hasDeriv_F1 1 one_ne_zero
  have h2 := hasDeriv_F2 1 one_ne_zero
  have h3 := hasDeriv_F3 1 one_ne_zero
  obtain ⟨_, a1, a2, a3, a4⟩ := flat_jet
  rw [a1] at h0
  rw [a2] at h1
  rw [a3] at h2
  rw [a4] at h3
  exact ⟨h0, h1, h2, h3⟩

theorem taylor_remainder (d t : ℝ) (hd : d ≠ 0) (ht : t ≠ 0) :
    F t - (F d + F1 d * (t - d) + F2 d * (t - d) ^ 2 / 2)
      = (t - d) ^ 3 * (4 * d * t - d - 3 * t) / (d ^ 4 * t ^ 2) := by
  unfold F F1 F2
  field_simp
  ring

theorem IR_condition_general (H r0 f1 f2 : ℝ) (hH : H ≠ 0) (hr : r0 ≠ 0) :
    -6 * H ^ 2 * r0 * (f1 + f2 * r0 / 2) = 0 ↔ f1 + r0 / 2 * f2 = 0 := by
  have hn : -6 * H ^ 2 * r0 ≠ 0 := by
    have : H ^ 2 ≠ 0 := pow_ne_zero 2 hH
    intro h
    have : (-6 : ℝ) * (H ^ 2 * r0) = 0 := by linarith
    rcases mul_eq_zero.mp this with h | h
    · norm_num at h
    · rcases mul_eq_zero.mp h with h | h <;> contradiction
  rw [mul_eq_zero, or_iff_right hn]
  constructor <;> intro h <;> linarith

/-- The reciprocal barrier satisfies R6 for every r0 (f1 = F'(1), f2 = F''(1)). -/
theorem reciprocal_satisfies_R6 (H r0 : ℝ) :
    -6 * H ^ 2 * r0 * (F1 1 + F2 1 * r0 / 2) = 0 := by
  obtain ⟨_, a1, a2, _, _⟩ := flat_jet
  rw [a1, a2]; ring

end M3B

#print axioms M3B.hasDeriv_F
#print axioms M3B.hasDeriv_F1
#print axioms M3B.hasDeriv_F2
#print axioms M3B.hasDeriv_F3
#print axioms M3B.flat_jet
#print axioms M3B.jet_at_one
#print axioms M3B.taylor_remainder
#print axioms M3B.IR_condition_general
#print axioms M3B.reciprocal_satisfies_R6
