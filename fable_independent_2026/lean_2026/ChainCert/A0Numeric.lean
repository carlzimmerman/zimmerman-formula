import Mathlib

/-!
# ChainCert.A0Numeric -- a certified interval for a0 = kappa c sqrt(G rho_Lambda), from STATED input intervals

With `rho_Lambda = 3 H0^2 Omega_Lambda / (8 pi G)` (flat FRW, the canonical pure-dark-energy footing), G cancels and
`a0 = kappa c H0 sqrt(3 Omega_Lambda / (8 pi))` (`a0_of_rhoLambda`).  `a0num_interval` bounds it from input intervals and
rational square-root brackets (pi is bracketed by Mathlib's `Real.pi_gt_d6`, `Real.pi_lt_d6`).

PREMISES (inputs; nothing here certifies them):
* kappa = 1/2 -- FITTED to the BTFR zero point, not derived;
* c = 299792458 m/s (exact by the SI definition); G = 6.6743e-11 m^3 kg^-1 s^-2 (CODATA 2018, declared; it cancels);
* 1 Mpc = 3.0856775814913673e22 m (declared, the value the repo's scripts use);
* H0 and Omega_Lambda in the stated intervals: `a0_interval` takes H0 in [66.9, 67.9] km/s/Mpc and Omega_Lambda in
  [0.6774, 0.6920] (Planck 2018 central values +- about 1 sigma, declared), and certifies 9.24e-11 < a0 < 9.48e-11 m/s^2;
  `a0_point` takes H0 = 67.4 and Omega_Lambda = 0.6847 and certifies 9.36e-11 < a0 < 9.361e-11 m/s^2, consistent with the
  record's canonical 9.36e-11.
NOT certified: the input values, the footing choice (rho_Lambda, not the total density -- the alternative footing gives 1.13e-10),
or that a0 has this form in nature.
-/

open Real

namespace A0Numeric

/-- the SI speed of light (exact) -/
noncomputable def cSI : ℝ := 299792458
/-- Newton's constant, CODATA 2018 value (declared; it cancels) -/
noncomputable def GSI : ℝ := 6.6743e-11
/-- one megaparsec in metres (declared) -/
noncomputable def Mpc : ℝ := 3.0856775814913673e22

/-- the closed form kappa c H sqrt(3 Omega/(8 pi)) -/
noncomputable def a0num (κ c H Ω : ℝ) : ℝ := κ * c * H * Real.sqrt (3 * Ω / (8 * π))

/-- G cancels: kappa c sqrt(G rho_Lambda) with rho_Lambda = 3 H^2 Omega/(8 pi G) is the closed form -/
theorem a0_of_rhoLambda {κ c G H Ω : ℝ} (hG : 0 < G) (hH : 0 ≤ H) :
    κ * c * Real.sqrt (G * (3 * H ^ 2 * Ω / (8 * π * G))) = a0num κ c H Ω := by
  have hpi : 0 < π := Real.pi_pos
  have e : G * (3 * H ^ 2 * Ω / (8 * π * G)) = H ^ 2 * (3 * Ω / (8 * π)) := by
    field_simp
  rw [e, Real.sqrt_mul (sq_nonneg H), Real.sqrt_sq hH, a0num]
  ring

/-- interval bound from input intervals and rational brackets `slo^2 8 pi <= 3 Omega_lo`, `3 Omega_hi <= shi^2 8 pi` -/
theorem a0num_interval {κ c H Ω Hlo Hhi Ωlo Ωhi slo shi : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hHlo : 0 < Hlo)
    (hH : Hlo ≤ H ∧ H ≤ Hhi) (hΩ : Ωlo ≤ Ω ∧ Ω ≤ Ωhi) (hslo : 0 ≤ slo) (hshi : 0 ≤ shi)
    (hlo : slo ^ 2 * (8 * π) ≤ 3 * Ωlo) (hhi : 3 * Ωhi ≤ shi ^ 2 * (8 * π)) :
    κ * c * Hlo * slo ≤ a0num κ c H Ω ∧ a0num κ c H Ω ≤ κ * c * Hhi * shi := by
  have hpi : 0 < 8 * π := by have := Real.pi_pos; linarith
  have hs1 : slo ≤ Real.sqrt (3 * Ω / (8 * π)) := by
    apply Real.le_sqrt_of_sq_le
    rw [le_div_iff₀ hpi]; linarith [hΩ.1]
  have hs2 : Real.sqrt (3 * Ω / (8 * π)) ≤ shi := by
    rw [Real.sqrt_le_iff]; refine ⟨hshi, ?_⟩; rw [div_le_iff₀ hpi]; linarith [hΩ.2]
  have hkc : 0 < κ * c := mul_pos hκ hc
  unfold a0num
  constructor
  · exact mul_le_mul (mul_le_mul_of_nonneg_left hH.1 hkc.le) hs1 hslo (by nlinarith [hH.1])
  · exact mul_le_mul (mul_le_mul_of_nonneg_left hH.2 hkc.le) hs2 (Real.sqrt_nonneg _)
      (by nlinarith [hH.1, hH.2])

/-- CERTIFIED INTERVAL (premises: kappa = 1/2 FITTED; c, G, Mpc declared; H0 in [66.9, 67.9] km/s/Mpc and Omega_Lambda in
    [0.6774, 0.6920] declared): 9.24e-11 < a0 < 9.48e-11 m/s^2. -/
theorem a0_interval {H0 ΩΛ : ℝ} (hH : 66.9 ≤ H0 ∧ H0 ≤ 67.9) (hΩ : 0.6774 ≤ ΩΛ ∧ ΩΛ ≤ 0.6920) :
    9.24e-11 < (1 / 2) * cSI * Real.sqrt (GSI * (3 * (H0 * 1000 / Mpc) ^ 2 * ΩΛ / (8 * π * GSI))) ∧
    (1 / 2) * cSI * Real.sqrt (GSI * (3 * (H0 * 1000 / Mpc) ^ 2 * ΩΛ / (8 * π * GSI))) < 9.48e-11 := by
  have hMpc : 0 < Mpc := by unfold Mpc; norm_num
  have hG : 0 < GSI := by unfold GSI; norm_num
  have hH0 : 0 ≤ H0 * 1000 / Mpc := by have := hH.1; positivity
  rw [a0_of_rhoLambda hG hH0]
  have hp1 := Real.pi_gt_d6
  have hp2 := Real.pi_lt_d6
  have b := a0num_interval (κ := 1 / 2) (c := cSI) (H := H0 * 1000 / Mpc) (Ω := ΩΛ)
    (Hlo := 66.9 * 1000 / Mpc) (Hhi := 67.9 * 1000 / Mpc) (Ωlo := 0.6774) (Ωhi := 0.6920)
    (slo := 0.28435) (shi := 0.287405) (by norm_num) (by unfold cSI; norm_num) (by positivity)
    ⟨by gcongr; exact hH.1, by gcongr; exact hH.2⟩ hΩ (by norm_num) (by norm_num)
    (by nlinarith) (by nlinarith)
  have e1 : (9.24e-11 : ℝ) < 1 / 2 * cSI * (66.9 * 1000 / Mpc) * 0.28435 := by
    unfold cSI Mpc; norm_num
  have e2 : 1 / 2 * cSI * (67.9 * 1000 / Mpc) * 0.287405 < (9.48e-11 : ℝ) := by
    unfold cSI Mpc; norm_num
  exact ⟨lt_of_lt_of_le e1 b.1, lt_of_le_of_lt b.2 e2⟩

/-- CERTIFIED POINT (premises: kappa = 1/2 FITTED; c, G, Mpc declared; H0 = 67.4 km/s/Mpc and Omega_Lambda = 0.6847
    declared): 9.36e-11 < a0 < 9.361e-11 m/s^2, the record's canonical 9.36e-11. -/
theorem a0_point :
    9.36e-11 < (1 / 2) * cSI * Real.sqrt (GSI * (3 * (67.4 * 1000 / Mpc) ^ 2 * 0.6847 / (8 * π * GSI))) ∧
    (1 / 2) * cSI * Real.sqrt (GSI * (3 * (67.4 * 1000 / Mpc) ^ 2 * 0.6847 / (8 * π * GSI))) < 9.361e-11 := by
  have hMpc : 0 < Mpc := by unfold Mpc; norm_num
  have hG : 0 < GSI := by unfold GSI; norm_num
  rw [a0_of_rhoLambda hG (by positivity)]
  have hp1 := Real.pi_gt_d6
  have hp2 := Real.pi_lt_d6
  have b := a0num_interval (κ := 1 / 2) (c := cSI) (H := 67.4 * 1000 / Mpc) (Ω := 0.6847)
    (Hlo := 67.4 * 1000 / Mpc) (Hhi := 67.4 * 1000 / Mpc) (Ωlo := 0.6847) (Ωhi := 0.6847)
    (slo := 0.285884) (shi := 0.285885) (by norm_num) (by unfold cSI; norm_num) (by positivity)
    ⟨le_rfl, le_rfl⟩ ⟨le_rfl, le_rfl⟩ (by norm_num) (by norm_num) (by nlinarith) (by nlinarith)
  have e1 : (9.36e-11 : ℝ) < 1 / 2 * cSI * (67.4 * 1000 / Mpc) * 0.285884 := by
    unfold cSI Mpc; norm_num
  have e2 : 1 / 2 * cSI * (67.4 * 1000 / Mpc) * 0.285885 < (9.361e-11 : ℝ) := by
    unfold cSI Mpc; norm_num
  exact ⟨lt_of_lt_of_le e1 b.1, lt_of_le_of_lt b.2 e2⟩

end A0Numeric
