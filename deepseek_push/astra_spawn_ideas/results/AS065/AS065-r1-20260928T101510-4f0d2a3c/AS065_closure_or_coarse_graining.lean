/-
AS065 -- Closure of the OR class under coarse graining: Lean 4 certificate.

Certifies the algebraic core of AS065 (zimmerman-formula, seed AS065,
run AS065-r1-20260928T101510-4f0d2a3c):

  * OR-closure under coarse graining: for any partition n = k*m of equal
    independent channels, 1 - (1 - p_G)^k = 1 - (1-p)^(km) with the group
    engagement p_G = 1 - (1-p)^m.  Pure power associativity (pow_mul).
  * The deep-MOND slope is the total count: for the corpus member
    p(Y) = Y/(1+Y), mu_n(Y) = 1 - (1+Y)^(-n) has slope n at the origin --
    certified as the punctured-filter limit  lim_{Y -> 0, Y != 0} mu_n(Y)/Y
    for the physically relevant counts 1, 2, 3, 4 (deep-MOND slope).
  * NEGATIVE CONTROL (live): the group engagement of two channels has slope
    2 in the vacuum unit, NOT 1 (B2/D1); a hand renormalization to unit
    slope moves the unit to s/2, with the count interpretation changing
    2 -> 1 while the matched kappa ratio stays 1/2.
  * Scale covariance of the count reading: at drive-unit rescaling
    s_lam = lam*s the reading slope is n*lam (certified for lam = 1/2, 2
    at n = 2), the covariant matched ratio a0/s stays 1/2 for every
    nonzero lam, and unit-confused readings give 1/(2*lam).
  * The kappa = 1/m family of grouping renormalizations (any grouping is
    internally consistent; the product identity does not select 1/2).

Punctured-neighborhood convention: the slopes below are limits at the
punctured filter nhdsWithin 0 {t | t != 0} (the Y != 0 hypothesis is where
the difference quotients live; Lean's total functions make the value at
Y = 0 junk, so the punch is required).

Every theorem below is a statement about real numbers and standard limits;
no physical law is claimed to hold of the world by Lean.
-/
import Mathlib

open Set
open scoped Topology

/- ------------------------------------------------------------------ -/
/- OR closure under coarse graining (pure algebra)                    -/
/- ------------------------------------------------------------------ -/

/-- Power associativity: ((1-p)^m)^k = (1-p)^(m*k). -/
theorem AS065_or_closure_pow (m k : ℕ) (x : ℝ) :
    (x ^ m) ^ k = x ^ (m * k) := by
  rw [pow_mul]

/-- Closure: the response of k groups of m channels equals the (k*m)-channel
    response for ANY per-channel survival shape p. -/
theorem AS065_or_closure_response (m k : ℕ) (p : ℝ) :
    1 - (1 - (1 - (1 - p) ^ m)) ^ k = 1 - (1 - p) ^ (m * k) := by
  have hbase : 1 - (1 - (1 - p) ^ m) = (1 - p) ^ m := by ring
  rw [hbase, AS065_or_closure_pow m k (1 - p)]

/-- Corpus member (p = Y/(1+Y)), 2x2 grouping: the composed group response is
    exactly the 4-channel response. -/
theorem AS065_closure_member_two_times_two (Y : ℝ) :
    1 - (1 - (1 - (1 - Y / (1 + Y)) ^ 2)) ^ 2 = 1 - (1 - Y / (1 + Y)) ^ 4 := by
  rw [show (4 : ℕ) = 2 * 2 by norm_num]
  exact AS065_or_closure_response 2 2 (Y / (1 + Y))

/-- Seed boxed identity, unequally: survival products regroup exactly
    (independence only). -/
theorem AS065_survival_grouping (q1 q2 q3 q4 : ℝ) :
    (q1 * q2) * (q3 * q4) = q1 * q2 * q3 * q4 := by
  ring

/- ------------------------------------------------------------------ -/
/- Difference-quotient algebra: the identity on the punctured filter    -/
/- ------------------------------------------------------------------ -/

/-- Membership helper: on a sufficiently small punctured interval, both
    Y != 0 and (1 + Y)^k != 0 hold eventually. -/
