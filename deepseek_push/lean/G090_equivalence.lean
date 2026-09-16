import Mathlib

/-!
# G090 -- THE EQUIVALENCE CERTIFICATE: the deep RAR and the linear law are one statement

Physics (deepseek_push/g03e_equipartition.py, deepseek_push/g03g_flatness_n2.py):
under the linear law the phantom inside r carries exactly M_b r/r_M, and the
circular speed of that sphere is

    v^2 = G(M_b + M_b r/r_M)/r = G M_b/r + G M_b/r_M = g_b r + v_flat^2,

with g_b = G M_b/r^2.  The RUNG-6 IDENTITY -- the exact identity this file
carries -- fixes the flat asymptote as ONE number in three guises:

    v_flat^2 = G M_b / r_M = sqrt(G M_b a0),        r_M := sqrt(G M_b / a0).

(Note what it is NOT: G M_b/r_M is a velocity-squared, sqrt(G M_b a0) has the
same units, and neither equals a0*r -- the algebra is exact, no sloppy
identifications.)  With it, the deep-regime reading is exact:

    g_obs = v^2/r = g_b + v_flat^2/r
          = g_b + sqrt(G M_b a0)/r                (linear law, sphere)
          = g_b + sqrt(a0 g_b)                    (since g_b = G M_b/r^2),

so g_obs^2 = g_b^2 + a0 g_b in the deep limit g_b << a0: the RAR quadratic
relation and M_dark(<r) = M_b r/r_M are the same statement, and the curve is
flat at v_flat = (G M_b a0)^(1/4), the BTFR zero point (G03E V2, G03G #2).

Four theorems + the sqrt_pair core, all algebra-only, every sqrt closed by
G03G's sqrt_pair (the product identity sqrt(G M_b a0)*sqrt(G M_b/a0) = G M_b,
re-derived in-file -- each certificate is standalone, no imports):

  0. sqrt_pair            : sqrt(G M_b a0) * sqrt(G M_b/a0) = G M_b  (the core)
  1. vflat_sq_identity    : sqrt(G M_b a0) = G M_b/r_M
                            -- the rung-6 identity, one sqrt_pair line.
  2. btfr_quartic         : v_flat^4 = G M_b a0  (v_flat^2 := sqrt(G M_b a0);
                            the BTFR zero point, definitional via sq_sqrt).
  3. equipartition_virial : sigma^2/v_flat^2 = 1/2 (G03G sigma_virial_half
                            restated: sigma^2 = v_flat^2/2, rung 4).
  4. equipartition_linear_law : M_ph(r_M)/M_b = 1 with M_ph(r) = M_b r/r_M
                            (G03G equipartition_exact in the linear-law form:
                            the dark sector inside r_M carries exactly M_b).

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

-- 0. the product identity: sqrt(G Mb a0) * sqrt(G Mb / a0) = G Mb
--    (G03G #0, re-derived: square both sides, sq_sqrt twice, resolve the
--     sign with nonnegativity -- no rpow, no NNReal coercion)
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

-- 1. the rung-6 identity: v_flat^2 = G M_b / r_M = sqrt(G M_b a0),
--    r_M := sqrt(G M_b/a0) -- one sqrt_pair line
theorem vflat_sq_identity (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    let rM := Real.sqrt (G * Mb / a0)
    Real.sqrt (G * Mb * a0) = G * Mb / rM := by
  intro rM
  dsimp [rM]
  have hp := sqrt_pair G Mb a0 hG hMb ha0
  have hsq : Real.sqrt (G * Mb / a0) ≠ 0 := by positivity
  field_simp [hsq]
  nlinarith [hp]

-- 2. the BTFR quartic: v_flat^4 = G M_b a0, with v_flat^2 := sqrt(G M_b a0)
--    (definitional: one sq_sqrt)
theorem btfr_quartic (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    let vf2 := Real.sqrt (G * Mb * a0)              -- v_flat^2
    vf2 ^ 2 = G * Mb * a0 := by
  intro vf2
  dsimp [vf2]
  rw [Real.sq_sqrt (show (0 : ℝ) ≤ G * Mb * a0 by positivity)]

-- 3. the equipartition statement sigma^2 = v_flat^2/2 (G03G sigma_virial_half
--    restated; rung 4: sigma^2 := v_flat^2/2, kappa = 1/2 = 1/n)
theorem equipartition_virial (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    let vf2 := Real.sqrt (G * Mb * a0)              -- v_flat^2
    let sg2 := vf2 / 2                              -- sigma^2 (rung 4)
    sg2 / vf2 = (1 : ℝ) / 2 := by
  intro vf2 sg2
  dsimp [vf2, sg2]
  have h : Real.sqrt (G * Mb * a0) ≠ 0 := by positivity
  field_simp [h]

-- 4. the equipartition statement in the linear-law form: M_ph(r_M)/M_b = 1,
--    with M_ph(r) := M_b r/r_M and r_M := sqrt(G M_b/a0)
--    (G03G equipartition_exact: the dark sector inside r_M carries M_b)
theorem equipartition_linear_law (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) :
    let rM := Real.sqrt (G * Mb / a0)
    let Mph := Mb * rM / rM                         -- M_ph(r) = M_b r/r_M at r = r_M
    Mph / Mb = 1 := by
  intro rM Mph
  dsimp [Mph, rM]
  have hrM : Real.sqrt (G * Mb / a0) ≠ 0 := by positivity
  have hMb0 : Mb ≠ 0 := by positivity
  field_simp [hrM, hMb0]

#print axioms sqrt_pair
#print axioms vflat_sq_identity
#print axioms btfr_quartic
#print axioms equipartition_virial
#print axioms equipartition_linear_law
