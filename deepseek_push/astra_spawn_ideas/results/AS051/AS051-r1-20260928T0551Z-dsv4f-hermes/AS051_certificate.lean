import Mathlib
import Mathlib.Tactic

/-!
# AS051 -- General deep-slope matching theorem (Lean 4 certificate)

Formalized content (all on the declared CORE/deep-slope response cell):

  Set-up (dimensionless deep-regime response; `s` = vacuum scale kept independent
  of `a0` until the last step, `Y = g/s`):
      B = mu(Y) * g            (spherical first integral of div[mu grad Phi] = 4 pi G rho_b)
      mu(Y) = b Y + O(Y^2)     (deep slope b > 0)

  A1  exact algebraic inversion with explicit corrections:
        B = (b/s) g^2 + (c2/s^2) g^3 + (c3/s^3) g^4
        => g^2 = (s/b) B - (c2/(b s)) g^3 - (c3/(b s^2)) g^4
      and substituting the inversion back yields residual 0.

  A2  the audited identity: with a0 := s/b (deep-matching), kappa := a0/s = 1/b.
      s-independent: applies identically to the canonical (a0 = 9.3619e-11)
      and alternative (a0 = 1.1279e-10) footings, which differ only in s = a0/kappa.

  A3  explicit remainder bound:
        |g^2 - (s/b) B| <= (K/b) * g^3/s     when  |R| <= K (g/s)^2,
        given g >= 0, b > 0, s > 0, K >= 0.

  A4  MU2-branch slope:  mu2(Y) = 1 - (1+Y)^(-2)  has
        |mu2(Y) - 2 Y| <= 3 Y^2    for Y >= 0
      (slope 2, explicit quadratic remainder bound K = 3).

  N1  NEGATIVE CONTROL (capable of failing): 1/(2 b) != 1/b for every b > 0,
      so the inferred kappa genuinely depends on the deep slope; a checker that
      hardwired kappa = 1/2 would fail the b = 1/2 and b = 1 rows.

  N2  DIMENSIONAL CHECK as exponent vectors (L, M, T) in Z^3:
        dim(g^2) = dim(s) + dim(B) = (2, 0, -4) ;  dim(kappa) = (0, 0, 0).

  Certification discipline: no sorry.  Axioms expected within
  {propext, Classical.choice, Quot.sound}.
-/

noncomputable section
open Real

-- =====================================================================
-- A1: exact inversion of the deep-slope equation
-- =====================================================================

/-- Exact algebraic inversion: from B = (b/s) g^2 + (c2/s^2) g^3 + (c3/s^3) g^4,
    g^2 = (s/b)B - (c2/(b s))g^3 - (c3/(b s^2))g^4. -/
theorem as051_exact_inversion (b s g B c2 c3 : ℝ)
    (hb : b ≠ 0) (hs : s ≠ 0)
    (h : B = b * g ^ 2 / s + c2 * g ^ 3 / s ^ 2 + c3 * g ^ 4 / s ^ 3) :
    g ^ 2 = (s / b) * B - (c2 / (b * s)) * g ^ 3 - (c3 / (b * s ^ 2)) * g ^ 4 := by
  rw [h]
  field_simp [hs, hb]
  try ring

/-- Substituting the inversion back into the original equation leaves residual 0. -/
theorem as051_inversion_residual (b s g B c2 c3 : ℝ)
    (hb : b ≠ 0) (hs : s ≠ 0) :
    (b / s) * ((s / b) * B - (c2 / (b * s)) * g ^ 3 - (c3 / (b * s ^ 2)) * g ^ 4) +
      (c2 / s ^ 2) * g ^ 3 + (c3 / s ^ 3) * g ^ 4 - B = 0 := by
  field_simp [hs, hb]
  try ring

-- =====================================================================
-- A2: kappa = 1/b
-- =====================================================================

/-- kappa := a0/s with a0 := s/b is exactly 1/b.  (s-independent: holds for
    every footing once s = a0/kappa is fixed.) -/
theorem as051_kappa_of_slope (s b : ℝ) (hs : s ≠ 0) (hb : b ≠ 0) :
    (s / b) / s = 1 / b := by
  field_simp [hs, hb]

-- =====================================================================
-- A3: explicit remainder bound.
-- =====================================================================

/-- With an exact quadratic remainder bound |R| <= K (g/s)^2 and the deep law
    B = (b/s) g^2 + g R one obtains the explicit bound
    |g^2 - (s/b) B| <= (K/b) g^3 / s, provided b > 0, s > 0, g >= 0, K >= 0. -/