private lemma AS065_punctured_basic (k : ℕ) :
    {t : ℝ | t ≠ 0 ∧ (1 + t) ^ k ≠ 0} ∈ nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}) := by
  rw [mem_nhdsWithin]
  refine ⟨Set.Ioo (-(1 / 3 : ℝ)) (1 / 3 : ℝ), isOpen_Ioo, by simp, ?_⟩
  intro Y hY
  rcases hY with ⟨hb, hz⟩
  have hy0 : Y ≠ 0 := by simpa using hz
  simp at hb
  rcases hb with ⟨hlo, hhi⟩
  have h1p : 0 < 1 + Y := by nlinarith
  exact ⟨hy0, pow_ne_zero k (ne_of_gt h1p)⟩

/-- Membership helper at lambda = 1/2: 1 + t/2 != 0 on a punctured interval. -/
private lemma AS065_punctured_half :
    {t : ℝ | t ≠ 0 ∧ 1 + (1 / 2 : ℝ) * t ≠ 0} ∈ nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}) := by
  rw [mem_nhdsWithin]
  refine ⟨Set.Ioo (-(1 / 3 : ℝ)) (1 / 3 : ℝ), isOpen_Ioo, by simp, ?_⟩
  intro Y hY
  rcases hY with ⟨hb, hz⟩
  have hy0 : Y ≠ 0 := by simpa using hz
  simp at hb
  rcases hb with ⟨hlo, hhi⟩
  have h1p : 0 < 1 + (1 / 2 : ℝ) * Y := by nlinarith
  exact ⟨hy0, ne_of_gt h1p⟩

/-- Membership helper at lambda = 2: 1 + 2t != 0 on a punctured interval. -/
private lemma AS065_punctured_two :
    {t : ℝ | t ≠ 0 ∧ 1 + (2 : ℝ) * t ≠ 0} ∈ nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}) := by
  rw [mem_nhdsWithin]
  refine ⟨Set.Ioo (-(1 / 3 : ℝ)) (1 / 3 : ℝ), isOpen_Ioo, by simp, ?_⟩
  intro Y hY
  rcases hY with ⟨hb, hz⟩
  have hy0 : Y ≠ 0 := by simpa using hz
  simp at hb
  rcases hb with ⟨hlo, hhi⟩
  have h1p : 0 < 1 + (2 : ℝ) * Y := by nlinarith
  exact ⟨hy0, ne_of_gt h1p⟩

/-- mu_1(Y)/Y = 1/(1+Y) on the punctured filter (rational on the left for
    Filter.Tendsto.congr' use: the rational is the function whose tendsto we
    construct). -/
private lemma AS065_dq_one :
    ∀ᶠ Y in nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}),
      1 / (1 + Y) = (1 - (1 + Y)⁻¹) / Y := by
  filter_upwards [AS065_punctured_basic 1] with Y hY
  rcases hY with ⟨hy0, hy1z⟩
  have hy1 : 1 + Y ≠ 0 := by simpa using hy1z
  have hm2 : (1 - (1 + Y)⁻¹) * (1 + Y) = Y := by
    rw [sub_mul, one_mul, inv_mul_cancel₀ hy1]
    ring
  have hmain : ((1 - (1 + Y)⁻¹) / Y) * (1 + Y) = 1 := by
    rw [div_mul_eq_mul_div]
    rw [hm2]
    field_simp [hy0]
  have hx : ((1 - (1 + Y)⁻¹) / Y) * (1 + Y) = (1 / (1 + Y)) * (1 + Y) := by
    rw [hmain]
    field_simp [hy1]
  exact (mul_right_cancel₀ hy1 hx).symm

/-- mu_2(Y)/Y = (2 + Y)/(1+Y)^2 on the punctured filter. -/
private lemma AS065_dq_two :
    ∀ᶠ Y in nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}),
      (2 + Y) / (1 + Y) ^ 2 = (1 - ((1 + Y) ^ 2)⁻¹) / Y := by
  filter_upwards [AS065_punctured_basic 2] with Y hY
  rcases hY with ⟨hy0, ha⟩
  have hsq : (1 + Y) ^ 2 - 1 = Y * (2 + Y) := by ring
  have hm2 : (1 - ((1 + Y) ^ 2)⁻¹) * (1 + Y) ^ 2 = Y * (2 + Y) := by
    rw [sub_mul, one_mul, inv_mul_cancel₀ ha, hsq]
  have hmain : ((1 - ((1 + Y) ^ 2)⁻¹) / Y) * (1 + Y) ^ 2 = 2 + Y := by
    rw [div_mul_eq_mul_div]
    rw [hm2]
    field_simp [hy0]
  have hx : ((1 - ((1 + Y) ^ 2)⁻¹) / Y) * (1 + Y) ^ 2 =
      ((2 + Y) / (1 + Y) ^ 2) * (1 + Y) ^ 2 := by
    rw [hmain]
    have hy1 : 1 + Y ≠ 0 := by
      intro h
      apply ha
      rw [h]
      simp
    field_simp [hy1]
  exact (mul_right_cancel₀ ha hx).symm

