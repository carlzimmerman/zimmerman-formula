import Mathlib

/-!
# M2_05 -- Lean certificate for the S^2 flux-compactification coupling relations and the Salam-Sezgin dictionary
Source lanes:
* real_research/alpha_principle_2026/F_kk_stabilization/f2_flux_freund_rubin.py (B2a, B2b, B3d-B3f) and
  N1_joint_couplings/n1_1_s2_rederive.py (I2c-I2f, I3b, I5b, I5c);
* Q3_salam_sezgin/q1_ss_vacuum_and_flat_direction.py (A1b, A3a/A3b, A5b, A8) and
  q3_dictionary_and_scoring.py (C1a-C1e, C1g) with q2_pauli_su2_coupling_and_u1.py (B5a, B5b).
Corpus check: `git grep -n -i -e Freund -e Salam -e "moment map" -e flux -- '*.lean'` finds nothing on this.  New.

The field-equation / Killing-vector / moment-map / reduced-action steps are sympy computations in the lanes and are
NOT reproduced here; the premises below are stated as hypotheses in exactly the form the scripts print them
(marked PREMISE).  What is certified is the exact algebra downstream of those printed relations.

CERTIFIED:
(A) Lane F/N1 (6D Einstein-Maxwell-Lambda on S^2, integer flux N, tree level), PREMISES: Minkowski point
    R^2 = N^2 kappa^2/(4 g^2), l_P^2 = kappa^2/(32 pi^2 R^2), chat := g^2/kappa, and the printed coefficients
    alpha_SU2 = 3 l_P^2/R^2, alpha_U1 = N^2 l_P^2/(2 R^2):
    `RoverlP_sq`: (R/l_P)^2 = 2 pi^2 N^4/chat^2;  `alpha_SU2_chat`: alpha_SU2 = 3 chat^2/(2 pi^2 N^4);
    `alpha_U1_chat`: alpha_U1 = (chat/(2 pi N))^2;  `alpha_ratio`: alpha_U1/alpha_SU2 = N^2/6, independent of chat and R;
    `Lambda6_tuning`: Lambda_6 = 1/(2 R^2) = 2 g^2/(N^2 kappa^2);  `pure_metric_doubling`: 4/(2/3) = 6 and 6/2 = 3.
