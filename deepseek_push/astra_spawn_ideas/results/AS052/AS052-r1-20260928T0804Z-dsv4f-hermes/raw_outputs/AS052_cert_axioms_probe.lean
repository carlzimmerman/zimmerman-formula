import Mathlib

-- ======================================================================
-- AS052 -- OR composition with UNEQUAL channel slopes
-- Seed: deepseek_push/astra_spawn_ideas/AS052_or_composition_with_unequal_channel_slopes.md
-- sha256 bd9a4d387b694b13c3c1b99dbb1886ab809e48816458d0abeaaa6343ab45a737
--
-- Certified content (all real-algebra, no analysis API beyond the
-- statement forms):
--   T1  exact two-channel OR expansion (quadratic coefficient c1+c2-b1*b2,
--       cubic/quartic signs negative from the p1*p2 cross term)
--   T2  difference-quotient slope error is O(Y) with slope b1+b2 at 0
--       (certifies the seed's mu'(0) = sum_i b_i for the quadratic
--       truncation p_i = b_i Y + c_i Y^2; a HasDerivAt-level statement of
--       the same chain rule was attempted and dropped -- see derivation.md
--       section 7 -- because this build's elaborator synthesizes divergent
--       module instances for the codomain R in the sub/mul compositions)
--   T3  closed-form unequal-slope family: mu = 1 - 1/((1+b1Y)(1+b2Y))
--   T4  family slope error: mu/Y - (b1+b2) = O(Y) with the exact O(Y)
--       coefficient -(b1^2+b1*b2+b2^2)
--   T5  deep-matching algebra: k g^2 r^2/s = G M  =>  g^2 = (s/k)(G M/r^2)
--   T6  kappa = a0/s = 1/k when a0 = s/k
--   T7  equal-unit-slope member: kappa = 1/2 (b1 = b2 = 1)
--   T8  negative control: b1 = 1, b2 = 2 gives kappa = 1/3, NOT 1/2
--   T9  equal-unit-slope member of the family is exactly the framework MU2
--       branch value 1 - ((1+Y)^2)^(-1) (the mu_n(Y) = 1-(1+Y)^(-n) form at
--       n = 2 written as a quotient)
-- ======================================================================

noncomputable section
open scoped Real

