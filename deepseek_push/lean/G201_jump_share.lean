import Mathlib

/-!
# G201 -- THE JUMP, THE SHARE, THE LIFT (Lean certificate)

Three new closed forms from the G159/G186 wave, certified algebra-only in
the G03G/G083/G090 spine convention (each certificate standalone, no imports;
every sqrt closed by the sqrt_pair sign-resolution technique -- square both
sides, resolve the sign with nonnegativity, no rpow, no NNReal coercion):

  1. THE JUMP (G159).  The cluster amplitude A_b = rho_ph/rho_d was derived
     in G159 as A_b = (sigma_ph/sigma_d)^3 = exp(dS/k_B).  THE ALGEBRA LEAN
     CARRIES -- and the first thing it does NOT carry is the naive isothermal
     reading.  With both phases in the SAME well (shared C) the isothermal-
     sphere identity rho*sigma^2 = C/(4 pi G r^2) at equal r gives
     rho_ph*sigma_ph^2 = rho_d*sigma_d^2, i.e. ONLY the 2D mechanical
     relation rho_ph/rho_d = (sigma_d/sigma_ph)^2 -- exponent 2, ratio
     INVERTED.  The (sigma_ph/sigma_d)^3 of G159 is an ENTROPY statement:
     the coexistence entropy jump in the shared class is
     dS/k_B = 3 ln(sigma_ph/sigma_d) (one ln per phase-space dimension --
     the 3 is the dimension count), and A_b = exp(dS/k_B).  The certificate
     carries the exact algebra: ln A_b = 3 ln(sigma_ph/sigma_d)
     (entropy_jump_log), log((sph/sd)^3) = 3 log(sph/sd)
     (entropy_jump_cube), exp(3 ln(sph/sd)) = (sph/sd)^3
     (entropy_jump_additivity), and jump_cube = the G159 amplitude read as
     the entropy jump.  NO overclaim: Lean certifies the ALGEBRA of the
     jump given the entropy; the dressed physics input (the collisionless
     dust's local dispersion at the cap is the potential scale, G103/G137,
     NOT its kinetic temperature) is a committed-lane claim, not a theorem.

  2. THE SHARE (G186/G197).  With M_ph = M_b*r/r_M (the linear law, the
     Gauss-map charge) and M_dyn = f*M_b (the dynamical mass in units of the
     baryon mass), the phantom's share of the MISSING mass is
     M_ph/(M_dyn - M_b) = (M_b*r/r_M)/((f-1)*M_b) = (r/r_M)/(f-1) -- one
     field_simp line (share_identity), plus the r_M := sqrt(G*M_b/a0)
     instantiation (share_identity_deep), rM2 = G*M_b/a0 kept symbolic under
     the single sqrt.

  3. THE LIFT (the deep RAR).  g^2 = a0*g_N was already certified (G031
     deep_rar, coefficient exactly 1); G201 RESTATES it in the equilibrium
     form (g := S/r with S := sqrt(G*M_b*a0), g_N := G*M_b/r^2) and adds
     the NEW closed form, the sq root READING: in the deep limit
     g = sqrt(a0*g_N) -- the deep-limit acceleration is the GEOMETRIC MEAN
     of a0 and g_N.  Stated carefully: it is the same statement in
     geometric-mean form, not an independent law -- it holds because
     g >= 0 (sq_eq + nonnegativity, the sqrt_pair resolution technique);
     the only sqrts are S := sqrt(G*M_b*a0) (closed by Real.sq_sqrt) and
     sqrt(a0*g_N) (closed by the sign resolution), rM2 = G*M_b/a0 nowhere
     expanded.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
Physics provenance: deepseek_push/G159_jump_condition.py,
deepseek_push/G186_one_boundary.py, deepseek_push/G197_galaxy_pie.py.
-/

-- ============================================================
-- 1. THE JUMP -- first the 2D mechanical truth, then the entropy cube
-- ============================================================

-- 1a. what the shared-well MECHANICS actually gives: exponent 2, inverted
--     (isothermal-sphere identity rho*sigma^2 = C/(4 pi G r^2) at equal r
--      in the SAME well C: rho_ph*sigma_ph^2 = rho_d*sigma_d^2
--      -> rho_ph/rho_d = (sigma_d/sigma_ph)^2 -- the honest 2D statement)
theorem isothermal_density_ratio (rph rd sph sd : ℝ) (hrd : 0 < rd)
    (hs : 0 < sph) (hC : rph * sph ^ 2 = rd * sd ^ 2) :
    rph / rd = (sd / sph) ^ 2 := by
  have hsph0 : sph ≠ 0 := ne_of_gt hs
  have hrd0 : rd ≠ 0 := ne_of_gt hrd
  field_simp [hsph0, hrd0]
  nlinarith [hC]

-- 1b. the entropy jump at the log level, EXACTLY as G159 states it:
--     ln A_b = 3 ln(sigma_ph/sigma_d) with A_b := exp(3 ln(ratio)) -- the 3
--     the phase-space dimension count (one Real.log_exp; unconditional)
theorem entropy_jump_log (sph sd : ℝ) :
    let Ab := Real.exp (3 * Real.log (sph / sd))
    Real.log Ab = 3 * Real.log (sph / sd) := by
  intro Ab
  dsimp [Ab]
  rw [Real.log_exp]

-- 1c. the same 3 at the power level: log((sph/sd)^3) = 3 log(sph/sd)
--     (Real.log_pow is unconditional; the (3 : ℕ) coerces to 3)
theorem entropy_jump_cube (sph sd : ℝ) :
    Real.log ((sph / sd) ^ 3) = 3 * Real.log (sph / sd) := by
  rw [Real.log_pow]
  norm_num

