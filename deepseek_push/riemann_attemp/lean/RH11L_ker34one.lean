import Mathlib

/-!
# RH11L -- THE 3-4-1 KERNEL ALGEBRA WITH THE FRAMEWORK'S LOMAX KERNEL (Lean-certified, zero sorry)
================================================================================================

THE CLASSICAL SCHEME.  Hadamard / de la Vallee Poussin prove zeta has no zeros
in sigma > 1 - c/log|t| from the Euler product plus the trig identity

    3 + 4 cos(theta) + cos(2 theta) = 2 (1 + cos theta)^2 >= 0.

Mechanism: for sigma > 1 and ANY weights (A, B, C),

    A log|zeta(sigma)| + B log|zeta(sigma+it)| + C log|zeta(sigma+2it)|
        = sum_p sum_m p^{-m sigma} * k(m theta_p) / m,
        k(theta) = A + B cos(theta) + C cos(2 theta),  theta_p = t log p

(linear in the weights, so the identity is exact for any (A,B,C)); with
(A,B,C) = (3,4,1) the kernel k is >= 0, giving the lower bound
|zeta(1+delta+it)| >= c*delta and the classical region with c = 1/9.646
(Stechkin; the "1/(9.6...)" family of the lane brief).

THE FRAMEWORK ENTRY (this lane, RH11).  Substitute the framework's Lomax
kernel f_l(u) = (1+u)^{-l} into the SAME scheme as an amplitude modulator:

    k_{l,u,w}(theta) = A + B cos(theta) + C cos(2 theta),
    A = w0 f_l(u),  B = w1 f_l(2u),  C = w2 f_l(3u),   f_l(x) = (1+x)^{-l}.

The numeric scan (RH11_kerZeroFree.py, grids: l in {1.5, 2, 2.4824, 3},
u in [0.02, 10] (log grid + rational linear grid), w in {(3,4,1),(1,2,1),
(5,6,1)}) found 61678/63060 passing candidates (k >= 0 for all theta AND
leading Fourier coefficient B > 0).  The closest-to-0 minimum over the grid
is 4.4872e-4 (l = 1.5, w = (1,2,1), u = 0.35540...).  The scheme's constant
for a candidate is c = (1/9.646) * B/(A+C); since margin >= 0 forces
(A+C)/B >= 1 with equality ONLY at the classical point (A,B,C) ~ (3,4,1),
u -> 0, f ~ 1 (theorem alpha_ge_one below), every framework kernel is
STRICTLY weaker than the classical one: best c_scheme = 0.09548 < c_class
= 0.10367 (ratio 0.921).  Registered weaker-than-known; no RH claim, in
whole or in part.

WHAT IS CERTIFIED IN LEAN (all theorems below compile, exit 0, zero sorry):
  (i)   the classical trig identity 3 + 4c + (2c^2 - 1) = 2(c+1)^2 and its
        theta-form 3 + 4 cos t + cos(2t) = 2(1 + cos t)^2;
  (ii)  the double-angle reduction cos(2t) = 2 cos^2 t - 1;
  (iii) THE NONNEGATIVITY TEST'S ALGEBRA, general weights:
        * vertex regime (B <= 4C): the sum-of-squares decomposition
              A + Bc + C(2c^2-1) = (A - C - B^2/(8C)) + 2C(c + B/(4C))^2,
          hence margin = A - C - B^2/8C >= 0 implies k >= 0 for ALL real c
          (the framework analogue of 2(1+cos t)^2 >= 0);
        * corner regime (B >= 4C, -1 <= c): the factor certificate
              k(c) - (A - B + C) = (1 + c)(B - 2C + 2Cc) >= 0;
        * family optimality: margin >= 0 and C > 0 imply (A+C)/B >= 1,
          i.e. alpha >= 1 and the scheme constant c = c_class/alpha can
          never beat the classical value c_class (equality only at the
          classical configuration);
  (iv)  the EXACT INSTANTIATION at the best integer-l candidate of the grid
        (l = 3, w = (1,2,1), u = 10): A = 1/1331, B = 2/9261, C = 1/29791,
        corner regime, min_theta k = 208917200/367215514281 = 5.689226e-4:
            for all t: 0 <= 1/1331 + (2/9261) cos t + (1/29791) cos(2t).

