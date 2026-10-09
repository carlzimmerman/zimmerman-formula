import Mathlib

/-!
# LEPTON_CHAIN: what follows if the lepton sector is TM1 + Dirac + m_lightest = ρ_Λ^{1/4}

Criteria frozen in LEPTON_CHAIN_CRITERIA.md (8eb733fc8). This file certifies IMPLICATIONS from stated assumptions. It does not
certify that the assumptions hold in nature.

CERTIFIED (zero sorry, standard axioms):
(L1) `tm1_s12_rule`: c12²c13² = 2/3 (TM1's |U_e1|²), with s12² + c12² = 1, s13² + c13² = 1 and s13² < 1, gives
     s12² = 1 − 2/(3(1 − s13²)).
(L2) `tm1_s12_window`: TM1 with s13² ∈ [0.020, 0.025] gives s12² ∈ [0.3162, 0.3198]. So if s13² is in [0.020, 0.025] and
     the whole 3σ s12² range lies outside [0.3162, 0.3198], TM1 is excluded. (The criteria froze an upper edge of 0.3197; the true value at s13² = 0.020 is 0.319728, which was my
     arithmetic slip. Disclosed; the certified edge is 0.3198.)
(L3) `tm2_s12_floor`: TM2 (s12²c13² = 1/3, with 0 < c13² ≤ 1) gives s12² ≥ 1/3.
(L4) `tm1_octant_decides_delta`: the main result. Take the first PMNS column in the PDG parametrisation, built as complex numbers:
       U_μ1 = −s12 c23 − c12 s23 s13 e^{iδ},   U_τ1 = s12 s23 − c12 c23 s13 e^{iδ}.
     Impose TM1 (c12²c13² = 2/3, |U_μ1|² = |U_τ1|² = 1/6), positive sines and cosines with s² + c² = 1, and s13² < 1/5. Then:
     upper octant (s23² > 1/2) ⇒ cos δ > 0; lower octant (s23² < 1/2) ⇒ cos δ < 0; maximal mixing (s23² = 1/2) ⇒ cos δ = 0.
     The proof goes through the identity 4 s12 c12 s13 s23 c23 cos δ = (s12² − c12² s13²)(s23² − c23²) with
     3(s12² − c12² s13²)(1 − s13²) = 1 − 5 s13² (`tm1_mu_tau_identity`, `tm1_K_pos`).
     `tm1_consistent`: the hypotheses are NOT vacuous. An exact witness meets all of them: s13² = 1/50, c12² = 100/147,
     s23² = 1/2, δ = π/2.
(L5) `spectrum_sum_window` (normal ordering): m1 = 2.24 meV, Δm²21 ∈ [7.38, 7.62]e-5 eV² and Δm²31 ∈ [2.49, 2.56]e-3 eV², with
     m_i = √(m1² + Δm²i1), give 0.0609 < Σ m < 0.0620 eV. `below_desi`: 0.0620 < 0.0642 (DESI DR2, ΛCDM-based, quoted).
(L6) `mbeta_bound`: same m1 and splittings, the TM1 row |U_e|² = (2/3, 1/3 − s13², s13²) with 0 ≤ s13² ≤ 0.0228:
     m_β = √(Σ|U_ei|² m_i²) < 0.0095 eV. That is below Project 8's stated ~0.04 eV goal, so this output is not testable.
(L7) `rho_from_a0`, `mlight_scaling`: a0 = κ c √(G ρ) (κ, c, G > 0, ρ ≥ 0) gives ρ = a0²/(κ² c² G). Substituting, m⁴ = K ρ reads
     m⁴ = K a0²/(κ² c² G). If m_j⁴ = K ρ_j at two footings (a0_1, a0_2), with the same κ, c, G and any K, then
     m_2⁴ a0_1² = m_1⁴ a0_2². Read informally: |m_lightest| ∝ √a0 for a0 ≠ 0.
(L8) `dirac_no_0nubb`: DEFINITIONAL. Dirac is modelled only as zero Majorana masses: if every Majorana mass is zero, m_ββ = |Σ U_ei² m_i| = 0. No physics content.

NOT CERTIFIED (inputs and assumptions, stated plainly):
- TM1 itself;
- that neutrinos are Dirac (atomos FS11: non-SUSY AdS conjecture plus numerics);
- m_lightest = ρ_Λ^{1/4} (on its own a coincidence);
- κ = 1/2 (FITTED);
- the δ values 262°/285° (FS16 Python);
- the residual-symmetry scans (FS01/FS03 Python);
- every experimental number (quoted inputs).
Lean shows what follows from these assumptions and what would falsify them. Joint consistency is witnessed only for L4's
hypotheses (`tm1_consistent`). It does not show why the
lepton sector is like this.
-/

namespace LeptonChain
open Complex

/-! ## L1–L3: the solar angle -/

theorem tm1_s12_rule (s12 c12 s13 c13 : ℝ) (h12 : s12 ^ 2 + c12 ^ 2 = 1) (h13 : s13 ^ 2 + c13 ^ 2 = 1)
    (hy : s13 ^ 2 < 1) (htm1 : c12 ^ 2 * c13 ^ 2 = 2 / 3) : s12 ^ 2 = 1 - 2 / (3 * (1 - s13 ^ 2)) := by
  have hc13 : c13 ^ 2 = 1 - s13 ^ 2 := by linarith
  have hpos : (0:ℝ) < 3 * (1 - s13 ^ 2) := by linarith
  have hc12 : c12 ^ 2 = 2 / (3 * (1 - s13 ^ 2)) := by
    rw [eq_div_iff hpos.ne']; rw [hc13] at htm1; linarith
  linarith

theorem tm1_s12_window (s12 c12 s13 c13 : ℝ) (h12 : s12 ^ 2 + c12 ^ 2 = 1) (h13 : s13 ^ 2 + c13 ^ 2 = 1)
    (htm1 : c12 ^ 2 * c13 ^ 2 = 2 / 3) (hlo : (0.020 : ℝ) ≤ s13 ^ 2) (hhi : s13 ^ 2 ≤ 0.025) :
    (0.3162 : ℝ) ≤ s12 ^ 2 ∧ s12 ^ 2 ≤ 0.3198 := by
  have hc12 : c12 ^ 2 = 1 - s12 ^ 2 := by linarith
  have hc13 : c13 ^ 2 = 1 - s13 ^ 2 := by linarith
  rw [hc12, hc13] at htm1
  constructor
  · by_contra h; push Not at h
    nlinarith [mul_le_mul_of_nonneg_left hhi (by nlinarith : (0:ℝ) ≤ 1 - s12 ^ 2)]
  · by_contra h; push Not at h
    nlinarith [mul_le_mul_of_nonneg_left hlo (by nlinarith [sq_nonneg c12] : (0:ℝ) ≤ 1 - s12 ^ 2)]

theorem tm2_s12_floor (s12 c13 : ℝ) (_hc : 0 < c13 ^ 2) (hc1 : c13 ^ 2 ≤ 1) (htm2 : s12 ^ 2 * c13 ^ 2 = 1 / 3) :
    (1 : ℝ) / 3 ≤ s12 ^ 2 := by
  nlinarith [sq_nonneg s12]

/-! ## L4: the octant decides the half-plane of δ -/

/-- |a + b e^{iδ}|² = a² + b² + 2ab cos δ for real a, b, δ. -/
theorem normSq_two_term (a b δ : ℝ) :
    Complex.normSq ((a : ℂ) + (b : ℂ) * Complex.exp ((δ : ℂ) * Complex.I)) = a ^ 2 + b ^ 2 + 2 * a * b * Real.cos δ := by
  rw [Complex.normSq_apply]
  simp [Complex.exp_ofReal_mul_I_re, Complex.exp_ofReal_mul_I_im]
  linear_combination b ^ 2 * Real.sin_sq_add_cos_sq δ

/-- PDG U_μ1 = −s12 c23 − c12 s23 s13 e^{iδ}. -/
noncomputable def Umu1 (s12 c12 s13 s23 c23 δ : ℝ) : ℂ :=
  ((-(s12 * c23) : ℝ) : ℂ) + ((-(c12 * s23 * s13) : ℝ) : ℂ) * Complex.exp ((δ : ℂ) * Complex.I)

/-- PDG U_τ1 = s12 s23 − c12 c23 s13 e^{iδ}. -/
noncomputable def Utau1 (s12 c12 s13 s23 c23 δ : ℝ) : ℂ :=
  ((s12 * s23 : ℝ) : ℂ) + ((-(c12 * c23 * s13) : ℝ) : ℂ) * Complex.exp ((δ : ℂ) * Complex.I)

theorem tm1_mu_tau_identity (s12 c12 s13 s23 c23 δ : ℝ)
    (hmu : Complex.normSq (Umu1 s12 c12 s13 s23 c23 δ) = 1 / 6)
    (htau : Complex.normSq (Utau1 s12 c12 s13 s23 c23 δ) = 1 / 6) :
    4 * (s12 * c12 * s13 * s23 * c23) * Real.cos δ = (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) * (s23 ^ 2 - c23 ^ 2) := by
  unfold Umu1 at hmu; unfold Utau1 at htau
  rw [normSq_two_term] at hmu htau
  linear_combination hmu - htau

theorem tm1_K_pos (s12 c12 s13 c13 : ℝ) (h12 : s12 ^ 2 + c12 ^ 2 = 1) (h13 : s13 ^ 2 + c13 ^ 2 = 1)
    (htm1 : c12 ^ 2 * c13 ^ 2 = 2 / 3) (hsmall : s13 ^ 2 < 1 / 5) :
    3 * (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) * (1 - s13 ^ 2) = 1 - 5 * s13 ^ 2 ∧ 0 < s12 ^ 2 - c12 ^ 2 * s13 ^ 2 := by
  have hc13 : c13 ^ 2 = 1 - s13 ^ 2 := by linarith
  have hs12 : s12 ^ 2 = 1 - c12 ^ 2 := by linarith
  have key : 3 * (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) * (1 - s13 ^ 2) = 1 - 5 * s13 ^ 2 := by
    rw [hs12]; rw [hc13] at htm1; linear_combination (-3 * (1 + s13 ^ 2)) * htm1
  refine ⟨key, ?_⟩
  by_contra h; push Not at h
  nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ -(s12 ^ 2 - c12 ^ 2 * s13 ^ 2)) (by nlinarith : (0:ℝ) ≤ 1 - s13 ^ 2)]

