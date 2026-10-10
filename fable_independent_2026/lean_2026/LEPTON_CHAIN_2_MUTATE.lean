import Mathlib

/-! MUTATE for LEPTON_CHAIN_2: three FALSE statements. Each must FAIL, and each has a concrete counterexample.
(M4) cos²δ ≤ 0.20 under TM1 on the box. FALSE: the box maximum is 0.2061 (s13² = 0.020, s23² = 0.596; Python scan).
(M5) DESI caps m1 < 0.0040 eV. FALSE: m1 = 4.2 meV with Δm²21 = 7.38e-5, Δm²31 = 2.49e-3 gives Σ = 0.06384 < 0.0642.
(M6) IO Σ ≥ 0.10 eV. FALSE: m3 = 0, Δm²32 = 2.40e-3, Δm²21 = 7.62e-5 gives Σ = 0.0972. -/

namespace LeptonChain2Mutate
open Complex

open Complex

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


/-- t(1 − t) ≥ 0.2407 on [0.43, 0.596]. -/
theorem st_ct_floor (s23 c23 : ℝ) (h23 : s23 ^ 2 + c23 ^ 2 = 1) (t1 : (0.43 : ℝ) ≤ s23 ^ 2) (t2 : s23 ^ 2 ≤ 0.596) :
    (0.2407 : ℝ) ≤ s23 ^ 2 * c23 ^ 2 := by
  have : c23 ^ 2 = 1 - s23 ^ 2 := by linarith
  rw [this]; nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ s23 ^ 2 - 0.43) (by linarith : (0:ℝ) ≤ 0.596 - s23 ^ 2)]

/-- (s12 c12 s13 s23 c23)² ≥ 0.0010355 on the box. -/
theorem X2_floor (s12 c12 s13 c13 s23 c23 : ℝ) (h12 : s12 ^ 2 + c12 ^ 2 = 1) (h13 : s13 ^ 2 + c13 ^ 2 = 1)
    (h23 : s23 ^ 2 + c23 ^ 2 = 1) (htm1 : c12 ^ 2 * c13 ^ 2 = 2 / 3)
    (y1 : (0.020 : ℝ) ≤ s13 ^ 2) (y2 : s13 ^ 2 ≤ 0.025) (t1 : (0.43 : ℝ) ≤ s23 ^ 2) (t2 : s23 ^ 2 ≤ 0.596) :
    (0.0010355 : ℝ) ≤ (s12 * c12 * s13 * s23 * c23) ^ 2 := by
  obtain ⟨w1, w2⟩ := tm1_s12_window s12 c12 s13 c13 h12 h13 htm1 y1 y2
  have hP : (0.21508 : ℝ) ≤ s12 ^ 2 * c12 ^ 2 := by
    have : c12 ^ 2 = 1 - s12 ^ 2 := by linarith
    rw [this]; nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ s12 ^ 2 - 0.3162) (by linarith : (0:ℝ) ≤ 0.3198 - s12 ^ 2)]
  have hT := st_ct_floor s23 c23 h23 t1 t2
  have e : (s12 * c12 * s13 * s23 * c23) ^ 2 = (s12 ^ 2 * c12 ^ 2) * s13 ^ 2 * (s23 ^ 2 * c23 ^ 2) := by ring
  rw [e]
  have h1 : (0.21508 : ℝ) * 0.020 ≤ (s12 ^ 2 * c12 ^ 2) * s13 ^ 2 := mul_le_mul hP y1 (by norm_num) (by positivity)
  have h2 := mul_le_mul h1 hT (by norm_num) (by positivity)
  nlinarith

