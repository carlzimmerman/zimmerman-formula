/-
AS029 — MU2 implicit force cubic: exact algebraic certificate.
Task: deepseek_push/astra_spawn_ideas/AS029_mu2_implicit_force_cubic.md
Branch: MU2 (comparison branch; operative target is filtered nu_mono with causality
criterion B — never identified). Dimensionless form: x = g/a0 > 0, y = B/a0 > 0,
mu2(x) = 1 - (1 + x/2)^(-2), implicit response y = x * mu2(x).

Certified here (all algebraic, no transcendental machinery):
  1. mu2(x) = 1 - 4/(x+2)^2 on x ≠ -2, hence x*mu2(x) = x^2(x+4)/(x+2)^2 =: yFwd x.
  2. The implicit equation y = x*mu2(x) is exactly equivalent to the cubic
     P_y(x) = x^3 + (4-y)x^2 - 4yx - 4y = 0 on x > 0, y > 0.
  3. Full root structure of P_y for every y > 0:
       * exactly three distinct real roots (roots.card = 3);
       * exactly one positive root, in the explicit bracket (y, y+4);
       * the two negative roots lie in (-(y+4), -2) and (-2, 0).
     (existence: intermediate-value theorem; uniqueness and no-other-roots:
     sign bounds P < 0 on (0,y], P > 0 on [y+4,∞), strict increase on [y,y+4],
     and the degree-3 bound via Polynomial.card_roots)
  4. Discriminant identity and sign: cubicDiscriminant 1 (4-y) (-4y) (-4y)
       = 16 y (2 y^2 + 13 y + 64) > 0 for y > 0.
  5. mu2: 0 < mu2(x) < 1 and strictly increasing on x > 0; yFwd strictly increasing
     on x > 0 (so B ↦ g is strictly increasing; surjectivity onto (0,∞) is carried
     in the Python lane).

Hard bar: zero `sorry`; axioms subseteq {propext, Classical.choice, Quot.sound}.
-/
import Mathlib
import Mathlib.Data.Real.Basic

open Polynomial
noncomputable section

/-- MU2 kernel: mu2(x) = 1 - (1 + x/2)^(-2). -/
def mu2 (x : ℝ) : ℝ := 1 - (1 + x / 2) ^ (-2 : ℤ)

/-- Forward map: y = x*mu2(x) in exact rational form (for x ≠ -2). -/
def yFwd (x : ℝ) : ℝ := x^2 * (x + 4) / (x + 2)^2

/-- The cleared cubic P_y(x) = x^3 + (4-y)x^2 - 4yx - 4y (as a plain function). -/
def Pyl (y x : ℝ) : ℝ := x^3 + (4 - y) * x^2 - 4 * y * x - 4 * y

/-- P_y as a polynomial (for the exact root count). -/
def Ppoly (y : ℝ) : Polynomial ℝ := X^3 + C (4 - y) * X^2 - C (4 * y) * X - C (4 * y)

/-- The difference bracket in P_y(x2) - P_y(x1) = (x2-x1)*Q (positive on y < x1 < x2). -/
def Qbr (y x1 x2 : ℝ) : ℝ := x1^2 + x1 * x2 + x2^2 + (4 - y) * (x1 + x2) - 4 * y

/-- Standard discriminant of the cubic a x^3 + b x^2 + c x + d. -/
def cubicDiscriminant (a b c d : ℝ) : ℝ :=
  b^2 * c^2 - 4 * a * c^3 - 4 * b^3 * d - 27 * a^2 * d^2 + 18 * a * b * c * d

/-! ## 1. Rational form of mu2 -/

lemma two_pow_neg_two {x : ℝ} (hx2 : x + 2 ≠ 0) :
    (1 + x / 2) ^ (-2 : ℤ) = 4 / (x + 2)^2 := by
  have hz : (1 + x / 2 : ℝ) ^ (-2 : ℤ) = ((1 + x / 2 : ℝ) ^ (2 : ℤ))⁻¹ := by
    simpa using (zpow_neg (a := (1 + x / 2 : ℝ)) (n := (2 : ℤ)))
  rw [hz]
  have hz2 : (1 + x / 2 : ℝ) ^ (2 : ℤ) = (1 + x / 2 : ℝ)^2 := by norm_num
  rw [hz2, inv_eq_one_div]
  have hs : (1 + x / 2 : ℝ)^2 = (x + 2)^2 / 4 := by ring
  rw [hs]
  field_simp [hx2]

