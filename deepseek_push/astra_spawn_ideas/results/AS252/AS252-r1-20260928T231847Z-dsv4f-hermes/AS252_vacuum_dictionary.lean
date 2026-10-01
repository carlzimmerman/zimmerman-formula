import Mathlib

/-!
AS252 Lean 4 certificate — match the cosmological Einstein coefficient to
measured Newton gravity (Tier-0b vacuum-scale dictionary).

Seed: AS252_match_the_cosmological_einstein_coefficient_to_measured_newton_gravity.md
      (sha256 6de8d3e8bd3b8da9fe7e2953e04d0055d54382adafaaac64826ee12bbff1f5d2)
Action: real_research/common_action_2026_09_26/action/FINAL_ACTION.md
      (sha256 b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e)
Framework inputs: kappa = 1/2 adopted; rho_Lambda = 4 a0^2/(G_N c^2);
G_cosm = G_bare = (8 pi M_P^2)^-1; c_N = 1 - alpha/2 in (0,1); the derived
ratio G_cosm/G_N = c_N (upstream results/AS226, FINAL_ACTION eq. (18)).

Theorems certified (all real arithmetic):
 1. vacuum-scale dictionary: Lambda_eff = 32 pi c_N a0^2 / c^4
    from rho_Lambda = 4 a0^2/(G_N c^2), G_cosm = c_N G_N,
    Lambda_eff = 8 pi G_cosm rho_Lambda / c^2
 2. H_vac^2 = Lambda_eff / 3 = (32 pi / 3) c_N a0^2 / c^4
 3. rho_Lambda propagated into G_cosm: 4 a0^2/(G_N c^2) = 4 c_N a0^2/(G_cosm c^2)
 4. Einstein coefficient extraction: from 3 M_P^2 H^2 = M_P^2 Lambda + rho
    with M_P^2 = 1/(8 pi G_bare), H^2 = Lambda/3 + (8 pi G_bare) rho / 3
 5. negative control (premature G_cosm = G_N): Lambda_naive - Lambda_eff
    = (alpha/2) Lambda_naive  with c_N = 1 - alpha/2
 6. negative control fires: Lambda_naive != Lambda_eff for alpha != 0
 7. alpha -> 0 recovers the naive same-G dictionary (Einstein normalization)
-/

noncomputable section

open scoped Real

-- 1. vacuum-scale dictionary
theorem lambda_eff_of_rho_Lambda (a0 c GN Gc cN rho Le : ℝ)
    (hrho : rho = 4 * a0 ^ 2 / (GN * c ^ 2))
    (hG : Gc = cN * GN)
    (hLe : Le = 8 * Real.pi * Gc * rho / c ^ 2)
    (hGN : GN ≠ 0) (hc : c ≠ 0) (hpi : Real.pi ≠ 0) :
    Le = 32 * Real.pi * cN * a0 ^ 2 / c ^ 4 := by
  rw [hLe, hrho, hG]
  field_simp [hGN, hc, hpi]
  ring

-- 2. H_vac^2 from the dictionary
theorem h_vac_square (a0 c GN Gc cN rho Le H2 : ℝ)
    (hrho : rho = 4 * a0 ^ 2 / (GN * c ^ 2))
    (hG : Gc = cN * GN)
    (hLe : Le = 8 * Real.pi * Gc * rho / c ^ 2)
    (hH : H2 = Le / 3)
    (hGN : GN ≠ 0) (hc : c ≠ 0) (hpi : Real.pi ≠ 0) :
    H2 = (32 * Real.pi * cN * a0 ^ 2) / (3 * c ^ 4) := by
  rw [hH, hLe, hrho, hG]
  field_simp [hGN, hc, hpi]
  ring

-- 3. rho_Lambda propagated into G_cosm
theorem rho_lambda_in_gcosm (a0 c GN Gc cN : ℝ)
    (hG : Gc = cN * GN) (hcN : cN ≠ 0) (hGN : GN ≠ 0) (hc : c ≠ 0) :
    4 * a0 ^ 2 / (GN * c ^ 2) = 4 * cN * a0 ^ 2 / (Gc * c ^ 2) := by
  rw [hG]
  field_simp [hcN, hGN, hc]

