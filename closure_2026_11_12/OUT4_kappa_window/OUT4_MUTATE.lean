/-
OUT-4 (KAPPA WINDOW) MUTATE -- the FALSE TWIN.

This file asserts the claim the lane rejects:

    "T* DERIVES kappa = 1/2."

It must NOT compile.  Each of the four false statements below is the direct negation (or a
strict contradiction) of a theorem proved in OUT4.lean:

  F1  claims  rSchwBall / lamL = 1            -- i.e. lambda_L IS its own Schwarzschild radius,
                                                 so c^2/(2 lambda_L) IS a surface gravity.
                                                 OUT4 proves the ratio is 8*pi/3 = 8.3776.
  F2  claims  (lamL)^2 <= 3/Lambda            -- i.e. lambda_L lies inside the horizon bound,
                                                 so a horizon can sit there.
                                                 OUT4 proves 3/Lambda < (lamL)^2.
  F3  claims  T* holds at kappa = 1/3         -- i.e. T* is compatible with some other kappa,
                                                 so it is an extra law and not a restatement.
                                                 OUT4 proves T* <-> kappa = 1/2.
  F4  claims  kappa is G_lambda-invariant     -- i.e. kappa does not carry the scaling weight,
                                                 so the flat direction does not exist.
                                                 OUT4 proves kappa(lam a0) = lam kappa(a0).

The expected result is a non-zero exit with elaboration errors.  Nothing in this file is a
theorem of the lane; it exists only so that the rejection is demonstrated, not asserted.
-/

import Mathlib

noncomputable section

namespace Out4Mutate

open Real

def kappa (a0 c G rho : ℝ) : ℝ := a0 / (c * sqrt (G * rho))
def lamL (c G rho : ℝ) : ℝ := c / sqrt (G * rho)
def rSchwBall (G rho R c : ℝ) : ℝ := 2 * G * ((4 * Real.pi / 3) * rho * R ^ 3) / c ^ 2

lemma sqrt_pos_of_pos {G rho : ℝ} (hG : 0 < G) (hrho : 0 < rho) :
    0 < sqrt (G * rho) := by exact sqrt_pos.2 (mul_pos hG hrho)

-- F1 (FALSE): lambda_L is its own Schwarzschild radius, so c^2/(2 lambda_L) is a surface gravity.
theorem F1_lambdaL_is_its_own_horizon {G rho c : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0) :
    rSchwBall G rho (lamL c G rho) c / lamL c G rho = 1 := by
  unfold rSchwBall lamL
  have hsq : (sqrt (G * rho)) ^ 2 = G * rho := by
    rw [sq_sqrt (le_of_lt (mul_pos hG hrho))]
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  field_simp [hc, hs]
  ring_nf
  nlinarith

-- F2 (FALSE): the Jeans length lies within the horizon bound, so a horizon can sit there.
theorem F2_lambdaL_within_horizon_bound {c G rho Lam : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : 0 < c)
    (hLam_def : Lam = 8 * Real.pi * G * rho / c ^ 2) :
    (lamL c G rho) ^ 2 ≤ 3 / Lam := by
  rw [hLam_def]
  unfold lamL
  have hsq : (sqrt (G * rho)) ^ 2 = G * rho := by
    rw [sq_sqrt (le_of_lt (mul_pos hG hrho))]
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  have hne : 8 * Real.pi * G * rho / c ^ 2 ≠ 0 := by positivity
  field_simp [hne, ne_of_gt hc, hs]
  ring_nf
  nlinarith [Real.pi_gt_three]

-- F3 (FALSE): T* is an independent law, compatible with kappa = 1/3 as well as 1/2.
theorem F3_Tstar_compatible_with_one_third {a0 c G rho : ℝ}
    (hc : c ≠ 0) (hG : 0 < G) (hrho : 0 < rho)
    (hT : a0 = c ^ 2 / (2 * lamL c G rho)) :
    kappa a0 c G rho = 1 / 3 := by
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  unfold kappa lamL at *
  field_simp [hc, hs] at hT ⊢
  ring_nf at hT ⊢
  nlinarith

-- F4 (FALSE): kappa is invariant under the scaling, so it is not a flat direction.
theorem F4_kappa_is_invariant {a0 c G rho lam : ℝ} (hlam : lam ≠ 0) :
    kappa (lam * a0) c G rho = kappa a0 c G rho := by
  unfold kappa
  ring_nf
  nlinarith

end Out4Mutate

end
