import Mathlib

/-!
# G227-PROTOTYPE -- THE GAUSS-MAP CHARGE (candidate certificate, roadmap proof)

The G154/G180 charge: on the static branch the dark mass is the Gauss-map
charge of the sourced field,

    M_ph(<r) = (1/4πG) ∮_{S(r)} g·dA

For the isothermal well (the deep equilibrium), g = S/r with
S := sqrt(G M_b a0), and g is CONSTANT on the sphere S(r), so

    ∮_{S(r)} g dA = (4π r²) · (S/r) = 4π S r = 4π sqrt(G M_b a0) r

and therefore

    M_ph(<r) = S r / G = sqrt(G M_b a0) r / G = M_b r / r_M,   r_M := sqrt(G M_b / a0),

the framework's universal linear law (G03E V2 / G154 C3 / Lean G03G/G090).

THEOREMS IN THIS FILE (all algebra-only, the G03G sqrt_pair technique:
square both sides, resolve the sign with nonnegativity, no rpow):

  1. isothermal_flux : the surface integral of g over S(r) is
     4π sqrt(G M_b a0) r -- the exact task statement (a).
  2. gauss_map_charge : M_enc(<r) = (1/4πG)∮ = sqrt(G M_b a0) r / G.
  3. gauss_map_linear_law : M_enc(<r) = M_b r / r_M (needs sqrt_pair).
  4. gauss_map_equipartition : M_enc(<r_M) = M_b exactly (the G03G/G090
     equipartition, reached from the surface integral).

The surface integral is rendered algebraically: g constant on S(r) makes
∮_{S(r)} g dA = (sphere area) · g = 4π r² · g -- the 4π r² is a stated
premise (the sphere's area), the algebra that follows is the theorem.
Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

-- ============================================================
-- 1. THE FLUX: ∮_{S(r)} g dA = 4π sqrt(G M_b a0) r, g := S/r, S := sqrt(G M_b a0)
-- ============================================================
theorem isothermal_flux (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : r ≠ 0) :
    let S := Real.sqrt (G * Mb * a0)
    let g := S / r
    (4 * Real.pi) * r ^ 2 * g = 4 * Real.pi * Real.sqrt (G * Mb * a0) * r := by
  intro S g
  dsimp [g, S]
  field_simp [hr]

-- ============================================================
-- 2. THE CHARGE: M_ph(<r) = (1/4πG) ∮ g dA = sqrt(G M_b a0) r / G
-- ============================================================
theorem gauss_map_charge (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : r ≠ 0) :
    let S := Real.sqrt (G * Mb * a0)
    let g := S / r
    ((4 * Real.pi) * r ^ 2 * g) / (4 * Real.pi * G) = Real.sqrt (G * Mb * a0) * r / G := by
  intro S g
  dsimp [g, S]
  have hpi : (4 * Real.pi : ℝ) ≠ 0 := by positivity
  field_simp [hpi, hr, hG.ne']

-- ============================================================
-- 3. THE LINEAR LAW: M_ph(<r) = M_b r / r_M, r_M := sqrt(G M_b / a0)
--    (the sqrt_pair product sqrt(G M_b a0) * sqrt(G M_b / a0) = G M_b
--     is re-derived in-file -- standalone, no imports)
-- ============================================================
theorem sqrt_pair (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
  have hG0 : G ≠ 0 := by positivity
  have hx : 0 ≤ G * Mb * a0 := by positivity
  have hy : 0 ≤ G * Mb / a0 := by positivity
  have hs : (Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0)) ^ 2 = (G * Mb) ^ 2 := by
    rw [mul_pow]
    rw [Real.sq_sqrt hx]
    rw [Real.sq_sqrt hy]
    field_simp [hG0]
  have hnonneg : 0 ≤ Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) := by positivity
  have hGpos : 0 ≤ G * Mb := by positivity
  have hor : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb
      ∨ Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = -(G * Mb) :=
    eq_or_eq_neg_of_sq_eq_sq _ _ hs
  rcases hor with h | h
  · exact h
  · nlinarith

theorem gauss_map_linear_law (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : r ≠ 0) :
    let rM := Real.sqrt (G * Mb / a0)
    let S := Real.sqrt (G * Mb * a0)
    let g := S / r
    ((4 * Real.pi) * r ^ 2 * g) / (4 * Real.pi * G) = Mb * (r / rM) := by
  intro rM S g
  dsimp [g, S, rM]
  have hpi : (4 * Real.pi : ℝ) ≠ 0 := by positivity
  have hG0 : G ≠ 0 := by positivity
  have hMb0 : Mb ≠ 0 := by positivity
  have hsq : Real.sqrt (G * Mb / a0) ≠ 0 := by positivity
  have hp := sqrt_pair G Mb a0 hG hMb ha0
  field_simp [hpi, hr, hG0, hMb0, hsq]
  nlinarith [hp]

-- ============================================================
-- 4. THE EQUIPARTITION: M_ph(<r_M) = M_b exactly (from the surface integral)
-- ============================================================
theorem gauss_map_equipartition (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) :
    let rM := Real.sqrt (G * Mb / a0)
    let S := Real.sqrt (G * Mb * a0)
    let g := S / rM
    ((4 * Real.pi) * rM ^ 2 * g) / (4 * Real.pi * G) = Mb := by
  intro rM S g
  dsimp [g, S, rM]
  have hpi : (4 * Real.pi : ℝ) ≠ 0 := by positivity
  have hG0 : G ≠ 0 := by positivity
  have hMb0 : Mb ≠ 0 := by positivity
  have hsq : Real.sqrt (G * Mb / a0) ≠ 0 := by positivity
  have hp := sqrt_pair G Mb a0 hG hMb ha0
  field_simp [hpi, hG0, hMb0, hsq]
  nlinarith [hp]

#print axioms isothermal_flux
#print axioms gauss_map_charge
#print axioms gauss_map_linear_law
#print axioms gauss_map_equipartition