theorem tm1_octant_decides_delta (s12 c12 s13 c13 s23 c23 δ : ℝ)
    (p12 : 0 < s12) (q12 : 0 < c12) (p13 : 0 < s13) (p23 : 0 < s23) (q23 : 0 < c23)
    (h12 : s12 ^ 2 + c12 ^ 2 = 1) (h13 : s13 ^ 2 + c13 ^ 2 = 1) (h23 : s23 ^ 2 + c23 ^ 2 = 1)
    (htm1 : c12 ^ 2 * c13 ^ 2 = 2 / 3)
    (hmu : Complex.normSq (Umu1 s12 c12 s13 s23 c23 δ) = 1 / 6)
    (htau : Complex.normSq (Utau1 s12 c12 s13 s23 c23 δ) = 1 / 6)
    (hsmall : s13 ^ 2 < 1 / 5) :
    (1 / 2 < s23 ^ 2 → 0 < Real.cos δ) ∧ (s23 ^ 2 < 1 / 2 → Real.cos δ < 0) ∧ (s23 ^ 2 = 1 / 2 → Real.cos δ = 0) := by
  have hid := tm1_mu_tau_identity s12 c12 s13 s23 c23 δ hmu htau
  have hK := (tm1_K_pos s12 c12 s13 c13 h12 h13 htm1 hsmall).2
  have hX : 0 < 4 * (s12 * c12 * s13 * s23 * c23) := by positivity
  refine ⟨fun hu => ?_, fun hl => ?_, fun hm => ?_⟩
  · have : 0 < (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) * (s23 ^ 2 - c23 ^ 2) := mul_pos hK (by linarith)
    rw [← hid] at this
    exact pos_of_mul_pos_right this hX.le
  · have : (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) * (s23 ^ 2 - c23 ^ 2) < 0 := mul_neg_of_pos_of_neg hK (by linarith)
    rw [← hid] at this
    by_contra h; push Not at h
    nlinarith [mul_nonneg hX.le h]
  · have : (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) * (s23 ^ 2 - c23 ^ 2) = 0 := by rw [show s23 ^ 2 - c23 ^ 2 = 0 by linarith]; ring
    rw [← hid] at this
    rcases mul_eq_zero.mp this with h | h
    · exact absurd h hX.ne'
    · exact h