/-- mu_3(Y)/Y = (3 + 3*Y + Y^2)/(1+Y)^3 on the punctured filter. -/
private lemma AS065_dq_three :
    ∀ᶠ Y in nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}),
      (3 + 3 * Y + Y ^ 2) / (1 + Y) ^ 3 = (1 - ((1 + Y) ^ 3)⁻¹) / Y := by
  filter_upwards [AS065_punctured_basic 3] with Y hY
  rcases hY with ⟨hy0, ha⟩
  have hsq : (1 + Y) ^ 3 - 1 = Y * (3 + 3 * Y + Y ^ 2) := by ring
  have hm2 : (1 - ((1 + Y) ^ 3)⁻¹) * (1 + Y) ^ 3 = Y * (3 + 3 * Y + Y ^ 2) := by
    rw [sub_mul, one_mul, inv_mul_cancel₀ ha, hsq]
  have hmain : ((1 - ((1 + Y) ^ 3)⁻¹) / Y) * (1 + Y) ^ 3 = 3 + 3 * Y + Y ^ 2 := by
    rw [div_mul_eq_mul_div]
    rw [hm2]
    field_simp [hy0]
  have hx : ((1 - ((1 + Y) ^ 3)⁻¹) / Y) * (1 + Y) ^ 3 =
      ((3 + 3 * Y + Y ^ 2) / (1 + Y) ^ 3) * (1 + Y) ^ 3 := by
    rw [hmain]
    have hy1 : 1 + Y ≠ 0 := by
      intro h
      apply ha
      rw [h]
      simp
    field_simp [hy1]
  exact (mul_right_cancel₀ ha hx).symm

/-- mu_4(Y)/Y = (4 + 6*Y + 4*Y^2 + Y^3)/(1+Y)^4 on the punctured filter. -/
private lemma AS065_dq_four :
    ∀ᶠ Y in nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}),
      (4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) / (1 + Y) ^ 4 = (1 - ((1 + Y) ^ 4)⁻¹) / Y := by
  filter_upwards [AS065_punctured_basic 4] with Y hY
  rcases hY with ⟨hy0, ha⟩
  have hsq : (1 + Y) ^ 4 - 1 = Y * (4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) := by ring
  have hm2 : (1 - ((1 + Y) ^ 4)⁻¹) * (1 + Y) ^ 4 = Y * (4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) := by
    rw [sub_mul, one_mul, inv_mul_cancel₀ ha, hsq]
  have hmain : ((1 - ((1 + Y) ^ 4)⁻¹) / Y) * (1 + Y) ^ 4 = 4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3 := by
    rw [div_mul_eq_mul_div]
    rw [hm2]
    field_simp [hy0]
  have hx : ((1 - ((1 + Y) ^ 4)⁻¹) / Y) * (1 + Y) ^ 4 =
      ((4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) / (1 + Y) ^ 4) * (1 + Y) ^ 4 := by
    rw [hmain]
    have hy1 : 1 + Y ≠ 0 := by
      intro h
      apply ha
      rw [h]
      simp
    field_simp [hy1]
  exact (mul_right_cancel₀ ha hx).symm

/-- mu_2(Y)/Y at unit s/2: = (1 + Y/4)/(1 + Y/2)^2 on the punctured filter. -/
private lemma AS065_dq_half :
    ∀ᶠ Y in nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}),
      (1 + (1 / 4 : ℝ) * Y) / (1 + (1 / 2 : ℝ) * Y) ^ 2 = (1 - ((1 + (1 / 2 : ℝ) * Y) ^ 2)⁻¹) / Y := by
  filter_upwards [AS065_punctured_half] with Y hY
  rcases hY with ⟨hy0, hy1z⟩
  have ha : (1 + (1 / 2 : ℝ) * Y) ^ 2 ≠ 0 := pow_ne_zero 2 hy1z
  have hsq : (1 + (1 / 2 : ℝ) * Y) ^ 2 - 1 = Y * (1 + (1 / 4 : ℝ) * Y) := by ring
  have hm2 : (1 - ((1 + (1 / 2 : ℝ) * Y) ^ 2)⁻¹) * (1 + (1 / 2 : ℝ) * Y) ^ 2 =
      Y * (1 + (1 / 4 : ℝ) * Y) := by
    rw [sub_mul, one_mul, inv_mul_cancel₀ ha, hsq]
  have hmain : ((1 - ((1 + (1 / 2 : ℝ) * Y) ^ 2)⁻¹) / Y) * (1 + (1 / 2 : ℝ) * Y) ^ 2 =
      1 + (1 / 4 : ℝ) * Y := by
    rw [div_mul_eq_mul_div]
    rw [hm2]
    field_simp [hy0]
  have hx : ((1 - ((1 + (1 / 2 : ℝ) * Y) ^ 2)⁻¹) / Y) * (1 + (1 / 2 : ℝ) * Y) ^ 2 =
      ((1 + (1 / 4 : ℝ) * Y) / (1 + (1 / 2 : ℝ) * Y) ^ 2) * (1 + (1 / 2 : ℝ) * Y) ^ 2 := by
    rw [hmain]
    have h2 : 2 + Y ≠ 0 := by
      intro h
      apply hy1z
      nlinarith
    field_simp [h2]
  exact (mul_right_cancel₀ ha hx).symm