theorem tm1_cp_large (s12 c12 s13 c13 s23 c23 δ : ℝ)
    (h12 : s12 ^ 2 + c12 ^ 2 = 1) (h13 : s13 ^ 2 + c13 ^ 2 = 1) (h23 : s23 ^ 2 + c23 ^ 2 = 1)
    (htm1 : c12 ^ 2 * c13 ^ 2 = 2 / 3)
    (hmu : Complex.normSq (Umu1 s12 c12 s13 s23 c23 δ) = 1 / 6)
    (htau : Complex.normSq (Utau1 s12 c12 s13 s23 c23 δ) = 1 / 6)
    (y1 : (0.020 : ℝ) ≤ s13 ^ 2) (y2 : s13 ^ 2 ≤ 0.025) (t1 : (0.43 : ℝ) ≤ s23 ^ 2) (t2 : s23 ^ 2 ≤ 0.596) :
    Real.cos δ ^ 2 ≤ 0.20 := by
  have hid := tm1_mu_tau_identity s12 c12 s13 s23 c23 δ hmu htau
  obtain ⟨key, hK⟩ := tm1_K_pos s12 c12 s13 c13 h12 h13 htm1 (by linarith)
  have hKmax : s12 ^ 2 - c12 ^ 2 * s13 ^ 2 ≤ 0.3062 := by
    by_contra h; push Not at h
    have := mul_lt_mul_of_pos_right h (by linarith : (0:ℝ) < 1 - s13 ^ 2)
    nlinarith
  have hD : (s23 ^ 2 - c23 ^ 2) ^ 2 ≤ 0.036864 := by
    have e : c23 ^ 2 = 1 - s23 ^ 2 := by linarith
    rw [e]; nlinarith
  have hX2 := X2_floor s12 c12 s13 c13 s23 c23 h12 h13 h23 htm1 y1 y2 t1 t2
  have hsq : 16 * (s12 * c12 * s13 * s23 * c23) ^ 2 * Real.cos δ ^ 2
      = (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) ^ 2 * (s23 ^ 2 - c23 ^ 2) ^ 2 := by
    calc 16 * (s12 * c12 * s13 * s23 * c23) ^ 2 * Real.cos δ ^ 2
        = (4 * (s12 * c12 * s13 * s23 * c23) * Real.cos δ) ^ 2 := by ring
      _ = ((s12 ^ 2 - c12 ^ 2 * s13 ^ 2) * (s23 ^ 2 - c23 ^ 2)) ^ 2 := by rw [hid]
      _ = _ := by ring
  have hK2 : (s12 ^ 2 - c12 ^ 2 * s13 ^ 2) ^ 2 ≤ 0.3062 ^ 2 := pow_le_pow_left₀ hK.le hKmax 2
  have hKD := mul_le_mul hK2 hD (sq_nonneg _) (by norm_num)
  by_contra h; push Not at h
  have h3 := mul_le_mul_of_nonneg_right hX2 (sq_nonneg (Real.cos δ))
  have h4 : (0.0010355 : ℝ) * 0.21 < 0.0010355 * Real.cos δ ^ 2 := by linarith
  linarith