lemma mu2_eq_rational {x : ℝ} (hx2 : x + 2 ≠ 0) : mu2 x = 1 - 4 / (x + 2)^2 := by
  unfold mu2
  rw [two_pow_neg_two hx2]

lemma forward_eq {x : ℝ} (hx2 : x + 2 ≠ 0) : x * mu2 x = yFwd x := by
  unfold yFwd mu2
  rw [two_pow_neg_two hx2]
  field_simp [hx2]
  ring

/-! ## 2. Equivalence of the implicit relation and the cubic -/

lemma Pyl_eq_x2x4 (y x : ℝ) : Pyl y x = x^2 * (x + 4) - y * (x + 2)^2 := by
  unfold Pyl
  ring

theorem cubic_iff_forward {x y : ℝ} (hx2 : x + 2 ≠ 0) :
    Pyl y x = 0 ↔ y = yFwd x := by
  have hsq : (x + 2)^2 ≠ 0 := pow_ne_zero 2 hx2
  have hid : Pyl y x = x^2 * (x + 4) - y * (x + 2)^2 := Pyl_eq_x2x4 y x
  unfold yFwd
  constructor
  · intro hp
    have hA : x^2 * (x + 4) - y * (x + 2)^2 = 0 := by
      nlinarith [hid, hp]
    have hB : y * (x + 2)^2 = x^2 * (x + 4) := by nlinarith
    rw [← hB]
    field_simp [hsq]
  · intro hye
    have hB : y * (x + 2)^2 = x^2 * (x + 4) := by
      rw [hye]
      field_simp [hsq]
    nlinarith [hid, hB]

theorem implicit_eq_cubic {x y : ℝ} (hx : 0 < x) (_hy : 0 < y) :
    (y = x * mu2 x) ↔ Pyl y x = 0 := by
  have hx2 : x + 2 ≠ 0 := by linarith
  rw [forward_eq hx2]
  exact (cubic_iff_forward (x := x) (y := y) hx2).symm

/-! ## 3. Root structure of the cubic -/

/- values at the bracketing points -/
lemma Pyl_y (y : ℝ) : Pyl y y = -4 * y := by unfold Pyl; ring
lemma Pyl_y4 (y : ℝ) : Pyl y (y + 4) = 4 * y^2 + 44 * y + 128 := by unfold Pyl; ring
lemma Pyl_neg2 (y : ℝ) : Pyl y (-2) = 8 := by unfold Pyl; ring
lemma Pyl_zero (y : ℝ) : Pyl y 0 = -4 * y := by unfold Pyl; ring
lemma Pyl_neg_y4 (y : ℝ) : Pyl y (-(y + 4)) = -2 * y * (y^2 + 6 * y + 10) := by unfold Pyl; ring

lemma Pyl_eq_eval (y x : ℝ) : Pyl y x = eval x (Ppoly y) := by
  unfold Pyl Ppoly
  simp [eval_add, eval_sub, eval_mul, eval_pow, eval_C, eval_X]

lemma Ppoly_coeff3 (y : ℝ) : (Ppoly y).coeff 3 = 1 := by
  unfold Ppoly
  rw [coeff_sub, coeff_sub, coeff_add]
  rw [coeff_mul_X_pow (p := C (4 - y)) (n := 2) (d := 1)]
  rw [coeff_mul_X (p := C (4 * y)) (n := 2)]
  simp

lemma Ppoly_ne_zero (y : ℝ) : Ppoly y ≠ 0 := by
  intro h
  have hc := congrArg (fun p : Polynomial ℝ => p.coeff 3) h
  rw [Ppoly_coeff3] at hc
  norm_num at hc