/-- mu_2(Y)/Y at unit 2s: = (4 + 4*Y)/(1 + 2Y)^2 on the punctured filter. -/
private lemma AS065_dq_two_lam :
    ∀ᶠ Y in nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0}),
      (4 + 4 * Y) / (1 + (2 : ℝ) * Y) ^ 2 = (1 - ((1 + (2 : ℝ) * Y) ^ 2)⁻¹) / Y := by
  filter_upwards [AS065_punctured_two] with Y hY
  rcases hY with ⟨hy0, hy1z⟩
  have ha : (1 + (2 : ℝ) * Y) ^ 2 ≠ 0 := pow_ne_zero 2 hy1z
  have hsq : (1 + (2 : ℝ) * Y) ^ 2 - 1 = Y * (4 + 4 * Y) := by ring
  have hm2 : (1 - ((1 + (2 : ℝ) * Y) ^ 2)⁻¹) * (1 + (2 : ℝ) * Y) ^ 2 = Y * (4 + 4 * Y) := by
    rw [sub_mul, one_mul, inv_mul_cancel₀ ha, hsq]
  have hmain : ((1 - ((1 + (2 : ℝ) * Y) ^ 2)⁻¹) / Y) * (1 + (2 : ℝ) * Y) ^ 2 = 4 + 4 * Y := by
    rw [div_mul_eq_mul_div]
    rw [hm2]
    field_simp [hy0]
  have hx : ((1 - ((1 + (2 : ℝ) * Y) ^ 2)⁻¹) / Y) * (1 + (2 : ℝ) * Y) ^ 2 =
      ((4 + 4 * Y) / (1 + (2 : ℝ) * Y) ^ 2) * (1 + (2 : ℝ) * Y) ^ 2 := by
    rw [hmain]
    have h21 : 1 + Y * 2 ≠ 0 := by
      intro h
      apply hy1z
      nlinarith
    field_simp [h21]
  exact (mul_right_cancel₀ ha hx).symm

/- ------------------------------------------------------------------ -/
/- Continuity of the rational representatives at 0                     -/
/- ------------------------------------------------------------------ -/

private lemma AS065_cont_shift : ContinuousAt (fun Y : ℝ => 1 + Y) 0 := by
  exact ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (1 : ℝ)))
    (continuousAt_id (x := (0 : ℝ)))

private lemma AS065_cont_pow (k : ℕ) : ContinuousAt (fun Y : ℝ => (1 + Y) ^ k) 0 :=
  AS065_cont_shift.pow k

private lemma AS065_cont_num_one : ContinuousAt (fun Y : ℝ => (1 : ℝ)) 0 := by
  exact continuousAt_const (x := (0 : ℝ)) (y := (1 : ℝ))

private lemma AS065_cont_num_two : ContinuousAt (fun Y : ℝ => 2 + Y) 0 := by
  exact ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (2 : ℝ)))
    (continuousAt_id (x := (0 : ℝ)))

private lemma AS065_cont_num_three : ContinuousAt (fun Y : ℝ => 3 + 3 * Y + Y ^ 2) 0 := by
  exact ContinuousAt.add
    (ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (3 : ℝ)))
      ((continuousAt_id (x := (0 : ℝ))).const_mul (3 : ℝ)))
    ((continuousAt_id (x := (0 : ℝ))).pow 2)

