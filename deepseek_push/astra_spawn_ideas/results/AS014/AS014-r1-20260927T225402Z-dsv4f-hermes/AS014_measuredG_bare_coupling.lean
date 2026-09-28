import Mathlib

/-!
# AS014 — Measured G versus bare action coupling: conversion audit (Lean 4)

CORE scale identities under the conversion `G_bare = C_N * G_N`.  All
variables are real; positivities are stated as premises.  The AS002-certified
identity `Lambda_eff = 32*pi*(G_E/G_N)*a0^2/c^4` is reused here as the
hypothesis `hT1` (see AS002-r1: `AS002_lambda_conversion.lean`, T1) and is
NOT re-derived as a new claim; AS014's new content is the substitution into
r_M, the BTFR and the vacuum identity, the matching equivalence and the
C_N=2 negative-control instances.

Axioms of the declarations below are checked externally with `#print axioms`
(unfiltered): the bar is subseteq {propext, Classical.choice, Quot.sound}.
-/

namespace AS014

variable {a0 a0b kappa c rho GN Gb CN M rM2 rM2b v4 v4b GE Lambda a0inf : ℝ}

/-! ## L1: scale conversion  a0_b = sqrt(C_N) * a0  -/
theorem scale_conversion
    (ha0 : a0 = kappa * c * Real.sqrt (GN * rho))
    (ha0b : a0b = kappa * c * Real.sqrt (Gb * rho))
    (hGb : Gb = CN * GN)
    (_hGN : 0 < GN) (_hrho : 0 < rho) (hCN : 0 < CN) :
    a0b = Real.sqrt CN * a0 := by
  calc
    a0b = kappa * c * Real.sqrt (Gb * rho) := ha0b
    _ = kappa * c * Real.sqrt ((CN * GN) * rho) := by rw [hGb]
    _ = kappa * c * (Real.sqrt CN * Real.sqrt (GN * rho)) := by
      have h1 : Real.sqrt ((CN * GN) * rho) =
          Real.sqrt CN * Real.sqrt (GN * rho) := by
        rw [mul_assoc]
        rw [Real.sqrt_mul hCN.le (GN * rho)]
      rw [h1]
    _ = Real.sqrt CN * (kappa * c * Real.sqrt (GN * rho)) := by ring
    _ = Real.sqrt CN * a0 := by rw [ha0]

/-! ## L2: MOND-radius substitution (squared form)  r_M^2(G_bare) = C_N r_M^2(G_N)  -/
theorem mond_radius_substitution
    (hr : rM2 = GN * M / a0) (hrb : rM2b = Gb * M / a0)
    (hGb : Gb = CN * GN) (ha0 : a0 ≠ 0) :
    rM2b = CN * rM2 := by
  rw [hrb, hGb, hr]
  field_simp [ha0]

/-! ## L3: BTFR substitution  v_flat^4(G_bare) = C_N v_flat^4(G_N)  -/
theorem btfr_substitution
    (hv : v4 = a0 * GN * M) (hvb : v4b = a0b * Gb * M)
    (ha0b : a0b = a0) (hGb : Gb = CN * GN) :
    v4b = CN * v4 := by
  rw [hvb, ha0b, hGb, hv]
  ring

/-! ## L4: full-cell deep law  v_flat^4 = a0_b G_bare M  with  a0_b = sqrt(C_N) a0
        gives  v_flat^4 = (sqrt C_N)^3 v_flat^4(G_N)  -/
theorem deep_law_full_cell
    (hv : v4 = a0 * GN * M) (hvb : v4b = a0b * Gb * M)
    (ha0b : a0b = Real.sqrt CN * a0) (hGb : Gb = CN * GN)
    (hCN : 0 ≤ CN) :
    v4b = (Real.sqrt CN) ^ 3 * v4 := by
  rw [hvb, ha0b, hGb, hv]
  have hsq : (Real.sqrt CN) ^ 2 = CN := Real.sq_sqrt hCN
  have hcube : (Real.sqrt CN) ^ 3 = CN * Real.sqrt CN := by
    rw [pow_succ, hsq]
  rw [hcube]
  ring

/-! ## L5: vacuum identity with G_E = G_bare = C_N G_N
        (AS002 T1 reused as the premise hT1)
        Lambda_eff = 32 pi (G_E/G_N) a0^2/c^4  and  G_E = G_bare = C_N G_N
        entails  Lambda_eff = 32 pi C_N a0^2 / c^4  -/
theorem vacuum_identity_bare
    (hT1 : Lambda = 32 * Real.pi * (GE / GN) * a0 ^ 2 / c ^ 4)
    (hGE : GE = Gb) (hGb : Gb = CN * GN)
    (hGN : GN ≠ 0) (hc : c ≠ 0) :
    Lambda = 32 * Real.pi * CN * a0 ^ 2 / c ^ 4 := by
  have hc4 : c ^ 4 ≠ 0 := pow_ne_zero 4 hc
  rw [hT1, hGE, hGb]
  field_simp [hGN, hc4]

/-! ## L6: matching equivalence
        Under the same premises,  Lambda_eff = 32 pi a0^2/c^4  (the framework
        same-G dictionary value) holds IFF the action forces C_N = 1,
        i.e. G_bare = G_N.  The framework identity is a matching condition
        on the candidate, not permission to set the couplings equal.  -/
