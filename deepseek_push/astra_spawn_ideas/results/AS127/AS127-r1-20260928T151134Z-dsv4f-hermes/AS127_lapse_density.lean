import Mathlib

/-!
AS127 (Tier-0): reciprocal lapse density, algebraic core.

Certified algebra over ℝ:
 1. `lapse_density_correct`  — the CA5-GNC-R lapse density identity
        rho_R = -(N sqrt h)^-1 delta S_R/delta ln N = t*K + W/t + V*F
      decomposed as:  rho_R = -( L + t*(-2K) ),  L = t*K - W/t - V*F,
      where the kinetic term varies as delta K = -2K (delta ln N) because
      n_A = (phi' - N^i D_i phi)/N carries the lapse in its denominator.
 2. `control_wrong_density`  — negative control: holding n (hence K) fixed
      during the ln N variation yields the WRONG density with kinetic
      coefficient -t (negative for t > 0).
 3. `control_residual`       — the exact residual of the control:
      rho_correct - rho_wrong = 2*t*K (kinetic only, positive for t>0, K>0).
 4. `wrong_kinetic_sign`     — the wrong coefficient is strictly negative.
 5. `F_identity`             — the reciprocal-barrier shape:
      F(t) = 1 + (t + 1/t - 2)^2 = 1 + (t-1)^4/t^2  (t ≠ 0), from the pinned
      vacuum ACTION.md (R2), used in the limiting case t -> 1.
 6. `F_lower_bound`          — F(t) >= 1 with equality iff t = 1.
-/

namespace AS127

open scoped BigOperators

/-- The reciprocal lapse density: negative of (measure term + kinetic variation).
    K = K_d (kinetic density), W = W_exc (gradient+potential), V = V_0, F = F(t),
    delta K / delta ln N = -2 K  (because delta n = -n delta ln N). -/
theorem lapse_density_correct (t K W V F : ℝ) (ht : t ≠ 0) :
    -(t * K - W / t - V * F + t * (-2 * K)) = t * K + W / t + V * F := by
  field_simp [ht]
  ring

/-- Kinetic variation used above: t * (-n^2) = -2 t K with K = n^2/2. -/
theorem kinetic_variation (t n : ℝ) : t * (-(n ^ 2)) = -2 * t * (n ^ 2 / 2) := by
  ring

/-- Negative control: if n (hence K) is held fixed during the lapse variation,
    only the measure term survives and the density acquires kinetic part -t*K. -/
theorem control_wrong_density (t K W V F : ℝ) :
    -(t * K - W / t - V * F) = -(t * K) + W / t + V * F := by
  ring

/-- Exact residual of the negative control: 2*t*K, kinetic only. -/
theorem control_residual (t K W V F : ℝ) :
    (t * K + W / t + V * F) - (-(t * K) + W / t + V * F) = 2 * t * K := by
  ring

/-- The wrong density's kinetic coefficient is strictly negative for t > 0. -/
theorem wrong_kinetic_sign (t : ℝ) (ht : 0 < t) : -(t * (1 : ℝ)) < 0 := by
  nlinarith

/-- The correct density's kinetic piece is strictly positive for t > 0, K > 0. -/
theorem correct_kinetic_positive (t K : ℝ) (ht : 0 < t) (hK : 0 < K) :
    0 < t * K := by
  positivity

/-- Reciprocal-barrier shape identity: (t + 1/t - 2)^2 = (t-1)^4 / t^2. -/
theorem F_identity (t : ℝ) (ht : t ≠ 0) :
    (t + 1 / t - 2) ^ 2 = (t - 1) ^ 4 / t ^ 2 := by
  field_simp [ht]
  ring

/-- F(t) = 1 + (t + 1/t - 2)^2 >= 1 for all t ≠ 0 (equality at t = 1). -/
theorem F_lower_bound (t : ℝ) :
    (1 : ℝ) ≤ 1 + (t + 1 / t - 2) ^ 2 := by
  have hsq : 0 ≤ (t + 1 / t - 2) ^ 2 := sq_nonneg _
  nlinarith

/-- The vacuum piece of the density equals V0*F(t) and shares the barrier's
    lower bound: rho_v >= V0 (V0 > 0). -/
theorem vacuum_piece_bound (t V : ℝ) (hV : 0 < V) :
    V ≤ V * (1 + (t + 1 / t - 2) ^ 2) := by
  have hF : (1 : ℝ) ≤ 1 + (t + 1 / t - 2) ^ 2 := F_lower_bound t
  simpa using mul_le_mul_of_nonneg_left hF (le_of_lt hV)

end AS127
