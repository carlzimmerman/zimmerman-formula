import Mathlib

/-!
# AS004 — Natural units and reduced Planck mass: algebraic certificates

SCOPE. Lean certifies the pure real-algebra core of
`deepseek_push/astra_spawn_ideas/AS004_natural_units_and_reduced_planck_mass.md`:

  in c = hbar = 1 units,  M_L^4 = epsilon_L,  M_Plot = G^(-1/2),
  Mbar_P = (8 pi G)^(-1/2),
        a0 = M_L^2 / (2 M_Plot) = M_L^2 / (2 sqrt(8 pi) Mbar_P),
  and the SI restoration
        a0 = (1/2) (c^3/hbar) M_L^2 / M_Plot,   M_L^4 = hbar^3 rho / c^3,
        M_Plot^2 = hbar c / G,
  are EXACTLY equivalent to the framework relation
        a0 = (1/2) c sqrt(G rho_Lambda)
  (kappa = 1/2 is an ADOPTED input; nothing here derives kappa).

All statements are plain identities in positive reals; units and the physics
(the kernel, the action, criterion B, the gates) live outside this file.  The
Negative Control of the task is the third theorem: substituting the reduced
Planck mass Mbar_P for M_Plot WITHOUT the sqrt(8 pi) factor changes a0 by the
factor sqrt(8 pi) ~ 5.0133; `reduced_trap_neq` certifies a0' != a0.

Theorems
* `framework_squared_iff`  — a0 = (c/2) sqrt(G rho)  <=>  4 a0^2 = G c^2 rho.
* `natural_units_core`     — with M_L^4 = eps, M_Plot^2 = 1/G:
                            a0 = M_L^2/(2 M_Plot) <=> 4 a0^2 = G eps.
* `si_restoration`         — the two representations are the same object:
                            (1/2)(c^3/hbar) M_L^2/M_Plot = (1/2) c sqrt(G rho)
                            for M_L^4 = hbar^3 rho/c^3, M_Plot^2 = hbar c/G.
* `framework_natural_iff`  — a0 equals the natural-units form iff it equals
                            the framework form (same prediction in equivalent
                            variables; no independent fitted input).
* `reduced_planck_mismatch_sq` — with Mbar_P^2 = 1/(8 pi G):
                            (M_L^2/(2 Mbar_P))^2 = 8 pi (M_L^2/(2 M_Plot))^2.
* `reduced_trap_neq`       — the wrong substitution gives a0' != a0
                            (NEGATIVE CONTROL fires).
* `footing_rescale`        — with kappa fixed, eps_a/eps_c = (a0_a/a0_c)^2:
                            both footings are the SAME identity with a
                            rescaled density, not a second kappa.
* `lambda_dictionary`      — a0 = c^2 sqrt(Lambda/(32 pi)) <=> Lambda =
                            32 pi a0^2/c^4 (geometric Lambda, coincident G).
-/

lemma eq_of_sq_eq {x y : ℝ} (hx : 0 < x) (hy : 0 < y) (h : x ^ 2 = y ^ 2) : x = y := by
  rcases sq_eq_sq_iff_eq_or_eq_neg.mp h with h1 | h2
  · exact h1
  · exfalso
    nlinarith [hx, hy, h2]

theorem framework_squared_iff {a0 c G ρ : ℝ} (ha0 : 0 < a0) (hc : 0 < c) (hG : 0 < G)
    (hρ : 0 < ρ) :
    a0 = (1 / 2 : ℝ) * c * Real.sqrt (G * ρ) ↔ 4 * a0 ^ 2 = G * c ^ 2 * ρ := by
  constructor
  · intro h
    rw [h]
    ring_nf
    rw [Real.sq_sqrt (by positivity : 0 ≤ G * ρ)]
    ring
  · intro h
    have hR : 0 < (1 / 2 : ℝ) * c * Real.sqrt (G * ρ) := by positivity
    have hsq : ((1 / 2 : ℝ) * c * Real.sqrt (G * ρ)) ^ 2 = a0 ^ 2 := by
      have hp : ((1 / 2 : ℝ) * c * Real.sqrt (G * ρ)) ^ 2 =
          (1 / 4 : ℝ) * c ^ 2 * (Real.sqrt (G * ρ)) ^ 2 := by ring
      rw [hp, Real.sq_sqrt (by positivity : 0 ≤ G * ρ)]
      nlinarith [h]
    exact (eq_of_sq_eq hR ha0 hsq).symm