private lemma AS065_cont_num_four : ContinuousAt (fun Y : ℝ => 4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) 0 := by
  exact ContinuousAt.add
    (ContinuousAt.add
      (ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (4 : ℝ)))
        ((continuousAt_id (x := (0 : ℝ))).const_mul (6 : ℝ)))
      ((continuousAt_id (x := (0 : ℝ))).pow 2 |> fun h2 =>
        (h2.const_mul (4 : ℝ))))
    ((continuousAt_id (x := (0 : ℝ))).pow 3)

private lemma AS065_cont_num_half : ContinuousAt (fun Y : ℝ => 1 + (1 / 4 : ℝ) * Y) 0 := by
  exact ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (1 : ℝ)))
    ((continuousAt_id (x := (0 : ℝ))).const_mul (1 / 4 : ℝ))

private lemma AS065_cont_num_two_lam : ContinuousAt (fun Y : ℝ => 4 + 4 * Y) 0 := by
  exact ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (4 : ℝ)))
    ((continuousAt_id (x := (0 : ℝ))).const_mul (4 : ℝ))

private lemma AS065_cont_half_sq : ContinuousAt (fun Y : ℝ => (1 + (1 / 2 : ℝ) * Y) ^ 2) 0 := by
  exact ContinuousAt.pow
    (ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (1 : ℝ)))
      ((continuousAt_id (x := (0 : ℝ))).const_mul (1 / 2 : ℝ))) 2

private lemma AS065_cont_two_lam_sq : ContinuousAt (fun Y : ℝ => (1 + (2 : ℝ) * Y) ^ 2) 0 := by
  exact ContinuousAt.pow
    (ContinuousAt.add (continuousAt_const (x := (0 : ℝ)) (y := (1 : ℝ)))
      ((continuousAt_id (x := (0 : ℝ))).const_mul (2 : ℝ))) 2

/- ------------------------------------------------------------------ -/
/- The deep-MOND slope is the count (corpus member), n = 1..4          -/
/- ------------------------------------------------------------------ -/

/-- mu_1'(0) = 1: the one-channel (scalar) response's slope is the count 1. -/
theorem AS065_slope_one :
    Filter.Tendsto (fun Y : ℝ => (1 - (1 + Y)⁻¹) / Y)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (1 : ℝ)) := by
  have hnumT : Filter.Tendsto (fun Y : ℝ => (1 : ℝ)) (𝓝 (0 : ℝ)) (𝓝 (1 : ℝ)) := by
    simpa using (tendsto_const_nhds (f := 𝓝 (0 : ℝ)) (x := (1 : ℝ)))
  have hdenT : Filter.Tendsto (fun Y : ℝ => 1 + Y) (𝓝 (0 : ℝ)) (𝓝 (1 + 0)) :=
    ContinuousAt.tendsto AS065_cont_shift
  have h0 : Filter.Tendsto (fun Y : ℝ => (1 : ℝ) / (1 + Y)) (𝓝 (0 : ℝ))
      (𝓝 ((1 : ℝ) / (1 + 0))) :=
    Filter.Tendsto.div hnumT hdenT (by norm_num : (1 + 0 : ℝ) ≠ 0)
  have h0' : Filter.Tendsto (fun Y : ℝ => (1 : ℝ) / (1 + Y)) (𝓝 (0 : ℝ)) (𝓝 (1 : ℝ)) := by
    simpa using h0
  have hw : Filter.Tendsto (fun Y : ℝ => (1 : ℝ) / (1 + Y))
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (1 : ℝ)) := h0'.mono_left nhdsWithin_le_nhds
  exact Filter.Tendsto.congr' AS065_dq_one hw

/-- mu_2'(0) = 2: the two-channel response's deep-MOND slope is the count 2. -/
theorem AS065_slope_two :
    Filter.Tendsto (fun Y : ℝ => (1 - ((1 + Y) ^ 2)⁻¹) / Y)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (2 : ℝ)) := by
  have hnumT : Filter.Tendsto (fun Y : ℝ => 2 + Y) (𝓝 (0 : ℝ)) (𝓝 (2 + 0)) :=
    ContinuousAt.tendsto AS065_cont_num_two
  have hdenT : Filter.Tendsto (fun Y : ℝ => (1 + Y) ^ 2) (𝓝 (0 : ℝ)) (𝓝 ((1 + 0) ^ 2)) := by
    have hmm := (ContinuousAt.tendsto AS065_cont_shift).mul (ContinuousAt.tendsto AS065_cont_shift)
    simpa [pow_two] using hmm
  have h0 : Filter.Tendsto (fun Y : ℝ => (2 + Y) / (1 + Y) ^ 2) (𝓝 (0 : ℝ))
      (𝓝 ((2 + 0) / (1 + 0) ^ 2)) :=
    Filter.Tendsto.div hnumT hdenT (by norm_num : (1 + 0 : ℝ) ^ 2 ≠ 0)
  have h0' : Filter.Tendsto (fun Y : ℝ => (2 + Y) / (1 + Y) ^ 2) (𝓝 (0 : ℝ)) (𝓝 (2 : ℝ)) := by
    simpa using h0
  have hw : Filter.Tendsto (fun Y : ℝ => (2 + Y) / (1 + Y) ^ 2)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (2 : ℝ)) := h0'.mono_left nhdsWithin_le_nhds
  exact Filter.Tendsto.congr' AS065_dq_two hw

