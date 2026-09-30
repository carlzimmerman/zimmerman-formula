import Mathlib
import P4_macdowell_mansouri

/-! MUTATE controls for P4_macdowell_mansouri.lean: each `M4*` is a FALSE variant re-using the true proof script with one wrong constant
(must FAIL to compile); each `M4*_refuted` proves the negation from the true theorems plus an explicit instance (must COMPILE). -/

open Real MacDowellMansouri

-- M4a: matching with 8 pi in place of 16 pi -- false
theorem M4a_matching_wrong {L ħ G ig kg : ℝ} (hħ : 0 < ħ) (hG : 0 < G) :
    2 * (8 * π ^ 2 * ig) = kg * π * L ^ 2 / (ħ * G) ↔ ig = kg * L ^ 2 / (8 * π * ħ * G) := by
  have hp := Real.pi_pos
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  rw [eq_div_iff (by positivity), eq_div_iff (by positivity)]
  constructor
  · intro h
    have h3 : π * (ig * (8 * π * ħ * G) - kg * L ^ 2) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp h3 with h4 | h4
    · exact absurd h4 hp.ne'
    · linarith
  · intro h
    have h3 : ig * (8 * π * ħ * G) * π = kg * L ^ 2 * π := by rw [h]
    nlinarith [h3]

theorem M4a_refuted : ¬ (∀ L ħ G ig kg : ℝ, 0 < ħ → 0 < G →
    (2 * (8 * π ^ 2 * ig) = kg * π * L ^ 2 / (ħ * G) ↔ ig = kg * L ^ 2 / (8 * π * ħ * G))) := by
  intro h
  have hp := Real.pi_pos
  have h1 := (matching_iff (L := 1) (ħ := 1) (G := 1) (ig := 1 * 1 ^ 2 / (16 * π * 1 * 1)) (kg := 1) one_pos one_pos).mpr rfl
  have h2 := (h 1 1 1 _ 1 one_pos one_pos).mp h1
  field_simp at h2
  nlinarith

-- M4b: (1/4) ig |F|^2 Vol = 4 pi^2 ig per chirality -- false
theorem M4b_action_wrong {L ig V : ℝ} (hL : L ≠ 0) (hV : V = 8 * π ^ 2 * L ^ 4 / 3) :
    (1 / 4) * ig * (12 / L ^ 4) * V = 4 * π ^ 2 * ig := by
  rw [hV]
  field_simp; ring

theorem M4b_refuted : ¬ (∀ L ig V : ℝ, L ≠ 0 → V = 8 * π ^ 2 * L ^ 4 / 3 → (1 / 4) * ig * (12 / L ^ 4) * V = 4 * π ^ 2 * ig) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 1 (8 * π ^ 2 * 1 ^ 4 / 3) one_ne_zero rfl
  have h2 := (action_per_chirality (L := 1) (ig := 1) (V := 8 * π ^ 2 * 1 ^ 4 / 3) one_ne_zero rfl).1
  rw [h1] at h2
  nlinarith [sq_pos_of_pos hp]

-- M4c: ratio per chirality = 4 pi hbar G ig/L^2 (wrong factor 2) -- false
theorem M4c_ratio_wrong {L ħ G ig : ℝ} (hL : L ≠ 0) (hG : 0 < G) :
    (ħ * ig * (12 / L ^ 4) / 4) / rhoL L G = 4 * π * ħ * G * ig / L ^ 2 := by
  have hp := Real.pi_pos
  have h2 : G ≠ 0 := hG.ne'
  unfold rhoL
  field_simp
  ring

theorem M4c_refuted : ¬ (∀ L ħ G ig : ℝ, L ≠ 0 → 0 < G → (ħ * ig * (12 / L ^ 4) / 4) / rhoL L G = 4 * π * ħ * G * ig / L ^ 2) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 1 1 1 one_ne_zero one_pos
  rw [ratio_per_chirality one_ne_zero one_pos] at h1
  nlinarith

-- M4d: per-chirality ratio is 1 at k_g = 1 (true: 1/2) -- false
theorem M4d_pm_wrong {L ħ G ig : ℝ} (hL : L ≠ 0) (hħ : 0 < ħ) (hG : 0 < G) (h : ig = L ^ 2 / (16 * π * ħ * G)) :
    (ħ * ig * (12 / L ^ 4) / 4) / rhoL L G = 1 := by
  have hp := Real.pi_pos
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  rw [ratio_per_chirality hL hG, h]
  field_simp

