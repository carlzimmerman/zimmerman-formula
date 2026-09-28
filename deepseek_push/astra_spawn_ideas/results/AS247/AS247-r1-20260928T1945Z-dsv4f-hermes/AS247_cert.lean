import Mathlib

noncomputable section
open scoped Real

/-!
AS247 Lean 4 certificate — same-action Shapiro-delay functional.
Seed: AS247_construct_a_same_action_shapiro_delay_integral.md
      (sha256 68357b52d30e87c91f7fad43e8c0798c4db573dacf3ca5adf6aa746913562714)
Metric (weak field, c restored by the caller): ds^2 = -(1+2u) c^2 dt^2 + (1-2v) dx^2
with u = Phi/c^2, v = Psi/c^2 dimensionless. Null rays: c dt/dl = sqrt((1-2v)/(1+2u)).
Delay functional: Delta t = -(1/c^3) integral (Phi + Psi) dl = -(1/c) integral (u + v) dl
at linear order. Certified here (real analysis only):
 1. linear_remainder: exact remainder of the linearization  sqrt-exact vs (1 - (u+v))
 2. weak_field_denominators: 1+2u, 1-2v, 1-(u+v) > 0 for |u|,|v| <= 1/100
 3. linear_remainder_bound: |remainder| <= 151/125000 for fields bounded by 1/100
 4. delay_sign: attractive potentials u,v < 0 give a positive (delay) correction
 5. endpoint_shift: additive constant shifts of the potentials shift the integral by
    (c + c')*(b-a) -> the DIFFERENCE between two rays with the same shift is invariant
 6. slip_shift: the delay functional responds linearly to the slip psi - phi
 7. slip_changes_delay: a nonzero slip changes the delay (negative-control algebra)
 8. newton_antideriv: d/dx log(x + sqrt(x^2 + b^2)) = 1/sqrt(x^2 + b^2)
 9. newton_delay_closed: the Newtonian two-sided chord integral closed form
    (the standard Shapiro geometry: Phi = Psi = -GM/r on a chord at impact b)
10. point_mass_delay: that closed form is strictly positive
11. deep_log_antideriv: d/dx [x log sqrt(x^2+b^2) + b arctan(x/b) - x] = log sqrt(x^2+b^2)
12. deep_log_integral: symmetric closed form for the deep log-potential delay
Helpers (strict sqrt monotonicity by the two-sided square argument, b > 0):
    sqrt_gt_abs: |x| < sqrt(x^2 + b^2);  sqrt_gt_x: X < sqrt(X^2 + b^2) for X > 0;
    sum_pos: 0 < x + sqrt(x^2 + b^2).
-/

-- ============================================================
-- helpers: strict sqrt monotonicity (never linarith inside sqrt)
-- ============================================================
lemma sqrt_gt_abs (x b : ℝ) (hb : 0 < b) : |x| < Real.sqrt (x ^ 2 + b ^ 2) := by
  have hsq0 : 0 ≤ x ^ 2 := sq_nonneg x
  have hsq : 0 ≤ x ^ 2 + b ^ 2 := by nlinarith [sq_nonneg x, sq_nonneg b]
  have hlt : x ^ 2 < x ^ 2 + b ^ 2 := by nlinarith [sq_pos_of_pos hb]
  have h1 : Real.sqrt (x ^ 2) < Real.sqrt (x ^ 2 + b ^ 2) :=
    Real.sqrt_lt_sqrt hsq0 hlt
  rwa [Real.sqrt_sq_eq_abs] at h1

lemma sqrt_gt_x (X b : ℝ) (hX : 0 < X) (hb : 0 < b) :
    X < Real.sqrt (X ^ 2 + b ^ 2) := by
  have hg := sqrt_gt_abs X b hb
  have hx : |X| = X := abs_of_pos hX
  rwa [hx] at hg

lemma sum_pos (x b : ℝ) (hb : 0 < b) : 0 < x + Real.sqrt (x ^ 2 + b ^ 2) := by
  have hg := sqrt_gt_abs x b hb
  have hroot : 0 < Real.sqrt (x ^ 2 + b ^ 2) :=
    Real.sqrt_pos.2 (by nlinarith [sq_nonneg x, hb])
  by_cases hx : x ≤ 0
  · have ha : |x| = -x := abs_of_nonpos hx
    linarith
  · have hx0 : 0 ≤ x := le_of_not_gt (fun h0x => hx (le_of_lt h0x))
    nlinarith [hroot, hx0]

-- ============================================================
-- 1. exact remainder of the linearization
-- ============================================================
theorem linear_remainder (u v : ℝ) :
    (1 - (u + v)) ^ 2 * (1 + 2 * u) - (1 - 2 * v)
      = (u + v) ^ 2 + 2 * u * (u + v) ^ 2 - 4 * u * (u + v) := by
  ring

-- ============================================================
-- 2. denominators positive on the weak-field domain
-- ============================================================
theorem weak_field_denominators (u v : ℝ)
    (hu1 : -(1 / 100 : ℝ) ≤ u) (hu2 : u ≤ 1 / 100)
    (hv1 : -(1 / 100 : ℝ) ≤ v) (hv2 : v ≤ 1 / 100) :
    0 < 1 + 2 * u ∧ 0 < 1 - 2 * v ∧ 0 < 1 - (u + v) := by
  constructor
  · nlinarith
  · constructor
    · nlinarith
    · nlinarith

-- ============================================================
-- 3. remainder bound: |R| <= 151/125000 = 12e-4 + 8e-6  (eps = 1/100)
-- ============================================================
theorem linear_remainder_bound (u v : ℝ)
    (hu1 : -(1 / 100 : ℝ) ≤ u) (hu2 : u ≤ 1 / 100)
    (hv1 : -(1 / 100 : ℝ) ≤ v) (hv2 : v ≤ 1 / 100) :
    (1 - (u + v)) ^ 2 * (1 + 2 * u) - (1 - 2 * v) ≤ 151 / 125000 ∧
    -((1 - (u + v)) ^ 2 * (1 + 2 * u) - (1 - 2 * v)) ≤ 151 / 125000 := by
  rw [linear_remainder]
  have hs1low : -(1 / 50 : ℝ) ≤ u + v := by nlinarith
  have hs1hi : u + v ≤ 1 / 50 := by nlinarith
  have hsqs : (u + v) ^ 2 ≤ (1 / 50 : ℝ) ^ 2 := by
    have hA : 0 ≤ 1 / 50 - (u + v) := by linarith
    have hB : 0 ≤ 1 / 50 + (u + v) := by linarith
    have hprod : 0 ≤ (1 / 50 - (u + v)) * (1 / 50 + (u + v)) :=
      mul_nonneg hA hB
    nlinarith
  have h1p : 0 ≤ 1 + 2 * u := by nlinarith
  have h1p2 : 1 + 2 * u ≤ 1 + 2 / 100 := by nlinarith
  have hA' : (u + v) ^ 2 * (1 + 2 * u) ≤ (1 / 50 : ℝ) ^ 2 * (1 + 2 / 100) :=
    mul_le_mul hsqs h1p2 h1p (by norm_num : 0 ≤ (1 / 50 : ℝ) ^ 2)
  have hsqv : v ^ 2 ≤ (1 / 100 : ℝ) ^ 2 := by
    have hA : 0 ≤ 1 / 100 - v := by linarith
    have hB : 0 ≤ 1 / 100 + v := by linarith
    have hprod : 0 ≤ (1 / 100 - v) * (1 / 100 + v) := mul_nonneg hA hB
    nlinarith
  have hUs : -(1 / 100 : ℝ) * (1 / 50) ≤ u * (u + v) := by
    have hsq1 : 0 ≤ (u + v / 2) ^ 2 := sq_nonneg (u + v / 2)
    nlinarith [hsq1, hsqv]
  have hB' : -4 * u * (u + v) ≤ 8 * (1 / 100 : ℝ) ^ 2 := by nlinarith [hUs]
  constructor
  · nlinarith [hA', hB']
  · have hneg : -((u + v) ^ 2 * (1 + 2 * u)) ≤ 0 := by
      nlinarith [mul_nonneg (sq_nonneg (u + v)) h1p]
    have hB2 : 4 * u * (u + v) ≤ 8 * (1 / 100 : ℝ) ^ 2 := by nlinarith [hUs]
    nlinarith [hneg, hB2]

-- ============================================================
-- 4. attractive potentials delay (positive correction; no-slip u = v = -GM/(c^2 r))
-- ============================================================
theorem delay_sign (u v : ℝ) (hu : u < 0) (hv : v < 0) : 0 < -(u + v) := by
  nlinarith

-- ============================================================
-- 5. endpoint / additive normalization of the delay integral
-- ============================================================
theorem endpoint_shift (a b c c' : ℝ) (u v : ℝ → ℝ)
    (hu : Continuous u) (hv : Continuous v) :
    (∫ x in a..b, u x + c) + (∫ x in a..b, v x + c')
      = (∫ x in a..b, u x) + (∫ x in a..b, v x) + c * (b - a) + c' * (b - a) := by
  have hui : IntervalIntegrable u MeasureTheory.volume a b :=
    Continuous.intervalIntegrable hu a b
  have hvi : IntervalIntegrable v MeasureTheory.volume a b :=
    Continuous.intervalIntegrable hv a b
  have hcst : IntervalIntegrable (fun _ : ℝ => c) MeasureTheory.volume a b :=
    Continuous.intervalIntegrable continuous_const a b
  have hcst' : IntervalIntegrable (fun _ : ℝ => c') MeasureTheory.volume a b :=
    Continuous.intervalIntegrable continuous_const a b
  have h1 : ∫ x in a..b, u x + c = (∫ x in a..b, u x) + c * (b - a) := by
    rw [intervalIntegral.integral_add hui hcst]
    rw [intervalIntegral.integral_const]
    simp [smul_eq_mul]
    ring
  have h2 : ∫ x in a..b, v x + c' = (∫ x in a..b, v x) + c' * (b - a) := by
    rw [intervalIntegral.integral_add hvi hcst']
    rw [intervalIntegral.integral_const]
    simp [smul_eq_mul]
    ring
  rw [h1, h2]
  ring

-- ============================================================
-- 6. slip sensitivity: linear response of the functional to Psi -> Psi + delta
-- ============================================================
theorem slip_shift (a b : ℝ) (u δ : ℝ → ℝ)
    (hu : Continuous u) (hδ : Continuous δ) :
    ∫ x in a..b, (u x + δ x) = (∫ x in a..b, u x) + (∫ x in a..b, δ x) := by
  exact intervalIntegral.integral_add (Continuous.intervalIntegrable hu a b)
    (Continuous.intervalIntegrable hδ a b)

-- ============================================================
-- 7. negative control: a nonvanishing slip changes the delay
-- ============================================================
theorem slip_changes_delay (a b : ℝ) (u δ : ℝ → ℝ)
    (hu : Continuous u) (hδ : Continuous δ) (hδi : ∫ x in a..b, δ x ≠ 0) :
    ∫ x in a..b, (u x + δ x) ≠ ∫ x in a..b, u x := by
  intro h
  have hs := slip_shift a b u δ hu hδ
  rw [h] at hs
  have hz : ∫ x in a..b, δ x = 0 := by linarith
  exact hδi hz

-- ============================================================
-- 8. Newtonian antiderivative
-- ============================================================
theorem newton_antideriv (b : ℝ) (hb : 0 < b) (x : ℝ) :
    HasDerivAt (fun t : ℝ => Real.log (t + Real.sqrt (t ^ 2 + b ^ 2)))
      (1 / Real.sqrt (x ^ 2 + b ^ 2)) x := by
  have hsq : 0 ≤ x ^ 2 + b ^ 2 := by nlinarith [sq_nonneg x, sq_nonneg b]
  have hsqp : 0 < x ^ 2 + b ^ 2 := by nlinarith [sq_nonneg x, hb]
  have hsqrt : Real.sqrt (x ^ 2 + b ^ 2) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hsqp)
  have harg : x + Real.sqrt (x ^ 2 + b ^ 2) ≠ 0 := ne_of_gt (sum_pos x b hb)
  have hid : HasDerivAt (fun t : ℝ => t) 1 x := hasDerivAt_id x
  have hpow : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := by
    simpa using (hasDerivAt_pow 2 x)
  have hadd : HasDerivAt (fun t : ℝ => t ^ 2 + b ^ 2) (2 * x) x := by
    convert hpow.add (hasDerivAt_const x (b ^ 2)) using 4
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring
  have hscomp : HasDerivAt (fun t : ℝ => Real.sqrt (t ^ 2 + b ^ 2))
      (x / Real.sqrt (x ^ 2 + b ^ 2)) x := by
    have hds : HasDerivAt (fun t : ℝ => Real.sqrt (t ^ 2 + b ^ 2))
        (1 / (2 * Real.sqrt (x ^ 2 + b ^ 2)) * (2 * x)) x := by
      convert HasDerivAt.comp x
        (Real.hasDerivAt_sqrt (by nlinarith : x ^ 2 + b ^ 2 ≠ 0)) hadd using 3
      · first | rfl | ring
      · first | rfl | ring
      · first | rfl | ring
    have hval : 1 / (2 * Real.sqrt (x ^ 2 + b ^ 2)) * (2 * x)
        = x / Real.sqrt (x ^ 2 + b ^ 2) := by
      field_simp [hsqrt]
    rwa [hval] at hds
  have hsum : HasDerivAt (fun t : ℝ => t + Real.sqrt (t ^ 2 + b ^ 2))
      (1 + x / Real.sqrt (x ^ 2 + b ^ 2)) x := by
    convert hid.add hscomp using 3
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring

  have hlog : HasDerivAt (fun t : ℝ => Real.log (t + Real.sqrt (t ^ 2 + b ^ 2)))
      (1 / Real.sqrt (x ^ 2 + b ^ 2)) x := by
    have hds : HasDerivAt (fun t : ℝ => Real.log (t + Real.sqrt (t ^ 2 + b ^ 2)))
        ((x + Real.sqrt (x ^ 2 + b ^ 2))⁻¹ * (1 + x / Real.sqrt (x ^ 2 + b ^ 2))) x := by
      convert HasDerivAt.comp x (Real.hasDerivAt_log harg) hsum using 3
      · first | rfl | ring
      · first | rfl | ring
      · first | rfl | ring

    have hval : (x + Real.sqrt (x ^ 2 + b ^ 2))⁻¹ * (1 + x / Real.sqrt (x ^ 2 + b ^ 2))
        = 1 / Real.sqrt (x ^ 2 + b ^ 2) := by
      have hmain : (x + Real.sqrt (x ^ 2 + b ^ 2)) *
            ((x + Real.sqrt (x ^ 2 + b ^ 2))⁻¹ * (1 + x / Real.sqrt (x ^ 2 + b ^ 2)))
          = (x + Real.sqrt (x ^ 2 + b ^ 2)) * (1 / Real.sqrt (x ^ 2 + b ^ 2)) := by
        field_simp [harg, hsqrt]
        ring
      exact mul_left_cancel₀ harg hmain
    rwa [hval] at hds
  exact hlog

-- ============================================================
-- 9. Newtonian chord delay closed form (Phi = Psi = -GM/r, point mass)
-- ============================================================
theorem newton_delay_closed (m X b : ℝ) (hm : 0 < m) (hX : 0 < X) (hb : 0 < b) :
    ∫ x in -X..X, (2 * m / Real.sqrt (x ^ 2 + b ^ 2))
      = 2 * m * Real.log ((X + Real.sqrt (X ^ 2 + b ^ 2)) /
          (Real.sqrt (X ^ 2 + b ^ 2) - X)) := by
  have hder : ∀ x ∈ Set.uIcc (-X) X,
      HasDerivAt (fun t : ℝ => Real.log (t + Real.sqrt (t ^ 2 + b ^ 2)))
        (1 / Real.sqrt (x ^ 2 + b ^ 2)) x := by
    intro x hx
    exact newton_antideriv b hb x
  have hcont : Continuous (fun x : ℝ => (Real.sqrt (x ^ 2 + b ^ 2))⁻¹) := by
    apply Continuous.inv₀
    · exact Real.continuous_sqrt.comp
        (by fun_prop : Continuous (fun x : ℝ => x ^ 2 + b ^ 2))
    · intro x
      exact ne_of_gt (Real.sqrt_pos.2 (by nlinarith [sq_nonneg x, sq_pos_of_pos hb]))
  have hint : IntervalIntegrable (fun x : ℝ => 1 / Real.sqrt (x ^ 2 + b ^ 2))
      MeasureTheory.volume (-X) X := by
    simpa [one_div] using Continuous.intervalIntegrable hcont (-X) X
  have hF0 : ∫ x in -X..X, 1 / Real.sqrt (x ^ 2 + b ^ 2)
      = Real.log (X + Real.sqrt (X ^ 2 + b ^ 2))
        - Real.log (-X + Real.sqrt ((-X) ^ 2 + b ^ 2)) :=
    intervalIntegral.integral_eq_sub_of_hasDerivAt hder hint
  have hneg : (-X) ^ 2 = X ^ 2 := by ring
  have hswap : -X + Real.sqrt (X ^ 2 + b ^ 2) = Real.sqrt (X ^ 2 + b ^ 2) - X := by
    ring
  have hF : ∫ x in -X..X, 1 / Real.sqrt (x ^ 2 + b ^ 2)
      = Real.log (X + Real.sqrt (X ^ 2 + b ^ 2))
        - Real.log (Real.sqrt (X ^ 2 + b ^ 2) - X) := by
    rw [hneg] at hF0
    rw [hswap] at hF0
    exact hF0
  have hpx : 0 < X + Real.sqrt (X ^ 2 + b ^ 2) := sum_pos X b hb
  have hmn : 0 < Real.sqrt (X ^ 2 + b ^ 2) - X :=
    sub_pos.mpr (sqrt_gt_x X b hX hb)
  have hlog : Real.log (X + Real.sqrt (X ^ 2 + b ^ 2))
        - Real.log (Real.sqrt (X ^ 2 + b ^ 2) - X)
      = Real.log ((X + Real.sqrt (X ^ 2 + b ^ 2)) /
          (Real.sqrt (X ^ 2 + b ^ 2) - X)) := by
    rw [← Real.log_div (ne_of_gt hpx) (ne_of_gt hmn)]
  have hlift : ∫ x in -X..X, (2 * m / Real.sqrt (x ^ 2 + b ^ 2))
      = 2 * m * ∫ x in -X..X, (1 / Real.sqrt (x ^ 2 + b ^ 2)) := by
    calc
      ∫ x in -X..X, (2 * m / Real.sqrt (x ^ 2 + b ^ 2))
          = ∫ x in -X..X, (2 * m) * (1 / Real.sqrt (x ^ 2 + b ^ 2)) := by
            apply intervalIntegral.integral_congr
            intro x hx
            have hsx : Real.sqrt (x ^ 2 + b ^ 2) ≠ 0 := ne_of_gt
              (Real.sqrt_pos.2 (by nlinarith [sq_nonneg x, sq_pos_of_pos hb]))
            field_simp [hsx]
      _ = (2 * m) * ∫ x in -X..X, (1 / Real.sqrt (x ^ 2 + b ^ 2)) := by
            rw [intervalIntegral.integral_const_mul]
  rw [hlift, hF, hlog]

-- ============================================================
-- 10. the Newtonian delay is strictly positive
-- ============================================================
theorem point_mass_delay (m X b : ℝ) (hm : 0 < m) (hX : 0 < X) (hb : 0 < b) :
    0 < ∫ x in -X..X, (2 * m / Real.sqrt (x ^ 2 + b ^ 2)) := by
  rw [newton_delay_closed m X b hm hX hb]
  have hpx : 0 < X + Real.sqrt (X ^ 2 + b ^ 2) := sum_pos X b hb
  have hmn : 0 < Real.sqrt (X ^ 2 + b ^ 2) - X :=
    sub_pos.mpr (sqrt_gt_x X b hX hb)
  have hgt1 : 1 < (X + Real.sqrt (X ^ 2 + b ^ 2)) /
      (Real.sqrt (X ^ 2 + b ^ 2) - X) := by
    rw [one_lt_div hmn]
    nlinarith [hX]
  have hlog : 0 < Real.log ((X + Real.sqrt (X ^ 2 + b ^ 2)) /
      (Real.sqrt (X ^ 2 + b ^ 2) - X)) := Real.log_pos hgt1
  nlinarith [hm, hlog]

-- ============================================================
-- 11. deep log-potential antiderivative
-- ============================================================
theorem deep_log_antideriv (b : ℝ) (hb : 0 < b) (x : ℝ) :
    HasDerivAt (fun t : ℝ => t * Real.log (Real.sqrt (t ^ 2 + b ^ 2))
        + b * Real.arctan (t / b) - t)
      (Real.log (Real.sqrt (x ^ 2 + b ^ 2))) x := by
  have hsq : 0 ≤ x ^ 2 + b ^ 2 := by nlinarith [sq_nonneg x, sq_nonneg b]
  have hsqp : 0 < x ^ 2 + b ^ 2 := by nlinarith [sq_nonneg x, hb]
  have hsqrt : Real.sqrt (x ^ 2 + b ^ 2) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.2 hsqp)
  have hsqid : Real.sqrt (x ^ 2 + b ^ 2) ^ 2 = x ^ 2 + b ^ 2 :=
    Real.sq_sqrt hsq
  have hid : HasDerivAt (fun t : ℝ => t) 1 x := hasDerivAt_id x
  have hpow : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := by
    simpa using (hasDerivAt_pow 2 x)
  have hadd : HasDerivAt (fun t : ℝ => t ^ 2 + b ^ 2) (2 * x) x := by
    convert hpow.add (hasDerivAt_const x (b ^ 2)) using 4
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring
  have hscomp : HasDerivAt (fun t : ℝ => Real.sqrt (t ^ 2 + b ^ 2))
      (x / Real.sqrt (x ^ 2 + b ^ 2)) x := by
    have hds : HasDerivAt (fun t : ℝ => Real.sqrt (t ^ 2 + b ^ 2))
        (1 / (2 * Real.sqrt (x ^ 2 + b ^ 2)) * (2 * x)) x := by
      convert HasDerivAt.comp x
        (Real.hasDerivAt_sqrt (by nlinarith : x ^ 2 + b ^ 2 ≠ 0)) hadd using 3
      · first | rfl | ring
      · first | rfl | ring
      · first | rfl | ring
    have hval : 1 / (2 * Real.sqrt (x ^ 2 + b ^ 2)) * (2 * x)
        = x / Real.sqrt (x ^ 2 + b ^ 2) := by
      field_simp [hsqrt]
    rwa [hval] at hds
  have hval : (Real.sqrt (x ^ 2 + b ^ 2))⁻¹ * (x / Real.sqrt (x ^ 2 + b ^ 2))
      = x / (x ^ 2 + b ^ 2) := by
    have h1 : (Real.sqrt (x ^ 2 + b ^ 2))⁻¹ * (x / Real.sqrt (x ^ 2 + b ^ 2))
        = x / (Real.sqrt (x ^ 2 + b ^ 2) * Real.sqrt (x ^ 2 + b ^ 2)) := by
      field_simp [hsqrt]
    have hr2 : Real.sqrt (x ^ 2 + b ^ 2) * Real.sqrt (x ^ 2 + b ^ 2)
        = Real.sqrt (x ^ 2 + b ^ 2) ^ 2 := by ring
    have h2 : x / (Real.sqrt (x ^ 2 + b ^ 2) * Real.sqrt (x ^ 2 + b ^ 2))
        = x / (x ^ 2 + b ^ 2) := by
      rw [hr2, hsqid]
    rwa [h2] at h1
  have hlogc : HasDerivAt (fun t : ℝ => Real.log (Real.sqrt (t ^ 2 + b ^ 2)))
      (x / (x ^ 2 + b ^ 2)) x := by
    have hds : HasDerivAt (fun t : ℝ => Real.log (Real.sqrt (t ^ 2 + b ^ 2)))
        ((Real.sqrt (x ^ 2 + b ^ 2))⁻¹ * (x / Real.sqrt (x ^ 2 + b ^ 2))) x := by
      convert HasDerivAt.comp x (Real.hasDerivAt_log hsqrt) hscomp using 3
      · first | rfl | ring
      · first | rfl | ring
      · first | rfl | ring
    rwa [hval] at hds
  have hmulc : HasDerivAt (fun t : ℝ =>
      t * Real.log (Real.sqrt (t ^ 2 + b ^ 2)))
      (Real.log (Real.sqrt (x ^ 2 + b ^ 2)) + x * (x / (x ^ 2 + b ^ 2))) x := by
    convert hid.mul hlogc using 4
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring
  have hds : HasDerivAt (fun t : ℝ => Real.arctan (t / b))
      (1 / (1 + (x / b) ^ 2) * (1 / b)) x := by
    have hdiv : HasDerivAt (fun t : ℝ => t / b) (1 / b) x := by
      simpa using hid.div_const b
    exact HasDerivAt.comp x (Real.hasDerivAt_arctan (x / b)) hdiv
  have hval2 : 1 / (1 + (x / b) ^ 2) * (1 / b) = b / (x ^ 2 + b ^ 2) := by
    field_simp [hb.ne']
    ring
  have hdsp : HasDerivAt (fun t : ℝ => Real.arctan (t / b))
      (b / (x ^ 2 + b ^ 2)) x := by
    rwa [hval2] at hds
  have harct : HasDerivAt (fun t : ℝ => b * Real.arctan (t / b))
      (b ^ 2 / (x ^ 2 + b ^ 2)) x := by
    have hdsb : HasDerivAt (fun t : ℝ => b * Real.arctan (t / b))
        (b * (b / (x ^ 2 + b ^ 2))) x := by
      convert (hasDerivAt_const x b).mul hdsp using 4
      · first | rfl | ring
      · first | rfl | ring
      · first | rfl | ring
      · first | rfl | ring
    have hval3 : b * (b / (x ^ 2 + b ^ 2)) = b ^ 2 / (x ^ 2 + b ^ 2) := by
      ring
    rwa [hval3] at hdsb
  have hsum : HasDerivAt (fun t : ℝ =>
      t * Real.log (Real.sqrt (t ^ 2 + b ^ 2))
        + b * Real.arctan (t / b))
      (Real.log (Real.sqrt (x ^ 2 + b ^ 2)) + x * (x / (x ^ 2 + b ^ 2))
        + b ^ 2 / (x ^ 2 + b ^ 2)) x := by
    convert hmulc.add harct using 3
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring


  have htot : HasDerivAt (fun t : ℝ =>
      t * Real.log (Real.sqrt (t ^ 2 + b ^ 2))
        + b * Real.arctan (t / b) - t)
      (Real.log (Real.sqrt (x ^ 2 + b ^ 2)) + x * (x / (x ^ 2 + b ^ 2))
        + b ^ 2 / (x ^ 2 + b ^ 2) - 1) x := by
    convert hsum.sub hid using 3
    · first | rfl | ring
    · first | rfl | ring
    · first | rfl | ring


  have hval' : Real.log (Real.sqrt (x ^ 2 + b ^ 2))
        + x * (x / (x ^ 2 + b ^ 2)) + b ^ 2 / (x ^ 2 + b ^ 2) - 1
      = Real.log (Real.sqrt (x ^ 2 + b ^ 2)) := by
    have hdiv1 : x * (x / (x ^ 2 + b ^ 2)) + b ^ 2 / (x ^ 2 + b ^ 2) = 1 := by
      field_simp [hsqp.ne']
    nlinarith
  rwa [hval'] at htot

-- ============================================================
-- 12. deep log potential symmetric chord integral
-- ============================================================
theorem deep_log_integral (X b : ℝ) (hX : 0 < X) (hb : 0 < b) :
    ∫ x in -X..X, Real.log (Real.sqrt (x ^ 2 + b ^ 2))
      = 2 * X * Real.log (Real.sqrt (X ^ 2 + b ^ 2))
        + 2 * b * Real.arctan (X / b) - 2 * X := by
  have hder : ∀ x ∈ Set.uIcc (-X) X,
      HasDerivAt (fun t : ℝ => t * Real.log (Real.sqrt (t ^ 2 + b ^ 2))
          + b * Real.arctan (t / b) - t)
        (Real.log (Real.sqrt (x ^ 2 + b ^ 2))) x := by
    intro x hx
    exact deep_log_antideriv b hb x
  have hcont : Continuous (fun x : ℝ => Real.log (Real.sqrt (x ^ 2 + b ^ 2))) := by
    refine Continuous.log ?_ ?_
    · exact Real.continuous_sqrt.comp
        (by fun_prop : Continuous (fun x : ℝ => x ^ 2 + b ^ 2))
    · intro x
      exact ne_of_gt (Real.sqrt_pos.2 (by nlinarith [sq_nonneg x, sq_pos_of_pos hb]))
  have hint : IntervalIntegrable (fun x : ℝ => Real.log (Real.sqrt (x ^ 2 + b ^ 2)))
      MeasureTheory.volume (-X) X := Continuous.intervalIntegrable hcont (-X) X
  have hF : ∫ x in -X..X, Real.log (Real.sqrt (x ^ 2 + b ^ 2))
      = (X * Real.log (Real.sqrt (X ^ 2 + b ^ 2))
          + b * Real.arctan (X / b) - X)
        - ((-X) * Real.log (Real.sqrt ((-X) ^ 2 + b ^ 2))
          + b * Real.arctan ((-X) / b) - (-X)) := by
    exact intervalIntegral.integral_eq_sub_of_hasDerivAt hder hint
  have hneg : (-X) ^ 2 = X ^ 2 := by ring
  have hneg2 : Real.sqrt ((-X) ^ 2 + b ^ 2) = Real.sqrt (X ^ 2 + b ^ 2) := by
    rw [hneg]
  have harct_neg : Real.arctan ((-X) / b) = -Real.arctan (X / b) := by
    rw [show (-X) / b = -(X / b) by ring]
    exact Real.arctan_neg (X / b)
  rw [hneg2, harct_neg] at hF
  nlinarith

-- ============================================================
-- examples exercising the tactics as required by the build house rules
-- ============================================================
example (x : ℝ) : (1 - (x + x)) ^ 2 * (1 + 2 * x) - (1 - 2 * x)
    = 8 * x ^ 3 - 4 * x ^ 2 := by
  ring

example (u v : ℝ) (hu : u < 0) (hv : v < 0) : 0 < -(u + v) := by
  nlinarith

example (x : ℝ) (hx : 1 / 100 ≤ x) (hx2 : x ≤ 1 / 100) : x = 1 / 100 := by
  linarith

example (a b : ℝ) : ∫ x in a..b, (2 : ℝ) = 2 * (b - a) := by
  simp [intervalIntegral.integral_const, smul_eq_mul, mul_comm]

example (m X b : ℝ) (hm : 0 < m) (hX : 0 < X) (hb : 0 < b) :
    ∫ x in -X..X, (2 * m / Real.sqrt (x ^ 2 + b ^ 2))
      = 2 * m * Real.log ((X + Real.sqrt (X ^ 2 + b ^ 2)) /
          (Real.sqrt (X ^ 2 + b ^ 2) - X)) := by
  exact newton_delay_closed m X b hm hX hb

example (X b : ℝ) (hX : 0 < X) (hb : 0 < b) :
    ∫ x in -X..X, Real.log (Real.sqrt (x ^ 2 + b ^ 2))
      = 2 * X * Real.log (Real.sqrt (X ^ 2 + b ^ 2))
        + 2 * b * Real.arctan (X / b) - 2 * X := by
  exact deep_log_integral X b hX hb

example (u v : ℝ) :
    (1 - (u + v)) ^ 2 * (1 + 2 * u) - (1 - 2 * v)
      = (u + v) ^ 2 + 2 * u * (u + v) ^ 2 - 4 * u * (u + v) := by
  ring

example (u v : ℝ) (hu1 : -(1 / 100 : ℝ) ≤ u) (hu2 : u ≤ 1 / 100)
    (hv1 : -(1 / 100 : ℝ) ≤ v) (hv2 : v ≤ 1 / 100) :
    (1 - (u + v)) ^ 2 * (1 + 2 * u) - (1 - 2 * v) ≤ 151 / 125000 := by
  exact (linear_remainder_bound u v hu1 hu2 hv1 hv2).1

example (b : ℝ) (hb : 0 < b) (x : ℝ) :
    HasDerivAt (fun t : ℝ => Real.log (t + Real.sqrt (t ^ 2 + b ^ 2)))
      (1 / Real.sqrt (x ^ 2 + b ^ 2)) x := by
  exact newton_antideriv b hb x

example (b : ℝ) (hb : 0 < b) (x : ℝ) :
    HasDerivAt (fun t : ℝ => t * Real.log (Real.sqrt (t ^ 2 + b ^ 2))
        + b * Real.arctan (t / b) - t)
      (Real.log (Real.sqrt (x ^ 2 + b ^ 2))) x := by
  exact deep_log_antideriv b hb x

-- ============================================================
-- axioms
-- ============================================================
#print axioms linear_remainder
#print axioms linear_remainder_bound
#print axioms delay_sign
#print axioms endpoint_shift
#print axioms slip_shift
#print axioms slip_changes_delay
#print axioms newton_antideriv
#print axioms newton_delay_closed
#print axioms point_mass_delay
#print axioms deep_log_antideriv
#print axioms deep_log_integral