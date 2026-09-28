import Mathlib

/-!
# AS022 — What a scale identity can actually derive: algebraic certificates

SCOPE. Lean certifies the pure algebra of the AS022 meta-audit
(`deepseek_push/astra_spawn_ideas/AS022_what_a_scale_identity_can_actually_derive.md`):
the framework scale identity

    a0 = kappa c sqrt(G rho_Lambda),   kappa = 1/2 ADOPTED,

together with the vacuum-density constraint F2: Lambda = 8 pi G rho_Lambda / c^2,
is a *relationship among quantities*.  It derives relations (rearrangements,
compositions, equivalent-variable identities) but cannot derive the magnitudes
of kappa, rho_Lambda, G or a0 by itself; one external datum is required.

Certified here:

* `scale_identity_iff`        — a0 = (c/2) sqrt(G rho)  ⟺  4 a0^2 = G c^2 rho
                               (squaring is lossless exactly when a0 ≥ 0; this is
                                the README's '4 a0^2 = G c^2 rho_Lambda' form).
* `lambda_from_two_constraints` — F1 ∧ F2  ⇒  Lambda = 32 pi a0^2 / c^4
                               (the README closed form; rearrangements only).
* `a0_from_lambda_sq`, `a0_from_lambda` — F1 ∧ F2  ⇒  a0 = c^2 sqrt(Lambda/(32 pi))
                               (equivalent variables give the same prediction).
* `deep_v4_composition`       — deep Q limit g^2 = B a0 with kinematics
                               v^2 = r g and B = G M / r^2  ⇒  v^4 = G M a0
                               (the deep-MOND / BTFR law is a *composition*
                                of the identity with stated kinematics and source
                                convention — not a new constraint).
* `btfr_vacuum_form`          — v^4 = G M a0 in the vacuum variables:
                               v^4 = (1/2) c G M sqrt(G rho_L).
* `deep_limit_factor`         — sqrt(B^2 + a0 B) = sqrt(a0 B) sqrt(1 + B/a0),
                               the exact identity behind the deep-limit
                               expansion's leading factor.
* `rM_transition_sq`          — B(r) = a0 with B = G M / r^2  ⇒  r^2 = G M / a0
                               (the MOND-radius relation is the same identity
                                read at the transition).

These certify algebra only, and only the implications named.  They do NOT
certify that kappa = 1/2, the magnitude of rho_Lambda, or the magnitude of a0
are derived: the audit's rank statement (2 constraints on 3 variables ⇒ a
one-parameter family) is a property of the constraint system, not a theorem of
this file.  All variables are real; positivity hypotheses are stated where the
square root or a division demands them.
-/

theorem scale_identity_iff (a0 c G rho : ℝ) (ha0 : 0 ≤ a0) (hc : 0 < c)
    (hG : 0 < G) (hrho : 0 < rho) :
    a0 = (1 / 2) * c * Real.sqrt (G * rho) ↔ 4 * a0 ^ 2 = G * c ^ 2 * rho := by
  constructor
  · intro h
    rw [h]
    have hs : (Real.sqrt (G * rho)) ^ 2 = G * rho := Real.sq_sqrt (by positivity)
    calc
      4 * ((1 / 2 : ℝ) * c * Real.sqrt (G * rho)) ^ 2
          = 4 * ((1 / 2 : ℝ) ^ 2 * c ^ 2 * (Real.sqrt (G * rho)) ^ 2) := by ring
      _ = 4 * ((1 / 4 : ℝ) * c ^ 2 * (G * rho)) := by rw [hs]; ring
      _ = G * c ^ 2 * rho := by ring
  · intro h
    have hx2 : a0 ^ 2 = (G * c ^ 2 * rho) / 4 := by nlinarith
    have hqr : 0 ≤ G * rho := by positivity
    have hqc2 : 0 ≤ (c / 2) ^ 2 := by positivity
    have hq : Real.sqrt ((G * c ^ 2 * rho) / 4) = (1 / 2) * c * Real.sqrt (G * rho) := by
      have h1 : (G * c ^ 2 * rho) / 4 = (G * rho) * (c / 2) ^ 2 := by ring
      rw [h1, Real.sqrt_mul hqr ((c / 2) ^ 2), Real.sqrt_sq_eq_abs (c / 2),
        abs_of_nonneg (div_nonneg (le_of_lt hc) (by norm_num))]
      ring
    calc
      a0 = Real.sqrt (a0 ^ 2) := by rw [Real.sqrt_sq_eq_abs, abs_of_nonneg ha0]
      _ = Real.sqrt ((G * c ^ 2 * rho) / 4) := by rw [hx2]
      _ = (1 / 2) * c * Real.sqrt (G * rho) := hq