theorem M4d_refuted : ¬ (∀ L ħ G ig : ℝ, L ≠ 0 → 0 < ħ → 0 < G → ig = L ^ 2 / (16 * π * ħ * G) →
    (ħ * ig * (12 / L ^ 4) / 4) / rhoL L G = 1) := by
  intro h
  have hp := Real.pi_pos
  have hig : (1 : ℝ) ^ 2 / (16 * π * 1 * 1) = 1 ^ 2 / (16 * π * 1 * 1) := rfl
  have h1 := h 1 1 1 _ one_ne_zero one_pos one_pos rfl
  have h2 := (ratio_matching (L := 1) (ħ := 1) (G := 1) (ig := 1 ^ 2 / (16 * π * 1 * 1)) (kg := 1) one_ne_zero one_pos one_pos
    (by ring)).1
  rw [h1] at h2
  norm_num at h2

-- M4e: with the Lagrangian's 1/4 present the pair ratio is 4 -- false
theorem M4e_pair_wrong {L ħ G ig : ℝ} (hL : L ≠ 0) (hħ : 0 < ħ) (hG : 0 < G) (h : ig = L ^ 2 / (16 * π * ħ * G)) :
    2 * ((ħ * ig * (12 / L ^ 4) / 4) / rhoL L G) = 4 := by
  have hp := Real.pi_pos
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  rw [ratio_per_chirality hL hG, h]
  field_simp
  ring

theorem M4e_refuted : ¬ (∀ L ħ G ig : ℝ, L ≠ 0 → 0 < ħ → 0 < G → ig = L ^ 2 / (16 * π * ħ * G) →
    2 * ((ħ * ig * (12 / L ^ 4) / 4) / rhoL L G) = 4) := by
  intro h
  have h1 := h 1 1 1 _ one_ne_zero one_pos one_pos rfl
  have h2 := (ratio_pair_not_four (L := 1) (ħ := 1) (G := 1) (ig := 1 ^ 2 / (16 * π * 1 * 1)) one_ne_zero one_pos one_pos rfl).2
  exact h2 h1

-- M4f: with the 1/4 omitted the pair ratio is 2 (true: 4) -- false
theorem M4f_quarter_wrong {L ħ G ig : ℝ} (hL : L ≠ 0) (hħ : 0 < ħ) (hG : 0 < G) (h : ig = L ^ 2 / (16 * π * ħ * G)) :
    (ħ * ig * (12 / L ^ 4) * 2) / rhoL L G = 2 := by
  have hp := Real.pi_pos
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  unfold rhoL
  rw [h]
  field_simp
  ring

theorem M4f_refuted : ¬ (∀ L ħ G ig : ℝ, L ≠ 0 → 0 < ħ → 0 < G → ig = L ^ 2 / (16 * π * ħ * G) →
    (ħ * ig * (12 / L ^ 4) * 2) / rhoL L G = 2) := by
  intro h
  have h1 := h 1 1 1 _ one_ne_zero one_pos one_pos rfl
  have h2 := quarter_omitted (L := 1) (ħ := 1) (G := 1) (ig := 1 ^ 2 / (16 * π * 1 * 1)) one_ne_zero one_pos one_pos rfl
  rw [h1] at h2
  norm_num at h2

-- M4g: the puzzle relocated: a0^2 = G s_pm/4 (true: /2) -- false
theorem M4g_relocation_wrong {G ρ a0 spm : ℝ} (h : G * ρ = 4 * a0 ^ 2) (h1 : spm = ρ / 2) : a0 ^ 2 = G * spm / 4 := by
  subst h1
  linarith

theorem M4g_refuted : ¬ (∀ G ρ a0 spm : ℝ, G * ρ = 4 * a0 ^ 2 → spm = ρ / 2 → a0 ^ 2 = G * spm / 4) := by
  intro h
  have h1 := h 1 1 (1 / 2) (1 / 2) (by norm_num) (by norm_num)
  norm_num at h1

-- M4h: 32 pi^2 = 4 x (4 pi^2) -- false
theorem M4h_ledger_wrong : 4 * (4 * π ^ 2) = 32 * π ^ 2 := by ring

theorem M4h_refuted : ¬ (4 * (4 * π ^ 2) = 32 * π ^ 2) := by
  have hp := Real.pi_pos
  intro h; nlinarith [sq_pos_of_pos hp]

#print axioms M4a_refuted
#print axioms M4b_refuted
#print axioms M4c_refuted
#print axioms M4d_refuted
#print axioms M4e_refuted
#print axioms M4f_refuted
#print axioms M4g_refuted
#print axioms M4h_refuted
#print axioms M4a_matching_wrong
#print axioms M4b_action_wrong
#print axioms M4c_ratio_wrong
#print axioms M4d_pm_wrong
#print axioms M4e_pair_wrong
#print axioms M4f_quarter_wrong
#print axioms M4g_relocation_wrong
#print axioms M4h_ledger_wrong