theorem tm1_consistent : ∃ s12 c12 s13 c13 s23 c23 δ : ℝ,
    0 < s12 ∧ 0 < c12 ∧ 0 < s13 ∧ 0 < s23 ∧ 0 < c23 ∧
    s12 ^ 2 + c12 ^ 2 = 1 ∧ s13 ^ 2 + c13 ^ 2 = 1 ∧ s23 ^ 2 + c23 ^ 2 = 1 ∧ c12 ^ 2 * c13 ^ 2 = 2 / 3 ∧
    Complex.normSq (Umu1 s12 c12 s13 s23 c23 δ) = 1 / 6 ∧ Complex.normSq (Utau1 s12 c12 s13 s23 c23 δ) = 1 / 6 ∧
    s13 ^ 2 < 1 / 5 := by
  refine ⟨Real.sqrt (47 / 147), Real.sqrt (100 / 147), Real.sqrt (1 / 50), Real.sqrt (49 / 50), Real.sqrt (1 / 2),
    Real.sqrt (1 / 2), Real.pi / 2, ?_⟩
  have e1 := Real.sq_sqrt (show (0:ℝ) ≤ 47 / 147 by norm_num)
  have e2 := Real.sq_sqrt (show (0:ℝ) ≤ 100 / 147 by norm_num)
  have e3 := Real.sq_sqrt (show (0:ℝ) ≤ 1 / 50 by norm_num)
  have e4 := Real.sq_sqrt (show (0:ℝ) ≤ 49 / 50 by norm_num)
  have e5 := Real.sq_sqrt (show (0:ℝ) ≤ 1 / 2 by norm_num)
  unfold Umu1 Utau1
  rw [normSq_two_term, normSq_two_term, Real.cos_pi_div_two]
  refine ⟨by positivity, by positivity, by positivity, by positivity, by positivity, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  all_goals (simp only [mul_pow, neg_sq, mul_zero, add_zero, e1, e2, e3, e4, e5]; norm_num)

