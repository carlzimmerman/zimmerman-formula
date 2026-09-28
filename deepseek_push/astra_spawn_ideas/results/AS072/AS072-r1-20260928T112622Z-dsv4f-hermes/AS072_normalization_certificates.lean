import Mathlib
open Real

noncomputable section

/-!
AS072 -- A normalization theorem with explicit assumptions.
Lean 4 certificates for the algebraic core of the conditional theorem
"n = 2 OR-composition with unit per-channel slopes + vacuum scale s
  => deep matching g^2 = (s/2) B => kappa = a0/s = 1/2".

Certified here (and ONLY here):
  T1  the equal-channel OR expansion on the generic 2-jet (ring):
      mu = 2y + (2c-1) y^2 - 2 c y^3 - c^2 y^4   -- origin slope 2, completion-independent
  T2  the unequal-channel OR expansion (ring): origin slope b1 + b2
  T3  HasDerivAt version of T1: d/dy [1-(1-(y+c y^2))^2] |_0 = 2 for every c
  T4  the lambda-family jet: d/dy [1-(1-(lam y + c y^2))^2] |_0 = 2 lam
      (the A3-removal counterexample: per-channel slope lam changes kappa)
  T5  generic chain rule THROUGH the OR composition: from p_i(0)=0 and
      HasDerivAt p_i b_i 0 follows mu'(0) = b1 + b2
  T6  the rational lambda-family member p(y) = lam y / (1 + lam y) has
      p(0) = 0 and HasDerivAt p lam 0   (the premise family of AS053)
  T7  the truncated L230 matching identity: b (g/s) g = B  =>  g^2 = s B / b
  T8  its n = 2, b = 2 specialization: 2 (g/s) g = B => g^2 = (s/2) B
  T9  kappa = 1/2: (s/2)/s = 1/2 for s ≠ 0
  T10 saturation cleared forms: the corpus OR member and the lambda-family
      saturation (mu(inf) = 1) as epsilon-M statements
-/

/-- T1: equal-channel OR composition on the generic 2-jet p = y + c y^2:
    mu_OR = 1 - (1-p)^2 = 2y + (2c-1) y^2 - 2c y^3 - c^2 y^4. -/
theorem or_slope_jet_expansion (y c : ℝ) :
    1 - (1 - (y + c * y ^ 2)) ^ 2 =
      2 * y + (2 * c - 1) * y ^ 2 - 2 * c * y ^ 3 - c ^ 2 * y ^ 4 := by
  ring

/-- T2: unequal-channel OR composition on generic 2-jets
    p_i = b_i y + c_i y^2: mu'(0) coefficient is b1 + b2. -/
theorem or_unequal_jet_expansion (y b1 b2 c1 c2 : ℝ) :
    1 - (1 - (b1 * y + c1 * y ^ 2)) * (1 - (b2 * y + c2 * y ^ 2)) =
      (b1 + b2) * y + (c1 + c2 - b1 * b2) * y ^ 2
        - (b1 * c2 + b2 * c1) * y ^ 3 - c1 * c2 * y ^ 4 := by
  ring

/-- T3: derivative certificate of T1: the origin slope of the OR
    composition over one unit-slope jet is exactly 2, for EVERY completion
    coefficient c. -/
theorem or_slope_deriv (c : ℝ) :
    HasDerivAt (fun y : ℝ => 1 - (1 - (y + c * y ^ 2)) ^ 2) 2 0 := by
  have hlin : HasDerivAt (fun y : ℝ => y) 1 0 := hasDerivAt_id 0
  have hsqy : HasDerivAt (fun y : ℝ => y ^ 2) 0 0 := by
    convert! hasDerivAt_pow 2 (0 : ℝ) using 1 <;> simp
  have hin : HasDerivAt (fun y : ℝ => y + c * y ^ 2) 1 0 := by
    convert! hlin.add (hsqy.const_mul c) using 1 <;> simp
  have hone : HasDerivAt (fun y : ℝ => 1 - (y + c * y ^ 2)) (-1) 0 := by
    convert! hin.neg.const_add 1 using 1 <;> simp
  have hsqu : HasDerivAt (fun x : ℝ => x ^ 2) (2 * (1 : ℝ) ^ 1) 1 := by
    convert! hasDerivAt_pow 2 (1 : ℝ) using 1 <;> simp
  have hsq : HasDerivAt (fun y : ℝ => (1 - (y + c * y ^ 2)) ^ 2) (-2) 0 := by
    convert! hone.pow 2 using 1 <;> simp
  convert! hsq.neg.const_add 1 using 1 <;> simp

/-- T4: the A3-removal family at jet level: per-channel slope lam changes
    the OR slope to 2 lam (so the inferred kappa = 1/(2 lam)). -/
