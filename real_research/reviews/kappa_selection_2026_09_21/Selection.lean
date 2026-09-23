import Mathlib

/-! Exact normalization obstruction for the specified static auxiliary family.
No assertion about all covariant completions or empirical adequacy is made. -/
namespace KappaSelection
noncomputable section

def engagement (lam y : ℝ) : ℝ := lam*y/(1+lam*y)
def response (lam y : ℝ) : ℝ := 1-(1-engagement lam y)^2
def a0 (s lam : ℝ) : ℝ := s/(2*lam)
def normalizedResponse (lam x : ℝ) : ℝ := response lam (x/(2*lam))

/-- Two equal channels do not set their common susceptibility. -/
theorem channel_susceptibility (lam : ℝ) :
    HasDerivAt (engagement lam) lam 0 := by
  have hn : HasDerivAt (fun y : ℝ => lam*y) lam 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).const_mul lam
  convert! hn.div (hn.const_add 1) (by norm_num : (1 : ℝ)+lam*0 ≠ 0) using 1
  simp

theorem response_susceptibility (lam : ℝ) :
    HasDerivAt (response lam) (2*lam) 0 := by
  have h := ((channel_susceptibility lam).const_sub 1).pow 2 |>.const_sub 1
  convert! h using 1
  simp [engagement]

/-- Channel count multiplies susceptibility; it does not replace it. -/
theorem channel_count_slope (n : ℕ) (lam : ℝ) :
    HasDerivAt (fun y : ℝ => 1-(1-engagement lam y)^n) ((n:ℝ)*lam) 0 := by
  have h := ((channel_susceptibility lam).const_sub 1).pow n |>.const_sub 1
  convert! h using 1
  simp [engagement]

/-- Same independently fixed positive s, two different matched coefficients. -/
theorem fixed_scale_counterexample {s : ℝ} (hs : s ≠ 0) :
    a0 s 1 / s = (1:ℝ)/2 ∧ a0 s 2 / s = (1:ℝ)/4 ∧
    a0 s 2 / s ≠ (1:ℝ)/2 := by
  simp only [a0]
  constructor
  · field_simp
  constructor
  · field_simp; ring
  · field_simp
    norm_num

/-- At x=g/a0 the lambda-dependence cancels, without taking a limit. -/
theorem normalized_response_exact {lam : ℝ} (hlam : lam ≠ 0) (x : ℝ) :
    normalizedResponse lam x = response 1 (x/2) := by
  have h : lam*(x/(2*lam)) = x/2 := by field_simp
  simp [normalizedResponse, response, engagement, h]

/-- No predicate of this entire normalized curve can distinguish positive weights. -/
theorem no_normalized_shape_selector
    (P : (ℝ → ℝ) → Prop) {lam₁ lam₂ : ℝ} (h₁ : lam₁ ≠ 0) (h₂ : lam₂ ≠ 0) :
    P (normalizedResponse lam₁) ↔ P (normalizedResponse lam₂) := by
  have he : normalizedResponse lam₁ = normalizedResponse lam₂ := by
    funext x
    rw [normalized_response_exact h₁, normalized_response_exact h₂]
  rw [he]

/-- Actual static density before eliminating either auxiliary variable.
U is arbitrary here: the scaling obstruction does not depend on its detailed form. -/
def density (U : ℝ → ℝ) (s lam g q₁ q₂ : ℝ) : ℝ :=
  s^2 * ((g/s)^2*(1-q₁*q₂) + (U q₁+U q₂)/lam^2)

theorem action_depends_on_ratio (U : ℝ → ℝ) {s lam : ℝ}
    (hs : s ≠ 0) (hlam : lam ≠ 0) (g q₁ q₂ : ℝ) :
    density U s lam g q₁ q₂ = density U (s/lam) 1 g q₁ q₂ := by
  unfold density
  field_simp

/-- Rewriting the full density in terms of the matched acceleration removes lambda. -/
theorem action_at_fixed_a0 (U : ℝ → ℝ) {s lam : ℝ}
    (hs : s ≠ 0) (hlam : lam ≠ 0) (g q₁ q₂ : ℝ) :
    density U s lam g q₁ q₂ =
    g^2*(1-q₁*q₂) + 4*(a0 s lam)^2*(U q₁+U q₂) := by
  unfold density a0
  field_simp
  ring

/-- These are the static transverse and longitudinal principal coefficients;
the derivative identification is also checked independently in verify.py. -/
def transverse (lam y : ℝ) : ℝ :=
  (lam*y)*(lam*y+2)/(1+lam*y)^2
def longitudinal (lam y : ℝ) : ℝ :=
  (lam*y)*((lam*y)^2+3*lam*y+4)/(1+lam*y)^3

theorem static_admissibility {lam y : ℝ} (hlam : 0 < lam) (hy : 0 < y) :
    0 < transverse lam y ∧ 0 < longitudinal lam y := by
  unfold transverse longitudinal
  constructor <;> positivity

theorem bounded_response {lam y : ℝ} (hlam : 0 < lam) (hy : 0 ≤ y) :
    0 ≤ response lam y ∧ response lam y ≤ 1 := by
  have ht : 0 ≤ lam*y := mul_nonneg hlam.le hy
  have hd : 0 < 1+lam*y := by linarith
  have hp : 0 ≤ engagement lam y := div_nonneg ht hd.le
  have hpu : engagement lam y ≤ 1 := by
    unfold engagement
    apply (div_le_one hd).mpr
    linarith
  unfold response
  constructor
  · nlinarith [sq_nonneg (engagement lam y)]
  · nlinarith [sq_nonneg (1-engagement lam y)]

/-- Formal non-entailment from the stated static inequalities, at fixed s.
Saturation and the variational identification are separately checked in verify.py. -/
theorem static_conditions_do_not_force_half {s : ℝ} (hs : 0 < s) :
    ∃ lam : ℝ, 0 < lam ∧
      (∀ y : ℝ, 0 ≤ y → 0 ≤ response lam y ∧ response lam y ≤ 1) ∧
      (∀ y : ℝ, 0 < y → 0 < transverse lam y ∧ 0 < longitudinal lam y) ∧
      a0 s lam / s ≠ (1:ℝ)/2 := by
  refine ⟨2, by norm_num, ?_, ?_, (fixed_scale_counterexample hs.ne').2.2⟩
  · intro y hy
    exact bounded_response (by norm_num) hy
  · intro y hy
    exact static_admissibility (by norm_num) hy

/-- Saturation rate and deep susceptibility supply no independent normalization:
their product is the same for every nonzero lambda. -/
theorem slope_tail_invariant {lam : ℝ} (hlam : lam ≠ 0) :
    (2*lam)^2 * (1/lam^2) = (4:ℝ) := by field_simp; ring

/-- The lambda derivative of the reduced W at lambda=y=1 is strictly positive.
verify.py separately checks that derivative identification from the raw expression. -/
theorem unit_weight_variation_positive : 0 < 4*Real.log 2 - (5:ℝ)/2 := by
  have h := Real.lt_log_one_add_of_pos (show (0:ℝ) < 1 by norm_num)
  norm_num at h
  linarith

#print axioms channel_susceptibility
#print axioms response_susceptibility
#print axioms channel_count_slope
#print axioms fixed_scale_counterexample
#print axioms normalized_response_exact
#print axioms no_normalized_shape_selector
#print axioms action_depends_on_ratio
#print axioms action_at_fixed_a0
#print axioms static_admissibility
#print axioms bounded_response
#print axioms static_conditions_do_not_force_half
#print axioms slope_tail_invariant
#print axioms unit_weight_variation_positive
end
end KappaSelection
