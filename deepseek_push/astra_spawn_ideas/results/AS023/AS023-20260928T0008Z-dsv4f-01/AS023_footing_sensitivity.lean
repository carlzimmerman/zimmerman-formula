import Mathlib
import Mathlib.Tactic

/-
  AS023 -- Lean certificate for "Footing sensitivity of physical radii and pressures"
  (deepseek_push/astra_spawn_ideas/AS023_footing_sensitivity_of_physical_radii_and_pressures.md).

  Framework premises (FRAMEWORK_CONTRACT.md; kappa = 1/2 ADOPTED as input, not derived):
      r_M  = sqrt(G*M_b/a0),   C = sqrt(G*M_b*a0)  (= v_flat^2,  v_flat^4 = G M_b a0)
  Conditional deep-equilibrium inputs/targets (NOT free laws):
      rho_ph = C/(4 pi G r^2),  sigma^2 = C/2,  P = sigma^2 rho_ph.
  Squared-premise style: hC2 : C^2 = G*M_b*a0 and hrM2 : rM^2 = G*M_b/a0 replace the
  square roots (house convention: no sqrt manipulation; both cell footings positive).

  Claims certified here (the task's scaling structures at fixed r and fixed x = r/r_M):

    (1) as023_C_sq_a0rM      C^2 = a0^2 * r_M^2               (single algebraic fact)
    (2) as023_rM_ratio       r_M(a0_2)^2 = r_M(a0_1)^2 * a0_1/a0_2
                             (r_M proportional to a0^(-1/2); footing conversion exponent -1/2)
    (3) as023_vflat_ratio    v_flat(a0_2)^4 = v_flat(a0_1)^4 * a0_2/a0_1
                             (v_flat proportional to a0^(1/4))
    (4) as023_rho_fixed_r_sq rho_ph^2 at fixed PHYSICAL r:  rho^2 = M_b*a0 / (16 pi^2 G r^4)
                             (rho_ph proportional to a0^(1/2) at fixed r)
    (5) as023_rho_fixed_x_sq rho_ph^2 at fixed x = r/r_M:    rho^2 = a0^3 / (16 pi^2 G^3 M_b x^4)
                             (rho_ph proportional to a0^(3/2) at fixed x)
    (6) as023_P_fixed_r      P(r) = M_b*a0 / (8 pi r^2)      (P proportional to a0 at fixed r)
    (7) as023_P_fixed_x      P(x*r_M) = a0^2 / (8 pi G x^2)  (P proportional to a0^2 at fixed x;
                             P(r_M) = a0^2/(8 pi G) at x = 1; independent of M_b)
    (8) as023_Mph_handoff    enclosed phantom mass  M_ph(<x*r_M) = C*(x*r_M)/G = x*M_b
                             (footing-INVARIANT at fixed x; M_ph(<r_M) = M_b at x = 1)
    (9) as023_y_at_rM        Newtonian argument at r_M: G*M_b/r_M^2 = a0  (y(r_M) = 1)
    (10) as023_Q_dimensionless  labelled Q comparison (g^2 = B^2 + a0*B, B = a0/x^2):
                             (g/a0)^2 = 1/x^4 + 1/x^2, a footing-invariant dimensionless curve
    (11) as023_rhoL_bookkeeping  rho_Lambda = 4 a0^2/(G c^2)  <->  a0^2 = G c^2 rho_Lambda/4
                             (rho_Lambda proportional to a0^2 at fixed kappa = 1/2)

  All statements are exact identities in the real numbers; no numerical evaluation is needed.
  They do NOT assert that the conditional deep-equilibrium relations are derivable from the
  (time-dependent) field equations -- that derivation is a separate, explicitly open
  dependency (see result.json limitations). The Q-branch appears ONLY as a labelled
  comparison kernel (item 10); no branch translation is made.
-/

noncomputable section
open Real

/-- (1) C^2 = a0^2 * r_M^2 from C^2 = G*M_b*a0 and r_M^2 = G*M_b/a0. -/
theorem as023_C_sq_a0rM {C a0 G rM Mb : ℝ} (hG : G ≠ 0) (ha0 : a0 ≠ 0)
    (hC2 : C ^ 2 = G * Mb * a0) (hrM2 : rM ^ 2 = G * Mb / a0) :
    C ^ 2 = a0 ^ 2 * rM ^ 2 := by
  have hGMr : G * Mb = rM ^ 2 * a0 := by
    calc
      G * Mb = (G * Mb / a0) * a0 := by
        field_simp [ha0]
      _ = rM ^ 2 * a0 := by
        rw [← hrM2]
  rw [hC2, hGMr]
  ring

/-- (2) r_M(a0_2)^2 = r_M(a0_1)^2 * (a0_1/a0_2): the r_M footing conversion (exponent -1/2). -/
theorem as023_rM_ratio {a01 a02 G Mb rM1 rM2 : ℝ} (ha01 : a01 ≠ 0) (ha02 : a02 ≠ 0)
    (h1 : rM1 ^ 2 = G * Mb / a01) (h2 : rM2 ^ 2 = G * Mb / a02) :
    rM2 ^ 2 = rM1 ^ 2 * (a01 / a02) := by
  have hGMr : G * Mb = rM1 ^ 2 * a01 := by
    calc
      G * Mb = (G * Mb / a01) * a01 := by
        field_simp [ha01]
      _ = rM1 ^ 2 * a01 := by
        rw [← h1]
  rw [h2, hGMr]
  field_simp [ha02]

/-- (3) v_flat(a0_2)^4 = v_flat(a0_1)^4 * (a0_2/a0_1): the v_flat footing conversion (exponent 1/4). -/
theorem as023_vflat_ratio {a01 a02 G Mb v1 v2 : ℝ} (ha01 : a01 ≠ 0)
    (h1 : v1 ^ 4 = G * Mb * a01) (h2 : v2 ^ 4 = G * Mb * a02) :
    v2 ^ 4 = v1 ^ 4 * (a02 / a01) := by
  rw [h2, h1]
  field_simp [ha01]

/-- (4) Phantom density at fixed PHYSICAL r: rho^2 = M_b*a0 / (16 pi^2 G r^4)  (proportional to a0). -/
theorem as023_rho_fixed_r_sq {rho C a0 G Mb r : ℝ} (hG : G ≠ 0) (hr : r ≠ 0)
    (hC2 : C ^ 2 = G * Mb * a0)
    (hrho : rho = C / (4 * Real.pi * G * r ^ 2)) :
    rho ^ 2 = Mb * a0 / (16 * Real.pi ^ 2 * G * r ^ 4) := by
  rw [hrho]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  calc
    (C / (4 * Real.pi * G * r ^ 2)) ^ 2 = C ^ 2 / (16 * Real.pi ^ 2 * G ^ 2 * r ^ 4) := by
      field_simp [hG, hr, hpi] <;> ring_nf
    _ = (G * Mb * a0) / (16 * Real.pi ^ 2 * G ^ 2 * r ^ 4) := by
      rw [hC2]
    _ = Mb * a0 / (16 * Real.pi ^ 2 * G * r ^ 4) := by
      field_simp [hG, hpi, hr]

/-- (5) Phantom density at fixed x = r/r_M: rho^2 = a0^3 / (16 pi^2 G^3 M_b x^4)  (proportional to a0^3).
The extra a0-power relative to the fixed-r form comes from r = x*r_M with r_M proportional to a0^(-1/2). -/
theorem as023_rho_fixed_x_sq {rho C a0 G Mb x rM : ℝ} (hG : G ≠ 0) (hMb : Mb ≠ 0) (ha0 : a0 ≠ 0)
    (hx : x ≠ 0) (hrM : rM ≠ 0)
    (hC2 : C ^ 2 = G * Mb * a0) (hrM2 : rM ^ 2 = G * Mb / a0)
    (hrho : rho = C / (4 * Real.pi * G * (x * rM) ^ 2)) :
    rho ^ 2 = a0 ^ 3 / (16 * Real.pi ^ 2 * G ^ 3 * Mb * x ^ 4) := by
  rw [hrho]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have hsq : (x * rM) ^ 2 = x ^ 2 * (G * Mb / a0) := by
    rw [mul_pow, hrM2]
  have h4 : (x * rM) ^ 4 = x ^ 4 * (G * Mb / a0) ^ 2 := by
    rw [show (x * rM) ^ 4 = ((x * rM) ^ 2) ^ 2 by ring, hsq, mul_pow]
    ring
  calc
    (C / (4 * Real.pi * G * (x * rM) ^ 2)) ^ 2 = C ^ 2 / (16 * Real.pi ^ 2 * G ^ 2 * (x * rM) ^ 4) := by
      field_simp [hG, hx, hrM, hpi] <;> ring_nf
    _ = (G * Mb * a0) / (16 * Real.pi ^ 2 * G ^ 2 * (x ^ 4 * (G * Mb / a0) ^ 2)) := by
      rw [hC2, h4]
    _ = a0 ^ 3 / (16 * Real.pi ^ 2 * G ^ 3 * Mb * x ^ 4) := by
      field_simp [hG, hMb, ha0, hx, hpi]

/-- (6) Pressure at fixed PHYSICAL r: P(r) = M_b*a0/(8 pi r^2)  (proportional to a0). -/
theorem as023_P_fixed_r {P C a0 G Mb r : ℝ} (hG : G ≠ 0) (hr : r ≠ 0)
    (hC2 : C ^ 2 = G * Mb * a0)
    (hP : P = (C / 2) * (C / (4 * Real.pi * G * r ^ 2))) :
    P = Mb * a0 / (8 * Real.pi * r ^ 2) := by
  rw [hP]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  calc
    (C / 2) * (C / (4 * Real.pi * G * r ^ 2)) = C ^ 2 / (8 * Real.pi * G * r ^ 2) := by
      field_simp [hG, hr, hpi] <;> ring_nf
    _ = (G * Mb * a0) / (8 * Real.pi * G * r ^ 2) := by
      rw [hC2]
    _ = Mb * a0 / (8 * Real.pi * r ^ 2) := by
      field_simp [hG, hpi, hr]

/-- (7) Pressure at fixed x = r/r_M: P(x*r_M) = a0^2/(8 pi G x^2)  (proportional to a0^2,
INDEPENDENT of M_b; P(r_M) = a0^2/(8 pi G) at x = 1). -/
theorem as023_P_fixed_x {P C a0 G Mb x rM : ℝ} (hG : G ≠ 0) (hx : x ≠ 0) (hrM : rM ≠ 0) (ha0 : a0 ≠ 0)
    (hC2 : C ^ 2 = G * Mb * a0) (hrM2 : rM ^ 2 = G * Mb / a0)
    (hP : P = (C / 2) * (C / (4 * Real.pi * G * (x * rM) ^ 2))) :
    P = a0 ^ 2 / (8 * Real.pi * G * x ^ 2) := by
  rw [hP]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have hC2' : C ^ 2 = a0 ^ 2 * rM ^ 2 := as023_C_sq_a0rM hG ha0 hC2 hrM2
  calc
    (C / 2) * (C / (4 * Real.pi * G * (x * rM) ^ 2)) = C ^ 2 / (8 * Real.pi * G * (x * rM) ^ 2) := by
      field_simp [hG, hx, hrM, hpi] <;> ring_nf
    _ = (a0 ^ 2 * rM ^ 2) / (8 * Real.pi * G * (x ^ 2 * rM ^ 2)) := by
      rw [hC2', mul_pow]
    _ = a0 ^ 2 / (8 * Real.pi * G * x ^ 2) := by
      field_simp [hG, hx, hrM, hpi]

/-- (8) Enclosed phantom mass M_ph(<r) := C*r/G (closed form of int_0^r rho_ph 4 pi s^2 ds = C*r/G):
M_ph(<x*r_M) = x*M_b -- FOOTING-INVARIANT at fixed x; the handoff M_ph(<r_M) = M_b at x = 1.
The integration identity itself is carried by the Python lane (quadrature, C9); this theorem
certifies the closed-form evaluation at the radius x*r_M. -/
def as023_Mph (C G : ℝ) (r : ℝ) : ℝ := C * r / G

theorem as023_Mph_handoff {C a0 G Mb x rM : ℝ} (hG : G ≠ 0) (hGp : 0 < G) (hMbp : 0 < Mb)
    (ha0n : a0 ≠ 0) (hpC : 0 < C) (hprM : 0 < rM)
    (hC2 : C ^ 2 = G * Mb * a0) (hrM2 : rM ^ 2 = G * Mb / a0) :
    as023_Mph C G (x * rM) = x * Mb := by
  have hCsqm : (C * rM) ^ 2 = (G * Mb) ^ 2 := by
    rw [mul_pow, mul_pow, hC2, hrM2]
    field_simp [hG, ha0n]
  have hCrpos : 0 < C * rM := mul_pos hpC hprM
  have hGMrpos : 0 < G * Mb := mul_pos hGp hMbp
  have hCsqm' : (C * rM) * (C * rM) = (G * Mb) * (G * Mb) := by
    simpa [pow_two] using hCsqm
  have hCrm : C * rM = G * Mb := by
    rcases (mul_self_eq_mul_self_iff.mp hCsqm') with h | h
    · exact h
    · exfalso
      linarith
  unfold as023_Mph
  calc
    C * (x * rM) / G = (C * rM) * x / G := by ring
    _ = (G * Mb) * x / G := by rw [hCrm]
    _ = x * Mb := by field_simp [hG]

/-- (9) Newtonian argument at the MOND radius: G*M_b/r_M^2 = a0, i.e. y(r_M) = 1 identically. -/
theorem as023_y_at_rM {a0 G Mb rM : ℝ} (hG : G ≠ 0) (ha0 : a0 ≠ 0) (hMb : Mb ≠ 0)
    (hrM2 : rM ^ 2 = G * Mb / a0) :
    G * Mb / rM ^ 2 = a0 := by
  rw [hrM2]
  field_simp [hG, ha0, hMb]

/-- (10) Labelled Q-branch comparison (g^2 = B^2 + a0*B with B = a0/x^2 at r = x*r_M):
(g/a0)^2 = 1/x^4 + 1/x^2, a footing-invariant dimensionless curve. No branch translation. -/
theorem as023_Q_dimensionless {a0 B g x : ℝ} (ha0 : a0 ≠ 0) (hx : x ≠ 0)
    (hB : B = a0 / x ^ 2) (hQ : g ^ 2 = B ^ 2 + a0 * B) :
    (g / a0) ^ 2 = 1 / x ^ 4 + 1 / x ^ 2 := by
  rw [div_pow, hQ, hB]
  field_simp [ha0]

/-- (11) Vacuum bookkeeping at kappa = 1/2: rho_Lambda = 4 a0^2/(G c^2)  <->  a0^2 = G c^2 rho_Lambda/4
(rho_Lambda proportional to a0^2 at fixed kappa; the alternative footing at fixed kappa
therefore changes the density by (a0_alt/a0_can)^2). -/
theorem as023_rhoL_bookkeeping {a0 c G rhoL : ℝ} (hG : G ≠ 0) (hc : c ≠ 0)
    (hrho : rhoL = 4 * a0 ^ 2 / (G * c ^ 2)) :
    a0 ^ 2 = G * c ^ 2 * rhoL / 4 := by
  rw [hrho]
  field_simp [hG, hc]

end