theorem tm1_jarlskog_floor (s12 c12 s13 c13 s23 c23 δ : ℝ)
    (h12 : s12 ^ 2 + c12 ^ 2 = 1) (h13 : s13 ^ 2 + c13 ^ 2 = 1) (h23 : s23 ^ 2 + c23 ^ 2 = 1)
    (htm1 : c12 ^ 2 * c13 ^ 2 = 2 / 3)
    (hmu : Complex.normSq (Umu1 s12 c12 s13 s23 c23 δ) = 1 / 6)
    (htau : Complex.normSq (Utau1 s12 c12 s13 s23 c23 δ) = 1 / 6)
    (y1 : (0.020 : ℝ) ≤ s13 ^ 2) (y2 : s13 ^ 2 ≤ 0.025) (t1 : (0.43 : ℝ) ≤ s23 ^ 2) (t2 : s23 ^ 2 ≤ 0.596) :
    (0.00077 : ℝ) ≤ (s12 * c12 * s13 * c13 ^ 2 * s23 * c23 * Real.sin δ) ^ 2 := by
  have hc := tm1_cp_large s12 c12 s13 c13 s23 c23 δ h12 h13 h23 htm1 hmu htau y1 y2 t1 t2
  have hs : (0.79 : ℝ) ≤ Real.sin δ ^ 2 := by nlinarith [Real.sin_sq_add_cos_sq δ]
  have hX2 := X2_floor s12 c12 s13 c13 s23 c23 h12 h13 h23 htm1 y1 y2 t1 t2
  have hc4 : (0.950625 : ℝ) ≤ (c13 ^ 2) ^ 2 := by
    have : (0.975 : ℝ) ≤ c13 ^ 2 := by linarith
    nlinarith
  have e : (s12 * c12 * s13 * c13 ^ 2 * s23 * c23 * Real.sin δ) ^ 2
      = (s12 * c12 * s13 * s23 * c23) ^ 2 * (c13 ^ 2) ^ 2 * Real.sin δ ^ 2 := by ring
  rw [e]
  have h1 := mul_le_mul hX2 hc4 (by norm_num) (by positivity)
  have h2 := mul_le_mul h1 hs (by norm_num) (by positivity)
  nlinarith

/-! ## Ordering and absolute mass from DESI -/

theorem io_excluded_by_desi (m3 d21 d32 : ℝ) (hm : 0 ≤ m3) (a : d21 ≤ 7.62e-5) (b : (2.40e-3 : ℝ) ≤ d32) (_c : d21 ≤ d32) :
    (0.10 : ℝ) ≤ m3 + Real.sqrt (m3 ^ 2 + d32) + Real.sqrt (m3 ^ 2 + d32 - d21) := by
  have l2 : (0.0489 : ℝ) < Real.sqrt (m3 ^ 2 + d32) := (Real.lt_sqrt (by norm_num)).mpr (by nlinarith)
  have l1 : (0.0482 : ℝ) < Real.sqrt (m3 ^ 2 + d32 - d21) := (Real.lt_sqrt (by norm_num)).mpr (by nlinarith)
  linarith

theorem io_above_desi : (0.0642 : ℝ) < 0.0970 := by norm_num

theorem desi_caps_m1 (m1 d21 d31 : ℝ) (hm : 0 ≤ m1) (a : (7.38e-5 : ℝ) ≤ d21) (b : (2.49e-3 : ℝ) ≤ d31)
    (hs : m1 + Real.sqrt (m1 ^ 2 + d21) + Real.sqrt (m1 ^ 2 + d31) < 0.0642) : m1 < 0.0040 := by
  by_contra h; push Not at h
  have q : (2.116e-5 : ℝ) ≤ m1 ^ 2 := by nlinarith
  have l2 : (0.00974 : ℝ) < Real.sqrt (m1 ^ 2 + d21) := (Real.lt_sqrt (by norm_num)).mpr (by nlinarith)
  have l3 : (0.05011 : ℝ) < Real.sqrt (m1 ^ 2 + d31) := (Real.lt_sqrt (by norm_num)).mpr (by nlinarith)
  linarith

theorem desi_caps_a0_under_A3 (m1 a0 ac : ℝ) (hm : 0 ≤ m1) (hm1 : m1 < 0.0046) (_ha : 0 < a0) (hc : 0 < ac)
    (hscale : m1 ^ 4 * ac ^ 2 = (2.24e-3 : ℝ) ^ 4 * a0 ^ 2) : a0 < 4.22 * ac := by
  have h4 : m1 ^ 4 < (0.0046 : ℝ) ^ 4 := pow_lt_pow_left₀ hm1 hm (by norm_num)
  by_contra h; push Not at h
  have hsq : (4.22 * ac) ^ 2 ≤ a0 ^ 2 := pow_le_pow_left₀ (by positivity) h 2
  have hac2 : 0 < ac ^ 2 := by positivity
  nlinarith [mul_lt_mul_of_pos_right h4 hac2]

end LeptonChain2Mutate