/-- mu_3'(0) = 3: the three-channel response's slope is the count 3. -/
theorem AS065_slope_three :
    Filter.Tendsto (fun Y : ℝ => (1 - ((1 + Y) ^ 3)⁻¹) / Y)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (3 : ℝ)) := by
  have hnumT : Filter.Tendsto (fun Y : ℝ => 3 + 3 * Y + Y ^ 2) (𝓝 (0 : ℝ))
      (𝓝 (3 + 3 * 0 + 0 ^ 2)) := ContinuousAt.tendsto AS065_cont_num_three
  have hdenT : Filter.Tendsto (fun Y : ℝ => (1 + Y) ^ 3) (𝓝 (0 : ℝ)) (𝓝 ((1 + 0) ^ 3)) :=
    ContinuousAt.tendsto (AS065_cont_pow 3)
  have h0 : Filter.Tendsto (fun Y : ℝ => (3 + 3 * Y + Y ^ 2) / (1 + Y) ^ 3) (𝓝 (0 : ℝ))
      (𝓝 ((3 + 3 * 0 + 0 ^ 2) / (1 + 0) ^ 3)) :=
    Filter.Tendsto.div hnumT hdenT (by norm_num : (1 + 0 : ℝ) ^ 3 ≠ 0)
  have h0' : Filter.Tendsto (fun Y : ℝ => (3 + 3 * Y + Y ^ 2) / (1 + Y) ^ 3)
      (𝓝 (0 : ℝ)) (𝓝 (3 : ℝ)) := by
    simpa using h0
  have hw : Filter.Tendsto (fun Y : ℝ => (3 + 3 * Y + Y ^ 2) / (1 + Y) ^ 3)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (3 : ℝ)) := h0'.mono_left nhdsWithin_le_nhds
  exact Filter.Tendsto.congr' AS065_dq_three hw

/-- mu_4'(0) = 4: the 2x2 grouped (four-channel) response's slope is 4 = 2*2. -/
theorem AS065_slope_four :
    Filter.Tendsto (fun Y : ℝ => (1 - ((1 + Y) ^ 4)⁻¹) / Y)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (4 : ℝ)) := by
  have hnumT : Filter.Tendsto (fun Y : ℝ => 4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) (𝓝 (0 : ℝ))
      (𝓝 (4 + 6 * 0 + 4 * 0 ^ 2 + 0 ^ 3)) := ContinuousAt.tendsto AS065_cont_num_four
  have hdenT : Filter.Tendsto (fun Y : ℝ => (1 + Y) ^ 4) (𝓝 (0 : ℝ)) (𝓝 ((1 + 0) ^ 4)) :=
    ContinuousAt.tendsto (AS065_cont_pow 4)
  have h0 : Filter.Tendsto (fun Y : ℝ => (4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) / (1 + Y) ^ 4)
      (𝓝 (0 : ℝ)) (𝓝 ((4 + 6 * 0 + 4 * 0 ^ 2 + 0 ^ 3) / (1 + 0) ^ 4)) :=
    Filter.Tendsto.div hnumT hdenT (by norm_num : (1 + 0 : ℝ) ^ 4 ≠ 0)
  have h0' : Filter.Tendsto (fun Y : ℝ => (4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) / (1 + Y) ^ 4)
      (𝓝 (0 : ℝ)) (𝓝 (4 : ℝ)) := by
    simpa using h0
  have hw : Filter.Tendsto (fun Y : ℝ => (4 + 6 * Y + 4 * Y ^ 2 + Y ^ 3) / (1 + Y) ^ 4)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (4 : ℝ)) := h0'.mono_left nhdsWithin_le_nhds
  exact Filter.Tendsto.congr' AS065_dq_four hw

