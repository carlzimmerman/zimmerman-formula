import Mathlib

/-!
# G03G -- THE TRIAD AND THE EQUIPARTITION (Lean certificate)

Theorem set for the breakthrough lane "FLATNESS SELECTS n = 2"
(deepseek_push/g03g_flatness_n2.py, 4/4 PASS):

  0. sqrt_pair : the one algebraic core shared by the two theorems:
     sqrt(G M_b a0) * sqrt(G M_b / a0) = G M_b  (the product identity)
  1. equipartition_exact : M_ph(<r_M) = M_b exactly
     (A = sqrt(G M_b a0)/(4 pi G), r_M = sqrt(G M_b/a0):
      the dark sector inside the MOND radius carries exactly the baryon mass)
  2. vc_flat_exact        : under the linear law M_ph(<r) = M_b r/r_M,
     v_c(r)^2 = G M_b/r_M = sqrt(G M_b a0) =: v_flat^2 -- the FLATNESS
     SELECTION instantiated: rho ~ r^-2 (gamma = 2) gives a flat curve at
     the exact BTFR zero point, no force modification
  3. sigma_virial_half    : sigma^2 / v_flat^2 = 1/2 (the virial half;
     with kappa = 1/2 (G002) and c_s^2(K->0) = 1/2 (G038), the triad is ONE
     number, one isothermal origin)
  4. the general "power-law flatness forces p = 1" form is REDUCED to its
     instantiation (theorem 2); the general proof needs the rpow-log
     injectivity extraction (2^q = 1 -> q = 0), whose Mathlib interface in
     this toolchain (v4.34.0-rc2) failed synthesis -- named, not hidden.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

-- 0. the product identity: sqrt(G Mb a0) * sqrt(G Mb / a0) = G Mb
--    (route: square both sides, sq_sqrt twice, resolve the sign with
--     nonnegativity -- no rpow, no NNReal coercion)
theorem sqrt_pair (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
  have hG0 : G ≠ 0 := by positivity
  have hx : 0 ≤ G * Mb * a0 := by positivity
  have hy : 0 ≤ G * Mb / a0 := by positivity
  have hxy : 0 ≤ (G * Mb * a0) * (G * Mb / a0) := by positivity
  have hs : (Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0)) ^ 2 = (G * Mb) ^ 2 := by
    rw [mul_pow]
    rw [Real.sq_sqrt hx]
    rw [Real.sq_sqrt hy]
    field_simp [hG0] <;> ring
  have hnonneg : 0 ≤ Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) := by positivity
  have hGpos : 0 ≤ G * Mb := by positivity
  have hor : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb
      ∨ Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = -(G * Mb) :=
    eq_or_eq_neg_of_sq_eq_sq _ _ hs
  rcases hor with h | h
  · exact h
  · nlinarith

-- 1. the equipartition: 4 pi A r_M = M_b
theorem equipartition_exact (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    let rM := Real.sqrt (G * Mb / a0)
    let A := Real.sqrt (G * Mb * a0) / (4 * Real.pi * G)
    (4 * Real.pi) * A * rM = Mb := by
  intro rM A
  dsimp [A, rM]
  have hG0 : G ≠ 0 := by positivity
  have hMb0 : Mb ≠ 0 := by positivity
  field_simp [hG0, hMb0]
  nlinarith [sqrt_pair G Mb a0 hG hMb ha0]

-- 2. the flatness selection, instantiated: M_ph = M_b r/r_M  =>  v_c^2 = v_flat^2
theorem vc_flat_exact (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hr : r ≠ 0) :
    let rM := Real.sqrt (G * Mb / a0)
    G * (Mb * (r / rM)) / r = Real.sqrt (G * Mb * a0) := by
  intro rM
  dsimp [rM]
  have hG0 : G ≠ 0 := by positivity
  have hMb0 : Mb ≠ 0 := by positivity
  have hdiv : G * Mb / Real.sqrt (G * Mb / a0) = Real.sqrt (G * Mb * a0) := by
    have hp := sqrt_pair G Mb a0 hG hMb ha0
    have hsq : Real.sqrt (G * Mb / a0) ≠ 0 := by positivity
    field_simp [hsq]
    nlinarith [hp]
  field_simp [hr, hG0, hMb0]
  nlinarith [sqrt_pair G Mb a0 hG hMb ha0]

-- 3. the virial half: sigma^2 / v_flat^2 = 1/2
theorem sigma_virial_half (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    let vf2 := Real.sqrt (G * Mb * a0)              -- v_flat^2
    let sg2 := Real.sqrt (G * Mb * a0) / 2          -- sigma^2 (rung 4)
    sg2 / vf2 = (1 : ℝ) / 2 := by
  intro vf2 sg2
  dsimp [vf2, sg2]
  have h : Real.sqrt (G * Mb * a0) ≠ 0 := by positivity
  field_simp [h]

#print axioms sqrt_pair
#print axioms equipartition_exact
#print axioms vc_flat_exact
#print axioms sigma_virial_half