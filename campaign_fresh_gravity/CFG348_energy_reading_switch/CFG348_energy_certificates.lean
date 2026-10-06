import Mathlib

/-!
# CFG348 -- certificates for the energy-reading switch eps_b = v^2/2 + U

* E1 FRW shell identity: with flat Friedmann H^2 = 8 pi G rho/3 + Lambda/3 the shell energy is exactly 0.
* E2 zero threshold has no OFF neighbourhood: a gate W = S(-eps/eps_on) with S > 0 on (0, oo) is > 0 arbitrarily
  close to eps = 0 on the bound side; E2c with E1, FRW sits on the gate's edge.
* E3 baryonic escape: nu > 2 => g_N r (nu/2 - 1) > 0; E3f flat curve beyond 2 G M / v_f^2 has v_f^2/2 - GM/r > 0.
* E4 velocity-reading gate no-ghost: eps_on > B s1/rho and S' <= s1 => rho + B W' > 0 (W' = -S'/eps_on).
* E5 saturated-interior fidelity: W' = W'' = 0 leaves both inertias equal to rho.
* E6 nested wells (numeric, from the run): the linear rms well exceeds the theory's minimum width, which exceeds the
  shallowest host's |eps| at 30 kpc.
-/

theorem E1_frw_shell (H G ρ Λ r : ℝ) (hF : H ^ 2 = 8 * Real.pi * G * ρ / 3 + Λ / 3) :
    H ^ 2 * r ^ 2 / 2 - 4 / 3 * Real.pi * G * ρ * r ^ 2 - Λ * r ^ 2 / 6 = 0 := by
  rw [show H ^ 2 * r ^ 2 / 2 = (H ^ 2) * r ^ 2 / 2 by ring, hF]; ring

theorem E2_no_off_nbhd (S : ℝ → ℝ) (hS : ∀ x, 0 < x → 0 < S x) (eon : ℝ) (heon : 0 < eon) :
    ∀ δ > 0, ∃ e : ℝ, -δ < e ∧ e < 0 ∧ 0 < S (-e / eon) := by
  intro δ hδ
  refine ⟨-δ / 2, by linarith, by linarith, hS _ ?_⟩
  apply div_pos <;> linarith

theorem E2c_frw_on_edge (S : ℝ → ℝ) (hS : ∀ x, 0 < x → 0 < S x) (eon H G ρ Λ r : ℝ) (heon : 0 < eon)
    (hF : H ^ 2 = 8 * Real.pi * G * ρ / 3 + Λ / 3) :
    (H ^ 2 * r ^ 2 / 2 - 4 / 3 * Real.pi * G * ρ * r ^ 2 - Λ * r ^ 2 / 6 = 0) ∧
    ∀ δ > 0, ∃ e : ℝ, -δ < e ∧ e < 0 ∧ 0 < S (-e / eon) :=
  ⟨E1_frw_shell H G ρ Λ r hF, E2_no_off_nbhd S hS eon heon⟩

theorem E3_baryonic_escape (gN r ν : ℝ) (hg : 0 < gN) (hr : 0 < r) (hν : 2 < ν) :
    0 < ν * gN * r / 2 - gN * r := by
  have : 0 < gN * r := mul_pos hg hr
  nlinarith

theorem E3f_flat_escape (GM vf2 r : ℝ) (hGM : 0 < GM) (hv : 0 < vf2) (hr : 2 * GM / vf2 < r) :
    0 < vf2 / 2 - GM / r := by
  have hr0 : 0 < r := lt_trans (div_pos (by linarith) hv) hr
  have h1 : 2 * GM < r * vf2 := by rwa [div_lt_iff₀ hv] at hr
  rw [sub_pos, div_lt_div_iff₀ hr0 (by norm_num : (0:ℝ) < 2)]
  linarith

theorem E4_no_ghost (ρ B s1 Sp eon : ℝ) (hρ : 0 < ρ) (hB : 0 ≤ B) (heon : 0 < eon) (hSp : Sp ≤ s1)
    (hw : B * s1 / ρ < eon) : 0 < ρ + B * (-Sp / eon) := by
  have h1 : B * s1 < eon * ρ := by rwa [div_lt_iff₀ hρ] at hw
  have h2 : B * Sp ≤ B * s1 := mul_le_mul_of_nonneg_left hSp hB
  have h3 : B * (-Sp / eon) = -(B * Sp) / eon := by ring
  rw [h3, neg_div, ← sub_eq_add_neg, sub_pos, div_lt_iff₀ heon]
  nlinarith

theorem E5_saturated_fidelity (ρ B W1 W2 v : ℝ) (h1 : W1 = 0) (h2 : W2 = 0) :
    ρ + B * W1 = ρ ∧ ρ + B * (W1 + W2 * v ^ 2) = ρ := by
  subst h1; subst h2; constructor <;> ring

/-- run numbers (m^2/s^2): sigma_Phi,lin(z=0) = 6.880e11; eps_on,min = 2.196e11; shallowest host |eps_ms(30 kpc)| = 2.572e10 -/
theorem E6_nested_wells :
    (2.196e11 : ℝ) < 6.880e11 ∧ (2.572e10 : ℝ) < 2.196e11 := by norm_num

/-- an ON host needs |eps_host| >= eps_on; a linear well deeper than eps_on is then ON too (the reader is additive). -/
theorem E6g_nested_general (eon ehost sphi : ℝ) (hon : eon ≤ ehost) (hdeep : ehost ≤ sphi) : eon ≤ sphi :=
  le_trans hon hdeep

#print axioms E1_frw_shell
#print axioms E2c_frw_on_edge
#print axioms E3_baryonic_escape
#print axioms E3f_flat_escape
#print axioms E4_no_ghost
#print axioms E5_saturated_fidelity
#print axioms E6_nested_wells
#print axioms E6g_nested_general
