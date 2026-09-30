import Mathlib
import PuzzleChain

/-! MUTATE controls for PuzzleChain.lean: each `M9*` is a FALSE variant re-using the true proof script with one wrong constant or forgotten hypothesis
(must FAIL to compile); each `M9*_refuted` proves the negation from the true theorems plus a witness model (must COMPILE). -/

open Real PuzzleChain

-- M9a: the premise IS a theorem of the definitions -- false
theorem M9a_premise_theorem : ∀ S : Setup, OpenPremise S := fun S => by
  refine ⟨?_⟩
  have := S.rho_iff
  have hp := Real.pi_pos
  unfold Setup.Lam
  field_simp
  nlinarith

theorem M9a_refuted : ¬ (∀ S : Setup, OpenPremise S) := none_is_theorem .premise

-- M9b: the area form with 16 pi^2 (wrong; true: 32 pi^2) is equivalent to the premise -- false
theorem M9b_area_wrong : ∀ S : Setup, (S.area * S.Lam = 16 * π ^ 2) ↔ OpenPremise S := fun S => by
  have := iff_premise .area S
  unfold Form.holds at this
  exact this

theorem M9b_refuted : ¬ (∀ S : Setup, (S.area * S.Lam = 16 * π ^ 2) ↔ OpenPremise S) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (h S_on).mpr S_on_premise
  have h2 := all_hold_S_on .area
  unfold Form.holds at h2
  nlinarith [sq_pos_of_pos hp]

-- M9c: the Rindler length = R* (wrong; true: 2 R*) is equivalent to the premise -- false
theorem M9c_rindler_wrong : ∀ S : Setup, (S.rindler = S.Rstar) ↔ OpenPremise S := fun S => by
  have := iff_premise .rindler S
  unfold Form.holds at this
  exact this

theorem M9c_refuted : ¬ (∀ S : Setup, (S.rindler = S.Rstar) ↔ OpenPremise S) := by
  intro h
  have h1 := (h S_on).mpr S_on_premise
  have h2 := all_hold_S_on .rindler
  unfold Form.holds at h2
  have hs := S_on.sqrt_rho_pos
  have hR : 0 < S_on.Rstar := by unfold Setup.Rstar; positivity
  linarith

-- M9d: kappa = 1 is equivalent to the premise -- false
theorem M9d_kappa_wrong : ∀ S : Setup, (S.kappa = 1) ↔ OpenPremise S := fun S => by
  have := iff_premise .kappa S
  unfold Form.holds at this
  exact this

theorem M9d_refuted : ¬ (∀ S : Setup, (S.kappa = 1) ↔ OpenPremise S) := by
  intro h
  have h1 := (h S_on).mpr S_on_premise
  have h2 := all_hold_S_on .kappa
  unfold Form.holds at h2
  rw [h1] at h2
  norm_num at h2

-- M9e: N = 4 is equivalent to the premise -- false
theorem M9e_N_wrong : ∀ S : Setup, (S.Nchan = 4) ↔ OpenPremise S := fun S => by
  have := iff_premise .N S
  unfold Form.holds at this
  exact this

theorem M9e_refuted : ¬ (∀ S : Setup, (S.Nchan = 4) ↔ OpenPremise S) := by
  intro h
  have h1 := (h S_on).mpr S_on_premise
  have h2 := all_hold_S_on .N
  unfold Form.holds at h2
  rw [h1] at h2
  norm_num at h2

-- M9f: M1 = (2/3) t_Lambda is equivalent to the premise -- false
theorem M9f_M1_wrong : ∀ S : Setup, (S.M1 = (2 / 3) * S.Rstar) ↔ OpenPremise S := fun S => by
  have := iff_premise .M1 S
  unfold Form.holds at this
  exact this

theorem M9f_refuted : ¬ (∀ S : Setup, (S.M1 = (2 / 3) * S.Rstar) ↔ OpenPremise S) := by
  intro h
  have h1 := (h S_on).mpr S_on_premise
  have h2 := all_hold_S_on .M1
  unfold Form.holds at h2
  have hs := S_on.sqrt_rho_pos
  have hR : 0 < S_on.Rstar := by unfold Setup.Rstar; positivity
  linarith

-- M9g: Z^2 = 8 pi/3 (the kappa = 1 kernel) is equivalent to the premise -- false
theorem M9g_Z_wrong : ∀ S : Setup, (S.Z ^ 2 = 8 * π / 3) ↔ OpenPremise S := fun S => by
  have := iff_premise .Zsq S
  unfold Form.holds at this
  exact this

theorem M9g_refuted : ¬ (∀ S : Setup, (S.Z ^ 2 = 8 * π / 3) ↔ OpenPremise S) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (h S_on).mpr S_on_premise
  have h2 := all_hold_S_on .Zsq
  unfold Form.holds at h2
  rw [h1] at h2
  nlinarith

-- M9h: W_v = 1 is equivalent to the premise -- false
theorem M9h_W_wrong : ∀ S : Setup, (S.Wv = 1) ↔ OpenPremise S := fun S => by
  have := iff_premise .Wv S
  unfold Form.holds at this
  exact this

theorem M9h_refuted : ¬ (∀ S : Setup, (S.Wv = 1) ↔ OpenPremise S) := by
  intro h
  have h1 := (h S_on).mpr S_on_premise
  have h2 := all_hold_S_on .Wv
  unfold Form.holds at h2
  rw [h1] at h2
  norm_num at h2