theorem matching_iff
    (hT1 : Lambda = 32 * Real.pi * (GE / GN) * a0 ^ 2 / c ^ 4)
    (hGE : GE = Gb) (hGb : Gb = CN * GN)
    (hGN : GN ≠ 0) (hc : c ≠ 0) (ha0 : a0 ≠ 0) :
    (Lambda = 32 * Real.pi * a0 ^ 2 / c ^ 4) ↔ CN = 1 := by
  constructor
  · intro h
    have hb : Lambda = 32 * Real.pi * CN * a0 ^ 2 / c ^ 4 :=
      vacuum_identity_bare hT1 hGE hGb hGN hc
    rw [hb] at h
    have hc4 : c ^ 4 ≠ 0 := pow_ne_zero 4 hc
    have hE2 : 32 * Real.pi * CN * a0 ^ 2 = 32 * Real.pi * a0 ^ 2 := by
      field_simp [hc4] at h ⊢
      exact h
    have hF : (32 * Real.pi * a0 ^ 2 / c ^ 4) ≠ 0 := by
      exact div_ne_zero
        (mul_ne_zero (mul_ne_zero (by norm_num : (32 : ℝ) ≠ 0) Real.pi_ne_zero)
          (pow_ne_zero 2 ha0)) hc4
    have hsub : (32 * Real.pi * a0 ^ 2 / c ^ 4) * CN =
        (32 * Real.pi * a0 ^ 2 / c ^ 4) * 1 := by
      rw [mul_one]
      calc (32 * Real.pi * a0 ^ 2 / c ^ 4) * CN
              = 32 * Real.pi * a0 ^ 2 * CN / c ^ 4 := by ring
        _ = 32 * Real.pi * CN * a0 ^ 2 / c ^ 4 := by ring
        _ = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by rw [hE2]
    exact mul_left_cancel₀ hF (by simpa using hsub)
  · intro hCN1
    have hb : Lambda = 32 * Real.pi * CN * a0 ^ 2 / c ^ 4 :=
      vacuum_identity_bare hT1 hGE hGb hGN hc
    calc Lambda = 32 * Real.pi * CN * a0 ^ 2 / c ^ 4 := hb
      _ = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by simp [hCN1]

/-! ## L7: task negative control (C_N = 2), vacuum channel:
        with C_N = 2 the unconverted (same-G) identity fails:  -/
theorem control_lambda_mismatch
    (hL : Lambda = 32 * Real.pi * CN * a0 ^ 2 / c ^ 4)
    (hCN : CN = 2) (hc : c ≠ 0) (ha0 : a0 ≠ 0) :
    Lambda ≠ 32 * Real.pi * a0 ^ 2 / c ^ 4 := by
  intro h
  rw [hCN] at hL
  have hE : 32 * Real.pi * 2 * a0 ^ 2 / c ^ 4 = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by
    rw [← hL]
    exact h
  have hc4 : c ^ 4 ≠ 0 := pow_ne_zero 4 hc
  have hE2 : 32 * Real.pi * 2 * a0 ^ 2 = 32 * Real.pi * a0 ^ 2 := by
    field_simp [hc4] at hE ⊢
    exact hE
  have hF : (32 * Real.pi * a0 ^ 2) ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (by norm_num : (32 : ℝ) ≠ 0) Real.pi_ne_zero)
      (pow_ne_zero 2 ha0)
  have hsub : (32 * Real.pi * a0 ^ 2) * 2 = (32 * Real.pi * a0 ^ 2) * 1 := by
    rw [mul_one]
    calc (32 * Real.pi * a0 ^ 2) * 2 = 32 * Real.pi * a0 ^ 2 * 2 := by ring
      _ = 32 * Real.pi * 2 * a0 ^ 2 := by ring
      _ = 32 * Real.pi * a0 ^ 2 := hE2
  have htwo : (2 : ℝ) = 1 := mul_left_cancel₀ hF (by simpa using hsub)
  norm_num at htwo

/-! ## L8: task negative control (C_N = 2), inferred-scale channel, mixed cell:
        a0_inf = C_N a0 (analyst uses measured G_N, action forces on G_bare)  -/
theorem control_inferred_scale_mixed
    (hinf : a0inf = CN * a0) (hCN : CN = 2) (ha0 : a0 ≠ 0) :
    a0inf ≠ a0 := by
  intro h
  rw [hCN] at hinf
  have hE : 2 * a0 = a0 := by
    rw [← hinf]
    exact h
  have haz : a0 = 0 := by nlinarith [hE]
  exact ha0 haz

/-! ## L9: task negative control (C_N = 2), inferred-scale channel, full cell:
        a0_inf = (sqrt C_N)^3 a0  -/
theorem control_inferred_scale_full
    (hinf : a0inf = (Real.sqrt CN) ^ 3 * a0) (hCN : CN = 2) (ha0 : a0 ≠ 0) :
    a0inf ≠ a0 := by
  intro h
  rw [hCN] at hinf
  have hE : (Real.sqrt 2) ^ 3 * a0 = a0 := by
    rw [← hinf]
    exact h
  have hs_ne : (Real.sqrt 2) ^ 3 ≠ 1 := by
    intro hh
    have hsq : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
    -- s^3 = 1 with s^2 = 2: multiply the second by s: s^3 = 2 s, so 2 s = 1,
    -- hence s^2 = (2 s)^2 / 4 = 1/4, contradicting s^2 = 2.
    have h2s : 2 * Real.sqrt 2 = 1 := by nlinarith [hh, hsq]
    have hs14 : (Real.sqrt 2) ^ 2 = 1 / 4 := by nlinarith [h2s]
    nlinarith [hs14, hsq]
  have hlin : ((Real.sqrt 2) ^ 3 - 1) * a0 = 0 := by nlinarith [hE]
  have haz : a0 = 0 := (mul_eq_zero.mp hlin).resolve_left (sub_ne_zero.mpr hs_ne)
  exact ha0 haz

end AS014
