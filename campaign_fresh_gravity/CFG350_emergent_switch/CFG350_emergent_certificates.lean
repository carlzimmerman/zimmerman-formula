import Mathlib

/-!
# CFG350 -- certificates for the emergent (coarse-grained sigma) switch

10-moment closure in smooth flow: sigma(t) = G sigma0 G^T, det G = rho/rho0.

* E1 sigma = 0 invariance (single stream stays cold) and positivity (a warm state never returns to 0), 1D form.
* E2 det (G S G^T) = det G ^ 2 * det S (3x3).
* E3 the adiabat: det sigma / rho^2 is conserved.
* E4 no flicker for the zero threshold: a positive-definite congruence of a positive-definite sigma stays positive definite.
* E5 the empty-window obstruction: if maxOff >= minOn no threshold t has maxOff < t <= minOn.
* E5n the run's numbers: 12.17 km/s (post-reion IGM incl. delta 0.1) >= 10 km/s (local HI disc).
* E6 the IGM bound: k T/(mu m_p) at T = 1e4 K, mu = 0.59 exceeds (11.8 km/s)^2.
* E7 conservative form conserves the total: a periodic telescoping sum of flux differences is 0.
* E8 the R-s void lemma: for gamma < 5/3 and Delta < 1, (1.5 (gamma - 1) - 1) ln Delta > 0.
* E9 the RH entropy jump at gamma = 5/3 is nonnegative at Mach 2 (spot certificate of the second law used in D3).
-/

open Matrix

theorem E1_zero_invariant (g s0 : ℝ) (h : s0 = 0) : g ^ 2 * s0 = 0 := by simp [h]

theorem E1_positive (g s0 : ℝ) (hg : g ≠ 0) (hs : 0 < s0) : 0 < g ^ 2 * s0 :=
  mul_pos (by positivity) hs

theorem E2_det_congruence (Gm S : Matrix (Fin 3) (Fin 3) ℝ) :
    (Gm * S * Gmᵀ).det = Gm.det ^ 2 * S.det := by
  rw [det_mul, det_mul, det_transpose]; ring

theorem E3_adiabat (dS0 rho0 gdet : ℝ) (hr : rho0 ≠ 0) (hg : gdet ≠ 0) :
    (gdet ^ 2 * dS0) / (gdet * rho0) ^ 2 = dS0 / rho0 ^ 2 := by
  field_simp

theorem E4_no_flicker (Gm S : Matrix (Fin 3) (Fin 3) ℝ) (hS : S.PosDef) (hG : IsUnit Gm) :
    (Gm * S * Gmᵀ).PosDef := by
  have hT : IsUnit Gmᵀ := (Matrix.isUnit_iff_isUnit_det _).mpr
    (by rw [det_transpose]; exact (Matrix.isUnit_iff_isUnit_det _).mp hG)
  have hB : Function.Injective Gmᵀ.mulVec := Matrix.mulVec_injective_iff_isUnit.mpr hT
  have h := hS.conjTranspose_mul_mul_same hB
  have e : (Gmᵀ)ᴴ = Gm := by
    ext i j; simp [conjTranspose_apply]
  rwa [e] at h

theorem E5_empty_window (maxOff minOn : ℝ) (h : minOn ≤ maxOff) :
    ¬ ∃ t : ℝ, maxOff < t ∧ t ≤ minOn := by
  rintro ⟨t, h1, h2⟩; linarith

theorem E5n_run_window : ¬ ∃ t : ℝ, (12.17 : ℝ) < t ∧ t ≤ 10 :=
  E5_empty_window 12.17 10 (by norm_num)

theorem E6_igm_sigma :
    (1.380649e-23 : ℝ) * 1e4 / (0.59 * 1.67262192e-27) > (11.8e3 : ℝ) ^ 2 := by norm_num

theorem E7_conservative (n : ℕ) [NeZero n] (F : Fin n → ℝ) :
    ∑ i, (F (i + 1) - F i) = 0 := by
  rw [Finset.sum_sub_distrib, sub_eq_zero]
  exact Fintype.sum_equiv (Equiv.addRight 1) _ _ (fun _ => rfl)

theorem E8_void_above_adiabat (γ Δ : ℝ) (hγ : γ < 5 / 3) (hΔ0 : 0 < Δ) (hΔ : Δ < 1) :
    0 < (1.5 * (γ - 1) - 1) * Real.log Δ := by
  have hl : Real.log Δ < 0 := Real.log_neg hΔ0 hΔ
  have hc : 1.5 * (γ - 1) - 1 < 0 := by linarith
  nlinarith

theorem E9_RH_mach2 :
    -- gamma = 5/3, M = 2: p2/p1 = 19/4, rho2/rho1 = 16/7; jump = ln(19/4) - (5/3) ln(16/7) >= 0
    (16 / 7 : ℝ) ^ (5 : ℕ) ≤ (19 / 4 : ℝ) ^ (3 : ℕ) := by norm_num
#print axioms E1_zero_invariant
#print axioms E1_positive
#print axioms E2_det_congruence
#print axioms E3_adiabat
#print axioms E4_no_flicker
#print axioms E5_empty_window
#print axioms E5n_run_window
#print axioms E6_igm_sigma
#print axioms E7_conservative
#print axioms E8_void_above_adiabat
#print axioms E9_RH_mach2
