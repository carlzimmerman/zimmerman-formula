/-
  Q008 -- THE GLOBAL VIRIAL DUAL: the boundary term 3 P_s V = sigma^2 M_T,
  LEAN-CERTIFIED.

  Q007 derived sigma^2 = v_flat^2/2 by the LOCAL route (isothermal
  hydrostatics on the r^-2 profile closes to v_c^2 = 2*sigma^2).  G091
  (deepseek, just landed) independently derived the SAME C/2 by the GLOBAL
  route: the virial theorem for the truncated self-gravitating isothermal
  phantom, 2T + W_self + W_bar = 3 P_s V.  G091 cites the Q007 draft and
  notes the bare collisionless virial (no boundary term) gives C/3, not C/2.

  THIS FILE CERTIFIES THE BOUNDARY-TERM IDENTITY:  3 P_s V = sigma^2 M_T
  is EXACTLY the term that shifts the coefficient from 3 (collisionless,
  reading A: 2T+W=0 -> sigma^2 = C/3) to 2 (fluid, reading B:
  2T+W = 3 P_s V -> sigma^2 = C/2).  The 1/2 is the SAME number from two
  independent routes (local hydrostatics Q007, global virial Q008) -- that
  agreement is the robustness statement.

  Notation:  C := 4*pi*G*A := v_flat^2 (the flat value, Q007 vflat2_of_rM),
  A = the r^-2 density coefficient, M_T = 4*pi*A*R the linear-law enclosed
  mass at the truncation R, P = sigma^2*rho the isothermal EOS at the cap.
  All theorems are pure real algebra: zero numerics, zero sqrt.
-/
import Mathlib
open Real

/-- The linear-law enclosed mass at truncation R: M_T = 4*pi*A*R. -/
noncomputable def MT (A R : ℝ) : ℝ := 4 * Real.pi * A * R

/-- V2: THE BOUNDARY-TERM IDENTITY  3 P_s V = sigma^2 * M_T.
  P = sigma^2 * A / R^2 (isothermal EOS at the cap), V = 4*pi*R^3/3. -/
theorem boundary_term (A R sigma2 : ℝ) (hA : 0 < A) (hR : 0 < R) :
    3 * (sigma2 * A / R ^ 2) * (4 * Real.pi * R ^ 3 / 3) = sigma2 * MT A R := by
  dsimp [MT]
  field_simp [hR.ne]

/-- V1: W_self = -G M_T^2 / R (the shell-theorem closed form for rho = A/r^2
   truncated at R: W_self = -16*pi^2*G*A^2*R = -G M_T^2/R). -/
theorem wself_closed_form (G A R : ℝ) (hG : 0 < G) (hA : 0 < A) (hR : 0 < R) :
    -16 * (Real.pi) ^ 2 * G * A ^ 2 * R = -G * (MT A R) ^ 2 / R := by
  dsimp [MT]
  field_simp [hR.ne]
  ring

/-- V3: reading A (collisionless, 2T + W_self = 0): sigma^2 = C/3.
  T = (3/2) M_T sigma^2, W_self = -G M_T^2/R, C = 4*pi*G*A. -/
theorem readingA_collisionless (G A R sigma2 : ℝ) (hG : 0 < G) (hA : 0 < A) (hR : 0 < R)
    (hvir : 2 * ((3:ℝ) / 2 * MT A R * sigma2) - G * (MT A R) ^ 2 / R = 0) :
    sigma2 = (4 * Real.pi * G * A) / 3 := by
  have hW : G * (MT A R) ^ 2 / R = (4 * Real.pi * G * A) * (MT A R) := by
    field_simp [hR.ne]
    dsimp [MT]
    ring
  have hT : 2 * ((3:ℝ) / 2 * MT A R * sigma2) = 3 * MT A R * sigma2 := by ring
  rw [hT, hW] at hvir
  have hMTne : MT A R ≠ 0 := by
    dsimp [MT]
    positivity
  have hlin : 3 * MT A R * sigma2 = (4 * Real.pi * G * A) * (MT A R) := by
    linarith
  have hdiv : 3 * sigma2 = 4 * Real.pi * G * A := by
    exact (mul_right_inj' hMTne).mp (by
      ring_nf at hlin ⊢
      linarith)
  field_simp
  linarith

/-- V4: reading B (fluid, 2T + W_self = 3 P_s V = sigma^2 M_T): sigma^2 = C/2. -/
theorem readingB_fluid (G A R sigma2 : ℝ) (hG : 0 < G) (hA : 0 < A) (hR : 0 < R)
    (hvir : 2 * ((3:ℝ) / 2 * MT A R * sigma2) - G * (MT A R) ^ 2 / R = sigma2 * MT A R) :
    sigma2 = (4 * Real.pi * G * A) / 2 := by
  have hW : G * (MT A R) ^ 2 / R = (4 * Real.pi * G * A) * (MT A R) := by
    field_simp [hR.ne]
    dsimp [MT]
    ring
  have hT : 2 * ((3:ℝ) / 2 * MT A R * sigma2) = 3 * MT A R * sigma2 := by ring
  rw [hT, hW] at hvir
  have hMTne : MT A R ≠ 0 := by
    dsimp [MT]
    positivity
  -- 3 M_T sigma2 - C M_T = sigma2 M_T  =>  2 sigma2 M_T = C M_T  => sigma2 = C/2
  have hsub : 2 * MT A R * sigma2 = (4 * Real.pi * G * A) * MT A R := by
    linarith
  have hdiv : 2 * sigma2 = 4 * Real.pi * G * A := by
    exact (mul_right_inj' hMTne).mp (by
      ring_nf at hsub ⊢
      linarith)
  field_simp
  linarith

/-- V6: the coefficient shift 3 -> 2 IS the boundary term.  The virial
  closure differs between reading A (RHS = 0) and reading B (RHS = boundary)
  by exactly the boundary term; evaluated at the fluid solution sigma^2 = C/2
  the boundary term is (C/2) * M_T.  (C := 4*pi*G*A.) -/
theorem coefficient_shift_is_boundary (G A R : ℝ) (hG : 0 < G) (hA : 0 < A) (hR : 0 < R) :
    3 * (((4 * Real.pi * G * A) / 2) * A / R ^ 2) * (4 * Real.pi * R ^ 3 / 3) =
    ((4 * Real.pi * G * A) / 2) * MT A R := by
  rw [boundary_term A R ((4 * Real.pi * G * A) / 2) hA hR]

/-#
  KILL condition (same as Q007): if the G081 relaxation/stability N-body
  finds the sector relaxes to sigma^2 != C/2 (K001 currently relaxes to
  0.53 R0, no attractor), the hydrostatic/virial reading is wrong even if
  this algebra stands.  The algebra is footing-independent; the dynamics
  is the test.
-/
#print axioms boundary_term
#print axioms wself_closed_form
#print axioms readingA_collisionless
#print axioms readingB_fluid
#print axioms coefficient_shift_is_boundary
#check MT
#check boundary_term
#check wself_closed_form
#check readingA_collisionless
#check readingB_fluid
#check coefficient_shift_is_boundary