lemma Ppoly_degree_le (y : ℝ) : (Ppoly y).degree ≤ (3 : WithBot ℕ) := by
  have hd1 : ((X : Polynomial ℝ)^3).degree ≤ (3 : WithBot ℕ) := by simp
  have hd2a : (C (4 - y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 - y = 0
    · simp [h]
    · rw [degree_C h]
  have hd2b : ((X : Polynomial ℝ)^2).degree = (2 : WithBot ℕ) := by simp
  have hd2 : (C (4 - y) * X^2).degree ≤ (2 : WithBot ℕ) := by
    exact le_trans (degree_mul_le (C (4 - y)) (X^2)) (by
      rw [hd2b]
      exact add_le_add hd2a le_rfl)
  have hd3a : (C (4 * y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 * y = 0
    · simp [h]
    · rw [degree_C h]
  have hd3b : (X : Polynomial ℝ).degree = (1 : WithBot ℕ) := by simp
  have hd3 : (C (4 * y) * X).degree ≤ (1 : WithBot ℕ) := by
    exact le_trans (degree_mul_le (C (4 * y)) X) (by
      rw [hd3b]
      exact add_le_add hd3a le_rfl)
  have hd4 : (C (4 * y)).degree ≤ (0 : WithBot ℕ) := by
    by_cases h : 4 * y = 0
    · simp [h]
    · rw [degree_C h]
  have hnegC : degree (-(C (4 * y) * X)) ≤ (1 : WithBot ℕ) := by
    rw [degree_neg]
    exact hd3
  have ht1 : (X^3 + C (4 - y) * X^2).degree ≤ (3 : WithBot ℕ) := by
    exact le_trans (degree_add_le (X^3) (C (4 - y) * X^2))
      (max_le_iff.mpr ⟨hd1, le_trans hd2 (by norm_num)⟩)
  have ht2 : (X^3 + C (4 - y) * X^2 - C (4 * y) * X).degree ≤ (3 : WithBot ℕ) := by
    exact le_trans (degree_add_le (X^3 + C (4 - y) * X^2) (-(C (4 * y) * X)))
      (max_le_iff.mpr ⟨ht1, le_trans hnegC (by norm_num)⟩)
  have hnegD : degree (-(C (4 * y))) ≤ (0 : WithBot ℕ) := by
    rw [degree_neg]
    exact hd4
  unfold Ppoly
  exact le_trans (degree_add_le (X^3 + C (4 - y) * X^2 - C (4 * y) * X) (-(C (4 * y))))
    (max_le_iff.mpr ⟨ht2, le_trans hnegD (by norm_num)⟩)

/- sign bounds: P < 0 on (0, y], P > 0 on [y+4, infinity) -/
lemma Pyl_lt_zero_low {x y : ℝ} (hy : 0 < y) (hx : 0 < x) (hxy : x ≤ y) : Pyl y x < 0 := by
  have hf : Pyl y x = x * (x + 4) * (x - y) - 4 * y := by unfold Pyl; ring
  have hxy' : x - y ≤ 0 := by linarith
  have hA : 0 ≤ x * (x + 4) := by positivity
  have hB : x * (x + 4) * (x - y) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hA hxy'
  nlinarith

lemma Pyl_pos_high {x y : ℝ} (hy : 0 < y) (hxy : y + 4 ≤ x) : 0 < Pyl y x := by
  have hx : 0 < x := by nlinarith
  have hf : Pyl y x = x * (x + 4) * (x - y) - 4 * y := by unfold Pyl; ring
  have hx4 : 4 ≤ x - y := by linarith
  have hA : 0 ≤ x * (x + 4) := by positivity
  have hB : 4 * x * (x + 4) ≤ x * (x + 4) * (x - y) := by
    calc 4 * x * (x + 4) = x * (x + 4) * 4 := by ring
      _ ≤ x * (x + 4) * (x - y) := mul_le_mul_of_nonneg_left hx4 hA
  have hC : 0 < 4 * x^2 + 12 * x + 16 := by positivity
  nlinarith

/- the difference bracket Q is positive when both arguments sit above y -/
lemma Qbr_pos {y x1 x2 : ℝ} (hy : 0 < y) (hx1 : y < x1) (hx2 : y < x2)
    (hx1' : 0 < x1) (hx2' : 0 < x2) : 0 < Qbr y x1 x2 := by
  have h1 : 0 < x1 * (x1 - y) := mul_pos hx1' (sub_pos.mpr hx1)
  have h2 : 0 < x2 * (x2 - y) := mul_pos hx2' (sub_pos.mpr hx2)
  have h3 : 0 < x1 * x2 := mul_pos hx1' hx2'
  have h4 : 0 < 4 * (x1 + x2) - 4 * y := by nlinarith
  unfold Qbr
  nlinarith

lemma Pyl_sub (y x1 x2 : ℝ) : Pyl y x2 - Pyl y x1 = (x2 - x1) * Qbr y x1 x2 := by
  unfold Pyl Qbr
  ring

/- existence in the bracket (y, y+4) by IVT -/
lemma exists_root_bracket {y : ℝ} (hy : 0 < y) : ∃ x, y < x ∧ x < y + 4 ∧ Pyl y x = 0 := by
  have hcont : Continuous (fun t : ℝ => Pyl y t) := by
    unfold Pyl
    fun_prop
  have hlow : Pyl y y < 0 := by rw [Pyl_y]; nlinarith
  have hhigh : 0 < Pyl y (y + 4) := by rw [Pyl_y4]; nlinarith
  have himg : Set.Icc (Pyl y y) (Pyl y (y + 4)) ⊆
      (fun t : ℝ => Pyl y t) '' Set.Icc y (y + 4) := by
    exact intermediate_value_Icc (by linarith) hcont.continuousOn
  have hmem : (0 : ℝ) ∈ Set.Icc (Pyl y y) (Pyl y (y + 4)) := by
    exact Set.mem_Icc.mpr ⟨le_of_lt hlow, le_of_lt hhigh⟩
  rcases himg hmem with ⟨x, hxmem, hx0⟩
  have hxne : x ≠ y := by
    intro h
    have : Pyl y y = 0 := by simpa [h] using hx0
    rw [Pyl_y] at this
    nlinarith
  have hxne4 : x ≠ y + 4 := by
    intro h
    have : Pyl y (y + 4) = 0 := by simpa [h] using hx0
    rw [Pyl_y4] at this
    nlinarith [sq_nonneg y]
  exact ⟨x, lt_of_le_of_ne hxmem.1 (Ne.symm hxne), lt_of_le_of_ne hxmem.2 hxne4, hx0⟩

/- uniqueness in the bracket -/
lemma unique_root_bracket {y : ℝ} (hy : 0 < y) :
    ∃! x, y < x ∧ x < y + 4 ∧ Pyl y x = 0 := by
  rcases exists_root_bracket hy with ⟨x0, hx0lo, hx0hi, hP0⟩
  refine ⟨x0, ⟨hx0lo, hx0hi, hP0⟩, ?_⟩
  intro x1 hx1
  by_contra hne
  have hlt : x1 < x0 ∨ x0 < x1 := lt_or_gt_of_ne hne
  rcases hlt with hlt | hgt
  · have hQ : 0 < Qbr y x1 x0 :=
      Qbr_pos hy hx1.1 hx0lo (by linarith [hy, hx1.1]) (by linarith [hy, hx0lo])
    have hd : Pyl y x0 - Pyl y x1 = (x0 - x1) * Qbr y x1 x0 := Pyl_sub y x1 x0
    have hdpos : 0 < Pyl y x0 - Pyl y x1 := by
      rw [hd]
      exact mul_pos (sub_pos.mpr hlt) hQ
    have hd0 : Pyl y x0 - Pyl y x1 = 0 := by rw [hP0, hx1.2.2]; ring
    linarith
  · have hQ : 0 < Qbr y x0 x1 :=
      Qbr_pos hy hx0lo hx1.1 (by linarith [hy, hx0lo]) (by linarith [hy, hx1.1])
    have hd : Pyl y x1 - Pyl y x0 = (x1 - x0) * Qbr y x0 x1 := Pyl_sub y x0 x1
    have hdpos : 0 < Pyl y x1 - Pyl y x0 := by
      rw [hd]
      exact mul_pos (sub_pos.mpr hgt) hQ
    have hd0 : Pyl y x1 - Pyl y x0 = 0 := by rw [hx1.2.2, hP0]; ring
    linarith

/- no positive root outside the bracket -/
lemma pos_root_in_bracket {x y : ℝ} (hy : 0 < y) (hx : 0 < x) (hP : Pyl y x = 0) :
    y < x ∧ x < y + 4 := by
  by_cases h1 : x ≤ y
  · have : Pyl y x < 0 := Pyl_lt_zero_low hy hx h1
    linarith
  · have hxgt : y < x := lt_of_not_ge h1
    by_cases h2 : y + 4 ≤ x
    · have : 0 < Pyl y x := Pyl_pos_high hy h2
      linarith
    · exact ⟨hxgt, lt_of_not_ge h2⟩

/- two negative roots, in explicit intervals, by IVT -/
lemma two_neg_roots {y : ℝ} (hy : 0 < y) :
    ∃ r1 r2 : ℝ, -(y + 4) < r1 ∧ r1 < r2 ∧ r2 < 0 ∧ Pyl y r1 = 0 ∧ Pyl y r2 = 0 := by
  have hcont : Continuous (fun t : ℝ => Pyl y t) := by
    unfold Pyl
    fun_prop
  have hA1 : Pyl y (-(y + 4)) < 0 := by rw [Pyl_neg_y4]; nlinarith [sq_nonneg y, hy]
  have hA2 : 0 < Pyl y (-2) := by rw [Pyl_neg2]; norm_num
  have hB2 : Pyl y 0 < 0 := by rw [Pyl_zero]; nlinarith
  -- interval A: [-(y+4), -2]
  have himgA : Set.uIcc (Pyl y (-(y + 4))) (Pyl y (-2)) ⊆
      (fun t : ℝ => Pyl y t) '' Set.uIcc (-(y + 4)) (-2) := by
    exact intermediate_value_uIcc hcont.continuousOn
  have hmemA : (0 : ℝ) ∈ Set.uIcc (Pyl y (-(y + 4))) (Pyl y (-2)) := by
    exact Set.mem_uIcc.mpr (Or.inl ⟨le_of_lt hA1, le_of_lt hA2⟩)
  rcases himgA hmemA with ⟨r1, hr1mem, hP1⟩
  -- interval B: [-2, 0]
  have himgB : Set.uIcc (Pyl y (-2)) (Pyl y 0) ⊆
      (fun t : ℝ => Pyl y t) '' Set.uIcc (-2) 0 := by
    exact intermediate_value_uIcc hcont.continuousOn
  have hmemB : (0 : ℝ) ∈ Set.uIcc (Pyl y (-2)) (Pyl y 0) := by
    exact Set.mem_uIcc.mpr (Or.inr ⟨le_of_lt hB2, le_of_lt hA2⟩)
  rcases himgB hmemB with ⟨r2, hr2mem, hP2⟩
  -- the interval inequalities (uIcc membership is a disjunction; the other branch is false)
  have hr1I : -(y + 4) ≤ r1 ∧ r1 ≤ -2 := by
    rcases (Set.mem_uIcc.mp hr1mem) with h | h
    · exact h
    · exfalso; linarith
  have hr2I : -2 ≤ r2 ∧ r2 ≤ 0 := by
    rcases (Set.mem_uIcc.mp hr2mem) with h | h
    · exact h
    · exfalso; linarith
  -- strict interior of the intervals
  have hA1' : -(y + 4) < r1 := by
    have hrs : r1 ≠ -(y + 4) := by
      intro h
      have : Pyl y (-(y + 4)) = 0 := by simpa [h] using hP1
      rw [Pyl_neg_y4] at this
      nlinarith [sq_nonneg y, hy]
    exact lt_of_le_of_ne hr1I.1 (Ne.symm hrs)
  have hr1lt : r1 < -2 := by
    have hrs : r1 ≠ -2 := by
      intro h
      have : Pyl y (-2) = 0 := by simpa [h] using hP1
      rw [Pyl_neg2] at this
      norm_num at this
    exact lt_of_le_of_ne hr1I.2 hrs
  have hneg2lt : -2 < r2 := by
    have hrs : r2 ≠ -2 := by
      intro h
      have : Pyl y (-2) = 0 := by simpa [h] using hP2
      rw [Pyl_neg2] at this
      norm_num at this
    exact lt_of_le_of_ne hr2I.1 (Ne.symm hrs)
  have hr2lt : r2 < 0 := by
    have hrs : r2 ≠ 0 := by
      intro h
      have : Pyl y 0 = 0 := by simpa [h] using hP2
      rw [Pyl_zero] at this
      nlinarith
    exact lt_of_le_of_ne hr2I.2 hrs
  exact ⟨r1, r2, hA1', lt_trans hr1lt hneg2lt, hr2lt, hP1, hP2⟩

/- exactly three distinct real roots: three found, degree bound gives the count -/
theorem roots_card_eq_three {y : ℝ} (hy : 0 < y) : (Ppoly y).roots.card = 3 := by
  have hp0 : Ppoly y ≠ 0 := Ppoly_ne_zero y
  rcases exists_root_bracket hy with ⟨rp, hrplo, hrphi, hPp⟩
  rcases two_neg_roots hy with ⟨r1, r2, hr1lo, hr1r2, hr2hi, hP1, hP2⟩
  have hmemrp : rp ∈ (Ppoly y).roots := by
    rw [Polynomial.mem_roots hp0, Polynomial.IsRoot.def]
    rw [← Pyl_eq_eval]
    exact hPp
  have hmem1 : r1 ∈ (Ppoly y).roots := by
    rw [Polynomial.mem_roots hp0, Polynomial.IsRoot.def]
    rw [← Pyl_eq_eval]
    exact hP1
  have hmem2 : r2 ∈ (Ppoly y).roots := by
    rw [Polynomial.mem_roots hp0, Polynomial.IsRoot.def]
    rw [← Pyl_eq_eval]
    exact hP2
  have hr1ne2 : r1 ≠ r2 := ne_of_lt hr1r2
  have hr1nerp : r1 ≠ rp := by
    intro h; linarith [hr2hi, hr1r2, hrplo]
  have hr2nerp : r2 ≠ rp := by
    intro h; linarith [hr2hi, hrplo]
  rcases Multiset.exists_cons_of_mem hmem1 with ⟨t1, ht1⟩
  have hmem2' : r2 ∈ t1 := by
    have h := hmem2
    rw [ht1] at h
    exact (Multiset.mem_cons.mp h).elim (fun h => by linarith) id
  rcases Multiset.exists_cons_of_mem hmem2' with ⟨t2, ht2⟩
  have hmemrp' : rp ∈ t2 := by
    have h := hmemrp
    rw [ht1, ht2] at h
    exact (Multiset.mem_cons.mp h).elim (fun he => by linarith)
      (fun hin => (Multiset.mem_cons.mp hin).elim (fun he2 => by linarith) id)
  rcases Multiset.exists_cons_of_mem hmemrp' with ⟨t3, ht3⟩
  have hroots : (Ppoly y).roots = r1 ::ₘ r2 ::ₘ rp ::ₘ t3 := by
    rw [ht1, ht2, ht3]
  have hcardge : 3 ≤ (Ppoly y).roots.card := by
    rw [hroots]
    simp [Multiset.card_cons]
  have hcardle : (Ppoly y).roots.card ≤ 3 := by
    have hc := Polynomial.card_roots hp0
    have hc' : ((Ppoly y).roots.card : WithBot ℕ) ≤ (3 : WithBot ℕ) :=
      le_trans hc (Ppoly_degree_le y)
    exact_mod_cast hc'
  omega

/- every real root is one of the three -/
lemma root_iff_three {y : ℝ} (hy : 0 < y) :
    ∃ r₁ r₂ rp : ℝ, r₁ < r₂ ∧ r₂ < 0 ∧ y < rp ∧ rp < y + 4 ∧
      ∀ x : ℝ, Pyl y x = 0 ↔ x = r₁ ∨ x = r₂ ∨ x = rp := by
  rcases exists_root_bracket hy with ⟨rp, hrplo, hrphi, hPp⟩
  rcases two_neg_roots hy with ⟨r1, r2, hr1lo, hr1r2, hr2hi, hP1, hP2⟩
  refine ⟨r1, r2, rp, hr1r2, hr2hi, hrplo, hrphi, ?_⟩
  intro x
  constructor
  · intro hx0
    by_cases hpos : 0 < x
    · have hb := pos_root_in_bracket hy hpos hx0
      have hu := unique_root_bracket hy
      rcases hu with ⟨u, hu1, hu2⟩
      have hxu : x = u := hu2 x ⟨hb.1, hb.2, hx0⟩
      have hru : rp = u := hu2 rp ⟨hrplo, hrphi, hPp⟩
      exact Or.inr (Or.inr (by linarith))
    · have hx0' : x ≤ 0 := le_of_not_gt hpos
      have hnpos : x ≠ 0 := by
        intro h
        rw [h] at hx0
        have : Pyl y 0 = 0 := hx0
        rw [Pyl_zero] at this
        nlinarith
      have hxneg : x < 0 := lt_of_le_of_ne hx0' hnpos
      have hcard : (Ppoly y).roots.card = 3 := roots_card_eq_three hy
      have hmemx : x ∈ (Ppoly y).roots := by
        rw [Polynomial.mem_roots (Ppoly_ne_zero y), Polynomial.IsRoot.def]
        rw [← Pyl_eq_eval]
        exact hx0
      have hmem1 : r1 ∈ (Ppoly y).roots := by
        rw [Polynomial.mem_roots (Ppoly_ne_zero y), Polynomial.IsRoot.def]
        rw [← Pyl_eq_eval]
        exact hP1
      have hmem2 : r2 ∈ (Ppoly y).roots := by
        rw [Polynomial.mem_roots (Ppoly_ne_zero y), Polynomial.IsRoot.def]
        rw [← Pyl_eq_eval]
        exact hP2
      have hmemrp : rp ∈ (Ppoly y).roots := by
        rw [Polynomial.mem_roots (Ppoly_ne_zero y), Polynomial.IsRoot.def]
        rw [← Pyl_eq_eval]
        exact hPp
      rcases Multiset.exists_cons_of_mem hmem1 with ⟨t1, ht1⟩
      have hmem2' : r2 ∈ t1 := by
        have h := hmem2
        rw [ht1] at h
        exact (Multiset.mem_cons.mp h).elim (fun h => by linarith) id
      rcases Multiset.exists_cons_of_mem hmem2' with ⟨t2, ht2⟩
      have hmemrp' : rp ∈ t2 := by
        have h := hmemrp
        rw [ht1, ht2] at h
        exact (Multiset.mem_cons.mp h).elim (fun he => by linarith)
          (fun hin => (Multiset.mem_cons.mp hin).elim (fun he2 => by linarith) id)
      rcases Multiset.exists_cons_of_mem hmemrp' with ⟨t3, ht3⟩
      have hroots : (Ppoly y).roots = r1 ::ₘ r2 ::ₘ rp ::ₘ t3 := by rw [ht1, ht2, ht3]
      have ht3card : t3.card = 0 := by
        have hc : (r1 ::ₘ r2 ::ₘ rp ::ₘ t3).card = 3 := by
          rw [← hroots]
          exact hcard
        have hc' : t3.card + 3 = 3 := by
          simpa [Multiset.card_cons, add_assoc, add_comm, add_left_comm] using hc
        omega
      have ht3eq : t3 = 0 := Multiset.card_eq_zero.mp ht3card
      have hmemx' : x ∈ (r1 ::ₘ r2 ::ₘ rp ::ₘ 0 : Multiset ℝ) := by
        simpa [ht3eq, hroots] using hmemx
      exact (Multiset.mem_cons.mp hmemx').elim (fun h => Or.inl h)
        (fun h1 => (Multiset.mem_cons.mp h1).elim (fun h => Or.inr (Or.inl h))
          (fun h2 => (Multiset.mem_cons.mp h2).elim (fun h => Or.inr (Or.inr h))
            (fun hempty => False.elim (by simpa using hempty))))
  · intro hx3
    rcases hx3 with hx1 | hx2 | hxp
    · simpa [hx1] using hP1
    · simpa [hx2] using hP2
    · simpa [hxp] using hPp

/-! ## 4. Discriminant -/

theorem cubic_discriminant_identity (y : ℝ) :
    cubicDiscriminant 1 (4 - y) (-4 * y) (-4 * y) = 16 * y * (2 * y^2 + 13 * y + 64) := by
  unfold cubicDiscriminant
  ring

theorem cubic_discriminant_pos {y : ℝ} (hy : 0 < y) :
    0 < cubicDiscriminant 1 (4 - y) (-4 * y) (-4 * y) := by
  rw [cubic_discriminant_identity]
  have hq : 0 < 2 * y^2 + 13 * y + 64 := by
    nlinarith [sq_nonneg (y + 13 / 4)]
  nlinarith [hy, hq]

/-! ## 5. mu2 and the forward map -/

theorem mu2_unit {x : ℝ} (hx : 0 < x) : 0 < mu2 x ∧ mu2 x < 1 := by
  have hx2 : x + 2 ≠ 0 := by linarith
  have hsq : 0 < (x + 2)^2 := sq_pos_of_ne_zero hx2
  rw [mu2_eq_rational (x := x) (by linarith)]
  constructor
  · have hq : 4 < (x + 2)^2 := by nlinarith [hx]
    have hd : 4 / (x + 2)^2 < 1 := by
      rw [div_lt_one hsq]
      exact hq
    exact sub_pos.mpr hd
  · have hp : 0 < 4 / (x + 2)^2 := div_pos (by norm_num) hsq
    linarith

theorem mu2_strictMono {x1 x2 : ℝ} (hx1 : 0 < x1) (hx2 : 0 < x2) (h : x1 < x2) :
    mu2 x1 < mu2 x2 := by
  rw [mu2_eq_rational (x := x1) (by linarith), mu2_eq_rational (x := x2) (by linarith)]
  have hs1 : (x1 + 2)^2 ≠ 0 := pow_ne_zero 2 (by linarith)
  have hs2 : (x2 + 2)^2 ≠ 0 := pow_ne_zero 2 (by linarith)
  have hd : 4 / (x2 + 2)^2 < 4 / (x1 + 2)^2 := by
    field_simp [hs1, hs2]
    nlinarith [h]
  linarith

theorem yFwd_strictMono {x1 x2 : ℝ} (hx1 : 0 < x1) (hx2 : 0 < x2) (h : x1 < x2) :
    yFwd x1 < yFwd x2 := by
  have hx2' : x1 + 2 ≠ 0 := by linarith
  have hx2'' : x2 + 2 ≠ 0 := by linarith
  have hM : 0 < x1^2 * x2^2 + 4 * x1^2 * x2 + 4 * x1^2 + 4 * x1 * x2^2 + 20 * x1 * x2
      + 16 * x1 + 4 * x2^2 + 16 * x2 := by
    positivity
  have hdf : yFwd x2 - yFwd x1 =
      (x2 - x1) * (x1^2 * x2^2 + 4 * x1^2 * x2 + 4 * x1^2 + 4 * x1 * x2^2 + 20 * x1 * x2
        + 16 * x1 + 4 * x2^2 + 16 * x2) / ((x1 + 2)^2 * (x2 + 2)^2) := by
    unfold yFwd
    field_simp [hx2', hx2'']
    ring
  have hpos : 0 < yFwd x2 - yFwd x1 := by
    rw [hdf]
    exact div_pos (mul_pos (sub_pos.mpr h) hM)
      (mul_pos (sq_pos_of_ne_zero hx2') (sq_pos_of_ne_zero hx2''))
  linarith

/-! ## 6. The main statement of the MU2 implicit-force cubic -/

/-- For every y > 0 the implicit MU2 response y = x*mu2(x) (x > 0) is exactly
    equivalent to a cubic with three distinct real roots; the physical root is the
    unique positive one and lies in the explicit bracket (y, y+4); the two other
    roots are negative. -/
theorem mu2_implicit_force_cubic {y : ℝ} (hy : 0 < y) :
    ∃ r₁ r₂ rp : ℝ,
      r₁ < r₂ ∧ r₂ < 0 ∧ y < rp ∧ rp < y + 4 ∧
      (∀ x : ℝ, 0 < x → (y = x * mu2 x ↔ x = rp)) ∧
      (∀ x : ℝ, Pyl y x = 0 ↔ x = r₁ ∨ x = r₂ ∨ x = rp) := by
  rcases root_iff_three hy with ⟨r1, r2, rp, hr1r2, hr2hi, hrplo, hrphi, hroot⟩
  refine ⟨r1, r2, rp, hr1r2, hr2hi, hrplo, hrphi, ?_, hroot⟩
  intro x hx
  rw [implicit_eq_cubic hx hy]
  constructor
  · intro hP
    have hb := pos_root_in_bracket hy hx hP
    have hx3 := (hroot x).1 hP
    rcases hx3 with hx1 | hx2 | hxp
    · exfalso; linarith [hr2hi, hr1r2, hb.1]
    · exfalso; linarith [hr2hi, hb.1]
    · exact hxp
  · intro hxpeq
    have hPr : Pyl y rp = 0 := (hroot rp).2 (Or.inr (Or.inr rfl))
    simpa [hxpeq] using hPr

#print axioms mu2_implicit_force_cubic
#print axioms implicit_eq_cubic
#print axioms cubic_iff_forward
#print axioms roots_card_eq_three
#print axioms root_iff_three
#print axioms cubic_discriminant_identity
#print axioms cubic_discriminant_pos
#print axioms mu2_unit
#print axioms mu2_strictMono
#print axioms yFwd_strictMono
#print axioms exists_root_bracket
#print axioms unique_root_bracket
#print axioms two_neg_roots
#print axioms pos_root_in_bracket