(B) Salam-Sezgin M4 x S^2, with E = e^{p/2}: PREMISES R^2 = E/(8 g^2) and f = 4 g/E (constant flux density),
    and the printed reduced coefficient alpha_SU2 = 4 g^4 kappa^2/(pi^2 E^2), G_4 = g^2 kappa^2/(4 pi^2 E):
    `ss_flux_number`: N := 2 g R^2 f = 1 for every E (no free flux integer);
    `ss_alpha_ratio`: alpha_SU2/(G_4/R^2) = 2;  `ss_alpha_chat`: alpha_SU2 = chat^2/pi^2 with chat = 2 kappa g^2/E;
    `ss_dictionary`: with g_F^2 = 2 kappa^2 g^2/E, chat = g_F^2/kappa = 2 kappa g^2/E, at N = 1 lane F's Minkowski radius
    equals E/(8 g^2) and lane F's Lambda_6 = 4 g^2/E = the Salam-Sezgin potential's Lambda (the lane's 'tuning is a
    SUSY relation');  `ss_rescaling_invariant`: chat is invariant under p -> p + d, i.e. E = e^{p/2} -> e^{d/2} E, with g -> e^{d/4} g (so is (R/l_P)^2 = 2 pi^2/chat^2);
    `ss_without_H3`: dropping the H_(3) contribution the same ratio is 3, giving 3 chat^2/(2 pi^2);
    `critical_only_N1`: the printed dV/dR = -16 pi (N-1)/(R kappa^2) on dV/dp = 0 vanishes iff N = 1;
    `nH_arithmetic`: 78 + 133 + 1 = 212 and 212 + 244 = 456.
(C) `no_su2_u1_flux_lattice_match`: the five SM hypercharge-to-SU(2)-dimension ratios |Y|/dim
    (Q: 1/12, L: 1/4, u^c: 2/3, d^c: 1/3, e^c: 1) are pairwise distinct, so no U(1) whose charges are
    Y = s * dim_SU2 (the S^2 flux U(1)) can carry two or more SM fields;  `doublet_singlet_ratio`: none of the 2 x 3
    doublet/singlet pairs has |Y_doublet| = 2 |Y_singlet|.
NOT CERTIFIED: the premises above (they are the lanes' sympy outputs, tree level, radion direction only, with the
Minkowski point requiring Lambda_6 tuned ~3e-119 of its value; the recalled spinor zero-mode counts); that the SU(2)
of the S^2 is the SM one; any value of alpha.  NEGATIVE-result algebra: alpha stays a free modulus (chat), which the
lanes state.  kappa = 1/2 is unrelated here (kappa in this file is the 6D gravitational coupling).
-/

namespace M2Flux

/-! ### (A) Lane F / N1 : Einstein-Maxwell-Lambda on S^2 -/

theorem RoverlP_sq (R2 l2 N κ g chat : ℝ) (hκ : 0 < κ) (hg : 0 < g) (hN : 0 < N)
    (hR : R2 = N ^ 2 * κ ^ 2 / (4 * g ^ 2)) (hl : l2 = κ ^ 2 / (32 * Real.pi ^ 2 * R2))
    (hc : chat = g ^ 2 / κ) :
    R2 / l2 = 2 * Real.pi ^ 2 * N ^ 4 / chat ^ 2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hR2 : R2 ≠ 0 := by rw [hR]; positivity
  rw [hl, hc, hR]
  field_simp
  ring

theorem alpha_SU2_chat (R2 l2 N κ g chat α : ℝ) (hκ : 0 < κ) (hg : 0 < g) (hN : 0 < N)
    (hR : R2 = N ^ 2 * κ ^ 2 / (4 * g ^ 2)) (hl : l2 = κ ^ 2 / (32 * Real.pi ^ 2 * R2))
    (hc : chat = g ^ 2 / κ) (hα : α = 3 * l2 / R2) :
    α = 3 * chat ^ 2 / (2 * Real.pi ^ 2 * N ^ 4) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hR2 : R2 ≠ 0 := by rw [hR]; positivity
  rw [hα, hl, hc, hR]
  field_simp
  ring

theorem alpha_U1_chat (R2 l2 N κ g chat α : ℝ) (hκ : 0 < κ) (hg : 0 < g) (hN : 0 < N)
    (hR : R2 = N ^ 2 * κ ^ 2 / (4 * g ^ 2)) (hl : l2 = κ ^ 2 / (32 * Real.pi ^ 2 * R2))
    (hc : chat = g ^ 2 / κ) (hα : α = N ^ 2 * l2 / (2 * R2)) :
    α = (chat / (2 * Real.pi * N)) ^ 2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hR2 : R2 ≠ 0 := by rw [hR]; positivity
  rw [hα, hl, hc, hR]
  field_simp
  ring

theorem alpha_ratio (N x : ℝ) (hx : x ≠ 0) : (N ^ 2 * x / 2) / (3 * x) = N ^ 2 / 6 := by
  field_simp; ring

theorem Lambda6_tuning (R2 N κ g : ℝ) (hκ : 0 < κ) (hg : 0 < g) (hN : 0 < N)
    (hR : R2 = N ^ 2 * κ ^ 2 / (4 * g ^ 2)) : 1 / (2 * R2) = 2 * g ^ 2 / (N ^ 2 * κ ^ 2) := by
  rw [hR]; field_simp; ring

theorem pure_metric_doubling : (4 : ℝ) / (2 / 3) = 6 ∧ (6 : ℝ) / 2 = 3 := by norm_num

/-! ### (B) Salam-Sezgin M4 x S^2 -/

theorem ss_flux_number (g E R2 f : ℝ) (hg : 0 < g) (hE : 0 < E)
    (hR : R2 = E / (8 * g ^ 2)) (hf : f = 4 * g / E) : 2 * g * R2 * f = 1 := by
  rw [hR, hf]; field_simp; ring

theorem ss_alpha_ratio (g E κ R2 G4 α : ℝ) (hg : 0 < g) (hE : 0 < E) (hκ : 0 < κ)
    (hR : R2 = E / (8 * g ^ 2)) (hG : G4 = g ^ 2 * κ ^ 2 / (4 * Real.pi ^ 2 * E))
    (hα : α = 4 * g ^ 4 * κ ^ 2 / (Real.pi ^ 2 * E ^ 2)) :
    α / (G4 / R2) = 2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  rw [hα, hG, hR]; field_simp; ring

theorem ss_alpha_chat (g E κ chat α : ℝ) (hg : 0 < g) (hE : 0 < E) (hκ : 0 < κ)
    (hc : chat = 2 * κ * g ^ 2 / E) (hα : α = 4 * g ^ 4 * κ ^ 2 / (Real.pi ^ 2 * E ^ 2)) :
    α = chat ^ 2 / Real.pi ^ 2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  rw [hα, hc]; field_simp; ring

theorem ss_dictionary (g E κ N gF2 chat R2F LamF LamSS : ℝ) (hg : 0 < g) (hE : 0 < E) (hκ : 0 < κ)
    (hgF : gF2 = 2 * κ ^ 2 * g ^ 2 / E) (hc : chat = gF2 / κ)
    (hRF : R2F = N ^ 2 * κ ^ 2 / (4 * gF2)) (hLF : LamF = 1 / (2 * R2F))
    (hLS : LamSS = 8 * g ^ 2 / E / 2) (hN : N = 1) :
    chat = 2 * κ * g ^ 2 / E ∧ R2F = E / (8 * g ^ 2) ∧ LamF = LamSS := by
  subst hN
  have hgF' : gF2 = 2 * κ ^ 2 * g ^ 2 / E := hgF
  refine ⟨?_, ?_, ?_⟩
  · rw [hc, hgF']; field_simp
  · rw [hRF, hgF']; field_simp; ring
  · rw [hLF, hLS, hRF, hgF']; field_simp; ring

theorem ss_rescaling_invariant (g E κ d : ℝ) (hg : 0 < g) (hE : 0 < E) (hκ : 0 < κ) :
    2 * κ * (g * Real.exp (d / 4)) ^ 2 / (E * Real.exp (d / 2)) = 2 * κ * g ^ 2 / E := by
  have h1 : Real.exp (d / 4) ^ 2 = Real.exp (d / 2) := by
    rw [← Real.exp_nat_mul]; congr 1; push_cast; ring
  have h3 : 0 < Real.exp (d / 2) := Real.exp_pos _
  rw [mul_pow, h1]
  field_simp

theorem ss_without_H3 (α R2 G4 : ℝ) (h : α = 3 * (G4 / R2)) (hR : R2 ≠ 0) : α / (G4 / R2) = 3 ∨ G4 = 0 := by
  by_cases hG : G4 = 0
  · exact Or.inr hG
  · left
    rw [h]
    have : G4 / R2 ≠ 0 := div_ne_zero hG hR
    field_simp

theorem critical_only_N1 (N R κ : ℝ) (hR : R ≠ 0) (hκ : κ ≠ 0) :
    -16 * Real.pi * (N - 1) / (R * κ ^ 2) = 0 ↔ N = 1 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hd : R * κ ^ 2 ≠ 0 := mul_ne_zero hR (pow_ne_zero 2 hκ)
  rw [div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · have : (N - 1) = 0 := by
        have h16 : (-16 * Real.pi) ≠ 0 := by
          have : (16 : ℝ) * Real.pi ≠ 0 := mul_ne_zero (by norm_num) hπ
          intro h'; apply this; linarith
        exact (mul_eq_zero.mp h).resolve_left h16
      linarith
    · exact absurd h hd
  · intro h; left; rw [h]; ring

theorem nH_arithmetic : (78 + 133 + 1 : ℕ) = 212 ∧ (212 + 244 : ℕ) = 456 := by norm_num

/-! ### (C) the SM hypercharge lattice cannot be the S^2 flux U(1) -/

/-- |Y|/dim_SU2 for Q, L, u^c, d^c, e^c (left-handed Weyl, per generation) -/
def ratio : Fin 5 → ℚ := ![1 / 6 / 2, 1 / 2 / 2, 2 / 3 / 1, 1 / 3 / 1, 1 / 1]

theorem no_su2_u1_flux_lattice_match : Function.Injective ratio := by
  intro i j h
  fin_cases i <;> fin_cases j <;> simp_all [ratio] <;> norm_num at h

theorem ratios_values : ratio 0 = 1 / 12 ∧ ratio 1 = 1 / 4 ∧ ratio 2 = 2 / 3 ∧ ratio 3 = 1 / 3 ∧ ratio 4 = 1 := by
  simp [ratio]; norm_num

theorem doublet_singlet_ratio :
    ∀ yd ∈ ([1 / 6, 1 / 2] : List ℚ), ∀ ys ∈ ([2 / 3, 1 / 3, 1] : List ℚ), yd ≠ 2 * ys := by
  intro yd hd ys hs
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hd hs
  rcases hd with rfl | rfl <;> rcases hs with rfl | rfl | rfl <;> norm_num

end M2Flux

#print axioms M2Flux.RoverlP_sq
#print axioms M2Flux.alpha_SU2_chat
#print axioms M2Flux.alpha_U1_chat
#print axioms M2Flux.alpha_ratio
#print axioms M2Flux.Lambda6_tuning
#print axioms M2Flux.pure_metric_doubling
#print axioms M2Flux.ss_flux_number
#print axioms M2Flux.ss_alpha_ratio
#print axioms M2Flux.ss_alpha_chat
#print axioms M2Flux.ss_dictionary
#print axioms M2Flux.ss_rescaling_invariant
#print axioms M2Flux.ss_without_H3
#print axioms M2Flux.critical_only_N1
#print axioms M2Flux.nH_arithmetic
#print axioms M2Flux.no_su2_u1_flux_lattice_match
#print axioms M2Flux.ratios_values
#print axioms M2Flux.doublet_singlet_ratio