/- ------------------------------------------------------------------ -/
/- Negative control: the GROUP slope is 2, not 1, in the vacuum unit     -/
/- ------------------------------------------------------------------ -/

/-- The group of two channels (corpus member) has vacuum-unit slope 2
    (this is AS065_slope_two read as the GROUPED response).  -/
theorem AS065_group_two_slope_two :
    Filter.Tendsto (fun Y : ℝ => (1 - ((1 + Y) ^ 2)⁻¹) / Y)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (2 : ℝ)) :=
  AS065_slope_two

/-- The claim "the normalized group drive slope remains one after grouping"
    is FALSE: the slope is 2, and 2 is not 1. -/
theorem AS065_group_slope_not_one : (2 : ℝ) ≠ 1 := by
  norm_num

/- ------------------------------------------------------------------ -/
/- kappa matching and the grouping family                             -/
/- ------------------------------------------------------------------ -/

/-- Generic grouping reading: the m-channel world's kappa is 1/m.  -/
theorem AS065_kappa_matching_generic (s m : ℝ) (hs : s ≠ 0) (hm : m ≠ 0) :
    (s / m) / s = 1 / m := by
  field_simp [hs, hm]

/-- kappa = 1/2 for the two-channel world (and for every scale s != 0). -/
theorem AS065_kappa_half_landing (a0 s : ℝ) (hs : s ≠ 0) (ha0 : a0 = s / 2) :
    a0 / s = 1 / 2 := by
  rw [ha0]
  field_simp [hs]

/-- The full deep-MOND chain: slope-2 response (mu ~ 2 g/s) in the Poisson
    equation plus the a0-line implies a0 = s/2. -/
theorem AS065_a0_line_chain (g s a0 gN : ℝ) (hs : s ≠ 0) (hgN : gN ≠ 0)
    (hdeep : 2 * (g / s) * g = gN) (hline : g ^ 2 = a0 * gN) :
    a0 = s / 2 := by
  have hg2 : g ^ 2 = (s / 2) * gN := by
    rw [← hdeep]
    field_simp [hs] <;> ring
  have ha0 : a0 * gN = (s / 2) * gN := by
    calc
      a0 * gN = g ^ 2 := hline.symm
      _ = (s / 2) * gN := hg2
  exact mul_right_cancel₀ hgN ha0

/- ------------------------------------------------------------------ -/
/- lambda diagnostics: scale covariance of the count reading            -/
/- ------------------------------------------------------------------ -/

/-- Covariant ratio: for every nonzero unit rescaling lambda, the matched
    scale over the vacuum rate is 1/2 (a0_lam = (lam*s)/(2*lam)). -/
theorem AS065_kappa_covariant_lambda (s lam : ℝ) (hs : s ≠ 0) (hlam : lam ≠ 0) :
    ((s * lam) / (2 * lam)) / s = 1 / 2 := by
  field_simp [hs, hlam]

/-- Reading slope at lam = 1/2 (unit s/2): the SAME two-channel response
    reads as ONE unit-slope channel: slope 2*(1/2) = 1. -/
theorem AS065_lambda_reading_half :
    Filter.Tendsto (fun Y : ℝ => (1 - ((1 + (1 / 2 : ℝ) * Y) ^ 2)⁻¹) / Y)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (1 : ℝ)) := by
  have hnumT : Filter.Tendsto (fun Y : ℝ => 1 + (1 / 4 : ℝ) * Y) (𝓝 (0 : ℝ))
      (𝓝 (1 + (1 / 4 : ℝ) * 0)) := ContinuousAt.tendsto AS065_cont_num_half
  have hdenT : Filter.Tendsto (fun Y : ℝ => (1 + (1 / 2 : ℝ) * Y) ^ 2) (𝓝 (0 : ℝ))
      (𝓝 ((1 + (1 / 2 : ℝ) * 0) ^ 2)) := ContinuousAt.tendsto AS065_cont_half_sq
  have h0 : Filter.Tendsto
      (fun Y : ℝ => (1 + (1 / 4 : ℝ) * Y) / (1 + (1 / 2 : ℝ) * Y) ^ 2)
      (𝓝 (0 : ℝ))
      (𝓝 ((1 + (1 / 4 : ℝ) * 0) / (1 + (1 / 2 : ℝ) * 0) ^ 2)) :=
    Filter.Tendsto.div hnumT hdenT (by norm_num : (1 + (1 / 2 : ℝ) * 0) ^ 2 ≠ 0)
  have h0' : Filter.Tendsto
      (fun Y : ℝ => (1 + (1 / 4 : ℝ) * Y) / (1 + (1 / 2 : ℝ) * Y) ^ 2)
      (𝓝 (0 : ℝ)) (𝓝 (1 : ℝ)) := by
    simpa using h0
  have hw : Filter.Tendsto
      (fun Y : ℝ => (1 + (1 / 4 : ℝ) * Y) / (1 + (1 / 2 : ℝ) * Y) ^ 2)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (1 : ℝ)) := h0'.mono_left nhdsWithin_le_nhds
  exact Filter.Tendsto.congr' AS065_dq_half hw

