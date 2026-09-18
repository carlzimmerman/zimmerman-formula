import Mathlib

/-!
# RH16-L -- THE ZETA'S RAR: THE PER-PAIR MODULUS ALGEBRA, Lean-certified (zero sorry)
=====================================================================================

THE STATEMENT (the framework reads RH through its own signature quadratic form):

With s = sigma + i t, u = sigma - 1/2, and a zero rho = beta + i gamma,
d = beta - 1/2, w = (t - gamma)^2, the modulus-squared of the completed
zeta's Hadamard factor for the SYMMETRIC PAIR  rho, 1-rho  is

    P_rho(u) = [(u-d)^2 + w] * [(u+d)^2 + w]

and its AXIS EXCESS (the zeta's "RAR" residual, the analogue of
g_obs^2 - g_bar^2 for |xi| instead of g) is

    P_rho(u) - P_rho(0) = u^2 * (u^2 + 2w - 2d^2).

THE CRITICAL FACT (what makes this THE equivalence): at t = gamma
(w = 0) the excess is  u^2 (u^2 - 2d^2), which is NEGATIVE for
0 < u < d*sqrt(2)  WHENEVER the zero is OFF-AXIS (d != 0); for an
ON-AXIS zero (d = 0) the excess is  u^2 (u^2 + 2w) >= 0  ALWAYS.
So per-pair:  all-on-axis  <->  excess >= 0 for all u, for every t.
The classical criterion (RH  <->  |xi(sigma+it)| non-decreasing in
sigma >= 1/2 for all t -- Titchmarsh's monotonicity theorem) is the
product over pairs of this per-pair fact.  This file certifies the
ALGEBRA: the factorization, the excess identity, and the sign flip.
The product/function convergence and the equivalence itself are the
classical theorem (cited in the lane .py), not reproved here.

THEOREMS:
  (1) pair_factor       : [(u-d)^2 + w] * [(u+d)^2 + w] = (u^2 + d^2 + w)^2 - 4*u^2*d^2
  (2) excess_identity   : the axis excess = u^2*(u^2 + 2w - 2d^2)
  (3) on_axis_nonneg    : d = 0 -> excess = u^2*(u^2 + 2w) >= 0  (w >= 0)
  (4) off_axis_flip     : w = 0, 0 < u < d -> excess < 0  (the RAR residual goes
                          negative exactly when a zero leaves the critical line)
  (5) ratio_below_one   : w = 0, 0 < u < d -> P_rho(u) < P_rho(0)
                          (the corresponding |xi|-factor ratio drops below 1)
-/

noncomputable section

open scoped Real

-- (1) the pair-factor square identity
theorem pair_factor (u d w : ℝ) :
    ((u - d) ^ 2 + w) * ((u + d) ^ 2 + w) = (u ^ 2 + d ^ 2 + w) ^ 2 - 4 * u ^ 2 * d ^ 2 := by
  ring

-- (2) the axis excess
theorem excess_identity (u d w : ℝ) :
    ((u - d) ^ 2 + w) * ((u + d) ^ 2 + w) - ((0 - d) ^ 2 + w) * ((0 + d) ^ 2 + w)
      = u ^ 2 * (u ^ 2 + 2 * w - 2 * d ^ 2) := by
  ring

-- (3) on-axis: nonnegative excess for all u, all w >= 0
theorem on_axis_nonneg (u w : ℝ) (hw : 0 ≤ w) :
    0 ≤ u ^ 2 * (u ^ 2 + 2 * w) := by
  have h1 : 0 ≤ u ^ 2 := sq_nonneg u
  have h2 : 0 ≤ u ^ 2 + 2 * w := by
    nlinarith [h1, hw]
  exact mul_nonneg h1 h2

-- (4) off-axis flip: w = 0 and 0 < u < d  ->  excess < 0
theorem off_axis_flip (u d : ℝ) (hu : 0 < u) (hd : u < d) :
    u ^ 2 * (u ^ 2 - 2 * d ^ 2) < 0 := by
  have hsq : u ^ 2 < d ^ 2 := by
    nlinarith [hu, hd]
  have h2 : u ^ 2 - 2 * d ^ 2 < 0 := by
    nlinarith [hsq, hu]
  have hpos : 0 < u ^ 2 := by
    exact sq_pos_of_pos hu
  exact mul_neg_of_pos_of_neg hpos h2

-- (5) the ratio drops below 1 exactly when a zero is off-axis
theorem ratio_below_one (u d : ℝ) (hu : 0 < u) (hd : u < d) :
    ((u - d) ^ 2 + 0) * ((u + d) ^ 2 + 0) < ((0 - d) ^ 2 + 0) * ((0 + d) ^ 2 + 0) := by
  have hfact : ((u - d) ^ 2 + 0) * ((u + d) ^ 2 + 0)
                 - ((0 - d) ^ 2 + 0) * ((0 + d) ^ 2 + 0)
               = u ^ 2 * (u ^ 2 - 2 * d ^ 2) := by
    rw [excess_identity u d 0]
    ring
  have hflip : u ^ 2 * (u ^ 2 - 2 * d ^ 2) < 0 := off_axis_flip u d hu hd
  have hneg : ((u - d) ^ 2 + 0) * ((u + d) ^ 2 + 0)
                - ((0 - d) ^ 2 + 0) * ((0 + d) ^ 2 + 0) < 0 := by
    rw [hfact]
    exact hflip
  exact sub_neg.mp hneg

end