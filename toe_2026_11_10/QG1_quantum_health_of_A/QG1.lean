/-
QG1 (gate T2 of TOE0): the algebraic identities that carry the verdict. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

1. Unitary gauge, scalar sector of the khronometric form
   (M^2/2) N sqrt h [(1-beta) K_ij K^ij - (1+lambda) K^2 + R3 + alpha a^2]:
   the shift B enters the kinetic term with coefficient (1-beta) - (1+lambda) = -(beta+lambda) on (d d B)^2.
   (A) has beta = lambda = 0, so B is a Lagrange multiplier and the BPS numerator (beta+lambda)(2-alpha) vanishes.
2. Newtonian reduction: omega^2 = G k^2 (b - a)/(a b); on Minkowski the charge G = n_d + D.P is 0, so omega^2 = 0.
3. The law with a renormalized Planck mass, mu_eff(u) = 1 - 1/((1+eps)(1+u)), differs from u/(1+u) by
   eps/((1+eps)(1+u)), and returns the law at eps = 0.
4. Longitudinal mixing: 1 - K m0 = 1 - 1/(1+u)^2 = u(2+u)/(1+u)^2 (vanishes at u = 0: alpha_a = 2).
-/
import Mathlib

theorem qg1_shift_coeff (β l : ℝ) : (1 - β) - (1 + l) = -(β + l) := by ring

theorem qg1_shift_multiplier_A : (1 - (0:ℝ)) - (1 + 0) = 0 := by norm_num

theorem qg1_bps_numerator_A (α : ℝ) : ((0:ℝ) + 0) * (2 - α) = 0 := by ring

theorem qg1_omega2_zero_charge (k a b : ℝ) : (0:ℝ) * k ^ 2 * (b - a) / (a * b) = 0 := by simp

theorem qg1_dmu (u ε : ℝ) (hu : 0 < 1 + u) (he : 0 < 1 + ε) :
    1 / (1 + u) - 1 / ((1 + ε) * (1 + u)) = ε / ((1 + ε) * (1 + u)) := by
  have h1 : (1 + u) ≠ 0 := ne_of_gt hu
  have h2 : (1 + ε) ≠ 0 := ne_of_gt he
  field_simp
  ring

theorem qg1_law_back (u : ℝ) (hu : 0 < 1 + u) : 1 - 1 / ((1 + 0) * (1 + u)) = u / (1 + u) := by
  have h1 : (1 + u) ≠ 0 := ne_of_gt hu
  field_simp
  ring

theorem qg1_one_minus_Km_par (u : ℝ) (hu : 0 < 1 + u) :
    1 - 1 / (1 + u) ^ 2 = u * (2 + u) / (1 + u) ^ 2 := by
  have h1 : (1 + u) ≠ 0 := ne_of_gt hu
  field_simp
  ring

theorem qg1_alpha2_at_zero : 1 - 1 / (1 + (0:ℝ)) ^ 2 = 0 := by norm_num
