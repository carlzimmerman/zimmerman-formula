import Mathlib

/-!
# G083 -- THE UNIVERSAL SURFACE DENSITY CERTIFICATE (Lean certificate)

Physics (deepseek_push/g078_surface_density.py, 4/4 PASS): the mean dark
surface density inside the MOND radius r_M is UNIVERSAL:

    <Sigma_ph>(<r_M) := M_ph(<r_M)/(pi r_M^2) = M_b/(pi r_M^2) = a0/(pi G),

the M_b cancels -- a pure function of the one scale a0, mass independent,
galaxy independent.  This is the composition theorem: the equipartition law
(G03G equipartition_exact: M_ph(<r_M) = M_b) and hy4's H033
(Sigma = a0/(pi G), 213.74 M_sun/pc^2) are ONE statement.

  a0/(pi G) = 0.44651 kg/m^2 = 213.75 M_sun/pc^2.

Four theorems, all algebra-only, stated to AVOID sqrt entirely (r_M^2 =
G*M_b/a0 kept symbolic; only the sqrt-flavoured restatement (4) brings in
one sqrt, closed with Real.sq_sqrt -- no sqrt_pair product needed):

  1. surface_density_universal:  with rM2 := G*Mb/a0,
        Mb/(pi*rM2) = a0/(pi*G)          -- one field_simp/ring line.
  2. surface_density_equipartition_form: G03G's equipartition_exact
        restated through the linear law M_ph(r) = M_b*r/r_M at r = r_M:
        M_b*r_M/r_M = M_b                 -- trivial cancellation.
  3. num_sigma_bar_msun: the NUMBER as an interval (G036 style), with the
        certified SI constants a0 = 9.3619e-11 m/s^2, G = 6.674e-11, the
        unit conversion M_sun/pc^2 = MSUN/PC^2 (MSUN = 1.989e30 kg,
        PC = 3.0857e16 m): 213.75 in (213, 215) M_sun/pc^2 -- the pi bounds
        Real.pi_lt_d4 / Real.pi_gt_d6 reduce every comparison to rational
        arithmetic, norm_num-closable (no sqrt).
  4. surface_density_mean: the identity sigma_bar = a0/(pi*G) with
        sigma_bar := M_b/(pi*r_M^2), r_M = sqrt(G*Mb/a0) -- pi kept
        symbolic; the interval companion (with the pi bounds) is (3).
  C. surface_density_composition: the physics line itself,
        M_ph(<r_M)/(pi*r_M^2) = a0/(pi*G) given the equipartition
        M_ph(<r_M) = M_b -- "the M_b cancels".

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

-- 1. the universality: the mean dark surface density inside r_M is a0/(pi G)
--    (rM2 := G*Mb/a0 kept SYMBOLIC -- no sqrt appears)
theorem surface_density_universal (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) :
    let rM2 := G * Mb / a0
    Mb / (Real.pi * rM2) = a0 / (Real.pi * G) := by
  intro rM2
  dsimp [rM2]
  field_simp [hG.ne', ha0.ne', Real.pi_ne_zero]

-- 2. the equipartition form: G03G's equipartition_exact restated through the
--    linear law M_ph(r) = M_b*r/r_M, evaluated at r = r_M: M_ph(r_M) = M_b
theorem surface_density_equipartition_form (Mb rM : ℝ) (hrM : rM ≠ 0) :
    Mb * rM / rM = Mb := by
  field_simp [hrM]