-- 4. Einstein coefficient extraction in H^2 (homogeneous lapse constraint)
theorem coeff_of_rho_in_H2 (MP2 Gb H2 Lam rho : ℝ)
    (hFr : 3 * MP2 * H2 = MP2 * Lam + rho)
    (hMP : MP2 = 1 / (8 * Real.pi * Gb))
    (hMPn : MP2 ≠ 0) (hGb : Gb ≠ 0) (hpi : Real.pi ≠ 0) :
    H2 = Lam / 3 + (8 * Real.pi * Gb) * rho / 3 := by
  have h3m : 3 * MP2 ≠ 0 := mul_ne_zero (by norm_num : (3 : ℝ) ≠ 0) hMPn
  have hH' : H2 = (MP2 * Lam + rho) / (3 * MP2) := by
    apply (eq_div_iff h3m).2
    simpa [mul_assoc, mul_comm, mul_left_comm] using hFr
  have hH'' : H2 = Lam / 3 + rho / (3 * MP2) := by
    rw [hH']
    field_simp [h3m]
  rw [hH'', hMP]
  field_simp [hGb, hpi]

-- 5. negative control: mismatch of the premature (G_cosm = G_N) dictionary
theorem negative_control_mismatch (a0 c cN alpha Ln Le : ℝ)
    (hLn : Ln = 32 * Real.pi * a0 ^ 2 / c ^ 4)
    (hcN : cN = 1 - alpha / 2)
    (hLe : Le = 32 * Real.pi * cN * a0 ^ 2 / c ^ 4)
    (hc : c ≠ 0) (hpi : Real.pi ≠ 0) :
    Ln - Le = (alpha / 2) * Ln := by
  rw [hLn, hLe, hcN]
  field_simp [hc, hpi]
  ring

-- 6. negative control fires (capable of failing: needs a0 != 0 and alpha != 0)
theorem negative_control_fires (a0 c cN alpha Ln Le : ℝ)
    (hLn : Ln = 32 * Real.pi * a0 ^ 2 / c ^ 4)
    (hcN : cN = 1 - alpha / 2)
    (hLe : Le = 32 * Real.pi * cN * a0 ^ 2 / c ^ 4)
    (ha0 : a0 ≠ 0) (ha : alpha ≠ 0) (hc : c ≠ 0) (hpi : Real.pi ≠ 0) :
    Ln ≠ Le := by
  intro hEq
  have hm : Ln - Le = (alpha / 2) * Ln :=
    negative_control_mismatch a0 c cN alpha Ln Le hLn hcN hLe hc hpi
  have hz : (alpha / 2) * Ln = 0 := by
    rw [← hm, hEq, sub_self]
  have hLn0 : Ln ≠ 0 := by
    rw [hLn, div_eq_mul_inv]
    exact mul_ne_zero
      (mul_ne_zero (mul_ne_zero (by norm_num : (32 : ℝ) ≠ 0) hpi) (pow_ne_zero 2 ha0))
      (inv_ne_zero (pow_ne_zero 4 hc))
  have halpha2 : alpha / 2 ≠ 0 := div_ne_zero ha (by norm_num : (2 : ℝ) ≠ 0)
  exact (mul_ne_zero halpha2 hLn0) hz

-- 7. alpha -> 0 recovers the naive same-G dictionary (Einstein normalization)
theorem alpha_zero_recovers (a0 c cN alpha Ln Le : ℝ)
    (halpha : alpha = 0)
    (hcN : cN = 1 - alpha / 2)
    (hLn : Ln = 32 * Real.pi * a0 ^ 2 / c ^ 4)
    (hLe : Le = 32 * Real.pi * cN * a0 ^ 2 / c ^ 4) :
    Le = Ln := by
  rw [hLe, hcN, halpha, hLn]
  norm_num

#check lambda_eff_of_rho_Lambda
#check h_vac_square
#check rho_lambda_in_gcosm
#check coeff_of_rho_in_H2
#check negative_control_mismatch
#check negative_control_fires
#check alpha_zero_recovers

#print axioms lambda_eff_of_rho_Lambda
#print axioms h_vac_square
#print axioms rho_lambda_in_gcosm
#print axioms coeff_of_rho_in_H2
#print axioms negative_control_mismatch
#print axioms negative_control_fires
#print axioms alpha_zero_recovers