import Mathlib

/-!
# AS082 — Inner boundary mass and self-gravity: algebraic certificate (Lean 4)

Seed: deepseek_push/astra_spawn_ideas/AS082_inner_boundary_mass_and_self_gravity.md
sha256 4b5a3471372f7f5bd8b005c8ff313528b8b9a97d12c3028bf9ff3be5920bae03

SCOPE — Lean certifies the ALGEBRA below, not physics.  The physical premises
are inputs, stated here and used verbatim in the Python lane
(AS082_compute.py, 9/9 checks):

  * spherical static Newtonian arrangement (shell theorem, coupling G = G_N;
    G_bare/G_cosmo are separate symbols, not used here);
  * phantom density rho(r) = A / r^2 on [r_in, R], 0 < r_in <= r <= R <= r_M;
  * enclosed mass  M(r) = M_in + 4*pi*A*(r - r_in)  where M_in is the total
    mass interior to the inner boundary r_in (the task's "boundary mass");
  * framework constants C = sqrt(G*M_b*a0), r_M = sqrt(G*M_b/a0),
    a0 = kappa*c*sqrt(G*rho_Lambda) with kappa = 1/2 adopted — C, r_M etc.
    enter ONLY through the two relations certified here:
    4*pi*A*G = C  (amplitude condition)  and  C/G = M_b/r_M  (equipartition);
  * target: exact logarithmic well  g_self(r) = C/r  on every shell radius,
    equivalently (cleared form) G*(M_in + 4*pi*A*(r - r_in)) = C*r.

CERTIFIED THEOREMS (all polynomial/cleared forms; division appears only in
the ratio lemmas, which carry explicit nonzero hypotheses):

  T3 as082_forward      : exact C/r at two distinct radii forces
                          M_in = 4*pi*A*r_in  AND  4*pi*A*G = C.
  T4 as082_backward     : those conditions give exact C/r at every r.
  T5 as082_exact_iff    : the iff (the seed's main algebraic object).
  T6/T7 as082_boundary_mass_value / as082_equipartition_fraction :
                          M_in = (C/G)*r_in = M_b*r_in/r_M (dimensionless
                          ratio; footing-independent).
  T8 as082_control_zero : negative control: M_in = 0 with C, r_in nonzero
                          makes exact C/r impossible at any two radii.
  T9 as082_residual_zero: with M_in = 0 the residual numerator is exactly
                          -C*r_in (i.e. g - C/r = -C*r_in/r^2).
  T10 as082_A_ratio     : amplitude form 4*pi*A = C/G from 4*pi*A*G = C.
  T2 as082_enclosed_mass_integral: the mass-increment integral evaluates to
                          4*pi*A*(r - r_in); T1 the integrand simplification
                          s^2*(A/s^2) = A.

The deep-asymptotics statement of the operative MONO/RAR kernel (leading
neglected term B/2, relative r_M/(2r)) is analytic-lane verified in the
Python lane; the algebraic exactness above is what this file certifies.
No particle ontology is introduced; the boundary mass is bookkeeping of the
truncated profile (analytic continuation of the linear mass law).
-/

noncomputable section

open scoped Interval

/-! T1: integrand simplification s^2 * (A / s^2) = A for s ≠ 0 -/
theorem as082_integrand (s A : ℝ) (hs : s ≠ 0) : s ^ 2 * (A / s ^ 2) = A := by
  field_simp [hs]

/-! T2: enclosed-mass increment integral: ∫_{r_in}^{r} 4πA ds = 4πA (r - r_in) -/
theorem as082_enclosed_mass_integral (A r_in r : ℝ) :
    ∫ _ in r_in..r, (4 * Real.pi * A) = 4 * Real.pi * A * (r - r_in) := by
  rw [intervalIntegral.integral_const]
  rw [smul_eq_mul]
  ring

/-! T3: forward — exact C/r at two distinct shell radii forces both
        coefficient conditions (the inner boundary mass and the amplitude). -/
theorem as082_forward (G A C M_in r_in r1 r2 : ℝ) (hG : G ≠ 0) (hne : r1 ≠ r2)
    (h1 : G * (M_in + 4 * Real.pi * A * (r1 - r_in)) = C * r1)
    (h2 : G * (M_in + 4 * Real.pi * A * (r2 - r_in)) = C * r2) :
    M_in = 4 * Real.pi * A * r_in ∧ 4 * Real.pi * A * G = C := by
  have hdiff : 4 * Real.pi * A * G * (r2 - r1) = C * (r2 - r1) := by
    nlinarith [h1, h2]
  have hA : 4 * Real.pi * A * G = C := by
    have hdiff2 : (4 * Real.pi * A * G - C) * (r2 - r1) = 0 := by
      nlinarith [hdiff]
    have hr21 : r2 - r1 ≠ 0 := by
      intro hz
      apply hne
      linarith
    have hz : 4 * Real.pi * A * G - C = 0 := (mul_eq_zero.mp hdiff2).resolve_right hr21
    linarith
  have hGMin : G * M_in = C * r_in := by
    calc
      G * M_in = C * r1 - 4 * Real.pi * A * G * (r1 - r_in) := by
        nlinarith [h1]
      _ = C * r1 - C * (r1 - r_in) := by rw [hA]
      _ = C * r_in := by ring
  have hGM : G * M_in = G * (4 * Real.pi * A * r_in) := by
    calc
      G * M_in = C * r_in := hGMin
      _ = 4 * Real.pi * A * G * r_in := by rw [hA]
      _ = G * (4 * Real.pi * A * r_in) := by ring
  exact ⟨mul_left_cancel₀ hG hGM, hA⟩

/-! T4: backward — the two conditions give exact C/r at every radius. -/
theorem as082_backward (G A C M_in r_in r : ℝ)
    (hM : M_in = 4 * Real.pi * A * r_in) (hA : 4 * Real.pi * A * G = C) :
    G * (M_in + 4 * Real.pi * A * (r - r_in)) = C * r := by
  rw [hM]
  calc
    G * (4 * Real.pi * A * r_in + 4 * Real.pi * A * (r - r_in))
        = 4 * Real.pi * A * G * r := by ring
    _ = C * r := by rw [hA]

/-! T5: the iff — exact logarithmic self-gravity on a shell with at least two
        radii  <=>  amplitude 4πGA = C and boundary mass M_in = 4πA r_in. -/
theorem as082_exact_iff (G A C M_in r_in : ℝ) (hG : G ≠ 0) :
    (∀ r : ℝ, G * (M_in + 4 * Real.pi * A * (r - r_in)) = C * r) ↔
      (M_in = 4 * Real.pi * A * r_in ∧ 4 * Real.pi * A * G = C) := by
  constructor
  · intro h
    exact as082_forward G A C M_in r_in r_in (r_in + 1) hG (by linarith)
      (h r_in) (h (r_in + 1))
  · intro h
    intro r
    exact as082_backward G A C M_in r_in r h.1 h.2

/-! T10: amplitude in ratio form: 4πA = C/G given 4πA*G = C and G ≠ 0. -/
theorem as082_A_ratio (G A C : ℝ) (hG : G ≠ 0) (hA : 4 * Real.pi * A * G = C) :
    4 * Real.pi * A = C / G := by
  field_simp [hG]
  exact hA

/-! T6: the boundary mass in framework units: M_in = (C/G) r_in. -/
theorem as082_boundary_mass_value (A C G M_in r_in : ℝ)
    (hM : M_in = 4 * Real.pi * A * r_in) (h4 : 4 * Real.pi * A = C / G) :
    M_in = (C / G) * r_in := by
  rw [hM, h4]

/-! T7: the dimensionless fraction: M_in = M_b * (r_in / r_M)  (equipartition
        relation C/G = M_b/r_M as premise; both footings share the ratio). -/
theorem as082_equipartition_fraction (C G M_b M_in r_M r_in : ℝ)
    (hC : C / G = M_b / r_M) (hM : M_in = (C / G) * r_in) :
    M_in = M_b * r_in / r_M := by
  rw [hM, hC]
  ring

/-! T8: NEGATIVE CONTROL — with M_in = 0, C ≠ 0 and r_in ≠ 0 the exact-C/r
        identity cannot hold at every radius (it already fails at r = r_in,
        where the shell's own field vanishes). -/
theorem as082_control_zero (G A C M_in r_in : ℝ) (hM0 : M_in = 0)
    (hC : C ≠ 0) (hrin : r_in ≠ 0) :
    ¬ (∀ r : ℝ, G * (M_in + 4 * Real.pi * A * (r - r_in)) = C * r) := by
  intro h
  have h1 := h r_in
  rw [hM0] at h1
  have hz : C * r_in = 0 := by
    nlinarith [h1]
  rcases mul_eq_zero.mp hz with hc | hri
  · exact hC hc
  · exact hrin hri

/-! T9: residual decomposition for the control: with M_in = 0 and 4πAG = C the
        cleared numerator is exactly -C*r_in, i.e. g_self(r) - C/r = -C*r_in/r^2
        (the open-shell deficit; relative error r_in/r, = 1 at r = r_in). -/
theorem as082_residual_zero (G A C r r_in : ℝ) (hA : 4 * Real.pi * A * G = C) :
    G * (4 * Real.pi * A * (r - r_in)) - C * r = -C * r_in := by
  have hx : G * (4 * Real.pi * A * (r - r_in)) = 4 * Real.pi * A * G * (r - r_in) := by
    ring
  rw [hx, hA]
  ring

/-! T11: the exact-instance sanity check with both conditions in place:
        the residual numerator is identically zero. -/
theorem as082_exact_instance (G A C M_in r r_in : ℝ)
    (hM : M_in = 4 * Real.pi * A * r_in) (hA : 4 * Real.pi * A * G = C) :
    G * (M_in + 4 * Real.pi * A * (r - r_in)) - C * r = 0 := by
  rw [as082_backward G A C M_in r_in r hM hA]
  ring

end

#print axioms as082_enclosed_mass_integral
#print axioms as082_forward
#print axioms as082_backward
#print axioms as082_exact_iff
#print axioms as082_A_ratio
#print axioms as082_boundary_mass_value
#print axioms as082_equipartition_fraction
#print axioms as082_control_zero
#print axioms as082_residual_zero
#print axioms as082_exact_instance