/-- Reading slope at lam = 2 (unit 2s): the SAME response reads as FOUR
    channels: slope 2*2 = 4. -/
theorem AS065_lambda_reading_two :
    Filter.Tendsto (fun Y : ℝ => (1 - ((1 + (2 : ℝ) * Y) ^ 2)⁻¹) / Y)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (4 : ℝ)) := by
  have hnumT : Filter.Tendsto (fun Y : ℝ => 4 + 4 * Y) (𝓝 (0 : ℝ))
      (𝓝 (4 + 4 * 0)) := ContinuousAt.tendsto AS065_cont_num_two_lam
  have hdenT : Filter.Tendsto (fun Y : ℝ => (1 + (2 : ℝ) * Y) ^ 2) (𝓝 (0 : ℝ))
      (𝓝 ((1 + (2 : ℝ) * 0) ^ 2)) := ContinuousAt.tendsto AS065_cont_two_lam_sq
  have h0 : Filter.Tendsto (fun Y : ℝ => (4 + 4 * Y) / (1 + (2 : ℝ) * Y) ^ 2)
      (𝓝 (0 : ℝ)) (𝓝 ((4 + 4 * 0) / (1 + (2 : ℝ) * 0) ^ 2)) :=
    Filter.Tendsto.div hnumT hdenT (by norm_num : (1 + (2 : ℝ) * 0) ^ 2 ≠ 0)
  have h0' : Filter.Tendsto (fun Y : ℝ => (4 + 4 * Y) / (1 + (2 : ℝ) * Y) ^ 2)
      (𝓝 (0 : ℝ)) (𝓝 (4 : ℝ)) := by
    simpa using h0
  have hw : Filter.Tendsto (fun Y : ℝ => (4 + 4 * Y) / (1 + (2 : ℝ) * Y) ^ 2)
      (nhdsWithin (0 : ℝ) ({t : ℝ | t ≠ 0})) (𝓝 (4 : ℝ)) := h0'.mono_left nhdsWithin_le_nhds
  exact Filter.Tendsto.congr' AS065_dq_two_lam hw

/-- Unit-confused readings (mistaking lam*s for the vacuum rate s):
    kappa = 1/(2*lam) gives {1, 1/2, 1/4} at lam = 1/2, 1, 2. -/
theorem AS065_naive_readings :
    (1 / (2 * (1 / 2 : ℝ)) = 1) ∧ (1 / (2 * (1 : ℝ)) = 1 / 2) ∧ (1 / (2 * (2 : ℝ)) = 1 / 4) := by
  norm_num

#check AS065_or_closure_pow
#check AS065_or_closure_response
#check AS065_closure_member_two_times_two
#check AS065_survival_grouping
#check AS065_slope_one
#check AS065_slope_two
#check AS065_slope_three
#check AS065_slope_four
#check AS065_group_two_slope_two
#check AS065_group_slope_not_one
#check AS065_kappa_matching_generic
#check AS065_kappa_half_landing
#check AS065_a0_line_chain
#check AS065_kappa_covariant_lambda
#check AS065_lambda_reading_half
#check AS065_lambda_reading_two
#check AS065_naive_readings

#print axioms AS065_or_closure_pow
#print axioms AS065_or_closure_response
#print axioms AS065_closure_member_two_times_two
#print axioms AS065_survival_grouping
#print axioms AS065_slope_one
#print axioms AS065_slope_two
#print axioms AS065_slope_three
#print axioms AS065_slope_four
#print axioms AS065_group_two_slope_two
#print axioms AS065_group_slope_not_one
#print axioms AS065_kappa_matching_generic
#print axioms AS065_kappa_half_landing
#print axioms AS065_a0_line_chain
#print axioms AS065_kappa_covariant_lambda
#print axioms AS065_lambda_reading_half
#print axioms AS065_lambda_reading_two
#print axioms AS065_naive_readings