-- M9i: Z^2 kappa^2 = 32 pi/3 in every Setup (wrong; true: 8 pi/3) -- false
theorem M9i_relation_wrong (S : Setup) : S.Z ^ 2 * S.kappa ^ 2 = 32 * π / 3 := by
  have hp := Real.pi_pos
  have hL := S.L_pos
  have ha := S.a0_pos
  have hs2 := S.sqrt_rho_sq
  have hk : (S.a0 / Real.sqrt S.rho) ^ 2 = S.a0 ^ 2 / S.rho := by rw [div_pow, hs2]
  have hz : ((1 / S.L) / S.a0) ^ 2 = 1 / (S.L ^ 2 * S.a0 ^ 2) := by field_simp
  have hrho : S.rho = 3 / (8 * π * S.L ^ 2) := by unfold Setup.rho Setup.Lam; field_simp
  unfold Setup.Z Setup.kappa Setup.H
  rw [hk, hz, hrho]
  field_simp

theorem M9i_refuted : ¬ (∀ S : Setup, S.Z ^ 2 * S.kappa ^ 2 = 32 * π / 3) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h S_off
  rw [Zkappa_relation] at h1
  nlinarith

-- M9j: rho_Lambda A_dS = 3 F_max in every Setup (wrong: 6) -- false
theorem M9j_friend_wrong (S : Setup) : S.rho * (4 * π * S.L ^ 2) = 3 * (1 / 4) := by
  have hp := Real.pi_pos
  have hL := S.L_pos
  have hL0 : S.L ≠ 0 := hL.ne'
  unfold Setup.rho Setup.Lam
  field_simp
  ring

theorem M9j_refuted : ¬ (∀ S : Setup, S.rho * (4 * π * S.L ^ 2) = 3 * (1 / 4)) := by
  intro h
  have h1 := h S_off
  rw [(false_friends S_off).1] at h1
  norm_num at h1

-- M9k: Z = sqrt(32 pi/3) is rational -- false
theorem M9k_Z_rational : ∃ q : ℚ, (q : ℝ) = Real.sqrt (32 * π / 3) := by
  refine ⟨6, ?_⟩
  have hp := Real.pi_gt_three
  rw [eq_comm, Real.sqrt_eq_iff_mul_self_eq (by positivity) (by norm_num)]
  norm_num
  nlinarith

theorem M9k_refuted : ¬ (∃ q : ℚ, (q : ℝ) = Real.sqrt (32 * π / 3)) := fun ⟨q, hq⟩ => Z_irrational ⟨q, hq⟩

-- M9l: the premise holds in the family S_Z iff Z'^2 = 8 pi/3 (wrong; true: 32 pi/3) -- false
theorem M9l_family_wrong {Z' : ℝ} (hZ : 0 < Z') : OpenPremise (S_Z Z' hZ) ↔ Z' ^ 2 = 8 * π / 3 := by
  have := iff_premise .Zsq (S_Z Z' hZ)
  unfold Form.holds at this
  rw [S_Z_Z hZ] at this
  exact this.symm

theorem M9l_refuted : ¬ (∀ Z' : ℝ, ∀ hZ : 0 < Z', (OpenPremise (S_Z Z' hZ) ↔ Z' ^ 2 = 8 * π / 3)) := by
  intro h
  have hp := Real.pi_pos
  have hZp : 0 < Real.sqrt (32 * π / 3) := Real.sqrt_pos.mpr (by positivity)
  have hZ2 : Real.sqrt (32 * π / 3) ^ 2 = 32 * π / 3 := Real.sq_sqrt (by positivity)
  have h1 := (Z_free hZp).choose_spec.2
  have hz := (Z_free hZp).choose_spec.1
  -- use the family directly
  have h2 := (iff_premise .Zsq (S_Z (Real.sqrt (32 * π / 3)) hZp))
  unfold Form.holds at h2
  rw [S_Z_Z hZp, hZ2] at h2
  have h3 := (h2.mp rfl)
  have h4 := (h _ hZp).mp h3
  rw [hZ2] at h4
  nlinarith

-- M9m: a RATIONAL kappa gives a rational Z^2 = 8 pi/(3 kappa^2) -- false
theorem M9m_rational : ∃ q : ℚ, (q : ℝ) = 8 * π / (3 * ((1 / 2 : ℚ) : ℝ) ^ 2) := by
  refine ⟨100, ?_⟩
  have hp := Real.pi_gt_three
  push_cast
  field_simp
  nlinarith

theorem M9m_refuted : ¬ (∃ q : ℚ, (q : ℝ) = 8 * π / (3 * ((1 / 2 : ℚ) : ℝ) ^ 2)) := by
  rintro ⟨q, hq⟩
  exact kappa_rational_Z_irrational (1 / 2) (by norm_num) ⟨q, hq⟩

#print axioms M9a_refuted
#print axioms M9b_refuted
#print axioms M9c_refuted
#print axioms M9d_refuted
#print axioms M9e_refuted
#print axioms M9f_refuted
#print axioms M9g_refuted
#print axioms M9h_refuted
#print axioms M9i_refuted
#print axioms M9j_refuted
#print axioms M9k_refuted
#print axioms M9l_refuted
#print axioms M9m_refuted
#print axioms M9a_premise_theorem
#print axioms M9b_area_wrong
#print axioms M9c_rindler_wrong
#print axioms M9d_kappa_wrong
#print axioms M9e_N_wrong
#print axioms M9f_M1_wrong
#print axioms M9g_Z_wrong
#print axioms M9h_W_wrong
#print axioms M9i_relation_wrong
#print axioms M9j_friend_wrong
#print axioms M9k_Z_rational
#print axioms M9l_family_wrong
#print axioms M9m_rational