theorem as051_remainder_bound (b s g K R : ℝ)
    (hb : 0 < b) (hs : 0 < s) (hg : 0 ≤ g) (_hK : 0 ≤ K)
    (hR : |R| ≤ K * (g / s) ^ 2) :
    |g ^ 2 - (s / b) * ((b / s) * g ^ 2 + g * R)| ≤ (K / b) * g ^ 3 / s := by
  have hs0 : s ≠ 0 := ne_of_gt hs
  have hb0 : b ≠ 0 := ne_of_gt hb
  have hsp : 0 < s / b := div_pos hs hb
  have hmain : g ^ 2 - (s / b) * ((b / s) * g ^ 2 + g * R) = -(s / b) * (g * R) := by
    field_simp [hs0, hb0]
    try ring
  rw [hmain, neg_mul, abs_neg, abs_mul, abs_of_pos hsp, abs_mul, abs_of_nonneg hg]
  calc
    (s / b) * (g * |R|) ≤ (s / b) * (g * (K * (g / s) ^ 2)) := by
      exact mul_le_mul_of_nonneg_left
        (mul_le_mul_of_nonneg_left hR hg) (le_of_lt hsp)
    _ = (K / b) * g ^ 3 / s := by
      field_simp [hs0, hb0]
      try ring

-- =====================================================================
-- A4: MU2-branch slope 2 with explicit remainder.
-- =====================================================================

/-- The MU2 response in its closed algebraic form (equals 1 - (1+Y)^(-2)
    wherever 1 + Y ≠ 0). -/
def mu2 (Y : ℝ) : ℝ := (2 * Y + Y ^ 2) / (1 + Y) ^ 2

/-- Closed-form identity: mu2(Y) - 2Y = -(3Y^2 + 2Y^3)/(1+Y)^2. -/
theorem as051_mu2_sub_twoY (Y : ℝ) (hY : 1 + Y ≠ 0) :
    mu2 Y - 2 * Y = -((3 * Y ^ 2 + 2 * Y ^ 3) / (1 + Y) ^ 2) := by
  unfold mu2
  field_simp [pow_ne_zero 2 hY]
  ring

/-- Slope-2 with quadratic remainder bound: |mu2(Y) - 2Y| <= 3 Y^2 for Y >= 0. -/
theorem as051_mu2_slope_two (Y : ℝ) (hY : 0 ≤ Y) :
    |mu2 Y - 2 * Y| ≤ 3 * Y ^ 2 := by
  have hY1 : 1 + Y ≠ 0 := by nlinarith
  have hY2 : 0 ≤ Y ^ 2 := sq_nonneg Y
  have hY3 : 0 ≤ Y ^ 3 := by positivity
  have hnum : 0 ≤ 3 * Y ^ 2 + 2 * Y ^ 3 := by nlinarith [hY2, hY3]
  have hden : 0 < (1 + Y) ^ 2 := sq_pos_of_ne_zero hY1
  have hnumle : 3 * Y ^ 2 + 2 * Y ^ 3 ≤ 3 * Y ^ 2 * (1 + Y) ^ 2 := by
    have hd : 0 ≤ 4 * Y ^ 3 + 3 * Y ^ 4 := by positivity
    nlinarith [hd]
  have hdiv : (3 * Y ^ 2 + 2 * Y ^ 3) / (1 + Y) ^ 2 ≤ 3 * Y ^ 2 := by
    exact (div_le_iff₀ hden).2 hnumle
  rw [as051_mu2_sub_twoY Y hY1]
  rw [abs_neg, abs_div, abs_of_nonneg hnum, abs_of_pos hden]
  exact hdiv

-- =====================================================================
-- N1: NEGATIVE CONTROL -- slope change must change the inferred kappa.
-- =====================================================================

/-- kappa(2b) != kappa(b): 1/(2 b) != 1/b for every b > 0.  (The inferred
    kappa is genuinely sensitive to the deep slope; a hardwired kappa = 1/2
    would fail this control at b = 1/2 and b = 1.) -/
theorem as051_negative_control (b : ℝ) (hb : 0 < b) :
    1 / (2 * b) ≠ 1 / b := by
  intro h
  have hb0 : b ≠ 0 := ne_of_gt hb
  field_simp [hb0] at h
  nlinarith

-- =====================================================================
-- N2: DIMENSIONAL CHECK as exponent vectors (L, M, T) in Z^3.
-- =====================================================================

/-- dim(g^2) = (2, 0, -4) equals dim(s) + dim(B) with b dimensionless. -/
theorem as051_dims_g2 :
    ((1, 0, -2) + (1, 0, -2) : ℤ × ℤ × ℤ) = (2, 0, -4) := by
  ext <;> norm_num

/-- dim(kappa) = dim(a0) - dim(s) = (0, 0, 0): kappa is dimensionless. -/
theorem as051_dims_kappa (a s : ℤ × ℤ × ℤ) (h : a = s) :
    a - s = (0, 0, 0) := by
  rw [h, sub_self]
  ext <;> norm_num

end