/-
  FINAL-17 (KAPPA_A) -- the load-bearing algebra of the self-source / capacity route.

  Lane: FINAL MILE, lane FINAL-17 (KAPPA_A), hy4_preview_push.  2026-11-11.
  TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing.
  Footings never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2).
  kappa = 1/2 FITTED; not theory closed.

  THE ROUTE.  Write the canonical law as

      g_N = g^2 / (g + a0),        u := g - g_N   (the cold component's own field),

  so that (S1) u = a0*g/(g+a0), (S2) u/a0 = nu/(1+nu) with nu := g/a0,
  (S3) 0 < u < a0 for a0,g > 0 -- the CAPACITY is a0 -- and (S4) the deficiency
  a0 - u = a0^2/(g+a0) vanishes only in the limit g -> infinity.

  THE LOAD-BEARING STEP (this file's point).  The capacity condition is
  NORMALISATION-BLIND.  Under the one-parameter group

      G_lam :  (a0, g, g_N, u) -> (lam*a0, lam*g, lam*g_N, lam*u),
               c, G, rho_Lambda, M_b, r  fixed,

  every relation of the route is covariant:  (T5) u(lam a0, lam g) = lam u(a0,g)
  and (T6) the SHAPE u/a0 is invariant.  Hence the capacity statement
  "sup u = a0" is the single equation a0 = a0, and in

      a0 = kappa * c * sqrt(G * rho_Lambda)

  kappa -> lam * kappa is the ONLY charged quantity.  There is no G_lam-invariant
  in the route's data to fix the orbit coordinate: kappa is a flat direction of
  the self-source/capacity route.  This is the third independent channel to reach
  that conclusion (FINAL-16 J1 reached it for the formation reading; FINAL-16 J3
  for the kernel family index).

  THE HALF THAT DOES SURVIVE (Q1 = DERIVED).  On the saturated branch
  rho_c = a0/(2 pi G r) the enclosed mass is M_c(r) = (a0/G) r^2 and the route
  closes: (T8) Poisson, dM_c/dr = 4 pi r^2 rho_c; (T9) the field G M_c/r^2 = a0
  -- the configuration sits EXACTLY at the capacity; (T10) the universal column
  M_c/(pi r^2) = a0/(pi G).  All three are a0-free in shape and none evaluates
  a0 against cosmology.

  BRANCH DISTINCTNESS (AG4 G3, re-verified in this lane's variables).  For the
  capacity family u^2 + n gbar u = a0 gbar the canonical law's own u solves the
  n = 1 member (T11) and leaves the residual gbar*u = a0 g^3/(g+a0)^2 > 0 in the
  n = 2 member (T12/T13): the quadratic a0-line is a different theory.
-/

import Mathlib

noncomputable section

/-- the cold component's own field: total minus baryonic. -/
def phantom (a0 g : ℝ) : ℝ := g - g ^ 2 / (g + a0)

/-- the baryonic (Newtonian) field of the canonical law. -/
def gbar (a0 g : ℝ) : ℝ := g ^ 2 / (g + a0)

/-- the enclosed cold mass on the saturated (deep) branch. -/
def Mc (a0 G r : ℝ) : ℝ := (a0 / G) * r ^ 2

-- S1-S4 : the capacity is a0, and the shape carries no a0

/-- (S1)  u = a0*g/(g+a0) : the load-bearing algebraic step, in isolation. -/
theorem phantom_eq (a0 g : ℝ) (hg : g + a0 ≠ 0) :
    phantom a0 g = a0 * g / (g + a0) := by
  unfold phantom
  field_simp [hg] <;> ring

/-- (S4)  the capacity deficiency: a0 - u = a0^2/(g+a0) > 0, so u < a0 strictly
    and the ceiling is approached only as g -> infinity. -/
theorem phantom_deficiency (a0 g : ℝ) (hg : g + a0 ≠ 0) :
    a0 - phantom a0 g = a0 ^ 2 / (g + a0) := by
  rw [phantom_eq a0 g hg]
  field_simp [hg] <;> ring

/-- (S3a)  the cold field is positive wherever the total field and a0 are. -/
theorem phantom_pos (a0 g : ℝ) (ha0 : 0 < a0) (hg : 0 < g) :
    0 < phantom a0 g := by
  have hden : 0 < g + a0 := by linarith
  rw [phantom_eq a0 g (ne_of_gt hden)]
  positivity

/-- (S3b)  THE CAPACITY: u < a0 for every g > 0.  The cold component's own
    self-gravity saturates at a0 -- and at nothing else. -/
theorem phantom_capacity (a0 g : ℝ) (ha0 : 0 < a0) (hg : 0 < g) :
    phantom a0 g < a0 := by
  have hden : 0 < g + a0 := by linarith
  rw [phantom_eq a0 g (ne_of_gt hden)]
  rw [div_lt_iff₀ hden]
  nlinarith [sq_pos_of_pos ha0]

-- T5-T6 : the load-bearing step -- the capacity condition is
-- NORMALISATION-BLIND, so kappa is a flat direction

/-- (T5)  covariance of the cold field under G_lam: u carries weight 1. -/
theorem phantom_covariant (a0 g lam : ℝ) (hl : lam ≠ 0) (hg : g + a0 ≠ 0) :
    phantom (lam * a0) (lam * g) = lam * phantom a0 g := by
  unfold phantom
  have hden : lam * g + lam * a0 = lam * (g + a0) := by ring
  rw [hden]
  field_simp [hl, hg]

/-- (T6)  the response SHAPE u/a0 is G_lam-INVARIANT: everything the route
    determines about the cold component's response is a0-free.  This is why the
    capacity condition can pin the shape but never the normalisation. -/
theorem phantom_shape_invariant (a0 g lam : ℝ) (ha0 : a0 ≠ 0) (hl : lam ≠ 0)
    (hg : g + a0 ≠ 0) :
    phantom (lam * a0) (lam * g) / (lam * a0) = phantom a0 g / a0 := by
  rw [phantom_covariant a0 g lam hl hg]
  field_simp [ha0, hl]

/-- (T7)  the capacity statement itself is weight-1: under G_lam the bound
    u < a0 becomes lam*u < lam*a0.  It is preserved for every lam, i.e. it is
    the equation a0 = a0 and selects no value of a0 (hence none of kappa). -/
theorem capacity_bound_covariant (a0 g lam : ℝ) (hl : lam ≠ 0) (hg : g + a0 ≠ 0) :
    (lam * a0) - phantom (lam * a0) (lam * g) = lam * (a0 - phantom a0 g) := by
  rw [phantom_covariant a0 g lam hl hg]
  ring

-- T8-T10 : what the route DOES derive -- the saturated self-sourced branch

/-- (T8)  Poisson on the saturated branch: the enclosed mass's radial derivative
    is exactly 4 pi r^2 rho_c with rho_c = a0/(2 pi G r). -/
theorem saturated_poisson (a0 G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    2 * a0 * r / G = 4 * Real.pi * r ^ 2 * (a0 / (2 * Real.pi * G * r)) := by
  have hpi : (Real.pi : ℝ) ≠ 0 := by positivity
  field_simp [hG, hr, hpi] <;> ring

/-- (T9)  the self-sourced configuration sits EXACTLY at the capacity:
    G M_c(r)/r^2 = a0 for every r.  The route's one real output. -/
theorem saturated_field (a0 G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    G * Mc a0 G r / r ^ 2 = a0 := by
  unfold Mc
  field_simp [hG, hr]

/-- (T10)  the universal column of the saturated branch: M_c/(pi r^2) = a0/(pi G)
    (= 213.7 Msun/pc^2 on the canonical footing; AG4's n=1 capacity ceiling). -/
theorem saturated_column (a0 G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    Mc a0 G r / (Real.pi * r ^ 2) = a0 / (Real.pi * G) := by
  have hpi : (Real.pi : ℝ) ≠ 0 := by positivity
  unfold Mc
  field_simp [hG, hr, hpi]

-- T11-T13 : branch distinctness -- the canonical law is the n = 1 member,
-- the quadratic a0-line is the n = 2 member, a different theory

/-- (T11)  the canonical law's own cold field solves the n = 1 rest state
    u^2 + gbar u = a0 gbar exactly (AG4's capacity family at n = 1). -/
theorem canonical_is_n1_rest_state (a0 g : ℝ) (hg : g + a0 ≠ 0) :
    (phantom a0 g) ^ 2 + (gbar a0 g) * (phantom a0 g) - a0 * (gbar a0 g) = 0 := by
  unfold phantom gbar
  field_simp [hg] <;> ring

/-- (T12)  the SAME field leaves a nonzero residual in the n = 2 member:
    u^2 + 2 gbar u - a0 gbar = a0 g^3/(g+a0)^2.  The quadratic a0-line is
    therefore not the canonical rest state. -/
theorem canonical_n2_residual (a0 g : ℝ) (hg : g + a0 ≠ 0) :
    (phantom a0 g) ^ 2 + 2 * (gbar a0 g) * (phantom a0 g) - a0 * (gbar a0 g)
      = a0 * g ^ 3 / (g + a0) ^ 2 := by
  unfold phantom gbar
  field_simp [hg] <;> ring

/-- (T13)  that residual is strictly positive for a0, g > 0: the two branches
    cannot be confused, so no n = 2 argument can be used to fix the canonical
    coefficient. -/
theorem canonical_n2_residual_pos (a0 g : ℝ) (ha0 : 0 < a0) (hg : 0 < g) :
    0 < (phantom a0 g) ^ 2 + 2 * (gbar a0 g) * (phantom a0 g) - a0 * (gbar a0 g) := by
  have hden : g + a0 ≠ 0 := by
    have : 0 < g + a0 := by linarith
    exact ne_of_gt this
  rw [canonical_n2_residual a0 g hden]
  positivity

end

#print axioms phantom_eq
#print axioms phantom_deficiency
#print axioms phantom_pos
#print axioms phantom_capacity
#print axioms phantom_covariant
#print axioms phantom_shape_invariant
#print axioms capacity_bound_covariant
#print axioms saturated_poisson
#print axioms saturated_field
#print axioms saturated_column
#print axioms canonical_is_n1_rest_state
#print axioms canonical_n2_residual
#print axioms canonical_n2_residual_pos