-- 1d. the amplitude as exp(dS/k_B): exp(3 ln(sph/sd)) = (sph/sd)^3
--     (positivity of the ratio closes Real.exp_log)
theorem entropy_jump_additivity (sph sd : ℝ) (hs : 0 < sph) (hsd : 0 < sd) :
    Real.exp (3 * Real.log (sph / sd)) = (sph / sd) ^ 3 := by
  have hcube : Real.log ((sph / sd) ^ 3) = 3 * Real.log (sph / sd) :=
    entropy_jump_cube sph sd
  calc Real.exp (3 * Real.log (sph / sd))
      = Real.exp (Real.log ((sph / sd) ^ 3)) := by rw [← hcube]
    _ = (sph / sd) ^ 3 := Real.exp_log (by positivity)

-- 1e. THE G159 AMPLITUDE, entropy-carried (no overclaim): with
--     A_b := exp(dS/k_B), dS/k_B := 3 ln(sigma_ph/sigma_d):
--     A_b = (sigma_ph/sigma_d)^3 -- the jump of G159, NOT the 2D
--     isothermal ratio of 1a (which is inverted and squared)
theorem jump_cube (sph sd : ℝ) (hs : 0 < sph) (hsd : 0 < sd) :
    let Ab := Real.exp (3 * Real.log (sph / sd))
    Ab = (sph / sd) ^ 3 := by
  intro Ab
  dsimp [Ab]
  exact entropy_jump_additivity sph sd hs hsd

-- ============================================================
-- 2. THE SHARE -- M_ph/(M_dyn - M_b) = (r/r_M)/(f-1), one field_simp
-- ============================================================

-- the phantom share of the missing mass: M_ph = M_b*r/r_M (linear law),
-- M_dyn = f*M_b, so share = M_ph/(M_dyn - M_b) = (M_b*r/r_M)/((f-1)*M_b)
-- = (r/r_M)/(f-1) -- pure cancellation, rM kept SYMBOLIC (no sqrt)
theorem share_identity (r rM Mb f : ℝ) (hrM : rM ≠ 0) (hMb : Mb ≠ 0)
    (hf : f - 1 ≠ 0) :
    (Mb * (r / rM)) / (f * Mb - Mb) = (r / rM) / (f - 1) := by
  field_simp [hrM, hMb, hf]

-- the same share at the deep instantiation r_M := sqrt(G*M_b/a0)
-- (rM2 = G*M_b/a0 kept symbolic under the single sqrt)
theorem share_identity_deep (G Mb a0 r f : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hf : f - 1 ≠ 0) :
    let rM := Real.sqrt (G * Mb / a0)
    (Mb * (r / rM)) / (f * Mb - Mb) = (r / rM) / (f - 1) := by
  intro rM
  dsimp [rM]
  have hrM0 : Real.sqrt (G * Mb / a0) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mpr (by positivity))
  exact share_identity r (Real.sqrt (G * Mb / a0)) Mb f hrM0 hMb.ne' hf

-- ============================================================
-- 3. THE LIFT -- the deep RAR restated + the sq root reading
-- ============================================================

-- the deep RAR g^2 = a0*g_N with the equilibrium (g := S/r, S := sqrt(G*M_b*a0),
-- g_N := G*M_b/r^2; the square law was first certified as G031 deep_rar) AND
-- the NEW closed form: the deep-limit acceleration's sqrt reading
-- g = sqrt(a0*g_N) -- the geometric mean of a0 and g_N, valid because g >= 0
-- (sq_eq + nonnegativity: the sqrt_pair sign-resolution technique)
theorem deep_limit_sq (G Mb a0 r S : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : 0 < r) (hS : S = Real.sqrt (G * Mb * a0)) :
    let g := S / r
    let gN := G * Mb / r ^ 2
    g ^ 2 = a0 * gN ∧ g = Real.sqrt (a0 * gN) := by
  intro g gN
  dsimp [g, gN]
  have hS2 : S ^ 2 = G * Mb * a0 := by
    rw [hS]
    exact Real.sq_sqrt (by positivity)
  constructor
  · calc (S / r) ^ 2 = S ^ 2 / r ^ 2 := by ring
      _ = G * Mb * a0 / r ^ 2 := by rw [hS2]
      _ = a0 * (G * Mb / r ^ 2) := by ring
  · have hsq : Real.sqrt (a0 * (G * Mb / r ^ 2)) ^ 2 = (S / r) ^ 2 := by
      rw [Real.sq_sqrt (show (0 : ℝ) ≤ a0 * (G * Mb / r ^ 2) by positivity)]
      rw [div_pow]
      rw [hS2]
      ring
    have hS0 : (0 : ℝ) ≤ S := by
      rw [hS]
      exact Real.sqrt_nonneg _
    have hg0 : (0 : ℝ) ≤ S / r := by positivity
    have hs0 : (0 : ℝ) ≤ Real.sqrt (a0 * (G * Mb / r ^ 2)) := Real.sqrt_nonneg _
    have hor := eq_or_eq_neg_of_sq_eq_sq (Real.sqrt (a0 * (G * Mb / r ^ 2))) (S / r) hsq
    rcases hor with h | h
    · exact h.symm
    · nlinarith

#print axioms isothermal_density_ratio
#print axioms entropy_jump_log
#print axioms entropy_jump_cube
#print axioms entropy_jump_additivity
#print axioms jump_cube
#print axioms share_identity
#print axioms share_identity_deep
#print axioms deep_limit_sq