import Mathlib

/-! # Cert deep-phantom algebra (deep-MOND log law)

Certifies the ALGEBRA of the deep-MOND phantom laws used by lanes T3/T4/T6:

1. Enclosed phantom mass: M_ph(<r) = r^2 * g_ph(r)/G with the deep field
   g_ph(r) = sqrt(G M a0)/r  gives  M_ph(<r) = r * sqrt(G M a0)/G.
2. Deep phantom density: rho_ph(r) = sqrt(G M a0)/(4 pi G r^2), i.e.
   4 pi G r^2 rho_ph = sqrt(G M a0) (the divergence reading of the law).
3. Field-energy prefactor collapse: the deep-MOND field energy
   E = (1/(12 pi G a0)) * (sqrt(G M a0))^3 * ln(R/r_in) — written here with
   the geometric-mean factor sqrt(G M a0) * (G M a0) in place of the cube —
   collapses to E = (1/3) * M * sqrt(G M a0) * ln(R/r_in):
   (1/(12 pi G a0)) * (sqrt(G M a0) * (G M a0)) * (4 pi) = (1/3) M sqrt(G M a0).

Physics mapping (divergence theorem in spherical symmetry, the lane scripts
with the FULL kernel nu(y) = 1/(1 - exp(-sqrt y)) at g_N/a0 >> 1, declared
tolerances): t1_fam374 (C6), t3_jko_settling, t4_sharp_constants (C_b2/C_b3:
1.1% at 100 r_t). This file certifies the closed-form arithmetic only.
-/

noncomputable section

variable {G M a0 r : ℝ}

/-- Enclosed phantom mass from the deep field: r^2 * g_ph(r)/G with
g_ph(r) = sqrt(G M a0)/r is r sqrt(G M a0)/G. -/
theorem enclosed_mass_from_deep_field (hr : r ≠ 0) (hG : G ≠ 0) :
    (r ^ 2 * (Real.sqrt (G * M * a0) / r)) / G = r * Real.sqrt (G * M * a0) / G := by
  field_simp [hr, hG] <;> ring

-- Same statement with the positivity hypotheses used in the lanes.
theorem m_ph_deep (hr : 0 < r) (hG : 0 < G) (hMa : 0 ≤ M * a0) :
    (r ^ 2 * (Real.sqrt (G * M * a0) / r)) / G = r * Real.sqrt (G * M * a0) / G := by
  field_simp [ne_of_gt hr, ne_of_gt hG] <;> ring

/-- Deep phantom density identity: 4 pi G r^2 rho_ph = sqrt(G M a0). -/
theorem deep_density (hr : r ≠ 0) (hG : G ≠ 0) :
    4 * Real.pi * G * r ^ 2 * (Real.sqrt (G * M * a0) / (4 * Real.pi * G * r ^ 2))
      = Real.sqrt (G * M * a0) := by
  field_simp [hr, hG, Real.pi_ne_zero] <;> ring

/-- Field-energy prefactor collapse: the 4 pi/(12 pi G a0) factor times the
geometric-mean factor sqrt(G M a0) * (G M a0) equals (1/3) M sqrt(G M a0). -/
theorem field_energy_prefactor (hG : G ≠ 0) (ha0 : a0 ≠ 0) :
    (1 / (12 * Real.pi * G * a0)) * (Real.sqrt (G * M * a0) * (G * M * a0)) * (4 * Real.pi)
      = (1 / 3) * M * Real.sqrt (G * M * a0) := by
  field_simp [hG, ha0, Real.pi_ne_zero] <;> ring

end