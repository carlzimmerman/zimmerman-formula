import Mathlib
import Mathlib.Tactic

/-
  AS059 -- Deep coefficient in a general static action (Lean 4 certificate).

  Action class (the task's mathematical object):
      E[Phi] = A s^2 int K(|grad Phi|/s) dV + B int rho Phi dV
  variation gives the E-L equation
      div[ A (K'(Y)/Y) grad Phi ] = B rho ,     Y = |grad Phi|/s ,
  and the response after normalization is  mu(Y) = K'(Y)/(2Y)  (so the flux
  coefficient is 2A mu).  Frozen-vacuum boundary conditions K(0)=K'(0)=0 and
  mu(0)=0 kill the linear and quadratic terms of K, leaving the CUBIC deep
  coefficient k3 to set the deep response slope:  mu(Y) = (3 k3 / 2) Y,
  n = mu'(0) = 3 k3 / 2.

  Formalized content (all pure real algebra; the physics mapping is in
  derivation.md):
    R1  response expansion: K'(Y)/(2Y) = k1/(2Y) + k2 + (3 k3/2) Y    (Y ≠ 0)
    R2  frozen vacuum (k1 = k2 = 0):  K'(Y)/(2Y) = (3 k3/2) Y          (Y ≠ 0)
    R3  deep slope set by the cubic coefficient: (d/dY)[(3 k3/2) Y] at 0 = 3 k3/2
    R4  NEGATIVE CONTROL (k2): the quadratic offset term contributes ZERO to the
        deep slope: (d/dY)[(3 k3/2) Y + k2] at 0 = 3 k3/2 for every k2
    R5  deep matching: 4 pi r^2 (2A mu g) = B M with mu = n g/s gives
        g^2 = B M s / (8 pi A n r^2)
    R6  the combination that sets kappa: if a0 = B s/(8 pi A G n) then
        kappa = a0/s = B/(8 pi A G n)
    R7  conditional landing: with the Newtonian normalization B = 8 pi A G and
        the adopted count n = 2, kappa = 1/2  (condition depends on the inputs;
        the action class alone does not remove the freedom -- R9)
    R8  cubic form: with B = 8 pi A G and n = 3 k3/2, kappa = 2/(3 k3)
    R9  COUNTEREXAMPLE TO UNIQUENESS: the action class realizes EVERY coefficient:
        for any kap0 (nonzero), the inputs (B = 8 pi A G, n = 1/kap0) give
        kappa = kap0 exactly -- the general static action fixes NO coefficient
    R10 slope freedom is one real parameter: 1/n1 = 1/n2 with n1, n2 != 0
        implies n1 = n2 (distinct slopes give distinct coefficients)
-/

noncomputable section
open Real

/-- kappa = a0/s (dimensionless deep coefficient of the matched a0-line). -/
def kappaOf (a0 s : ℝ) : ℝ := a0 / s

/- R1: response expansion of the order-3 kinetic K(Y) = k3 Y^3 + k2 Y^2 + k1 Y + k0:
   K'(Y)/(2Y) = k1/(2Y) + k2 + (3 k3/2) Y  for Y != 0. -/
theorem response_expansion (k1 k2 k3 Y : ℝ) (hY : Y ≠ 0) :
    (3 * k3 * Y ^ 2 + 2 * k2 * Y + k1) / (2 * Y) = k1 / (2 * Y) + k2 + (3 * k3 / 2) * Y := by
  field_simp [hY] <;> ring

/- R2: frozen vacuum (k1 = k2 = 0): the deep response is linear, slope 3 k3/2. -/
theorem deep_response_frozen_vacuum (k3 Y : ℝ) (hY : Y ≠ 0) :
    (3 * k3 * Y ^ 2) / (2 * Y) = (3 * k3 / 2) * Y := by
  field_simp [hY] <;> ring

/- R3: the deep slope is set by the CUBIC coefficient k3. -/
theorem deep_slope_set_by_cubic (k3 : ℝ) :
    HasDerivAt (fun Y : ℝ => (3 * k3 / 2) * Y) (3 * k3 / 2) 0 := by
  simpa using ((hasDerivAt_id (x := 0)).const_mul (3 * k3 / 2))

/- R4 NEGATIVE CONTROL: the quadratic coefficient k2 contributes zero to the slope. -/
theorem quadratic_offset_irrelevant (k3 k2 : ℝ) :
    HasDerivAt (fun Y : ℝ => (3 * k3 / 2) * Y + k2) (3 * k3 / 2) 0 := by
  have h1 : HasDerivAt (fun Y : ℝ => (3 * k3 / 2) * Y) (3 * k3 / 2) 0 :=
    deep_slope_set_by_cubic k3
  have h2 : HasDerivAt (fun Y : ℝ => k2) 0 0 := hasDerivAt_const 0 k2
  have hsum : HasDerivAt ((fun Y : ℝ => (3 * k3 / 2) * Y) + (fun Y : ℝ => k2))
      ((3 * k3 / 2) + 0) 0 := h1.add h2
  have hval : (3 * k3 / 2) + 0 = 3 * k3 / 2 := by ring
  rw [hval] at hsum
  exact hsum

/- R5: deep matching from the flux balance (point mass, spherical, mu = n g/s):
   the a0-line g^2 = (B s/(8 pi A n)) (M/r^2) follows. -/
theorem deep_line_from_flux (g s n A B M r : ℝ) (hn : n ≠ 0) (hs : s ≠ 0)
    (hr : r ≠ 0) (hA : A ≠ 0) (hM : M ≠ 0)
    (hflux : n * g ^ 2 / s = B * M / (8 * Real.pi * A * r ^ 2)) :
    g ^ 2 = B * M * s / (8 * Real.pi * A * n * r ^ 2) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  calc
    g ^ 2 = n * g ^ 2 / s * (s / n) := by field_simp [hn, hs]
    _ = (B * M / (8 * Real.pi * A * r ^ 2)) * (s / n) := by rw [hflux]
    _ = B * M * s / (8 * Real.pi * A * n * r ^ 2) := by
      field_simp [hflux, hn, hs, hr, hA, hpi] <;> ring

/- R6: the combination of A, B and the deep slope (cubic coefficient) that sets
   kappa:  a0 = B s/(8 pi A G n)  =>  kappa = a0/s = B/(8 pi A G n). -/
theorem kappa_combination (a0 s A B G n : ℝ) (hA0 : a0 = B * s / (8 * Real.pi * A * G * n))
    (hs : s ≠ 0) (hA : A ≠ 0) (hG : G ≠ 0) (hn : n ≠ 0) :
    kappaOf a0 s = B / (8 * Real.pi * A * G * n) := by
  unfold kappaOf
  rw [hA0]
  field_simp [hA, hG, hn, hs, Real.pi_ne_zero] <;> ring

/- R7 conditional landing: Newtonian normalization B = 8 pi A G and the adopted
   channel count n = 2 give kappa = 1/2.  The inputs (B, n) are conditions, not
   consequences of the action class (R9 shows the class alone fixes nothing). -/
theorem kappa_half_conditional (a0 s A B G : ℝ) (hB : B = 8 * Real.pi * A * G)
    (hA0 : a0 = B * s / (8 * Real.pi * A * G * 2)) (hs : s ≠ 0)
    (hA : A ≠ 0) (hG : G ≠ 0) : kappaOf a0 s = 1 / 2 := by
  have hk := kappa_combination a0 s A B G 2 hA0 hs hA hG (by norm_num : (2 : ℝ) ≠ 0)
  rw [hk, hB]
  field_simp [hA, hG, Real.pi_ne_zero] <;> ring

/- R8 cubic form: with B = 8 pi A G and the slope-cubic relation n = 3 k3/2,
   kappa = 2/(3 k3) -- the cubic deep coefficient sets kappa once the
   normalization and the slope are given. -/
theorem kappa_from_cubic (a0 s A B G k3 : ℝ) (hB : B = 8 * Real.pi * A * G)
    (hA0 : a0 = B * s / (8 * Real.pi * A * G * (3 * k3 / 2)))
    (hs : s ≠ 0) (hA : A ≠ 0) (hG : G ≠ 0) (hk : k3 ≠ 0) :
    kappaOf a0 s = 2 / (3 * k3) := by
  have h32 : (3 : ℝ) * k3 / 2 ≠ 0 := by
    exact div_ne_zero (mul_ne_zero (by norm_num : (3 : ℝ) ≠ 0) hk) (by norm_num : (2 : ℝ) ≠ 0)
  have hkres := kappa_combination a0 s A B G (3 * k3 / 2) hA0 hs hA hG h32
  rw [hkres, hB]
  field_simp [hA, hG, hk, Real.pi_ne_zero] <;> ring

/- R9 COUNTEREXAMPLE TO UNIQUENESS: the general static action realizes EVERY
   coefficient: given kap0 != 0, take n = 1/kap0 and B = 8 pi A G; then
   kappa = kap0 exactly.  The action class therefore removes no independent
   freedom; kappa = 1/2 is an input (adopted), not a derived result. -/
theorem any_kappa_realized (kap0 s A G : ℝ) (hk0 : kap0 ≠ 0) (hs : s ≠ 0)
    (hA : A ≠ 0) (hG : G ≠ 0) :
    kappaOf ((8 * Real.pi * A * G) * s / (8 * Real.pi * A * G * (1 / kap0))) s = kap0 := by
  unfold kappaOf
  field_simp [hk0, hs, hA, hG, Real.pi_ne_zero] <;> ring

/- R10: the deep-slope freedom is one real parameter: distinct slopes give
   distinct coefficients (the diagnostic lambdas at kappa = 1/2, 1, 2 require
   slopes n = 2, 1, 1/2 -- pairwise distinct). -/
theorem slope_injects_into_coefficient (n1 n2 : ℝ) (hn1 : n1 ≠ 0) (hn2 : n2 ≠ 0)
    (h : 1 / n1 = 1 / n2) : n1 = n2 := by
  have hc : 1 / (1 / n1) = 1 / (1 / n2) := congrArg (fun x : ℝ => 1 / x) h
  field_simp [hn1, hn2] at hc
  exact hc

#check deep_slope_set_by_cubic
#check quadratic_offset_irrelevant
#check deep_line_from_flux
#check kappa_combination
#check kappa_half_conditional
#check kappa_from_cubic
#check any_kappa_realized
#check slope_injects_into_coefficient

#print axioms deep_slope_set_by_cubic
#print axioms quadratic_offset_irrelevant
#print axioms deep_line_from_flux
#print axioms kappa_combination
#print axioms kappa_half_conditional
#print axioms kappa_from_cubic
#print axioms any_kappa_realized
#print axioms slope_injects_into_coefficient