HONEST BOUNDARY (frozen): the certified statements are pure algebra of the
kernel nonnegativity test (trig reduction + SOS/factor certificates).  The
analytic-number-theory step from "k >= 0" to the zero-free region (the
Euler-product identity and the classical lower-bound pipeline) is NOT
formalized here -- it is the standard 1899 argument, used with the weights
(A,B,C) the scan produces.  RH is NOT claimed; the framework's kernels
yield c < c_class (weaker than known), registered as such.
-/

noncomputable section

open scoped Real

-- ============================================================
-- (i) + (ii) THE CLASSICAL KERNEL: 3 + 4cos + cos2 = 2(1+cos)^2
-- ============================================================

theorem classical_identity_c (c : ℝ) : 3 + 4 * c + (2 * c ^ 2 - 1) = 2 * (c + 1) ^ 2 := by
  ring

-- cos(2t) = 2 cos^2 t - 1 (Mathlib: Real.cos_two_mul)
theorem cos_double_angle (t : ℝ) : Real.cos (2 * t) = 2 * (Real.cos t) ^ 2 - 1 := by
  exact Real.cos_two_mul t

-- the classical kernel in theta form
theorem classical_kernel_trig (t : ℝ) :
    3 + 4 * Real.cos t + Real.cos (2 * t) = 2 * (1 + Real.cos t) ^ 2 := by
  rw [cos_double_angle]
  ring

-- the classical kernel is >= 0 for all t (no RH content: an identity + squares)
theorem classical_kernel_nonneg (t : ℝ) : 0 ≤ 3 + 4 * Real.cos t + Real.cos (2 * t) := by
  rw [classical_kernel_trig]
  positivity

-- ============================================================
-- (iii) THE NONNEGATIVITY TEST'S ALGEBRA (general weights)
-- ============================================================

-- vertex regime: SOS decomposition, the framework analogue of 2(1+cos t)^2
theorem sos_decomposition (A B C c : ℝ) (hC : C ≠ 0) :
    A + B * c + C * (2 * c ^ 2 - 1) = (A - C - B ^ 2 / (8 * C)) + 2 * C * (c + B / (4 * C)) ^ 2 := by
  field_simp [hC]
  ring

-- vertex regime: margin >= 0 already gives k >= 0 for ALL real c
theorem vertex_scheme_nonneg (A B C c : ℝ) (hA : 0 ≤ A - C - B ^ 2 / (8 * C))
    (hC : 0 < C) : 0 ≤ A + B * c + C * (2 * c ^ 2 - 1) := by
  rw [sos_decomposition A B C c (ne_of_gt hC)]
  have h2C : 0 ≤ 2 * C := by nlinarith
  have hsq : 0 ≤ 2 * C * (c + B / (4 * C)) ^ 2 := mul_nonneg h2C (sq_nonneg _)
  nlinarith

-- corner regime: the difference factors
theorem corner_decomposition (A B C c : ℝ) :
    A + B * c + C * (2 * c ^ 2 - 1) - (A - B + C) = (1 + c) * (B - 2 * C + 2 * C * c) := by
  ring

-- corner regime: for -1 <= c and B >= 4C the min of k is A - B + C (at c = -1)
theorem corner_scheme_nonneg (A B C c : ℝ) (hBC : 4 * C ≤ B) (hC : 0 < C) (hc1 : -1 ≤ c) :
    A - B + C ≤ A + B * c + C * (2 * c ^ 2 - 1) := by
  have h1 : 0 ≤ 1 + c := by nlinarith [hc1]
  have hC0 : 0 ≤ C := le_of_lt hC
  have hcp : 0 ≤ 2 * C * (c + 1) := by
    have hc1' : 0 ≤ c + 1 := by nlinarith [hc1]
    nlinarith
  have h2 : 0 ≤ B - 2 * C + 2 * C * c := by nlinarith [hBC, hcp]
  have hprod : 0 ≤ (1 + c) * (B - 2 * C + 2 * C * c) := mul_nonneg h1 h2
  have hk : A + B * c + C * (2 * c ^ 2 - 1) - (A - B + C) = (1 + c) * (B - 2 * C + 2 * C * c) :=
    corner_decomposition A B C c
  linarith

