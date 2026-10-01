import Mathlib

/-!
AS500 — gate-lattice algebraic core certificates.

1. ppn_gamma_one_of_no_slip:  in the req-3 metric ansatz
   ds² = -(1+2Φ/c²)c²dt² + (1-2Ψ/c²)δ_ij dxⁱdxʲ, the PPN isotropic matching
   gives Ψ = γΦ on the galactic branch; Φ = Ψ ⇒ γ = 1.  (P3 ⇒ P4(γ).)
2. kappa_sq_at_rstar / kappa_half_at_rstar:
   κ(r) = √(2/(r+2b)) with r* = 8−2b lands exactly at κ = 1/2 — the unique
   continuum point (AS651/AS138.C01); still ADOPTED there, not derived
   (no fixing equation exists).
3. kappa_projection_injective: r ↦ κ(r) = √(2/(r+2b)) is injective for r > 0,
   so the κ-projection of the conserving continuum is a continuum (B-iv
   fails ⇒ no rank-1 selection; P13's derive-arm independent of audited class).
-/
namespace AS500

open scoped Real

theorem ppn_gamma_one_of_no_slip
    (Phi Psi gamma : ℝ) (hPhi : Phi ≠ 0)
    (hgamma : gamma = Psi / Phi) (h : Phi = Psi) : gamma = 1 := by
  have hPsi : Psi ≠ 0 := by
    rwa [← h]
  rw [hgamma]
  rw [← h]
  field_simp [hPsi]

theorem kappa_sq_at_rstar
    (kappa r b : ℝ) (hk : kappa = Real.sqrt (2 / (r + 2*b))) (hr : r = 8 - 2*b) :
    kappa * kappa = (1 : ℝ) / 4 := by
  rw [hk, hr]
  have hden : 8 - 2*b + 2*b = 8 := by ring
  have hq : 2 / (8 - 2*b + 2*b) = (2 : ℝ) / 8 := by rw [hden]
  have hsqrt : Real.sqrt (2 / (8 - 2*b + 2*b)) *
      Real.sqrt (2 / (8 - 2*b + 2*b)) = 2 / (8 - 2*b + 2*b) := by
    apply Real.mul_self_sqrt
    rw [hden]
    apply div_nonneg <;> norm_num
  rw [hsqrt, hq]
  norm_num

theorem kappa_half_at_rstar
    (kappa r b : ℝ) (hk : kappa = Real.sqrt (2 / (r + 2*b))) (hr : r = 8 - 2*b) :
    kappa = (1 : ℝ) / 2 := by
  have hsq := kappa_sq_at_rstar kappa r b hk hr
  have hsq_half : kappa * kappa = (1 : ℝ) / 2 * ((1 : ℝ) / 2) := by
    rw [hsq]
    norm_num
  have hsq_eq := mul_self_eq_mul_self_iff.mp hsq_half
  rcases hsq_eq with hk12 | hkneg
  · exact hk12
  · exfalso
    have hnonneg : 0 ≤ kappa := by
      rw [hk]
      exact Real.sqrt_nonneg _
    nlinarith

theorem kappa_projection_injective
    (r1 r2 b : ℝ) (hb : 0 < b) (hr1 : 0 < r1) (hr2 : 0 < r2)
    (h : Real.sqrt (2 / (r1 + 2*b)) = Real.sqrt (2 / (r2 + 2*b))) : r1 = r2 := by
  have hnr1 : 0 ≤ 2 / (r1 + 2*b) := by
    apply div_nonneg
    · norm_num
    · nlinarith [hr1, hb]
  have hnr2 : 0 ≤ 2 / (r2 + 2*b) := by
    apply div_nonneg
    · norm_num
    · nlinarith [hr2, hb]
  have hs1 : Real.sqrt (2 / (r1 + 2*b)) * Real.sqrt (2 / (r1 + 2*b)) =
      2 / (r1 + 2*b) := Real.mul_self_sqrt hnr1
  have hs2 : Real.sqrt (2 / (r2 + 2*b)) * Real.sqrt (2 / (r2 + 2*b)) =
      2 / (r2 + 2*b) := Real.mul_self_sqrt hnr2
  have hcross : 2 / (r1 + 2*b) = 2 / (r2 + 2*b) := by
    rw [← hs1, ← hs2, h]
  have h2nz : (2 : ℝ) ≠ 0 := by norm_num
  have hinv : (r1 + 2*b)⁻¹ = (r2 + 2*b)⁻¹ := by
    have hA : 2 / (r1 + 2*b) = 2 * (r1 + 2*b)⁻¹ := by rw [div_eq_mul_inv]
    have hB : 2 / (r2 + 2*b) = 2 * (r2 + 2*b)⁻¹ := by rw [div_eq_mul_inv]
    have hc : 2 * (r1 + 2*b)⁻¹ = 2 * (r2 + 2*b)⁻¹ := by
      rw [← hA, ← hB]
      exact hcross
    exact mul_left_cancel₀ h2nz hc
  have hden : r1 + 2*b = r2 + 2*b := (inv_inj.mp hinv)
  nlinarith

end AS500