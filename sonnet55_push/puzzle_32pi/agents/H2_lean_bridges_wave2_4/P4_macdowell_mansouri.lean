import Mathlib

open Real

/-!
# P4: MacDowell-Mansouri / same-instanton density ratio (lane Q, lane A)

Conventions: L > 0 the de Sitter radius, hbar > 0, G > 0 (hbar and G kept, so the hbar-bookkeeping of lane Q is visible); rho_Lambda = 3/(8 pi G L^2) (Lambda = 3/L^2,
rho_Lambda = Lambda/(8 pi G)).  ig = 1/g^2 is the inverse squared gauge coupling of the SU(2)_+ x SU(2)_- description of gravity on S^4(L).
S_dS = A/(4 G hbar) = pi L^2/(G hbar) (A = 4 pi L^2).  Per chirality the (anti)self-dual field of the S^4 spin connection has |F|^2 = 12/L^4 (INPUT, lane Q q04; the
Euclidean YM action density is (hbar/(4 g^2))|F|^2) and Vol(S^4_L) = 8 pi^2 L^4/3 (INPUT, certified in the earlier lane H2_s4_euler).

CERTIFIED (premises => conclusions):
 (a) `SdS_eq`: A/(4 G hbar) = pi L^2/(G hbar).  `matching_iff`: k_g-matching 2 x (8 pi^2 ig) = k_g pi L^2/(hbar G) <=> ig = k_g L^2/(16 pi hbar G); k_g = 1 is lane A's matching
     S_dS/hbar = 2 x (8 pi^2/g^2)  (`matching_kg1`).  The matching DEFINES g: it is not a check.
 (b) `action_per_chirality`: (1/4) ig |F|^2 Vol = 8 pi^2 ig per chirality (from |F|^2 Vol = 12 x 8 pi^2/3 = 32 pi^2), 16 pi^2 ig for the pair.
 (c) `ratio_per_chirality`: (hbar ig |F|^2/4)/rho_Lambda = 8 pi hbar G ig/L^2 = k_g/2 with ig = k_g L^2/(16 pi hbar G), so 1/2 per chirality and 1 for the pair at k_g = 1
     (`ratio_matching`); the pair value 1 is the EH-on-shell-density identity (= rho_Lambda), by construction of k_g.
 (d) `quarter_omitted`: with the Lagrangian's 1/4 OMITTED the pair ratio is exactly 4 at k_g = 1 (the only way a "4" appears); with the 1/4 present it is 1, not 4 (`ratio_pair_not_four`).
 (e) `puzzle_rewritten`: G rho_Lambda = 4 a0^2 with s_pm = rho_Lambda/2 (one chirality) reads a0^2 = G s_pm/2 = G s_pair/4: the puzzle's 4 relocated, not derived.
 (f) `unit_ledger`: 32 pi^2 = 4 x 8 pi^2 = Vol(S^3) x 16 = 2 x 16 pi^2 (arithmetic of lane Q's ledger).

NOT certified: that gravity is an SU(2) x SU(2) gauge theory with that coupling, that the S^4 instanton is the vacuum, |F|^2 = 12/L^4, anything about a0 or kappa = 1/2.
-/

namespace MacDowellMansouri

/-- de Sitter entropy in units of hbar: A/(4 G hbar) with A = 4 pi L^2 -/
theorem SdS_eq {L ħ G : ℝ} (hħ : 0 < ħ) (hG : 0 < G) : 4 * π * L ^ 2 / (4 * G * ħ) = π * L ^ 2 / (ħ * G) := by
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  field_simp

/-- (a) matching: 2 x (8 pi^2 ig) = k_g pi L^2/(hbar G)  <=>  ig = k_g L^2/(16 pi hbar G) -/
theorem matching_iff {L ħ G ig kg : ℝ} (hħ : 0 < ħ) (hG : 0 < G) :
    2 * (8 * π ^ 2 * ig) = kg * π * L ^ 2 / (ħ * G) ↔ ig = kg * L ^ 2 / (16 * π * ħ * G) := by
  have hp := Real.pi_pos
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  rw [eq_div_iff (by positivity), eq_div_iff (by positivity)]
  constructor
  · intro h
    have h3 : π * (ig * (16 * π * ħ * G) - kg * L ^ 2) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp h3 with h4 | h4
    · exact absurd h4 hp.ne'
    · linarith
  · intro h
    have h3 : ig * (16 * π * ħ * G) * π = kg * L ^ 2 * π := by rw [h]
    nlinarith [h3]

theorem matching_kg1 {L ħ G ig : ℝ} (hħ : 0 < ħ) (hG : 0 < G) :
    2 * (8 * π ^ 2 * ig) = π * L ^ 2 / (ħ * G) ↔ ig = L ^ 2 / (16 * π * ħ * G) := by
  have := matching_iff (L := L) (ħ := ħ) (G := G) (ig := ig) (kg := 1) hħ hG
  simpa using this

/-- (b) (1/4) ig |F|^2 Vol with |F|^2 = 12/L^4, Vol = 8 pi^2 L^4/3: 8 pi^2 ig per chirality -/
theorem action_per_chirality {L ig V : ℝ} (hL : L ≠ 0) (hV : V = 8 * π ^ 2 * L ^ 4 / 3) :
    (1 / 4) * ig * (12 / L ^ 4) * V = 8 * π ^ 2 * ig ∧ (12 / L ^ 4) * V = 32 * π ^ 2 := by
  rw [hV]
  constructor <;> field_simp <;> ring

theorem action_pair {L ig V : ℝ} (hL : L ≠ 0) (hV : V = 8 * π ^ 2 * L ^ 4 / 3) :
    2 * ((1 / 4) * ig * (12 / L ^ 4) * V) = 16 * π ^ 2 * ig := by
  rw [(action_per_chirality hL hV).1]; ring

/-- rho_Lambda = 3/(8 pi G L^2) -/
noncomputable def rhoL (L G : ℝ) : ℝ := 3 / (8 * π * G * L ^ 2)

/-- (c) YM action density per chirality over rho_Lambda: (hbar ig |F|^2/4)/rho_Lambda = 8 pi hbar G ig/L^2 -/
theorem ratio_per_chirality {L ħ G ig : ℝ} (hL : L ≠ 0) (hG : 0 < G) :
    (ħ * ig * (12 / L ^ 4) / 4) / rhoL L G = 8 * π * ħ * G * ig / L ^ 2 := by
  have hp := Real.pi_pos
  have h2 : G ≠ 0 := hG.ne'
  unfold rhoL
  field_simp
  ring

/-- with ig = k_g L^2/(16 pi hbar G): the ratio is k_g/2 per chirality, k_g for the pair; k_g = 1: 1/2 and 1 -/
theorem ratio_matching {L ħ G ig kg : ℝ} (hL : L ≠ 0) (hħ : 0 < ħ) (hG : 0 < G) (h : ig = kg * L ^ 2 / (16 * π * ħ * G)) :
    (ħ * ig * (12 / L ^ 4) / 4) / rhoL L G = kg / 2 ∧ 2 * ((ħ * ig * (12 / L ^ 4) / 4) / rhoL L G) = kg := by
  have hp := Real.pi_pos
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  rw [ratio_per_chirality hL hG, h]
  constructor
  · field_simp; ring
  · field_simp; ring

/-- (d) the Lagrangian's 1/4 omitted: the pair ratio hbar(|F+|^2 + |F-|^2) ig/rho_Lambda is 4 at k_g = 1 -/
theorem quarter_omitted {L ħ G ig : ℝ} (hL : L ≠ 0) (hħ : 0 < ħ) (hG : 0 < G) (h : ig = L ^ 2 / (16 * π * ħ * G)) :
    (ħ * ig * (12 / L ^ 4) * 2) / rhoL L G = 4 := by
  have hp := Real.pi_pos
  have h1 : ħ ≠ 0 := hħ.ne'
  have h2 : G ≠ 0 := hG.ne'
  unfold rhoL
  rw [h]
  field_simp
  ring

/-- with the 1/4 present the pair ratio is 1, never 4 -/
theorem ratio_pair_not_four {L ħ G ig : ℝ} (hL : L ≠ 0) (hħ : 0 < ħ) (hG : 0 < G) (h : ig = L ^ 2 / (16 * π * ħ * G)) :
    2 * ((ħ * ig * (12 / L ^ 4) / 4) / rhoL L G) = 1 ∧ (2 * ((ħ * ig * (12 / L ^ 4) / 4) / rhoL L G)) ≠ 4 := by
  have := (ratio_matching (ig := ig) hL hħ hG (kg := 1) (by rw [h]; ring)).2
  refine ⟨this, ?_⟩
  rw [this]; norm_num

/-- (e) the puzzle G rho = 4 a0^2, with s_pm = rho/2 (one chirality) and s_pair = rho: a0^2 = G s_pm/2 = G s_pair/4 (relabelling) -/
theorem puzzle_rewritten {G ρ a0 spm spair : ℝ} (h : G * ρ = 4 * a0 ^ 2) (h1 : spm = ρ / 2) (h2 : spair = ρ) :
    a0 ^ 2 = G * spm / 2 ∧ a0 ^ 2 = G * spair / 4 := by
  subst h1 h2
  constructor <;> linarith

/-- (f) the ledger of 32 pi^2 -/
theorem unit_ledger : 4 * (8 * π ^ 2) = 32 * π ^ 2 ∧ (2 * π ^ 2) * 16 = 32 * π ^ 2 ∧ 2 * (16 * π ^ 2) = 32 * π ^ 2 := by
  refine ⟨by ring, by ring, by ring⟩

end MacDowellMansouri

#print axioms MacDowellMansouri.SdS_eq
#print axioms MacDowellMansouri.matching_iff
#print axioms MacDowellMansouri.matching_kg1
#print axioms MacDowellMansouri.action_per_chirality
#print axioms MacDowellMansouri.ratio_per_chirality
#print axioms MacDowellMansouri.ratio_matching
#print axioms MacDowellMansouri.quarter_omitted
#print axioms MacDowellMansouri.ratio_pair_not_four
#print axioms MacDowellMansouri.puzzle_rewritten
#print axioms MacDowellMansouri.unit_ledger