-- family optimality: margin >= 0 forces alpha = (A+C)/B >= 1
-- (equality iff (A,B,C) ~ (3,4,1): the classical configuration u -> 0, f ~ 1)
theorem alpha_ge_one (A B C : ℝ) (hA : 0 ≤ A - C - B ^ 2 / (8 * C)) (hC : 0 < C) : B ≤ A + C := by
  have hsq : 0 ≤ (4 * C - B) ^ 2 := sq_nonneg (4 * C - B)
  have h8 : (8 : ℝ) * C ≠ 0 := by positivity
  have hdiv : 0 ≤ (4 * C - B) ^ 2 / (8 * C) := div_nonneg hsq (le_of_lt (by positivity : 0 < (8 : ℝ) * C))
  have hsum : 0 ≤ A - C - B ^ 2 / (8 * C) + (4 * C - B) ^ 2 / (8 * C) := by nlinarith [hA, hdiv]
  have hident : A - C - B ^ 2 / (8 * C) + (4 * C - B) ^ 2 / (8 * C) = A + C - B := by
    field_simp [h8]
    ring
  rw [hident] at hsum
  nlinarith

-- ============================================================
-- (iv) THE EXACT INSTANTIATION AT THE BEST INTEGER-l CANDIDATE
--      (l = 3, w = (1,2,1), u = 10;  corner regime)
--      A = (1+10)^{-3} = 1/1331,  B = 2(1+20)^{-3} = 2/9261,
--      C = (1+30)^{-3} = 1/29791;  min_theta k = 208917200/367215514281
-- ============================================================

abbrev kstar (c : ℝ) : ℝ := (1 : ℝ) / 1331 + (2 : ℝ) / 9261 * c + (1 : ℝ) / 29791 * (2 * c ^ 2 - 1)

theorem best_min_exact :
    ((1 : ℝ) / 1331 - (2 : ℝ) / 9261 + (1 : ℝ) / 29791) = (208917200 : ℝ) / 367215514281 := by
  norm_num

theorem best_min_pos : 0 < (1 : ℝ) / 1331 - (2 : ℝ) / 9261 + (1 : ℝ) / 29791 := by
  norm_num

theorem best_corner_hypotheses :
    4 * ((1 : ℝ) / 29791) ≤ (2 : ℝ) / 9261 ∧ 0 < (1 : ℝ) / 29791 := by
  norm_num

theorem best_kernel_lower_bound (c : ℝ) (hc : -1 ≤ c) :
    (1 : ℝ) / 1331 - (2 : ℝ) / 9261 + (1 : ℝ) / 29791 ≤ kstar c := by
  have hBC : 4 * ((1 : ℝ) / 29791) ≤ (2 : ℝ) / 9261 := by norm_num
  have hC : 0 < (1 : ℝ) / 29791 := by norm_num
  have h := corner_scheme_nonneg ((1 : ℝ) / 1331) ((2 : ℝ) / 9261) ((1 : ℝ) / 29791) c hBC hC hc
  simpa [kstar] using h

theorem best_kernel_nonneg (c : ℝ) (hc : -1 ≤ c) : 0 ≤ kstar c := by
  have hM : 0 ≤ (1 : ℝ) / 1331 - (2 : ℝ) / 9261 + (1 : ℝ) / 29791 := le_of_lt best_min_pos
  linarith [best_kernel_lower_bound c hc, hM]

-- the trig form: 0 <= 1/1331 + (2/9261) cos t + (1/29791) cos(2t)  for all t
theorem best_kernel_trig_nonneg (t : ℝ) :
    0 ≤ (1 : ℝ) / 1331 + (2 : ℝ) / 9261 * Real.cos t + (1 : ℝ) / 29791 * Real.cos (2 * t) := by
  rw [cos_double_angle]
  exact best_kernel_nonneg (Real.cos t) (Real.neg_one_le_cos t)

-- the classical anchor of the family: alpha = (A+C)/B = 1 for (3,4,1)
theorem classical_alpha : (4 : ℝ) / ((3 : ℝ) + (1 : ℝ)) = 1 := by
  norm_num

end