theorem natural_units_core {a0 eps G ML MP : ℝ} (ha0 : 0 < a0) (hMLpos : 0 < ML)
    (hMPpos : 0 < MP) (hG : 0 < G) (hML : ML ^ 4 = eps) (hMP : MP ^ 2 = 1 / G) :
    a0 = ML ^ 2 / (2 * MP) ↔ 4 * a0 ^ 2 = G * eps := by
  constructor
  · intro h
    rw [h]
    have hp : (ML ^ 2 / (2 * MP)) ^ 2 = ML ^ 4 / (4 * MP ^ 2) := by
      rw [div_pow]
      field_simp [hMPpos.ne']
      ring
    rw [hp, ← hML, hMP]
    field_simp [hG.ne']
  · intro h
    have hGmp : G * MP ^ 2 = 1 := by
      rw [hMP]
      field_simp [hG.ne']
    have h' : 4 * a0 ^ 2 * MP ^ 2 = ML ^ 4 := by
      nlinarith [h, hGmp, hML]
    have hX : 0 < ML ^ 2 / (2 * MP) := by positivity
    have hX4 : (ML ^ 2 / (2 * MP)) ^ 2 = ML ^ 4 / (4 * MP ^ 2) := by
      rw [div_pow]
      field_simp [hMPpos.ne']
      ring
    have htarget : a0 ^ 2 = (ML ^ 2 / (2 * MP)) ^ 2 := by
      rw [hX4]
      field_simp [hMPpos.ne']
      ring_nf at h' ⊢
      exact h'
    exact eq_of_sq_eq ha0 hX htarget

theorem si_restoration {c hbar G ρ ML MP : ℝ} (hc : 0 < c) (hh : 0 < hbar) (hG : 0 < G)
    (hρ : 0 < ρ) (hMLpos : 0 < ML) (hMPpos : 0 < MP) (hML : ML ^ 4 = hbar ^ 3 * ρ / c ^ 3)
    (hMP : MP ^ 2 = hbar * c / G) :
    (1 / 2 : ℝ) * (c ^ 3 / hbar) * ML ^ 2 / MP = (1 / 2 : ℝ) * c * Real.sqrt (G * ρ) := by
  have hhinv : hbar⁻¹ ^ 2 = 1 / hbar ^ 2 := by
    rw [inv_pow]
    field_simp [hh.ne']
  have hMPinv : MP⁻¹ ^ 2 = G / (hbar * c) := by
    rw [inv_pow, hMP]
    field_simp [hc.ne', hh.ne', hG.ne']
  have hL2 : ((1 / 2 : ℝ) * (c ^ 3 / hbar) * ML ^ 2 / MP) ^ 2 = (1 / 4 : ℝ) * c ^ 2 * (G * ρ) := by
    rw [div_pow]
    ring_nf
    rw [hML, hMPinv, hhinv]
    field_simp [hc.ne', hh.ne', hG.ne']
  have hR2 : ((1 / 2 : ℝ) * c * Real.sqrt (G * ρ)) ^ 2 = (1 / 4 : ℝ) * c ^ 2 * (G * ρ) := by
    have hp : ((1 / 2 : ℝ) * c * Real.sqrt (G * ρ)) ^ 2 =
        (1 / 4 : ℝ) * c ^ 2 * (Real.sqrt (G * ρ)) ^ 2 := by ring
    rw [hp, Real.sq_sqrt (by positivity : 0 ≤ G * ρ)]
  have hposL : 0 < (1 / 2 : ℝ) * (c ^ 3 / hbar) * ML ^ 2 / MP := by positivity
  have hposR : 0 < (1 / 2 : ℝ) * c * Real.sqrt (G * ρ) := by positivity
  exact eq_of_sq_eq hposL hposR (by rw [hL2, hR2])

theorem framework_natural_iff {a0 c hbar G ρ ML MP : ℝ} (_ha0 : 0 < a0) (hc : 0 < c)
    (hh : 0 < hbar) (hG : 0 < G) (hρ : 0 < ρ) (hMLpos : 0 < ML) (hMPpos : 0 < MP)
    (hML : ML ^ 4 = hbar ^ 3 * ρ / c ^ 3) (hMP : MP ^ 2 = hbar * c / G) :
    a0 = (1 / 2 : ℝ) * (c ^ 3 / hbar) * ML ^ 2 / MP ↔
      a0 = (1 / 2 : ℝ) * c * Real.sqrt (G * ρ) := by
  rw [si_restoration hc hh hG hρ hMLpos hMPpos hML hMP]

theorem reduced_planck_mismatch_sq {ML MP Mbar G : ℝ} (hMLpos : 0 < ML) (hMPpos : 0 < MP)
    (hMBpos : 0 < Mbar) (hG : 0 < G) (hMbar : Mbar ^ 2 = 1 / (8 * Real.pi * G))
    (hMP : MP ^ 2 = 1 / G) :
    (ML ^ 2 / (2 * Mbar)) ^ 2 = 8 * Real.pi * (ML ^ 2 / (2 * MP)) ^ 2 := by
  rw [div_pow, div_pow, mul_pow, mul_pow]
  norm_num
  rw [hMbar, hMP]
  field_simp [hG.ne', hMBpos.ne', hMPpos.ne']

theorem reduced_trap_neq {a0 a0' ML MP Mbar G : ℝ} (ha0 : 0 < a0) (hMLpos : 0 < ML)
    (hMPpos : 0 < MP) (hMBpos : 0 < Mbar) (hG : 0 < G)
    (hMbar : Mbar ^ 2 = 1 / (8 * Real.pi * G)) (hMP : MP ^ 2 = 1 / G)
    (hdef : a0 = ML ^ 2 / (2 * MP)) (hdef' : a0' = ML ^ 2 / (2 * Mbar)) : a0' ≠ a0 := by
  intro h
  have hsq : a0' ^ 2 = 8 * Real.pi * a0 ^ 2 := by
    rw [hdef', hdef]
    exact reduced_planck_mismatch_sq hMLpos hMPpos hMBpos hG hMbar hMP
  have ha0sq : 0 < a0 ^ 2 := sq_pos_of_ne_zero (ne_of_gt ha0)
  have hpi : 8 * Real.pi = 1 := by nlinarith [ha0sq, hsq, h]
  nlinarith [Real.pi_gt_three, hpi]

theorem footing_rescale {a_a a_c eps_a eps_c G : ℝ} (hG : 0 < G) (a_c_ne : a_c ≠ 0)
    (h1 : 4 * a_c ^ 2 = G * eps_c) (h2 : 4 * a_a ^ 2 = G * eps_a) :
    eps_a / eps_c = (a_a / a_c) ^ 2 := by
  have h1' : eps_c = 4 * a_c ^ 2 / G := by
    calc
      eps_c = (G * eps_c) / G := by field_simp [hG.ne']
      _ = (4 * a_c ^ 2) / G := by rw [h1]
  have h2' : eps_a = 4 * a_a ^ 2 / G := by
    calc
      eps_a = (G * eps_a) / G := by field_simp [hG.ne']
      _ = (4 * a_a ^ 2) / G := by rw [h2]
  rw [h2', h1']
  field_simp [hG.ne', a_c_ne, pow_ne_zero 2 a_c_ne]

theorem lambda_dictionary {a0 Lam c : ℝ} (ha0 : 0 < a0) (hLam : 0 < Lam) (hc : 0 < c) :
    a0 = c ^ 2 * Real.sqrt (Lam / (32 * Real.pi)) ↔ Lam = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by
  have h32 : (32 * Real.pi : ℝ) ≠ 0 := by positivity
  constructor
  · intro h
    rw [h]
    have hp : (c ^ 2 * Real.sqrt (Lam / (32 * Real.pi))) ^ 2 =
        c ^ 4 * (Real.sqrt (Lam / (32 * Real.pi))) ^ 2 := by ring
    rw [hp, Real.sq_sqrt (by positivity : 0 ≤ Lam / (32 * Real.pi))]
    field_simp [hc.ne', h32]
  · intro h
    have hR : 0 < c ^ 2 * Real.sqrt (Lam / (32 * Real.pi)) := by positivity
    have hXsq : (c ^ 2 * Real.sqrt (Lam / (32 * Real.pi))) ^ 2 = a0 ^ 2 := by
      have hp : (c ^ 2 * Real.sqrt (Lam / (32 * Real.pi))) ^ 2 =
          c ^ 4 * (Real.sqrt (Lam / (32 * Real.pi))) ^ 2 := by ring
      rw [hp, h]
      have hx : 0 ≤ (32 * Real.pi * a0 ^ 2 / c ^ 4) / (32 * Real.pi) := by positivity
      rw [Real.sq_sqrt hx]
      field_simp [hc.ne', h32]
    exact (eq_of_sq_eq hR ha0 hXsq).symm

#print axioms eq_of_sq_eq
#print axioms framework_squared_iff
#print axioms natural_units_core
#print axioms si_restoration
#print axioms framework_natural_iff
#print axioms reduced_planck_mismatch_sq
#print axioms reduced_trap_neq
#print axioms footing_rescale
#print axioms lambda_dictionary