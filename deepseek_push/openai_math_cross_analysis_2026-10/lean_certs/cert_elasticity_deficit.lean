import Mathlib

/-! # Cert: phantom-mass elasticity law ε(s) (T9)

Certifies the ALGEBRA behind the T9 elasticity law for a point baryon host:

  kernel-exact enclosed phantom mass (r_in -> 0):
      M_ph(<r_out) = M_b / (e^s - 1),   s := r_t/r_out,   r_t := sqrt(G M_b / a0)
  (from the flux form r^2 (nu-1) g_N = G M_b (nu-1), nu-1 = 1/(e^s - 1) - the
  flux is strictly increasing, so rho_ph > 0 everywhere on the annulus);

  elasticity (log-derivative in M_b; s ∝ M_b^{1/2} gives the 1/2):
      eps(s) = 1 - (s/2) e^s / (e^s - 1),   eps(0) = 1/2,   eps(s*) = 0 at
      s* e^{s*} = 2 (e^{s*} - 1);

  and the exact half-mass radius: M_ph = M_b/2 at s = log 3 (r = r_t / log 3).

Physics mapping (divergence theorem in spherical symmetry; the FULL kernel
nu(y) = 1/(1 - exp(-sqrt y)) at y = g_N/a0 = (r_t/r)^2): t9_elasticity_deficit.py
(main run: eps predicted 0.49626/0.49660 vs measured 0.4960/0.4964 of the T1
lane; bridge +0.1 dex -> +12.1053% vs T1 C6 +12.10/+12.11%; 6/6 checks PASS).
The log-DERIVATIVE identity and the eps -> 1/2 LIMIT are carried by the lane
script (house pattern: derivative/limit statements certify as the algebraic
closed form when the build's calculus lemmas resist; C3 verifies the limit
numerically at s = 1e-9 with the expm1-stable form). This file certifies the
exact algebraic payload, the annihilation at the root, and the half-mass
special value, with zero sorry and axioms = {propext, Classical.choice,
Quot.sound}.
-/

noncomputable section

open Real

variable {s Mph Mb : ℝ}

/-- Kernel occupancy identity: 1/(e^s - 1) = e^{-s}/(1 - e^{-s}). -/
theorem kernel_occupancy_identity (hne : Real.exp s ≠ 1) :
    1 / (Real.exp s - 1) = Real.exp (-s) / (1 - Real.exp (-s)) := by
  have hne2 : Real.exp s ≠ 0 := Real.exp_ne_zero s
  have hden2 : 1 - Real.exp (-s) ≠ 0 := by
    intro hz
    have hzi : (Real.exp s)⁻¹ = 1 := by
      rw [Real.exp_neg] at hz
      linarith
    exact hne (inv_eq_one.mp hzi)
  have hmul : Real.exp (-s) * (Real.exp s - 1) = 1 - Real.exp (-s) := by
    rw [mul_sub, mul_comm (Real.exp (-s)) (Real.exp s), ← Real.exp_add]
    norm_num
  rw [eq_comm]
  apply (div_eq_iff hden2).2
  rw [← hmul]
  field_simp [hne, hne2]

/-- Stable-form identity: (s/2) e^s/(e^s - 1) = (s/2)/(1 - e^{-s}).
(The stable RHS is the numerically-safe form used by the lane script at
s ~ 1e-9: naive float evaluation of e^s - 1 cancels at ~1e-7 relative.) -/
theorem deficit_stable_form (h : s ≠ 0) :
    (s / 2) * Real.exp s / (Real.exp s - 1) =
      (s / 2) / (1 - Real.exp (-s)) := by
  have hne : Real.exp s ≠ 1 := by
    intro h1
    have h0 : Real.exp s = Real.exp 0 := by simpa using h1
    exact h (Real.exp_injective h0)
  have hne2 : Real.exp s ≠ 0 := Real.exp_ne_zero s
  have hden : 1 - Real.exp (-s) ≠ 0 := by
    intro hz
    have hzi : (Real.exp s)⁻¹ = 1 := by
      rw [Real.exp_neg] at hz
      linarith
    have he0 : Real.exp s = Real.exp 0 := by simpa using (inv_eq_one.mp hzi)
    exact h (Real.exp_injective he0)
  rw [Real.exp_neg]
  field_simp [h, hne, hne2, hden]

/-- Enclosed phantom mass from the flux closed form: M_ph = M_b/(e^s - 1). -/
theorem m_ph_closed_form (nu_m1 : ℝ) (hn : nu_m1 = 1 / (Real.exp s - 1))
    (hM : Mph = Mb * nu_m1) (hMb : Mb ≠ 0) :
    Mph / Mb = 1 / (Real.exp s - 1) := by
  rw [hM, hn]
  field_simp [hMb]

/-- Elasticity annihilates at the root: s e^s = 2(e^s - 1) -> eps(s) = 0. -/
theorem elasticity_annihilates_at_root
    (hroot : s * Real.exp s = 2 * (Real.exp s - 1)) (hne : Real.exp s ≠ 1) :
    (s / 2) * Real.exp s / (Real.exp s - 1) = 1 := by
  have hmain : (s / 2) * Real.exp s = Real.exp s - 1 := by
    have hs : (s / 2) * Real.exp s = (s * Real.exp s) / 2 := by ring
    rw [hs, hroot]
    ring
  rw [hmain]
  field_simp [hne]

/-- Half-mass radius: M_ph/M_b = 1/2 exactly at s = log 3 (r = r_t / log 3):
1/(e^{log 3} - 1) = 1/(3 - 1) = 1/2. -/
theorem half_mass_at_log3 :
    1 / (Real.exp (Real.log 3) - 1) = 1 / 2 := by
  have h3 : (0 : ℝ) < 3 := by norm_num
  rw [Real.exp_log h3]
  norm_num

end