theorem lambda_family_slope_deriv (lam c : ℝ) :
    HasDerivAt (fun y : ℝ => 1 - (1 - (lam * y + c * y ^ 2)) ^ 2) (2 * lam) 0 := by
  have hlin : HasDerivAt (fun y : ℝ => y) 1 0 := hasDerivAt_id 0
  have hsqy : HasDerivAt (fun y : ℝ => y ^ 2) 0 0 := by
    convert! hasDerivAt_pow 2 (0 : ℝ) using 1 <;> simp
  have hin : HasDerivAt (fun y : ℝ => lam * y + c * y ^ 2) lam 0 := by
    convert! (hlin.const_mul lam).add (hsqy.const_mul c) using 1 <;> simp
  have hone : HasDerivAt (fun y : ℝ => 1 - (lam * y + c * y ^ 2)) (-lam) 0 := by
    convert! hin.neg.const_add 1 using 1 <;> simp
  have hsq : HasDerivAt (fun y : ℝ => (1 - (lam * y + c * y ^ 2)) ^ 2)
      (-(2 * lam)) 0 := by
    convert! hone.pow 2 using 1 <;> simp
  convert! hsq.neg.const_add 1 using 1 <;> ring

/-- T5: generic chain rule THROUGH the OR composition: with p_i(0) = 0 and
    p_i'(0) = b_i, the OR response has origin slope b1 + b2. -/
theorem or_chain_rule_unequal {p1 p2 : ℝ → ℝ} {b1 b2 : ℝ}
    (hp10 : p1 0 = 0) (hp20 : p2 0 = 0)
    (hp1 : HasDerivAt p1 b1 0) (hp2 : HasDerivAt p2 b2 0) :
    HasDerivAt (fun y : ℝ => 1 - (1 - p1 y) * (1 - p2 y)) (b1 + b2) 0 := by
  have hn1 : HasDerivAt (fun y : ℝ => 1 - p1 y) (-b1) 0 := by
    simpa [sub_eq_add_neg, add_comm] using hp1.neg.const_add 1
  have hn2 : HasDerivAt (fun y : ℝ => 1 - p2 y) (-b2) 0 := by
    simpa [sub_eq_add_neg, add_comm] using hp2.neg.const_add 1
  have hv1 : (1 - p1 0) = 1 := by simp [hp10]
  have hv2 : (1 - p2 0) = 1 := by simp [hp20]
  have hpr : HasDerivAt (fun y : ℝ => (1 - p1 y) * (1 - p2 y))
      ((-b1) * (1 - p2 0) + (1 - p1 0) * (-b2)) 0 := hn1.mul hn2
  have hprod : HasDerivAt (fun y : ℝ => (1 - p1 y) * (1 - p2 y))
      (-(b1 + b2)) 0 := by
    convert hpr using 1
    rw [hv1, hv2]
    ring
  convert! hprod.neg.const_add 1 using 1 <;> simp

/-- T6: the rational lambda-family member p(y) = lam y / (1 + lam y):
    p(0) = 0 and p'(0) = lam.  Everything in the premise A3 is varied by
    lam except the endpoints p(0)=0, p(inf)=1 and monotonicity. -/
theorem p_lam_value_zero (lam : ℝ) : lam * 0 / (1 + lam * 0) = 0 := by
  norm_num

theorem p_lam_has_deriv (lam : ℝ) :
    HasDerivAt (fun y : ℝ => lam * y / (1 + lam * y)) lam 0 := by
  have hlin : HasDerivAt (fun y : ℝ => y) 1 0 := hasDerivAt_id 0
  have hnum : HasDerivAt (fun y : ℝ => lam * y) lam 0 := by
    simpa using hlin.const_mul lam
  have hden : HasDerivAt (fun y : ℝ => 1 + lam * y) lam 0 := by
    simpa using (hlin.const_mul lam).const_add 1
  have hden0 : 1 + lam * 0 ≠ 0 := by norm_num
  have hdiv : HasDerivAt (fun y : ℝ => (lam * y) / (1 + lam * y))
      ((lam * (1 + lam * 0) - (lam * 0) * lam) / (1 + lam * 0) ^ 2) 0 :=
    hnum.div hden hden0
  convert! hdiv using 1 <;> simp

/-- T7: truncated L230 matching: the deep equation with mu ~ b*g/s,
    b (g/s) g = B, implies g^2 = s B / b (b ≠ 0, s ≠ 0). -/
theorem l230_truncated_matching {b s g B : ℝ} (hb : b ≠ 0) (hs : s ≠ 0)
    (h : b * (g / s) * g = B) : g ^ 2 = s * B / b := by
  have hclear : b * g ^ 2 = B * s := by
    field_simp [hs] at h
    nlinarith [h]
  field_simp [hb]
  nlinarith [hclear]

/-- T8: the n = 2 specialization: 2 (g/s) g = B implies g^2 = (s/2) B. -/
theorem l230_matching_two {s g B : ℝ} (hs : s ≠ 0)
    (h : 2 * (g / s) * g = B) : g ^ 2 = s * B / 2 := by
  exact l230_truncated_matching (by norm_num) hs h

/-- T9: kappa = a0/s = 1/2 for a0 = s/2, s ≠ 0. -/
theorem kappa_half (s : ℝ) (hs : s ≠ 0) : (s / 2) / s = 1 / 2 := by
  field_simp [hs]