theorem lambda_from_two_constraints (a0 G c rho Lambda : ℝ) (hG : G ≠ 0) (hc : c ≠ 0) :
    4 * a0 ^ 2 = G * c ^ 2 * rho → Lambda = 8 * Real.pi * G * rho / c ^ 2 →
    Lambda = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by
  intro h1 h2
  have ha2 : a0 ^ 2 = (G * c ^ 2 * rho) / 4 := by nlinarith
  calc
    Lambda = 8 * Real.pi * G * rho / c ^ 2 := h2
    _ = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by rw [ha2]; field_simp; ring

theorem a0_from_lambda_sq (a0 G c rho Lambda : ℝ) (hG : G ≠ 0) (hc : c ≠ 0) :
    4 * a0 ^ 2 = G * c ^ 2 * rho → Lambda = 8 * Real.pi * G * rho / c ^ 2 →
    a0 ^ 2 = c ^ 4 * Lambda / (32 * Real.pi) := by
  intro h1 h2
  have ha2 : a0 ^ 2 = (G * c ^ 2 * rho) / 4 := by nlinarith
  rw [h2, ha2]
  field_simp
  ring

theorem a0_from_lambda (a0 c Lambda : ℝ) (ha0 : 0 ≤ a0) (hL : 0 < Lambda) :
    a0 ^ 2 = c ^ 4 * Lambda / (32 * Real.pi) → a0 = c ^ 2 * Real.sqrt (Lambda / (32 * Real.pi)) := by
  intro h
  calc
    a0 = Real.sqrt (a0 ^ 2) := by rw [Real.sqrt_sq_eq_abs, abs_of_nonneg ha0]
    _ = Real.sqrt (c ^ 4 * Lambda / (32 * Real.pi)) := by rw [h]
    _ = c ^ 2 * Real.sqrt (Lambda / (32 * Real.pi)) := by
      have hc2 : 0 ≤ (c ^ 2) ^ 2 := by positivity
      have hL32 : 0 ≤ Lambda / (32 * Real.pi) := by positivity
      have h1 : c ^ 4 * Lambda / (32 * Real.pi) = (c ^ 2) ^ 2 * (Lambda / (32 * Real.pi)) := by ring
      rw [h1, Real.sqrt_mul hc2 (Lambda / (32 * Real.pi)), Real.sqrt_sq_eq_abs (c ^ 2),
        abs_of_nonneg (sq_nonneg c)]

theorem deep_v4_composition (g B v r M G a0 : ℝ) (hr : r ≠ 0) :
    g ^ 2 = B * a0 → v ^ 2 = r * g → B = G * M / r ^ 2 → v ^ 4 = G * M * a0 := by
  intro h1 h2 h3
  calc
    v ^ 4 = (v ^ 2) ^ 2 := by ring
    _ = (r * g) ^ 2 := by rw [h2]
    _ = r ^ 2 * g ^ 2 := by ring
    _ = r ^ 2 * (B * a0) := by rw [h1]
    _ = r ^ 2 * ((G * M / r ^ 2) * a0) := by rw [h3]
    _ = G * M * a0 := by field_simp

theorem btfr_vacuum_form (v G M a0 c rho : ℝ) :
    v ^ 4 = G * M * a0 → a0 = (1 / 2) * c * Real.sqrt (G * rho) →
    v ^ 4 = (1 / 2) * c * G * M * Real.sqrt (G * rho) := by
  intro h1 h2
  rw [h1, h2]
  ring

theorem deep_limit_factor (a0 B : ℝ) (ha0 : 0 < a0) (hB : 0 ≤ B) :
    Real.sqrt (B ^ 2 + a0 * B) = Real.sqrt (a0 * B) * Real.sqrt (1 + B / a0) := by
  have h1 : B ^ 2 + a0 * B = (a0 * B) * (1 + B / a0) := by
    field_simp [ne_of_gt ha0]
    ring
  have hgr : 0 ≤ a0 * B := by positivity
  have hb : 0 ≤ 1 + B / a0 := by positivity
  rw [h1, Real.sqrt_mul hgr (1 + B / a0)]

theorem rM_transition_sq (r G M a0 : ℝ) (hr : r ≠ 0) (ha0 : a0 ≠ 0) :
    G * M / r ^ 2 = a0 → r ^ 2 = G * M / a0 := by
  intro h
  have h' : G * M = a0 * r ^ 2 := by
    field_simp [hr] at h
    linarith
  rw [h']
  field_simp [ha0]

#print axioms scale_identity_iff
#print axioms lambda_from_two_constraints
#print axioms a0_from_lambda_sq
#print axioms a0_from_lambda
#print axioms deep_v4_composition
#print axioms btfr_vacuum_form
#print axioms deep_limit_factor
#print axioms rM_transition_sq