/-! ## L5–L6: the mass spectrum -/

theorem spectrum_sum_window (d21 d31 : ℝ) (a1 : (7.38e-5 : ℝ) ≤ d21) (a2 : d21 ≤ 7.62e-5)
    (b1 : (2.49e-3 : ℝ) ≤ d31) (b2 : d31 ≤ 2.56e-3) :
    let m1 : ℝ := 2.24e-3
    (0.0609 : ℝ) < m1 + Real.sqrt (m1 ^ 2 + d21) + Real.sqrt (m1 ^ 2 + d31) ∧
      m1 + Real.sqrt (m1 ^ 2 + d21) + Real.sqrt (m1 ^ 2 + d31) < 0.0620 := by
  intro m1
  have l2 : (0.0088 : ℝ) < Real.sqrt (m1 ^ 2 + d21) := Real.lt_sqrt (by norm_num) |>.mpr (by norm_num [m1]; linarith)
  have l3 : (0.0499 : ℝ) < Real.sqrt (m1 ^ 2 + d31) := Real.lt_sqrt (by norm_num) |>.mpr (by norm_num [m1]; linarith)
  have u2 : Real.sqrt (m1 ^ 2 + d21) < 0.00902 := (Real.sqrt_lt' (by norm_num)).mpr (by norm_num [m1]; linarith)
  have u3 : Real.sqrt (m1 ^ 2 + d31) < 0.0507 := (Real.sqrt_lt' (by norm_num)).mpr (by norm_num [m1]; linarith)
  constructor <;> norm_num [m1] at * <;> linarith

theorem below_desi : (0.0620 : ℝ) < 0.0642 := by norm_num

theorem mbeta_bound (d21 d31 y : ℝ) (a2 : d21 ≤ 7.62e-5) (_a0 : 0 ≤ d21) (b2 : d31 ≤ 2.56e-3) (_b0 : 0 ≤ d31)
    (y0 : 0 ≤ y) (y1 : y ≤ 0.0228) :
    let m1 : ℝ := 2.24e-3
    Real.sqrt (2 / 3 * m1 ^ 2 + (1 / 3 - y) * (m1 ^ 2 + d21) + y * (m1 ^ 2 + d31)) < 0.0095 := by
  intro m1
  rw [Real.sqrt_lt' (by norm_num)]
  have : (1 / 3 - y) * d21 ≤ 1 / 3 * 7.62e-5 := by nlinarith
  have : y * d31 ≤ 0.0228 * 2.56e-3 := by nlinarith
  norm_num [m1] at *; nlinarith

/-! ## L7: the framework link (a0 → ρ → m_lightest) -/

theorem rho_from_a0 (a0 κ c G ρ : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 ≤ ρ)
    (h : a0 = κ * c * Real.sqrt (G * ρ)) : ρ = a0 ^ 2 / (κ ^ 2 * c ^ 2 * G) := by
  have hs : Real.sqrt (G * ρ) ^ 2 = G * ρ := Real.sq_sqrt (by positivity)
  rw [h, eq_div_iff (by positivity)]
  rw [mul_pow, mul_pow, hs]; ring

theorem mlight_scaling (a1 a2 κ c G ρ1 ρ2 K m1 m2 : ℝ) (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G)
    (hρ1 : 0 ≤ ρ1) (hρ2 : 0 ≤ ρ2)
    (h1 : a1 = κ * c * Real.sqrt (G * ρ1)) (h2 : a2 = κ * c * Real.sqrt (G * ρ2))
    (hm1 : m1 ^ 4 = K * ρ1) (hm2 : m2 ^ 4 = K * ρ2) : m2 ^ 4 * a1 ^ 2 = m1 ^ 4 * a2 ^ 2 := by
  rw [hm1, hm2, rho_from_a0 a1 κ c G ρ1 hκ hc hG hρ1 h1, rho_from_a0 a2 κ c G ρ2 hκ hc hG hρ2 h2]
  field_simp

/-! ## L8: zero Majorana masses ⇒ m_ββ = 0 (definitional) -/

noncomputable def mbb (U : Fin 3 → ℂ) (m : Fin 3 → ℝ) : ℝ := ‖∑ i, U i ^ 2 * (m i : ℂ)‖

theorem dirac_no_0nubb (U : Fin 3 → ℂ) : mbb U (fun _ => 0) = 0 := by
  simp [mbb]

end LeptonChain

#print axioms LeptonChain.tm1_s12_rule
#print axioms LeptonChain.tm1_s12_window
#print axioms LeptonChain.tm2_s12_floor
#print axioms LeptonChain.tm1_octant_decides_delta
#print axioms LeptonChain.tm1_consistent
#print axioms LeptonChain.spectrum_sum_window
#print axioms LeptonChain.mbeta_bound
#print axioms LeptonChain.rho_from_a0
#print axioms LeptonChain.mlight_scaling
#print axioms LeptonChain.dirac_no_0nubb
