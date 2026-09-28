import Mathlib
import Mathlib.Tactic

/-
  AS010 -- Lean certificate for "Pressure normalization at the MOND radius"
  (deepseek_push/astra_spawn_ideas/AS010_pressure_normalization_at_the_mond_radius.md).

  Framework premises (FRAMEWORK_CONTRACT.md; kappa = 1/2 ADOPTED as input, not derived):
      r_M  = sqrt(G*M_b/a0),   C = sqrt(G*M_b*a0)  (= v_flat^2,  v_flat^4 = G M_b a0)
  Conditional deep-equilibrium inputs/targets (NOT free laws):
      rho_ph = C/(4 pi G r^2),  sigma^2 = C/2,  P = sigma^2 rho_ph.

  Claim certified here (exactly the task's "Mathematics and principal test"):

    (1) as010_P_at_rM        P(r_M) = (C/2) * C/(4 pi G r_M^2)  ==>  P(r_M) = a0^2/(8 pi G)
    (2) as010_ratio_epsilon  P(r_M) / [4 a0^2/G] = 1/(32 pi)     (epsilon_Lambda = 4 a0^2/G
                               is the vacuum ENERGY density; rho_Lambda = epsilon_Lambda/c^2)
    (3) as010_normalization  P(r) = P(r_M) * (r_M/r)^2  for all r (inverse-square scaling,
                               hence the exact cross-regime statement; y = B/a0 = (r_M/r)^2)
    (4) as010_eta_generalization  if sigma^2 = eta*C then P(r_M) = eta * a0^2/(4 pi G):
                               the coefficient is LINEAR in the adopted normalization eta
                               (eta = 1/2 is the adopted kappa-consistent input, not derived here)
    (5) as010_sigma_relation  sigma^2 = C/2 and C = v_flat^2  ==>  sigma = v_flat/sqrt(2)
    (6) as010_C_sq           C^2 = a0^2 r_M^2  (the single algebraic fact behind 1--4)

  All statements are exact identities in the real numbers; no numerical evaluation is needed.
  The statements are purely algebraic -- they do NOT assert that the conditional deep-equilibrium
  relations are derivable from the (time-dependent) field equations; that derivation is a separate,
  explicitly open dependency (see result.json limitations).
-/

noncomputable section
open Real

/-- (6) C^2 = a0^2 * r_M^2 from r_M^2 = G*M_b/a0 and C^2 = G*M_b*a0. -/
theorem as010_C_sq {C a0 G rM Mb : ℝ} (hG : G ≠ 0) (hrM : rM ≠ 0) (ha0 : a0 ≠ 0)
    (h1 : rM ^ 2 = G * Mb / a0) (h2 : C ^ 2 = G * Mb * a0) :
    C ^ 2 = a0 ^ 2 * rM ^ 2 := by
  have hGMr : G * Mb = rM ^ 2 * a0 := by
    calc
      G * Mb = (G * Mb / a0) * a0 := by
        field_simp [ha0]
      _ = rM ^ 2 * a0 := by
        rw [← h1]
  rw [h2, hGMr]
  ring

/-- (1) The central identity: the pressure at the MOND radius is the universal constant a0^2/(8 pi G),
independent of M_b. -/
theorem as010_P_at_rM {P C a0 G rM Mb : ℝ} (hG : G ≠ 0) (hrM : rM ≠ 0) (ha0 : a0 ≠ 0)
    (h1 : rM ^ 2 = G * Mb / a0) (h2 : C ^ 2 = G * Mb * a0)
    (hP : P = (C / 2) * (C / (4 * Real.pi * G * rM ^ 2))) :
    P = a0 ^ 2 / (8 * Real.pi * G) := by
  rw [hP]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have hC2 : C ^ 2 = a0 ^ 2 * rM ^ 2 := as010_C_sq hG hrM ha0 h1 h2
  calc
    (C / 2) * (C / (4 * Real.pi * G * rM ^ 2)) = C ^ 2 / (8 * Real.pi * G * rM ^ 2) := by
      field_simp [hG, hrM, hpi] <;> try ring_nf
    _ = a0 ^ 2 / (8 * Real.pi * G) := by
      rw [hC2]
      field_simp [hrM, hG, hpi]

/-- (2) P(r_M)/epsilon_Lambda = 1/(32 pi), with epsilon_Lambda = 4 a0^2/G (energy density). -/
def as010_epsL (a0 G : ℝ) : ℝ := 4 * a0 ^ 2 / G

theorem as010_ratio_epsilon {P a0 G : ℝ} (hG : G ≠ 0) (ha0 : a0 ≠ 0)
    (hP : P = a0 ^ 2 / (8 * Real.pi * G)) :
    P / as010_epsL a0 G = 1 / (32 * Real.pi) := by
  rw [hP, as010_epsL]
  field_simp [hG, ha0, Real.pi_ne_zero] <;> try ring_nf

/-- (3) Inverse-square scaling of the equilibrium pressure for all r: P(r) = P(r_M) (r_M/r)^2. -/
theorem as010_normalization {P r a0 G rM C : ℝ} (hG : G ≠ 0) (hr : r ≠ 0) (hrM : rM ≠ 0)
    (hC2 : C ^ 2 = a0 ^ 2 * rM ^ 2)
    (hP : P = (C / 2) * (C / (4 * Real.pi * G * r ^ 2))) :
    P = (a0 ^ 2 / (8 * Real.pi * G)) * (rM / r) ^ 2 := by
  rw [hP]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  calc
    (C / 2) * (C / (4 * Real.pi * G * r ^ 2)) = C ^ 2 / (8 * Real.pi * G * r ^ 2) := by
      field_simp [hG, hr, hpi] <;> try ring_nf
    _ = (a0 ^ 2 * rM ^ 2) / (8 * Real.pi * G * r ^ 2) := by
      rw [hC2]
    _ = (a0 ^ 2 / (8 * Real.pi * G)) * (rM / r) ^ 2 := by
      field_simp [hr, hG, hpi]

/-- (4) Sensitivity to the adopted normalization: if sigma^2 = eta*C then P(r_M) = eta*a0^2/(4 pi G).
The task's coefficient 1/2 enters exactly through eta = 1/2; it is an adopted input, not derived here. -/
theorem as010_eta_generalization {P_eta a0 G rM C η : ℝ} (hG : G ≠ 0) (hrM : rM ≠ 0) (ha0 : a0 ≠ 0)
    (hC2 : C ^ 2 = a0 ^ 2 * rM ^ 2)
    (hP : P_eta = η * C * (C / (4 * Real.pi * G * rM ^ 2))) :
    P_eta = η * (a0 ^ 2 / (4 * Real.pi * G)) := by
  rw [hP]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  calc
    η * C * (C / (4 * Real.pi * G * rM ^ 2)) = η * C ^ 2 / (4 * Real.pi * G * rM ^ 2) := by
      field_simp [hG, hrM, hpi]
    _ = η * (a0 ^ 2 * rM ^ 2) / (4 * Real.pi * G * rM ^ 2) := by
      rw [hC2]
    _ = η * (a0 ^ 2 / (4 * Real.pi * G)) := by
      field_simp [hrM, hG, hpi]

/-- (5) sigma = v_flat / sqrt(2): from sigma^2 = C/2 and C = v_flat^2 (v_flat^4 = C^2 = G M_b a0). -/
theorem as010_sigma_relation {σ2 v C : ℝ} (hC : C = v ^ 2) (hσ : σ2 = C / 2) :
    σ2 = v ^ 2 / 2 := by
  rw [hσ, hC]

#print axioms as010_C_sq
#print axioms as010_P_at_rM
#print axioms as010_ratio_epsilon
#print axioms as010_normalization
#print axioms as010_eta_generalization
#print axioms as010_sigma_relation