import Mathlib

/-! MUTATE for LEPTON_CHAIN: the same file with three FALSE statements. Each must FAIL.
(M1) the octant theorem with s13² < 1/4 in place of 1/5. The statement is FALSE, not just unproved: s13² = 0.22, s23² = 0.6 gives
     a valid TM1 point (c12² = 0.855) with cos δ = −0.026 < 0 in the upper octant.
(M2) the TM1 window's lower edge raised to 0.3190 (the true minimum at s13² = 0.025 is 0.316239).
(M3) the spectrum sum bounded above by 0.0605 eV (the true sum is about 0.0614). -/

namespace LeptonChainMutate
open Complex

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
    (0.3190 : ℝ) ≤ s12 ^ 2 ∧ s12 ^ 2 ≤ 0.3198 := by
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
    (hsmall : s13 ^ 2 < 1 / 4) :
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

/-! ## L5–L6: the mass spectrum -/

theorem spectrum_sum_window (d21 d31 : ℝ) (a1 : (7.38e-5 : ℝ) ≤ d21) (a2 : d21 ≤ 7.62e-5)
    (b1 : (2.49e-3 : ℝ) ≤ d31) (b2 : d31 ≤ 2.56e-3) :
    let m1 : ℝ := 2.24e-3
    (0.0609 : ℝ) < m1 + Real.sqrt (m1 ^ 2 + d21) + Real.sqrt (m1 ^ 2 + d31) ∧
      m1 + Real.sqrt (m1 ^ 2 + d21) + Real.sqrt (m1 ^ 2 + d31) < 0.0605 := by
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

/-! ## L8: Dirac ⇒ no neutrinoless double beta (definitional) -/

noncomputable def mbb (U : Fin 3 → ℂ) (m : Fin 3 → ℝ) : ℝ := ‖∑ i, U i ^ 2 * (m i : ℂ)‖

theorem dirac_no_0nubb (U : Fin 3 → ℂ) : mbb U (fun _ => 0) = 0 := by
  simp [mbb]

end LeptonChainMutate