/-- T10a: saturation of the corpus OR member mu(y) = 1 - 1/(1+y)^2,
    cleared form: the response is within eps of one for all y >= M
    (1 - mu = 1/(1+y)^2 < eps). -/
theorem sat_or_cleared : ∀ ε : ℝ, ε > 0 → ∃ M ≥ 0, ∀ y ≥ M, 1 < ε * (1 + y) ^ 2 := by
  intro ε hε
  refine ⟨1 / ε, ?M0, ?ball⟩
  · exact le_of_lt (div_pos (by norm_num) hε)
  · intro y hy
    have hMpos : 0 < 1 / ε := div_pos (by norm_num) hε
    have hy0 : 0 < y := lt_of_lt_of_le hMpos hy
    have hεinv : ε * (1 / ε) = 1 := by field_simp [hε.ne']
    have hle : 1 ≤ ε * y := by
      rw [← hεinv]
      exact mul_le_mul_of_nonneg_left hy hε.le
    nlinarith [hle, hε, hy0]

/-- T10b: saturation of the lambda-family member 1 - (1 - p)^2 with
    p = lam y/(1 + lam y) for lam > 0: cleared form 1 < eps (1 + lam y)^2
    for y large (M = 2/(lam sqrt eps) -- M must depend on lam because the
    family saturates at rate 1/(lam y)^2).  Saturation at one holds for
    EVERY lam > 0; the slope at the origin is 2 lam (T4) - so saturation
    does not discriminate the slope (premise A3 is genuinely load-bearing). -/
theorem sat_lambda_family_cleared : ∀ lam : ℝ, lam > 0 →
    ∀ ε : ℝ, ε > 0 → ∃ M ≥ 0, ∀ y ≥ M, 1 < ε * (1 + lam * y) ^ 2 := by
  intro lam hlam ε hε
  refine ⟨2 / (lam * Real.sqrt ε), ?M0, ?ball⟩
  · have hs0 : 0 < Real.sqrt ε := Real.sqrt_pos.2 hε
    exact le_of_lt (div_pos (by norm_num) (mul_pos hlam hs0))
  · intro y hy
    have hlam0 : lam ≠ 0 := ne_of_gt hlam
    have hε0 : ε ≠ 0 := ne_of_gt hε
    have hs0 : 0 < Real.sqrt ε := Real.sqrt_pos.2 hε
    have hden0 : lam * Real.sqrt ε ≠ 0 := mul_ne_zero hlam0 (ne_of_gt hs0)
    have hMpos : 0 < 2 / (lam * Real.sqrt ε) := div_pos (by norm_num) (mul_pos hlam hs0)
    have hy0 : 0 < y := lt_of_lt_of_le hMpos hy
    have hm : lam * (2 / (lam * Real.sqrt ε)) ≤ lam * y :=
      mul_le_mul_of_nonneg_left hy hlam.le
    have hred : lam * (2 / (lam * Real.sqrt ε)) = 2 / Real.sqrt ε := by
      field_simp [hlam0, hden0]
    have hly : 2 / Real.sqrt ε ≤ lam * y := by
      rw [← hred]
      exact hm
    have h2s : 0 < 2 / Real.sqrt ε := div_pos (by norm_num) hs0
    have hbig : 1 / Real.sqrt ε < 1 + lam * y := by
      have h1 : 1 / Real.sqrt ε < 1 + 2 / Real.sqrt ε := by
        apply sub_pos.mp
        have : 1 + 2 / Real.sqrt ε - 1 / Real.sqrt ε = 1 + 1 / Real.sqrt ε := by ring
        rw [this]
        positivity
      nlinarith [h1, hly]
    have hpos1 : 0 < 1 / Real.sqrt ε := div_pos (by norm_num) hs0
    have hpos2 : 0 < 1 + lam * y := by nlinarith [hly, h2s]
    have habs : |1 / Real.sqrt ε| < |1 + lam * y| := by
      rw [abs_of_pos hpos1, abs_of_pos hpos2]
      exact hbig
    have hsq : (1 / Real.sqrt ε) ^ 2 < (1 + lam * y) ^ 2 := sq_lt_sq.mpr habs
    have hsqrt : (Real.sqrt ε) ^ 2 = ε := Real.sq_sqrt hε.le
    have hεsq : ε * (1 / Real.sqrt ε) ^ 2 = 1 := by
      have hs2 : (Real.sqrt ε) ^ 2 = ε := Real.sq_sqrt hε.le
      rw [div_pow, hs2]
      norm_num
      field_simp [hε0]
    have hmul : ε * (1 / Real.sqrt ε) ^ 2 < ε * (1 + lam * y) ^ 2 :=
      mul_lt_mul_of_pos_left hsq hε
    rwa [hεsq] at hmul

end

#print axioms or_slope_jet_expansion
#print axioms or_unequal_jet_expansion
#print axioms or_slope_deriv
#print axioms lambda_family_slope_deriv
#print axioms or_chain_rule_unequal
#print axioms p_lam_value_zero
#print axioms p_lam_has_deriv
#print axioms l230_truncated_matching
#print axioms l230_matching_two
#print axioms kappa_half
#print axioms sat_or_cleared
#print axioms sat_lambda_family_cleared
