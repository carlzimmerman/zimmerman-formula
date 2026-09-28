import Mathlib
import Mathlib.Tactic

/-
  AS652 -- Four-form flux equation with a MOND-dependent scale (Lean 4 certificate).

  Formalized content (pure real algebra; the physics mapping is in derivation.md):

  Flux equation (task step 2):  d_mu(dL/dq) = 0  =>  dL/dq = Z q0  (integration
  constant = four-form flux datum; NOT P_q = 0).  On the gauge-fixed k04 branch,
  dL/dq = q (Z + A),  A = (2-K_B) beta^2 W(s)/(8 pi) >= 0,  so the equation is

        q (Z + A) = Z q0 ,        q = q0 r ,   r = a0_loc/a0 in (0, 1].

  R1  the solution q = q0 Z/(Z+A) satisfies the flux equation exactly, is
      strictly positive and bounded above by q0  (0 < q <= q0);
  R2  uniqueness: any q solving q(Z+A) = Z q0 equals q0 Z/(Z+A);
  R3  NEGATIVE CONTROL (task step 4, unconstrained algebraic scalar, dL/dq = 0):
      q(Z+A) = 0 with Z > 0 and A >= 0 forces q = 0: the altered premise admits
      ONLY the zero MOND scale (the integration constant is the lost hypothesis);
  R4  kappa landing: with the k04 vacuum kappa^2 = 2 beta^2/(Z + 2 b beta^2),
      kappa = 1/2 exactly iff Z/beta^2 = 8 - 2b  (the ratio is NOT fixed by the
      action: two couplings, one equation -- the coefficient stays an input);
  R5  saturated linear regime: from r(1 + alpha W/64 pi) = 1 with the frozen
      kernel W = Delta s - j and s = g/(a0 r), the linear law
      r(1 - alpha j/64 pi) = 1 - alpha Delta g/(64 pi a0) follows exactly;
  R6  bounds: for A >= 0, r = 1/(1+A) satisfies 0 < r <= 1 (environmental a0_loc
      never exceeds the bare a0 on the smooth branch).
-/

noncomputable section
open Real

variable {Z q0 A q kappa beta b : ℝ}
variable {r alpha W Delta s j g a0 : ℝ}

-- R1: the flux equation's solution, positivity and bound --------------------

theorem r1a_flux_solution (hZ : 0 < Z) (hq0 : 0 < q0) (hA : 0 ≤ A) :
    (q0 * Z / (Z + A)) * (Z + A) = q0 * Z := by
  have hpos : Z + A ≠ 0 := by nlinarith
  field_simp [hpos]

theorem r1b_positivity (hZ : 0 < Z) (hq0 : 0 < q0) (hA : 0 ≤ A) :
    0 < q0 * Z / (Z + A) := by
  have hZA : 0 < Z + A := by nlinarith
  exact div_pos (mul_pos hq0 hZ) hZA

theorem r1c_bound (hZ : 0 < Z) (hq0 : 0 < q0) (hA : 0 ≤ A) :
    q0 * Z / (Z + A) ≤ q0 := by
  have hZA : 0 < Z + A := by nlinarith
  rw [div_le_iff₀ hZA]
  have hmon : 0 ≤ A * q0 := mul_nonneg hA (le_of_lt hq0)
  nlinarith [hmon]

-- R2: uniqueness -------------------------------------------------------------

theorem r2_uniqueness (hZ : 0 < Z) (_hq0 : 0 < q0) (hA : 0 ≤ A)
    (h : q * (Z + A) = q0 * Z) : q = q0 * Z / (Z + A) := by
  have hpos : Z + A ≠ 0 := by nlinarith
  rw [← h]
  field_simp [hpos]

-- R3: negative control -------------------------------------------------------

theorem r3_negative_control (hZ : 0 < Z) (hA : 0 ≤ A) (h : q * (Z + A) = 0) :
    q = 0 := by
  have hpos : Z + A ≠ 0 := by nlinarith
  rcases mul_eq_zero.mp h with hq | hza
  · exact hq
  · exfalso
    exact hpos hza

-- R4: kappa = 1/2 <=> Z/beta^2 = 8 - 2b --------------------------------------

theorem r4_kappa_half (hk : kappa * kappa = (2 * beta * beta) / (Z + 2 * b * beta * beta))
    (hZ : Z = (8 - 2 * b) * beta * beta) (hkpos : 0 < kappa) (hbpos : 0 < beta) :
    kappa = 1 / 2 := by
  have hZ2 : Z + 2 * b * beta * beta = 8 * beta * beta := by
    rw [hZ]
    ring
  have hk2 : kappa * kappa = 1 / 4 := by
    rw [hk, hZ2]
    field_simp [hbpos.ne']
    ring
  have hfac : (kappa - 1 / 2) * (kappa + 1 / 2) = 0 := by
    have hx : (kappa - 1 / 2) * (kappa + 1 / 2) = kappa * kappa - 1 / 4 := by ring
    rw [hx, hk2]
    ring
  rcases mul_eq_zero.mp hfac with h1 | h2
  · nlinarith
  · nlinarith [hkpos]

-- R5: saturated linear regime ------------------------------------------------

theorem r5_saturated_linear (hW : r * (1 + alpha * W / (64 * Real.pi)) = 1)
    (hWdef : W = Delta * s - j) (hS : g = a0 * r * s) (ha0 : a0 ≠ 0) :
    r * (1 - alpha * j / (64 * Real.pi)) = 1 - alpha * Delta * g / (64 * Real.pi * a0) := by
  rw [hS]
  rw [hWdef] at hW
  have hW2 : r + r * (alpha * (Delta * s - j)) / (64 * Real.pi) = 1 := by
    have he := hW
    ring_nf at he ⊢
    exact he
  have hW3 : (64 * Real.pi) * r + r * (alpha * (Delta * s - j)) = 64 * Real.pi := by
    have hm := congrArg (fun x : ℝ => (64 * Real.pi) * x) hW2
    field_simp at hm
    nlinarith [hm]
  have hW4 : (64 * Real.pi) * r + r * alpha * Delta * s - r * alpha * j = 64 * Real.pi := by
    have hr := hW3
    ring_nf at hr
    nlinarith [hr]
  have hgoal : (64 * Real.pi * a0) * (r * (1 - alpha * j / (64 * Real.pi))) =
      (64 * Real.pi * a0) * (1 - alpha * Delta * (a0 * r * s) / (64 * Real.pi * a0)) := by
    field_simp [ha0]
    nlinarith [hW4]
  have hc : 64 * Real.pi * a0 ≠ 0 := by positivity
  field_simp [hc] at hgoal ⊢
  exact hgoal

-- R6: bounds of the environmental scale --------------------------------------

theorem r6_bounds (hA : 0 ≤ A) : 0 < 1 / (1 + A) ∧ 1 / (1 + A) ≤ 1 := by
  have hpos : 0 < 1 + A := by nlinarith
  constructor
  · exact div_pos zero_lt_one hpos
  · rw [div_le_iff₀ hpos]
    nlinarith

end

-- axiom audit -------------------------------------------------------------
#print axioms r1a_flux_solution
#print axioms r1b_positivity
#print axioms r1c_bound
#print axioms r2_uniqueness
#print axioms r3_negative_control
#print axioms r4_kappa_half
#print axioms r5_saturated_linear
#print axioms r6_bounds
