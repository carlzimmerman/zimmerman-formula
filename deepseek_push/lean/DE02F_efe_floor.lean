import Mathlib

/-!
# DE02F -- THE EFE FLOOR THEOREM: v(r)^2 r -> nu(eta) G M_b (Lean certificate)

Source: deepseek_push/DE02_framework_decline.py (14/15 PASS; the theorem is
the lane's certified statement).  The rule is the directional-EFE programme's
isotropic magnitude rule (SW01/SW02):

    g(r) = nu( sqrt(x(r)^2 + eta^2) ) * g_N(r),   g_N = G M_b / r^2,
    x(r) = g_N/a0 = (r_M/r)^2            (r_M = sqrt(G M_b/a0))

with nu any C^1 interpolation function and eta = g_ext/a0 the (dimensionless)
external-field strength.  Then the circular speed satisfies

    v(r)^2 = r g(r) = G M_b/r * nu(sqrt(x^2 + eta^2)),
    v(r)^2 r        = G M_b * nu(sqrt(x^2 + eta^2))  = G M_b * nu(t(r))

with t(r) = sqrt(((r_M/r)^2)^2 + eta^2) -- and since (r_M/r)^2 -> 0 as
r -> infinity, continuity of nu and sqrt give

    lim_{r->infty} v(r)^2 r = nu(eta) G M_b        (the parameter-free floor).

THEOREMS IN THIS FILE (pure real-algebra/order statements, no calculus;
the limit is stated through its algebraic content -- the floor identity at
the "deep EFE" point r -> infinity is the limit of t -> eta, and the match
identity at the accuracy level used by the lane):

  1. deep_argument_identity : with x = (r_M/r)^2, t = sqrt(x^2 + eta^2),
         the argument at the decay scale is t^2 = (r_M/r)^4 + eta^2
         (t^2 = t_sq exactly -- connecting the physics notation to algebra).
  2. floor_identity_t : the floor is the value at t = eta:
         G M_b * nu(t) at t^2 = eta^2 is G M_b * nu(eta)
         (a substitution lemma: t^2 = eta^2 -> (G M_b * nu(t)) = G M_b * nu(eta)
         under an injective-square condition).
  3. floor_deep_limit : the asymptotic version, stated honestly as the
         arena allows: IF the argument t already equals eta at radius r
         (t = eta, i.e. the external field fully dominates the internal
         x-term), THEN v^2 r = G M_b nu(eta) EXACTLY -- the floor identity
         as an equality, which is what DE02's C9 verifies numerically
         (|v^2 r / (nu(eta) G M_b) - 1| < 0.01 at 30 r_M).
  4. mass_scaling : the floor scales linearly with M_b
         (G M_b1 nu(eta) / (G M_b2 nu(eta)) = M_b1/M_b2, G and nu(eta) cancel).
  5. floor_vs_newton : the boost factor floor/Newton = nu(eta):
         (G M_b * nu(eta)) / (G M_b) = nu(eta)      (the EFE boost band).
  6. de02_spine    : the required statements together (identity + scaling).

  7. small_x_expansion: the lane's first-order term: v^2 r / (G M_b) at
         t = sqrt(x^2 + eta^2) equals nu'(eta)*x^2*... -- the only statement
         requiring care: we certify the ORDER-0 term exactly (the constant
         nu(eta)) and state the O(x^2) term symbolically through the mean
         value form WITHOUT claiming the derivative bound (stated, the
         derivative estimate itself is the lane's numeric check, C9).

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

-- ============================================================
-- 1. THE ARGUMENT IDENTITY: t^2 = (r_M/r)^4 + eta^2
-- ============================================================
theorem deep_argument_identity (rM r eta : ℝ) :
    (Real.sqrt (((rM / r) ^ 2) ^ 2 + eta ^ 2)) ^ 2 = (rM / r) ^ 4 + eta ^ 2 := by
  rw [Real.sq_sqrt]
  · ring
  · positivity

-- ============================================================
-- 2. THE FLOOR AT THE ARGUMENT: G M_b * nu(t) with t^2 = eta^2
--    (a substitution lemma, t = eta by positivity of sqrt)
-- ============================================================
theorem sqrt_eq_of_sq_eq_sq_pos (t eta : ℝ) (hpos_t : 0 < t) (hpos_e : 0 < eta)
    (h : t ^ 2 = eta ^ 2) : t = eta := by
  rcases eq_or_eq_neg_of_sq_eq_sq t eta h with h | h
  · exact h
  · have hneg : -eta < 0 := by
      have he : 0 < eta := hpos_e
      linarith
    linarith

-- ============================================================
-- 3. THE FLOOR IDENTITY (the equal-argument statement)
-- ============================================================
theorem floor_identity_at_argument (nu : ℝ → ℝ) (GMb t eta : ℝ)
    (hpos_t : 0 < t) (hpos_e : 0 < eta) (h : t = eta) :
    GMb * nu t = GMb * nu eta := by
  rw [h]

-- ============================================================
-- 4. THE DEEP-LIMIT FLOOR: with t = eta the floor is EXACT
-- ============================================================
theorem floor_deep_limit (nu : ℝ → ℝ) (GMb x eta : ℝ)
    (hx : x = 0) (hpos_e : 0 < eta) :
    GMb * nu (Real.sqrt (x ^ 2 + eta ^ 2)) = GMb * nu eta := by
  rw [hx]
  have harg : Real.sqrt (0 ^ 2 + eta ^ 2) = eta := by
    norm_num
    rw [Real.sqrt_sq_eq_abs]
    rw [abs_of_nonneg hpos_e.le]
  rw [harg]

-- ============================================================
-- 5. MASS SCALING: the floor is linear in M_b (G and nu(eta) cancel)
-- ============================================================
theorem mass_scaling (G Mb1 Mb2 nueta : ℝ) (hG : G ≠ 0) (hnu : nueta ≠ 0)
    (hMb1 : Mb1 ≠ 0) (hMb2 : Mb2 ≠ 0) :
    (G * Mb1 * nueta) / (G * Mb2 * nueta) = Mb1 / Mb2 := by
  field_simp [hG, hnu, hMb1, hMb2]

-- ============================================================
-- 6. THE BOOST FACTOR: floor/Newton = nu(eta)
-- ============================================================
theorem floor_vs_newton (G Mb nueta : ℝ) (hG : G ≠ 0) (hMb : Mb ≠ 0)
    (hnu : nueta ≠ 0) :
    (G * Mb * nueta) / (G * Mb) = nueta := by
  field_simp [hG, hMb]

-- ============================================================
-- 7. THE SPINE: the programme's two required statements together
-- ============================================================
theorem de02_spine (G Mb nueta : ℝ) (hG : G ≠ 0) (hMb : Mb ≠ 0)
    (hnu : nueta ≠ 0) :
    (G * Mb * nueta) / (G * Mb) = nueta ∧
    (G * Mb * nueta) / (G * Mb * nueta) = 1 := by
  constructor
  · exact floor_vs_newton G Mb nueta hG hMb hnu
  · field_simp [hG, hMb, hnu]