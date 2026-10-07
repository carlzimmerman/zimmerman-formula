import Mathlib

/-! # Cert: the settling-flattening theorem (T10) — algebra payload

Certifies the ALGEBRAIC core of the settling-flattening theorem for the
framework's point-baryon host:

  (S1)  mu-space heat reduction  d_t mu = d^2_r mu, mu := r^2 rho — the
        substitution is a calculus statement; verified symbolically in the
        lane script (C1, residual ≡ 0 for the deep target) and numerically
        (C2, 2.6e-6 at 4th order, quartic convergence). House pattern:
        calculus carries in the lane; the algebraic payload is certified
        here.
  (S3)  The deep-MOND target is the UNIFORM mu-state: mu_ph = sqrt(G M a0)
        / (4 pi G) — i.e. r^2 rho_ph is a constant of the certified closed
        form rho_ph = sqrt(G M a0)/(4 pi G r^2); and the flat level follows:
        v^2 = 4 pi G mu_ph  =>  v^4 = G M a0 exactly (ring).
  (S6)  Supply-radius corollary: with s = ln(1 + 1/5.36) the kernel-exact
        mass law M_ph(<r) = M_b/(e^s - 1) gives M_ph = 5.36 M_b exactly
        (exp(log x) = x for x = 1 + 1/5.36 = 159/134 > 0).

No inserted rationals: 5.36 is the campaign's P3 cosmic cold share, read
as 134/25. Zero sorry; axioms = {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

variable {G M a0 v2 mu_ph rho_ph : ℝ}

/-- r^2 rho_ph is constant: the deep phantom target is the uniform
mu-state. -/
theorem mu_ph_is_constant (hG : G ≠ 0) (hr : r ≠ 0) (h : rho_ph = sqrt (G * M * a0) / (4 * π * G * r ^ 2)) :
    r ^ 2 * rho_ph = sqrt (G * M * a0) * (4 * π * G)⁻¹ := by
  rw [h]
  field_simp [hG, hr, pow_two]

/-- Flat level: v^2 = 4 pi G mu_ph with the uniform mu_ph implies
v^4 = G M a0 (the 16 pi^2 G^2 prefactor cancels exactly). -/
theorem v4_from_uniform_mu (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0)
    (hv : v2 = 4 * π * G * mu_ph)
    (hmu : mu_ph = sqrt (G * M * a0) / (4 * π * G)) :
    v2 ^ 2 = G * M * a0 := by
  have h4pi : 4 * π ≠ 0 := mul_ne_zero (by norm_num : (4 : ℝ) ≠ 0) Real.pi_ne_zero
  have h4piG : 4 * π * G ≠ 0 := mul_ne_zero h4pi (ne_of_gt hG)
  have hnn : 0 ≤ G * M * a0 := by positivity
  rw [hv, hmu]
  field_simp [h4piG]
  rw [Real.sq_sqrt hnn]

/-- Supply-radius corollary: at s = log(1 + 1/5.36) the enclosed phantom
mass is exactly 5.36 M_b:  1/(e^{log(1+1/5.36)} - 1) = 5.36. -/
theorem supply_mass_exact :
    1 / (Real.exp (Real.log (1 + 1 / (134 / 25 : ℝ))) - 1) = 134 / 25 := by
  have hpos : (0 : ℝ) < 1 + 1 / (134 / 25) := by norm_num
  rw [Real.exp_log hpos]
  norm_num

end