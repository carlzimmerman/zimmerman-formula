import Mathlib

-- ============================================================================
-- AS039 — Deep homogeneity of the static energy (Zimmerman gravity framework)
-- Run dir: deepseek_push/astra_spawn_ideas/results/AS039/AS039-r1-20260928T0328Z-dsv4f-hermes
--
-- Framework cell: a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ADOPTED (input).
-- Branches Q, RAR, MU2, EXP, MONO share the AQUAL primitive
--     F(X) = int_0^X mu(sqrt(t)) dt,  X = |grad Phi|^2 / a0^2,
-- and the deep (X -> 0+) asymptote  mu(s) ~ s  =>  F(X) ~ (2/3) X^(3/2).
-- The pure deep primitive is F0(X) = (2/3) X sqrt(X).
--
-- Certified here (algebra; the deriv content is carried numerically/lane-side
-- because this lean_2026 build has no Real.hasDerivAt_sqrt):
--   1. deep_energy_homogeneity_degree_three : F0(lam^2 X) = lam^3 F0(X)
--      for all lam >= 0, X >= 0 -- exact homogeneity degree 3 in the field
--      amplitude, i.e. 3/2 in X. (Step 2 of AS039: scaling under
--      grad Phi -> lam grad Phi.)
--   2. deep_energy_density_identity : the deep energy density
--      eps = (a0^2/8pi G) F0(g^2/a0^2) = g^3/(12 pi G a0)  (g >= 0, a0 > 0).
--   3. deep_force_square : spherical field equation g*mu(g/a0) = B with
--      mu(s) = s gives g^2 = a0 B (deep-MOND force law, g >= 0 side included
--      in the field equation identity).
--   4. deep_btfr : g = v^2/r, B = G M/r^2, g^2 = a0 B  =>  v^4 = G M a0.
--   5. q_branch_line_identity : y = (sqrt(1+4x^2)-1)/2 (the Q-branch inverse
--      mu) satisfies y^2 + y = x^2, x >= 0 -- the g^2 = B^2 + a0 B line.
-- ============================================================================

noncomputable section

open Real

/-- Pure deep static-energy primitive: F0(X) = (2/3) X sqrt(X). -/
def F0 (X : ℝ) : ℝ := (2 / 3 : ℝ) * X * √X

/-- Theorem 1 (AS039 step 2): deep energy is exactly homogeneous of degree 3
    under field rescaling  Phi -> lam*Phi  (X -> lam^2 X):
        F0(lam^2 * X) = lam^3 * F0(X)   for all lam >= 0, X >= 0. -/
theorem deep_energy_homogeneity_degree_three {lam X : ℝ} (hlam : 0 ≤ lam) (hX : 0 ≤ X) :
    F0 (lam ^ 2 * X) = lam ^ 3 * F0 X := by
  unfold F0
  have hsqrt : √(lam ^ 2 * X) = lam * √X := by
    rw [Real.sqrt_mul' (lam ^ 2) hX]
    rw [Real.sqrt_sq hlam]
  rw [hsqrt]
  ring

/-- Theorem 2: deep energy density from the primitive.
    eps = (a0^2 / 8 pi G) * F0(g^2/a0^2) = g^3 / (12 pi G a0). -/
theorem deep_energy_density_identity (g a0 G : ℝ) (hg : 0 ≤ g) (ha0 : 0 < a0)
    (hG : G ≠ 0) :
    (a0 ^ 2 / (8 * Real.pi * G)) * F0 (g ^ 2 / a0 ^ 2) = g ^ 3 / (12 * Real.pi * G * a0) := by
  unfold F0
  have hgdiv : 0 ≤ g / a0 := div_nonneg hg (le_of_lt ha0)
  have hsqrt : √(g ^ 2 / a0 ^ 2) = g / a0 := by
    have hsq : g ^ 2 / a0 ^ 2 = (g / a0) ^ 2 := by ring
    rw [hsq, Real.sqrt_sq hgdiv]
  rw [hsqrt]
  field_simp [hG, ha0.ne', Real.pi_ne_zero] <;> ring

/-- Theorem 3: deep spherical force law.  mu(s) = s in
    g * mu(g/a0) = B  gives  g^2 = a0 * B. -/
theorem deep_force_square (g a0 B : ℝ) (ha0 : a0 ≠ 0)
    (h : g * (g / a0) = B) : g ^ 2 = a0 * B := by
  field_simp [ha0] at h
  simpa [sq] using h

/-- Theorem 4: deep BTFR.  g = v^2/r, B = G M / r^2, g^2 = a0 B  =>  v^4 = G M a0. -/
theorem deep_btfr (v r M G a0 : ℝ) (hr : r ≠ 0)
    (h : (v ^ 2 / r) ^ 2 = a0 * (G * M / r ^ 2)) : v ^ 4 = G * M * a0 := by
  field_simp [hr] at h
  ring_nf at h
  simpa [mul_assoc, mul_comm, mul_left_comm] using h

/-- Theorem 5: Q-branch inverse identity.  With
    y = (sqrt(1 + 4 x^2) - 1) / 2  (so that g = x a0, B = y a0):
        y^2 + y = x^2,   i.e.  g^2 = B^2 + a0 B. -/
theorem q_branch_line_identity {x y : ℝ} (hx : 0 ≤ x)
    (h : y = (√(1 + 4 * x ^ 2) - 1) / 2) : y ^ 2 + y = x ^ 2 := by
  rw [h]
  have hs : (√(1 + 4 * x ^ 2)) ^ 2 = 1 + 4 * x ^ 2 := by
    exact Real.sq_sqrt (by positivity)
  nlinarith [hs]

end
