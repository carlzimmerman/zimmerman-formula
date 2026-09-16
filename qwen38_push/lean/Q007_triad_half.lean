/-
  Q007 -- THE 1/2: the triad temperature coefficient, LEAN-CERTIFIED.

  The repository (GRAVITY_EVERYWHERE S2.ii / G031 V3 / G03G V1) carried
  sigma^2 = sqrt(G*M_b*a0)/2 and rho = sqrt(G*M_b*a0)/(4*pi*G*r^2) as
  ASSERTED exact values ("sympy-exact", "coefficient exactly 1").  The
  flatness argument selects the r^-2 SHAPE; it says nothing about the
  AMPLITUDE.  This file derives the amplitude: isothermal hydrostatic
  equilibrium of the flatness-selected r^-2 profile closes to
  v_c^2 = 2*sigma^2, and the r^-2 circular velocity is exactly v_flat^2
  (G03E's certified linear mass law M(<r) = M_b*r/r_M).  Hence
  sigma^2 = v_flat^2/2 = sqrt(G*M_b*a0)/2 at every r -- and the density
  coefficient and the temperature coefficient are ONE identity,
  A = sigma^2/(2*pi*G) (with sigma^2 = v_flat^2/2).

  All theorems are pure real algebra: zero numerics, zero sqrt beyond the
  symbolic r_M := sqrt(G*M_b/a0), zero axioms beyond propext/choice/Quot.
-/
import Mathlib
open Real

/-- The MOND radius, kept symbolic (r_M = sqrt(G*M_b/a0)). -/
noncomputable def rM (G M_b a0 : ℝ) : ℝ := Real.sqrt (G * M_b / a0)

/-- v_flat^2 = G*M_b/r_M = a0*r_M = sqrt(G*M_b*a0).  (G083-style:
  let-bound r_M, one sq_sqrt, no product-of-sqrts.) -/
theorem vflat2_of_rM (G M_b a0 : ℝ) (hG : 0 < G) (hM : 0 < M_b) (ha : 0 < a0) :
    G * M_b / rM G M_b a0 = Real.sqrt (G * M_b * a0) := by
  have hrM2 : (rM G M_b a0) ^ 2 = G * M_b / a0 :=
      Real.sq_sqrt (by positivity)
  have hrMne : rM G M_b a0 ≠ 0 := (Real.sqrt_pos.mpr (by positivity)).ne'
  -- step 1: G*M_b/r_M = a0*r_M
  have hstep : G * M_b / (rM G M_b a0) = a0 * (rM G M_b a0) := by
    rw [show G * M_b = a0 * (rM G M_b a0) ^ 2 by
          rw [hrM2]; field_simp [ha.ne]]
    field_simp [hrMne, pow_two]
  -- step 2: a0*r_M = sqrt(G*M_b*a0); square both sides (both positive)
  have hpos : 0 < a0 * (rM G M_b a0) :=
      mul_pos ha (Real.sqrt_pos.mpr (by positivity))
  have hsq : (a0 * (rM G M_b a0)) ^ 2 = G * M_b * a0 := by
    ring_nf
    rw [hrM2]
    field_simp [ha.ne]
  have hsqrt : a0 * (rM G M_b a0) = Real.sqrt ((a0 * (rM G M_b a0)) ^ 2) :=
      (Real.sqrt_sq (le_of_lt hpos)).symm
  rw [hstep, hsqrt, hsq]

/-- The r^-2 phantom profile's circular velocity is exactly the flat value
  at every r:  v_c^2 = G*M(<r)*/r = G*(M_b*r/r_M)*/r = G*M_b/r_M (G03E). -/
theorem vc2_of_profile (G M_b a0 : ℝ) (hG : 0 < G) (hM : 0 < M_b) (ha : 0 < a0)
    (r : ℝ) (hr : 0 < r) :
    G * (M_b * r / rM G M_b a0) / r = G * M_b / rM G M_b a0 := by
  have hrMne : rM G M_b a0 ≠ 0 := (Real.sqrt_pos.mpr (by positivity)).ne'
  field_simp [hr.ne, hrMne]

/-- Isothermal hydrostatic closure on r^-2:  with dlog(rho)/dr = -2/r,
  the hydrostatic force -sigma^2 * r * dlog(rho)/dr = 2*sigma^2. -/
theorem hydro_r2_closes (r sigma2 : ℝ) (hr : 0 < r) :
    -sigma2 * r * (-2 / r) = 2 * sigma2 := by
  field_simp [hr.ne]

/-- THE 1/2:  v_c^2 = 2*sigma^2 (hydrostatic) and v_c^2 = G*M_b/r_M
  (the profile's circular velocity)  =>  sigma^2 = (G*M_b/r_M)/2. -/
theorem sigma2_is_half (G M_b a0 : ℝ) (hG : 0 < G) (hM : 0 < M_b) (ha : 0 < a0)
    (r : ℝ) (hr : 0 < r) (sigma2 : ℝ)
    (hvc : G * (M_b * r / rM G M_b a0) / r = 2 * sigma2) :
    sigma2 = (G * M_b / rM G M_b a0) / 2 := by
  have hv : G * (M_b * r / rM G M_b a0) / r = G * M_b / rM G M_b a0 :=
      vc2_of_profile G M_b a0 hG hM ha r hr
  rw [hv] at hvc
  linarith

/-- THE ONE EQUATION: the density coefficient A = sqrt(G*M_b*a0)/(4*pi*G)
  is the flat value over 4*pi*G -- the "exact 1" in the density and the
  1/2 in the temperature are one identity (A = sigma^2/(2*pi*G) with
  sigma^2 = v_flat^2/2). -/
theorem density_coeff_from_sigma2 (G M_b a0 : ℝ) (hG : 0 < G) (hM : 0 < M_b) (ha : 0 < a0) :
    (G * M_b / rM G M_b a0) / (4 * Real.pi * G) =
        Real.sqrt (G * M_b * a0) / (4 * Real.pi * G) := by
  rw [vflat2_of_rM G M_b a0 hG hM ha]

/-#
  KILL condition (stated, not proved): if the G081 relaxation/stability
  N-body finds the sector relaxes to sigma^2 != sqrt(G*M_b*a0)/2 (K001
  currently relaxes to 0.53 R0, no attractor), the hydrostatic reading is
  wrong even if this algebra stands.  The algebra is footing-independent;
  the dynamics is the test.
-/
#print axioms vflat2_of_rM
#print axioms vc2_of_profile
#print axioms hydro_r2_closes
#print axioms sigma2_is_half
#print axioms density_coeff_from_sigma2
#check rM
#check vflat2_of_rM
#check vc2_of_profile
#check hydro_r2_closes
#check sigma2_is_half
#check density_coeff_from_sigma2
