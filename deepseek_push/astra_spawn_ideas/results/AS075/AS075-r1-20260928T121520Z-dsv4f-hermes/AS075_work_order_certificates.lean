/-
AS075 -- Constructive missing-premise work order for kappa: Lean certificates
of the algebraic core of the two-obligation theorem and its negative controls.

Statements (all in R, self-contained, house build):
  * A1r  removal_deriv_identity  -- the boundary-fixing algebra: d/dlam[-lam^2/(1+lam)]
                                   equals -mu_2(lam) (the FTC form of J(0) = -lam^2/(1+lam));
  * B-r  boundary_family_kappa_free  -- the obligation-B-only system {kappa = 1/b,
                                   j = -lam^2/(1+lam)} realises EVERY kappa > 0
                                   (kappa is not selected by the boundary family);
  * B-r2 obligB_alone_not_half    -- a concrete witness (b = 1, lam = 1) with kappa = 1
                                   != 1/2: obligation B alone does not derive one half;
  * A-r  obligA_alone_j_free      -- at fixed b = 2 (kappa = 1/2), two distinct negative
                                   vacuum data are realisable (lam = 1/2, 1): the vacuum
                                   datum is not selected by obligation A alone;
  * C-r  relabel_* -- the re-labelled input "rho_vac = rho_Lambda" (j = a kappa^2,
                                   a > 0) is a bijection kappa -> (0, inf): strictly
                                   monotone, injective, surjective onto (0, inf);
                                   relabel_selects_nothing: every kappa has a datum;
                                   relabel_diagnostics_distinct: the diagnostic data at
                                   kappa = 1/2, 1, 2 are pairwise distinct;
  * S-r  slope_family_diagnostics -- the obligation-A counterexample family
                                   kappa(lam) = 1/(2 lam) at lam in {1/2, 1, 2} gives
                                   kappa in {1, 1/2, 1/4}, pairwise distinct;
  * D-r  boundary_j_neg + diag_vacua_distinct -- boundary-fixed vacuum data are
                                   negative and pairwise distinct at lam in {1/2, 1, 2};
  * F-r  full_system_lands_half -- the joint system's endpoint: kappa = 1/b with b = 2
                                   gives kappa = 1/2 (the sufficiency half).
-/
import Mathlib

noncomputable section

open Real