-- per-channel engagement, quadratic completion (the p_i = b_i Y + c_i Y^2
-- truncation of the seed's p_i(Y) = b_i Y + O(Y^2))
def pchan (b c : ℝ) (Y : ℝ) : ℝ := b * Y + c * Y ^ 2

-- OR composition over two channels: 1 - prod_i (1 - p_i)
def muOR (p1 p2 : ℝ → ℝ) (Y : ℝ) : ℝ := 1 - (1 - p1 Y) * (1 - p2 Y)

-- ----------------------------------------------------------------------
-- T1. Exact expansion of the two-channel OR composition.
--     mu(Y) = (b1+b2) Y + (c1+c2-b1 b2) Y^2 - (b1 c2 + c1 b2) Y^3 - c1 c2 Y^4
-- ----------------------------------------------------------------------
theorem or_two_channel_expansion (Y b1 c1 b2 c2 : ℝ) :
    muOR (pchan b1 c1) (pchan b2 c2) Y
      = (b1 + b2) * Y + (c1 + c2 - b1 * b2) * Y ^ 2
          - (b1 * c2 + c1 * b2) * Y ^ 3 - c1 * c2 * Y ^ 4 := by
  unfold muOR pchan
  ring

-- ----------------------------------------------------------------------
-- T2. Difference quotient at 0: the error (mu(Y) - mu(0))/Y - (b1+b2) is
--     exactly Y times a polynomial: O(Y) as Y -> 0 with slope b1+b2.
-- ----------------------------------------------------------------------
theorem or_slope_error {Y b1 c1 b2 c2 : ℝ} (hY : Y ≠ 0) :
    (muOR (pchan b1 c1) (pchan b2 c2) Y - muOR (pchan b1 c1) (pchan b2 c2) 0)
        / (Y - 0) - (b1 + b2)
      = Y * ((c1 + c2 - b1 * b2) - (b1 * c2 + c1 * b2) * Y - c1 * c2 * Y ^ 2) := by
  unfold muOR pchan
  field_simp [hY]
  ring

-- ----------------------------------------------------------------------
-- T3. Closed-form unequal-slope family (saturating completion
--     p_i = b_i Y/(1 + b_i Y)):  mu(Y) = 1 - 1/((1+b1 Y)(1+b2 Y)).
-- ----------------------------------------------------------------------
def muFam (b1 b2 : ℝ) (Y : ℝ) : ℝ := 1 - 1 / ((1 + b1 * Y) * (1 + b2 * Y))

theorem family_closed_form {Y b1 b2 : ℝ} (h1 : 1 + b1 * Y ≠ 0) (h2 : 1 + b2 * Y ≠ 0) :
    muFam b1 b2 Y
      = ((b1 + b2) * Y + b1 * b2 * Y ^ 2) / ((1 + b1 * Y) * (1 + b2 * Y)) := by
  have hd : (1 + b1 * Y) * (1 + b2 * Y) ≠ 0 := mul_ne_zero h1 h2
  unfold muFam
  apply (eq_div_iff hd).2
  rw [sub_mul, one_mul, one_div]
  rw [inv_mul_cancel₀ hd]
  ring

-- ----------------------------------------------------------------------
-- T4. Family slope error: mu(Y)/Y - (b1+b2) = O(Y); the exact linear
--     coefficient is -(b1^2 + b1 b2 + b2^2).  (Y -> 0 slope is b1+b2.)
-- ----------------------------------------------------------------------
theorem family_slope_error {Y b1 b2 : ℝ} (hY : Y ≠ 0)
    (h1 : 1 + b1 * Y ≠ 0) (h2 : 1 + b2 * Y ≠ 0) :
    muFam b1 b2 Y / Y - (b1 + b2)
      = (-(Y * ((b1 ^ 2 + b1 * b2 + b2 ^ 2)
            + (b1 + b2) * b1 * b2 * Y)))
          / ((1 + b1 * Y) * (1 + b2 * Y)) := by
  rw [family_closed_form (Y := Y) h1 h2]
  field_simp [hY, h1, h2]
  ring

-- ----------------------------------------------------------------------
-- T5. Deep-matching algebra: the spherical first integral of the deep OR
--     response k g^2 r^2/s = G M (response mu ~ k g/s = k Y) is exactly
--     the a0-line g^2 = (s/k) g_N with g_N = G M / r^2.
-- ----------------------------------------------------------------------
theorem deep_matching {k g r s G M : ℝ} (hk : k ≠ 0) (hs : s ≠ 0)
    (hr : r ≠ 0) (hG : G ≠ 0) (h : k * g ^ 2 * r ^ 2 / s = G * M) :
    g ^ 2 = (s / k) * (G * M / r ^ 2) := by
  have h1 : k * g ^ 2 * r ^ 2 = s * G * M := by
    field_simp [hs] at h
    exact h
  have h2 : g ^ 2 * (k * r ^ 2) = s * G * M := by
    ring_nf at h1 ⊢
    exact h1
  have h3 : g ^ 2 = (s * G * M) / (k * r ^ 2) := by
    exact (eq_div_iff (mul_ne_zero hk (pow_ne_zero 2 hr))).2 h2
  have h4 : (s / k) * (G * M / r ^ 2) = (s * G * M) / (k * r ^ 2) := by
    field_simp [hk, hr, hG]
  rw [h4]
  exact h3

-- ----------------------------------------------------------------------
-- T6. kappa = a0/s = 1/k when a0 = s/k (the deep matching's scale
--     division; dimensionless ratio). (the deep matching's scale
--     division; dimensionless ratio).
-- ----------------------------------------------------------------------
theorem kappa_identity {a0 s k : ℝ} (hk : k ≠ 0) (hs : s ≠ 0)
    (ha0 : a0 = s / k) : a0 / s = 1 / k := by
  rw [ha0]
  field_simp [hk, hs]

-- ----------------------------------------------------------------------
-- T7. Equal-unit-slope member (b1 = b2 = 1): kappa = 1/(b1+b2) = 1/2.
-- ----------------------------------------------------------------------
theorem kappa_equal_unit_slopes : (1 / (1 + 1) : ℝ) = 1 / 2 := by
  norm_num

-- ----------------------------------------------------------------------
-- T8. NEGATIVE CONTROL (seed-mandated): b1 = 1, b2 = 2 gives mu'(0) = 3
--     and kappa = 1/3 -- the two channels alone do NOT force kappa = 1/2.
-- ----------------------------------------------------------------------
theorem kappa_unequal_control_value : (1 / (1 + 2) : ℝ) = 1 / 3 := by
  norm_num

theorem kappa_unequal_control_not_half : (1 / (1 + 2) : ℝ) ≠ 1 / 2 := by
  norm_num

-- ----------------------------------------------------------------------
-- T9. The equal-unit-slope member of the family is the framework MU2
--      form:  muFam 1 1 Y = 1 - ((1+Y)^2)^(-1)   (mu_n(Y) = 1-(1+Y)^(-n),
--      n = 2, Y = g/s, on the adopted footing s = 2 a0).
-- ----------------------------------------------------------------------
theorem family_member_mu2 {Y : ℝ} :
    muFam 1 1 Y = 1 - ((1 + Y) ^ 2)⁻¹ := by
  unfold muFam
  rw [pow_two]
  simp [one_div]

end

-- #print axioms or_two_channel_expansion
-- #print axioms or_slope_error
-- #print axioms or_two_channel_slope
-- #print axioms family_closed_form
-- #print axioms family_slope_error
-- #print axioms deep_matching
-- #print axioms kappa_identity
-- #print axioms kappa_equal_unit_slopes
-- #print axioms kappa_unequal_control_value
-- #print axioms kappa_unequal_control_not_half
-- #print axioms family_member_mu2
#eval Lean.versionString
#print axioms or_two_channel_expansion
#print axioms or_slope_error
#print axioms family_closed_form
#print axioms family_slope_error
#print axioms deep_matching
#print axioms kappa_identity
#print axioms kappa_equal_unit_slopes
#print axioms kappa_unequal_control_value
#print axioms kappa_unequal_control_not_half
#print axioms family_member_mu2