-- 3. the number as an interval (G036 style): with the certified SI constants
--    a0 = 9.3619e-11 m/s^2 and G = 6.674e-11, and the unit conversion
--    M_sun/pc^2 = MSUN/PC^2 (MSUN = 1.989e30 kg, PC = 3.0857e16 m), the
--    universal surface density a0/(pi*G) = 213.75 M_sun/pc^2 lies strictly
--    between 213 and 215 M_sun/pc^2.  All comparisons are rational after
--    bounding pi with Real.pi_lt_d4 / Real.pi_gt_d6 -- no sqrt anywhere.
theorem num_sigma_bar_msun :
    (213:ℝ) * 1.989e30 / (3.0857e16) ^ 2 < 9.3619e-11 / (Real.pi * 6.674e-11) ∧
    9.3619e-11 / (Real.pi * 6.674e-11) < 215 * 1.989e30 / (3.0857e16) ^ 2 := by
  have hden : (0:ℝ) < Real.pi * 6.674e-11 := by positivity
  have hkey : (0.445:ℝ) < 9.3619e-11 / (Real.pi * 6.674e-11) := by
    rw [lt_div_iff₀ hden]
    calc (0.445:ℝ) * (Real.pi * 6.674e-11)
        = (0.445:ℝ) * 6.674e-11 * Real.pi := by ring
      _ ≤ (0.445:ℝ) * 6.674e-11 * 3.1416 :=
          mul_le_mul_of_nonneg_left Real.pi_lt_d4.le
            (by norm_num : (0:ℝ) ≤ (0.445:ℝ) * 6.674e-11)
      _ < 9.3619e-11 := by norm_num
  have hkey2 : 9.3619e-11 / (Real.pi * 6.674e-11) < (0.447:ℝ) := by
    rw [div_lt_iff₀ hden]
    calc (9.3619e-11:ℝ) < 0.447 * 6.674e-11 * 3.141592 := by norm_num
      _ ≤ 0.447 * 6.674e-11 * Real.pi :=
          mul_le_mul_of_nonneg_left (le_of_lt Real.pi_gt_d6)
            (by norm_num : (0:ℝ) ≤ 0.447 * 6.674e-11)
      _ = 0.447 * (Real.pi * 6.674e-11) := by ring
  constructor
  · calc (213:ℝ) * 1.989e30 / (3.0857e16) ^ 2 < 0.445 := by norm_num
      _ < 9.3619e-11 / (Real.pi * 6.674e-11) := hkey
  · calc 9.3619e-11 / (Real.pi * 6.674e-11) < 0.447 := hkey2
      _ < 215 * 1.989e30 / (3.0857e16) ^ 2 := by norm_num

-- 4. the mean identity: sigma_bar = a0/(pi*G), where
--    sigma_bar := M_b/(pi*r_M^2) with r_M = sqrt(G*Mb/a0) -- the ONLY
--    theorem where a sqrt appears, closed by Real.sq_sqrt (G03G's sqrt_pair
--    is not needed: the square of a single sqrt, not a product of two).
theorem surface_density_mean (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) :
    let rM := Real.sqrt (G * Mb / a0)
    let sigma_bar := Mb / (Real.pi * rM ^ 2)
    sigma_bar = a0 / (Real.pi * G) := by
  intro rM sigma_bar
  dsimp [sigma_bar, rM]
  rw [Real.sq_sqrt (show (0:ℝ) ≤ G * Mb / a0 by positivity)]
  field_simp [hG.ne', ha0.ne', Real.pi_ne_zero]

-- C. the composition (g078 V2, the physics line itself): given the
--    equipartition M_ph(<r_M) = M_b, the mean dark surface density inside
--    r_M is a0/(pi*G) -- "the M_b cancels".
theorem surface_density_composition (G Mb a0 Mph : ℝ) (hG : 0 < G)
    (hMb : 0 < Mb) (ha0 : 0 < a0) (hE : Mph = Mb) :
    let rM2 := G * Mb / a0
    Mph / (Real.pi * rM2) = a0 / (Real.pi * G) := by
  intro rM2
  dsimp [rM2]
  rw [hE]
  field_simp [hG.ne', ha0.ne', Real.pi_ne_zero]

#print axioms surface_density_universal
#print axioms surface_density_equipartition_form
#print axioms num_sigma_bar_msun
#print axioms surface_density_mean
#print axioms surface_density_composition