/-- The boundary-fixed vacuum datum: j(lam) = -lam^2/(1+lam) in dimensionless s-units
(J = kinetic primitive with J' = mu_2, reference J(lam) = 0). -/
def jBoundary (lam : ℝ) : ℝ := -lam ^ 2 / (1 + lam)

/-- The re-labelled candidate relation: j = a kappa^2 with a = 64 pi / alpha > 0 (c = 1). -/
def jRel (a kappa : ℝ) : ℝ := a * kappa ^ 2

/-- The obligation-A counterexample family: kappa(lam) = 1/(2 lam). -/
def kappaSlope (lam : ℝ) : ℝ := 1 / (2 * lam)

/-- FTC identity behind the boundary fixing: the derivative of -lam^2/(1+lam) is -mu_2(lam),
mu_2(Y) = 1 - 1/(1+Y)^2, for every lam > 0 (exact, no finite-precision content). -/
theorem removal_deriv_identity (lam : ℝ) (hlam : 0 < lam) :
    -((2 * lam * (1 + lam) - lam ^ 2) / (1 + lam) ^ 2) = -(1 - 1 / (1 + lam) ^ 2) := by
  have hd : (1 + lam) ^ 2 ≠ 0 := pow_ne_zero 2 (by nlinarith [hlam])
  field_simp [hd] <;> ring

/-- Obligation B alone (boundary family) realises every positive kappa: for every kappa_0 > 0
there is (b, lam) > 0 such that the system {kappa0 = 1/b, j = jBoundary lam} holds. -/
theorem boundary_family_kappa_free : ∀ k0 : ℝ, 0 < k0 →
    ∃ b lam : ℝ, 0 < b ∧ 0 < lam ∧ k0 = 1 / b ∧ jBoundary lam = jBoundary 1 := by
  intro k0 hk0
  refine ⟨1 / k0, 1, ?_, ?_, ?_, ?_⟩
  · exact div_pos zero_lt_one hk0
  · norm_num
  · field_simp [ne_of_gt hk0] <;> ring
  · rfl

/-- Obligation B alone does NOT force kappa = 1/2: witness b = 1, lam = 1 gives kappa = 1. -/
theorem obligB_alone_not_half :
    ∃ b lam : ℝ, 0 < b ∧ 0 < lam ∧ 1 / b ≠ 1 / 2 ∧ jBoundary lam = jBoundary 1 := by
  refine ⟨1, 1, ?_, ?_, ?_, ?_⟩
  · norm_num
  · norm_num
  · norm_num
  · rfl

/-- Obligation A alone (b = 2, kappa = 1/2) leaves the vacuum datum free:
two distinct negative data are realisable at references lam = 1/2 and lam = 1. -/
theorem obligA_alone_j_free :
    jBoundary (1 / 2 : ℝ) ≠ jBoundary 1 ∧ jBoundary (1 / 2 : ℝ) < 0 ∧ jBoundary 1 < 0 := by
  constructor
  · unfold jBoundary
    norm_num
  · constructor
    · unfold jBoundary
      norm_num
    · unfold jBoundary
      norm_num

/-- Strict monotonicity of the re-labelled relation: 0 < k1 < k2 implies a k1^2 < a k2^2. -/
theorem relabel_strict_mono (a : ℝ) (ha : 0 < a) : ∀ {k1 k2 : ℝ},
    0 < k1 → 0 < k2 → k1 < k2 → a * k1 ^ 2 < a * k2 ^ 2 := by
  intro k1 k2 hk1 hk2 hlt
  have hsum : 0 < k1 + k2 := add_pos hk1 hk2
  have hd : k1 - k2 < 0 := sub_neg.mpr hlt
  have hprod : (k1 - k2) * (k1 + k2) < 0 := mul_neg_of_neg_of_pos hd hsum
  have hsq : k1 ^ 2 < k2 ^ 2 := by nlinarith [hprod]
  exact mul_lt_mul_of_pos_left hsq ha

/-- Injectivity of the re-labelled relation on (0, inf). -/
theorem relabel_injective (a : ℝ) (ha : 0 < a) : ∀ {k1 k2 : ℝ},
    0 < k1 → 0 < k2 → a * k1 ^ 2 = a * k2 ^ 2 → k1 = k2 := by
  intro k1 k2 hk1 hk2 h
  have hsq : k1 ^ 2 = k2 ^ 2 := mul_left_cancel₀ (ne_of_gt ha) h
  rw [sq, sq] at hsq
  have hc := (mul_self_eq_mul_self_iff.mp hsq)
  rcases hc with h1 | h2
  · exact h1
  · linarith [h2, hk1, hk2]

/-- Surjectivity of the re-labelled relation onto (0, inf): every positive datum is attained
by some positive kappa (the constraint surface is a graph over kappa). -/
theorem relabel_surjective (a : ℝ) (ha : 0 < a) : ∀ j : ℝ, 0 < j →
    ∃ kappa : ℝ, 0 < kappa ∧ a * kappa ^ 2 = j := by
  intro j hj
  refine ⟨Real.sqrt (j / a), ?_, ?_⟩
  · exact Real.sqrt_pos.2 (div_pos hj ha)
  · have hja : 0 ≤ j / a := le_of_lt (div_pos hj ha)
    have hm := Real.mul_self_sqrt hja
    rw [sq, hm]
    field_simp [ne_of_gt ha] <;> ring

/-- The re-labelled candidate selects no kappa: every positive kappa admits the datum. -/
theorem relabel_selects_nothing (a : ℝ) (ha : 0 < a) : ∀ k0 : ℝ, 0 < k0 →
    ∃ j : ℝ, 0 < j ∧ jRel a k0 = j := by
  intro k0 hk0
  refine ⟨jRel a k0, ?_, rfl⟩
  unfold jRel
  exact mul_pos ha (sq_pos_of_pos hk0)

/-- The diagnostic data at kappa = 1/2, 1, 2 are pairwise distinct (same relation,
same a > 0): the relation does not identify the data with the target. -/
theorem relabel_diagnostics_distinct (a : ℝ) (ha : 0 < a) :
    jRel a (1 / 2 : ℝ) < jRel a 1 ∧ jRel a 1 < jRel a 2 := by
  have h12 : (1 / 2 : ℝ) < 1 := by norm_num
  have h23 : (1 : ℝ) < 2 := by norm_num
  constructor
  · exact relabel_strict_mono a ha (by norm_num) (by norm_num) h12
  · exact relabel_strict_mono a ha (by norm_num) (by norm_num) h23

/-- The obligation-A counterexample family: kappa(lam) = 1/(2 lam) at
lam in {1/2, 1, 2} takes the values {1, 1/2, 1/4}, pairwise distinct. -/
theorem slope_family_diagnostics :
    kappaSlope (1 / 2 : ℝ) = 1 ∧ kappaSlope 1 = 1 / 2 ∧ kappaSlope 2 = 1 / 4
      ∧ kappaSlope (1 / 2 : ℝ) ≠ kappaSlope 1 ∧ kappaSlope 1 ≠ kappaSlope 2 := by
  constructor
  · unfold kappaSlope
    norm_num
  · constructor
    · unfold kappaSlope
      norm_num
    · constructor
      · unfold kappaSlope
        norm_num
      · constructor
        · unfold kappaSlope
          norm_num
        · unfold kappaSlope
          norm_num

/-- Boundary-fixed vacuum data are negative for every positive reference. -/
theorem boundary_j_neg : ∀ lam : ℝ, 0 < lam → jBoundary lam < 0 := by
  intro lam hlam
  unfold jBoundary
  have hl2 : 0 < lam ^ 2 := sq_pos_of_pos hlam
  have hnum : -lam ^ 2 < 0 := neg_lt_zero.mpr hl2
  have hd : 0 < 1 + lam := by nlinarith [hlam]
  exact div_neg_of_neg_of_pos hnum hd

/-- The diagnostic boundary-fixed vacua at lam in {1/2, 1, 2}: exact values, negative,
pairwise distinct. -/
theorem diag_vacua_distinct :
    jBoundary (1 / 2 : ℝ) = -1 / 6 ∧ jBoundary 1 = -1 / 2 ∧ jBoundary 2 = -4 / 3
      ∧ jBoundary (1 / 2 : ℝ) ≠ jBoundary 1 ∧ jBoundary 1 ≠ jBoundary 2 := by
  constructor
  · unfold jBoundary
    norm_num
  · constructor
    · unfold jBoundary
      norm_num
    · constructor
      · unfold jBoundary
        norm_num
      · constructor
        · unfold jBoundary
          norm_num
        · unfold jBoundary
          norm_num

/-- The joint-system endpoint (sufficiency half of the work order): the matching
kappa = 1/b with the adopted b = 2 lands kappa = 1/2 exactly. -/
theorem full_system_lands_half (b kappa : ℝ) (hm : kappa = 1 / b) (hb : b = 2) :
    kappa = 1 / 2 := by
  rw [hm, hb]

end
