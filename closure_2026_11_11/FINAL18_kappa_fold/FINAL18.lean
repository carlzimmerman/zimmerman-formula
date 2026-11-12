/-
FINAL-18 (KAPPA_B): the load-bearing algebra of the fold matching condition.

    (V)  a_0 = kappa c sqrt(G rho_Lambda)                    -- the definition of kappa
    (M)  M_ph(R_fold; a_0) = Q_fold                          -- cold-charge continuity at the fold
         M_ph = M_b X,  X = (sqrt(1+4x^2)-1)/2,  x = R_fold/r_M,  r_M = sqrt(G M_b/a_0)

Certified here:

  clock_cancel         : with the law force U(u) = a_0 u/(a_0-u) and u = G(M_x-M_bg)/r^2 the excess
                         (polarization) field, the clock's inward pull is -G M_bg/r^2 + u^2/(a_0-u):
                         the excess's own gravity is cancelled exactly and the remainder is second order.
  residual_quadratic   : U(u) - u = u^2/(a_0-u)                      (the a_0-dependence of infall)
  law_excess_relative  : (U(u)-u)/u = u/(a_0-u)                      (the small parameter)
  share_of_radius      : X >= 0 and X(1+X) = x^2  =>  X = (sqrt(1+4x^2)-1)/2      (FLD1's theorem)
  share_quad           : the share X(x) satisfies X(1+X) = x^2 exactly
  fold_match_solves    : (M) with X = q gives x^2 = q(1+q), i.e. a_0 = G M_b q(1+q)/R_fold^2  (exact)
  fold_match_exists    : for every q >= 0 there is an x^2 realising it
  share_strict_mono    : X is strictly increasing in x^2 (hence in a_0 at fixed R, M_b)
  fold_match_unique    : so (M) has AT MOST ONE solution -- if it has one, kappa is pinned
  kappa_scales         : under a_0 -> lambda a_0 at fixed rho_Lambda, kappa -> lambda kappa

SCOPE.  This file certifies ALGEBRA.  It does not certify that (M) is a law of nature, that the clock
is the cold component, or that the numerical values of R_fold and Q_fold are the ones the universe
realises; those are measured (FLD1) and graded (final18.out).
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace FINAL18

/-- G1. The clock's own excess does not gravitate. c = G/r^2, u = c*(M_x - M_bg). -/
theorem clock_cancel (c Mx Mbg a0 : ℝ) (h : a0 - c * (Mx - Mbg) ≠ 0) :
    -c * Mx + a0 * (c * (Mx - Mbg)) / (a0 - c * (Mx - Mbg))
      = -c * Mbg + (c * (Mx - Mbg)) ^ 2 / (a0 - c * (Mx - Mbg)) := by
  field_simp [h]
  ring

/-- G1. The law force differs from a pure cancellation by u^2/(a_0-u): second order in the excess. -/
theorem residual_quadratic (a0 u : ℝ) (hd : a0 - u ≠ 0) :
    a0 * u / (a0 - u) - u = u ^ 2 / (a0 - u) := by
  field_simp [hd]
  ring

/-- G1. The relative remainder: the small parameter of the fold's a_0-dependence. -/
theorem law_excess_relative (a0 u : ℝ) (hu : u ≠ 0) (hd : a0 - u ≠ 0) :
    (a0 * u / (a0 - u) - u) / u = u / (a0 - u) := by
  field_simp [hu, hd]
  ring

/-- KA-3. The non-negative root of X(1+X) = x^2 (FLD1's share_of_radius, restated). -/
theorem share_of_radius (X : ℝ) (hX : 0 ≤ X) :
    (-1 + Real.sqrt (1 + 4 * (X * (X + 1)))) / 2 = X := by
  have h : 1 + 4 * (X * (X + 1)) = (2 * X + 1) ^ 2 := by ring
  rw [h, Real.sqrt_sq (by linarith)]
  ring

/-- KA-3. The share X(x) = (sqrt(1+4x^2)-1)/2 satisfies X(1+X) = x^2 exactly. -/
theorem share_quad (x : ℝ) :
    ((-1 + Real.sqrt (1 + 4 * x ^ 2)) / 2) * (1 + ((-1 + Real.sqrt (1 + 4 * x ^ 2)) / 2)) = x ^ 2 := by
  have h0 : 0 ≤ 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
  set s := Real.sqrt (1 + 4 * x ^ 2) with hs
  have hs2 : s ^ 2 = 1 + 4 * x ^ 2 := by
    rw [hs, Real.sq_sqrt h0]
  nlinarith

/-- The fold matching condition (M) at X = q, inverted: x^2 = q(1+q).
    With x^2 = a_0 R^2/(G M_b) this is a_0 = G M_b q(1+q)/R^2, the lane's closed form. -/
theorem fold_match_solves (q x : ℝ) (h : (-1 + Real.sqrt (1 + 4 * x ^ 2)) / 2 = q) :
    x ^ 2 = q * (1 + q) := by
  have hs := share_quad x
  rw [h] at hs
  nlinarith

/-- Existence: every non-negative delivered share q is realised by some x^2 >= 0. -/
theorem fold_match_exists (q : ℝ) (hq : 0 ≤ q) :
    (-1 + Real.sqrt (1 + 4 * (q * (q + 1)))) / 2 = q := by
  have h : 1 + 4 * (q * (q + 1)) = (2 * q + 1) ^ 2 := by ring
  rw [h, Real.sqrt_sq (by linarith)]
  ring

/-- The share is strictly increasing in x^2 (hence in a_0 at fixed R, M_b). -/
theorem share_strict_mono (k0 k1 : ℝ) (h0 : 0 ≤ k0) (h01 : k0 < k1) :
    (-1 + Real.sqrt (1 + 4 * k0)) / 2 < (-1 + Real.sqrt (1 + 4 * k1)) / 2 := by
  have hs : Real.sqrt (1 + 4 * k0) < Real.sqrt (1 + 4 * k1) := Real.sqrt_lt_sqrt (by linarith)
  linarith

/-- Uniqueness: (M) has at most one solution. If a solution exists, kappa is pinned (not a flat
    direction). Together with fold_match_exists: exactly one. -/
theorem fold_match_unique (k0 k1 q : ℝ) (h0 : 0 ≤ k0) (h1 : 0 ≤ k1)
    (e0 : (-1 + Real.sqrt (1 + 4 * k0)) / 2 = q)
    (e1 : (-1 + Real.sqrt (1 + 4 * k1)) / 2 = q) : k0 = k1 := by
  rcases lt_trichotomy k0 k1 with hlt | heq | hgt
  · have hm := share_strict_mono k0 k1 h0 hlt
    rw [e0, e1] at hm
    linarith
  · exact heq
  · have hm := share_strict_mono k1 k0 h1 hgt
    rw [e0, e1] at hm
    linarith

/-- (V): at fixed rho_Lambda, kappa is proportional to a_0. -/
theorem kappa_scales (a0 lam croot : ℝ) (hc : croot ≠ 0) :
    (lam * a0) / croot = lam * (a0 / croot) := by
  field_simp [hc]
  ring

end FINAL18
